#!/bin/bash

curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash 

echo export PATH="~/.pyenv/bin:$PATH" >> ~/.bashrc
echo eval "$(pyenv init -)" >> ~/.bashrc
echo eval "$(pyenv virtualenv-init -)" >> ~/.bashrc

exec "$SHELL"


sudo apt-get update

sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
xz-utils tk-dev

sudo apt install libffi-dev 

pyenv install 3.8.6

pyenv virtualenv 3.8.6 py38

pyenv activate py38
