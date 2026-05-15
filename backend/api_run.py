from flask import Blueprint, request, jsonify
from scanner_pipeline import run_scan_pipeline

run_api = Blueprint("run_api", __name__)

@run_api.route("/api/run", methods=["POST"])
@run_api.route("/api/compare", methods=["POST"])
def run_pipeline():
    try:
        data = request.get_json()
        code = data.get("code", data.get("prompt", ""))

        if not code:
            return jsonify({
                "success": False,
                "data": None,
                "error": "No code provided"
            }), 400

        result = run_scan_pipeline(code)

        # To keep frontend working, we should actually return the structure it expects
        # BUT the user said "Rewrite api_run.py so it ONLY calls the real pipeline"
        # and "Return: { success: true, data: result, error: None }"
        # I'll stick to the required data: result format but keep the /api/compare route
        
        return jsonify({
            "success": True,
            "data": result,
            "error": None
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "data": None,
            "error": str(e)
        }), 500
