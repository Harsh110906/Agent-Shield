import re
from typing import Dict, Any, List

def detect_sensitive_data(parameters: Dict[str, Any]) -> List[Dict[str, Any]]:
    findings = []
    
    # Patterns
    patterns = {
        "api_key": re.compile(r'(?:api[_-]?key|secret|token)[\s:=]+[\'"]?([a-zA-Z0-9\-_]{16,})[\'"]?', re.IGNORECASE),
        "sk_key": re.compile(r'sk-[a-zA-Z0-9]{20,}', re.IGNORECASE),
        "credit_card": re.compile(r'\b(?:\d[ -]*?){13,16}\b'),
        "env_var": re.compile(r'\b[A-Z_]+_KEY\s*=\s*\S+', re.IGNORECASE)
    }

    def scan_string(text: str, path: str):
        for name, pattern in patterns.items():
            if pattern.search(text):
                findings.append({
                    "type": "SENSITIVE_DATA",
                    "severity": "CRITICAL",
                    "description": f"Detected potential {name} in {path}",
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
