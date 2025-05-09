import os
from dotenv import load_dotenv

load_dotenv()

HUBSPOT_API_KEY = os.getenv("HUBSPOT_API_KEY")
MODEL_PATH = "models/"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
