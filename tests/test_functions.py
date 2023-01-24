import gspatial_plot as gsp


def test_dataset():
    assert str(type(gsp.us_states)) == "<class 'geopandas.geodataframe.GeoDataFrame'>"


def test_randommap():
    assert (
        str(type(gsp.randommap(gsp.us_states)))
        == "<class 'matplotlib.axes._subplots.AxesSubplot'>"
    )

def test_shapeplot():
    assert (
        str(type(gsp.shapeplot(gsp.us_states)))
        == "<class 'matplotlib.axes._subplots.AxesSubplot'>"
    )