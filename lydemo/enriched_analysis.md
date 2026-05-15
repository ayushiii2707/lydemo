# Enriched Security Analysis
**Date**: 2026-05-15
**Version**: 2.1

## Metric Breakdown
| Category | Gemini Score | Groq Score | Status |
| :--- | :--- | :--- | :--- |
| Injection | 0.82 | 0.71 | Gemini Lead |
| Authentication | 0.77 | 0.79 | Groq Lead |
| Cryptography | 0.91 | 0.88 | Gemini Lead |
| File I/O | 0.65 | 0.62 | Critical |

## Analysis of "Vulnerability Drift"
As the complexity of the generated code increases (Line Count > 50), both models show a significant drop in security adherence. This suggests that LLMs "forget" security constraints during large-scale refactoring tasks.
