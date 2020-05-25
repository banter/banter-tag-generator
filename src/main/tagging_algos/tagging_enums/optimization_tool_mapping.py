from enum import Enum

from src.main.utils.config_util import SportsConfig


class OptimizationToolMapping(Enum):
    BASEBALL = {"sport": "baseball",
                "leagues": ["MLB"]}
    BASKETBALL = {"sport": "basketball",
                  "leagues": ["NBA"]}
    FOOTBALL = {"sport": "football",
                "leagues": ["NFL"]}
    HOCKEY = {"sport": "hockey",
              "leagues": ["NHL"]}
    NONE = {"sport": "",
            "leagues": SportsConfig.sports_leagues}
