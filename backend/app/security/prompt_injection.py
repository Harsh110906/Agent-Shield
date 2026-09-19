import re
from typing import Dict, Any, List

def detect_prompt_injection(parameters: Dict[str, Any]) -> List[Dict[str, Any]]:
    findings = []
    
    suspicious_patterns = [
        re.compile(r'ignore (all )?previous instructions', re.IGNORECASE),
        re.compile(r'disregard (all )?system (instructions|prompts)', re.IGNORECASE),
        re.compile(r'forget (all )?previous', re.IGNORECASE),
        re.compile(r'override (all )?policies', re.IGNORECASE),
        re.compile(r'you are now', re.IGNORECASE),
        re.compile(r'system prompt', re.IGNORECASE),
        re.compile(r'bypass security', re.IGNORECASE),
    ]

    def scan_string(text: str, path: str):
        for pattern in suspicious_patterns:
            if pattern.search(text):
                findings.append({
                    "type": "PROMPT_INJECTION",
                    "severity": "CRITICAL",
                    "description": f"Detected potential prompt injection pattern in {path}",
                })

    def traverse(obj, path=""):
        if isinstance(obj, str):
            scan_string(obj, path)
        elif isinstance(obj, dict):
            for k, v in obj.items():
                traverse(v, f"{path}.{k}" if path else k)
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                traverse(v, f"{path}[{i}]")

    traverse(parameters)
    return findings
