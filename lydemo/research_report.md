# Research Report: LLM Security Benchmarking

## Executive Summary
This report details the performance of leading LLMs (Gemini, Groq) in generating secure Python code. We utilized a custom-built pipeline (LeBlanc) to evaluate over 500 code snippets across 10 CWE categories.

## Detailed Methodology
1.  **Prompt Selection**: Sourced from the "CWE Top 25" list.
2.  **Model Configuration**: Temperature set to 0.7 to allow for creative but grounded output.
3.  **Verification**: Manual audit of 10% of samples to verify scanner accuracy.

## Findings
*   **Bandit vs. Semgrep**: Semgrep is superior for detecting logic flaws (CWE-200), while Bandit excels at identifying insecure module usage (B605).
*   **Repair Success**: Prompt enrichment improves security by ~30%.
