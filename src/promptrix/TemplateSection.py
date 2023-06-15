#from promptrixTypes import *
from promptrix.PromptSectionBase import PromptSectionBase
from promptrix.Utilities import Utilities
from typing import List, Callable, Any
from enum import Enum
import asyncio

def get_mem_str(memory, value):
    #print (f'***** TemplateSection create_variable_renderer memory {memory}, value {value}')
    return value

class ParseState(Enum):
    IN_TEXT = 1
    IN_PARAMETER = 2
    IN_STRING = 3

class TemplateSection(PromptSectionBase):
    def __init__(self, template, role, tokens = -1, required = True, separator='\n', text_prefix = ''):
        super().__init__(tokens, required, separator, text_prefix)
        self.template = template
        self.role = role
        self._parts = []
        self.parse_template()
    
    async def renderAsMessages(self, memory: 'PromptMemory', functions: 'PromptFunctions', tokenizer: 'Tokenizer', max_tokens: int) -> 'RenderedPromptSection[List[Message]]':
        #print(f'***** TemplateSection entry {self._parts}')
        rendered_parts = [part(memory, functions, tokenizer, max_tokens) for part in self._parts]
        text = ''.join(rendered_parts)
        #print(f'***** TemplateSection rendered parts {rendered_parts}')
        length = len(tokenizer.encode(text))
        return self.return_messages([{'role': self.role, 'content': text}], length, tokenizer, max_tokens)

    """
    async def renderAsMessages(self, memory: 'PromptMemory', functions: 'PromptFunctions', tokenizer: 'Tokenizer', max_tokens: int) -> 'RenderedPromptSection[List[Message]]':
        rendered_parts = await asyncio.gather(*(part(memory, functions, tokenizer, max_tokens) for part in self._parts))
        text = ''.join(rendered_parts)
        length = len(tokenizer.encode(text))
        return self.return_messages([{'role': self.role, 'content': text}], length, tokenizer, max_tokens)
    """
    def parse_template(self):
        part = ''
        state = ParseState.IN_TEXT
        string_delim = ''
        skip_next = False
        for i in range(len(self.template)):
            if skip_next:
                skip_next = False
                continue
            char = self.template[i]
            if state == ParseState.IN_TEXT:
                if char == '{' and self.template[i + 1] == '{':
                    if len(part) > 0:
                        self._parts.append(self.create_text_renderer(part))
                        part = ''
                    state = ParseState.IN_PARAMETER
                    skip_next = True
                else:
                    part += char
            elif state == ParseState.IN_PARAMETER:
                if char == '}' and self.template[i + 1] == '}':
                    if len(part) > 0:
                        if part[0] == '$':
                            self._parts.append(self.create_variable_renderer(part[1:]))
                        else:
                            self._parts.append(self.create_function_renderer(part))
                        part = ''
                    state = ParseState.IN_TEXT
                    skip_next = True
                elif char in ["'", '"', '`']:
                    string_delim = char
                    state = ParseState.IN_STRING
                    part += char
                else:
                    part += char
            elif state == ParseState.IN_STRING:
                part += char
                if char == string_delim:
                    state = ParseState.IN_PARAMETER
        if state != ParseState.IN_TEXT:
            raise ValueError(f"Invalid template: {self.template}")
        if len(part) > 0:
            self._parts.append(self.create_text_renderer(part))
        
        
    def create_text_renderer(self, text: str) -> Callable[['PromptMemory', 'PromptFunctions', 'Tokenizer', int], 'Promise[str]']:
        return lambda memory, functions, tokenizer, max_tokens: text

    def create_variable_renderer(self, name: str) -> Callable[['PromptMemory', 'PromptFunctions', 'Tokenizer', int], 'Promise[str]']:
        #print (f'***** TemplateSection create_variable_renderer name {name}')
        return lambda memory, functions, tokenizer, max_tokens: get_mem_str(memory, Utilities.to_string(tokenizer, memory.get(name)))
 
    def create_function_renderer(self, param: str) -> Callable[['PromptMemory', 'PromptFunctions', 'Tokenizer', int], 'Promise[str]']:
        name = None
        args = []
        part = ''
        def save_part():
            nonlocal part, name, args
            if len(part) > 0:
                if not name:
                    name = part
                else:
                    args.append(part)
            part = ''

        state = ParseState.IN_TEXT
        string_delim = ''
        for i in range(len(param)):
            char = param[i]
            if state == ParseState.IN_TEXT:
                if char in ["'", '"', '`']:
                    save_part()
                    string_delim = char
                    state = ParseState.IN_STRING
                elif char == ' ':
                    save_part()
                else:
                    part += char
            elif state == ParseState.IN_STRING:
                if char == string_delim:
                    save_part()
                    state = ParseState.IN_TEXT
                else:
                    part += char
        save_part()
        
        #def renderer(memory, functions, tokenizer, max_tokens):
        #    value = await functions.invoke(name, memory, functions, tokenizer, args)
        #    return Utilities.to_string(tokenizer, value)

        return lambda memory, functions, tokenizer, max_tokens: Utilities.to_string(tokenizer, functions.invoke(name, memory, functions, tokenizer, args))

