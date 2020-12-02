#!/bin/bash
pip install -U pip 

pip install -r requirements.txt
sudo apt-get update
sudo apt-get -y install libstdc++6

# cd $PWD/pyfootdet
cd ./pyfootdet && . /env_config.sh $PWD
