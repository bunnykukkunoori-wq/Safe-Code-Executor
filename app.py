from flask import Flask, request, jsonify, render_template
import subprocess
import tempfile
import os

app = Flask(__name__)

MAX_CODE_SIZE = 5000  # Max characters allowed


# ✅ Home Page (Web UI)
@app.route("/")
def home():
    return render_template("index.html")


# ✅ API to Run Code
@app.route("/run", methods=["POST"])
def run_code():
    data = request.get_json()

    if not data or "code" not in data:
        return jsonify({"output": "No code provided"}), 400

    code = data["code"]

    # ✅ Limit code length
    if len(code) > MAX_CODE_SIZE:
        return jsonify({"output": "Error: Code too long (max 5000 characters)"}), 400

    # ✅ Write code to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as f:
        f.write(code.encode())
        filename = f.name

    try:
        command = [
            "docker", "run", "--rm",
            "--memory=128m",
            "--cpus=1",
            "--network", "none",
            "--read-only",
            "--pids-limit", "64",
            "-v", f"{filename}:/app/code.py:ro",
            "python:3.11-slim",
            "python", "/app/code.py"
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=10
        )

        # ✅ Detect Out-of-Memory
        if result.returncode == 137:
            return jsonify({"output": "Error: Out of memory (128MB limit)"}), 400

        # ✅ Return Python errors
        if result.stderr:
            return jsonify({"output": result.stderr.strip()}), 400

        # ✅ Return Successful Output
        return jsonify({"output": result.stdout.strip()})

    except subprocess.TimeoutExpired:
        return jsonify({"output": "Error: Execution timed out after 10 seconds"}), 400

    except Exception as e:
        return jsonify({"output": str(e)}), 500

    finally:
        try:
            os.remove(filename)
        except:
            pass


if __name__ == "__main__":
    app.run(debug=True)