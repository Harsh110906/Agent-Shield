from typing import Dict, Any

class MockTool:
    name: str
    
    def execute(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError
