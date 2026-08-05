from dotenv import load_dotenv
import os

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MAX_SUMMARY_MESSAGES = 150
SUMMARY_CONTEXT_MESSAGES = 50
MAX_PROMPT_CHARS = 30000