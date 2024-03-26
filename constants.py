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

# record_id = 'rmnr73yi8qw6w5p' # Sanders
record_id = '2u7dofvuxcp3s2n' # Fulcros
record2_id = 'lddbtbyby25zknp' 

npc_data = pb.collection('npcs').get_one(record_id)

lore_json = npc_data.lore
description = lore_json["description"]
characteristics = lore_json["characteristics"]

lore = f"<Description> You play as {description['full_name']}, the {description['occupation']} of {description['nationality']}, a fictitious {description['politics']} in a multiplayer nation-building role-playing game. </Description> <Characteristics> As {characteristics['short_name']}, you value {characteristics['values']}. You also {characteristics['Personality']}. </Characteristics>"




game_data = pb.collection('game').get_one(record2_id)
message_bank = pb.collection('npcs').get_one(record_id).conversation

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