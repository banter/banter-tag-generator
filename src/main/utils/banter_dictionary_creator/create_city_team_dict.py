import json
import os
from os.path import dirname, realpath

from src.main.utils.nlp_conversion_util import NLPConversionUtil
from src.main.utils.nlp_resource_util import NLPResourceUtil

BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(dirname(realpath(__file__)))))
SAVE_LOCATION = '%s/resources/reference_dict' % BASEDIR

nlp_resource_util = NLPResourceUtil()
existing_team_dict = {
    "NFL": {
        "Baltimore": "Baltimore Ravens",
        "San Francisco": "San Francisco 49ers",
        "Tampa Bay": "Tampa Bay Buccaneers",
        "New Orleans": "New Orleans Saints",
        "Kansas City": "Kansas City Chiefs",
        "Dallas": "Dallas Cowboys",
        "New England": "New England Patriots",
        "Minnesota": "Minnesota Vikings",
        "Seattle": "Seattle Seahawks",
        "Tennessee": "Tennessee Titans",
        "Philadelphia": "Philadelphia Eagles",
        "Atlanta": "Atlanta Falcons",
        "Houston": "Houston Texans",
        "Green Bay": "Green Bay Packers",
        "Arizona": "Arizona Cardinals",
        "Indianapolis": "Indianapolis Colts",
        "Detroit": "Detroit Lions",
        "Carolina": "Carolina Panthers",
        "Cleveland": "Cleveland Browns",
        "Buffalo": "Buffalo Bills",
        "Oakland": "Oakland Raiders",
        "Miami": "Miami Dolphins",
        "Jacksonville": "Jacksonville Jaguars",
        "Pittsburgh": "Pittsburgh Steelers",
        "Denver": "Denver Broncos",
        "Chicago": "Chicago Bears",
        "Cincinnati": "Cincinnati Bengals",
        "Washington": "Washington Redskins"
    },
    "NHL": {
        "Tampa Bay": "Tampa Bay Lightning",
        "Boston": "Boston Bruins",
        "Calgary": "Calgary Flames",
        "Washington": "Washington Capitals",
        "San Jose": "San Jose Sharks",
        "Toronto": "Toronto Maple Leafs",
        "Nashville": "Nashville Predators",
        "Pittsburgh": "Pittsburgh Penguins",
        "St. Louis": "St. Louis Blues",
        "Winnipeg": "Winnipeg Jets",
        "Carolina": "Carolina Hurricanes",
        "Columbus": "Columbus Blue Jackets",
        "Montreal": "Montreal Canadiens",
        "Dallas": "Dallas Stars",
        "Colorado": "Colorado Avalanche",
        "Florida": "Florida Panthers",
        "Arizona": "Arizona Coyotes",
        "Chicago": "Chicago Blackhawks",
        "Minnesota": "Minnesota Wild",
        "Philadelphia": "Philadelphia Flyers",
        "Vancouver": "Vancouver Canucks",
        "Anaheim": "Anaheim Ducks",
        "Edmonton": "Edmonton Oilers",
        "Buffalo": "Buffalo Sabres",
        "Detroit": "Detroit Red Wings",
        "New Jersey": "New Jersey Devils",
        "Ottawa": "Ottawa Senators",
        "Vegas": "Vegas Golden Knights"
    },
    "NBA": {
        "Milwaukee": "Milwaukee Bucks",
        "Golden State": "Golden State Warriors",
        "New Orleans": "New Orleans Pelicans",
        "Philadelphia": "Philadelphia 76ers",
        "Portland Trail": "Portland Trail Blazers",
        "Oklahoma City": "Oklahoma City Thunder",
        "Toronto": "Toronto Raptors",
        "Sacramento": "Sacramento Kings",
        "Washington": "Washington Wizards",
        "Houston": "Houston Rockets",
        "Atlanta": "Atlanta Hawks",
        "Minnesota": "Minnesota Timberwolves",
        "Boston": "Boston Celtics",
        "Brooklyn": "Brooklyn Nets",
        "Utah": "Utah Jazz",
        "San Antonio": "San Antonio Spurs",
        "Charlotte": "Charlotte Hornets",
        "Denver": "Denver Nuggets",
        "Dallas": "Dallas Mavericks",
        "Indiana": "Indiana Pacers",
        "Phoenix": "Phoenix Suns",
        "Orlando": "Orlando Magic",
        "Detroit": "Detroit Pistons",
        "Miami": "Miami Heat",
        "Chicago": "Chicago Bulls",
        "Cleveland": "Cleveland Cavaliers",
        "Memphis": "Memphis Grizzlies",
        "New York": "New York Knicks"
    },
    "MLB": {
        "Houston": "Houston Astros",
        "Minnesota": "Minnesota Twins",
        "Atlanta": "Atlanta Braves",
        "Oakland": "Oakland Athletics",
        "Tampa Bay": "Tampa Bay Rays",
        "Washington": "Washington Nationals",
        "Cleveland": "Cleveland Indians",
        "St. Louis": "St. Louis Cardinals",
        "Milwaukee": "Milwaukee Brewers",
        "Arizona": "Arizona Diamondbacks",
        "Boston": "Boston Red Sox",
        "Philadelphia": "Philadelphia Phillies",
        "Texas": "Texas Rangers",
        "San Francisco": "San Francisco Giants",
        "Cincinnati": "Cincinnati Reds"
    }
}


