from setuptools import find_packages, setup
import os

here = os.path.abspath(os.path.dirname(__file__))

long_description = open(os.path.join(here, 'README.md')).read()

setup(
    name="gspatial_plot",
    packages=find_packages(include=["gspatial_plot"]),
    version="0.2.0",
    author="Ambee",
    license="MIT",
    url='https://github.com/ambeelabs/gspatial_plot/',
    description="A geospatial plotting library built on top of geopandas.",
    long_description_content_type="text/markdown",
    long_description=long_description,
    install_requires=[
        "Fiona>=1.8.22",
        "folium>=0.12.1.post1",
        "geopandas>=0.11.0",
        "mapclassify>=2.5.0",
        "matplotlib>=3.6.2",
        "pandas>=1.5.2",
        "pyproj>=3.4.1",
        "rasterio>=1.3.8",
        "rioxarray>=0.13.3",
        "scikit-learn>=1.0.1",
        "scipy>=1.10.0",
        "seaborn>=0.12.2",
        "Shapely>=1.8.2",
    ],
     classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
    ],
    keywords='geospatial plot geopandas maps plotting graph folium',
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    test_suite="tests",
    include_package_data=True,
)
