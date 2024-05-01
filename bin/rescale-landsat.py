#! usr/bin/env/python


import argparse
import rasterio

from giscode.common import NODATAVAL


def main(inRaster, outRaster):
    """
    Re-scale the input raster file. The input raster file must be a Landsat 8
    or 9 Collection 2 Level 2 Science product containing surface temperature
    data. See https://www.usgs.gov/faqs/how-do-i-use-a-scale-factor-landsat-
    level-2-science-products for details. As the surface temperature data
    is in Kelvin, also convert to Celsius.

    @param inRaster: The C{str} name of the input file. Must be a Landsat 8 or
        9 file containint Surface Temperature information ending in *_B10.TIF.
    @param outRaster: The C{str} filename that the rescaled raster will be
        written to.
    """
    # Open the file
    raster = rasterio.open(inRaster)
    b10Data = raster.read(1)

    # Scale the surface temperature
    b10DataRescaled = (b10Data * 0.00341802) + 149

    # The no-data value is 0. If we convert to Celsius, some of the data may
    # be below 0, therefore we need to change the no-data value.
    b10DataRescaled[b10DataRescaled == 0] = NODATAVAL + 273.15

    # Convert to Celsius
    b10DataCelsius = b10DataRescaled - 273.15

    # Write the output file
    kwargs = raster.meta.copy()
    kwargs.update(
        {
            "driver": "GTiff",
            "width": raster.shape[1],
            "height": raster.shape[0],
            "count": 1,
            "dtype": "float64",
            "crs": raster.crs,
            "transform": raster.transform,
            "nodata": NODATAVAL,
        }
    )

    with rasterio.open(fp=outRaster, mode="w", **kwargs) as dst:
        dst.write(b10DataCelsius, 1)

    raster.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Re-scale landsat B10 band and convert to Celsius.",
    )

    parser.add_argument(
        "--inRaster", help="The name of the input file. Must end in *_B10.TIF."
    )

    parser.add_argument("--outRaster", help="The name of the output file.")

    args = parser.parse_args()

    main(args.inRaster, args.outRaster)
