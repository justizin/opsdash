#!/bin/sh

mkdir python
cd python
curl -O http://python.org/ftp/python/2.7.2/Python-2.7.2.tar.bz2
tar jxvpf Python-2.7.2.tar.bz2
cd Python-2.7.2
./configure --prefix=$HOME/opsdash/python/
nice make
nice make install
cd $HOME/opsdash
curl -O http://python-distribute.org/distribute_setup.py
python/bin/python distribute_setup.py
python/bin/easy_install virtualenv
python/bin/virtualenv .
hg clone http://hg.sqlalchemy.org/sqlalchemy/
cd sqlalchemy
../bin/python setup.py develop
cd $HOME/opsdash 
git clone http://github.com/ptahproject/ptah.git
cd ptah
../bin/python setup.py develop
cd $HOME/opsdash 
./bin/python bootstrap.py

