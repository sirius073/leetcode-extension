from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/fetch', methods=['POST'])
def fetch():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid or missing JSON"}), 400

    problem_url = data.get("problem_url")
    file_type = data.get("file_type")

    if not problem_url or not file_type:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # Prepare the command to run the fetch.py script
        command = ['python', 'fetch.py', '--url', problem_url, '--file_type', file_type]

        # Run the fetch.py script
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode != 0:
            return jsonify({"error": "Failed to run the fetch script", "details": result.stderr}), 500

        # Return success message with the generated file path
        return jsonify({
            "message": "Success",
            "problem_url": problem_url,
            "file_type": file_type,
            "output": result.stdout
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
