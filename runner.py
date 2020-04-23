import logging
from multiprocessing import Pool
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

    # Setting number of processes to pool count
    # p = Pool()
    # part_1 = ["Bucs win","TB12 declining?","Burfict suspended","Pick ems Week 5"]

    part_2 = [ "Clemson escapes","Auburn vs Florida","ESPN NBA top 10","Breakout players","CA Pass bill for college players","Baseball update"]

    part_3 = ["Should the Cowboys pay Zeke?", "Will AB and the Raiders work?", "Will OBJ & Jarvis work?", "NFL rookie of the year",
              "Top NBA players backing out of FIBA", "Kawhi and his camp demands", "Players you think will make a big jump?",
              "Wimbledon", "Zion to Jumpman"]

    values = generate_tags.generate_tags(part_3)

    # values = p.map(generate_tags.generate_tags, [part_1, part_2])
    print("Final Values", values)
