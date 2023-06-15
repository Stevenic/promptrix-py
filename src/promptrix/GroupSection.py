from typing import List
from promptrix.promptrixTypes import Message, PromptFunctions, PromptMemory, PromptSection, RenderedPromptSection, Tokenizer
from promptrix.PromptSectionBase import PromptSectionBase
from promptrix.LayoutEngine import LayoutEngine

class GroupSection(PromptSectionBase):
    def __init__(self, sections: List[PromptSection], role: str = 'system', tokens: int = -1, required: bool = True, separator: str = '\n\n', textPrefix: str = 'system'):
        super().__init__(tokens, required, separator, textPrefix)
        self._layoutEngine = LayoutEngine(sections, tokens, required, separator)
        self.sections = sections
        self.role = role

    async def renderAsMessages(self, memory: PromptMemory, functions: PromptFunctions, tokenizer: Tokenizer, maxTokens: int):
        # Render sections to text
        renderedPromptSection = await self._layoutEngine.renderAsText(memory, functions, tokenizer, maxTokens)
        output = renderedPromptSection.output
        length = renderedPromptSection.length
        # Return output as a single message
        return self.return_messages([{'role': self.role, 'content': output}], length, tokenizer, maxTokens)
