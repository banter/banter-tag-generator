from utils import HelperClass

helper = HelperClass()


# TODO Pending Addition Unique last Names?
def add_unique_last_names_to_dict():
    sports_dir = helper.set_player_dict()
    player_dir = sports_dir['nfl']
    tmp_dir = {}
    for player in player_dir.keys():
        print(player)
        first_last_name = player.split()
        print(first_last_name)
        try:
            if len(first_last_name) == 3:
                tmp_dir[first_last_name[2]] = player_dir[player]
            else:
                tmp_dir[first_last_name[1]] = player_dir[player]
        except IndexError as err:
            print(err)
            pass

    return tmp_dir


x = add_unique_last_names_to_dict()
