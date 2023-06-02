import asyncio
import VolatileMemory, FunctionRegistry, GPT3Tokenizer
import Prompt, SystemMessage, UserMessage

prompt = Prompt.Prompt([
    SystemMessage.SystemMessage('The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.'),
    UserMessage.UserMessage('{{$input}}')
])

memory = VolatileMemory.VolatileMemory({'input':input()})
functions = FunctionRegistry.FunctionRegistry()
tokenizer = GPT3Tokenizer.GPT3Tokenizer()
max_tokens = 2000

# Render the prompt for a Chat Completion call
async def render_chat_completion():
    memory = VolatileMemory.VolatileMemory({'input':input('chat:')})
    as_messages = await prompt.renderAsMessages(memory, functions, tokenizer, max_tokens)
    if not as_messages.tooLong:
        messages = as_messages.output
        print(messages)

# Render the prompt for a Text Completion call
async def render_text_completion():
    memory = VolatileMemory.VolatileMemory({'input':input('text:')})
    as_text = await prompt.renderAsText(memory, functions, tokenizer, max_tokens)
    if not as_text.tooLong:
        text = as_text.output
        print(text)
# Run the async functions
asyncio.run(render_chat_completion())
asyncio.run(render_text_completion())
