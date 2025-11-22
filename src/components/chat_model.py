from yaml import safe_load
from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace
from langchain_huggingface import HuggingFaceEndpoint

from config import config

load_dotenv()


_llm = HuggingFaceEndpoint(repo_id=config['model']['repo_id'] , task='text-generation')
chat_model = ChatHuggingFace(llm=_llm)