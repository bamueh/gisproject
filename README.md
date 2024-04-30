# Vulnerable populations affected by high temperatures in Zurich in summer 2022

This repo contains data and code to reproduce the work done for the GIS project that is part of the CAS Geographic Information Systems and Analysis at ETH Zurich.


## Generate data
To re-generate the data in this repo from scratch, download the raw data as described [data/README.md](here). Then run `$ make preprocess-landsat`, `$ make preprocess-population` and `$ make geojson`. The files of the last step of the processing done by those commands are in this repo, so if you don't want to start from scratch, you still have all the necessary data to work with.


## Run interactive website
To visualise temperature and population data and allow the user to interactively  explore where areas with high temperatures intersect with areas with a high number of older inhabitants I created a dash app. The app can be run locally by running `$ make server`.
