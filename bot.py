# Import Python Modules
import xml.etree.ElementTree as ET
import re
import discord
from discord import app_commands
from discord.utils import sleep_until
import asyncio
import time

# Import Local Modules
from env_loader import load_env_vars
from service_init import init_services
from messager import Messager

from constants import *

# XML RegEx
non_xml_pattern = re.compile(
    r'[^\u0009\u000a\u000d\u0020-\uD7FF\uE000-\uFFFD\u10000-\u10FFFF]+')


def strip_non_xml(string):
  cleaned_string = non_xml_pattern.sub('', string)
  return cleaned_string


# Load environment variables
env_vars = load_env_vars()

# Initialize external services
services = init_services(env_vars)
anthropic_client = services["anthropic_client"]
pb = services["pocketbase"]
auth_data = services["pocketbase_auth_data"]


# Bot Class
class Bot(discord.Client):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    tree = app_commands.CommandTree(self)
    self.tree = tree

  async def on_ready(self):
    print(f'We have logged in as {self.user}')

  async def on_message(self, message):
    target_channel_id = 1222064782333579335

    for i in author_blacklist:
      if message.author.id == i:
        return

    if message.channel.id == target_channel_id:
      player = players.get(message.author.id)
      player_message = message.content

      if player == None:
        strangers = [
            k for k, v in players.items() if v.startswith("Stranger #")
        ]
        next_stranger_number = len(strangers) + 1
        players[message.author.id] = f"Stranger #{next_stranger_number}"
        player = players.get(message.author.id)

      messager = Messager(message_bank)
      messager.set_system_message(f"""
          {game_data.master_prompt}
          {game_data.current_nations}
          Memories: {memories} 
          Lore: {lore} 
          It is currently Year {game_data.year}, Month {game_data.month}
        """)

      user_input = f"<message>{player}: {player_message}</message>"

      messager.add_user_message(user_input)

      messager.post_messages()
      assistant_message = messager.message_bank[-1]["content"]

      cleaned_message = assistant_message.replace('\\n', '').replace('\\', '')
      cleaned_message = strip_non_xml(cleaned_message)

      # Wrap the cleaned XML in a single root element
      wrapped_xml = f"<root>{cleaned_message}</root>"

      dialogue = ET.fromstring(wrapped_xml)

      for element in dialogue:
        tag_name = element.tag
        text = element.text.strip()

        if tag_name == "think":
          print(f"Thinking: {text}")

        if tag_name == "remember":
          print(f"Remember: {text}")

        elif tag_name == "chat" or tag_name == "prompt":
          async with message.channel.typing():
            time.sleep(1)
            webhook = await self.fetch_webhook(1222065090417655828)
            await webhook.send(
                username=f"{npc_data.username}",
                avatar_url=f"{env_vars['pocketbase_url']}/api/files/npcs/{record_id}/{npc_data.profile_pic}",
                content=text)

      pb.collection('npcs').update(record_id, {"conversation": message_bank})
