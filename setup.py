from setuptools import find_packages, setup

setup(
    name="gspatial_plot",
    packages=find_packages(include=["gspatial_plot"]),
    version="0.1.0",
    description="Simplifying geospatial plots in python. Aims to be seaborn equivalent for geospatial plots. Built on top of geopandas.",
    author="Ambeelabs",
    license="MIT",
    install_requires=[
        "Fiona>=1.8.22",
        "folium>=0.12.1.post1",
        "geopandas>=0.11.0",
        "mapclassify>=2.5.0",
        "matplotlib>=3.6.2",
        "pandas>=1.5.2",
        "pyproj>=3.4.1",
        "scikit-learn>=1.2.1",
        "scipy>=1.10.0",
        "seaborn>=0.12.2",
        "Shapely>=1.8.2",
    ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    test_suite="tests",
)
