from src.main.utils.banter_dictionary_creator.sports_reference_roster_scraper import SportsReferenceRosterScraper

if __name__ == '__main__':
    leagues = ["MLB", "NFL", "NBA", "NHL"]
    duplicates = []
    for league in leagues:
        players = SportsReferenceRosterScraper(league, get_rosters=True)
        players.save_league_roster_dict(f"{league}_player_dict_final")
        print(players.duplicate_names)
        duplicates.append(players.duplicate_names)
