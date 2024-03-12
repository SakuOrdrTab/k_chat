import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import re

class Phi2_api():
    def __init__(self):
        torch.set_default_device("cuda")
        # Introduce rudimentary context memory. Currently the context does not shrink, so the prompts to the model get big very soon. The list structure should be made into a queue
        self._context_memory = "conversation history:\n"
        # init MS phi-2
        self.model = AutoModelForCausalLM.from_pretrained("microsoft/phi-2", torch_dtype="auto", trust_remote_code=True)
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2", trust_remote_code=True)

    def wrap_prompt(self, prompt : str) -> str:
        # MS Phi-2 expects text generation to be wrapped with "INSTRUCT:"
        # In fact, pure chat would require different wrapping
        return "INSTRUCT: Write as a chat bot to this:" + prompt

    def clean_response_text(self, output : str) -> str:
        try:
            # Look for text after 'OUTPUT:' and capture until end of text or any potential end token.
            return re.findall(r"OUTPUT:\s+(.*?)(<\|endoftext\|>|$)", output, re.DOTALL)[0][0].strip()
        except Exception as e:
            print(f"Regex match error: {e}")
            # Just return the whole model prediction
            return output

    def get_answer(self, prompt : str, raw_answer : bool = False) -> str:
        inputs = self.tokenizer(self.wrap_prompt(self._context_memory + prompt), return_tensors="pt", return_attention_mask=False)
        outputs = self.model.generate(**inputs, max_new_tokens=200, pad_token_id=self.tokenizer.eos_token_id)

        # If raw answer is wanted:
        if raw_answer:
            return self.tokenizer.batch_decode(outputs)[0]
            
        
        # Strip model wrapping text and add to context memory
        text = self.clean_response_text(self.tokenizer.batch_decode(outputs)[0])
        self._context_memory += prompt + text
        return text

if __name__=="__main__":
    llm = Phi2_api()
    while True:
        prompt = input("You: ")
        print(f"LLM: {llm.get_answer(prompt)}")
