from bandit_runner import run_bandit
from semgrep_runner import run_semgrep

def run_scan_pipeline(code: str):
    results = []

    try:
        bandit_results = run_bandit(code)
        if bandit_results:
            results.extend(bandit_results)
    except Exception as e:
        print("Bandit error:", e)

    try:
        semgrep_results = run_semgrep(code)
        if semgrep_results:
            results.extend(semgrep_results)
    except Exception as e:
        print("Semgrep error:", e)

    return {
        "vulnerabilities": results,
        "total": len(results)
    }
