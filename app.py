import json
from flask import Flask, request
from flask_api import status
from src.main.tag_identifier import TagIdentifier
from src.main.tagging_algos.tagging_enums.optimization_tool_mapping import OptimizationToolMapping
from src.main.utils.logger_initializer import *
app = Flask(__name__)
PARENT_DIR = os.getcwd()
initialize_logger(PARENT_DIR)
hostname = os.popen('hostname').read()
# If on docker or local log to logs directory, if on AWS ec2 log to logs folder outside project
if 'ec2' in hostname:
    initialize_logger('../')
else:
    initialize_logger(PARENT_DIR)

@app.route('/actuator')
def actuator():
    logging.info("actuator")
    return "success!", status.HTTP_200_OK

@app.route('/')
def healthcheck():
    return "healthcheck", status.HTTP_200_OK

@app.route('/getTags', methods=["GET"])
def getTags():
    description = request.args.get('description')
    if description is None or len(description) == 0:
        logging.error(f"getTags processing {description}")
        return "please provide desscription in url", status.HTTP_400_BAD_REQUEST
    else:
        try:
            logging.info(f"getTags processing {description}")
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


@app.route('/rawnlp', methods=["GET"])
def rawNLP():
    description = request.args.get('description')
    if description is None or len(description) == 0:
        return "please provide desscription in url", status.HTTP_400_BAD_REQUEST
    else:
        pass
    nlp_response = TagIdentifier().base_handler.util.get_nlp_response(description)
    nlp_entities = TagIdentifier().base_handler.util.get_nlp_entities_from_nlp_response(nlp_response)
    response = [{"NLP Response": str(nlp_response), "NLP Entities": nlp_entities}]
    return json.dumps(response)

@app.route('/getTagsFromBody', methods=["GET", "POST"])
def getTagsFromBody():
    try:
        data = request.json
        description = data['description']
    except Exception as e:
        print(e)
        logging.error(f"getTags processing {request.data}")
        return "please provide description in json", status.HTTP_400_BAD_REQUEST
    try:
        tags = TagIdentifier().generate_tags_on_genre(description, 'sports')
    except Exception as e:
        logging.critical(f"getTags error for description:{description}, error:{e}")
        return str(e), status.HTTP_500_INTERNAL_SERVER_ERROR
    logging.info(f"getTags successful description: {description}, tags: {tags}")
    return json.dumps(tags)


if __name__ == "__main__":
    hostname = os.popen('hostname').read()
    if 'Austin' not in hostname:
        app.run(host="0.0.0.0", port=5000, debug=False)
    else:
        app.run(host="0.0.0.0", port=5005, debug=False)

