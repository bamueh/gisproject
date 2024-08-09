# Vulnerable populations affected by high temperatures in Zurich in summer 2022

This repo contains data and code to reproduce the work done for the GIS project that is part of the [CAS Geographic Information Systems and Analysis](https://ikg.ethz.ch/cas-ris/cas-ris.html) at ETH Zurich.

The frequency and intensity of heat waves and hot summers increases (Fischer & Knutti, 2015). People older than 65 years, especially older women, and people with cardiovascular diseases are particularly at risk from high temperatures (Benmarhnia et al., 2015). Cities tend to heat up more than the surrounding areas, due to built-up areas and blocked air flows (de Almeida et al., 2021). The heat in cities can be mitigated through structural measures such as greening roofs, using light-colored asphalt, or creating green spaces (de Almeida et al., 2021). Due to increased adverse health effects of heat on older people, it might be desirable to take into account not only temperature but also the age structure of the local population when planning and prioritizing such measures.

This project provides an interactive visualisation to allow the exploration of temperature across Zurich in relation to the age of the inhabitants.

![Website screenshot](./website.png)

## Generate data
To re-generate the data in this repo from scratch, download the raw data as described [here](data/README.md). Then run `$ make preprocess-landsat`, `$ make preprocess-population` and `$ make geojson`. The files of the last step of the processing done by those commands are in this repo, so if you don't want to start from scratch, you still have all the necessary data to work with.


## Run interactive website
To visualise temperature and population data and allow the user to interactively  explore where areas with high temperatures intersect with areas with a high number of older inhabitants I created a dash app. To run the app locally, `cd app` and then run `$ make server`.


## References
E. M. Fischer, R. Knutti, Anthropogenic contribution to global occurrence of heavy-precipitation and high-temperature extremes. Nat. Clim. Chang. 5, 560–564 (2015).

T. Benmarhnia, S. Deguen, J. S. Kaufman, A. Smargiassi, Review Article: Vulnerability to Heat-related Mortality: A Systematic Review, Meta-analysis, and Meta-regression Analysis. Epidemiology. 26, 781–793 (2015).

C. R. de Almeida, A. C. Teodoro, A. Gonçalves, Study of the Urban Heat Island (UHI) Using Remote Sensing Data/Techniques: A Systematic Review. Environments. 8, 105 (2021).
