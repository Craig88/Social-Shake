#!/bin/bash

git clone https://github.com/Craig88/Social_Shake_Source.git

sudo apt-get update
sudo apt-get install -y libfreetype6 libfreetype6-dev 
sudo apt-get install -y libpng12-0 libpng12-dev
sudo apt-get install -y graphviz graphviz-dev
sudo apt-get install -y python-pip python-dev

sudo pip install networkx
sudo pip install pyparsing==1.5.7
sudo pip install numpy
sudo pip install Matplotlib

cd Social_Shake_Source
mkdir Output
