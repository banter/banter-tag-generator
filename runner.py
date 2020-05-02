import logging
from multiprocessing import Pool
import mysql.connector
import os
import logging.config
import yaml
from tag_identifier import TagIdentifier
import configparser
logger = logging.getLogger(__name__)

def get_db_results_cursor(query: str):

    cnx = mysql.connector.connect(user='user', password='password',
                                  host='127.0.0.1',
                                  database='db', auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    result_list: list = [".".join(map(str, r)) for r in result]
    return result_list



if __name__ == '__main__':

    path = 'logging.yaml'
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.load(f.read())
            logging.config.dictConfig(config)

    generate_tags = TagIdentifier(store_ml_data = True)

    #
    # part_1 = ["Bucs win","TB12 declining?","Burfict suspended","Pick ems Week 5"]
    #
    # part_2 = [ "Clemson escapes","Auburn vs Florida","ESPN NBA top 10","Breakout players","CA Pass bill for college players","Baseball update"]
    #
    # part_3 = ["Should the Cowboys pay Zeke?", "Will AB and the Raiders work?", "Will OBJ & Jarvis work?", "NFL rookie of the year",
    #           "Top NBA players backing out of FIBA", "Kawhi and his camp demands", "Players you think will make a big jump?",
    #           "Wimbledon", "Zion to Jumpman"]
    #
    # pmt = ["MNF recap, the Bears are back and the Skins have PFT very angry"]
    #
    #
    #
    # cnx = mysql.connector.connect(user='user', password='password',
    #                               host='127.0.0.1',
    #                               database='db', auth_plugin='mysql_native_password')
    # cursor = cnx.cursor()
    # query = ("select description from discussion where match(description) against('sport' in natural language mode) order by match(description) against('belly but' in natural language mode) desc limit 50 offset 0")
    #
    # cursor.execute(query)
    #
    # description_list = []



    # fetch_size = 10
    # all_results = []
    # count = 0
    # while count < 4:
    #     result = cursor.fetchmany(10)
    #     partial_result: list = [".".join(map(str, r)) for r in result]
    #     all_results.append(partial_result)
    #     count +=1


    # while True:
    #     result = cursor.fetchmany(fetch_size)
    #     if not result:
    #         break
    #     else:
    #         # Converting list of tuples to list of strings
    #         partial_result: list = [".".join(map(str, r)) for r in result]
    #         all_results.append(partial_result)

    # result = cursor.fetchmany(10)
    # partial_result: list = [".".join(map(str, r)) for r in result]
    # values = generate_tags.generate_tags(partial_result)

    # Setting number of processes to pool count
    # p = Pool()
    # values = p.map(generate_tags.generate_tags, [part_2,part_1])

    query = ("select description from discussion where match(description) against('football' in natural language mode) limit 15 offset 0")

    db_results = get_db_results_cursor(query)
    results = []
    for description in db_results:
        values = generate_tags.generate_tags_on_genre(description, "sports")
        print(values)
        results.append({"description": description, "tags": values})

    print("Final Values", results)
