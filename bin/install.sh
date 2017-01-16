#!/usr/bin/env bash

# Assumes you have admin access
if [[ "$OSTYPE" == "linux-gnu" ]]; then
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
    # http://thelazylog.com/install-python-as-local-user-on-linux/
    mkdir ~/python
    cd ~/python
    # If don't have libssl-1.0.0, replace 2.7.13 everywhere with 2.6
    wget https://www.python.org/ftp/python/2.7.13/Python-2.7.13.tgz
    tar zxfv Python-2.7.13.tgz
    find ~/python -type d | xargs chmod 0755
    cd Python-2.7.13

    ./configure --prefix=$HOME/python
    make && make install

    echo "export PATH=$HOME/python/Python-2.7.13/:$PATH" >> ~/.bashrc_profile
    echo "export PYTHONPATH=$HOME/python/Python-2.7.13" >> ~/.bashrc_profile

    source ~/.bashrc_profile

    wget --no-check-certificate https://bootstrap.pypa.io/get-pip.py -O - | python - --user

    echo "export PATH=$HOME/.local/bin:$PATH" >> ~/.bashrc_profile

    source ~/.bashrc_profile

    # Install python packages
    python setup.py develop
elif [[ "$OSTYPE" == "darwin"* ]]; then

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