def create_new_city_team_dict():
    for sport in ['NFL', 'NHL', 'NBA', 'MLB']:
        ar = {}
        final = {}
        for index, k in enumerate(nlp_resource_util.sports_team_dict[sport].keys()):
            if index % 2 != 0:
                continue
            print(k)
            team = k
            spl = k.split()
            if len(spl) == 3:
                city = ' '.join(spl[0:2])
            if len(spl) == 2:
                city = spl[0]
            # Skipping Chicago because theres 2 teams in baseball
            if sport == 'MLB' and city == "Chicago" or city == "Chicago White":
                continue
            # Skipping Vegas because......Vegas probably not talking about vegas
            # if sport == 'nhl' and city == "Vegas Golden":
            #     continue
            if city == "Los Angeles" or city == "New York":
                continue
            if city in ["Toronto Maple", "Columbus Blue", "Detroit Red", "Boston Red",
                        "Chigago White", "Toronto Blue"]:
                city = spl[0]
                # team = ' '.join(spl[1:3])
                # print(city, team)
                ar[city] = team
                print(ar)
            else:
                ar[city] = team

        print(ar)
        final[sport] = ar
        # manually adding the knicks
        final['NBA']['New York'] = 'New York Knicks'
        return final


def save_dict(dictionary, file_name):
    tmp_json = json.dumps(dictionary)
    with open(f"{SAVE_LOCATION}/{file_name}.json", "w") as json_file:
        json_file.write(tmp_json)
        json_file.close()


def create_city_team_dict(edit_existing: bool, is_team_upper_case: bool = False):
    if edit_existing:
        if is_team_upper_case:
            final = existing_team_dict
            nfl_abreviations_upper = dict(
                (NLPConversionUtil().normalize_text(k), v.upper()) for k, v in final['NFL'].items())
            nba_abr_upper = dict((NLPConversionUtil().normalize_text(k), v.upper()) for k, v in final['NBA'].items())
            mlb_abv_upper = dict((NLPConversionUtil().normalize_text(k), v.upper()) for k, v in final['MLB'].items())
            nhl_ab_upper = dict((NLPConversionUtil().normalize_text(k), v.upper()) for k, v in final['NHL'].items())
            final = {'NFL': nfl_abreviations_upper,
                     'NBA': nba_abr_upper,
                     'MLB': mlb_abv_upper,
                     'NHL': nhl_ab_upper
                     }
            save_dict(final, "city_team_dict")

        else:
            final = existing_team_dict
            nfl_abreviations_upper = dict((NLPConversionUtil().normalize_text(k), v) for k, v in final['NFL'].items())
            nba_abr_upper = dict((NLPConversionUtil().normalize_text(k), v) for k, v in final['NBA'].items())
            mlb_abv_upper = dict((NLPConversionUtil().normalize_text(k), v) for k, v in final['MLB'].items())
            nhl_ab_upper = dict((NLPConversionUtil().normalize_text(k), v) for k, v in final['NHL'].items())
            final = {'NFL': nfl_abreviations_upper,
                     'NBA': nba_abr_upper,
                     'MLB': mlb_abv_upper,
                     'NHL': nhl_ab_upper
                     }
            save_dict(final, "city_team_dict")


    else:
        final = create_new_city_team_dict()
        save_dict(final, "city_team_dict")
