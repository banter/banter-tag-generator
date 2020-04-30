import logging
from multiprocessing import Pool
import mysql.connector
import os
import logging.config
import yaml
from tag_identifier import TagIdentifier
import configparser
logger = logging.getLogger(__name__)

if __name__ == '__main__':

    path = 'logging.yaml'
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.load(f.read())
            logging.config.dictConfig(config)

    generate_tags = TagIdentifier(store_ml_data = True)


    part_1 = ["Bucs win","TB12 declining?","Burfict suspended","Pick ems Week 5"]

    part_2 = [ "Clemson escapes","Auburn vs Florida","ESPN NBA top 10","Breakout players","CA Pass bill for college players","Baseball update"]

    part_3 = ["Should the Cowboys pay Zeke?", "Will AB and the Raiders work?", "Will OBJ & Jarvis work?", "NFL rookie of the year",
              "Top NBA players backing out of FIBA", "Kawhi and his camp demands", "Players you think will make a big jump?",
              "Wimbledon", "Zion to Jumpman"]

    pmt = ["MNF recap, the Bears are back and the Skins have PFT very angry"]

    import mysql.connector

    cnx = mysql.connector.connect(user='user', password='password',
                                  host='127.0.0.1',
                                  database='db', auth_plugin='mysql_native_password')
    cursor = cnx.cursor()
    query = ("select description from discussion where match(description) against('sport' in natural language mode) order by match(description) against('belly but' in natural language mode) desc limit 50 offset 0")

    cursor.execute(query)

    description_list = []



    fetch_size = 10
    all_results = []
    while True:
        result = cursor.fetchmany(fetch_size)
        if not result:
            break
        else:
            # Converting list of tuples to list of strings
            partial_result: list = [".".join(map(str, r)) for r in result]
            all_results.append(partial_result)
    # values = generate_tags.generate_tags(results)

    # Setting number of processes to pool count
    p = Pool()
    values = p.map(generate_tags.generate_tags, all_results)
    print("Final Values", values)
