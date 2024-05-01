.PHONY: download download-sensors preprocess-landsat preprocess-population reproject rescale clip mask-clouds resolution average population-raster clip-population geojson

## Commands for pre-processing data
# Download data
download:
	@echo Manually download remote sensing data, population statistics data and area files for Zurich as described in data/README.md
	download-sensors

# Preprocess the remote sensing data
preprocess-landsat:
	reproject rescale clip mask-clouds resolution average

# Preprocess the population data
preprocess-population:
	population-raster clip-population

# Make the GeoJSON file for displaying data in the web app.
geojson:
	python bin/make-geojson.py

## Individual commands
# Download sensor data
download-sensors:
	curl -L https://www.web.statistik.zh.ch/awel/LoRa/data/AWEL_Sensors_LoRa_202205.csv > data/sensors/AWEL_Sensors_LoRa_202205.csv
	curl -L https://www.web.statistik.zh.ch/awel/LoRa/data/AWEL_Sensors_LoRa_202206.csv > data/sensors/AWEL_Sensors_LoRa_202206.csv
	curl -L https://www.web.statistik.zh.ch/awel/LoRa/data/AWEL_Sensors_LoRa_202207.csv > data/sensors/AWEL_Sensors_LoRa_202207.csv
	curl -L https://www.web.statistik.zh.ch/awel/LoRa/data/AWEL_Sensors_LoRa_202208.csv > data/sensors/AWEL_Sensors_LoRa_202208.csv
	curl -L https://www.web.statistik.zh.ch/awel/LoRa/data/AWEL_Sensors_LoRa_202209.csv > data/sensors/AWEL_Sensors_LoRa_202209.csv

# Reproject remote sensing data from WGS84 to CH1903+ / LV95.
reproject:
	for dir in data/landsat/LC*; do \
		echo $$dir; \
		n=$$( echo $$dir | cut -d/ -f3); \
		gdalwarp -t_srs EPSG:2056 data/landsat/$$n/$$n\_ST_B10.TIF data/landsat/reprojected/$$n\_ST_B10-reprojected.TIF; \
		gdalwarp -t_srs EPSG:2056 data/landsat/$$n/$$n\_QA_PIXEL.TIF data/landsat/reprojected/$$n\_QA_PIXEL-reprojected.TIF; \
	done

# Re-scale the remote sensing data and convert from Kelvin to Celsius.
rescale:
	for dir in data/landsat/LC*; do \
		echo $$dir; \
		n=$$( echo $$dir | cut -d/ -f3); \
		python bin/rescale-landsat.py --inRaster data/landsat/reprojected/$$n\_ST_B10-reprojected.TIF --outRaster data/landsat/rescaled/$$n\_ST_B10-rescaled.TIF; \
	done

# Clip the remote sensing data to the area of Zurich.
clip:
	for dir in data/landsat/LC*; do \
		echo $$dir; \
		n=$$( echo $$dir | cut -d/ -f3); \
		echo data/landsat/$$n/$$n\_ST_B10.TIF; \
		gdalwarp -cutline data/gemeindegrenzen/UP_GEMEINDEN_OHNE_SEEN_F.shp -crop_to_cutline data/landsat/rescaled/$$n\_ST_B10-rescaled.TIF data/landsat/clipped/$$n\_ST_B10-clipped.TIF; \
		gdalwarp -cutline data/gemeindegrenzen/UP_GEMEINDEN_OHNE_SEEN_F.shp -crop_to_cutline data/landsat/reprojected/$$n\_QA_PIXEL-reprojected.TIF data/landsat/clipped/$$n\_QA_PIXEL-clipped.TIF; \
	done

# Mask the clouds in the remote sensing data.
mask-clouds:
	for dir in data/landsat/LC*; do \
		echo $$dir; \
		n=$$( echo $$dir | cut -d/ -f3); \
		python bin/mask-clouds.py --inRaster data/landsat/clipped/$$n\_ST_B10-clipped.TIF --outRaster data/landsat/masked/$$n\_ST_B10-masked.TIF; \
	done

# Change the resolution from 30x30 to 100x100m to match the population data. Suggested by ChatGPT.
resolution:
	for dir in data/landsat/LC*; do \
		echo $$dir; \
		n=$$( echo $$dir | cut -d/ -f3); \
		echo data/landsat/$$n/$$n\_ST_B10.TIF; \
		gdalwarp -tr 100 100 -te 2674600 1237800 2695100 1258100 -r near data/landsat/masked/$$n\_ST_B10-masked.TIF data/landsat/resolution/$$n\_ST_B10-resolution.TIF; \
	done

# Average remote sensing data
average:
	python bin/average-temperature-data.py --outRaster data/landsat/resolution/average-resolution.TIF

# Convert the population data to a raster dataset.
population-raster:
	python bin/rasterise-population-data.py --inCsv data/bevoelkerungsstatistik/Raumliche_Bevolkerungsstatistik_-OGD/BEVOELKERUNG_HA_P.csv --outRaster data/bevoelkerungsstatistik/Raumliche_Bevolkerungsstatistik_-OGD/BEVOELKERUNG_HA_P-raster.TIF; \

# Clip the population data to the area of Zurich.
clip-population:
	gdalwarp -cutline data/gemeindegrenzen/UP_GEMEINDEN_OHNE_SEEN_F.shp -crop_to_cutline data/bevoelkerungsstatistik/Raumliche_Bevolkerungsstatistik_-OGD/BEVOELKERUNG_HA_P-raster.TIF data/bevoelkerungsstatistik/Raumliche_Bevolkerungsstatistik_-OGD/BEVOELKERUNG_HA_P-raster-clipped.TIF; \

