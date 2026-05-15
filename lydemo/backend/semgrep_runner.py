import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Tuple

SCAN_TMP_DIR = Path(__file__).resolve().parent / "scan_tmp"
SCAN_TMP_DIR.mkdir(parents=True, exist_ok=True)

SEMGREP_CONFIG = "p/python-security"
SEMGREP_TIMEOUT = 30


class SemgrepExecutionError(Exception):
    pass


class SemgrepRunner:
    def __init__(self) -> None:
        self.binary = shutil.which("semgrep")

    def available(self) -> bool:
        return self.binary is not None

    def scan_code(
        self,
        code: str,
        filename: str = "snippet.py"
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:

        if not self.available():
            return [], {
                "scanner": "semgrep",
                "success": False,
                "error": "semgrep executable not found"
            }

        temp_dir = tempfile.mkdtemp(
            prefix="semgrep_",
            dir=SCAN_TMP_DIR
        )

        target_file = Path(temp_dir) / filename

        try:
            target_file.write_text(code, encoding="utf-8")

            command = [
                self.binary,
                "scan",
                "--config",
                SEMGREP_CONFIG,
                "--json",
                "--quiet",
                "--timeout",
                str(SEMGREP_TIMEOUT),
                str(target_file)
            ]

            process = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=SEMGREP_TIMEOUT + 10
            )

            stdout = process.stdout.strip()
            stderr = process.stderr.strip()

            if not stdout:
                return [], {
                    "scanner": "semgrep",
                    "success": False,
                    "error": stderr or "empty semgrep response"
                }

            try:
                payload = json.loads(stdout)

            except json.JSONDecodeError:
                return [], {
                    "scanner": "semgrep",
                    "success": False,
                    "error": "invalid semgrep json output",
                    "raw_output": stdout[:1000]
                }

            findings = payload.get("results", [])

            return findings, {
                "scanner": "semgrep",
                "success": True,
                "finding_count": len(findings),
                "errors": payload.get("errors", []),
                "stderr": stderr
            }

        except subprocess.TimeoutExpired:
            return [], {
                "scanner": "semgrep",
                "success": False,
                "error": "semgrep timed out"
            }

        except Exception as exc:
            return [], {
                "scanner": "semgrep",
                "success": False,
                "error": str(exc)
            }

        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
