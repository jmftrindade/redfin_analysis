# Description

Dead-simple analysis (e.g., simple histograms) of recently sold homes using Redfin data.

Currently only looks at specific types of homes [(2 to 3 BR, 1.25+ BA, 1200+ sqft)](https://github.com/jmftrindade/redfin_analysis/blob/b7754819c3b52d4190e8a9f4cdec005e7ee8a89c/main.py#L74) sold [in the last 90 days](https://github.com/jmftrindade/redfin_analysis/blob/master/main.py#L7), and only in [select cities from the Greater Boston area]((https://github.com/jmftrindade/redfin_analysis/blob/b7754819c3b52d4190e8a9f4cdec005e7ee8a89c/main.py#L171)).

# Requirements

For Jupyter notebooks:
```bash
# Install prereqs.
$ pip install wheel
$ pip install ipykernel jupyter
```

```
# Data processing.
$ pip install pandas
$ pip install numpy

# Optional if you do some ML.
$ pip install sklearn

# For seaborn cumulative distplots (aka CDFs).
$ pip install statsmodels
```

# Scrape Redfin Data

Slightly modified version of https://github.com/micahsteinberg/redfin-recently-sold-property-scraper.

Make sure to update the ids of cities of interest, which are [currently hardcoded in the script](https://github.com/jmftrindade/redfin_analysis/blob/b7754819c3b52d4190e8a9f4cdec005e7ee8a89c/main.py#L171).

This script uses Redfin *city* ids, and not neighborhood ids, e.g., you want "29663" (https://www.redfin.com/city/29663/MA/Burlington) and not "497396" (https://www.redfin.com/neighborhood/497396/MA/Burlington/Burlington) for Burlington, MA.

```
$ python3 main.py
```

# Run Notebook

```
$ jupyter notebook
```
