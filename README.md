# Shadow-AI Detector

Scans proxy/DNS logs for traffic to AI services, compares it to a
**sanctioned-AI allowlist**, and reports unsanctioned (shadow) AI use per
user — plus a repo scanner that finds hardcoded LLM API keys.

## Run
```bash
python detect_shadow_ai.py sample_data/proxy_logs.csv
python scan_repo_for_ai_keys.py .
```

## Output
```
UNSANCTIONED AI USAGE
user      domain              hits  bytes_out
bob       chat.deepseek.com      2     870000
...
```

## Ideas to extend
- Pull logs from Splunk / Sentinel instead of CSV
- Add Azure Resource Graph + boto3 collectors to inventory models/endpoints
- Export a CSV "AI asset register" for Power BI
