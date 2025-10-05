import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
OpenAI_KEY = os.getenv("OPENAI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")