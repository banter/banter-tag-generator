import json

from sportsreference.mlb.teams import Teams as MLBTeams
from sportsreference.nba.teams import Teams as NBATeams
from sportsreference.nfl.teams import Teams as NFLTeams
from sportsreference.nhl.teams import Teams as NHLTeams

from src.main.utils.nlp_conversion_util import NLPConversionUtil

import os
from os.path import dirname, realpath

BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(dirname(realpath(__file__)))))
SAVE_LOCATION = '%s/resources/reference_dict' % BASEDIR

# TODO Handle Soccer Teams/Players

def create_team_dict_ref(teams):
    team_dict = {}
    for team in teams:
        team_dict[team.name] = team.name
        # Getting Team Name I.e. Miami Heat ---- Heat
        # St. Louis Blues --- Blues
        tmp_team_array = team_dict[team.name].split()
        if len(team_dict[team.name].split()) == 3:
            if team.name == "Boston Red Sox":
                team_dict["Red Sox"] = team.name
            if team.name == "Chicago White Sox":
                team_dict["White Sox"] = team.name
            if team.name == "Toronto Blue Jays":
                team_dict["Blue Jays"] = team.name
            if team.name == "Toronto Maple Leafs":
                team_dict["Maple Leafs"] = team.name
            if team.name == "Detroit Red Wings":
                team_dict["Red Wings"] = team.name
            else:
                team_dict[tmp_team_array[2]] = team.name
        else:
            team_dict[tmp_team_array[1]] = team.name
        # team_dict[team.abbreviation] = team.name
    return team_dict


def create_college_dict(teams):
    team_dict = {}
    for team in teams:
        team_dict[team.name] = team.name
        team_dict[team.abbreviation] = team.name
    return team_dict

def save_dict(dictionary, file_name):
    tmp_json = json.dumps(dictionary)
    f = open(f"{SAVE_LOCATION}/{file_name}.json", "w")
    f.write(tmp_json)
    f.close()

def create_team_dict(is_team_upper_case: False):
    if is_team_upper_case:
        teams = NHLTeams(2019)
        nhl_dict = create_team_dict_ref(teams)
        nhl_dict_upper = dict((NLPConversionUtil().normalize_text(k), v.upper()) for k, v in nhl_dict.items())
        save_dict(nhl_dict_upper, "NHL_team_dict")

        teams = NBATeams(2019)
        nba_dict = create_team_dict_ref(teams)
        nba_dict_upper = dict((NLPConversionUtil().normalize_text(k), v.upper()) for k, v in nba_dict.items())
        save_dict(nba_dict_upper, "NBA_team_dict")

        teams = NFLTeams(2019)
        nfl_dict = create_team_dict_ref(teams)
        nfl_dict_upper = dict((NLPConversionUtil().normalize_text(k), v.upper()) for k, v in nfl_dict.items())
        save_dict(nfl_dict_upper, "NFL_team_dict")

        teams = MLBTeams(2019)
        mlb_dict = create_team_dict_ref(teams)
        mlb_dict_upper = dict((NLPConversionUtil().normalize_text(k), v.upper()) for k, v in mlb_dict.items())
        save_dict(mlb_dict_upper, "MLB_team_dict")

    else:
        teams = NHLTeams(2019)
        nhl_dict = create_team_dict_ref(teams)
        nhl_dict_upper = dict((NLPConversionUtil().normalize_text(k), v) for k, v in nhl_dict.items())
        save_dict(nhl_dict_upper, "NHL_team_dict")

        teams = NBATeams(2019)
        nba_dict = create_team_dict_ref(teams)
        nba_dict_upper = dict((NLPConversionUtil().normalize_text(k), v) for k, v in nba_dict.items())
        save_dict(nba_dict_upper, "NBA_team_dict")

        teams = NFLTeams(2019)
        nfl_dict = create_team_dict_ref(teams)
        nfl_dict_upper = dict((NLPConversionUtil().normalize_text(k), v) for k, v in nfl_dict.items())
        save_dict(nfl_dict_upper, "NFL_team_dict")

        teams = MLBTeams(2019)
        mlb_dict = create_team_dict_ref(teams)
        mlb_dict_upper = dict((NLPConversionUtil().normalize_text(k), v) for k, v in mlb_dict.items())
        save_dict(mlb_dict_upper, "MLB_team_dict")

# Removing College Sports for the time being (These references are extremely large
# And can leade to issues like..... Drake being interviewed but we tag it as a Drake the school podcast
# teams = NCAABTeams(2019)
# ncaab_dict = create_college_dict(teams)
# save_dict(ncaab_dict, "ncaab_teams")
# teams = NCAAFBTeams(2019)
# ncaafb_dict = create_college_dict(teams)
# save_dict(ncaafb_dict, "ncaafb_dict")
