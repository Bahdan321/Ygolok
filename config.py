from dotenv import load_dotenv
import os
from envparse import Env


load_dotenv()
env = Env()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")


REAL_DATABASE_URL = env.str(
    "REAL_DATABASE_URL",
    default=f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
)


SECRET_KEY: str = env.str("SECRET_KEY", default="secret_key")
ALGORITHM: str = env.str("ALGORITHM", default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = env.int("ACCESS_TOKEN_EXPIRE_MINUTES", default=30)


DEFAULT_PATH_ORG_IMAGE: str = os.environ.get("DEFAULT_PATH_ORG_IMAGE")
DEFAULT_PATH_WORKER_IMAGE: str = os.environ.get("DEFAULT_PATH_WORKER_IMAGE")
ORG_FILES_PATH: str = os.environ.get("ORG_FILES_PATH")
