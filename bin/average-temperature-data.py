#! usr/bin/env/python

import argparse
import rasterio
import numpy as np
from giscode.common import GOODSCENES, PROCLSDIR, NODATAVAL
from os.path import join


def main(outRaster):
    """
    Average temperature values from different input rasters.

    @param outRaster: The C{str} filename that the averaged raster will be
        written to.
    """
    # Instantiate the arrays
    arr = np.zeros((203, 205))
    arrCount = np.zeros((203, 205))

    # Loop through each scene, and at each pixel keep track of whether it has a
    # valid temperature and how many valid temperature readings there are at
    # each pixel. Then average temperature readings from all scenes with
    # available data.
    for file in GOODSCENES:
        ls = rasterio.open(file)

        counts = ls.read(1)
        counts[counts != NODATAVAL] = 1
        counts[counts == NODATAVAL] = 0

        arrCount += counts

        d = ls.read(1)
        d[d == NODATAVAL] = 0

        arr += d

        ls.close()

    # Average scenes
    arr = arr / arrCount

    # Save the average array
    # Open a source file
    tempRaster = rasterio.open(
        join(
            PROCLSDIR, "LC08_L2SP_194027_20220623_20220705_02_T1_ST_B10-resolution.TIF"
        )
    )

    kwargs = tempRaster.meta.copy()
    kwargs.update(
        {
            "driver": "GTiff",
            "width": tempRaster.shape[1],
            "height": tempRaster.shape[0],
            "count": 1,
            "dtype": "float64",
            "crs": tempRaster.crs,
            "transform": tempRaster.transform,
            "nodata": NODATAVAL,
        }
    )

    # Write the output file
    with rasterio.open(fp=outRaster, mode="w", **kwargs) as dst:
        dst.write(arr, 1)

    tempRaster.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Mask clouds in landsat data.",
    )

    parser.add_argument("--outRaster", help="The name of the output file.")

    args = parser.parse_args()

    main(args.outRaster)
