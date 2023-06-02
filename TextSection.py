from promptrix.promptrixTypes import PromptMemory, PromptFunctions, Tokenizer, RenderedPromptSection, Message
from promptrix.PromptSectionBase import PromptSectionBase

class TextSection(PromptSectionBase):
    def __init__(self, text: str, role: str, tokens: int = -1, required: bool = True, separator: str = '\n', text_prefix: str = None):
        super().__init__(tokens, required, separator, text_prefix)
        self.text = text
        self.role = role
        self._length = -1

    async def renderAsMessages(self, memory: PromptMemory, functions: PromptFunctions, tokenizer: Tokenizer, max_tokens: int):
        if self._length < 0:
            self._length = len(tokenizer.encode(self.text))

        return self.return_messages([{'role': self.role, 'content': self.text}], self._length, tokenizer, max_tokens)
