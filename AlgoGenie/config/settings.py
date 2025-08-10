import os
from dotenv import load_dotenv

from autogen_ext.models.openai import OpenAIChatCompletionClient
from config.constant import MODEL

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')



def get_model_client():
    model_client = OpenAIChatCompletionClient(model=MODEL, api_key=api_key)
    return model_client


