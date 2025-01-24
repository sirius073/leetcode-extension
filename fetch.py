import os
import cloudscraper
from bs4 import BeautifulSoup
import json
import re
import argparse

def save_test_cases(problem_folder, test_cases):
    """
    Save the test cases in their original format as given in the description.
    """
    named_path = os.path.join(problem_folder, "test_cases_named.json")
    with open(named_path, "w") as named_file:
        json.dump(test_cases, named_file, indent=4)
    print(f"Test cases saved in {named_path}.")

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

def save_problem_and_open(problem_url, file_type):
    """
    Fetch the LeetCode problem, extract details, and save test cases and solution files.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Referer": "https://leetcode.com/",
        }
        scraper = cloudscraper.create_scraper()
        scraper.get("https://leetcode.com")  # Ensure cookies are fetched

        response = scraper.get(problem_url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch the URL. HTTP Status Code: {response.status_code}")
            return

        soup = BeautifulSoup(response.text, "html.parser")
        meta_description = soup.find("meta", attrs={"name": "description"})
        if not meta_description:
            print("Meta description not found on the page.")
            return

        description = meta_description.get("content", "").strip()
        problem_title = "leetcode_problem"
        if "Can you solve this real interview question?" in description:
            problem_title = description.split("?")[1].split("-")[0].strip().replace(" ", "_").replace(":", "").replace("/", "_")

        inputs_outputs = []
        current_input, current_output = None, None
        for line in description.split("\n"):
            line = line.strip()
            if "Input:" in line:
                current_input = line.split("Input:")[1].strip()
            elif "Output:" in line:
                current_output = line.split("Output:")[1].strip()
            if current_input and current_output:
                inputs_outputs.append({"input": current_input, "output": current_output})
                current_input, current_output = None, None

        if not inputs_outputs:
            print("No inputs and outputs found.")
            return

        problem_folder = os.path.join("E:\leetcode", problem_title)
        os.makedirs(problem_folder, exist_ok=True)
        save_test_cases(problem_folder, inputs_outputs)

        solution_file_path = os.path.join(problem_folder, f"solution.{file_type}")
        first_input = inputs_outputs[0]["input"]

        if file_type.lower() == "py":
            python_args = []
            input_pattern = re.findall(r"(\w+)\s*=", first_input)
            python_args.extend(input_pattern)
            with open(solution_file_path, "w") as py_file:
                py_file.write(f"# {problem_url}\n")
                py_file.write("# Return your results for pretests\n\n")
                py_file.write(f"def solution({', '.join(python_args)}):\n")
                py_file.write("    # Write your solution here\n")

        elif file_type.lower() == "cpp":
            cpp_args = set()
            for case in inputs_outputs:
                raw_input = case["input"]
                parsed_args = parse_input_with_type_and_structure(raw_input)
                for arg, (value, python_type) in parsed_args.items():
                    cpp_type = determine_cpp_type(python_type, value)
                    cpp_args.add(f"{cpp_type} &{arg}")
            with open(solution_file_path, "w") as cpp_file:
                cpp_file.write(f"// {problem_url}\n")
                cpp_file.write("// NOTE: Print your results for pretests\n\n")
                cpp_file.write("#include <bits/stdc++.h>\nusing namespace std;\n\n")
                cpp_file.write(f"void solution({', '.join((cpp_args))}) {{\n")
                cpp_file.write("    // Write your solution here\n")
                cpp_file.write("}\n")

        else:
            print("Invalid file type. Use 'cpp' or 'py'.")
            return

        print(f"Solution file created: {solution_file_path}")
        return solution_file_path

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch LeetCode problem and create solution file.")
    parser.add_argument('--url', type=str, required=True, help="LeetCode problem URL")
    parser.add_argument('--file_type', type=str, required=True, choices=['py', 'cpp'], help="Programming language type")
    args = parser.parse_args()

    save_problem_and_open(args.url, args.file_type)
