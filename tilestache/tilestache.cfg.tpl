{
  "cache":
  {
    "name": "Test",
    "path": "/tmp/stache",
    "umask": "0000",
    "verbose": true
  },
  "layers":
  {
  {% for layer, path in layers.items %}
      "{{ layer }}":
      {
        "provider":
        {
          "name": "mapnik",
          "mapfile": "{{ path }}"
        },
        "projection": "spherical mercator"
      }{% if not forloop.last %},{% endif %}
    {% endfor %}
  }
}
