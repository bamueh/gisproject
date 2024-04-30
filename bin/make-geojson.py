#! usr/bin/env/python

import rasterio
import numpy as np
from shapely import Polygon
import geopandas as gpd
from pysal.explore import esda
from pysal.lib import weights
from os.path import join

from giscode.common import GOODSCENES, PROCLSDIR, BEVDIR, TOPDIR


def main():
    """
    Function to aggregate all data in two GeoJSON files, one containing all
    cells within the city of Zurich and the other only containing those cells
    that are inhabited.
    """
    columns = {}
    # Read temperature values
    for i, file in enumerate(GOODSCENES):
        with rasterio.open(file) as src:
            image = src.read(1).astype("float64")
            name = file.split("_")[3]
            columns[name] = image.flatten()

    # Read bevoelkerungsstatistik
    with rasterio.open(join(BEVDIR, "BEVOELKERUNG_HA_P-raster-clipped.TIF")) as src:
        image1 = src.read(1).astype("float64")
        image2 = src.read(2).astype("float64")
        image3 = src.read(3).astype("float64")

        columns["perc_old"] = image1.flatten()
        columns["n_old"] = image2.flatten()
        columns["n_total"] = image3.flatten()

    # Generate the polygons
    with rasterio.open(join(PROCLSDIR, "average-resolution.TIF")) as src:
        image4 = src.read(1).astype("float64")

        columns["average_temp"] = image4.flatten()

        transform = src.transform

        polygons = []
        for row in range(src.height):
            for col in range(src.width):
                # Get the coordinates of the pixel
                lon, lat = rasterio.transform.xy(transform, row, col)
                # Create a polygon for the pixel
                polygon = Polygon(
                    [
                        [lon, lat],
                        [lon + transform.a, lat],
                        [lon + transform.a, lat - transform.e],
                        [lon, lat - transform.e],
                        [lon, lat],
                    ]
                )
                polygons.append(polygon)

    # Generate geodataframe
    data = gpd.GeoDataFrame(columns, geometry=polygons, crs="EPSG:2056")

    # Convert coordinate system
    data = data.to_crs("EPSG:4326")

    # Drop empty cells
    data.dropna(subset=["average_temp"], inplace=True)

    # # Calculate Getis-Ord Gi* statistic for average_temp
    # # Make weight matrix
    w = weights.KNN.from_dataframe(data, k=8)
    # Row-standardization
    w.transform = "R"
    # # Calculate G statistic
    go_i_star = esda.getisord.G_Local(data["average_temp"], w, star=True)
    # Add results to data frame
    result = []
    for p, z in zip(go_i_star.p_sim, go_i_star.Zs):
        if p > 0.05:
            result.append("ns")
        else:
            if z > 0:
                result.append("pos")
            elif z <= 0:
                result.append("neg")
    data["average_temp_gis"] = result

    # Drop cells without population data
    popData = data.loc[data.n_total != -999]

    # Convert to GeoJSON
    # I originally used this code to save the files within the working
    # directory that I wrote the app in. Keeping this in for the record.
    # popData.to_file(
    #     'notebooks/240420-playing-with-interactive-maps/assets/pop-data.json',
    #     driver="GeoJSON")
    # data.to_file(
    #     'notebooks/240420-playing-with-interactive-maps/assets/all-data.json',
    #     driver="GeoJSON")
    popData.to_file(join(TOPDIR, "data", "geojson", "pop-data.json"), driver="GeoJSON")
    data.to_file(join(TOPDIR, "data", "geojson", "all-data.json"), driver="GeoJSON")


if __name__ == "__main__":
    main()
