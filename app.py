import json

from flask import Flask, request
from flask_api import status

from src.main.tag_identifier import TagIdentifier
import logging

import os
from os.path import dirname, realpath
from src.main.tagging_algos.tagging_enums.optimization_tool_mapping import OptimizationToolMapping

app = Flask(__name__)
CURRENT_DIR = os.path.dirname(os.path.dirname(dirname(realpath(__file__))))
logging.basicConfig(
    filename="log.log",
    level=logging.DEBUG)
print(CURRENT_DIR)

@app.route('/actuator')
def actuator():
    return "success", status.HTTP_200_OK


@app.route('/getTags', methods=["GET"])
def getTags():

    description = request.args.get('description')
    if description is None or len(description) == 0:
        logging.warning(f"getTags processing {description}")
        return "please provide desscription in url", status.HTTP_400_BAD_REQUEST
    else:
        try:
            app.logger.info(f"getTags processing {description}")
            subgenre = request.args.get('subgenre')
            if subgenre == 'FOOTBALL':
                tags = TagIdentifier().generate_tags_on_genre(description, 'sports', OptimizationToolMapping.FOOTBALL)
            elif subgenre == 'BASKETBALL':
                tags = TagIdentifier().generate_tags_on_genre(description, 'sports', OptimizationToolMapping.BASKETBALL)
            else:
                tags = TagIdentifier().generate_tags_on_genre(description, 'sports')
        except Exception as e:
            logging.critical(f"getTags error for description:{description}, error:{e}")
            return str(e), status.HTTP_500_INTERNAL_SERVER_ERROR
    logging.info(f"getTags successful description: {description}, tags: {tags}")
    return json.dumps(tags)


@app.route('/nlp', methods=["GET"])
def getNLP():
    description = request.args.get('description')
    if description is None or len(description) == 0:
        return "please provide desscription in url", status.HTTP_400_BAD_REQUEST
    else:
        pass
    tags = TagIdentifier().base_handler.util.get_normalized_and_filtered_nlp_entities(description)
    return json.dumps(tags)


@app.route('/getTagsFromBody', methods=["GET", "POST"])
def getTagsFromBody():
    try:
        data = request.json
        description = data['description']
    except Exception as e:
        print(e)
        app.logger.warning(f"getTags processing {request.data}")
        return "please provide description in json", status.HTTP_400_BAD_REQUEST
    try:
        tags = TagIdentifier().generate_tags_on_genre(description, 'sports')
    except Exception as e:
        app.logger.critical(f"getTags error for description:{description}, error:{e}")
        return str(e), status.HTTP_500_INTERNAL_SERVER_ERROR
    app.logger.info(f"getTags successful description: {description}, tags: {tags}")
    return json.dumps(tags)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=False)
