import configparser
import os

config = configparser.ConfigParser()
current_dir = os.path.abspath(".")
full_path = os.path.join(current_dir, "config/.env")
config.read(full_path, encoding="utf-8")


class Settings:
    LOG_DATA = config.get("S3", "LOG_DATA")
    ARN = config.get("IAM_ROLE", "ARN")
    REGION = config.get("IAM_ROLE", "REGION")
    LOG_JSON_PATH = config.get("S3", "LOG_JSONPATH")
    SONG_DATA = config.get("S3", "SONG_DATA")
    HOST = config.get("CLUSTER", "HOST")
    DB_NAME = config.get("CLUSTER", "DB_NAME")
    DB_USER = config.get("CLUSTER", "DB_USER")
    DB_PASSWORD = config.get("CLUSTER", "DB_PASSWORD")
    DB_PORT = config.get("CLUSTER", "DB_PORT")
