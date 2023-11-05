import unittest
from promptrix.ConversationHistory import ConversationHistory
from promptrix.VolatileMemory import VolatileMemory
from promptrix.FunctionRegistry import FunctionRegistry
from promptrix.GPT3Tokenizer import GPT3Tokenizer

class TestConversationHistory(unittest.TestCase):
    def setUp(self):
        self.memory = VolatileMemory({
            "history": [
                { "role": "user", "content": "Hello" },
                { "role": "assistant", "content": "Hi" },
            ],
            "longHistory": [
                { "role": "user", "content": "Hello" },
                { "role": "assistant", "content": "Hi! How can I help you?" },
                { "role": "user", "content": "I'd like to book a flight" },
                { "role": "assistant", "content": "Sure, where would you like to go?" },
            ]
        })
        self.functions = FunctionRegistry()
        self.tokenizer = GPT3Tokenizer()

    def test_constructor(self):
        section = ConversationHistory('history')
        self.assertEqual(section.variable, 'history')
        self.assertEqual(section.tokens, 1.0)
        self.assertEqual(section.required, False)
        self.assertEqual(section.separator, "\n")
        self.assertEqual(section.userPrefix, "user")
        self.assertEqual(section.assistantPrefix, "assistant")
        self.assertEqual(section.text_prefix, "")

    def test_renderAsMessages(self):
        section = ConversationHistory('history', 100)
        rendered = section.renderAsMessages(self.memory, self.functions, self.tokenizer, 100)
        self.assertEqual(rendered.output, [
            { "role": "user", "content": "Hello" },
            { "role": "assistant", "content": "Hi" },
        ])
        self.assertEqual(rendered.length, 2)
        self.assertEqual(rendered.tooLong, False)

    # Add other test cases...

if __name__ == '__main__':
    unittest.main()
