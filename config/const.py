from dotenv import load_dotenv, find_dotenv
import os


load_dotenv(find_dotenv())
TOKEN = os.environ.get("TOKEN")
STRPTIME_PATTERN = '%Y-%m-%d %H:%M'
ACCESS_ID_LIST = os.environ.get("ACCESS_ID_LIST").split(',')
