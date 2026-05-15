from flask import Flask
from flask_cors import CORS

from api_run import run_api

app = Flask(__name__)
CORS(app)

app.register_blueprint(run_api)

@app.route("/api/prompts")
def get_prompts():
    return {"success": True, "data": []}


@app.route("/")
def home():
    return {
        "success": True,
        "service": "LeBlanc Backend",
        "status": "operational"
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
