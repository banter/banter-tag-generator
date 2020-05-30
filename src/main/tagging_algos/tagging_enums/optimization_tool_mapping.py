from enum import Enum

from src.main.utils.config_util import SportsConfig


class OptimizationToolMapping(Enum):
    BASEBALL = {"sport": "BASEBALL",
                "leagues": ["MLB"]}
    BASKETBALL = {"sport": "BASKETBALL",
                  "leagues": ["NBA"]}
    FOOTBALL = {"sport": "FOOTBALL",
                "leagues": ["NFL"]}
    HOCKEY = {"sport": "HOCKEY",
              "leagues": ["NHL"]}
    NONE = {"sport": "",
            "leagues": SportsConfig.sports_leagues}
