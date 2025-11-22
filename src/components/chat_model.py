from yaml import safe_load

from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace
from langchain_huggingface import HuggingFaceEndpoint
from langchain_ollama import ChatOllama
from langchain_perplexity import ChatPerplexity

from config import config


load_dotenv()

chat_model_config = config['chat_model']

# Using HuggingFace Model
# _llm = HuggingFaceEndpoint(repo_id=chat_model_config['huggingface']['gpt_oss_model'] , task='text-generation')
# chat_model = ChatHuggingFace(llm=_llm)

# Using Ollama Model
# chat_model = ChatOllama(model=chat_model_config['ollama']['qwen_model'])

# Using Perplexity Model
chat_model = ChatPerplexity(model=chat_model_config['perplexity']['model'])
