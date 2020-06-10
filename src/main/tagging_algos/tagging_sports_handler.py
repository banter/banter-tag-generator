from typing import *

from src.main.models.tag_model import TagModel, NLPEntityModel
from src.main.tagging_algos.tagging_enums.optimization_tool_mapping import OptimizationToolMapping
from src.main.tagging_algos.tagging_utils.tagging_sports_util import TaggingSportsUtil
from src.main.utils.decorators import debug


class TaggingSportsHandler(TaggingSportsUtil):

    def get_sports_tags(self, description: str,
                        optimization_tool: OptimizationToolMapping = OptimizationToolMapping.NONE) -> List[TagModel]:
        self.optimization_tool = optimization_tool
        sports_tags = self.generate_sports_tags(description)
        return self.util.alter_tags_to_proper_response_format(sports_tags, "value")

    @debug
    def generate_sports_tags(self, description: str) -> List[TagModel]:
        description_tags: List[TagModel] = []
        location_entities: List[NLPEntityModel] = []
        nlp_entities = self.util.get_normalized_and_filtered_nlp_entities(description)
        description_tags += self.get_sport_and_league_tags_on_description(description)

        for nlp_entity in nlp_entities:
            # TODO why cant this just look through description tags
            if nlp_entity['text'].lower() in self.util.sports_leagues:
                # Handling sports leagues in other method skipping this
                continue
            entity_tags = self.generate_basic_sport_tags(nlp_entity)
            if len(entity_tags) == 0:
                entity_tags += self.handle_untagged_nlp_entity(nlp_entity)

            if len(entity_tags) == 0:
                # Checking if it is an untagged location, if it is will use later
                if self.util.is_nlp_entity_specific_type(nlp_entity, "GPE"):
                    location_entities.append(nlp_entity)
            description_tags += entity_tags
        # If there are untagged location tags, going to check if there is any
        # Reference to a sports league. This way we can use this as context for the discussion
        if len(location_entities) != 0:
            description_tags += self.generate_location_tags(location_entities)
        return description_tags

    @debug
    def generate_basic_sport_tags(self, nlp_entity: NLPEntityModel) -> List[TagModel]:
        nlp_entity_tags: list = []
        nlp_entity_tags += self.get_team_and_league_tags_on_team(nlp_entity)
        if len(nlp_entity_tags) == 0:
            nlp_entity_tags += self.get_team_player_league_tags_on_player(nlp_entity, self.util.sports_player_dict)
        if len(nlp_entity_tags) == 0:
            nlp_entity_tags += self.get_team_player_league_tags_on_coach(nlp_entity, self.util.sports_coach_dict)
        if len(nlp_entity_tags) == 0:
            nlp_entity_tags += self.get_sport_and_person_tags_on_non_team_sport(nlp_entity,
                                                                                self.util.individual_sports_dict)
        if len(nlp_entity_tags) == 0:
            nlp_entity_tags += self.get_team_player_league_tags_on_nickname(nlp_entity, self.util.sports_nickname_dict)
        # TODO Dont think sports terms is worth it, removing for now
        # if len(nlp_entity_tags) == 0:
        #     nlp_entity_tags += self.get_sport_tag_on_sports_terms(nlp_entity)

        return nlp_entity_tags

    @debug
    def generate_matchup_tags(self, nlp_entity: Dict) -> List[Dict]:
        """
        Breaking up the matchup i.e MIN@DAL into a list w each team
        then altering the existing keyword dict to get matchup tags
        with the "text" = "DAL"
        :param nlp_entity:key word dict
        :return: Return matchup_tags identifies
        """
        matchup_tags = []
        try:
            if '-' in nlp_entity["text"]:
                matchup: List[str, str] = nlp_entity["text"].split("-")
            elif '@' in nlp_entity["text"]:
                matchup: List[str, str] = nlp_entity["text"].split("@")
            else:
                matchup: List[str, str] = nlp_entity["text"].split("&")
            # Removing whitespace If there were trailing or leading 'Lakers '-----'Lakers'
            nlp_entity["text"] = matchup[0].strip()
            matchup_tags += self.get_team_and_league_tags_on_team(nlp_entity)
            nlp_entity["text"] = matchup[1].strip()
            matchup_tags += self.get_team_and_league_tags_on_team(nlp_entity)
            return matchup_tags
        except:
            return []

    def generate_location_tags(self, location_entities: List[NLPEntityModel]) -> \
            List[TagModel]:
        location_tags: List[TagModel] = []
        # checking Type Value Which is used for specif
        if self.optimization_tool.name != 'NONE':
            location_tags += self.get_team_and_league_tags_from_city(location_entities,
                                                                     self.optimization_tool.value["leagues"][0])
        return location_tags

    @debug
    def handle_untagged_nlp_entity(self, nlp_entity: NLPEntityModel) -> List[TagModel]:
        word_tags = []
        if self.is_nlp_entity_a_game_matchup(nlp_entity):
            word_tags += self.generate_matchup_tags(nlp_entity)
        if self.util.is_nlp_entity_specific_type(nlp_entity, "PERSON"):
            word_tags += self.get_person_tags(nlp_entity)
        if self.util.is_nlp_entity_specific_type(nlp_entity, "ORG"):
            adjusted_nlp_entity = self.util.remove_prefix_from_word(nlp_entity)
            if self.util.is_adjusted_entity_different(nlp_entity, adjusted_nlp_entity):
                word_tags += self.generate_basic_sport_tags(adjusted_nlp_entity)

        return word_tags

    @debug
    def is_nlp_entity_a_game_matchup(self, nlp_entity: NLPEntityModel) -> bool:
        for indicator in self.util.matchup_indicators:
            if indicator in nlp_entity["text"]:
                return True
        return False
