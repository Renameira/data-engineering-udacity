import configparser
import os


config = configparser.ConfigParser()
current_dir = os.path.abspath(".")
full_path = os.path.join(current_dir, "config/.env")
config.read(full_path, encoding="utf-8")


class Settings:
	CONNECTION_STRING_SPARKIFYDB = config["DB"]["CONNECTION_STRING_SPARKIFYDB"]
