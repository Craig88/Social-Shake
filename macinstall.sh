#!/bin/bash

git clone https://github.com/Craig88/Social_Shake_Source.git

brew update
brew install freetype 
brew install libpng
brew install graphviz

export PATH=$PATH:/usr/games/

sudo pip install networkx
sudo pip install pyparsing==1.5.7
sudo pip install numpy
sudo pip install pydot
sudo pip install Matplotlib

cd Social_Shake_Source
mkdir Output