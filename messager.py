# Import Local Modules
from env_loader import load_env_vars
from service_init import init_services

from constants import *

# Load environment variables
env_vars = load_env_vars()

# Initialize external services
services = init_services(env_vars)
anthropic_client = services["anthropic_client"]
pb = services["pocketbase"]
auth_data = services["pocketbase_auth_data"]

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