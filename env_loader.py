# env_loader.py
import os
from dotenv import load_dotenv

def load_env_vars():
    load_dotenv()
    webhook_url = os.getenv("WEBHOOK_URL")
    discord_token = os.getenv("DISCORD_API_KEY")
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    pocketbase_url = os.getenv("POCKETBASE_URL")
    pocketbase_email = os.getenv("POCKETBASE_EMAIL")
    pocketbase_password = os.getenv("POCKETBASE_PASSWORD")

    return {
        "webhook_url": webhook_url,
        "discord_token": discord_token,
        "anthropic_api_key": anthropic_api_key,
        "pocketbase_url": pocketbase_url,
        "pocketbase_email": pocketbase_email,
        "pocketbase_password": pocketbase_password,
    }