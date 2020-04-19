import logging
from multiprocessing import Pool
import os
import logging.config
import yaml
from tag_identifier import TagIdentifier
logger = logging.getLogger(__name__)

if __name__ == '__main__':

    path = 'logging.yaml'
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.load(f.read())
            logging.config.dictConfig(config)

    generate_tags = TagIdentifier()

    # Setting number of processes to pool count
    p = Pool()
    part_1 = ["Bucs win","TB12 declining?","Burfict suspended","Pick ems Week 5"]
    part_2 = [ "Clemson escapes","Auburn vs Florida","ESPN NBA top 10","Breakout players","CA Pass bill for college players","Baseball update"]

    values = p.map(generate_tags.generate_tags, [part_1, part_2])
    print("Final Values", values)
