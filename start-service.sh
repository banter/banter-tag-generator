#!/bin/bash -xe
source /home/ec2-user/.bash_profile
cd /home/ec2-user/app/release
nohup sudo bash create-swap.sh  > ../logs/run_swap.out 2> ../logs/run_swap.err &
sudo yum install -y python3 python3-pip
venv/bin/python3 setup/stanza_setup.py
nohup venv/bin/python3 app.py > ../logs/run.out 2> ../logs/run.err &