import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Tuple

SCAN_TMP_DIR = Path(__file__).resolve().parent / "scan_tmp"
SCAN_TMP_DIR.mkdir(parents=True, exist_ok=True)

BANDIT_TIMEOUT = 30


class BanditRunner:
    def __init__(self) -> None:
        self.binary = shutil.which("bandit")

    def available(self) -> bool:
        return self.binary is not None

    def scan_code(
        self,
        code: str,
        filename: str = "snippet.py"
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:

        if not self.available():
            return [], {
                "scanner": "bandit",
                "success": False,
                "error": "bandit executable not found"
            }

        temp_dir = tempfile.mkdtemp(
            prefix="bandit_",
            dir=SCAN_TMP_DIR
        )

        target_file = Path(temp_dir) / filename

        try:
            target_file.write_text(code, encoding="utf-8")

            command = [
                self.binary,
                "-r",
                str(target_file),
                "-f",
                "json",
                "-q"
            ]

            process = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=BANDIT_TIMEOUT
            )

            stdout = process.stdout.strip()
            stderr = process.stderr.strip()

            if not stdout:
                return [], {
                    "scanner": "bandit",
                    "success": False,
                    "error": stderr or "empty bandit response"
                }

            try:
                payload = json.loads(stdout)

            except json.JSONDecodeError:
                return [], {
                    "scanner": "bandit",
                    "success": False,
                    "error": "invalid bandit json output",
                    "raw_output": stdout[:1000]
                }

            findings = payload.get("results", [])

            return findings, {
                "scanner": "bandit",
                "success": True,
                "finding_count": len(findings),
                "metrics": payload.get("metrics", {}),
                "stderr": stderr
            }

        except subprocess.TimeoutExpired:
            return [], {
                "scanner": "bandit",
                "success": False,
                "error": "bandit timed out"
            }

        except Exception as exc:
            return [], {
                "scanner": "bandit",
                "success": False,
                "error": str(exc)
            }

        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
