# import time
from flask import Flask, request
from flask_api import status
import json
from src.main.tag_identifier import TagIdentifier
app = Flask(__name__)
tag_id = TagIdentifier()

@app.route('/actuator')
def actuator():
    print("AU")
    return "success", status.HTTP_200_OK


@app.route('/getTags', methods=["GET", "POST"])
def getTags():
    try:
        data = request.json
        description = data['description']
    except Exception as e:
        print(e)
        return "please provide description in json", status.HTTP_400_BAD_REQUEST

    tags = tag_id.generate_tags_on_genre(description, 'sports')
    return json.dumps(tags)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)

