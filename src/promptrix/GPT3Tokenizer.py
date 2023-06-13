from typing import List
from transformers import AutoModelForCausalLM, AutoTokenizer, LlamaTokenizer, StoppingCriteria, StoppingCriteriaList, TextIteratorStreamer
import tiktoken
enc = tiktoken.get_encoding("cl100k_base")
assert enc.decode(enc.encode("hello world")) == "hello world"

class GPT3Tokenizer:
    def __init__(self):
        self.ttk = tiktoken.get_encoding("cl100k_base")
        #self.ttk  = tiktoken.encoding_for_model("gpt-3.5", disallowed_special=())
        
    def decode(self, tokens) -> str:
        return self.ttk.decode(tokens, disallowed_special=())

    def encode(self, text) -> List[int]:
        return self.ttk.encode(text, disallowed_special=())
