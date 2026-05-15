# Step 7: Validation Results

## Automated Repair Benchmarks
*   **Initial Vulnerabilities**: 142
*   **Repaired (Automated)**: 98
*   **Failed Repair**: 44
*   **Success Rate**: 69%

## Top Performing Categories (Repair)
1.  **SQL Injection**: 85% success.
2.  **Insecure Randomness**: 92% success.
3.  **Hardcoded Credentials**: 100% success.

## Failure Analysis
Repairs often fail when the security fix conflicts with the intended logic of the function (e.g., changing `os.system` to `subprocess.run` breaks custom piping logic).
