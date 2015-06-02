#!/bin/bash -e

#### IMPORTANT NOTE !!!!!
# This file is an adaptation of
# https://github.com/TileStache/TileStache/blob/master/Vagrant/setup.sh
# A diff between this file and the original allows to understand the
# specifities of this file related to pycnikr

if [ -f ~/.bootstrap_complete ]; then
    exit 0
fi

set -x

whoami
sudo apt-get -q update
sudo apt-get -q install python-software-properties
sudo add-apt-repository ppa:mapnik/nightly-2.3 -y
sudo apt-get -q update
sudo apt-get -q install libmapnik-dev mapnik-utils python-mapnik virtualenvwrapper python-dev -y
sudo apt-get -q install gdal-bin=1.10.1+dfsg-5ubuntu1 -y
sudo apt-get -q install libgdal-dev=1.10.1+dfsg-5ubuntu1 -y

# create a python virtualenv
virtualenv -q ~/.virtualenvs/tilestache
source ~/.virtualenvs/tilestache/bin/activate

# make sure it gets activated the next time we log in
echo "source ~/.virtualenvs/tilestache/bin/activate" >> ~/.bashrc

# add system mapnik to virtualenv
ln -s /usr/lib/pymodules/python2.7/mapnik ~/.virtualenvs/tilestache/lib/python2.7/site-packages/mapnik

# for tests
sudo apt-get -q install postgresql-9.3-postgis-2.1 memcached -y
~/.virtualenvs/tilestache/bin/pip install nose coverage python-memcached psycopg2 werkzeug
~/.virtualenvs/tilestache/bin/pip install Pillow --allow-external Pillow --allow-unverified Pillow

# install basic TileStache requirements
~/.virtualenvs/tilestache/bin/pip install ModestMaps --allow-external ModestMaps --allow-unverified ModestMaps
~/.virtualenvs/tilestache/bin/pip install simplejson
~/.virtualenvs/tilestache/bin/pip install shapely

# workaround for gdal bindings
~/.virtualenvs/tilestache/bin/pip install --global-option=build_ext --global-option="-I/usr/include/gdal" GDAL==1.10.0

# allow any user to connect as postgres to this test data. DO NOT USE IN PRODUCTION
sudo sed -i '1i local  test_tilestache  postgres                     trust' /etc/postgresql/9.3/main/pg_hba.conf

sudo /etc/init.d/postgresql restart

# add some test data
sudo -u postgres psql -c "drop database if exists test_tilestache"
sudo -u postgres psql -c "create database test_tilestache"
sudo -u postgres psql -c "create extension postgis" -d test_tilestache
sudo -u postgres ogr2ogr -nlt MULTIPOLYGON -f "PostgreSQL" PG:"user=postgres dbname=test_tilestache" ./examples/sample_data/world_merc.shp

set +x
echo "
****************************************************************
* Warning: your postgres security settings (pg_hba.conf)
* are not setup for production (i.e. have been set insecurely).
****************************************************************"

# install TileStache
~/.virtualenvs/tilestache/bin/pip install TileStache

# install pycnik
echo "LC_CTYPE=en_US.UTF-8" >> ~/.bashrc
LC_CTYPE=en_US.UTF-8
sudo apt-get -q install libxslt1-dev

~/.virtualenvs/tilestache/bin/pip install pycnik

# install standard plugins for Mapnik
sudo apt-get -q install mapnik-input-plugin-gdal # for raster
sudo apt-get install mapnik-input-plugin-postgis # for PostGIS

# install the dependencies of pycnikr
~/.virtualenvs/tilestache/bin/pip install django
~/.virtualenvs/tilestache/bin/pip install requests

# we did it. let's mark the script as complete
touch ~/.bootstrap_complete
