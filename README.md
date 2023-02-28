# gspatial_plot

![](https://gspatial-plot.readthedocs.io/en/latest/_images/logo.png)

[![License](https://shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Downloads](https://static.pepy.tech/badge/gspatial-plot)](https://pepy.tech/project/gspatial-plot)
[![Documentation Status](https://readthedocs.org/projects/gspatial-plot/badge/?version=latest)](https://gspatial-plot.readthedocs.io/en/latest/?badge=latest)

A geospatial plotting library built on top of geopandas. The aim of this library is to simplify generation of various geospatial plot and provide a simple interface to various commonly used geospatial plot types.

# Documentation

[Welcome to gspatial-plot’s documentation! &mdash; gspatial-plot 0.1.0a0 documentation](https://gspatial-plot.readthedocs.io/en/latest/index.html)

# Features

1. Simple API

2. Better defaults compared to vanilla geopandas plot

3. Customizations made simple

4. Compatible with other geopandas or matplotlib axis objects

5. Provides functions for plotting bubbleplots, cartograms, heatmaps, spikemaps and densityplots

# Installing

`pip install gspatial-plot`

# Usage

```python
import gspatial_plot as gsp

usa = gsp.us_states


usa = usa[
    ~usa["NAME"].isin(
        [
            "Hawaii",
            "Guam",
            "American Samoa",
            "Commonwealth of the Northern Mariana Islands",
            "Alaska",
        ]
    )
]


gsp.randommap(usa, seed=3, annot=True, annot_column="NAME", figsize=(30, 30))
```

```python
gsp.shapeplot(usa, figsize=(15, 15))
```

```python
gsp.pointplot(usa_points, base=usa)
```

```python
gsp.choropleth(usa, "AWATER")
```

```python
gsp.bubblemap(usa, usa["AWATER"])
```

```python
gsp.cartogram(
    usa,
    "AWATER",
)
```

```python
gsp.densityplot(usa, clip=True, clip_factor=1.5)
```

```python
gsp.heatmap(usa, "AWATER")
```

```python
gsp.spikemap(usa, "AWATER")
```

```python
gsp.offline_static_basemap()
```

```python
gsp.offline_folium_basemap(crs="EPSG4326")
```
