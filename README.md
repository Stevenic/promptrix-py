# promptrix-py
Promptrix is a prompt layout engine for Large Language Models.

# Here is a first trivial example:

    from promptrix import promptrixTypes, VolatileMemory, FunctionRegistry, GPT3Tokenizer
    from promptrix.Prompt import Prompt
    from promptrix.SystemMessage import SystemMessage
    from promptrix.UserMessage import UserMessage
    from promptrix.AssistantMessage import AssistantMessage
    from promptrix.ConversationHistory import ConversationHistory

    functions = FunctionRegistry()
    tokenizer = GPT3Tokenizer()
    memory = VolatileMemory({'input':'', 'history':[]})
    max_tokens = 2000

    prompt_text = 'You are helpful, creative, clever, and very friendly. '
    PROMPT = Prompt([
        UserMessage(prompt_text),
        ConversationHistory('history', .5),    # allow history to use up 1/2 the remaining token budget left after the prompt and input 
        UserMessage('{{$input}}')
    ])

    async def render_messages_completion():
        as_msgs = await PROMPT.renderAsMessages(memory, functions, tokenizer, max_tokens)
        msgs = []
        if not as_msgs.tooLong:
            msgs = as_msgs.output
        return msgs

    ### basic chat loop
    while True:
        query = input('Hi, how can I help you?)
        memory.set('input', query)
        msgs = asyncio.run(render_messages_completion())
        response = ... your favorite llm api (model, msgs, ...)
        print(response)
        history = memory.get('history')
        history.append({'role':USER_PREFIX, 'content': query})
        history.append({'role': ASSISTANT_PREFIX, 'content': response})
        memory.set('history', history)
 
