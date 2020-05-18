import configparser
import json
import os
from os.path import dirname, realpath

filepath = realpath(__file__)
# Current File Base Dir
file_dir = dirname(filepath)
basedir = os.path.abspath(os.path.dirname(file_dir))
config_location = '%s/config/banter_tag_gen.config' % basedir
print(config_location)
config = configparser.ConfigParser()
config.read(config_location)
section = "DEFAULT"
test = json.loads(config.get(section, "SPORTS_LEAGUES"))
set(json.loads(config.get(section, "SPORTS_LEAGUES")))
print(test)
max = int(config.get(section, "MAX_DESCRIPTION_LENGTH"))
