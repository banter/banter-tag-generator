import json
# TODO Handle Soccer Teams/Players
# TODO Check Players, references spot check incomplete (Missing AJ Green)
import os
from os.path import dirname, realpath

from sportsreference.mlb.teams import Teams as MLBTeams
from sportsreference.nba.teams import Teams as NBATeams
from sportsreference.nfl.teams import Teams as NFLTeams
from sportsreference.nhl.teams import Teams as NHLTeams

from src.main.utils.nlp_conversion_util import NLPConversionUtil
from src.main.utils.nlp_resource_util import NLPResourceUtil

BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(dirname(realpath(__file__)))))
SAVE_LOCATION = '%s/resources/reference_dict' % BASEDIR


def create_player_dict_on_teams(teams):
    player_dict = {}
    for team in teams:
        roster = team.roster
        for player in roster.players:
            try:
                player_dict[NLPConversionUtil().normalize_text(player.name)] = team.name
            except:
                # Some players have a name as None in sportsreference dict
                print("HERE", player.name)
                player_dict[player.name] = team.name

    return player_dict


def save_dict(dictionary, file_name):
    tmp_json = json.dumps(dictionary)
    f = open(f"{SAVE_LOCATION}/{file_name}.json", "w")
    f.write(tmp_json)
    f.close()


def create_player_dict(modify_existing: bool, is_team_upper_case: False):
    if modify_existing:
        if is_team_upper_case:
            existing_dict = NLPResourceUtil().sports_player_dict
            nfl_upper = dict(
                (NLPConversionUtil().normalize_text(k), v.upper()) for k, v in existing_dict["NFL"].items())
            nba_upper = dict(
                (NLPConversionUtil().normalize_text(k), v.upper()) for k, v in existing_dict["NBA"].items())
            mlb_upper = dict(
                (NLPConversionUtil().normalize_text(k), v.upper()) for k, v in existing_dict["MLB"].items())
            nhl_upper = dict(
                (NLPConversionUtil().normalize_text(k), v.upper()) for k, v in existing_dict["NHL"].items())
            save_dict(nhl_upper, "NHL_player_dict")
            save_dict(nba_upper, "NBA_player_dict")
            save_dict(mlb_upper, "MLB_player_dict")
            save_dict(nfl_upper, "NFL_player_dict")
        else:
            existing_dict = NLPResourceUtil().sports_player_dict
            nfl_upper = dict((NLPConversionUtil().normalize_text(k), v) for k, v in existing_dict["NFL"].items())
            nba_upper = dict((NLPConversionUtil().normalize_text(k), v) for k, v in existing_dict["NBA"].items())
            mlb_upper = dict((NLPConversionUtil().normalize_text(k), v) for k, v in existing_dict["MLB"].items())
            nhl_upper = dict((NLPConversionUtil().normalize_text(k), v) for k, v in existing_dict["NHL"].items())
            save_dict(nhl_upper, "NHL_player_dict")
            save_dict(nba_upper, "NBA_player_dict")
            save_dict(mlb_upper, "MLB_player_dict")
            save_dict(nfl_upper, "NFL_player_dict")


    else:
        try:
            teams = NHLTeams(2020)
            nhl_dict = create_player_dict_on_teams(teams)
            save_dict(nhl_dict, "NHL_player_dict")
        except:
            teams = NHLTeams(2019)
            nhl_dict = create_player_dict_on_teams(teams)
            save_dict(nhl_dict, "NHL_player_dict")
        try:
            teams = NBATeams(2020)
            nba_dict = create_player_dict_on_teams(teams)
            save_dict(nba_dict, "NBA_player_dict")
        except:
            teams = NBATeams(2019)
            nba_dict = create_player_dict_on_teams(teams)
            save_dict(nba_dict, "NBA_player_dict")
        try:
            teams = MLBTeams(2019)
            mlb_dict = create_player_dict_on_teams(teams)
            save_dict(mlb_dict, "MLB_player_dict")
        except:
            teams = MLBTeams(2019)
            mlb_dict = create_player_dict_on_teams(teams)
            save_dict(mlb_dict, "MLB_player_dict")

        try:
            teams = NFLTeams(2019)
            nfl_dict = create_player_dict_on_teams(teams)
            # SPOT FIX
            nfl_dict["AJ GREEN"] = "CINCINNATI BENGALS"
            save_dict(nfl_dict, "NFL_player_dict")
        except:
            teams = NFLTeams(2019)
            nfl_dict = create_player_dict_on_teams(teams)
            # SPOT FIX
            nfl_dict["AJ GREEN"] = "CINCINNATI BENGALS"
            save_dict(nfl_dict, "NFL_player_dict")
