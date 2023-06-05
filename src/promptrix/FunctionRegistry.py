from typing import Callable, Dict, List, Any, Optional

class FunctionRegistry:
    """
    Registry of functions that can be invoked from a prompt template.
    """
    def __init__(self, functions: Optional[Dict[str, Callable]] = None):
        """
        Creates a new 'FunctionRegistry' instance.
        :param functions: Optional. Functions to add to this registry.
        """
        self._functions = {}
        if functions:
            for key, value in functions.items():
                self._functions[key] = value

    def has(self, name: str) -> bool:
        return name in self._functions

    def get(self, name: str) -> Callable:
        fn = self._functions.get(name)
        if not fn:
            raise Exception(f"Function {name} not found.")
        return fn

    def addFunction(self, name: str, value: Callable) -> None:
        if self.has(name):
            raise Exception(f"Function '{name}' already exists.")
        self._functions[name] = value

    def invoke(self, key: str, memory: Any, functions: Any, tokenizer: Any, args: List[str]) -> Any:
        fn = self.get(key)
        return fn(memory, functions, tokenizer, args)
