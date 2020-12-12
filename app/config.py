import os

from dotenv import load_dotenv

load_dotenv(dotenv_path=os.environ.get("ENV", "env_local.env"))
print("ENV", os.environ.get("ENV", "env_local.env"))


# Global constants
ENTITIES = os.environ["ENTITIES"]
