#! usr/bin/env/python


import argparse
import numpy as np
import pandas as pd
import rasterio
from rasterio.transform import from_origin
from rasterio import CRS

from giscode.common import NODATAVAL


def main(inCsv, outRaster):
    """
    Convert the population statistics dataset to raster. The population data
    CSV file has the filename 'BEVOELKERUNG_HA_P.csv' and was downloaded from
    https://www.geolion.zh.ch/geodatensatz/show?gdsid=63.

    @param inCsv: The C{str} name of the input csv file.
    @param outRaster: The C{str} filename that the rescaled raster will be
        written to.
    """
    # Open the file
    d = pd.read_csv(inCsv)

    # Add another column that calculates total number of >65 year olds
    d["J_65PLUS_T"] = d.apply(
        lambda row: (
            round((row["J_65_79_P"] + row["J_80PLUS_P"]) * row["PERS_N"] / 100, 0)
            if row["PERS_N"] != NODATAVAL
            else NODATAVAL
        ),
        axis=1,
    )

    # Add another column that summarises the fraction of people >65 years old
    d["J_65PLUS_P"] = d.apply(
        lambda row: (
            row["J_65_79_P"] + row["J_80PLUS_P"] if row["PERS_N"] != NODATAVAL else NODATAVAL
        ),
        axis=1,
    )

    # Get extent
    W = min(d["E"]) - 50
    E = max(d["E"]) + 50
    N = max(d["N"]) + 50
    S = min(d["N"]) - 50

    # Create arrays, suggested by ChatGPT
    # Total number of people
    total = np.full((int((N - S) / 100), int((E - W) / 100)), NODATAVAL)
    # Total number of people >65 years old
    totalOld = np.full((int((N - S) / 100), int((E - W) / 100)), NODATAVAL)
    # Fraction of people >65 years old.
    data = np.full((int((N - S) / 100), int((E - W) / 100)), NODATAVAL)

    for i, row in d.iterrows():
        wIndex = int((row["E"] - W) / 100)
        sIndex = int((row["N"] - S) / 100)
        total[268 - sIndex, wIndex] = float(row["PERS_N"])
        totalOld[268 - sIndex, wIndex] = float(row["J_65PLUS_T"])
        data[268 - sIndex, wIndex] = float(row["J_65PLUS_P"])

    # Save array as raster dataset
    new_dataset = rasterio.open(
        outRaster,
        "w",
        driver="GTiff",
        height=data.shape[0],
        width=data.shape[1],
        count=3,
        dtype=str(data.dtype),
        crs=CRS.from_epsg(2056),
        nodata=NODATAVAL,
        transform=from_origin(W, N, 100, 100),
    )

    # Add different bands to the raster data. Band 1 is the fraction of people
    # >65 years old, band 2 is the total number of people >65 years old, band
    # 3 is the total number of people.
    new_dataset.write(data, 1)
    new_dataset.write(totalOld, 2)
    new_dataset.write(total, 3)
    new_dataset.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Rasterise the population dataset.",
    )

    parser.add_argument("--inCsv", help="The name of the input CSV file.")

    parser.add_argument("--outRaster", help="The name of the output file.")

    args = parser.parse_args()

    main(args.inCsv, args.outRaster)
