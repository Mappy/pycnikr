"use strict";

// This class contains in its options an item named 'random' which,
// when printed, generates a random integer.
// This item can then be used in the pattern of the URL of the layer.
// This item will normally be ignored by the server (at least, this is
// the case for TileStache) and it will cheat leaflet, which otherwise,
// would use its own cache, which is different of the cache of the
// browser.
var random_layer = L.TileLayer.extend({
    options: {
        random: {
            toString: Math.random,
        }
    }
});

function get_layer(name) {
    var items = ["{{ tile_server_url.left }}",
                 name,
                 "{{ tile_server_url.center }}",
                 "{z}/{x}/{y}",
                 "{{ tile_server_url.right}}",
                 "?refresh={random}",
                ]
    var url = items.join("")
    return new random_layer(url);
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Check if the cookie string begins with the right name
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = cookie.substring(name.length + 1)
                cookieValue = decodeURIComponent(cookieValue);
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function ajaxSetup() {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            var csrftoken = getCookie("csrftoken");
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
    });
}

function aceEditor() {
    var editor = ace.edit("editor");
    editor.setTheme("ace/theme/twilight");
    editor.getSession().setMode("ace/mode/python");
    return editor;
}

function handleError(xhr) {
    var errorDetail;
    if (!xhr.readyState) {
        errorDetail = "SERVER UNREACHABLE";
    }
    else {
        var pattern = /[\s\S]*(Traceback:[\s\S]*)Request information/;
        errorDetail = pattern.exec(xhr.responseText)[1];
    }
    $("#errorDetail").text(errorDetail);
    $(".alert").show();
}

function add_layer(map, control) {
    var edited_layer = get_layer("{{ name }}");
    if (control != null) {
        control.addOverlay(edited_layer);
    }
    map.addLayer(edited_layer);
    $(".alert").hide();
    return edited_layer;
}

function remove_layer(map, edited_layer, control) {
    if (edited_layer != null) {
        map.removeLayer(edited_layer);
    }
    if (edited_layer != null && control != null) {
        control.removeLayer(edited_layer);
    }
}

function buttonsSetup(editor, map, control) {

    var edited_layer;

    var content;

    if (sessionStorage['pycnikr_show'] == null) {
        sessionStorage['pycnikr_show'] = "Code and map";
    }

    $("#previewButton").click( function() {

        var pycnikr_show = sessionStorage['pycnikr_show'];
        if (pycnikr_show == "Code and map") {
            show("#map", 6);
            show("#editor", 6);
        }
        else if (pycnikr_show == "Code only") {
            show("#editor", 12);
            hide("#map");
        }
        else if (pycnikr_show == "Map only") {
            hide("#editor");
            show("#map", 12);
        }
        else {
            alert('Invalid value for pycnikr_show (' + pycnikr_show + ')');
        }
        $("#showButton").text(pycnikr_show)

        var url = "preview/{{ name }}";
        var body = editor.getValue();
        $.post(url, body).done(
            function() {
                remove_layer(map, edited_layer, control);
                edited_layer = add_layer(map, control);
            }).fail(
                function(xhr) {
                    remove_layer(map, edited_layer, control);
                    handleError(xhr);
                });
    });

    $("#saveButton").click( function() {
        var url = "save/{{ name }}";
        var body = editor.getValue();
        $.post(url, body).done(
            function(result) {
                $(".alert").hide()
            }).fail(handleError);
    });

    $("#reloadButton").click( function() {
        window.location.reload();
    });

    function show(item, size) {
        var classes;
        var parent = $(item).parent();
        classes = parent.attr("class").split(" ");
        $.each(classes, function (index, item) {
            parent.removeClass(item)
        });
        parent.addClass("col-xs-" + size);
        parent.addClass("col-md-" + size);
        parent.show();
    }

    function hide(item) {
        $(item).parent().hide();
    }

    $("#show li a").click( function() {
        sessionStorage['pycnikr_show'] = $(this).text();
        $("#previewButton").trigger("click");
    })
}

$(document).ready(function() {

    // Set up the Ajax requests
    ajaxSetup();

    // Initialize the text editor
    var editor = aceEditor();

    // Initialize the map
    var map = L.map("map").setView({{ center }}, {{ zoom }});

    // Display the zoom and the center in the address bar
    var hash = new L.Hash(map);

    // Display on the bottom left the distance scale
    L.control.scale().addTo(map);

    // Display on the upper right the selector of the base layers if
    // the edited layer is an overlay
    var control;
    {% if base_layers %}
    {% for base_layer in base_layers %}
    var {{ base_layer }} = get_layer("{{ base_layer }}");
    {% endfor %}

    var baseLayers = {
        {% for base_layer in base_layers %}
        "{{ base_layer }}": {{ base_layer }},
        {% endfor %}
    };

    // We set the first base layer as the initial one
    map.addLayer({{ base_layers.0 }});

    control = L.control.activeLayers(baseLayers, {}, {collapsed: false});
    control.addTo(map);
    {% endif %}

    // Set the behavior of the buttons
    buttonsSetup(editor, map, control);

    // Click on Preview
    $("#previewButton").trigger("click");
});

