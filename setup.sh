#!/bin/bash
sudo apt-get update

sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
xz-utils tk-dev

pyenv install 3.8.6

pyenv virtualenv 3.8.6 py38

pyenv activate py38

pip install -U pip 

pip install -r requirements.txt --use-feature=2020-resolver
sudo apt-get update
sudo apt-get -y install libstdc++6

cd pyfootdet/
. env_config.sh $PWD

cd ..
