import context_memory
import openai
import os
from colorama import Fore, Style

class Chatgpt35_api():
    def __init__(self):
        self._context_memory = context_memory.Context_memory(max_size=10000)
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.api_key is None:
            raise ValueError("OpenAI API key not found")
        self._model = "gpt-3.5-turbo"

    def get_answer(self, prompt : str, raw_answer : bool = False) -> str:
        response = openai.Completion.create(
            engine=self._model,
            prompt=prompt,
            n=1,
            stop=None
        )
        answer = response.choices[0].text.strip()
        self._context_memory.append_chat_lines(user_str=prompt, answer_str=answer)
        return answer


if __name__=="__main__":
    llm = Chatgpt35_api()
    while True:
        prompt = input("You: ")
        print(f"LLM: {llm.get_answer(prompt)}")