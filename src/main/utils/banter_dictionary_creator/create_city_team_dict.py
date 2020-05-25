from src.main.utils.nlp_resource_util import NLPResourceUtil

x = NLPResourceUtil()

city_team_dict = {}
final = {}
for sport in ['NFL', 'NHL', 'NBA', 'MLB']:
    ar = {}
    for index, k in enumerate(x.sports_team_dict[sport].keys()):
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
        if sport == 'mlb' and city == "Chicago" or city == "Chicago White":
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
final['nba']['New York'] = 'New York Knicks'

import json


def save_dict(dictionary, file_name):
    tmp_json = json.dumps(dictionary)
    with open(f"../../resources/reference_dict/{file_name}.json", "w") as json_file:
        json_file.write(tmp_json)
        json_file.close()


save_dict(final, "city_team_dict")
