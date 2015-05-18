# Principles

**pycnikr** is a tool to design [Mapnik](http://mapnik.org/) templates with
the [pycnik](https://github.com/Mappy/pycnik) library.

It allows to edit in a web browser **pycnik** scripts and to view in real-time
and in the same window the rendering of the corresponding **Mapnik** templates.

The main blocks of the environment of **pycnikr** are represented on the figure
below.

![Alt text](http://g.gravizo.com/g?
  digraph G {
    aize ="4,4";
    geo_data_source [shape=note, label="Geographical data source\\n(Shape file, PostGIS, etc.)"];
    mapnik_templates [shape=note, label="Mapnik templates (XML)"];
    mapnik[label="Mapnik 2.1"];
    pycnik_lib[label="Pycnik library"];
    pycnik_scripts[label="Pycnik scripts"];
    tile_server[label="Tile server\\n(mod_tile, TileCache, TileStache, etc.)"];
    django[label="Django"];
    javascripts[shape=note, label="Third-parties Javascript files\\n(ace.js, leaflet.js)"];
    html[shape=note, label="Other static files\\n(HTML, CSS, PNG, etc.)"];
    web_server[label="Web server\\n(NginX, Apache, etc.)"];
    browser[label="Web browser\\n(Chrome, Firefox, etc.)"];
    mapnik -> geo_data_source;
    mapnik -> mapnik_templates;
    pycnik_lib -> mapnik_templates;
    pycnik_scripts -> pycnik_lib;
    pycnik_lib -> mapnik
    django -> pycnik_scripts;
    django -> javascripts;
    django -> html;
    web_server -> django;
    browser -> web_server;
    browser -> tile_server;
    tile_server -> mapnik;
  }
)

# Installation

## Preliminary remarks

**pycnikr** is only a module and must be integrated with various third-parties
(a Linux distribution, a web server, a tile server, a browser, etc.).

In order to keep the installation procedure as simple as possible, we assume
the following:

* The tile server is [TileStache](https://github.com/TileStache/TileStache)
* The whole system runs within the Vagrant VM described in the
[TileStache Vagrantfile](https://github.com/TileStache/TileStache/blob/master/Vagrantfile).

## Install TileStache

Install first the Vagrant VM of
[TileStache](https://github.com/TileStache/TileStache).

    git clone git@github.com:TileStache/TileStache.git
    cd TileStache
    vagrant up

Then, connect to the vagrant VM:
    vagrant ssh

And execute the following steps from the VM:

    pip uninstall PIL
    pip install Pillow
    cd /srv/TileStache
    ./run_tests.sh
    python setup.py install

Note : an error can occur for one test : the osgeo TMS server can be unreachable. If it happens, do not worry and continue the installation procedure.

## Install pycnik

The installation of TileStache already executed some steps required to install
**pycnik**:

* Install the system packages **libmapnik-dev** and **python-mapnik**
* Make the **mapnik** python package installed at the system level available in
the virtual environment

The installation of **pycnik** must be completed with the following steps:

    sudo apt-get install libxslt1-dev
    pip install pycnik

## Install pycnikr

    pip install requests
    cd /srv/tilestache
    git clone https://github.com/Mappy/pycnikr.git
    cd pycnikr/tests
    nosetests

## Install django

    pip install django
