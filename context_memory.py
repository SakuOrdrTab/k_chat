'''Context memory for LLM chats'''
from collections import deque

class Context_memory():
    def __init__(self, max_size : int = 512):
        """Create a new context memory for chatbot conversations. Remember to set
        a suitable value for maximum size, otherwise the prompts will grow far
        too long.

        Args:
            max_size (int, optional): Maximum characters in memory. Defaults to 512.
        """        
        self._context_memory = deque()
        self._max_size = max_size
        self._size = 0

    def append_chat_lines(self, user_str : str, answer_str : str) -> None:
        """Append context memory with user's prompt and LLM's answer.

        Args:
            user_str (str): Users prompt string without LLM specific wrapping
            answer_str (str): Answer without LLM specific wrapping
        """        
        self._context_memory.append("user: " + user_str + "\nchatbot: " + answer_str)
        self._size += len(user_str) + len(answer_str)
        while self._size > self._max_size:
            self._size -= len(self._context_memory.popleft())
        
    def get_context_memory(self) -> str:
        """Returns the context memorys current content.

        Returns:
            str: previous chat lines type (user:...chatbot:...)
        """        
        return "\n".join(self._context_memory)
    
if __name__ == "__main__":
    cm = Context_memory(max_size=1024)
    cm.append_chat_lines("Hello", "Hi")
    print(cm.get_context_memory())
    cm.append_chat_lines("How are you?", "I'm fine")
    cm.append_chat_lines("whaatsa wrooong", "nothing")
    print(cm.get_context_memory())