# Safe Code Executor — Learning Project

• A secure API that executes untrusted Python code inside Docker containers and safely returns the output.  

• This project demonstrates the real-world risks of running user code and how Docker can be used to apply  basic sandboxing and security limits.

# Project Overview
• The Safe Code Executor is a secure web service that allows users to submit and run untrusted code inside isolated Docker containers.

• It ensures safety, reliability, and resource control while providing a simple API and optional web UI for interacting with the system.

• The project is designed to teach:

• How to run untrusted code safely

• Why resource limits matter

• How Docker isolation works

• How to document and ship a secure mini-application

# Features

• Run Python code via API  

• Execute code inside Docker containers 

• Enforced execution timeout  

• Memory usage limit  

• No internet access inside containers 

• Read-only filesystem option  

• Clear error handling  

• Simple Web UI for testing  

• Fully documented security experiments  

# Execution Flow

1. User submits code → API receives JSON payload

2. API validates:

    • Code size (≤5000 chars)

    • Language (Python/JS)

3. API writes code to a temporary file

4. API runs a Docker container with:

   • No network

   • Memory limit

   • Timeout

   • Read-only filesystem

5. Container executes code

6. API returns:

   • stdout

   • cleaned stderr

   • friendly errors

# Create & Activate Virtual Environment

## 1. Create a Virtual Environment
```
python -m venv venv
```
## 2. Activate the Virtual Environment
```
venv\Scripts\activate
```

# Project Structure
```
safe-code-executor/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── templates/
│ └── index.html
├── README.md
```

# Prerequisites

1. Operating System

2. Docker Desktop

3. Python 3.10

4. pip (Python package manager)

5. Git

6. cURL(Client URL or Uniform Resource Locator)
        
# How It Works

The system works in five simple steps:

## 1. User Sends Python Code
The user sends a POST request to the API:
```
POST /run
{
  "code": "print(2 + 2)"
}
```
Or writes code in the HTML interface and clicks Run.

## 2. Server Saves Code to a Temporary File
The Flask backend receives the code and writes it into:
```
temp/user_code.py
```
This file exists only for the execution and can be deleted afterward.

## 3. Docker Container Executes the Code
The API runs this command:
```
docker run --rm \
  --memory=128m \
  --network=none \
  --read-only \
  -v /path/to/temp:/app \
  python:3.11-slim python /app/user_code.py
```
## 4. Output is Captured

## The API collects:

• Standard output (print statements)

• Standard error (exceptions)

• Timeout errors

• Memory violations

## Example output:
```
{ "output": "4" }
```
## If an error occurs:
```
{ "error": "Execution timed out after 10 seconds" }
```
## 5. Result Sent Back to User

The backend returns a JSON response or displays the result on the HTML page.

The UI shows the output clearly.

# Flask Installation

Flask is the Python framework used to build your API.

## Step 1: Check Python Installation

First, make sure Python is installed:
```
python3 --version
python --version
```
## Step 2: Create a Virtual Environment
```
python -m venv venv
venv\Scripts\activate
```
## Step 3: Install Flask
```
pip install flask
pip3 install flask
```
## Step 4: Verify Flask Installation

Open Python terminal:

Then type:
```
import flask
print(flask.__version__)
```
If no error appears, Flask is installed successfully.

## Step 5: Add Flask to requirements.txt

 Create or update requirements.txt:
```
flask
```
Then install from file:
```
pip install -r requirements.txt
```
## Flask Installation Completed
You can now run your API using:
```
python3 app.py
```

# Step 1: Make It Work

## Run the API
```
python3 app.py
```
![alt text](safe2.png)

![Safe Code Screenshot](images/safe-code-exe-2.png)



## Test the API

## 1) Hello world
```
curl -X POST http://127.0.0.1:5000/run \
  -H "Content-Type: application/json" \
  -d '{"code":"print(\"Hello World\")"}'
```
## What This API Does or Build

• A simple API where users send Python code, and your server runs it inside a Docker container and returns the result.
```
{ "code": "print(2 + 2)" }
```
#  Step 2 — Add Basic Safety

## 1. Infinite loops 
```
curl -X POST http://127.0.0.1:5000/run \
  -H "Content-Type: application/json" \
  -d "{\"code\":\"while True: pass\"}
```
## 2. Memory-heavy attacks  
```
curl -X POST http://127.0.0.1:5000/run \
  -H "Content-Type: application/json" \
  -d "{\"code\":\"x = 'a' * 1000000000\"}"
```
## 3. Internet access inside the container
```
curl -X POST http://127.0.0.1:5000/run \
  -H "Content-Type: application/json" \
  -d "{\"code\":\"import requests\nrequests.get('http://evil.com')\"}"
```

# Step 3 — Docker Security Experiments

## 1.Test: Read /etc/passwd inside container
```
curl -X POST http://127.0.0.1:5000/run \
  -H "Content-Type: application/json" \
  -d "{\"code\":\"print(open('/etc/passwd').read())\"}"
```
## 2.Write test
```
curl -X POST http://127.0.0.1:5000/run \
  -H "Content-Type: application/json" \
  -d "{\"code\":\"open('/app/script.py','w').write('hacked')\"}"
```

# Docker Engine
```
docker ps
```

# Learning Outcomes

1. Understand how Docker isolates and sandboxes untrusted code.

2. Learn what Docker can and cannot protect you from, including limitations    like container escapes.

3. Run untrusted code safely using controlled execution environments.

4. Implement timeout protection to stop infinite loops and long-running        programs.

5. Prevent memory abuse using Docker’s memory limits.

6. Block network access to stop malicious external requests.

7. Support multiple languages (Python + JavaScript) using separate Docker      images.

8. Design a simple web UI with textarea, submit button, and output area.

# Author

Bunny Kukkunoori

GitHub: github.com/bunnykukkunoori-wq

