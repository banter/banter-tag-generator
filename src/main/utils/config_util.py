import configparser
import json
import os
from os.path import dirname, realpath
from typing import *

# Current File Base Dir
BASEDIR = os.path.abspath(os.path.dirname(dirname(realpath(__file__))))
CONFIG_LOCATION = '%s/config/banter_tag_gen.config' % BASEDIR
CONFIG = configparser.ConfigParser()
CONFIG.read(CONFIG_LOCATION)
SECTION = "DEFAULT"


class SportsConfig:
    sports_reference_dir = r"%s/resources/reference_dict" % BASEDIR
    sports_leagues: List[str] = json.loads(CONFIG.get(SECTION, "SPORTS_LEAGUES"))
    sports_leagues_no_player_ref: List[str] = json.loads(CONFIG.get(SECTION, "SPORTS_LEAGUES_NO_PLAYER_REF"))
    sports_leagues_no_team_ref: List[str] = json.loads(
        CONFIG.get(SECTION, "SPORTS_LEAGUES_NO_TEAM_REF"))  # for database globals
    sports_with_references: List[str] = json.loads(CONFIG.get(SECTION, "SPORTS_WITH_REF"))
    sports_leagues_with_nickname_and_coaches: List[str] = json.loads(
        CONFIG.get(SECTION, "SPORTS_LEAGUES_WITH_NICKNAME_AND_COACHES"))
    # Todo add more indv. sports dicts
    individual_sports: List[str] = json.loads(CONFIG.get(SECTION, "INDIVIDUAL_SPORTS"))
    # TODO handle football/soccer vs american football
    all_sports: List[str] = json.loads(CONFIG.get(SECTION, "ALL_SPORTS"))


class LanguageConfig:
    # TODO Consider EVENTS
    token_types_analyzed = set(json.loads(CONFIG.get(SECTION, "TOKEN_TYPES_ANALYZED")))
    # TODO Consider NOUNS?
    language_types_analyzed: Set[str] = set(json.loads(CONFIG.get(SECTION, "LANGUAGE_TYPES_ANALYZED")))
    ignore_tags: set = set(json.loads(CONFIG.get(SECTION, "IGNORE_TAGS")))
    # TODO Consider max descrition size to consider
    max_description: int = int(CONFIG.get(SECTION, "MAX_DESCRIPTION_LENGTH"))


class DbConfig:
    pass
