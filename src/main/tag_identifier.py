from typing import *
from src.main.tagging_algos.tagging_base_handler import TaggingBaseHandler
from src.main.tagging_algos.tagging_enums.optimization_tool_mapping import OptimizationToolMapping
from src.main.tagging_algos.tagging_sports_handler import TaggingSportsHandler
from src.main.utils.decorators import debug, timeit

class TagIdentifier:

    @timeit
    def __init__(self, store_ml_data: bool = True):
        self.store_ml_data = store_ml_data
        self.sport_handler = TaggingSportsHandler()
        self.base_handler = TaggingBaseHandler()

    @debug
    def generate_tags_on_genre(self, description: str, genre: str,
                               subgenre: OptimizationToolMapping = OptimizationToolMapping.NONE) -> List[Dict]:
        if genre == "sports":
            return self.sport_handler.get_sports_tags(description, subgenre)
        else:
            return self.base_handler.get_basic_tags(description)
