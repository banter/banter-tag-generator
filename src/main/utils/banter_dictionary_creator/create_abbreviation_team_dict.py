import json
import os
from os.path import dirname, realpath

from src.main.utils.nlp_conversion_util import NLPConversionUtil

nfl_abreviations = {
    "ARI": "Arizona Cardinals",
    "ATL": "Atlanta Falcons",
    "BAL": "Baltimore Ravens",
    "BUF": "Buffalo Bills",
    "CAR": "Carolina Panthers",
    "CHI": "Chicago Bears",
    "CIN": "Cincinnati Bengals",
    "CLE": "Cleveland Browns",
    "DAL": "Dallas Cowboys",
    "DEN": "Denver Broncos",
    "DET": "Detroit Lions",
    "GB": "Green Bay Packers",
    "HOU": "Houston Texans",
    "IND": "Indianapolis Colts",
    "JAX": "Jacksonville Jaguars",
    "KC": "Kansas City Chiefs",
    "MIA": "Miami Dolphins",
    "MIN": "Minnesota Vikings",
    "NE": "New England Patriots",
    "NO": "New Orleans Saints",
    "NYG": "New York Giants",
    "NYJ": "New York Jets",
    "OAK": "Oakland Raiders",
    "PHI": "Philadelphia Eagles",
    "PIT": "Pittsburgh Steelers",
    "SD": "San Diego Chargers",
    "SEA": "Seattle Seahawks",
    "SF": "San Francisco 49ers",
    "STL": "Saint Louis Rams",
    "TB": "Tampa Bay Buccaneers",
    "TEN": "Tennessee Titans",
    "WAS": "Washington Redskins",
}
nba_abr = {
    "ATL": "Atlanta Hawks",
    "BKN": "Brooklyn Nets",
    "BOS": "Boston Celtics",
    "CHA": "Charlotte Hornets",
    "CHI": "Chicago Bulls",
    "CLE": "Cleveland Cavaliers",
    "DAL": "Dallas Mavericks",
    "DEN": "Denver Nuggets",
    "DET": "Detroit Pistons",
    "GSW": "Golden State Warriors",
    "HOU": "Houston Rockets",
    "IND": "Indiana Pacers",
    "LAC": "Los Angeles Clippers",
    "LAL": "Los Angeles Lakers",
    "MEM": "Memphis Grizzlies",
    "MIA": "Miami Heat",
    "MIL": "Milwaukee Bucks",
    "MIN": "Minnesota Timberwolves",
    "NOP": "New Orleans Pelicans",
    "NYK": "New York Knicks",
    "OKC": "Oklahoma City Thunder",
    "ORL": "Orlando Magic",
    "PHI": "Philadelphia 76ers",
    "PHX": "Phoenix Suns",
    "POR": "Portland Trail Blazers",
    "SAC": "Sacramento Kings",
    "SAS": "San Antonio Spurs",
    "TOR": "Toronto Raptors",
    "UTA": "Utah Jazz",
    "WAS": "Washington Wizards"
}
mlb_abv = {
    "HOU": "Houston Astros",
    "MIL": "Milwaukee Brewers",
    "PHI": "Philadelphia Phillies",
    "SLN": "St. Louis Cardinals",
    "BOS": "Boston Red Sox",
    "COL": "Colorado Rockies",
    "LAN": "Los Angeles Dodgers",
    "NYA": "New York Yankees",
    "SFN": "San Francisco Giants",
    "TOR": "Toronto Blue Jays",
    "ATL": "Atlanta Braves",
    "CIN": "Cincinnati Reds",
    "KCA": "Kansas City Royals",
    "MIN": "Minnesota Twins",
    "PIT": "Pittsburgh Pirates",
    "TBA": "Tampa Bay Rays",
    "CHN": "Chicago Cubs",
    "DET": "Detroit Tigers",
    "MIA": "Miami Marlins",
    "OAK": "Oakland Athletics",
    "SEA": "Seattle Mariners",
    "WAS": "Washington Nationals",
    "BAL": "Baltimore Orioles",
    "CLE": "Cleveland Indians",
    "ANA": "Los Angeles Angels",
    "NYN": "New York Mets",
    "SDN": "San Diego Padres",
    "TEX": "Texas Rangers",
    "ARI": "Arizona Diamondbacks",
    "CHA": "Chicago White Sox",
    "CWS": "Chicago White Sox",
}
nhl_ab = {
    "BOS": "Boston Bruins",
    "ARI": "Arizona Coyotes",
    "BUF": "Buffalo Sabres",
    "CAR": "Carolina Hurricanes",
    "CGY": "Calgary Flames",
    "CHI": "Chicago Blackhawks",
    "COL": "Colorado Avalanche",
    "DAL": "Dallas Stars",
    "CBJ": "Columbus Blue Jackets",
    "ANA": "Anaheim Ducks",
    "DET": "Detroit Red Wings",
    "EDM": "Edmonton Oilers",
    "FLA": "Florida Panthers",
    "LAK": "Los Angeles Kings",
    "MIN": "Minnesota Wild",
    "MTL": "Montreal Canadiens",
    "NSH": "Nashville Predators",
    "NJD": "New Jersey Devils",
    "NYI": "New York Islanders",
    "NYR": "New York Rangers",
    "OTT": "Ottawa Senators",
    "PHI": "Philadelphia Flyers",
    "PIT": "Pittsburgh Penguins",
    "SJS": "San Jose Sharks",
    "STL": "St. Louis Blues",
    "TBL": "Tampa Bay Lightning",
    "TOR": "Toronto Maple Leafs",
    "VAN": "Vancouver Canucks",
    "VGK": "Vegas Golden Knights",
    "WPG": "Winnipeg Jets",
    "WSH": "Washington Capitals",
}

# 2 levels up
BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(dirname(realpath(__file__)))))
SAVE_LOCATION = '%s/resources/reference_dict' % BASEDIR


def save_dict(dictionary, file_name):
    tmp_json = json.dumps(dictionary)
    f = open(f"{SAVE_LOCATION}/{file_name}.json", "w")
    f.write(tmp_json)
    f.close()


def create_abbreviation_team_dict(is_team_upper_case: bool = False):
    if is_team_upper_case:
        nfl_dict = dict((NLPConversionUtil().normalize_text(k), v.upper()) for k, v in nfl_abreviations.items())
        nba_dict = dict((NLPConversionUtil().normalize_text(k), v.upper()) for k, v in nba_abr.items())
        mlb_dict = dict((NLPConversionUtil().normalize_text(k), v.upper()) for k, v in mlb_abv.items())
        nhl_dict = dict((NLPConversionUtil().normalize_text(k), v.upper()) for k, v in nhl_ab.items())
        final = {'NFL': nfl_dict,
                 'NBA': nba_dict,
                 'MLB': mlb_dict,
                 'NHL': nhl_dict
                 }
        save_dict(final, "abbreviation_team_dict")
    else:
        nfl_dict = dict((NLPConversionUtil().normalize_text(k), v) for k, v in nfl_abreviations.items())
        nba_dict = dict((NLPConversionUtil().normalize_text(k), v) for k, v in nba_abr.items())
        mlb_dict = dict((NLPConversionUtil().normalize_text(k), v) for k, v in mlb_abv.items())
        nhl_dict = dict((NLPConversionUtil().normalize_text(k), v) for k, v in nhl_ab.items())
        final = {'NFL': nfl_dict,
                 'NBA': nba_dict,
                 'MLB': mlb_dict,
                 'NHL': nhl_dict
                 }
        save_dict(final, "abbreviation_team_dict")
