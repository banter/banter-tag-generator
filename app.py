# import time
from flask import Flask, request
from flask_api import status
import json
from src.main.tag_identifier import TagIdentifier
app = Flask(__name__)
tag_id = TagIdentifier()

@app.route('/actuator')
def actuator():
    return "success", status.HTTP_200_OK


@app.route('/getTags', methods=["GET"])
def getTags():

    description = request.args.get('description')
    if description is None or len(description) == 0:
        return "please provide desscription in url", status.HTTP_400_BAD_REQUEST
    else:
        pass

    tags = tag_id.generate_tags_on_genre(description, 'sports')
    return json.dumps(tags)



@app.route('/getTagsFromBody', methods=["GET", "POST"])
def getTagsFromBody():
    try:
        data = request.json
        description = data['description']
    except Exception as e:
        print(e)
        return "please provide description in json", status.HTTP_400_BAD_REQUEST

    tags = tag_id.generate_tags_on_genre(description, 'sports')
    return json.dumps(tags)



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)

