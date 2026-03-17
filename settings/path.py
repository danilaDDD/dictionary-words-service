import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_env_file_path(env: str =None) -> str:
    env_dir = "conf"
    env_file = f".env.{env}" if env else ".env"

    return os.path.join(BASE_DIR, env_dir, env_file)