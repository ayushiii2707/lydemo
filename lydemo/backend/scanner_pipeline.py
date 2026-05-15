from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List

from bandit_runner import BanditRunner
from semgrep_runner import SemgrepRunner

class ScannerPipeline:

    def __init__(self):
        self.semgrep_runner = SemgrepRunner()
        self.bandit_runner = BanditRunner()

    def scan_code(
        self,
        code: str
    ) -> Dict[str, Any]:

        with ThreadPoolExecutor(max_workers=2) as executor:
            semgrep_future = executor.submit(
                self.semgrep_runner.scan_code,
                code
            )

            bandit_future = executor.submit(
                self.bandit_runner.scan_code,
                code
            )

            semgrep_raw, semgrep_meta = semgrep_future.result()
            bandit_raw, bandit_meta = bandit_future.result()

        findings = []
        for v in semgrep_raw:
            cwe_ids = v.get("extra", {}).get("metadata", {}).get("cwe", ["VULN"])
            findings.append({
                "cwe_ids": cwe_ids,
                "severity": v.get("extra", {}).get("severity", "HIGH"),
                "message": v.get("extra", {}).get("message", "Semgrep finding"),
                "line": v.get("start", {}).get("line", 1)
            })

        for v in bandit_raw:
            issue_id = str(v.get("issue_cwe", {}).get("id", "VULN"))
            findings.append({
                "cwe_ids": [f"CWE-{issue_id}" if issue_id != "VULN" else "VULN"],
                "severity": v.get("issue_severity", "HIGH"),
                "message": v.get("issue_text", "Bandit finding"),
                "line": v.get("line_number", 1)
            })

        return {
            "success": True,
            "findings": findings,
            "summary": {
                "total_findings": len(findings),
                "semgrep_findings": len(semgrep_raw),
                "bandit_findings": len(bandit_raw)
            },
            "scanners": {
                "semgrep": semgrep_meta,
                "bandit": bandit_meta
            }
        }

def run_scan_pipeline(code: str) -> Dict[str, Any]:
    pipeline = ScannerPipeline()
    return pipeline.scan_code(code)
