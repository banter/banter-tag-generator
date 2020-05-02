"# banter_tag_gen"

Package Intallation 

`pip install -r requirements.txt`

If error on torch installation: https://stackoverflow.com/questions/56239310/could-not-find-a-version-that-satisfies-the-requirement-torch-1-0-0

`pip install torch===1.4.0 torchvision===0.5.0 -f https://download.pytorch.org/whl/torch_stable.html`


Running 

`python runner.py`


Resources 

# Python Issue on Windows https://stackoverflow.com/questions/56239310/could-not-find-a-version-that-satisfies-the-requirement-torch-1-0-0
# Information on what these the upos mean in each token: https://polyglot.readthedocs.io/en/latest/POS.html
# Objects information
# https://stanfordnlp.github.io/stanza/data_objects#document
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


"""