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
    pycnik_lib[label="pycnik library"];
    pycnik_scripts[label="pycnik scripts"];
    tile_server[label="Tile server\\n(TileStache, TileCache, mod_tile, etc.)"];
    django[label="Django"];
    javascripts[shape=note, label="Third-parties Javascript files\\n(ace.js, leaflet.js, etc.)"];
    html[shape=note, label="Other static files\\n(HTML, CSS, PNG, etc.)"];
    browser[label="Web browser\\n(Chrome, Firefox, etc.)"];
    mapnik -> geo_data_source[label="read"];
    mapnik -> mapnik_templates[label="read"];
    pycnik_lib -> mapnik_templates[label="write"];
    pycnik_scripts -> pycnik_lib[label="call"];
    django -> pycnik_scripts[label="read/write/call"];
    django -> tile_server[label="start/stop"];
    subgraph cluster {
        label="pycnikr"
        django -> javascripts;
        django -> html;
    }
    browser -> django[label="pycnik scripts",dir="both",fontcolor="red"];
    browser -> tile_server[label="tiles",dir="both", fontcolor="red"];
    tile_server -> mapnik[label="tiles",dir="both", fontcolor="red"];
  }
)

# Preliminary remarks

**pycnikr** is only a software component and must be integrated with various third-parties
(a Linux distribution, a tile server, a browser, etc.).

In order to keep the installation as simple as possible, we assume in the following procedure that:

* The tile server is [TileStache](https://github.com/TileStache/TileStache)
* The whole system, except the browser, runs within a Vagrant VM

# Installation

To install the VM with **pycnikr**:

    git clone https://github.com/Mappy/pycnikr.git
    cd pycnikr
    vagrant up

# Usage

## Launch pycnikr

To lauch **pycnikr**:

    vagrant ssh
    pycnikr-runserver

## Call pycnikr

In the host, open a web browser at the address *http://localhost:8001/example*.

An HTML page should appear, split in two parts, with the code on the left side
and a tile on the right side.

# Configuration

## Configure pycnikr

To edit the settings of the Django server:

    vagrant ssh
    pycnikr-config

The settings to be configured are all prefixed by **PYCNIKR_**.

The meaning of the different parameters is detailed in the comments inside the
file *settings.py*.

## Configure TileStache

To edit the settings of **TileStache**:

    vagrant ssh
    pycnikr-config-tilestache

For each style sheet (say *style\_sheet.py*) contained in directory identified by the Django setting **PYCNIKR_STYLE_SHEETS_DIR**:
* There must be a layer configured in **TileStache**
* This layer must contain a **mapfile** parameter, which contains the path of an XML file
* The directory of this file must be the same as the Django setting **PYCNIKR_TMP_STYLE_SHEETS_DIR**
* The name of the file must be the same as the one of the style sheet (i.e. *style\_sheet.xml* in our example).

# Replacement of TileStache by another tile server

The code of **pycnikr** contains a Django application named
**tilestache**, which manages the starting and the stopping of the
**TileStache** server when the Django server starts and stops.

It is normally relatively easy to adapt this application in order to create a
new application adapted to the needs of another tile server.

All in all, the replacement consists in the following steps:

* Install in the VM the system and Python dependencies of the new tile server
* Remove **tilestache** from the INSTALLED_APPS
* To start and stop the new tile server, there are 2 possibilities:
 * Develop a new application using the application **tilestache** of **pycnikr**
as model and add it in the INSTALLED_APPS
 * Start and stop manually the new tile server when starting and stopping **pycnikr**
* Set the configuration of the new tile server so that it is consistent with
the XML templates generated by **pycnikr**  (see the section
[Configure TileStache](#Configure TileStache))
