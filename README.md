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
    javascripts[shape=note, label="Third-parties Javascript files\\n(ace.js, leaflet.js, etc.)"];
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

## Install TileStache in a Vagrant VM

Install the Vagrant VM of
[TileStache](https://github.com/TileStache/TileStache):

    cd
    git clone git@github.com:TileStache/TileStache.git
    cd TileStache

Set the following synchronised folders in the file *Vagrantfile*:

    config.vm.synced_folder "~/TileStache", "/srv/tilestache"
    config.vm.synced_folder "~/pycnikr", "/srv/pycnikr"

Set the following port forwardings in the file *Vagrantfile*:

    config.vm.network :forwarded_port, host: 8001, guest: 8000
    config.vm.network :forwarded_port, host: 8081, guest: 8080

Connect to the Vagrant VM:

    vagrant up
    vagrant ssh

Execute the following steps inside the VM:

    pip uninstall PIL
    pip install Pillow
    pip install TileStache

## Install pycnik

The installation of TileStache already executed some steps required to install for the installation of [pycnik](https://github.com/Mappy/pycnik).

To finalize the installation of **pycnik**, complete the following steps inside the VM:

    LC_CTYPE=en_US.UTF-8
    sudo locale-gen
    sudo apt-get install libxslt1-dev
    pip install pycnik

## Install pycnikr

In the host:

    cd
    git clone https://github.com/Mappy/pycnikr.git


In the VM:

    pip install django
    pip install requests
    cd /srv/pycnikr
    cd tests
    nosetests

## Finalize Mapnik installation

To be able to render a raster on the map:

    sudo apt-get install mapnik-input-plugin-gdal

To be able to render a PostGIS database on the map:

    sudo apt-get install mapnik-input-plugin-postgis

# Configuration

## Configure pycnikr

In the VM, edit the settings of the Django server:

    cd /srv/pycnikr
    cd django_pycnikr
    vim settings.py

The settings to be configured are all prefixed by **PYCNIKR_**.

The meaning of the different parameters is detailed in the comments inside the
file *settings.py*.

## Configure TileStache

In the VM, edit the settings of TileStache:

    cd /srv/pycnikr
    cd tilestache
    vim tilestache.cfg

For each style sheet (say *style\_sheet.py*) contained in the style sheets directory configured in Django, there must be a layer configured in TileStache, with a **mapfile** parameter designating a file in the */tmp* directory and with the same name (i.e. */tmp/style\_sheet.xml* in our example).

# Usage

## Launch pycnikr

In the VM, lauch **pycnikr** in a shell:

    cd /srv/pycnikr
    python manage.py runserver 0.0.0.0:8000 --noreload

## Call pycnikr

In the host, launch a web browser.

Type *http://localhost:8001/example* in the address bar.

An HTML page should appear, split in two parts, with the code on the left side
and a tile on the right side.

# Replacement of TileStache by another tile server

The code of **pycnikr** contains a Django application named
**tilestache**, which manages the starting and the stopping of the
**TileStache** server when the Django server starts and stops.

It is normally relatively easy to adapt this application in order to create a
new application adapted to the needs of another tile server.

All in all, the replacement consists in the following steps:

* Install the system and Python dependencies of the new tile server
* Develop a new application using the application **tilestache** of **pycnikr**
as model
* Add the new application in the INSTALLED_APPS
* Remove **tilestache** from the INSTALLED_APPS
* Set the configuration of the new tile server so that it is consistent with
the XML templates generated by **pycnikr**  (see the section
[Configure TileStache](#Configure TileStache))
