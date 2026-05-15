import json
from datetime import datetime
from flask import Blueprint, jsonify, request
from scanner_pipeline import ScannerPipeline

run_api = Blueprint("run_api", __name__)
pipeline = ScannerPipeline()

@run_api.route("/api/run", methods=["POST"])
def run_scan():
    try:
        payload = request.get_json() or {}
        code = payload.get("code", "")

        if not code:
            return jsonify({"success": False, "data": None, "error": "No code provided"}), 400

        result = pipeline.scan_code(code)

        if not result.get("success"):
            return jsonify({"success": False, "data": None, "error": "Scan failed"}), 400

        findings = result.get("findings", [])
        return jsonify({
            "success": True, 
            "data": {
                "vulnerabilities": findings,
                "total": len(findings)
            }, 
            "error": None
        }), 200

    except Exception as exc:
        return jsonify({
            "success": False,
            "data": None,
            "error": str(exc)
        }), 500
