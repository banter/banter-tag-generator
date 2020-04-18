from sportsreference.nhl.teams import Teams as NHLTeams
from sportsreference.nba.teams import Teams as NBATeams
from sportsreference.nfl.teams import Teams as NFLTeams
from sportsreference.mlb.teams import Teams as MLBTeams
from sportsreference.ncaab.teams import Teams as NCAABTeams
from sportsreference.ncaaf.teams import Teams as NCAAFBTeams
import json


# TODO Handle Soccer Teams/Players

def create_player_dict(teams):
    player_dict = {}
    for team in teams:
        roster = team.roster
        for player in roster.players:
            player_dict[player.name] = team.name
    return player_dict


def save_dict(dictionary, file_name):
    tmp_json = json.dumps(dictionary)
    f = open(f"../assets/reference_dict/{file_name}.json", "w")
    f.write(tmp_json)
    f.close()


teams = NHLTeams(2019)
nhl_dict = create_player_dict(teams)
save_dict(nhl_dict, "nhl_player_dict")
teams = NBATeams(2019)
nba_dict = create_player_dict(teams)
save_dict(nba_dict, "nba_player_dict")
teams = NFLTeams(2019)
nfl_dict = create_player_dict(teams)
save_dict(nfl_dict, "nfl_player_dict")
teams = MLBTeams(2019)
mlb_dict = create_player_dict(teams)
save_dict(mlb_dict, "mlb_player_dict")
