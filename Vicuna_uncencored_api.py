'''Vicuna-13b-uncensored'''

import context_memory
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import re
from colorama import Fore, Style

class Vicuna_uncencored_api():
    def __init__(self):
        torch.set_default_device("cuda")
        # Introduce rudimentary context memory. Currently the context does not shrink, so the prompts to the model get big very soon. The list structure should be made into a queue
        self._context_memory = context_memory.Context_memory(max_size=1024)
        # init Vicuna uncencored 13b
        model_name = "TheBloke/Wizard-Vicuna-13B-Uncensored-GPTQ"
        self.model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype="auto", trust_remote_code=False, revision="main")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)

    def wrap_prompt(self, prompt : str, include_context_memory : bool = True) -> str:
        # The info for Vicuna uncencored: https://huggingface.co/TheBloke/Wizard-Vicuna-13B-Uncensored-GPTQ
        final_prompt = "A chat between a curious user and an artificial intelligence assistant.\n"
        final_prompt += "the assistant gives helpful, detailed, and polite answers to the user's questions.\n"
        if include_context_memory:
            final_prompt += "Chat history:\n" + self._context_memory.get_context_memory() + "\n"

        final_prompt += f"USER: {prompt} ASSISTANT:"

        return final_prompt

    def clean_response_text(self, output : str) -> str:
        try:
            # Look for text after 'Output:' and capture until end of text or any potential end token.
            res =  re.findall(r"Output:\s+(.*?)(<\|endoftext\|>|$)", output, re.DOTALL)[-1][0].strip()
            return res
        except Exception as e:
            print(f"Regex match error: {e}")
            # Just return the whole model prediction
            return output

    def get_answer(self, prompt : str, raw_answer : bool = False) -> str:
        modified_prompt = self.wrap_prompt(prompt)
        # Display the prompt that the model will see
        print(f"Model prompt: {Fore.RED}{modified_prompt}{Style.RESET_ALL}")
        inputs = self.tokenizer(modified_prompt, return_tensors="pt")
        outputs = self.model.generate(**inputs, max_new_tokens=200, pad_token_id=self.tokenizer.eos_token_id, return_dict_in_generate=True)

        # Phi-2 should get beam search soon
        candidate_generations = outputs["sequences"]

        try:
            # If beam search is used
            best_generation_index = torch.argmax(outputs["scores"]).item()
            best_generation = self.tokenizer.batch_decode(candidate_generations)[best_generation_index]
        except KeyError:
            # If beam search is not used (potentially top-k sampling)
            # Choose the first generation (or implement another selection method)
            best_generation = self.tokenizer.batch_decode(candidate_generations)[0]

        # Display the model's response
        print(f"Model response: {Fore.GREEN}{best_generation}{Style.RESET_ALL}")
        # If raw answer is wanted:
        if raw_answer:
            return best_generation
        
        # Strip model wrapping text and add to context memory
        cleaned_text = self.clean_response_text(best_generation)
        self._context_memory.append_chat_lines(user_str=prompt, answer_str=cleaned_text)
        return cleaned_text


if __name__=="__main__":
    llm = Vicuna_uncencored_api()
    while True:
        prompt = input("You: ")
        print(f"LLM: {llm.get_answer(prompt)}")