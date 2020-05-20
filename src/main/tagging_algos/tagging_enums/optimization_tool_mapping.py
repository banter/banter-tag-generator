from enum import Enum

from src.main.utils.config_util import SportsConfig


class OptimizationToolMapping(Enum):
    BASEBALL = {"sport": "baseball",
                "leagues": ["mlb"]}
    BASKETBALL = {"sport": "basketball",
                  "leagues": ["nba"]}
    FOOTBALL = {"sport": "american football",
                "leagues": ["nfl"]}
    HOCKEY = {"sport": "hockey",
              "leagues": ["nhl"]},
    NONE = {"sport": "",
            "leagues": SportsConfig.sports_leagues}
