import configparser
import os


current_dir = os.path.abspath(".")
full_path = os.path.join(current_dir, "config/.env")

config = configparser.ConfigParser()
config.read(full_path, encoding="utf-8")


class Settings:
    LOG_DATA = config.get("S3", "LOG_DATA")
    ARN = config.get("IAM_ROLE", "ARN")
    REGION = config.get("AWS", "REGION")
    LOG_JSON_PATH = config.get("S3", "LOG_JSONPATH")
    SONG_DATA = config.get("S3", "SONG_DATA")
    HOST = config.get("CLUSTER", "HOST")
    DB_NAME = config.get("CLUSTER", "DB_NAME")
    DB_USER = config.get("CLUSTER", "DB_USER")
    DB_PASSWORD = config.get("CLUSTER", "DB_PASSWORD")
    DB_PORT = config.get("CLUSTER", "DB_PORT")
    KEY = config.get("AWS", "KEY")
    SECRET = config.get("AWS", "SECRET")
    TOKEN = config.get("AWS", "TOKEN")
