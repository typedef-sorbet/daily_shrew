import json
from os.path import join

_ROOT_PATH = "/home/sanctity/daily_shrew"

def config_as_dict():
    """
        Returns project config.json as a Python dict.
    """
    with open(join(_ROOT_PATH, "config.json"), "r") as config_file:
        return json.loads(config_file.read())

def write_config(dikt):
    """
        Writes `dikt` to the config file.
        This function performs no checks. Use with caution.
    """
    with open(join(_ROOT_PATH, "config.json"), "w") as config_file:
        config_file.write(json.dumps(dikt))

def client_token():
    with open(join(_ROOT_PATH, "config.json"), "r") as config_file:
        return json.loads(config_file.read())["client_token"]

def channel():
    with open(join(_ROOT_PATH, "config.json"), "r") as config_file:
        return int(json.loads(config_file.read())["channel_id"])
