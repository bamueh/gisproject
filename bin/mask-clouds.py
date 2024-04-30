#! usr/bin/env/python


import argparse
import numpy as np
import rasterio


def main(inRaster, outRaster):
    """
    Mask the clouds in landsat data. Be conservative and mask everything not
    marked as 'Clear' (21824).

    @param inRaster: The C{str} name of the input file. Must be a Landsat 8 or
        9 file containint Surface Temperature information ending in *_B10.TIF.
    @param outRaster: The C{str} filename that the rescaled raster will be
        written to.
    """
    # Open the file
    tempRaster = rasterio.open(inRaster)
    tempData = tempRaster.read(1)

    qaRaster = rasterio.open(inRaster[0:-19] + "_QA_PIXEL-clipped.TIF")
    qaData = qaRaster.read(1)

    # Create the mask (clear pixels only)
    qaData[qaData != 21824] = 1
    qaData[qaData == 21824] = 0

    # Mask out the surface temperature data
    masked = np.ma.masked_array(tempData, mask=qaData)

    # Write the output file
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
            "nodata": -999,
        }
    )

    with rasterio.open(fp=outRaster, mode="w", **kwargs) as dst:
        dst.write(masked, 1)

    tempRaster.close()
    qaRaster.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Mask clouds in landsat data.",
    )

    parser.add_argument(
        "--inRaster", help="The name of the input surface temperature raster."
    )

    parser.add_argument("--outRaster", help="The name of the output file.")

    args = parser.parse_args()

    main(args.inRaster, args.outRaster)
