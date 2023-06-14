from typing import List, TypeVar, Optional, Callable, Union
from types import FunctionType
import asyncio

T = TypeVar('T')

class RenderedPromptSection:
    def __init__(self, output: T, length: int, tooLong: bool):
        self.output = output
        self.length = length
        self.tooLong = tooLong

class PromptSectionLayout:
    def __init__(self, section: 'PromptSection', layout = None):
        self.section = section
        self.layout = layout

class PromptSection:
    def __init__(self, sections, tokens: int, required: bool, separator: str):
        self.sections = sections
        self.required = required
        self.tokens = tokens
        self.separator = separator

class LayoutEngine(PromptSection):
    def __init__(self, sections: List[PromptSection], tokens: int, required: bool, separator: str):
        super().__init__(sections, tokens, required, separator)

    async def renderAsText(self, memory, functions, tokenizer, maxTokens):
        layout = []
        self.addSectionsToLayout(self.sections, layout)

        remaining = await self.layoutSections(
            layout,
            maxTokens,
            lambda section: section.renderAsText(memory, functions, tokenizer, maxTokens),
            lambda section, remaining: section.renderAsText(memory, functions, tokenizer, remaining),
            True,
            tokenizer
        )

        output = [section.layout.output for section in layout if section.layout]
        text = self.separator.join(output)
        return RenderedPromptSection(text, len(tokenizer.encode(text)), remaining < 0)

    async def renderAsMessages(self, memory: 'PromptMemory', functions: 'PromptFunctions', tokenizer: 'Tokenizer', maxTokens: int) -> RenderedPromptSection:

        layout = []
        self.addSectionsToLayout(self.sections, layout)

        remaining = await self.layoutSections(
            layout,
            maxTokens,
            lambda section: section.renderAsMessages(memory, functions, tokenizer, maxTokens),
            lambda section, remaining: section.renderAsMessages(memory, functions, tokenizer, remaining)
        )

        output = [message for section in layout if section.layout for message in section.layout.output]
        return RenderedPromptSection(output, self.getLayoutLength(layout), remaining < 0)

    def addSectionsToLayout(self, sections: List[PromptSection], layout: List):
        for section in sections:
            if isinstance(section, LayoutEngine):
                self.addSectionsToLayout(section.sections, layout)
            else:
                layout.append(PromptSectionLayout(section))

    async def layoutSections(self, layout, maxTokens, cbFixed, cbProportional, textLayout=False, tokenizer=None):
        await self.layoutFixedSections(layout, cbFixed)

        remaining = maxTokens - self.getLayoutLength(layout, textLayout, tokenizer)
        while remaining < 0 and self.dropLastOptionalSection(layout):
            remaining = maxTokens - self.getLayoutLength(layout, textLayout, tokenizer)

        if self.needsMoreLayout(layout) and remaining > 0:
            await self.layoutProportionalSections(layout, lambda section: cbProportional(section, remaining))

            remaining = maxTokens - self.getLayoutLength(layout, textLayout, tokenizer)
            while remaining < 0 and self.dropLastOptionalSection(layout):
                remaining = maxTokens - self.getLayoutLength(layout, textLayout, tokenizer)

        return remaining

    async def layoutFixedSections(self, layout, callback):

        async def process_section(section):
            output = await callback(section.section)
            setattr(section, 'layout', output)

        tasks = [process_section(section) for section in layout if section.section.tokens < 0 or section.section.tokens > 1.0]
        await asyncio.gather(*tasks)
        #promises = [callback(section.section).then(lambda output: setattr(section, 'layout', output)) for section in layout if section.section.tokens < 0 or section.section.tokens > 1.0]
        #await asyncio.gather(*promises)

    async def layoutProportionalSections(self, layout, callback):
        async def process_section(section):
            output = await callback(section.section)
            setattr(section, 'layout', output)

        tasks = [process_section(section) for section in layout if 0.0 <= section.section.tokens <= 1.0]
        await asyncio.gather(*tasks)

    def getLayoutLength(self, layout, textLayout=False, tokenizer=None) -> int:
        if textLayout and tokenizer:
            output = [section.layout.output for section in layout if section.layout]
            return len(tokenizer.encode(self.separator.join(output)))
        else:
            return sum(section.layout.length for section in layout if section.layout)

    def dropLastOptionalSection(self, layout) -> bool:
        for i in range(len(layout) - 1, -1, -1):
            if not layout[i].section.required:
                layout.pop(i)
                return True
        return False

    def needsMoreLayout(self, layout) -> bool:
        return any(not section.layout for section in layout)
