LeetCode Fetcher Extension
The LeetCode Fetcher is a Chrome extension designed to simplify the process of fetching test cases and generating solution files for LeetCode problems. With this extension, you can extract test cases directly from a problem page and generate Python (.py) or C++ (.cpp) solution files automatically. Additionally, you can test your solution files using the provided test.py script and VS Code tasks.

Features
Automatically detects the URL of the open LeetCode problem page.
Prompts the user to select the programming language (cpp or py) for the solution file.
Fetches test cases and saves them in a test_cases_named.json file.
Generates a boilerplate solution file in the selected language.
Allows you to test the solution file with predefined test cases using test.py.
Installation
1. Clone or Download the Repository
Clone this repository or download the files to your local machine.

2. Install the Chrome Extension
Open Chrome and navigate to chrome://extensions/.
Enable Developer mode in the top-right corner.
Click Load unpacked and select the folder containing this extension's files.
3. Set Up the API Server
Ensure you have Python installed.
Install the required Python packages:
bash
Copy
Edit
pip install flask cloudscraper beautifulsoup4
Start the Flask API server:
bash
Copy
Edit
python server.py
The server will run on http://127.0.0.1:5000.
Usage
1. Running the Extension
Open a LeetCode problem page in your browser.
Click the LeetCode Fetcher extension icon in the Chrome toolbar.
Select the desired programming language (cpp or py) when prompted.
The test cases and solution file will be generated in the default directory.
2. Folder Structure
The generated files will be organized under a leetcode folder (or a folder name you specify in fetch.py). The structure will look like this:

bash
Copy
Edit
/leetcode/
  ├── two-sum/
  │   ├── test_cases_named.json
  │   ├── solution.py
  │   ├── solution.cpp
  ├── test.py
  └── .vscode/
      └── tasks.json
Testing the Solution File
Prerequisites
Ensure the problem folder is created inside the leetcode folder.
Place test.py (provided in this repository) inside the leetcode folder.
Create a .vscode folder inside the leetcode folder and add the provided tasks.json file.
Running the Test
Open Visual Studio Code (VS Code).
Open the solution file you want to test (e.g., solution.py or solution.cpp).
Press Ctrl+Shift+P (or Cmd+Shift+P on Mac) and select Tasks: Run Task.
Select Test Current Solution from the task list.
The test results will be displayed in the terminal.
Important Notes
Folder Setup: Ensure the leetcode folder exists at the specified path. If you change the folder name, update it in fetch.py.
tasks.json: The tasks.json file is used to configure VS Code to run the test.py script with the selected solution file.
Language Selection: When using the extension, ensure you select the correct language (cpp or py).
Contributing
If you'd like to improve this extension or add new features, feel free to fork the repository and submit a pull request.

This README provides all the necessary information to get started with the LeetCode Fetcher extension.







You said:
convert this into readme.md
ChatGPT said:
ChatGPT
Here's the content formatted for a README.md file:

markdown
Copy
Edit
# LeetCode Fetcher Extension

The **LeetCode Fetcher** is a Chrome extension designed to simplify the process of fetching test cases and generating solution files for LeetCode problems. With this extension, you can extract test cases directly from a problem page and generate Python (`.py`) or C++ (`.cpp`) solution files automatically. Additionally, you can test your solution files using the provided `test.py` script and VS Code tasks.

---

## Features

- Automatically detects the URL of the open LeetCode problem page.
- Prompts the user to select the programming language (`cpp` or `py`) for the solution file.
- Fetches test cases and saves them in a `test_cases_named.json` file.
- Generates a boilerplate solution file in the selected language.
- Allows you to test the solution file with predefined test cases using `test.py`.

---

## Installation

### 1. Clone or Download the Repository
Clone this repository or download the files to your local machine.

### 2. Install the Chrome Extension
1. Open Chrome and navigate to `chrome://extensions/`.
2. Enable **Developer mode** in the top-right corner.
3. Click **Load unpacked** and select the folder containing this extension's files.

### 3. Set Up the API Server
1. Ensure you have Python installed.
2. Install the required Python packages:
   ```bash
   pip install flask cloudscraper beautifulsoup4
Start the Flask API server:
bash
Copy
Edit
python server.py
The server will run on http://127.0.0.1:5000.
Usage
1. Running the Extension
Open a LeetCode problem page in your browser.
Click the LeetCode Fetcher extension icon in the Chrome toolbar.
Select the desired programming language (cpp or py) when prompted.
The test cases and solution file will be generated in the default directory.
2. Folder Structure
The generated files will be organized under a leetcode folder (or a folder name you specify in fetch.py). The structure will look like this:

bash
Copy
Edit
/leetcode/
  ├── two-sum/
  │   ├── test_cases_named.json
  │   ├── solution.py
  │   ├── solution.cpp
  ├── test.py
  └── .vscode/
      └── tasks.json
Testing the Solution File
Prerequisites
Ensure the problem folder is created inside the leetcode folder.
Place test.py (provided in this repository) inside the leetcode folder.
Create a .vscode folder inside the leetcode folder and add the provided tasks.json file.
Running the Test
Open Visual Studio Code (VS Code).
Open the solution file you want to test (e.g., solution.py or solution.cpp).
Press Ctrl+Shift+P (or Cmd+Shift+P on Mac) and select Tasks: Run Task.
Select Test Current Solution from the task list.
The test results will be displayed in the terminal.
Important Notes
Folder Setup: Ensure the leetcode folder exists at the specified path. If you change the folder name, update it in fetch.py.
tasks.json: The tasks.json file is used to configure VS Code to run the test.py script with the selected solution file.
Language Selection: When using the extension, ensure you select the correct language (cpp or py).
