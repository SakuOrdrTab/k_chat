import context_memory
from openai import OpenAI
import os
from colorama import Fore, Style

class Chatgpt35_api():
    def __init__(self):
        self._context_memory = context_memory.Context_memory(max_size=10000)
        # Seems like the 3.5 turbo does not require api key anymore?
        # self.api_key = os.getenv("OPENAI_API_KEY")
        # if self.api_key is None:
        #     raise ValueError("OpenAI API key not found")
        
        self._model = "gpt-3.5-turbo"
        self._client = OpenAI()


    def wrap_prompt(self, prompt : str, include_context_memory : bool = True) -> str:
        '''Just add the context memory'''
        final_prompt = ""
        if include_context_memory:
            final_prompt += "Chat history:\n" + self._context_memory.get_context_memory() + "\n"
        
        final_prompt += prompt + "\n"
        return final_prompt

    def get_answer(self, prompt : str, raw_answer : bool = False) -> str:
        response = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a chat bot."
                },
                {
                    "role": "user",
                    "content": self.wrap_prompt(prompt)
                }
            ]
        )
        answer = response.choices[0].message.content
        self._context_memory.append_chat_lines(user_str=prompt, answer_str=answer)
        return answer


if __name__=="__main__":
    llm = Chatgpt35_api()
    while True:
        prompt = input("You: ")
        print(f"LLM: {llm.get_answer(prompt)}")