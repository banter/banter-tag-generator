from src.main.utils.nlp_resource_util import NLPResourceUtil


x = NLPResourceUtil()

city_team_dict = {}
final = {}
for sport in ['nfl', 'nhl', 'nba', 'mlb']:
    ar = {}
    for k in x.sports_team_dict[sport].keys():
        spl = k.split()
        if len(spl) == 3:
            city = ' '.join(spl[0:2])
            if city == "Los Angeles" or city == "New York":
                continue
            ar[city] = k
        if len(spl) == 2:
            city = spl[0]
            ar[city] = k
    final[sport] = ar

# manually adding the knicks
final['nba']['New York'] = 'New York Knicks'


import json


def save_dict(dictionary, file_name):
    tmp_json = json.dumps(dictionary)
    with open(f"../../resources/reference_dict/{file_name}.json", "w") as json_file:
        json_file.write(tmp_json)
        json_file.close()

save_dict(final, "city_team_dict")
