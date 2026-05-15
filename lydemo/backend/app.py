from flask import Flask
from flask_cors import CORS

from api_run import run_api

app = Flask(__name__)
CORS(app)

app.register_blueprint(run_api)

@app.route("/api/prompts")
def get_prompts():
    dummy_prompts = [
        {
            "id": "demo-1", 
            "name": "SQL Injection", 
            "code": "import sqlite3\n\ndef get_user(username):\n    conn = sqlite3.connect('users.db')\n    cursor = conn.cursor()\n    # Vulnerable to SQL injection\n    cursor.execute(f\"SELECT * FROM users WHERE username = '{username}'\")\n    return cursor.fetchall()"
        },
        {
            "id": "demo-2", 
            "name": "Command Injection", 
            "code": "import os\n\ndef ping_host(host):\n    # Vulnerable to command injection\n    return os.system(f'ping -c 1 {host}')"
        },
        {
            "id": "demo-3", 
            "name": "Hardcoded Secret", 
            "code": "def connect_to_api():\n    # Vulnerable: Hardcoded credentials\n    api_key = 'sk_live_super_secret_key_12345'\n    return api_key"
        }
    ]
    return {"success": True, "data": dummy_prompts}


@app.route("/")
def home():
    return {
        "success": True,
        "service": "LeBlanc Backend",
        "status": "operational"
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
