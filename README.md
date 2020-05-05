"# banter_tag_gen"

#Run th App
- `docker-compose up`

Note:
- This initial startup will take some time, if MemoryError, increase memory allocation for each container on the docker vm.
- Downloading: Python Packages, English model for neural pipeline and Setting default neural pipeline in english
- `docker-machine create -d virtualbox --virtualbox-cpu-count=2 --virtualbox-memory=4096 --virtualbox-disk-size=50000 default`    


Endpoints:

- /actuator: See if up 

- /getTags
    - GET 
    - parameter:description
    - Response:  [List of tags]
    - Sample Request: `curl --location --request GET 'http://localhost:5000/getTags?description=Austin%20Marchese%20is%20the%20man'`
    - Sample Response: `[{"type": "person", "value": "Austin Marchese"}]`
    
(Same as above different request format)
- /getTagsFromBody
    - (GET or POST) 
    - Request Body: {"description": Description string}
    - Response:  [List of tags]
    - Sample Curl Request:`curl --location --request GET 'http://localhost:5000/getTagsFromBody' \
--header 'Content-Type: application/json' \
--data-raw '{"description": "Is Jared Goff on the decline?"} '` 
    - Sample Response:`[{"type": "person", "value": "Jared Goff"}, {"type": "team", "value": "Los Angeles Rams"}, {"type": "league", "value":
"nfl"}]`




#Python Package Local Installation:


Local Installation 
`pip install -r requirements.txt`

If error on torch installation: https://stackoverflow.com/questions/56239310/could-not-find-a-version-that-satisfies-the-requirement-torch-1-0-0

`pip install torch===1.4.0 torchvision===0.5.0 -f https://download.pytorch.org/whl/torch_stable.html`

#Resources 

 Python Issue on Windows https://stackoverflow.com/questions/56239310/could-not-find-a-version-that-satisfies-the-requirement-torch-1-0-0
 Information on what these the upos mean in each token: https://polyglot.readthedocs.io/en/latest/POS.html
 Objects information
 https://stanfordnlp.github.io/stanza/data_objects#document
"""
Resources:
Stanza Overview: https://pypi.org/project/stanza/
    -Python Specifics: https://stanfordnlp.github.io/stanza/
    -https://stanfordnlp.github.io/stanza/installation_usage.html
Data Objects and Annotations: https://stanfordnlp.github.io/stanza/data_objects#sentence
Downloading on Windows 10: https://stackoverflow.com/questions/56239310/could-not-find-a-version-that-satisfies-the-requirement-torch-1-0-0

Linguistics Information:

Lemma:
https://simple.wikipedia.org/wiki/Lemma_(linguistics)
Parts of Speech Tagging: (ADJ = Adjective, ADP = adposition etc.) : https://polyglot.readthedocs.io/en/latest/POS.html

Entity Recognition:
Source: https://www.nltk.org/book/ch07.html
NE Type	Examples
ORGANIZATION	Georgia-Pacific Corp., WHO
PERSON	Eddy Bonte, President Obama
LOCATION	Murray River, Mount Everest
DATE	June, 2008-06-29
TIME	two fifty a m, 1:30 p.m.
MONEY	175 million Canadian Dollars, GBP 10.40
PERCENT	twenty pct, 18.75 %
FACILITY	Washington Monument, Stonehenge
GPE	South East Asia, Midlothian

Python Docker:

https://runnable.com/docker/python/docker-compose-with-flask-apps
https://djangostars.com/blog/what-is-docker-and-how-to-use-it-with-python/

Interesting POinters on compose:
https://medium.com/bitcraft/docker-composing-a-python-3-flask-app-line-by-line-93b721105777

Future Boilerplate?
https://github.com/gabimelo/flask-boilerplate

Windows Docker Port Forwarding: 
For me NATing the port in VirtualBox worked
Go to VirtualBox -> Your BOX -> Settings -> Network ->
Choose NAT
Open Advanced
Click Port Forwarding
Add new rule to map whatever port you need from host to guest
Click OK, OK
Then stop, start the BOX

"""