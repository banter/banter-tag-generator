import json
# TODO Handle Soccer Teams/Players
# TODO Check Players, references spot check incomplete (Missing AJ Green)
import os
from os.path import dirname, realpath

from sportsreference.mlb.teams import Teams as MLBTeams
from sportsreference.nba.teams import Teams as NBATeams
from sportsreference.nfl.teams import Teams as NFLTeams
from sportsreference.nhl.teams import Teams as NHLTeams
from sportsreference.mlb.player import AbstractPlayer

from src.main.utils.banter_dictionary_creator.sports_reference_player_scraper import SportsReferencePlayerScraper
from src.main.utils.banter_dictionary_creator.sports_reference_roster_scraper import SportsReferenceRosterScraper
from src.main.utils.nlp_conversion_util import NLPConversionUtil
from src.main.utils.nlp_resource_util import NLPResourceUtil

BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(dirname(realpath(__file__)))))
SAVE_LOCATION = '%s/resources/reference_dict' % BASEDIR

MLB_OUTFIELD_POSITIONS = ['LF', 'RF', 'OF', 'CF']
FANTASY_FOOTBALL_POSITIONS = ['QB', 'RB', 'WR', 'TE', 'K']
NBA_POSITIONS = ['PG', 'SG', 'SF', 'PF', 'C']


class PositionGenerator:

    def get_position(self, player, league):
        if league == 'MLB':
            return self.get_position_mlb(player)
        elif league == 'NFL':
            return self.get_position_nfl(player)
        elif league == 'NBA':
            return self.get_position_nba(player)
        else:
            return ''

    def is_position_attribute_corect(self, position) -> bool:
        if position == '' or position is None:
            return False
        else:
            return True

    def get_position_mlb(self, player):
        try:
            is_position_correct = self.is_position_attribute_corect(player.position)
            if is_position_correct:
                if player.position in MLB_OUTFIELD_POSITIONS:
                    return 'OF'
                else:
                    return player.position
            else:
                position = self.get_baseball_position_from_protected_attribute(player)
                return position
        except:
            position = self.get_baseball_position_from_protected_attribute(player)
            return position

    def get_baseball_position_from_protected_attribute(self, player):
        try:
            positions = player._position
            if type(positions) == list:
                if positions[0] not in MLB_OUTFIELD_POSITIONS:
                    return positions[0]
                else:
                    return 'OF'
            else:
                if positions != '':
                    if '/' in positions:
                        # CB/LB/RB
                        return positions.split('/')[0]
                    else:
                        return positions
                else:
                    return positions
        except:
            return ''

    def get_position_nfl(self, player):
        is_every_position_empty = True
        try:
            positions = player._position
            if type(positions) == list:
                for index, position in enumerate(positions):
                    if position.upper() in FANTASY_FOOTBALL_POSITIONS:
                        return position.upper()
                    else:
                        if position != '':
                            is_every_position_empty = False
                if is_every_position_empty:
                    return SportsReferencePlayerScraper()._scrape_sports_reference_for_nfl_players_position(player.player_id, FANTASY_FOOTBALL_POSITIONS)
                else:
                    return ''
            else:
                if positions != '':
                    if '/' in positions:
                        # CB/LB/RB
                        position = positions.split('/')[0]
                        if position in FANTASY_FOOTBALL_POSITIONS:
                            return position
                    else:
                        if positions in FANTASY_FOOTBALL_POSITIONS:
                            return positions
                    return ''
                else:
                    return ''
        except:
            return ''

    def get_position_nba(self, player):
        if player.position != '':
            return player.position
        else:
            try:
                positions = player._position
                if type(positions) == list:
                    if positions[0].upper() in NBA_POSITIONS:
                        return positions[0].upper()
                    else:
                        return ''
                else:
                    if positions != '' and positions.upper() in NBA_POSITIONS:
                        return positions.upper()
                    else:
                        return ''
            except:
                return ''


def create_player_dict_on_teams(teams, league):
    player_dict = {}
    for team in teams:
        roster = team.roster
        for player in roster.players:
            try:
                position = PositionGenerator().get_position(player, league)
                player_dict[NLPConversionUtil().normalize_text(player.name)] = {
                    "display": player.name,
                    "team": NLPConversionUtil().normalize_text(team.name),
                    "position": NLPConversionUtil().normalize_text(
                        position)}
            except:
                # Some players have a name as None in sportsreference dict
                try:
                    position = PositionGenerator().get_position(player, league)
                    player_dict[NLPConversionUtil().normalize_text(player.name)] = {
                        "display": player.name,
                        "team": NLPConversionUtil().normalize_text(team.name),
                        "position": NLPConversionUtil().normalize_text(position)}
                except:
                    pass

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
            nhl_dict = create_player_dict_on_teams(teams, 'NHL')
            save_dict(nhl_dict, "NHL_player_dict")
        except:
            teams = NHLTeams(2019)
            nhl_dict = create_player_dict_on_teams(teams, 'NHL')
            save_dict(nhl_dict, "NHL_player_dict")
        try:
            teams = NBATeams(2020)
            nba_dict = create_player_dict_on_teams(teams, 'NBA')
            save_dict(nba_dict, "NBA_player_dict")
        except:
            teams = NBATeams(2019)
            nba_dict = create_player_dict_on_teams(teams, 'NBA')
            save_dict(nba_dict, "NBA_player_dict")
        try:
            teams = MLBTeams(2019)
            mlb_dict = create_player_dict_on_teams(teams, 'MLB')
            save_dict(mlb_dict, "MLB_player_dict")
        except:
            teams = MLBTeams(2019)
            mlb_dict = create_player_dict_on_teams(teams, 'MLB')
            save_dict(mlb_dict, "MLB_player_dict")

        try:
            teams = NFLTeams(2019)
            nfl_dict = create_player_dict_on_teams(teams, 'NFL')
            # SPOT FIX
            nfl_dict["AJ GREEN"] = {"display": "A.J. Green", "team": "CINCINNATI BENGALS",
                                    "position": "WR"}
            del nfl_dict["MICHAEL JORDAN"]
            save_dict(nfl_dict, "NFL_player_dict")
        except:
            teams = NFLTeams(2019)
            nfl_dict = create_player_dict_on_teams(teams, 'NFL')
            # SPOT FIX
            nfl_dict["AJ GREEN"] = {"display": "A.J. Green", "team": "CINCINNATI BENGALS",
                                    "position": "WR"}
            del nfl_dict["MICHAEL JORDAN"]
            save_dict(nfl_dict, "NFL_player_dict")


if __name__ == '__main__':
    leagues = ["MLB", "NFL", "NBA", "NHL"]
    duplicates = []
    for league in leagues:
        players = SportsReferenceRosterScraper(league, get_rosters=True)
        players.save_league_roster_dict(f"{league}_player_dict_new_after_duplicate_changes")
        print(players.duplicate_names)
        duplicates.append(players.duplicate_names)
    print(duplicates)
    # teams = MLBTeams(2019)
    # mlb_dict = create_player_dict_on_teams(teams, 'MLB')
    # save_dict(mlb_dict, "MLB_player_dict")

