from typing import Any, List, TypeVar, Callable
from abc import ABC, abstractmethod
from dataclasses import dataclass

T = TypeVar('T')

@dataclass
class RenderedPromptSection:
    output: T
    length: int
    tooLong: bool

@dataclass
class Message:
    role: str
    content: T

class PromptMemory(ABC):
    @abstractmethod
    def has(self, key: str) -> bool:
        pass

    @abstractmethod
    def get(self, key: str) -> Any:
        pass

    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass

class PromptFunctions(ABC):
    @abstractmethod
    def has(self, name: str) -> bool:
        pass

    @abstractmethod
    def get(self, name: str) -> Callable:
        pass

    @abstractmethod
    def invoke(self, name: str, memory, functions, tokenizer, args) -> Any:
        pass

class Tokenizer(ABC):
    @abstractmethod
    def decode(self, tokens: List[int]) -> str:
        pass

    @abstractmethod
    def encode(self, text: str) -> List[int]:
        pass

PromptFunction = Callable[['PromptMemory', 'PromptFunctions', 'Tokenizer', T], Any]

class PromptSection(ABC):
    required: bool
    tokens: int

    @abstractmethod
    def renderAsText(self, memory, functions, tokenizer, maxTokens):
        pass

    @abstractmethod
    def renderAsMessages(self, memory, functions, tokenizer, maxTokens):
        pass
