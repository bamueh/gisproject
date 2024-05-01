#!/usr/bin/env python

# This implementation is based on
# https://www.dash-leaflet.com/docs/geojson_tutorial#a-choropleth-map

import numpy as np
import dash_leaflet as dl
from dash import Dash, html, Output, Input, dcc
from dash_extensions.javascript import arrow_function, assign
import json

# Stylesheet to control style
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

external_scripts = [
    "https://cdnjs.cloudflare.com/ajax/libs/chroma-js/2.1.0/chroma.min.js"
]


def main(local):
    if local:
        dashApp = Dash(
            name=__name__,
            external_stylesheets=external_stylesheets,
            external_scripts=external_scripts,
        )
    else:
        dashApp = Dash(
            name=__name__,
            url_base_pathname="/casgis/",
            external_stylesheets=external_stylesheets,
            external_scripts=external_scripts,
        )

    def get_info(feature=None):
        """
        Function that curates information on hovering for the population map.
        """
        htmlStyle = {"color": "black", "fontSize": 14, "line-height": 10}

        header = [
            html.P(
                "Population information",
                style={
                    "color": "black",
                    "fontSize": 14,
                    "line-height": 10,
                    "font-weight": "bold",
                },
            )
        ]
        if not feature:
            return header + [html.P("Hover over a cell", style=htmlStyle)]
        return (
            header
            + [
                html.P(
                    f"{feature['properties']['n_total']} inhabitants", style=htmlStyle
                )
            ]
            + [
                html.P(
                    f"{feature['properties']['n_old']} inhabitants >65 yo",
                    style=htmlStyle,
                )
            ]
            + [
                html.P(
                    f"{feature['properties']['perc_old']:.1f}% inhabitants >65 yo",
                    style=htmlStyle,
                )
            ]
            + [
                html.P(
                    f"{feature['properties']['average_temp']:.2f} mean "
                    f"temperature (C)",
                    style=htmlStyle,
                )
            ]
        )

    def get_info_2(feature=None):
        """
        Function that curates information on hovering for the temperature map.
        """
        htmlStyle = {"color": "black", "fontSize": 14, "line-height": 10}

        header = [
            html.P(
                "Temperature information",
                style={
                    "color": "black",
                    "fontSize": 14,
                    "line-height": 10,
                    "font-weight": "bold",
                },
            )
        ]
        if not feature:
            return header + [html.P("Hover over a cell", style=htmlStyle)]
        return (
            header
            + [
                html.P(
                    f"{feature['properties']['average_temp']:.2f} mean "
                    f"temperature (C)",
                    style=htmlStyle,
                )
            ]
            + [
                html.P(
                    f"{feature['properties']['20220716']:.2f} 2022-07-16 "
                    f"temperature (C)",
                    style=htmlStyle,
                )
            ]
            + [
                html.P(
                    f"{feature['properties']['20220717']:.2f} 2022-07-17 "
                    f"temperature (C)",
                    style=htmlStyle,
                )
            ]
            + [
                html.P(
                    f"{feature['properties']['20220725']:.2f} 2022-07-25 "
                    f"temperature (C)",
                    style=htmlStyle,
                )
            ]
            + [
                html.P(
                    f"{feature['properties']['20220801']:.2f} 2022-08-01 "
                    f"temperature (C)",
                    style=htmlStyle,
                )
            ]
            + [
                html.P(
                    f"{feature['properties']['20220802']:.2f} 2022-08-02 "
                    f"temperature (C)",
                    style=htmlStyle,
                )
            ]
            + [
                html.P(
                    f"{feature['properties']['20220809']:.2f} 2022-08-09 "
                    f"temperature (C)",
                    style=htmlStyle,
                )
            ]
            + [
                html.P(
                    f"{feature['properties']['20220810']:.2f} 2022-08-10 "
                    f"temperature (C)",
                    style=htmlStyle,
                )
            ]
        )

    # Create colorbar.
    classes = list(range(20, 60, 5))
    colorscale = [
        "#5D00B4",
        "darkmagenta",
        "red",
        "orange",
        "yellow",
        "#FFFED6",
        "white",
    ][::-1]
    colorbar = dl.Colorbar(
        colorscale=colorscale,
        width=300,
        height=30,
        min=20,
        max=55,
        nTicks=8,
        position="bottomright",
    )
    colorbar_2 = dl.Colorbar(
        colorscale=colorscale,
        width=300,
        height=30,
        min=20,
        max=55,
        nTicks=8,
        position="bottomright",
    )

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

    # Load the population dataset
    with open("assets/pop-data.json", "r") as f:
        zh_population = json.load(f)

    # Load the temperature dataset
    with open("assets/all-data.json", "r") as f:
        temp_data = json.load(f)

    # Create geojson for the population dataset
    if local:
        popURL = "/assets/pop-data.json"
    else:
        popURL = "/casgis/assets/pop-data.json"
    geojson = dl.GeoJSON(
        url=popURL,
        # How to style each polygon
        style=style_handle,
        zoomToBoundsOnClick=True,
        # Style applied on hover
        hoverStyle=arrow_function(dict(weight=1, color="#666", dashArray="")),
        # How to style the cell
        hideout=dict(
            colorscale=colorscale,
            classes=classes,
            style={
                "weight": 0,
                "opacity": 1,
                "color": "white",
                "dashArray": "3",
                "fillOpacity": 0.9,
            },
            colorProp="average_temp",
            min=min(classes),
            max=max(classes),
        ),
        id="geojson",
    )

    # Create geojson for the temperature dataset
    if local:
        allURL = "/assets/all-data.json"
    else:
        allURL = "/casgis/assets/all-data.json"
    geojson_2 = dl.GeoJSON(
        url=allURL,
        style=style_handle,
        zoomToBoundsOnClick=True,
        hoverStyle=arrow_function(
            dict(weight=1, color="#666", dashArray="", fillOpacity=0.6)
        ),
        hideout=dict(
            colorscale=colorscale,
            classes=classes,
            style={
                "weight": 0,
                "opacity": 1,
                "color": "white",
                "dashArray": "3",
                "fillOpacity": 0.9,
            },
            # Default property value for coloring
            colorProp="average_temp",
            min=20,
            max=55,
        ),
        id="geojson_2",
    )

    # Create information control for the population dataset
    info = html.Div(
        children=get_info(),
        id="info",
        className="info",
        style={
            "position": "absolute",
            "top": "10px",
            "right": "10px",
            "zIndex": "1000",
        },
    )

    # Create information control for the temperature dataset
    info_2 = html.Div(
        children=get_info_2(),
        id="info_2",
        className="info",
        style={
            "position": "absolute",
            "top": "10px",
            "right": "10px",
            "zIndex": "1000",
        },
    )

    dashApp.layout = html.Div(
        [
            # Div containing title and text at the top spanning both columns.
            html.Div(
                [
                    html.H1(
                        children=(
                            "Vulnerable populations affected by high "
                            "temperatures in Zurich in summer 2022"
                        ),
                    ),
                    html.P(
                        "Due to climate change, the frequency and intensity of heat waves and hot summers increases (Fischer & Knutti, 2015). People older than 65 years, especially older women, and people with cardiovascular diseases are particularly at risk from high temperatures (Benmarhnia et al., 2015). Cities tend to heat up more than the surrounding areas, due to built-up areas and blocked air flows (de Almeida et al., 2021). The heat in cities can be mitigated through structural measures such as greening roofs, using light-colored asphalt, or creating green spaces (de Almeida et al., 2021). Due to increased adverse health effects of heat on older people, it might be desirable to take into account not only temperature but also the age structure of the local population when planning and prioritizing such measures.",
                    ),
                    html.P(
                        "The maps on this page give an overview of the temperature in Zürich on selected days in the summer of 2022 (left), and allows the user to interactively explore where areas with high temperatures intersect with areas with a high number of older inhabitants (right)."
                    ),
                ],
                style={
                    "marginLeft": 75,
                    "marginRight": 100,
                    "marginBottom": 20,
                    "marginTop": 50,
                },
            ),
            # Div containing text, map, and sliders for the temperature map.
            html.Div(
                [
                    # Add title and explanations for the temperature map
                    html.H2(
                        children="Temperature",
                    ),
                    html.P(
                        "The map below shows the temperature in Zurich during the summer of 2022, extracted from remote sensing data. Use the slider below the map to select the day, or view the temperature averaged across eight different days. The colour of each cell corresponds to the temperature.",
                    ),
                    # Add the map
                    dl.Map(
                        children=[
                            dl.TileLayer(),
                            # Don't zoom when scrolling the page
                            dl.GestureHandling(),
                            geojson_2,
                            colorbar_2,
                            info_2,
                            # dl.TileLayer(url="https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_nolabels/{z}/{x}/{y}.png"),
                        ],
                        style={
                            "height": "80vh",
                            "width": "100%",
                            "display": "inline-block",
                        },
                        center=[47.3793, 8.55938],
                        zoom=12,
                    ),
                    # Slider for which temperature map should be displayed
                    html.Label("Image date"),
                    html.Div(
                        [
                            dcc.Slider(
                                id="image",
                                min=0,
                                max=8,
                                step=1,
                                value=0,
                                marks={
                                    0: "Average",
                                    1: "2022-06-23",
                                    2: "2022-07-16",
                                    3: "2022-07-17",
                                    4: "2022-07-25",
                                    5: "2022-08-01",
                                    6: "2022-08-02",
                                    7: "2022-08-09",
                                    8: "2022-08-10",
                                },
                            ),
                        ],
                        style={"width": "100%"},
                    ),
                ],
                style={
                    "width": "45%",
                    "display": "inline-block",
                    "marginLeft": 75,
                    "marginTop": 30,
                    "marginRight": 0,
                },
            ),
            # Div containing text, map, and sliders for the population map.
            html.Div(
                [
                    # Add title and explanations
                    html.H2(
                        children="Population",
                    ),
                    html.P(
                        "The map shows inhabited areas in Zurich. The colour of the raster cells corresponds to the mean temperature. Use the sliders to interactively explore cells with a high number or percentage of inhabitants older than 65 years, areas with a high total number of inhabitants, or high temperatures.",
                    ),
                    # Add the map
                    dl.Map(
                        children=[
                            dl.TileLayer(),
                            # Don't zoom when scrolling the page
                            dl.GestureHandling(),
                            geojson,
                            colorbar,
                            info,
                            # Style the background map
                            dl.TileLayer(
                                url="https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_nolabels/{z}/{x}/{y}.png"
                            ),
                        ],
                        style={
                            "height": "80vh",
                            "width": "100%",
                            "display": "inline-block",
                        },
                        center=[47.3793, 8.55938],
                        zoom=12,
                    ),
                    # Add the sliders
                    # Slider for total people threshold
                    html.Label("Total inhabitants"),
                    html.Div(
                        [
                            dcc.Slider(
                                id="total-people",
                                min=0,
                                max=600,
                                step=1,
                                value=0,
                                marks={i: str(i) for i in range(0, 650, 50)},
                                tooltip={
                                    "placement": "bottom",
                                    "always_visible": False,
                                },
                            )
                        ],
                        style={"width": "100%"},
                    ),
                    # Slider for number of old people threshold
                    html.Label("Inhabitants >65 years old"),
                    html.Div(
                        [
                            dcc.Slider(
                                id="old-people",
                                min=0,
                                max=170,
                                step=1,
                                value=0,
                                marks={i: str(i) for i in range(0, 180, 10)},
                                tooltip={
                                    "placement": "bottom",
                                    "always_visible": False,
                                },
                            )
                        ],
                        style={"width": "100%", "marginleft": 75},
                    ),
                    # Slider for percentage of old people threshold
                    html.Label("Percentage of inhabitants >65 years old"),
                    html.Div(
                        [
                            dcc.Slider(
                                id="perc-old-people",
                                min=0,
                                max=100,
                                step=1,
                                value=0,
                                marks={i: str(i) for i in range(0, 110, 10)},
                                tooltip={
                                    "placement": "bottom",
                                    "always_visible": False,
                                },
                            )
                        ],
                        style={"width": "100%"},
                    ),
                    # Slider for average temperature threshold
                    html.Label("Average temperature"),
                    html.Div(
                        [
                            dcc.Slider(
                                id="temperature",
                                min=20,
                                max=55,
                                step=1,
                                value=0,
                                marks={i: str(i) for i in range(20, 60, 5)},
                                tooltip={
                                    "placement": "bottom",
                                    "always_visible": False,
                                },
                            )
                        ],
                        style={"width": "100%"},
                    ),
                    # Slider for average temperature threshold
                    # html.Label("Is temperature hotspot"),
                    html.Div(
                        [
                            dcc.Checklist(
                                options=[
                                    {
                                        "label": "Show temperature hotspots only",
                                        "value": 1,
                                    },
                                ],
                                value=[0],
                                id="hotspot",
                            )
                        ],
                        style={"width": "50%"},
                    ),
                ],
                style={
                    "width": "45%",
                    "display": "inline-block",
                    "marginLeft": 75,
                    "marginTop": 30,
                    "marginRight": 0,
                    "verticalAlign": "top",
                },
            ),
            # Div for the methodology
            html.Div(
                [
                    html.H5("Methods"),
                    html.P(
                        [
                            "This page was created by Barbara Mühlemann as part of the final project of the CAS in ",
                            html.A(
                                "Geographic Information Systems and Analysis",
                                href="https://ikg.ethz.ch/cas-ris/cas-ris.html",
                            ),
                            " at ETH Zürich. Population data is from the ",
                            html.A(
                                "Räumliche Bevölkerungsstatistik",
                                href="https://www.geolion.zh.ch/geodatensatz/show?gdsid=63",
                            ),
                            " of the Canton of Zurich. Temperature information is from the Landsat Collection 2 Level 2 surface temperature science product. Remote sensing data from 2022-05-01 to 2022-09-30 with less than 50% cloud cover was downloaded from ",
                            html.A("USGS", href="https://earthexplorer.usgs.gov/"),
                            ", re-scaled to 100x100 metre resolution, and masked, only retaining clear pixels. Only scenes with more than 97% clear pixels within the city of Zurich and an average temperature above 30C were retained, resulting in the eight scenes shown in the left map above. Temperature hotspots were identified using the Getis-Ord Gi* statistic. This page was implemented using ",
                            html.A(
                                "dash-leaflet", href="https://www.dash-leaflet.com/"
                            ),
                            ". Code for the data pre-processing and implementation of this app is available on ",
                            html.A("GitHub", href="https://github.com/bamueh/gisproject"), ".",
                        ]
                    ),
                    html.H5("References"),
                    html.P(
                        "E. M. Fischer, R. Knutti, Anthropogenic contribution to global occurrence of heavy-precipitation and high-temperature extremes. Nat. Clim. Chang. 5, 560–564 (2015)."
                    ),
                    html.P(
                        "T. Benmarhnia, S. Deguen, J. S. Kaufman, A. Smargiassi, Review Article: Vulnerability to Heat-related Mortality: A Systematic Review, Meta-analysis, and Meta-regression Analysis. Epidemiology. 26, 781–793 (2015)."
                    ),
                    html.P(
                        "C. R. de Almeida, A. C. Teodoro, A. Gonçalves, Study of the Urban Heat Island (UHI) Using Remote Sensing Data/Techniques: A Systematic Review. Environments. 8, 105 (2021)."
                    ),
                ],
                style={
                    "marginLeft": 75,
                    "marginRight": 100,
                    "marginBottom": 150,
                    "marginTop": 200,
                },
            ),
        ]
    )

    # Callback functions
    @dashApp.callback(
        Output("geojson", "data"),
        [
            Input("total-people", "value"),
            Input("old-people", "value"),
            Input("perc-old-people", "value"),
            Input("temperature", "value"),
            Input("hotspot", "value"),
        ],
    )
    def update_geojson(value1, value2, value3, value4, value5):
        """
        Callback function that controls the sliders for the population map.
        """
        filtered_features = [
            feature
            for feature in zh_population["features"]
            if feature["properties"]["n_total"] > value1
            and feature["properties"]["n_old"] > value2
            and feature["properties"]["perc_old"] > value3
            and feature["properties"]["average_temp"] > value4
        ]
        if value5 == [1]:
            filtered_features = [
                feature
                for feature in filtered_features
                if feature["properties"]["average_temp_gis"] == "pos"
            ]

        return {"type": "FeatureCollection", "features": filtered_features}

    @dashApp.callback(Output("info", "children"), Input("geojson", "hoverData"))
    def info_hover(feature):
        """
        Callback function that controls the information displayed on hovering
        for the population map.
        """
        return get_info(feature)

    # Callback to update the temperature image according to the slider in the
    # temperature map
    dashApp.clientside_callback(
        """
    function(x, y){
        var input_to_day = {
            0: "average_temp",
            1: "20220623",
            2: "20220716",
            3: "20220717",
            4: "20220725",
            5: "20220801",
            6: "20220802",
            7: "20220809",
            8: "20220810"
        };
        return {
            colorscale: y.colorscale,
            classes: y.classes,
            style: y.style,
            colorProp: input_to_day[x],
            min: y.min,
            max: y.max
        };}
    """,
        Output("geojson_2", "hideout"),
        [Input("image", "value"), Input("geojson_2", "hideout")],
    ),

    @dashApp.callback(Output("info_2", "children"), Input("geojson_2", "hoverData"))
    def info_hover_2(feature):
        """
        Callback function that controls the information displayed on hovering
        for the temperature map.
        """
        return get_info_2(feature)

    return dashApp


# Run the app
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=("Show CAS GIS app."),
    )

    parser.add_argument(
        "--local",
        action="store_true",
        help="Run in local mode. Else assume the app is running on civnb.info",
    )

    args = parser.parse_args()

    dashApp = main(args.local)

    dashApp.run_server(debug=True)

else:
    dashApp = main(False)
    app = dashApp.server
