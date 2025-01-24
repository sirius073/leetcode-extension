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
3. Start flask server in the terminal.
   ```bash
   python app.py
4. The server will run on http://127.0.0.1:5000.

### Usage 
## 1. Running the extension
1. Open a LeetCode problem page in your browser.
2. Click the LeetCode Fetcher extension icon in the Chrome toolbar.
3. Select the desired programming language (cpp or py) when prompted.
4. The test cases and solution file will be generated in the default directory.

## 2. Folder Structure
  The generated files will be organized under a leetcode folder (or a folder name you specify in fetch.py). The structure will look like this:
  /leetcode/
    ├── two-sum/
    │   ├── test_cases_named.json
    │   ├── solution.py
    │   ├── solution.cpp
    ├── test.py
    └── .vscode/
        └── tasks.json

### Testing the solution file
## Prequisites
1. Place test.py (provided in this repository) inside the leetcode folder.
2. Create a .vscode folder inside the leetcode folder and add the provided tasks.json file.

## Running the test
1. Open Visual Studio Code (VS Code).
2. Open the solution file you want to test (e.g., solution.py or solution.cpp).
3. Press Ctrl+Shift+P (or Cmd+Shift+P on Mac) and select Tasks: Run Task.
4. Select Test Current Solution from the task list.
5. The test results will be displayed in the terminal.

### Important notes
1. Folder Setup: Ensure the leetcode folder exists at the specified path. If you change the folder name, update it in fetch.py.
  tasks.json: The tasks.json file is used to configure VS Code to run the test.py script with the selected solution file.
2. Language Selection: When using the extension, ensure you select the correct language (cpp or py).
