#!/bin/bash

brew update
brew install freetype 
brew install libpng
brew install libjpeg
brew install graphviz
brew install pip

export PATH=$PATH:/usr/games/

sudo pip install networkx
sudo pip install pyparsing==1.5.7
sudo pip install numpy
sudo pip install pydot
sudo pip install Matplotlib

