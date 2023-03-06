from dotenv import load_dotenv, find_dotenv
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(find_dotenv())

TOKEN = os.environ.get("TOKEN")
ACCESS_ID_LIST = os.environ.get("ACCESS_ID_LIST").split(',')

FORUM_CHAT_ID = os.environ.get("FORUM_CHAT_ID")

TORTOISE_CONFIG = {
    'connections': {
        # Dict format for connection
        'default': {
            'engine': 'tortoise.backends.sqlite',
            'credentials': {
                "file_path": BASE_DIR / os.environ.get("DB_NAME", "db_dev.sqlite3"),
                'user': os.environ.get("DB_USER", 'tortoise'),
                'password': os.environ.get("DB_PASSWORD", 'qwerty123'),
                'database': os.environ.get("DATABASE", 'dev'),
            }
        }
    },
    'apps': {
        'models': {
            'models': ['aerich.models', 'database.models'],
        }
    }
}
import datetime
print(datetime.datetime.now(tz=datetime.timezone.utc).tzinfo)