#!/bin/bash

curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash 

export PATH="~/.pyenv/bin:$PATH" >> ~/.bashrc
eval "$(pyenv init -)" >> ~/.bashrc
eval "$(pyenv virtualenv-init -)" >> ~/.bashrc

exec "$SHELL"
