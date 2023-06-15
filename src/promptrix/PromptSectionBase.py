from abc import ABC, abstractmethod
from typing import List, Tuple, Any
#from promptrixTypes import Message, PromptFunctions, PromptMemory, PromptSection, RenderedPromptSection
from promptrix.promptrixTypes import  RenderedPromptSection, Message
import promptrix.GPT3Tokenizer as Tokenizer
import traceback

class PromptSectionBase():
    def __init__(self, tokens = -1, required = True, separator = '\n', text_prefix = ''):
        self.required = required
        self.tokens = tokens
        self.separator = separator
        self.text_prefix = text_prefix
        if text_prefix is None:
            raise Exception

    @abstractmethod
    async def renderAsMessages(self, memory, functions, tokenizer, max_tokens):
        pass

    async def renderAsText(self, memory, functions, tokenizer, max_tokens):
        as_messages = await self.renderAsMessages(memory, functions, tokenizer, max_tokens)
        messages = as_messages.output
        text = ''
        for message in messages:
            text += message['content']+'\n'
        #text = self.separator.join([message['content'] for message in messages])
        prefix_length = len(tokenizer.encode(self.text_prefix))
        separator_length = len(tokenizer.encode(self.separator))
        length = prefix_length + as_messages.length + ((len(as_messages.output) - 1) * separator_length)
        text = self.text_prefix + text
        if self.tokens > 1.0 and length > self.tokens:
            encoded = tokenizer.encode(text)
            text = tokenizer.decode(encoded[:self.tokens])
            length = self.tokens
        if text.endswith('\n'):
            text = text[:-1]
        return RenderedPromptSection(output=text, length=length, tooLong=length > max_tokens)

    def return_messages(self, output, length, tokenizer, max_tokens):
        if self.tokens > 1.0:
            while length > self.tokens:
                msg = output.pop()
                encoded = tokenizer.encode(msg['content'])
                length -= len(encoded)
                if length < self.tokens:
                    delta = self.tokens - length
                    truncated = tokenizer.decode(encoded[:delta])
                    role = msg['role'] if type(msg) == dict else msg.role
                    output.append({'role':role, 'content':truncated})
                    length += delta
        return RenderedPromptSection(output=output, length=length, tooLong=length > max_tokens)
