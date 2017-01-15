#!/usr/bin/env bash

# Assumes you have admin access
if [[ "OSTYPE" == "linux-gnu" ]]; then
    wget http://minisat.se/downloads/minisat-2.2.0.tar.gz
    tar zxvf minisat*
    cd minisat
    export MROOT=$(pwd)
    cd core
    # sudo apt-get libghc-zlib-dev
    make
    ln -s $pwd/minisat /usr/local/bin/minisat
    cd ../../

    # TODO: install python packages

    # If not...install python locally
    # Install python packages
elif [[ "OSTYPE" == "darwin"* ]]; then

    brew install python
    python setup.py develop

    cd lib/minisat-os-x
    make config prefix=$(pwd)
    make install

    ln -s $(pwd)/lib/libminisat.a /usr/local/lib/libminisat.a
    ln -s $(pwd)/lib/libminisat.so /usr/local/lib/libminisat.so
    ln -s $(pwd)/lib/libminisat.so.2 /usr/local/lib/libminisat.so.2
    ln -s $(pwd)/lib/libminisat.so.2.1.0 /usr/local/lib/libminisat.so.2.1.0
    ln -s $(pwd)/bin/minisat /usr/local/bin/minisat

    cd ../../
fi