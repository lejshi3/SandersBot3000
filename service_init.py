# service_init.py
import anthropic
from pocketbase import PocketBase

def init_services(env_vars):
    anthropic_client = anthropic.Client(api_key=env_vars["anthropic_api_key"])
    pb = PocketBase(env_vars["pocketbase_url"])
    auth_data = pb.admins.auth_with_password(env_vars["pocketbase_email"], env_vars["pocketbase_password"])

    return {
        "anthropic_client": anthropic_client,
        "pocketbase": pb,
        "pocketbase_auth_data": auth_data,
    }