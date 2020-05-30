from src.main.utils.banter_dictionary_creator.create_abbreviation_team_dict import create_abbreviation_team_dict
from src.main.utils.banter_dictionary_creator.create_city_team_dict import create_city_team_dict
from src.main.utils.banter_dictionary_creator.create_golf_player_dict import create_golf_player_dict
from src.main.utils.banter_dictionary_creator.create_headcoach_dict import create_headcoach_dict
from src.main.utils.banter_dictionary_creator.create_nickname_dict import create_nickname_dict
from src.main.utils.banter_dictionary_creator.create_player_dict import create_player_dict
from src.main.utils.banter_dictionary_creator.create_sports_terms import create_sports_terms
from src.main.utils.banter_dictionary_creator.create_team_dict import create_team_dict

if __name__ == '__main__':
    create_abbreviation_team_dict(is_team_upper_case=True)
    create_city_team_dict(edit_existing=True, is_team_upper_case=True)
    create_headcoach_dict(is_team_upper_case=True)
    create_golf_player_dict()
    create_nickname_dict()
    create_player_dict(modify_existing=True, is_team_upper_case=True)
    create_team_dict(is_team_upper_case=True)
    # TODO conver to upper case/removing punctuation limits the effectivness
    create_sports_terms()