# "MLB",
# [{'display': 'Tyler White', 'team': 'LOS ANGELES DODGERS', 'position': '1B', 'player_id': 'whitety01'}, {'display': 'Tyler White', 'team': 'HOUSTON ASTROS', 'position': '1B', 'player_id': 'whitety01'}, {'display': 'Kendrys Morales', 'team': 'OAKLAND ATHLETICS', 'position': '1B', 'player_id': 'moralke01'}, {'display': 'Kendrys Morales', 'team': 'NEW YORK YANKEES', 'position': '1B', 'player_id': 'moralke01'}, {'display': 'Ryan Dull', 'team': 'OAKLAND ATHLETICS', 'position': 'P', 'player_id': 'dullry01'}, {'display': 'Ryan Dull', 'team': 'NEW YORK YANKEES', 'position': 'P', 'player_id': 'dullry01'}, {'display': "Travis d'Arnaud", 'team': 'TAMPA BAY RAYS', 'position': 'C', 'player_id': 'darnatr01'}, {'display': "Travis d'Arnaud", 'team': 'LOS ANGELES DODGERS', 'position': 'C', 'player_id': 'darnatr01'}, {'display': 'Casey Sadler', 'team': 'TAMPA BAY RAYS', 'position': 'P', 'player_id': 'sadleca02'}, {'display': 'Casey Sadler', 'team': 'LOS ANGELES DODGERS', 'position': 'P', 'player_id': 'sadleca02'}, {'display': 'Adam Kolarek', 'team': 'TAMPA BAY RAYS', 'position': 'P', 'player_id': 'kolarad01'}, {'display': 'Adam Kolarek', 'team': 'LOS ANGELES DODGERS', 'position': 'P', 'player_id': 'kolarad01'}, {'display': 'Jonny Venters', 'team': 'WASHINGTON NATIONALS', 'position': 'P', 'player_id': 'ventejo01'}, {'display': 'Jonny Venters', 'team': 'ATLANTA BRAVES', 'position': 'P', 'player_id': 'ventejo01'}, {'display': 'Austin Adams', 'team': 'WASHINGTON NATIONALS', 'position': 'P', 'player_id': 'adamsau02'}, {'display': 'Austin Adams', 'team': 'MINNESOTA TWINS', 'position': 'P', 'player_id': 'adamsau01'}, {'display': 'Fernando Rodney', 'team': 'WASHINGTON NATIONALS', 'position': 'P', 'player_id': 'rodnefe01'}, {'display': 'Fernando Rodney', 'team': 'OAKLAND ATHLETICS', 'position': 'P', 'player_id': 'rodnefe01'}, {'display': 'Andrew Velazquez', 'team': 'CLEVELAND INDIANS', 'position': '2B', 'player_id': 'velazan01'}, {'display': 'Andrew Velazquez', 'team': 'TAMPA BAY RAYS', 'position': '2B', 'player_id': 'velazan01'}, {'display': 'Hunter Wood', 'team': 'CLEVELAND INDIANS', 'position': 'P', 'player_id': 'woodhu01'}, {'display': 'Hunter Wood', 'team': 'TAMPA BAY RAYS', 'position': 'P', 'player_id': 'woodhu01'}, {'display': 'Jedd Gyorko', 'team': 'ST LOUIS CARDINALS', 'position': '3B', 'player_id': 'gyorkje01'}, {'display': 'Jedd Gyorko', 'team': 'LOS ANGELES DODGERS', 'position': '3B', 'player_id': 'gyorkje01'}, {'display': 'Adalberto Mejía', 'team': 'ST LOUIS CARDINALS', 'position': 'P', 'player_id': 'mejiaad01'}, {'display': 'Adalberto Mejía', 'team': 'MINNESOTA TWINS', 'position': 'P', 'player_id': 'mejiaad01'}, {'display': 'Jesús Aguilar', 'team': 'MILWAUKEE BREWERS', 'position': '1B', 'player_id': 'aguilje01'}, {'display': 'Jesús Aguilar', 'team': 'TAMPA BAY RAYS', 'position': '1B', 'player_id': 'aguilje01'}, {'display': 'Tyler Austin', 'team': 'MILWAUKEE BREWERS', 'position': '1B', 'player_id': 'austity01'}, {'display': 'Tyler Austin', 'team': 'MINNESOTA TWINS', 'position': '1B', 'player_id': 'austity01'}, {'display': 'Jake Faria', 'team': 'MILWAUKEE BREWERS', 'position': 'P', 'player_id': 'fariaja01'}, {'display': 'Jake Faria', 'team': 'TAMPA BAY RAYS', 'position': 'P', 'player_id': 'fariaja01'}, {'display': 'Adeiny Hechavarría', 'team': 'NEW YORK METS', 'position': '2B', 'player_id': 'hechaad01'}, {'display': 'Adeiny Hechavarría', 'team': 'ATLANTA BRAVES', 'position': '2B', 'player_id': 'hechaad01'}, {'display': "Travis d'Arnaud", 'team': 'NEW YORK METS', 'position': 'C', 'player_id': 'darnatr01'}, {'display': "Travis d'Arnaud", 'team': 'LOS ANGELES DODGERS', 'position': 'C', 'player_id': 'darnatr01'}, {'display': 'Wilmer Font', 'team': 'NEW YORK METS', 'position': 'P', 'player_id': 'fontwi01'}, {'display': 'Wilmer Font', 'team': 'TAMPA BAY RAYS', 'position': 'P', 'player_id': 'fontwi01'}, {'display': 'Donnie Hart', 'team': 'NEW YORK METS', 'position': 'P', 'player_id': 'hartdo01'}, {'display': 'Donnie Hart', 'team': 'MILWAUKEE BREWERS', 'position': 'P', 'player_id': 'hartdo01'}, {'display': 'John Ryan Murphy', 'team': 'ARIZONA DIAMONDBACKS', 'position': 'C', 'player_id': 'murphjr01'}, {'display': 'John Ryan Murphy', 'team': 'ATLANTA BRAVES', 'position': 'C', 'player_id': 'murphjr01'}, {'display': 'Zack Greinke', 'team': 'ARIZONA DIAMONDBACKS', 'position': 'P', 'player_id': 'greinza01'}, {'display': 'Zack Greinke', 'team': 'HOUSTON ASTROS', 'position': 'P', 'player_id': 'greinza01'}, {'display': 'Blake Swihart', 'team': 'BOSTON RED SOX', 'position': 'OF', 'player_id': 'swihabl01'}, {'display': 'Blake Swihart', 'team': 'ARIZONA DIAMONDBACKS', 'position': 'OF', 'player_id': 'swihabl01'}, {'display': 'Josh Smith', 'team': 'BOSTON RED SOX', 'position': 'P', 'player_id': 'smithjo07'}, {'display': 'Josh Smith', 'team': 'CLEVELAND INDIANS', 'position': 'P', 'player_id': 'smithjo08'}, {'display': 'Jhoulys Chacín', 'team': 'BOSTON RED SOX', 'position': 'P', 'player_id': 'chacijh01'}, {'display': 'Jhoulys Chacín', 'team': 'MILWAUKEE BREWERS', 'position': 'P', 'player_id': 'chacijh01'}, {'display': 'Tony Kemp', 'team': 'CHICAGO CUBS', 'position': '2B', 'player_id': 'kempto01'}, {'display': 'Tony Kemp', 'team': 'HOUSTON ASTROS', 'position': '2B', 'player_id': 'kempto01'}, {'display': 'Carlos González', 'team': 'CHICAGO CUBS', 'position': 'OF', 'player_id': 'gonzaca01'}, {'display': 'Carlos González', 'team': 'CLEVELAND INDIANS', 'position': 'OF', 'player_id': 'gonzaca01'}, {'display': 'Martín Maldonado', 'team': 'CHICAGO CUBS', 'position': 'C', 'player_id': 'maldoma01'}, {'display': 'Martín Maldonado', 'team': 'HOUSTON ASTROS', 'position': 'C', 'player_id': 'maldoma01'}, {'display': 'Brad Brach', 'team': 'CHICAGO CUBS', 'position': 'P', 'player_id': 'brachbr01'}, {'display': 'Brad Brach', 'team': 'NEW YORK METS', 'position': 'P', 'player_id': 'brachbr01'}, {'display': 'Brad Miller', 'team': 'PHILADELPHIA PHILLIES', 'position': '2B', 'player_id': 'millebr02'}, {'display': 'Brad Miller', 'team': 'CLEVELAND INDIANS', 'position': '2B', 'player_id': 'millebr02'}, {'display': 'Aaron Altherr', 'team': 'PHILADELPHIA PHILLIES', 'position': 'OF', 'player_id': 'altheaa01'}, {'display': 'Aaron Altherr', 'team': 'NEW YORK METS', 'position': 'OF', 'player_id': 'altheaa01'}, {'display': 'Jason Vargas', 'team': 'PHILADELPHIA PHILLIES', 'position': 'P', 'player_id': 'vargaja01'}, {'display': 'Jason Vargas', 'team': 'NEW YORK METS', 'position': 'P', 'player_id': 'vargaja01'}, {'display': 'Blake Parker', 'team': 'PHILADELPHIA PHILLIES', 'position': 'P', 'player_id': 'parkebl01'}, {'display': 'Blake Parker', 'team': 'MINNESOTA TWINS', 'position': 'P', 'player_id': 'parkebl01'}, {'display': 'Mike Morin', 'team': 'PHILADELPHIA PHILLIES', 'position': 'P', 'player_id': 'morinmi01'}, {'display': 'Mike Morin', 'team': 'MINNESOTA TWINS', 'position': 'P', 'player_id': 'morinmi01'}, {'display': 'Asdrúbal Cabrera', 'team': 'TEXAS RANGERS', 'position': '3B', 'player_id': 'cabreas01'}, {'display': 'Asdrúbal Cabrera', 'team': 'WASHINGTON NATIONALS', 'position': '3B', 'player_id': 'cabreas01'}, {'display': 'Drew Smyly', 'team': 'TEXAS RANGERS', 'position': 'P', 'player_id': 'smylydr01'}, {'display': 'Drew Smyly', 'team': 'PHILADELPHIA PHILLIES', 'position': 'P', 'player_id': 'smylydr01'}, {'display': 'Ian Gibaut', 'team': 'TEXAS RANGERS', 'position': 'P', 'player_id': 'gibauia01'}, {'display': 'Ian Gibaut', 'team': 'TAMPA BAY RAYS', 'position': 'P', 'player_id': 'gibauia01'}, {'display': 'Peter Fairbanks', 'team': 'TEXAS RANGERS', 'position': 'P', 'player_id': 'fairbpe01'}, {'display': 'Peter Fairbanks', 'team': 'TAMPA BAY RAYS', 'position': 'P', 'player_id': 'fairbpe01'}, {'display': 'Jesse Biddle', 'team': 'TEXAS RANGERS', 'position': 'P', 'player_id': 'biddlje01'}, {'display': 'Jesse Biddle', 'team': 'ATLANTA BRAVES', 'position': 'P', 'player_id': 'biddlje01'}, {'display': 'Chris Martin', 'team': 'TEXAS RANGERS', 'position': 'P', 'player_id': 'martich02'}, {'display': 'Chris Martin', 'team': 'ATLANTA BRAVES', 'position': 'P', 'player_id': 'martich02'}, {'display': 'Joe Panik', 'team': 'SAN FRANCISCO GIANTS', 'position': '2B', 'player_id': 'panikjo01'}, {'display': 'Joe Panik', 'team': 'NEW YORK METS', 'position': '2B', 'player_id': 'panikjo01'}, {'display': 'Tyler Austin', 'team': 'SAN FRANCISCO GIANTS', 'position': '1B', 'player_id': 'austity01'}, {'display': 'Tyler Austin', 'team': 'MINNESOTA TWINS', 'position': '1B', 'player_id': 'austity01'}, {'display': 'Mauricio Dubon', 'team': 'SAN FRANCISCO GIANTS', 'position': 'SS', 'player_id': 'dubonma01'}, {'display': 'Mauricio Dubon', 'team': 'MILWAUKEE BREWERS', 'position': 'SS', 'player_id': 'dubonma01'}, {'display': 'Gerardo Parra', 'team': 'SAN FRANCISCO GIANTS', 'position': 'OF', 'player_id': 'parrage01'}, {'display': 'Gerardo Parra', 'team': 'WASHINGTON NATIONALS', 'position': 'OF', 'player_id': 'parrage01'}, {'display': 'Erik Kratz', 'team': 'SAN FRANCISCO GIANTS', 'position': 'C', 'player_id': 'kratzer01'}, {'display': 'Erik Kratz', 'team': 'TAMPA BAY RAYS', 'position': 'C', 'player_id': 'kratzer01'}, {'display': 'Corban Joseph', 'team': 'SAN FRANCISCO GIANTS', 'position': '2B', 'player_id': 'josepco01'}, {'display': 'Corban Joseph', 'team': 'OAKLAND ATHLETICS', 'position': '2B', 'player_id': 'josepco01'}, {'display': 'Aaron Altherr', 'team': 'SAN FRANCISCO GIANTS', 'position': 'OF', 'player_id': 'altheaa01'}, {'display': 'Aaron Altherr', 'team': 'NEW YORK METS', 'position': 'OF', 'player_id': 'altheaa01'}, {'display': 'Drew Pomeranz', 'team': 'SAN FRANCISCO GIANTS', 'position': 'P', 'player_id': 'pomerdr01'}, {'display': 'Drew Pomeranz', 'team': 'MILWAUKEE BREWERS', 'position': 'P', 'player_id': 'pomerdr01'}, {'display': 'Derek Holland', 'team': 'SAN FRANCISCO GIANTS', 'position': 'P', 'player_id': 'hollade01'}, {'display': 'Derek Holland', 'team': 'CHICAGO CUBS', 'position': 'P', 'player_id': 'hollade01'}, {'display': 'Nick Vincent', 'team': 'SAN FRANCISCO GIANTS', 'position': 'P', 'player_id': 'vinceni01'}, {'display': 'Nick Vincent', 'team': 'PHILADELPHIA PHILLIES', 'position': 'P', 'player_id': 'vinceni01'}, {'display': 'Will Smith', 'team': 'SAN FRANCISCO GIANTS', 'position': 'P', 'player_id': 'smithwi04'}, {'display': 'Will Smith', 'team': 'LOS ANGELES DODGERS', 'position': 'C', 'player_id': 'smithwi05'}, {'display': 'Kyle Barraclough', 'team': 'SAN FRANCISCO GIANTS', 'position': 'P', 'player_id': 'barraky01'}, {'display': 'Kyle Barraclough', 'team': 'WASHINGTON NATIONALS', 'position': 'P', 'player_id': 'barraky01'}, {'display': 'Burch Smith', 'team': 'SAN FRANCISCO GIANTS', 'position': 'P', 'player_id': 'smithbu03'}, {'display': 'Burch Smith', 'team': 'MILWAUKEE BREWERS', 'position': 'P', 'player_id': 'smithbu03'}, {'display': 'Ray Black', 'team': 'SAN FRANCISCO GIANTS', 'position': 'P', 'player_id': 'blackra01'}, {'display': 'Ray Black', 'team': 'MILWAUKEE BREWERS', 'position': 'P', 'player_id': 'blackra01'}, {'display': 'Mark Melancon', 'team': 'SAN FRANCISCO GIANTS', 'position': 'P', 'player_id': 'melanma01'}, {'display': 'Mark Melancon', 'team': 'ATLANTA BRAVES', 'position': 'P', 'player_id': 'melanma01'}, {'display': 'Sam Dyson', 'team': 'SAN FRANCISCO GIANTS', 'position': 'P', 'player_id': 'dysonsa01'}, {'display': 'Sam Dyson', 'team': 'MINNESOTA TWINS', 'position': 'P', 'player_id': 'dysonsa01'}, {'display': 'Yasiel Puig', 'team': 'CINCINNATI REDS', 'position': 'OF', 'player_id': 'puigya01'}, {'display': 'Yasiel Puig', 'team': 'CLEVELAND INDIANS', 'position': 'OF', 'player_id': 'puigya01'}, {'display': 'Scooter Gennett', 'team': 'CINCINNATI REDS', 'position': '2B', 'player_id': 'gennesc01'}, {'display': 'Scooter Gennett', 'team': 'SAN FRANCISCO GIANTS', 'position': '2B', 'player_id': 'gennesc01'}, {'display': 'Tanner Roark', 'team': 'CINCINNATI REDS', 'position': 'P', 'player_id': 'roarkta01'}, {'display': 'Tanner Roark', 'team': 'OAKLAND ATHLETICS', 'position': 'P', 'player_id': 'roarkta01'}, {'display': 'Trevor Bauer', 'team': 'CINCINNATI REDS', 'position': 'P', 'player_id': 'bauertr01'}, {'display': 'Trevor Bauer', 'team': 'CLEVELAND INDIANS', 'position': 'P', 'player_id': 'bauertr01'}, {'display': 'Jared Hughes', 'team': 'CINCINNATI REDS', 'position': 'P', 'player_id': 'hugheja02'}, {'display': 'Jared Hughes', 'team': 'PHILADELPHIA PHILLIES', 'position': 'P', 'player_id': 'hugheja02'}, {'display': 'Wandy Peralta', 'team': 'CINCINNATI REDS', 'position': 'P', 'player_id': 'peralwa01'}, {'display': 'Wandy Peralta', 'team': 'SAN FRANCISCO GIANTS', 'position': 'P', 'player_id': 'peralwa01'}, {'display': 'Kevin Gausman', 'team': 'CINCINNATI REDS', 'position': 'P', 'player_id': 'gausmke01'}, {'display': 'Kevin Gausman', 'team': 'ATLANTA BRAVES', 'position': 'P', 'player_id': 'gausmke01'}, {'display': 'Héctor Santiago', 'team': 'CHICAGO WHITE SOX', 'position': 'P', 'player_id': 'santihe01'}, {'display': 'Héctor Santiago', 'team': 'NEW YORK METS', 'position': 'P', 'player_id': 'santihe01'}, {'display': 'Jonathan Lucroy', 'team': 'LOS ANGELES ANGELS', 'position': 'C', 'player_id': 'lucrojo01'}, {'display': 'Jonathan Lucroy', 'team': 'CHICAGO CUBS', 'position': 'C', 'player_id': 'lucrojo01'}, {'display': 'Dustin Garneau', 'team': 'LOS ANGELES ANGELS', 'position': 'C', 'player_id': 'garnedu01'}, {'display': 'Dustin Garneau', 'team': 'OAKLAND ATHLETICS', 'position': 'C', 'player_id': 'garnedu01'}, {'display': 'Anthony Bemboom', 'team': 'LOS ANGELES ANGELS', 'position': 'C', 'player_id': 'bemboan01'}, {'display': 'Anthony Bemboom', 'team': 'TAMPA BAY RAYS', 'position': 'C', 'player_id': 'bemboan01'}, {'display': 'Max Stassi', 'team': 'LOS ANGELES ANGELS', 'position': 'C', 'player_id': 'stassma01'}, {'display': 'Max Stassi', 'team': 'HOUSTON ASTROS', 'position': 'C', 'player_id': 'stassma01'}, {'display': 'Kean Wong', 'team': 'LOS ANGELES ANGELS', 'position': '2B', 'player_id': 'wongke01'}, {'display': 'Kean Wong', 'team': 'TAMPA BAY RAYS', 'position': '2B', 'player_id': 'wongke01'}, {'display': 'Adalberto Mejía', 'team': 'LOS ANGELES ANGELS', 'position': 'P', 'player_id': 'mejiaad01'}, {'display': 'Adalberto Mejía', 'team': 'MINNESOTA TWINS', 'position': 'P', 'player_id': 'mejiaad01'}, {'display': 'Yonder Alonso', 'team': 'COLORADO ROCKIES', 'position': '1B', 'player_id': 'alonsyo01'}, {'display': 'Yonder Alonso', 'team': 'CHICAGO WHITE SOX', 'position': '1B', 'player_id': 'alonsyo01'}, {'display': 'Wes Parsons', 'team': 'COLORADO ROCKIES', 'position': 'P', 'player_id': 'parsowe01'}, {'display': 'Wes Parsons', 'team': 'ATLANTA BRAVES', 'position': 'P', 'player_id': 'parsowe01'}, {'display': 'Joe Harvey', 'team': 'COLORADO ROCKIES', 'position': 'P', 'player_id': 'harvejo01'}, {'display': 'Joe Harvey', 'team': 'NEW YORK YANKEES', 'position': 'P', 'player_id': 'harvejo01'}, {'display': 'Franmil Reyes', 'team': 'SAN DIEGO PADRES', 'position': 'OF', 'player_id': 'reyesfr01'}, {'display': 'Franmil Reyes', 'team': 'CLEVELAND INDIANS', 'position': 'OF', 'player_id': 'reyesfr01'}, {'display': 'Nick Martini', 'team': 'SAN DIEGO PADRES', 'position': 'OF', 'player_id': 'martini02'}, {'display': 'Nick Martini', 'team': 'OAKLAND ATHLETICS', 'position': 'OF', 'player_id': 'martini02'}, {'display': 'Alex Dickerson', 'team': 'SAN DIEGO PADRES', 'position': 'OF', 'player_id': 'dickeal01'}, {'display': 'Alex Dickerson', 'team': 'SAN FRANCISCO GIANTS', 'position': 'OF', 'player_id': 'dickeal01'}, {'display': 'José Pirela', 'team': 'SAN DIEGO PADRES', 'position': 'OF', 'player_id': 'pireljo01'}, {'display': 'José Pirela', 'team': 'PHILADELPHIA PHILLIES', 'position': 'OF', 'player_id': 'pireljo01'}, {'display': 'Logan Allen', 'team': 'SAN DIEGO PADRES', 'position': 'P', 'player_id': 'allenlo01'}, {'display': 'Logan Allen', 'team': 'CLEVELAND INDIANS', 'position': 'P', 'player_id': 'allenlo01'}, {'display': 'Phil Maton', 'team': 'SAN DIEGO PADRES', 'position': 'P', 'player_id': 'matonph01'}, {'display': 'Phil Maton', 'team': 'CLEVELAND INDIANS', 'position': 'P', 'player_id': 'matonph01'}, {'display': 'Brad Wieck', 'team': 'SAN DIEGO PADRES', 'position': 'P', 'player_id': 'wieckbr01'}, {'display': 'Brad Wieck', 'team': 'CHICAGO CUBS', 'position': 'P', 'player_id': 'wieckbr01'}, {'display': 'Carl Edwards Jr.', 'team': 'SAN DIEGO PADRES', 'position': 'P', 'player_id': 'edwarca01'}, {'display': 'Carl Edwards Jr.', 'team': 'CHICAGO CUBS', 'position': 'P', 'player_id': 'edwarca01'}, {'display': 'Javy Guerra', 'team': 'SAN DIEGO PADRES', 'position': 'P', 'player_id': 'guerrja02'}, {'display': 'Javy Guerra', 'team': 'WASHINGTON NATIONALS', 'position': 'P', 'player_id': 'guerrja01'}, {'display': 'Corey Dickerson', 'team': 'PITTSBURGH PIRATES', 'position': 'OF', 'player_id': 'dickeco01'}, {'display': 'Corey Dickerson', 'team': 'PHILADELPHIA PHILLIES', 'position': 'OF', 'player_id': 'dickeco01'}, {'display': 'Francisco Cervelli', 'team': 'PITTSBURGH PIRATES', 'position': 'C', 'player_id': 'cervefr01'}, {'display': 'Francisco Cervelli', 'team': 'ATLANTA BRAVES', 'position': 'C', 'player_id': 'cervefr01'}, {'display': 'Corban Joseph', 'team': 'PITTSBURGH PIRATES', 'position': '2B', 'player_id': 'josepco01'}, {'display': 'Corban Joseph', 'team': 'OAKLAND ATHLETICS', 'position': '2B', 'player_id': 'josepco01'}, {'display': 'Jordan Lyles', 'team': 'PITTSBURGH PIRATES', 'position': 'P', 'player_id': 'lylesjo01'}, {'display': 'Jordan Lyles', 'team': 'MILWAUKEE BREWERS', 'position': 'P', 'player_id': 'lylesjo01'}, {'display': 'Chris Stratton', 'team': 'PITTSBURGH PIRATES', 'position': 'P', 'player_id': 'stratch01'}, {'display': 'Chris Stratton', 'team': 'LOS ANGELES ANGELS', 'position': 'P', 'player_id': 'stratch01'}, {'display': 'Tyler Lyons', 'team': 'PITTSBURGH PIRATES', 'position': 'P', 'player_id': 'lyonsty01'}, {'display': 'Tyler Lyons', 'team': 'NEW YORK YANKEES', 'position': 'P', 'player_id': 'lyonsty01'}, {'display': 'Wei-Chung Wang', 'team': 'PITTSBURGH PIRATES', 'position': 'P', 'player_id': 'wangwe01'}, {'display': 'Wei-Chung Wang', 'team': 'OAKLAND ATHLETICS', 'position': 'P', 'player_id': 'wangwe01'}, {'display': 'Williams Jerez', 'team': 'PITTSBURGH PIRATES', 'position': 'P', 'player_id': 'jerezwi01'}, {'display': 'Williams Jerez', 'team': 'SAN FRANCISCO GIANTS', 'position': 'P', 'player_id': 'jerezwi01'}, {'display': 'Yacksel Ríos', 'team': 'PITTSBURGH PIRATES', 'position': 'P', 'player_id': 'riosya01'}, {'display': 'Yacksel Ríos', 'team': 'PHILADELPHIA PHILLIES', 'position': 'P', 'player_id': 'riosya01'}, {'display': 'Edwin Encarnación', 'team': 'SEATTLE MARINERS', 'position': '1B', 'player_id': 'encared01'}, {'display': 'Edwin Encarnación', 'team': 'NEW YORK YANKEES', 'position': '1B', 'player_id': 'encared01'}, {'display': 'Jay Bruce', 'team': 'SEATTLE MARINERS', 'position': 'OF', 'player_id': 'bruceja01'}, {'display': 'Jay Bruce', 'team': 'PHILADELPHIA PHILLIES', 'position': 'OF', 'player_id': 'bruceja01'}, {'display': 'Mac Williamson', 'team': 'SEATTLE MARINERS', 'position': 'OF', 'player_id': 'willima11'}, {'display': 'Mac Williamson', 'team': 'SAN FRANCISCO GIANTS', 'position': 'OF', 'player_id': 'willima11'}, {'display': 'Keon Broxton', 'team': 'SEATTLE MARINERS', 'position': 'OF', 'player_id': 'broxtke01'}, {'display': 'Keon Broxton', 'team': 'NEW YORK METS', 'position': 'OF', 'player_id': 'broxtke01'}, {'display': 'Kristopher Negrón', 'team': 'SEATTLE MARINERS', 'position': 'OF', 'player_id': 'negrokr01'}, {'display': 'Kristopher Negrón', 'team': 'LOS ANGELES DODGERS', 'position': 'OF', 'player_id': 'negrokr01'}, {'display': 'David Freitas', 'team': 'SEATTLE MARINERS', 'position': 'C', 'player_id': 'freitda01'}, {'display': 'David Freitas', 'team': 'MILWAUKEE BREWERS', 'position': 'C', 'player_id': 'freitda01'}, {'display': 'Mike Leake', 'team': 'SEATTLE MARINERS', 'position': 'P', 'player_id': 'leakemi01'}, {'display': 'Mike Leake', 'team': 'ARIZONA DIAMONDBACKS', 'position': 'P', 'player_id': 'leakemi01'}, {'display': 'Austin Adams', 'team': 'SEATTLE MARINERS', 'position': 'P', 'player_id': 'adamsau02'}, {'display': 'Austin Adams', 'team': 'MINNESOTA TWINS', 'position': 'P', 'player_id': 'adamsau01'}, {'display': 'Parker Markel', 'team': 'SEATTLE MARINERS', 'position': 'P', 'player_id': 'markepa01'}, {'display': 'Parker Markel', 'team': 'PITTSBURGH PIRATES', 'position': 'P', 'player_id': 'markepa01'}, {'display': 'Cory Gearrin', 'team': 'SEATTLE MARINERS', 'position': 'P', 'player_id': 'gearrco01'}, {'display': 'Cory Gearrin', 'team': 'NEW YORK YANKEES', 'position': 'P', 'player_id': 'gearrco01'}, {'display': 'Matt Magill', 'team': 'SEATTLE MARINERS', 'position': 'P', 'player_id': 'magilma01'}, {'display': 'Matt Magill', 'team': 'MINNESOTA TWINS', 'position': 'P', 'player_id': 'magilma01'}, {'display': 'Roenis Elías', 'team': 'SEATTLE MARINERS', 'position': 'P', 'player_id': 'eliasro01'}, {'display': 'Roenis Elías', 'team': 'WASHINGTON NATIONALS', 'position': 'P', 'player_id': 'eliasro01'}, {'display': 'Zac Rosscup', 'team': 'SEATTLE MARINERS', 'position': 'P', 'player_id': 'rosscza01'}, {'display': 'Zac Rosscup', 'team': 'LOS ANGELES DODGERS', 'position': 'P', 'player_id': 'rosscza01'}, {'display': 'Jesse Biddle', 'team': 'SEATTLE MARINERS', 'position': 'P', 'player_id': 'biddlje01'}, {'display': 'Jesse Biddle', 'team': 'ATLANTA BRAVES', 'position': 'P', 'player_id': 'biddlje01'}, {'display': 'Matt Wisler', 'team': 'SEATTLE MARINERS', 'position': 'P', 'player_id': 'wislema01'}, {'display': 'Matt Wisler', 'team': 'SAN DIEGO PADRES', 'position': 'P', 'player_id': 'wislema01'}, {'display': 'R.J. Alaniz', 'team': 'SEATTLE MARINERS', 'position': 'P', 'player_id': 'alanirj01'}, {'display': 'R.J. Alaniz', 'team': 'CINCINNATI REDS', 'position': 'P', 'player_id': 'alanirj01'}, {'display': 'Hunter Strickland', 'team': 'SEATTLE MARINERS', 'position': 'P', 'player_id': 'strichu01'}, {'display': 'Hunter Strickland', 'team': 'WASHINGTON NATIONALS', 'position': 'P', 'player_id': 'strichu01'}, {'display': 'Anthony Swarzak', 'team': 'SEATTLE MARINERS', 'position': 'P', 'player_id': 'swarzan01'}, {'display': 'Anthony Swarzak', 'team': 'ATLANTA BRAVES', 'position': 'P', 'player_id': 'swarzan01'}, {'display': 'Freddy Galvis', 'team': 'TORONTO BLUE JAYS', 'position': 'SS', 'player_id': 'galvifr01'}, {'display': 'Freddy Galvis', 'team': 'CINCINNATI REDS', 'position': 'SS', 'player_id': 'galvifr01'}, {'display': 'Eric Sogard', 'team': 'TORONTO BLUE JAYS', 'position': '2B', 'player_id': 'sogarer01'}, {'display': 'Eric Sogard', 'team': 'TAMPA BAY RAYS', 'position': '2B', 'player_id': 'sogarer01'}, {'display': 'Derek Fisher', 'team': 'TORONTO BLUE JAYS', 'position': 'OF', 'player_id': 'fishede01'}, {'display': 'Derek Fisher', 'team': 'HOUSTON ASTROS', 'position': 'OF', 'player_id': 'fishede01'}, {'display': 'Kevin Pillar', 'team': 'TORONTO BLUE JAYS', 'position': 'OF', 'player_id': 'pillake01'}, {'display': 'Kevin Pillar', 'team': 'SAN FRANCISCO GIANTS', 'position': 'OF', 'player_id': 'pillake01'}, {'display': 'Breyvic Valera', 'team': 'TORONTO BLUE JAYS', 'position': '2B', 'player_id': 'valerbr01'}, {'display': 'Breyvic Valera', 'team': 'NEW YORK YANKEES', 'position': '2B', 'player_id': 'valerbr01'}, {'display': 'Beau Taylor', 'team': 'TORONTO BLUE JAYS', 'position': 'C', 'player_id': 'taylobe11'}, {'display': 'Beau Taylor', 'team': 'OAKLAND ATHLETICS', 'position': 'C', 'player_id': 'taylobe11'}, {'display': 'Aaron Sanchez', 'team': 'TORONTO BLUE JAYS', 'position': 'P', 'player_id': 'sanchaa01'}, {'display': 'Aaron Sanchez', 'team': 'HOUSTON ASTROS', 'position': 'P', 'player_id': 'sanchaa01'}, {'display': 'Marcus Stroman', 'team': 'TORONTO BLUE JAYS', 'position': 'P', 'player_id': 'stromma01'}, {'display': 'Marcus Stroman', 'team': 'NEW YORK METS', 'position': 'P', 'player_id': 'stromma01'}, {'display': 'Zack Godley', 'team': 'TORONTO BLUE JAYS', 'position': 'P', 'player_id': 'godleza01'}, {'display': 'Zack Godley', 'team': 'ARIZONA DIAMONDBACKS', 'position': 'P', 'player_id': 'godleza01'}, {'display': 'Joe Biagini', 'team': 'TORONTO BLUE JAYS', 'position': 'P', 'player_id': 'biagijo01'}, {'display': 'Joe Biagini', 'team': 'HOUSTON ASTROS', 'position': 'P', 'player_id': 'biagijo01'}, {'display': 'Neil Ramírez', 'team': 'TORONTO BLUE JAYS', 'position': 'P', 'player_id': 'ramirne01'}, {'display': 'Neil Ramírez', 'team': 'CLEVELAND INDIANS', 'position': 'P', 'player_id': 'ramirne01'}, {'display': 'Javy Guerra', 'team': 'TORONTO BLUE JAYS', 'position': 'P', 'player_id': 'guerrja01'}, {'display': 'Javy Guerra', 'team': 'WASHINGTON NATIONALS', 'position': 'P', 'player_id': 'guerrja01'}, {'display': 'Jimmy Cordero', 'team': 'TORONTO BLUE JAYS', 'position': 'P', 'player_id': 'cordeji01'}, {'display': 'Jimmy Cordero', 'team': 'CHICAGO WHITE SOX', 'position': 'P', 'player_id': 'cordeji01'}, {'display': 'Brock Stewart', 'team': 'TORONTO BLUE JAYS', 'position': 'P', 'player_id': 'stewabr01'}, {'display': 'Brock Stewart', 'team': 'LOS ANGELES DODGERS', 'position': 'P', 'player_id': 'stewabr01'}, {'display': 'Nick Kingham', 'team': 'TORONTO BLUE JAYS', 'position': 'P', 'player_id': 'kinghni01'}, {'display': 'Nick Kingham', 'team': 'PITTSBURGH PIRATES', 'position': 'P', 'player_id': 'kinghni01'}, {'display': 'Ryan Dull', 'team': 'TORONTO BLUE JAYS', 'position': 'P', 'player_id': 'dullry01'}, {'display': 'Ryan Dull', 'team': 'NEW YORK YANKEES', 'position': 'P', 'player_id': 'dullry01'}, {'display': 'David Phelps', 'team': 'TORONTO BLUE JAYS', 'position': 'P', 'player_id': 'phelpda01'}, {'display': 'David Phelps', 'team': 'CHICAGO CUBS', 'position': 'P', 'player_id': 'phelpda01'}, {'display': 'Wilmer Font', 'team': 'TORONTO BLUE JAYS', 'position': 'P', 'player_id': 'fontwi01'}, {'display': 'Wilmer Font', 'team': 'TAMPA BAY RAYS', 'position': 'P', 'player_id': 'fontwi01'}, {'display': 'Zac Rosscup', 'team': 'TORONTO BLUE JAYS', 'position': 'P', 'player_id': 'rosscza01'}, {'display': 'Zac Rosscup', 'team': 'LOS ANGELES DODGERS', 'position': 'P', 'player_id': 'rosscza01'}, {'display': 'Daniel Hudson', 'team': 'TORONTO BLUE JAYS', 'position': 'P', 'player_id': 'hudsoda01'}, {'display': 'Daniel Hudson', 'team': 'WASHINGTON NATIONALS', 'position': 'P', 'player_id': 'hudsoda01'}, {'display': 'Martín Maldonado', 'team': 'KANSAS CITY ROYALS', 'position': 'C', 'player_id': 'maldoma01'}, {'display': 'Martín Maldonado', 'team': 'HOUSTON ASTROS', 'position': 'C', 'player_id': 'maldoma01'}, {'display': 'Billy Hamilton', 'team': 'KANSAS CITY ROYALS', 'position': 'OF', 'player_id': 'hamilbi02'}, {'display': 'Billy Hamilton', 'team': 'ATLANTA BRAVES', 'position': 'OF', 'player_id': 'hamilbi02'}, {'display': 'Chris Owings', 'team': 'KANSAS CITY ROYALS', 'position': '2B', 'player_id': 'owingch01'}, {'display': 'Chris Owings', 'team': 'BOSTON RED SOX', 'position': '2B', 'player_id': 'owingch01'}, {'display': 'Homer Bailey', 'team': 'KANSAS CITY ROYALS', 'position': 'P', 'player_id': 'baileho02'}, {'display': 'Homer Bailey', 'team': 'OAKLAND ATHLETICS', 'position': 'P', 'player_id': 'baileho02'}, {'display': 'Mike Montgomery', 'team': 'KANSAS CITY ROYALS', 'position': 'P', 'player_id': 'montgmi01'}, {'display': 'Mike Montgomery', 'team': 'CHICAGO CUBS', 'position': 'P', 'player_id': 'montgmi01'}, {'display': 'Randy Rosario', 'team': 'KANSAS CITY ROYALS', 'position': 'P', 'player_id': 'rosarra01'}, {'display': 'Randy Rosario', 'team': 'CHICAGO CUBS', 'position': 'P', 'player_id': 'rosarra01'}, {'display': 'Jake Diekman', 'team': 'KANSAS CITY ROYALS', 'position': 'P', 'player_id': 'diekmja01'}, {'display': 'Jake Diekman', 'team': 'OAKLAND ATHLETICS', 'position': 'P', 'player_id': 'diekmja01'}, {'display': 'Jacob Barnes', 'team': 'KANSAS CITY ROYALS', 'position': 'P', 'player_id': 'barneja01'}, {'display': 'Jacob Barnes', 'team': 'MILWAUKEE BREWERS', 'position': 'P', 'player_id': 'barneja01'}, {'display': 'César Puello', 'team': 'MIAMI MARLINS', 'position': 'OF', 'player_id': 'puellce01'}, {'display': 'César Puello', 'team': 'LOS ANGELES ANGELS', 'position': 'OF', 'player_id': 'puellce01'}, {'display': 'Trevor Richards', 'team': 'MIAMI MARLINS', 'position': 'P', 'player_id': 'richatr01'}, {'display': 'Trevor Richards', 'team': 'TAMPA BAY RAYS', 'position': 'P', 'player_id': 'richatr01'}, {'display': 'Zac Gallen', 'team': 'MIAMI MARLINS', 'position': 'P', 'player_id': 'galleza01'}, {'display': 'Zac Gallen', 'team': 'ARIZONA DIAMONDBACKS', 'position': 'P', 'player_id': 'galleza01'}, {'display': 'Josh Smith', 'team': 'MIAMI MARLINS', 'position': 'P', 'player_id': 'smithjo08'}, {'display': 'Josh Smith', 'team': 'CLEVELAND INDIANS', 'position': 'P', 'player_id': 'smithjo08'}, {'display': 'Ryne Stanek', 'team': 'MIAMI MARLINS', 'position': 'P', 'player_id': 'stanery01'}, {'display': 'Ryne Stanek', 'team': 'TAMPA BAY RAYS', 'position': 'P', 'player_id': 'stanery01'}, {'display': 'Sergio Romo', 'team': 'MIAMI MARLINS', 'position': 'P', 'player_id': 'romose01'}, {'display': 'Sergio Romo', 'team': 'MINNESOTA TWINS', 'position': 'P', 'player_id': 'romose01'}, {'display': 'Nick Anderson', 'team': 'MIAMI MARLINS', 'position': 'P', 'player_id': 'anderni01'}, {'display': 'Nick Anderson', 'team': 'TAMPA BAY RAYS', 'position': 'P', 'player_id': 'anderni01'}, {'display': 'Joey Rickard', 'team': 'BALTIMORE ORIOLES', 'position': 'OF', 'player_id': 'rickajo01'}, {'display': 'Joey Rickard', 'team': 'SAN FRANCISCO GIANTS', 'position': 'OF', 'player_id': 'rickajo01'}, {'display': 'Keon Broxton', 'team': 'BALTIMORE ORIOLES', 'position': 'OF', 'player_id': 'broxtke01'}, {'display': 'Keon Broxton', 'team': 'NEW YORK METS', 'position': 'OF', 'player_id': 'broxtke01'}, {'display': 'José Rondón', 'team': 'BALTIMORE ORIOLES', 'position': '3B', 'player_id': 'rondojo02'}, {'display': 'José Rondón', 'team': 'CHICAGO WHITE SOX', 'position': '3B', 'player_id': 'rondojo02'}, {'display': 'Aaron Brooks', 'team': 'BALTIMORE ORIOLES', 'position': 'P', 'player_id': 'brookaa01'}, {'display': 'Aaron Brooks', 'team': 'OAKLAND ATHLETICS', 'position': 'P', 'player_id': 'brookaa01'}, {'display': 'Andrew Cashner', 'team': 'BALTIMORE ORIOLES', 'position': 'P', 'player_id': 'cashnan01'}, {'display': 'Andrew Cashner', 'team': 'BOSTON RED SOX', 'position': 'P', 'player_id': 'cashnan01'}, {'display': 'Tayler Scott', 'team': 'BALTIMORE ORIOLES', 'position': 'P', 'player_id': 'scottta02'}, {'display': 'Tayler Scott', 'team': 'SEATTLE MARINERS', 'position': 'P', 'player_id': 'scottta02'}, {'display': 'Ryan Eades', 'team': 'BALTIMORE ORIOLES', 'position': 'P', 'player_id': 'eadesry01'}, {'display': 'Ryan Eades', 'team': 'MINNESOTA TWINS', 'position': 'P', 'player_id': 'eadesry01'}, {'display': 'Yefry Ramirez', 'team': 'BALTIMORE ORIOLES', 'position': 'P', 'player_id': 'ramirye01'}, {'display': 'Yefry Ramirez', 'team': 'PITTSBURGH PIRATES', 'position': 'P', 'player_id': 'ramirye01'}, {'display': 'Ty Blach', 'team': 'BALTIMORE ORIOLES', 'position': 'P', 'player_id': 'blachty01'}, {'display': 'Ty Blach', 'team': 'SAN FRANCISCO GIANTS', 'position': 'P', 'player_id': 'blachty01'}, {'display': 'Shawn Armstrong', 'team': 'BALTIMORE ORIOLES', 'position': 'P', 'player_id': 'armstsh01'}, {'display': 'Shawn Armstrong', 'team': 'SEATTLE MARINERS', 'position': 'P', 'player_id': 'armstsh01'}, {'display': 'Mike Wright', 'team': 'BALTIMORE ORIOLES', 'position': 'P', 'player_id': 'wrighmi01'}, {'display': 'Mike Wright', 'team': 'SEATTLE MARINERS', 'position': 'P', 'player_id': 'wrighmi01'}, {'display': 'Nicholas Castellanos', 'team': 'DETROIT TIGERS', 'position': 'OF', 'player_id': 'casteni01'}, {'display': 'Nicholas Castellanos', 'team': 'CHICAGO CUBS', 'position': 'OF', 'player_id': 'casteni01'}, {'display': 'Trevor Rosenthal', 'team': 'DETROIT TIGERS', 'position': 'P', 'player_id': 'rosentr01'}, {'display': 'Trevor Rosenthal', 'team': 'WASHINGTON NATIONALS', 'position': 'P', 'player_id': 'rosentr01'}, {'display': 'Austin Adams', 'team': 'DETROIT TIGERS', 'position': 'P', 'player_id': 'adamsau01'}, {'display': 'Austin Adams', 'team': 'MINNESOTA TWINS', 'position': 'P', 'player_id': 'adamsau01'}, {'display': 'Edwin Jackson', 'team': 'DETROIT TIGERS', 'position': 'P', 'player_id': 'jacksed01'}, {'display': 'Edwin Jackson', 'team': 'TORONTO BLUE JAYS', 'position': 'P', 'player_id': 'jacksed01'}, {'display': 'Shane Greene', 'team': 'DETROIT TIGERS', 'position': 'P', 'player_id': 'greensh02'}, {'display': 'Shane Greene', 'team': 'ATLANTA BRAVES', 'position': 'P', 'player_id': 'greensh02'}, {'display': 'David McKay', 'team': 'DETROIT TIGERS', 'position': 'P', 'player_id': 'mckayda02'}, {'display': 'David McKay', 'team': 'SEATTLE MARINERS', 'position': 'P', 'player_id': 'mckayda02'}]
# [[{'display': 'Chase Hansen', 'team': 'NEW ORLEANS SAINTS', 'position': '', 'player_id': 'HansCh02'}, {'display': 'Chase Hansen', 'team': 'BALTIMORE RAVENS', 'position': '', 'player_id': 'HansCh02'}, {'display': 'Chris Jones', 'team': 'DALLAS COWBOYS', 'position': '', 'player_id': 'JoneCh02'}, {'display': 'Chris Jones', 'team': 'KANSAS CITY CHIEFS', 'position': '', 'player_id': 'JoneCh09'}, {'display': 'Brian Allen', 'team': 'LOS ANGELES RAMS', 'position': '', 'player_id': 'AlleBr02'}, {'display': 'Brian Allen', 'team': 'SEATTLE SEAHAWKS', 'position': '', 'player_id': 'AlleBr01'}, {'display': 'David Long', 'team': 'LOS ANGELES RAMS', 'position': '', 'player_id': 'LongDa02'}, {'display': 'David Long', 'team': 'TENNESSEE TITANS', 'position': '', 'player_id': 'LongDa04'}, {'display': 'Michael Thomas', 'team': 'HOUSTON TEXANS', 'position': '', 'player_id': 'ThomMi02'}, {'display': 'Michael Thomas', 'team': 'NEW ORLEANS SAINTS', 'position': 'WR', 'player_id': 'ThomMi05'}, {'display': 'Mazzi Wilkins', 'team': 'GREEN BAY PACKERS', 'position': '', 'player_id': 'WilkMa00'}, {'display': 'Mazzi Wilkins', 'team': 'TAMPA BAY BUCCANEERS', 'position': '', 'player_id': 'WilkMa00'}, {'display': 'Chris Jones', 'team': 'ARIZONA CARDINALS', 'position': '', 'player_id': 'JoneCh06'}, {'display': 'Chris Jones', 'team': 'KANSAS CITY CHIEFS', 'position': '', 'player_id': 'JoneCh09'}, {'display': 'Brandon Williams', 'team': 'ARIZONA CARDINALS', 'position': '', 'player_id': 'WillBr07'}, {'display': 'Brandon Williams', 'team': 'BALTIMORE RAVENS', 'position': '', 'player_id': 'WillBr02'}, {'display': 'Deone Bucannon', 'team': 'NEW YORK GIANTS', 'position': '', 'player_id': 'BucaDe00'}, {'display': 'Deone Bucannon', 'team': 'ATLANTA FALCONS', 'position': '', 'player_id': 'BucaDe00'}, {'display': 'Cameron Fleming', 'team': 'NEW YORK GIANTS', 'position': '', 'player_id': 'FlemCa00'}, {'display': 'Cameron Fleming', 'team': 'DALLAS COWBOYS', 'position': '', 'player_id': 'FlemCa00'}, {'display': 'Andre Smith', 'team': 'CAROLINA PANTHERS', 'position': '', 'player_id': 'SmitAn04'}, {'display': 'Andre Smith', 'team': 'BALTIMORE RAVENS', 'position': '', 'player_id': 'SmitAn23'}, {'display': 'Dylan Cantrell', 'team': 'LOS ANGELES CHARGERS', 'position': '', 'player_id': 'CantDy00'}, {'display': 'Dylan Cantrell', 'team': 'ARIZONA CARDINALS', 'position': '', 'player_id': 'CantDy00'}, {'display': 'Isaiah Johnson', 'team': 'OAKLAND RAIDERS', 'position': '', 'player_id': 'JohnIs02'}, {'display': 'Isaiah Johnson', 'team': 'INDIANAPOLIS COLTS', 'position': '', 'player_id': 'JohnIs01'}, {'display': 'Jayson Stanley', 'team': 'JACKSONVILLE JAGUARS', 'position': '', 'player_id': 'StanJa00'}, {'display': 'Jayson Stanley', 'team': 'SEATTLE SEAHAWKS', 'position': '', 'player_id': 'StanJa00'}, {'display': 'Chris Thompson', 'team': 'JACKSONVILLE JAGUARS', 'position': 'RB', 'player_id': 'ThomCh03'}, {'display': 'Chris Thompson', 'team': 'SAN FRANCISCO 49ERS', 'position': 'WR', 'player_id': 'ThomCh05'}, {'display': 'Josh Allen', 'team': 'JACKSONVILLE JAGUARS', 'position': '', 'player_id': 'AlleJo03'}, {'display': 'Josh Allen', 'team': 'BUFFALO BILLS', 'position': 'QB', 'player_id': 'AlleJo02'}, {'display': 'Devontae Booker', 'team': 'DENVER BRONCOS', 'position': 'RB', 'player_id': 'BookDe00'}, {'display': 'Devontae Booker', 'team': 'OAKLAND RAIDERS', 'position': 'RB', 'player_id': 'BookDe00'}, {'display': 'Kyle Fuller', 'team': 'CHICAGO BEARS', 'position': '', 'player_id': 'FullKy00'}, {'display': 'Kyle Fuller', 'team': 'SEATTLE SEAHAWKS', 'position': '', 'player_id': 'FullKy01'}, {'display': 'Connor McGovern', 'team': 'NEW YORK JETS', 'position': '', 'player_id': 'McGoCo00'}, {'display': 'Connor McGovern', 'team': 'DALLAS COWBOYS', 'position': '', 'player_id': 'McGoCo01'}, {'display': 'Ryan Griffin', 'team': 'NEW YORK JETS', 'position': 'TE', 'player_id': 'GrifRy00'}, {'display': 'Ryan Griffin', 'team': 'TAMPA BAY BUCCANEERS', 'position': 'QB', 'player_id': 'GrifRy01'}, {'display': 'Mike Liedtke', 'team': 'WASHINGTON REDSKINS', 'position': '', 'player_id': 'LiedMi00'}, {'display': 'Mike Liedtke', 'team': 'TAMPA BAY BUCCANEERS', 'position': '', 'player_id': 'LiedMi00'}], [], []]