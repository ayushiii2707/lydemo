from engine_b import scan_code
from llm_client import call_llm


def build_repair_prompt(code: str, findings: list) -> str:
    """Build a structured repair prompt from scanner findings."""
    vuln_lines = []
    for f in findings:
        cwe_ids = f.get("cwe_ids", f.get("cwes", ["unknown"]))
        severity = f.get("severity", "HIGH")
        line = f.get("line", "?")
        message = f.get("message", "No description")
        vuln_lines.append(f"  - {cwe_ids} ({severity}) at line {line}: {message}")

    cwe_list = []
    for f in findings:
        cwe_list.extend(f.get("cwe_ids", f.get("cwes", [])))
    cwe_section = "SECURITY REQUIREMENTS (CWEs relevant to this code): " + ", ".join(set(cwe_list))

    prompt = (
        "The following Python code has security vulnerabilities. Fix ALL of them "
        "and return ONLY the corrected code in a ```python``` block.\n\n"
        + cwe_section + "\n\n"
        + "VULNERABILITIES FOUND:\n"
        + "\n".join(vuln_lines)
        + "\n\nCODE TO FIX:\n```python\n"
        + code
        + "\n```\n\nReturn ONLY the fixed Python code. No explanations."
    )
    return prompt


def repair_loop(code: str, model_name: str = "gemini", max_iterations: int = 3) -> dict:
    """
    Run the repair loop: send vulns to LLM, get patched code, re-scan.
    Returns a list of iteration records and the final code.
    """
    if not code or not code.strip():
        return {"status": "no_code", "iterations": [], "final_code": code}

    iterations = []
    current_code = code

    for i in range(1, max_iterations + 1):
        findings = scan_code(current_code)
        if not findings:
            return {
                "status": "clean",
                "iterations": iterations,
                "final_code": current_code,
            }

        prompt = build_repair_prompt(current_code, findings)
        try:
            response = call_llm(prompt, model_name)
        except Exception as e:
            return {
                "status": "error",
                "iterations": iterations,
                "final_code": current_code,
                "error": str(e),
            }

        # Extract code from response
        import re
        match = re.search(r"```(?:python)?\s*\n(.*?)```", response, re.DOTALL)
        if match:
            patched_code = match.group(1).strip()
        else:
            patched_code = response.strip()

        iterations.append({
            "iteration": i,
            "vulns_before": len(findings),
            "findings": findings,
            "patched_code": patched_code,
        })
        current_code = patched_code

    # Final scan after max iterations
    final_findings = scan_code(current_code)
    for rec in iterations:
        rec["vulns_after"] = len(final_findings)

    return {
        "status": "not_converged" if final_findings else "clean",
        "iterations": iterations,
        "final_code": current_code,
        "final_findings": final_findings,
    }
