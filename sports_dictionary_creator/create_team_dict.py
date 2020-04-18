from sportsreference.nhl.teams import Teams as NHLTeams
from sportsreference.nba.teams import Teams as NBATeams
from sportsreference.nfl.teams import Teams as NFLTeams
from sportsreference.mlb.teams import Teams as MLBTeams
from sportsreference.ncaab.teams import Teams as NCAABTeams
from sportsreference.ncaaf.teams import Teams as NCAAFBTeams
import json


# TODO Handle Soccer Teams/Players

def create_team_dict(teams):
    team_dict = {}
    for team in teams:
        team_dict[team.name] = team.name
        # Getting Team Name I.e. Miami Heat ---- Heat
        # St. Louis Blues --- Blues
        tmp_team_array = team_dict[team.name].split()
        if len(team_dict[team.name].split()) == 3:
            team_dict[tmp_team_array[2]] = team.name
        else:
            team_dict[tmp_team_array[1]] = team.name
        team_dict[team.abbreviation] = team.name
    return team_dict


def create_college_dict(teams):
    team_dict = {}
    for team in teams:
        team_dict[team.name] = team.name
        team_dict[team.abbreviation] = team.name
    return team_dict


def save_dict(dictionary, file_name):
    tmp_json = json.dumps(dictionary)
    f = open(f"../assets/reference_dict/{file_name}.json", "w")
    f.write(tmp_json)
    f.close()


teams = NHLTeams(2019)
nhl_dict = create_team_dict(teams)
save_dict(nhl_dict, "nhl_dict")
teams = NBATeams(2019)
nba_dict = create_team_dict(teams)
save_dict(nba_dict, "nba_dict")
teams = NFLTeams(2019)
nfl_dict = create_team_dict(teams)
save_dict(nfl_dict, "nfl_dict")
teams = MLBTeams(2019)
mlb_dict = create_team_dict(teams)
save_dict(mlb_dict, "mlb_dict")
teams = NCAABTeams(2019)
ncaab_dict = create_college_dict(teams)
save_dict(ncaab_dict, "ncaab_teams")
teams = NCAAFBTeams(2019)
ncaafb_dict = create_college_dict(teams)
save_dict(ncaafb_dict, "ncaafb_dict")
