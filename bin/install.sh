#!/usr/bin/env bash

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