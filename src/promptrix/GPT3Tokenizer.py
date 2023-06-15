from typing import List
from transformers import AutoModelForCausalLM, AutoTokenizer, LlamaTokenizer, StoppingCriteria, StoppingCriteriaList, TextIteratorStreamer
import tiktoken
enc = tiktoken.get_encoding("cl100k_base")
assert enc.decode(enc.encode("hello world")) == "hello world"

class GPT3Tokenizer:
    def __init__(self):
        self.ttk = tiktoken.get_encoding("cl100k_base")
        #self.ttk  = tiktoken.encoding_for_model("gpt4")
        
    def decode(self, tokens) -> str:
        return self.ttk.decode(tokens)

    def encode(self, text) -> List[int]:
        return self.ttk.encode(text)
