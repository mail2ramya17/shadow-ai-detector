"""Find hardcoded LLM API keys and AI SDK usage in a code folder."""
import os, re, sys

KEY_PATTERNS = {
    "OpenAI key": r"sk-[A-Za-z0-9_-]{20,}",
    "Anthropic key": r"sk-ant-[A-Za-z0-9_-]{20,}",
    "HuggingFace token": r"hf_[A-Za-z0-9]{30,}",
}
SDK_PATTERNS = r"import (openai|anthropic|boto3)|from (langchain|openai|anthropic)"
SKIP = {".git", "node_modules", ".venv"}

root = sys.argv[1] if len(sys.argv) > 1 else "."
for dirpath, dirs, files in os.walk(root):
    dirs[:] = [d for d in dirs if d not in SKIP]
    for name in files:
        if not name.endswith((".py", ".js", ".ts", ".env", ".json", ".yaml", ".yml")):
            continue
        path = os.path.join(dirpath, name)
        try:
            text = open(path, errors="ignore").read()
        except OSError:
            continue
        for label, pat in KEY_PATTERNS.items():
            for m in re.finditer(pat, text):
                print(f"[SECRET] {label} in {path}: {m.group()[:8]}...")
        if re.search(SDK_PATTERNS, text):
            print(f"[AI-SDK] {path}")
