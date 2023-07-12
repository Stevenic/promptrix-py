from promptrix.promptrixTypes import Message, PromptFunctions, PromptMemory, RenderedPromptSection, Tokenizer
from promptrix.PromptSectionBase import PromptSectionBase
from promptrix.Utilities import Utilities

class ConversationHistory(PromptSectionBase):
    def __init__(self, variable, tokens=1.0, required=False, userPrefix='user', assistantPrefix='assistant', separator='\n'):
        super().__init__(tokens, required, separator)
        self.variable = variable
        self.userPrefix = userPrefix
        self.assistantPrefix = assistantPrefix

    def renderAsText(self, memory, functions, tokenizer, maxTokens):
        history = memory.get(self.variable)
        if history is None: history=[]
        tokens = 0
        budget = min(self.tokens, maxTokens) if self.tokens > 1.0 else maxTokens
        separatorLength = len(tokenizer.encode(self.separator))
        lines = []
        for i in range(len(history)-1, -1, -1):
            msg = history[i]
            message = Utilities.to_string(tokenizer, msg['content'])
            prefix = self.userPrefix if msg['role'] == 'user' else self.assistantPrefix
            line = prefix + message.content
            length = len(tokenizer.encode(line)) + (separatorLength if len(lines) > 0 else 0)
            if len(lines) == 0 and self.required:
                tokens += length
                lines.insert(0, line)
                continue
            if tokens + length > budget:
                break
            tokens += length
            lines.insert(0, line)
        return RenderedPromptSection(output=self.separator.join(lines), length=tokens, tooLong=tokens > maxTokens)

    def renderAsMessages(self, memory, functions, tokenizer, maxTokens):
        history = memory.get(self.variable)
        if history is None: history = []
        tokens = 0
        budget = min(self.tokens, maxTokens) if self.tokens > 1.0 else maxTokens
        messages = []
        for i in range(len(history)-1, -1, -1):
            msg = history[i]
            message = {'role':msg['role'], 'content':Utilities.to_string(tokenizer, msg['content'])}
            length = len(tokenizer.encode(message['content']))
            if len(messages) == 0 and self.required:
                tokens += length
                messages.insert(0, message)
                continue
            if tokens + length > budget:
                break
            tokens += length
            messages.insert(0, message)
        
        return RenderedPromptSection(output=messages, length=tokens, tooLong=tokens > maxTokens)
