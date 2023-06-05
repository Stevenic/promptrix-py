import json
from typing import Any, Dict

class VolatileMemory:
    def __init__(self, memory: Dict[str, Any] = None):
        self._memory = {}
        if memory:
            self._memory = {key: memory[key] for key in memory}

    def has(self, key: str) -> bool:
        return key in self._memory

    def get(self, key: str) -> Any:
        value = self._memory.get(key)
        if value is not None and isinstance(value, dict):
            return json.loads(json.dumps(value))
        else:
            return value

    def set(self, key: str, value: Any) -> None:
        if value is not None and isinstance(value, dict):
            clone = json.loads(json.dumps(value))
            self._memory[key] = clone
        else:
            self._memory[key] = value

    def delete(self, key: str) -> None:
        if key in self._memory:
            del self._memory[key]

    def clear(self) -> None:
        self._memory.clear()
