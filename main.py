import discord

# Import Local Modules
from env_loader import load_env_vars
from service_init import init_services
from bot import Bot

from constants import *

# Create an instance of the Bot class
intents = discord.Intents.default()
intents.message_content = True
bot = Bot(intents=intents)

# Ensure that you have a valid Discord token
if env_vars['discord_token'] is None:
    raise ValueError("Discord token is not set")

# Run the bot
bot.run(env_vars['discord_token'])