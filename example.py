import Prompt, SystemMessage, UserMessage

prompt = Prompt.Prompt([
    SystemMessage.SystemMessage('The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.'),
    UserMessage.UserMessage('{{$input}}')
])

print(prompt.getLayoutLength())
