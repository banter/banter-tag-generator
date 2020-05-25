import json

from flask import Flask, request
from flask_api import status

from src.main.tag_identifier import TagIdentifier

app = Flask(__name__)
from src.main.tagging_algos.tagging_enums.optimization_tool_mapping import OptimizationToolMapping

@app.route('/actuator')
def actuator():
    return "success", status.HTTP_200_OK

@app.route('/getTags', methods=["GET"])
def getTags():
    description = request.args.get('description')
    if description is None or len(description) == 0:
        return "please provide desscription in url", status.HTTP_400_BAD_REQUEST
    else:
        subgenre = request.args.get('subgenre')
        if subgenre == 'football':
            tags = TagIdentifier().generate_tags_on_genre(description, 'sports', OptimizationToolMapping.FOOTBALL)
        elif subgenre == 'basketball':
            tags = TagIdentifier().generate_tags_on_genre(description, 'sports', OptimizationToolMapping.BASKETBALL)
        else:
            tags = TagIdentifier().generate_tags_on_genre(description, 'sports')
    return json.dumps(tags)


@app.route('/nlp', methods=["GET"])
def getNLP():
    description = request.args.get('description')
    if description is None or len(description) == 0:
        return "please provide desscription in url", status.HTTP_400_BAD_REQUEST
    else:
        pass
    tags = TagIdentifier().base_handler.util.get_filtered_nlp_entities(description)
    return json.dumps(tags)


@app.route('/getTagsFromBody', methods=["GET", "POST"])
def getTagsFromBody():
    try:
        data = request.json
        description = data['description']
    except Exception as e:
        print(e)
        return "please provide description in json", status.HTTP_400_BAD_REQUEST
    tags = TagIdentifier().generate_tags_on_genre(description, 'sports')
    return json.dumps(tags)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
