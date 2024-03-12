# Kivy Chat

A small project to see, if mobile phones can run the smaller LLM's. I implemented the Microsoft's phi-2 that should be a very compact model, but so far it seems a bit too large at least for Samsung S10e. The default model for the kivy chat is currently the OpenAI's chatGPT 3.5 Turbo, which of course runs on phones, as it just makes a request to the openai and does no inferring locally. If you want to try other models, change the model in main file for corresponding API.

It seems chatGPT 2.5 Turbo does not require an API key anymore.. That's why the environmental variable 'OPEN_API_KEY' functionality is disabled. If this changes in the future, you have to provide the api key.

## Installation

The requirements for all APIs are in the 'requirements.txt'. Create a venv, install dependancies and run. Nowadays Kivy seems to be much easier to install, I had success installing it normally with pip.

```
python - m venv .venv

.\.venv\Scripts\activate

python -m pip install -r requirements.txt
```

Run with your favourite IDE or terminal:
```
python k_chat.py
```

## Notes

Gimme a msg if you are able to run LLMs locally with a phone
