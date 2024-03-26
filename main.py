# Import Python Modules
import discord
from discord import app_commands
import requests
import xml.etree.ElementTree as ET
import re

# Import Local Modules
from env_loader import load_env_vars
from service_init import init_services

# Load environment variables
env_vars = load_env_vars()

# Initialize external services
services = init_services(env_vars)
anthropic_client = services["anthropic_client"]
pb = services["pocketbase"]
auth_data = services["pocketbase_auth_data"]

# Get nation list

# nations = []
# nations_data = pb.collection('nations').get_full_list()

record_id = 'rmnr73yi8qw6w5p'
record2_id = 'lddbtbyby25zknp'

npc_data = pb.collection('npcs').get_one(record_id)
game_data = pb.collection('game').get_one(record2_id)
message_bank = pb.collection('npcs').get_one(record_id).conversation

non_xml_pattern = re.compile(r'[^\u0009\u000a\u000d\u0020-\uD7FF\uE000-\uFFFD\u10000-\u10FFFF]+')

def strip_non_xml(string):
    cleaned_string = non_xml_pattern.sub('', string)
    return cleaned_string

'''
for i in nations_data:
  nations.append({
    'name': i.name,
    'leader': i.leader,
    'ideology': i.ideology
  })
'''

# Blacklisted User IDs
author_blacklist = [
  1221324317850337310,
  1222065090417655828
]

# Player Pairings
players = {
  424296451661627392: "Samyra Cruz",
  691101488667295775: "Game-master",
  729416298454450236: "Marskalk Blixten",
  527375791781314561: "Imperator Crimsonus",
  474563589525733416: "Grandfather Calkins",
  883033081404092466: "John Klinderbaucle"
}

'''

print(f"""
    {npc_data.lore}
    {npc_data.memory}
    {env_vars['pocketbase_url']}/api/files/npcs/{record_id}/{npc_data.profile_pic}
""")

'''

# Entire AI Overhead Class
class Messager:
  MODELS = {
      "haiku": "claude-3-haiku-20240307",
      "sonnet": "claude-3-sonnet-20240229",
      "opus": "claude-3-opus-20240229"
  }

  def __init__(self, message_bank, model_name="sonnet", max_tokens=1024, temperature=1, system_message="You are a helpful assistant."):
      self.message_bank = message_bank
      self.model = self.MODELS[model_name]
      self.max_tokens = max_tokens
      self.temperature = temperature
      self.system_message = system_message

  def add_user_message(self, message_content):
      self.message_bank.append({"role": "user", "content": message_content})

  def add_assistant_message(self, message_content):
      self.message_bank.append({"role": "assistant", "content": message_content})

  def set_system_message(self, message_content):
      self.system_message = message_content

  def post_messages(self):
      response = anthropic_client.messages.create(
          model=self.model,
          max_tokens=self.max_tokens,
          temperature=self.temperature,
          system=self.system_message,
          messages=self.message_bank
      )
      self.add_assistant_message(response.content[0].text)

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
          strangers = [k for k, v in players.items() if v.startswith("Stranger #")]
          next_stranger_number = len(strangers) + 1
          players[message.author.id] = f"Stranger #{next_stranger_number}"
          player = players.get(message.author.id)

        messager = Messager(message_bank)
        messager.set_system_message(f"""
          {game_data.master_prompt}
          {game_data.current_nations}
          {npc_data.lore}
          {npc_data.memory}
          It is currently Year {game_data.year}, Month {game_data.month}
        """)

        user_input = f"<message>{player}: {player_message}</message>"
        
        messager.add_user_message(user_input)
        
        async with message.channel.typing():
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
                  webhook = await self.fetch_webhook(1222065090417655828)
                  await webhook.send(
                      username=f"{npc_data.username}",
                      avatar_url=f"{env_vars['pocketbase_url']}/api/files/npcs/{record_id}/{npc_data.profile_pic}",
                      content=text
                  )

          pb.collection('npcs').update(record_id, {"conversation": message_bank})
          

# Create an instance of the Bot class
intents = discord.Intents.default()
intents.message_content = True
bot = Bot(intents=intents)

# Ensure that you have a valid Discord token
if env_vars['discord_token'] is None:
    raise ValueError("Discord token is not set")

# Run the bot
bot.run(env_vars['discord_token'])

'''
await channel.create_webhook(
    name="Col. Sanders",
    avatar=avatar_bytes,
    reason="The chicken man is here"
)
'''
