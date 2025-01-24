import os
import subprocess
import json
import re
import importlib.util
import sys
import cloudscraper
from bs4 import BeautifulSoup

def compile_cpp_solution(solution_file_path):
    try:
        executable_path = solution_file_path.replace(".cpp", "")
        subprocess.run(["g++", "-std=c++20", "-w", "-o", executable_path, solution_file_path], check=True)
        return executable_path
    except subprocess.CalledProcessError as e:
        print(f"Compilation failed: {e}")
        return None

def determine_cpp_type(python_type, value):
    """
    Map Python types to equivalent C++ types.
    """
    if python_type == "int":
        return "int"
    elif python_type == "float":
        return "double"
    elif python_type == "string":
        return "string"
    elif python_type == "bool":
        return "bool"
    elif python_type == "list":
        if all(isinstance(item, int) for item in value):
            return "vector<int>"
        elif all(isinstance(item, (int, float)) for item in value):
            return "vector<double>"
        elif all(isinstance(item, bool) for item in value):
            return "vector<bool>"
        else:
            return "vector<auto>"
    elif python_type == "vector of vectors":
        inner_type = determine_cpp_type("list", value[0])  # Assume homogeneous lists
        return f"vector<{inner_type}>"
    else:
        return "auto"

def parse_input_with_type_and_structure(input_string):
    """
    Parse the input string into a dictionary of variable names and their Python values,
    determine the type of each variable, and identify structures like 'vector of vectors'.
    """
    variables = {}
    pattern = r'(\w+)\s*=\s*(.+)'
    matches = re.finditer(pattern, input_string)
    for match in matches:
        var, value = match.groups()
        try:
            if value.startswith("[") and value.endswith("]"):
                parsed_value = json.loads(value)
                if isinstance(parsed_value, list) and all(isinstance(item, list) for item in parsed_value):
                    value_type = "vector of vectors"
                else:
                    value_type = "list"
            elif value.startswith('"') or value.startswith("'"):
                parsed_value = value.strip('"').strip("'")
                value_type = "string"
            elif value.isdigit():
                parsed_value = int(value)
                value_type = "int"
            elif re.match(r"^\d+\.\d+$", value):
                parsed_value = float(value)
                value_type = "float"
            else:
                parsed_value = eval(value)
                value_type = type(parsed_value).__name__
            variables[var] = (parsed_value, value_type)
        except Exception as e:
            print(f"Error parsing value for variable '{var}': {e}")
            raise ValueError(f"Invalid value for variable '{var}'")
    return variables

def generate_cpp_code(parsed_input, test_case_idx):
    """
    Generate C++ code for test cases.
    """
    cpp_code = ""
    
    if test_case_idx == 1:
        cpp_code += "// Declare and initialize variables\n"
        for var_name, (var_value, value_type) in parsed_input.items():
            # Determine the C++ type based on the value
            cpp_type = determine_cpp_type(value_type, var_value)
            
            if isinstance(var_value, list):
                cpp_code += f"{cpp_type} {var_name} = {python_list_to_cpp_vector(var_value)};\n"
            elif isinstance(var_value, str):
                cpp_code += f'{cpp_type} {var_name} = "{var_value}";\n'
            elif isinstance(var_value, (int, float)):
                cpp_code += f"{cpp_type} {var_name} = {var_value};\n"
        cpp_code += "solution(" + ", ".join(parsed_input.keys()) + ");\n"
        cpp_code += 'cout << endl;\n\n'
    else:
        cpp_code += f"// Test Case {test_case_idx}\n"
        for var_name, (var_value, value_type) in parsed_input.items():
            cpp_type = determine_cpp_type(value_type, var_value)

            if isinstance(var_value, list):
                cpp_code += f"{var_name} = {python_list_to_cpp_vector(var_value)};\n"
            elif isinstance(var_value, str):
                cpp_code += f'{var_name} = "{var_value}";\n'
            elif isinstance(var_value, (int, float)):
                cpp_code += f"{var_name} = {var_value};\n"
        cpp_code += "solution(" + ", ".join(parsed_input.keys()) + ");\n"
        cpp_code += 'cout << endl;\n\n'

    return cpp_code

def python_list_to_cpp_vector(py_list):
    """
    Convert a Python list (including nested lists) into C++ vector syntax.
    """
    if isinstance(py_list, list):
        return "{" + ", ".join(python_list_to_cpp_vector(item) for item in py_list) + "}"
    elif isinstance(py_list, str):
        return f'"{py_list}"'
    else:
        return str(py_list)

def inject_test_case_code(solution_file_path, test_case_code):
    """
    Inject test case code into the C++ solution file.
    """
    with open(solution_file_path, "r") as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines):
        if "return 0;" in line:
            lines.insert(i, test_case_code)
            break
    
    with open(solution_file_path, "w") as f:
        f.writelines(lines)

