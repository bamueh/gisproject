# Vulnerable populations affected by high temperatures in Zurich in summer 2022

This repo contains data and code to reproduce the work done for the GIS project that is part of the CAS Geographic Information Systems and Analysis at ETH Zurich.

The frequency and intensity of heat waves and hot summers are increasing. Vicedo-Cabrera et al., 2023 found 623 heat-related deaths in Switzerland for the period June-August 2022, which accounted for 3.5% of total mortality (2). Across Europe, over 60,000 heat-related deaths were estimated for the same period (3). People older than 64, especially older women, and people with cardiovascular diseases are particularly at risk from increased temperatures (4). Cities usually heat up more in hot weather than the surrounding area. Due to the health impacts of heat on older people, it may be desirable to consider not only temperature but also the age structure of the local population when planning and prioritising such measures.

This project provides an interactive visualisation to allow the exploration of temperature across Zurich in relation to the age of the inhabitants.

![Website screenshot](./website.png)

## Generate data
To re-generate the data in this repo from scratch, download the raw data as described [here](data/README.md). Then run `$ make preprocess-landsat`, `$ make preprocess-population` and `$ make geojson`. The files of the last step of the processing done by those commands are in this repo, so if you don't want to start from scratch, you still have all the necessary data to work with.


## Run interactive website
To visualise temperature and population data and allow the user to interactively  explore where areas with high temperatures intersect with areas with a high number of older inhabitants I created a dash app. To run the app locally, `cd app` and then run `$ make server`.
