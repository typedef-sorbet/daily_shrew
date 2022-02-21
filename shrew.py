import json
import hashlib
from PIL import Image
import io
import config_loader

from os import listdir
from os.path import isfile, join
from random import shuffle

_ROOT_PATH = "/home/sanctity/daily_shrew"
_RSC_PATH = "/home/sanctity/daily_shrew/rsc"

def get_new_shrew():
    # Parse through /rsc and find a new shrew filename that hasn't been sent yet
    # TODO could probably optimize this by only grabbing all files once at startup
    all_shrews = [f for f in listdir(_RSC_PATH) if isfile(join(_RSC_PATH, f))]
    shuffle(all_shrews)

    used_shrews = config_loader.config_as_dict()["used_shrew_hashes"]

    for shrew in all_shrews:
        # Hash the image file to see if we've used it before
        shrew_hash = hashlib.md5(Image.open(join(_RSC_PATH, shrew)).tobytes()).hexdigest()

        if shrew_hash not in used_shrews:
            return join(_RSC_PATH, shrew)
    else:
        return False


def mark_shrew_as_used(shrew):
    config = config_loader.config_as_dict()
    shrew_path = shrew if "/home" not in shrew else join(_RSC_PATH, shrew)
    shrew_hash = hashlib.md5(Image.open(shrew_path).tobytes()).hexdigest()
    if shrew_hash not in config["used_shrew_hashes"]:
        config["used_shrew_hashes"].append(shrew_hash)
        config_loader.write_config(config)
