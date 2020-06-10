#!/bin/bash
sudo yum -y update
sudo yum install -y python3 python3-pip

wget https://github.com/banter/banter-tag-generator/archive/master.zip
[ -d "banter-tag-generator-master" ] && rm -rf banter-tag-generator-master
unzip master.zip
rm -rf master.zip

cd banter-tag-generator-master
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt --default-timeout=10000 --no-cache-dir -v
pip install stanza==1.0.1 --no-cache-dir -v
pip install nltk==3.5 --no-cache-dir -v
pip install waitress==1.4.3
waitress-serve --listen 0.0.0.0:5000 wsgi:app
