import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve API key
HF_API_KEY = os.getenv("HF_API_KEY")