#!/usr/bin/env python

# This implementation is based on
# https://www.dash-leaflet.com/docs/geojson_tutorial#a-choropleth-map

import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash import Dash, html, Output, Input
from dash_extensions.javascript import arrow_function, assign
import dash_core_components as dcc
import json
import numpy as np


def get_info(feature=None):
    header = [html.H4("US Population Density")]
    if not feature:
        return header + [html.P("Hover over a state")]
    return (
        header
        + [
            html.B(feature["properties"]["name"]),
            html.Br(),
            "{:.3f} people / mi".format(feature["properties"]["density"]),
            html.Sup("2"),
        ]
        + [html.B(), html.Br(), "{} something".format(feature["properties"]["xx"])]
    )


# # Create colorbar.
classes = [0, 10, 20, 50, 100, 200, 500, 1000]
style = dict(weight=2, opacity=1, color="white", dashArray="3", fillOpacity=0.7)
colorscale = [
    "#FFEDA0",
    "#FED976",
    "#FEB24C",
    "#FD8D3C",
    "#FC4E2A",
    "#E31A1C",
    "#BD0026",
    "#800026",
]
# js lib used for colors
chroma = "https://cdnjs.cloudflare.com/ajax/libs/chroma-js/2.1.0/chroma.min.js"
colorbar = dl.Colorbar(
    colorscale=colorscale, width=300, height=30, min=0, max=1000, position="bottomleft"
)  # , unit='/km2')

style_handle = assign(
    """function(feature, context){
    // get props from hideout
    const {min, max, classes, colorscale, style, colorProp} = context.hideout;
    // get value the determines the color
    const value = feature.properties[colorProp];
    // chroma lib to construct colorscale
    const csc = chroma.scale(colorscale).domain([min, max]);
    for (let i = 0; i < classes.length; ++i) {
        if (value > classes[i]) {
            // set color based on color prop
            style.fillColor = csc(feature.properties[colorProp]);
        }
    }
    return style;
}"""
)

# Load the different datasets
with open("assets/us-states.json", "r") as f:
    us_states = json.load(f)

# with open("assets/us-states-2.json", "r") as f:
#     us_states_2 = json.load(f)

# Create geojson
geojson = dl.GeoJSON(
    url="/assets/us-states.json",  # url to geojson file
    # how to style each polygon
    style=style_handle,
    # when true, zooms to bounds when data changes
    # (e.g. on load)
    # zoomToBounds=True,
    # when true, zooms to bounds of feature (e.g. polygon)
    # on click
    zoomToBoundsOnClick=True,
    # style applied on hover
    hoverStyle=arrow_function(dict(weight=1, color="#666", dashArray="")),
    hideout=dict(
        colorscale=colorscale,
        classes=classes,
        style=style,
        colorProp="density",
        min=0,
        max=1000,
    ),
    id="geojson",
)

# Create info control.
info = html.Div(
    children=get_info(),
    id="info",
    className="info",
    style={"position": "absolute", "top": "10px", "right": "10px", "zIndex": "1000"},
)

# Create app.
app = Dash(prevent_initial_callbacks=True, external_scripts=[chroma])
app.layout = html.Div(
    [
        dl.Map(
            children=[dl.TileLayer(), geojson, colorbar, info],
            style={"height": "50vh"},
            center=[40.52695, -97.59588],
            zoom=4,
        ),
        # Input component for user to specify density threshold
        html.Label("Density Threshold"),
        # Slider for density threshold
        dcc.Slider(
            id="density-threshold",
            min=0,
            max=max(classes),
            step=1,
            value=0,
            marks={i: str(i) for i in classes},
        ),
    ]
)


@app.callback(Output("geojson", "data"), Input("density-threshold", "value"))
def update_geojson(value):
    filtered_features = [
        feature
        for feature in us_states["features"]
        if feature["properties"]["density"] > value
    ]
    return {"type": "FeatureCollection", "features": filtered_features}


@app.callback(Output("info", "children"), Input("geojson", "hoverData"))
def info_hover(feature):
    return get_info(feature)


if __name__ == "__main__":
    app.run_server()