def run_cpp_solution(executable_path):
    try:
        process = subprocess.run([executable_path], text=True, capture_output=True, check=True)
        return process.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing solution: {e}")
        return None

def restore_cpp_solution(solution_file_path):
    """
    Restore the C++ solution file by removing the injected code.
    """
    with open(solution_file_path, "r") as f:
        lines = f.readlines()

    lines = [line for line in lines if "// Auto-generated test case code" not in line]

    with open(solution_file_path, "w") as f:
        f.writelines(lines)

def test_cpp_solution(solution_file_path):
    problem_folder = os.path.dirname(solution_file_path)
    test_cases_path = os.path.join(problem_folder, "test_cases_named.json")
    try:
        with open(test_cases_path, "r") as file:
            test_cases = json.load(file)
    except Exception as e:
        print(f"Error reading test cases: {e}")
        return

    test_case_code = ""
    for idx, case in enumerate(test_cases, start=1):
        inputs = case["input"]
        expected_output = case["output"]

        try:
            parsed_input = parse_input_with_type_and_structure(inputs)
            test_case_code += generate_cpp_code(parsed_input, idx)
        except Exception as e:
            print(f"Error parsing or generating code for test case {idx}: {e}")
            return

    try:
        with open(solution_file_path, "r") as file:
            original_code = file.read()

        main_injection = f"""
int main() {{
{test_case_code}
    return 0;
}}
"""
        with open(solution_file_path, "w") as file:
            file.write(original_code)
            file.write(main_injection)

    except Exception as e:
        print(f"Error writing test cases to solution file: {e}")
        return

    executable_path = compile_cpp_solution(solution_file_path)
    if not executable_path:
        print("Failed to compile the solution.")
        return

    print("Compiled successfully. Running test cases...\n")
    try:
        process = subprocess.run([executable_path], text=True, capture_output=True, check=True)
        cpp_output = process.stdout.strip()

        print("Your Output:")
        print(cpp_output)

        print("Expected Output:")
        for idx, case in enumerate(test_cases, start=1):
            expected_output = case["output"]
            print(f"{expected_output}")

    except Exception as e:
        print(f"Error executing solution: {e}")
        return

    try:
        with open(solution_file_path, "r") as file:
            solution_code = file.read()

        start = solution_code.find("int main()")
        if start != -1:
            open_brace_index = solution_code.find("{", start)
            close_brace_index = solution_code.find("}", open_brace_index)

            if open_brace_index != -1 and close_brace_index != -1:
                brace_depth = 0
                for i in range(open_brace_index, len(solution_code)):
                    if solution_code[i] == "{":
                        brace_depth += 1
                    elif solution_code[i] == "}":
                        brace_depth -= 1
                        if brace_depth == 0:
                            close_brace_index = i
                            break

                solution_code = solution_code[:start] + solution_code[close_brace_index + 1:]

                with open(solution_file_path, "w") as file:
                    file.write(solution_code)

            else:
                print("Couldn't find a matching brace for main function.")
        else:
            print("Main function not found.")

    except Exception as e:
        print(f"Error removing the main function: {e}")

def load_solution_function(solution_file_path):
    try:
        spec = importlib.util.spec_from_file_location("solution", solution_file_path)
        solution_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(solution_module)
        return solution_module.solution
    except Exception as e:
        print(f"Error loading solution: {e}")
        return None

def test_python_solution(solution_file_path):
    problem_folder = os.path.dirname(solution_file_path)
    test_cases_path = os.path.join(problem_folder, "test_cases_named.json")
    solution_function = load_solution_function(solution_file_path)
    if not solution_function:
        print("Solution function not found.")
        return
    try:
        with open(test_cases_path, "r") as file:
            test_cases = json.load(file)
            
        print("Your Output:")
        for idx, case in enumerate(test_cases, start=1):
            inputs = case["input"]
            args = eval(f"dict({inputs})")
            try:
                actual_output = solution_function(**args)
                print(f"{actual_output}")
            except Exception as e:
                print(f"Error executing test case {idx}: {e}")
        
        print("Expected Output:")
        for idx, case in enumerate(test_cases, start=1):
            expected_output = case["output"]
            try:
                print(f"{expected_output}")
            except Exception as e:
                print(f"Error executing test case {idx}: {e}")
    except Exception as e:
        print(f"Error reading test cases: {e}")
        
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_script.py <solution_file_path>")
        sys.exit(1)

    solution_file_path = sys.argv[1]
    language = solution_file_path.split(".")[-1].lower()

    if language == "py":
        test_python_solution(solution_file_path)
    elif language == "cpp":
        test_cpp_solution(solution_file_path)
    else:
        print("Unsupported language. Please use a Python (.py) or C++ (.cpp) file.")