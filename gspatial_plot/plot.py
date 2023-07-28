import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import folium
from sklearn.neighbors import KNeighborsRegressor
from geopandas.plotting import _PolygonPatch
from shapely.affinity import scale
from shapely.geometry import Polygon
from shapely.validation import make_valid
import rioxarray
from rasterio.plot import show
from .config import (
    colors,
    countries,
    ocean,
    gridlines,
    rivers,
    lakes,
    us_states,
)


def randommap(
    data,
    title=None,
    title_kwds={},
    figsize=(15, 15),
    facecolor="white",
    edgecolor="black",
    linewidth=0.5,
    seed=3,
    annot=False,
    annot_column=None,
    annot_align="center",
    annot_kwds={},
    ax=None,
    axis_on=False,
    colors=colors,
    **geopandas_plot_kwds,
):
    """
    Fills the data with random colors. Ideal for generating political maps.

    Args:
        data (GeoDataFrame): GeoDataFrame for which the map must be plotted
        title (str, optional): Title of the map. Defaults to None.
        title_kwds (dict, optional): Keyword arguments to matplotlib.pyplot.title. Defaults to {}.
        figsize (tuple, optional): Figure size. Defaults to (15, 15).
        facecolor (str, optional): Figure's face color. Defaults to "white".
        edgecolor (str, optional): Map's edge color. Defaults to "black".
        linewidth (float, optional): Width of lines for shapes. Defaults to 0.5.
        seed (int, optional): Seed for generating random colors. Defaults to 3.
        annot (bool, optional): If True, annotations are generated. Defaults to False.
        annot_column (str/GeoDataFrame column, optional): If annot is True, column should b passed as source for annotation. Defaults to None.
        annot_align (str, optional): Text alignment for annotation. Defaults to "center".
        annot_kwds (dict, optional): Keyword arguments for annotation. Defaults to {}.
        ax (matplotlib axis, optional): axis must be passed if plotting needs to be done on an existing axis. Defaults to None.
        axis_on (bool, optional): If True, axes will be visible. Defaults to False.
        colors (list/tuple, optional): List of colors to sample from. Defaults to a predefined set of colors.
        **geopandas_plot_kwds: Geopandas plot keyword arguments

    Returns:
        ax: matplotlib axis object

    """
    np.random.seed(seed=seed)
    colors = np.random.choice(colors, size=len(data))

    if ax is None:
        fig, ax = plt.subplots(figsize=figsize, facecolor=facecolor)

    if title is not None:
        plt.title(title, **title_kwds)

    ax.axis("off")

    if axis_on == True:
        ax.axis("on")

    ax = data.plot(
        color=colors,
        edgecolor=edgecolor,
        linewidth=linewidth,
        ax=ax,
        **geopandas_plot_kwds,
    )

    if annot == True and annot_column is not None:
        data.apply(
            lambda x: ax.annotate(
                text=x[annot_column],
                xy=x.geometry.representative_point().coords[0],
                ha=annot_align,
                **annot_kwds,
            ),
            axis=1,
        )

    return ax


def shapeplot(
    data,
    title=None,
    title_kwds={},
    figsize=(15, 15),
    facecolor="white",
    edgecolor="grey",
    linewidth=0.5,
    color="#F1F3F4",
    annot=False,
    annot_column=None,
    annot_align="center",
    annot_kwds={},
    ax=None,
    axis_on=False,
    **geopandas_plot_kwds,
):
    """

    Plots GeoDataFrame shapes. replacement for geopandas plot's default plot.

    Args:
        data (GeoDataFrame): GeoDataFrame for which the map must be plotted
        title (str, optional): Title of the map. Defaults to None.
        title_kwds (dict, optional): Keyword arguments to matplotlib.pyplot.title. Defaults to {}.
        figsize (tuple, optional): Figure size. Defaults to (15, 15).
        facecolor (str, optional): Figure's face color. Defaults to "white".
        edgecolor (str, optional): Map's edge color. Defaults to "black".
        linewidth (float, optional): Width of lines for shapes. Defaults to 0.5.
        color (str, optional): Color of the shape. Defaults to "#F1F3F4".
        annot (bool, optional): If True, annotations are generated. Defaults to False.
        annot_column (str/GeoDataFrame column, optional): If annot is True, column should b passed as source for annotation. Defaults to None.
        annot_align (str, optional): Text alignment for annotation. Defaults to "center".
        annot_kwds (dict, optional): Keyword arguments for annotation. Defaults to {}.
        ax (matplotlib axis, optional): axis must be passed if plotting needs to be done on an existing axis. Defaults to None.
        axis_on (bool, optional): If True, axes will be visible. Defaults to False.
        **geopandas_plot_kwds: Geopandas plot keyword arguments

    Returns:
        ax: matplotlib axis object

    """
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize, facecolor=facecolor)

    if title is not None:
        plt.title(title, **title_kwds)

    ax.axis("off")

    if axis_on == True:
        ax.axis("on")

    ax = data.plot(
        color=color,
        edgecolor=edgecolor,
        linewidth=linewidth,
        ax=ax,
        **geopandas_plot_kwds,
    )

    if annot == True and annot_column is not None:
        data.apply(
            lambda x: ax.annotate(
                text=x[annot_column],
                xy=x.geometry.representative_point().coords[0],
                ha=annot_align,
                **annot_kwds,
            ),
            axis=1,
        )

    return ax


def pointplot(
    data,
    base=None,
    title=None,
    title_kwds={},
    figsize=(15, 15),
    color="#ffb536",
    edgecolor="black",
    basecolor="#F1F3F4",
    baseboundarycolor="black",
    base_boundary=True,
    boundary_linewidth=0.5,
    linewidth=0.5,
    annot=False,
    annot_column=None,
    annot_align="center",
    annot_kwds={},
    ax=None,
    axis_on=False,
    facecolor="white",
    **geopandas_plot_kwds,
):
    """
    Plots point data. Can plot it over another GeoDataFrame

    Args:
        data (GeoDataFrame): GeoDataFrame for which the map must be plotted
        base (GeoDataFrame, optional): Base GeoDataFrame on top of which data must be plotted. Defaults to None.
        title (str, optional): Title of the map. Defaults to None.
        title_kwds (dict, optional): Keyword arguments to matplotlib.pyplot.title. Defaults to {}.
        figsize (tuple, optional): Figure size. Defaults to (15, 15).
        color (str, optional): Color of the point. Defaults to "#ffb536".
        edgecolor (str, optional): Map's edge color. Defaults to "black".
        basecolor (str, optional): Color of the base data. Defaults to "#F1F3F4".
        baseboundarycolor (str, optional): Boundary color of the base data. Defaults to "black".
        base_boundary (bool, optional): If Base data boundaries should be visible. Defaults to True.
        boundary_linewidth (float, optional): Linewidth of the base data boundaries. Defaults to 0.5.
        linewidth (float, optional): Width of lines for shapes. Defaults to 0.5.
        annot (bool, optional): If True, annotations are generated. Defaults to False.
        annot_column (str/GeoDataFrame column, optional): If annot is True, column should b passed as source for annotation. Defaults to None.
        annot_align (str, optional): Text alignment for annotation. Defaults to "center".
        annot_kwds (dict, optional): Keyword arguments for annotation. Defaults to {}.
        ax (matplotlib axis, optional): axis must be passed if plotting needs to be done on an existing axis. Defaults to None.
        axis_on (bool, optional): If True, axes will be visible. Defaults to False.
        facecolor (str, optional): Figure's face color. Defaults to "white".
        **geopandas_plot_kwds: Geopandas plot keyword arguments

    Returns:
        ax: matplotlib axis object

    """
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize, facecolor=facecolor)

    if title is not None:
        plt.title(title, **title_kwds)

    if base is not None:
        if base_boundary == True:
            ax = base.boundary.plot(
                color=baseboundarycolor,
                linewidth=boundary_linewidth,
                zorder=0,
                ax=ax,
            )
        else:
            ax = shapeplot(base, color=basecolor, linewidth=linewidth, ax=ax)

    ax.axis("off")

    if axis_on == True:
        ax.axis("on")

    data.plot(ax=ax, color=color, edgecolor=edgecolor, zorder=5, **geopandas_plot_kwds)

    if annot == True and annot_column is not None:
        data.apply(
            lambda x: ax.annotate(
                text=x[annot_column],
                xy=x.geometry.representative_point().coords[0],
                ha=annot_align,
                **annot_kwds,
            ),
            axis=1,
        )

    return ax


def choropleth(
    data,
    column,
    title=None,
    title_kwds={},
    figsize=(15, 15),
    cmap="YlOrRd",
    facecolor="white",
    scheme="percentiles",
    boundarycolor="black",
    boundary_linewidth=0.5,
    legend=True,
    annot=False,
    annot_column=None,
    annot_align="center",
    annot_kwds={},
    ax=None,
    axis_on=False,
    **geopandas_plot_kwds,
):
    """
    Generates Choropleth Map. Replacement for geopandas plot with a column passed in arguments.

    Args:
        data (GeoDataFrame): GeoDataFrame for which the map must be plotted
        column (str/GeoDataFrame column): Column for which choropleth map should be plotted
        title (str, optional): Title of the map. Defaults to None.
        title_kwds (dict, optional): Keyword arguments to matplotlib.pyplot.title. Defaults to {}.
        figsize (tuple, optional): Figure size. Defaults to (15, 15).
        cmap (str, optional): Colormap for the plot. Defaults to "YlOrRd".
        facecolor (str, optional): Figure's face color. Defaults to "white".
        scheme (str, optional): mapclassify scheme for assigning colors. Defaults to "percentiles".
        boundarycolor (str, optional): Map's boundary color. Defaults to "black".
        boundary_linewidth (float, optional): Linewidth of boundaries. Defaults to 0.5.
        legend (bool, optional): If True, legend is displayed. Defaults to True.
        annot (bool, optional): If True, annotations are generated. Defaults to False.
        annot_column (str/GeoDataFrame column, optional): If annot is True, column should b passed as source for annotation. Defaults to None.
        annot_align (str, optional): Text alignment for annotation. Defaults to "center".
        annot_kwds (dict, optional): Keyword arguments for annotation. Defaults to {}.
        ax (matplotlib axis, optional): axis must be passed if plotting needs to be done on an existing axis. Defaults to None.
        axis_on (bool, optional): If True, axes will be visible. Defaults to False.
        **geopandas_plot_kwds: Geopandas plot keyword arguments

    Returns:
        ax: matplotlib axis object

    """
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize, facecolor=facecolor)

    if title is not None:
        plt.title(title, **title_kwds)

    ax.axis("off")

    if axis_on == True:
        ax.axis("on")

    ax = data.boundary.plot(color=boundarycolor, linewidth=boundary_linewidth, ax=ax)

    data.plot(
        ax=ax,
        column=column,
        cmap=cmap,
        scheme=scheme,
        legend=legend,
        **geopandas_plot_kwds,
    )

    if annot == True and annot_column is not None:
        data.apply(
            lambda x: ax.annotate(
                text=x[annot_column],
                xy=x.geometry.representative_point().coords[0],
                ha=annot_align,
                **annot_kwds,
            ),
            axis=1,
        )

    return ax


def bubblemap(
    data,
    column,
    base=None,
    basecolor="#F1F3F4",
    baseboundarycolor="black",
    base_boundary=True,
    point_data=False,
    scale_factor=200,
    title=None,
    title_kwds={},
    figsize=(15, 15),
    linewidth=0.5,
    cmap="YlOrRd",
    edgecolor="black",
    facecolor="white",
    scheme="percentiles",
    boundarycolor="black",
    boundary_linewidth=0.5,
    legend=True,
    annot=False,
    annot_column=None,
    annot_align="center",
    annot_kwds={},
    ax=None,
    axis_on=False,
    **geopandas_plot_kwds,
):
    """
    Plots a bubble map.

    Args:
        data (GeoDataFrame): GeoDataFrame for which the map must be plotted
        column (str/GeoDataFrame column): Column for which the plot should be plotted
        base (GeoDataFrame, optional): Base GeoDataFrame on top of which data must be plotted. Defaults to None.
        basecolor (str, optional): Color of the base data. Defaults to "#F1F3F4".
        baseboundarycolor (str, optional): Boundary color of the base data. Defaults to "black".
        base_boundary (bool, optional): If Base data boundaries should be visible. Defaults to True.
        point_data (bool, optional): Must be true if the type of data being mapped is point shape. Defaults to False.
        scale_factor (int, optional): Scales the bubbles, higher scale factor means larger the bubble. Defaults to 200.
        title (str, optional): Title of the map. Defaults to None.
        title_kwds (dict, optional): Keyword arguments to matplotlib.pyplot.title. Defaults to {}.
        figsize (tuple, optional): Figure size. Defaults to (15, 15).
        linewidth (float, optional): Width of lines for shapes. Defaults to 0.5.
        cmap (str, optional): Colormap for the plot. Defaults to "YlOrRd".
        edgecolor (str, optional): Map's edge color. Defaults to "black".
        facecolor (str, optional): Figure's face color. Defaults to "white".
        scheme (str, optional): mapclassify scheme for assigning colors. Defaults to "percentiles".
        boundarycolor (str, optional): Map's boundary color. Defaults to "black".
        boundary_linewidth (float, optional): Linewidth of boundaries. Defaults to 0.5.
        legend (bool, optional): If True, legend is displayed. Defaults to True.
        annot (bool, optional): If True, annotations are generated. Defaults to False.
        annot_column (str/GeoDataFrame column, optional): If annot is True, column should b passed as source for annotation. Defaults to None.
        annot_align (str, optional): Text alignment for annotation. Defaults to "center".
        annot_kwds (dict, optional): Keyword arguments for annotation. Defaults to {}.
        ax (matplotlib axis, optional): axis must be passed if plotting needs to be done on an existing axis. Defaults to None.
        axis_on (bool, optional): If True, axes will be visible. Defaults to False.
        **geopandas_plot_kwds: Geopandas plot keyword arguments

    Returns:
        ax: matplotlib axis object

    """
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize, facecolor=facecolor)

    if title is not None:
        plt.title(title, **title_kwds)

    ax.axis("off")

    if axis_on == True:
        ax.axis("on")

    if point_data == False:
        plot_data = data.copy()
        plot_data["geometry"] = plot_data.representative_point()
        if type(column) == str:
            plot_data["size"] = (
                ((plot_data[column] - min(plot_data[column])))
                / (max(plot_data[column]) - min(plot_data[column]))
                * scale_factor
            )
        else:
            plot_data["size"] = (
                ((column - min(column))) / (max(column) - min(column)) * scale_factor
            )
        if base_boundary == True:
            ax = data.boundary.plot(
                color=boundarycolor, linewidth=boundary_linewidth, ax=ax
            )
        else:
            ax = shapeplot(data, color=basecolor, linewidth=linewidth, ax=ax)
    else:
        plot_data = data.copy()
        if type(column) == str:
            plot_data["size"] = (
                ((plot_data[column] - min(plot_data[column])))
                / (max(plot_data[column]) - min(plot_data[column]))
                * scale_factor
            )
        else:
            plot_data["size"] = (
                ((column - min(column))) / (max(column) - min(column)) * scale_factor
            )
        if base is not None:
            if base_boundary == True:
                ax = base.boundary.plot(
                    color=baseboundarycolor,
                    linewidth=boundary_linewidth,
                    zorder=0,
                    ax=ax,
                )
            else:
                ax = shapeplot(base, color=basecolor, linewidth=linewidth, ax=ax)

    plot_data.plot(
        ax=ax,
        column=column,
        markersize="size",
        linewidth=linewidth,
        cmap=cmap,
        edgecolor=edgecolor,
        scheme=scheme,
        legend=legend,
        **geopandas_plot_kwds,
    )

    if annot == True and annot_column is not None:
        data.apply(
            lambda x: ax.annotate(
                text=x[annot_column],
                xy=x.geometry.representative_point().coords[0],
                ha=annot_align,
                **annot_kwds,
            ),
            axis=1,
        )

    return ax


def cartogram(
    data,
    column,
    basecolor="#F1F3F4",
    base_boundary=True,
    cartogram_only=False,
    title=None,
    title_kwds={},
    figsize=(15, 15),
    linewidth=0.5,
    cmap="YlOrRd",
    edgecolor="black",
    facecolor="white",
    scheme="percentiles",
    boundarycolor="black",
    boundary_linewidth=0.5,
    legend=True,
    annot=False,
    annot_column=None,
    annot_align="center",
    annot_kwds={},
    ax=None,
    axis_on=False,
    **geopandas_plot_kwds,
):
    """
    Plots a cartogram

    Args:
        data (GeoDataFrame): GeoDataFrame for which the map must be plotted
        column (str/GeoDataFrame column): Column for which the plot should be plotted
        basecolor (str, optional): Color of the base data. Defaults to "#F1F3F4".
        base_boundary (bool, optional): If Base data boundaries should be visible. Defaults to True.
        cartogram_only (bool, optional): If True, function returns cartogram without base data. Defaults to False.
        title (str, optional): Title of the map. Defaults to None.
        title_kwds (dict, optional): Keyword arguments to matplotlib.pyplot.title. Defaults to {}.
        figsize (tuple, optional): Figure size. Defaults to (15, 15).
        linewidth (float, optional): Width of lines for shapes. Defaults to 0.5.
        cmap (str, optional): Colormap for the plot. Defaults to "YlOrRd".
        edgecolor (str, optional): Map's edge color. Defaults to "black".
        facecolor (str, optional): Figure's face color. Defaults to "white".
        scheme (str, optional): mapclassify scheme for assigning colors. Defaults to "percentiles".
        boundarycolor (str, optional): Map's boundary color. Defaults to "black".
        boundary_linewidth (float, optional): Linewidth of boundaries. Defaults to 0.5.
        legend (bool, optional): If True, legend is displayed. Defaults to True.
        annot (bool, optional): If True, annotations are generated. Defaults to False.
        annot_column (str/GeoDataFrame column, optional): If annot is True, column should b passed as source for annotation. Defaults to None.
        annot_align (str, optional): Text alignment for annotation. Defaults to "center".
        annot_kwds (dict, optional): Keyword arguments for annotation. Defaults to {}.
        ax (matplotlib axis, optional): axis must be passed if plotting needs to be done on an existing axis. Defaults to None.
        axis_on (bool, optional): If True, axes will be visible. Defaults to False.
        **geopandas_plot_kwds: Geopandas plot keyword arguments

    Returns:
        ax: matplotlib axis object

    """
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize, facecolor=facecolor)

    if title is not None:
        plt.title(title, **title_kwds)

    ax.axis("off")

    if axis_on == True:
        ax.axis("on")

    plot_data = data.copy()

    plot_data["repr_point"] = plot_data.representative_point()

    if type(column) == str:
        plot_data["size"] = plot_data[column] / plot_data[column].max()
    else:
        plot_data["size"] = column / column.max()

    scaled_geoms = [
        scale(
            x["geometry"],
            xfact=x["size"],
            yfact=x["size"],
            origin=x["repr_point"],
        )
        for x in plot_data.to_dict(orient="records")
    ]

    plot_data["geometry"] = scaled_geoms

    if cartogram_only == False:
        if base_boundary == True:
            ax = data.boundary.plot(
                color=boundarycolor, linewidth=boundary_linewidth, ax=ax
            )
        else:
            ax = shapeplot(data, color=basecolor, linewidth=linewidth, ax=ax)

    plot_data.plot(
        ax=ax,
        column=column,
        markersize="size",
        cmap=cmap,
        linewidth=linewidth,
        edgecolor=edgecolor,
        scheme=scheme,
        legend=legend,
        **geopandas_plot_kwds,
    )

    if annot == True and annot_column is not None:
        data.apply(
            lambda x: ax.annotate(
                text=x[annot_column],
                xy=x.geometry.representative_point().coords[0],
                ha=annot_align,
                **annot_kwds,
            ),
            axis=1,
        )

    return ax


def densityplot(
    data,
    base=None,
    clip=False,
    clip_factor=1.2,
    point_data=False,
    title=None,
    title_kwds={},
    figsize=(15, 15),
    cmap="YlOrRd",
    facecolor="white",
    boundarycolor="black",
    boundary_linewidth=0.5,
    ax=None,
    axis_on=False,
    **geopandas_plot_kwds,
):
    """
    Plots a kde plot over a GeoDataFrame

    Args:
        data (GeoDataFrame): GeoDataFrame for which the map must be plotted
        base (GeoDataFrame, optional): Base GeoDataFrame on top of which data must be plotted. Defaults to None.
        clip (bool, optional): If True, the plot is clipped to geo data boundary. Defaults to False.
        clip_factor (float, optional): Controls the scale of clipping mask, increase this if the plot is outside clipping boundary. Defaults to 1.2.
        point_data (bool, optional): Must be true if the type of data being mapped is point shape. Defaults to False.
        title (str, optional): Title of the map. Defaults to None.
        title_kwds (dict, optional): Keyword arguments to matplotlib.pyplot.title. Defaults to {}.
        figsize (tuple, optional): Figure size. Defaults to (15, 15).
        cmap (str, optional): Colormap for the plot. Defaults to "YlOrRd".
        boundarycolor (str, optional): Map's boundary color. Defaults to "black".
        boundary_linewidth (float, optional): Linewidth of boundaries. Defaults to 0.5.
        ax (matplotlib axis, optional): axis must be passed if plotting needs to be done on an existing axis. Defaults to None.
        axis_on (bool, optional): If True, axes will be visible. Defaults to False.
        **geopandas_plot_kwds: Geopandas plot keyword arguments


    Returns:
        ax: matplotlib axis object

    """
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize, facecolor=facecolor)

    if title is not None:
        plt.title(title, **title_kwds)

    ax.axis("off")

    if axis_on == True:
        ax.axis("on")

    if base is not None:
        ax = base.boundary.plot(
            color=boundarycolor,
            linewidth=boundary_linewidth,
            ax=ax,
            **geopandas_plot_kwds,
        )

    else:
        if point_data == False:
            ax = data.boundary.plot(
                color=boundarycolor,
                linewidth=boundary_linewidth,
                ax=ax,
                **geopandas_plot_kwds,
            )
    plot_data = data.copy()
    if point_data == False:
        plot_data["geometry"] = plot_data.representative_point()

    sns.kdeplot(
        x=plot_data["geometry"].x,
        y=plot_data["geometry"].y,
        fill=True,
        cmap=cmap,
        ax=ax,
    )

    if clip == True:
        if base is not None:
            not_clip = base.copy()
        else:
            not_clip = data.copy()

        not_clip["dissolve"] = "Dissolve"
        try:
            not_clip = not_clip.dissolve(by="dissolve")
        except:
            not_clip["geometry"] = not_clip["geometry"].apply(lambda x: make_valid(x))
            not_clip = not_clip.dissolve(by="dissolve")
        not_clip = not_clip.geometry[0]

        clip = scale(not_clip.envelope, xfact=clip_factor, yfact=clip_factor)
        clip = clip.difference(not_clip)

        if str(type(clip)) == "<class 'shapely.geometry.multipolygon.MultiPolygon'>":
            patches = [
                _PolygonPatch(geom, facecolor="white", edgecolor="white")
                for geom in clip.geoms
            ]
            for patch in patches:
                ax.add_patch(patch)
        else:
            patch = _PolygonPatch(clip, facecolor="white", edgecolor="white")
            ax.add_patch(patch)

    return ax


def heatmap(
    data,
    column,
    base=None,
    point_data=False,
    interpolate=False,
    interpolation_grid_space=0.05,
    clip=False,
    clip_factor=1.2,
    title=None,
    title_kwds={},
    figsize=(15, 15),
    cmap="YlOrRd",
    facecolor="white",
    scheme="percentiles",
    boundarycolor="black",
    boundary_linewidth=0.5,
    legend=True,
    ax=None,
    annot=False,
    annot_column=None,
    annot_align="center",
    annot_kwds={},
    axis_on=False,
    **geopandas_plot_kwds,
):
    """
    Plots heatmap. For polygons, the function returns a Choropleth map by default unless interpolated.

    Args:
        data (GeoDataFrame): GeoDataFrame for which the map must be plotted
        column (str/GeoDataFrame column): Column for which the plot should be plotted
        base (GeoDataFrame, optional): Base GeoDataFrame on top of which data must be plotted. Defaults to None.
        point_data (bool, optional): Must be true if the type of data being mapped is point shape. Defaults to False.
        interpolate (bool, optional): If True, data is interpolated using KNN. Defaults to False.
        interpolation_grid_space (float, optional): Grid Space for interpolation, Higher grid space needs more time and memory for interpolation. Defaults to 0.05.
        clip (bool, optional): If True, the plot is clipped to geo data boundary. Defaults to False.
        clip_factor (float, optional): Controls the scale of clipping mask, increase this if the plot is outside clipping boundary. Defaults to 1.2.
        title (str, optional): Title of the map. Defaults to None.
        title_kwds (dict, optional): Keyword arguments to matplotlib.pyplot.title. Defaults to {}.
        figsize (tuple, optional): Figure size. Defaults to (15, 15).
        cmap (str, optional): Colormap for the plot. Defaults to "YlOrRd".
        facecolor (str, optional): Figure's face color. Defaults to "white".
        scheme (str, optional): mapclassify scheme for assigning colors. Defaults to "percentiles".
        boundarycolor (str, optional): Map's boundary color. Defaults to "black".
        boundary_linewidth (float, optional): Linewidth of boundaries. Defaults to 0.5.
        legend (bool, optional): If True, legend is displayed. Defaults to True.
        annot (bool, optional): If True, annotations are generated. Defaults to False.
        annot_column (str/GeoDataFrame column, optional): If annot is True, column should b passed as source for annotation. Defaults to None.
        annot_align (str, optional): Text alignment for annotation. Defaults to "center".
        annot_kwds (dict, optional): Keyword arguments for annotation. Defaults to {}.
        ax (matplotlib axis, optional): axis must be passed if plotting needs to be done on an existing axis. Defaults to None.
        axis_on (bool, optional): If True, axes will be visible. Defaults to False.
        **geopandas_plot_kwds: Geopandas plot keyword arguments


    Returns:
        ax: matplotlib axis object
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize, facecolor=facecolor)

    if title is not None:
        plt.title(title, **title_kwds)

    ax.axis("off")

    if axis_on == True:
        ax.axis("on")

    if base is not None and point_data is True:
        ax = base.boundary.plot(
            color=boundarycolor, linewidth=boundary_linewidth, ax=ax
        )
    elif point_data is False:
        ax = data.boundary.plot(
            color=boundarycolor, linewidth=boundary_linewidth, ax=ax
        )

    plot_data = data.copy()

    if interpolate == True:
        grid_space = interpolation_grid_space

        minx, maxx = (
            plot_data["geometry"].total_bounds[0],
            plot_data["geometry"].total_bounds[2],
        )
        miny, maxy = (
            plot_data["geometry"].total_bounds[1],
            plot_data["geometry"].total_bounds[3],
        )

        grid_lon = np.arange(minx, maxx + grid_space, grid_space)
        grid_lat = np.arange(miny, maxy + grid_space, grid_space)

        all_lats = np.meshgrid(grid_lon, grid_lat)[1].ravel()
        all_lons = np.meshgrid(grid_lon, grid_lat)[0].ravel()
        del grid_lat, grid_lon

        pairs = list(zip(all_lats, all_lons))
        del all_lats, all_lons

        grid = pd.DataFrame(pairs, columns=["lat", "lon"])

        if point_data == False:
            plot_data["geometry"] = plot_data.representative_point()

        train = pd.DataFrame()
        train["lat"] = plot_data["geometry"].y
        train["lon"] = plot_data["geometry"].x

        if type(column) == str:
            train[column] = plot_data[column]
        else:
            train[column] = column

        model = KNeighborsRegressor(weights="distance", n_neighbors=len(train) - 1).fit(
            train[["lat", "lon"]], train[column].to_numpy().reshape(-1, 1)
        )

        grid[column] = model.predict(grid[["lat", "lon"]])

        grid = gpd.GeoDataFrame(
            grid, geometry=gpd.points_from_xy(grid["lon"], grid["lat"]), crs=data.crs
        )

        plot_data = grid

    plot_data.plot(
        ax=ax,
        column=column,
        cmap=cmap,
        scheme=scheme,
        legend=legend,
        **geopandas_plot_kwds,
    )

    if clip == True:
        if base is not None:
            not_clip = base.copy()
        else:
            not_clip = data.copy()

        not_clip["dissolve"] = "Dissolve"
        try:
            not_clip = not_clip.dissolve(by="dissolve")
        except:
            not_clip["geometry"] = not_clip["geometry"].apply(lambda x: make_valid(x))
            not_clip = not_clip.dissolve(by="dissolve")
        not_clip = not_clip.geometry[0]

        clip = scale(not_clip.envelope, xfact=clip_factor, yfact=clip_factor)
        clip = clip.difference(not_clip)

        if str(type(clip)) == "<class 'shapely.geometry.multipolygon.MultiPolygon'>":
            patches = [
                _PolygonPatch(geom, facecolor="white", edgecolor="white")
                for geom in clip.geoms
            ]
            for patch in patches:
                ax.add_patch(patch)
        else:
            patch = _PolygonPatch(clip, facecolor="white", edgecolor="white")
            ax.add_patch(patch)

    if annot == True and annot_column is not None:
        data.apply(
            lambda x: ax.annotate(
                text=x[annot_column],
                xy=x.geometry.representative_point().coords[0],
                ha=annot_align,
                **annot_kwds,
            ),
            axis=1,
        )

    return ax


def spikemap(
    data,
    column,
    shape="triangle",
    spike_only=False,
    base=None,
    basecolor="#F1F3F4",
    baseboundarycolor="black",
    base_boundary=True,
    point_data=False,
    not_wgs84=False,
    x_scale_factor=10,
    y_scale_factor=10,
    title=None,
    title_kwds={},
    figsize=(15, 15),
    linewidth=0.5,
    cmap="YlOrRd",
    edgecolor=None,
    facecolor="white",
    scheme="percentiles",
    boundarycolor="black",
    boundary_linewidth=0.5,
    legend=True,
    annot=False,
    annot_column=None,
    annot_align="center",
    annot_kwds={},
    ax=None,
    axis_on=False,
    **geopandas_plot_kwds,
):
    """
    Generates a spikemap.

    Args:
        data (GeoDataFrame): GeoDataFrame for which the map must be plotted
        column (str/GeoDataFrame column): Column for which the plot should be plotted
        shape (str, optional): Shape of spike, either rectangle or triangle. Defaults to "triangle".
        spike_only (bool, optional): If True, only spikes are returned without base map. Defaults to False.
        base (GeoDataFrame, optional): Base GeoDataFrame on top of which data must be plotted. Defaults to None.
        basecolor (str, optional): Color of the base data. Defaults to "#F1F3F4".
        baseboundarycolor (str, optional): Boundary color of the base data. Defaults to "black".
        base_boundary (bool, optional): If Base data boundaries should be visible. Defaults to True.
        point_data (bool, optional): Must be true if the type of data being mapped is point shape. Defaults to False.
        not_wgs84 (bool, optional): Needs to be true if data being plotted is not in WGS84/ESPG:4326. Defaults to False.
        x_scale_factor (int, optional): Scale factor for base of the shape. Defaults to 10.
        y_scale_factor (int, optional): Scale factor for height of the shape. Defaults to 10.
        title (str, optional): Title of the map. Defaults to None.
        title_kwds (dict, optional): Keyword arguments to matplotlib.pyplot.title. Defaults to {}.
        figsize (tuple, optional): Figure size. Defaults to (15, 15).
        linewidth (float, optional): Width of lines for shapes. Defaults to 0.5.
        cmap (str, optional): Colormap for the plot. Defaults to "YlOrRd".
        edgecolor (str, optional): Map's edge color. Defaults to "black".
        facecolor (str, optional): Figure's face color. Defaults to "white".
        scheme (str, optional): mapclassify scheme for assigning colors. Defaults to "percentiles".
        boundarycolor (str, optional): Map's boundary color. Defaults to "black".
        boundary_linewidth (float, optional): Linewidth of boundaries. Defaults to 0.5.
        legend (bool, optional): If True, legend is displayed. Defaults to True.
        annot (bool, optional): If True, annotations are generated. Defaults to False.
        annot_column (str/GeoDataFrame column, optional): If annot is True, column should b passed as source for annotation. Defaults to None.
        annot_align (str, optional): Text alignment for annotation. Defaults to "center".
        annot_kwds (dict, optional): Keyword arguments for annotation. Defaults to {}.
        ax (matplotlib axis, optional): axis must be passed if plotting needs to be done on an existing axis. Defaults to None.
        axis_on (bool, optional): If True, axes will be visible. Defaults to False.
        **geopandas_plot_kwds: Geopandas plot keyword arguments


    Returns:
        ax: matplotlib axis object

    """
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize, facecolor=facecolor)

    if title is not None:
        plt.title(title, **title_kwds)

    ax.axis("off")

    if axis_on == True:
        ax.axis("on")

    if point_data == False:
        plot_data = data.copy()
        plot_data["geometry"] = plot_data.representative_point()
        if type(column) == str:
            plot_data["size"] = plot_data[column] / plot_data[column].max()
        else:
            plot_data["size"] = column / column.max()
        if spike_only == False:
            if base_boundary == True:
                ax = data.boundary.plot(
                    color=boundarycolor, linewidth=boundary_linewidth, ax=ax
                )
            else:
                ax = shapeplot(data, color=basecolor, linewidth=linewidth, ax=ax)
    else:
        plot_data = data.copy()
        if type(column) == str:
            plot_data["size"] = plot_data[column] / plot_data[column].max()
        else:
            plot_data["size"] = column / column.max()
        if base is not None:
            if base_boundary == True:
                ax = base.boundary.plot(
                    color=baseboundarycolor,
                    linewidth=boundary_linewidth,
                    zorder=0,
                    ax=ax,
                )
            else:
                ax = shapeplot(base, color=basecolor, linewidth=linewidth, ax=ax)

    if not_wgs84 == True:
        original_crs = data.crs
        plot_data = plot_data.to_crs("4326")
    if shape == "rectangle":
        plot_data["geometry"] = plot_data.apply(
            lambda a: Polygon(
                [
                    [a.geometry.x - 0.01 * x_scale_factor, a.geometry.y],
                    [
                        a.geometry.x - 0.01 * x_scale_factor,
                        a.geometry.y + a["size"] * y_scale_factor,
                    ],
                    [
                        a.geometry.x + 0.01 * x_scale_factor,
                        a.geometry.y + a["size"] * y_scale_factor,
                    ],
                    [a.geometry.x + 0.01 * x_scale_factor, a.geometry.y],
                ],
            ),
            axis=1,
        )
    else:
        plot_data["geometry"] = plot_data.apply(
            lambda a: Polygon(
                [
                    [a.geometry.x - 0.01 * x_scale_factor, a.geometry.y],
                    [a.geometry.x, a.geometry.y + a["size"] * y_scale_factor],
                    [a.geometry.x + 0.01 * x_scale_factor, a.geometry.y],
                ],
            ),
            axis=1,
        )
    if not_wgs84 == True:
        plot_data = plot_data.to_crs(original_crs)
    plot_data.plot(
        ax=ax,
        column=column,
        linewidth=linewidth,
        cmap=cmap,
        edgecolor=edgecolor,
        scheme=scheme,
        legend=legend,
        **geopandas_plot_kwds,
    )

    if annot == True and annot_column is not None:
        data.apply(
            lambda x: ax.annotate(
                text=x[annot_column],
                xy=x.geometry.representative_point().coords[0],
                ha=annot_align,
                **annot_kwds,
            ),
            axis=1,
        )

    return ax


def offline_static_basemap(
    bounds=None,
    landcolor="#f1e9d7",
    watercolor="#7ae2ff",
    gridlinescolor="grey",
    gridlines_alpha=0.5,
    gridlines_width=0.5,
    figsize=(15, 15),
    title=None,
    title_kwds={},
    facecolor="white",
    edgecolor="black",
    edgewidth=0,
    linewidth=0,
    ax=None,
    axis_on=False,
    **geopandas_plot_kwds,
):
    """
    Generates a static basemap that can be used as base for other plots.
    This function can be used without internet as the map is generated using naturalearth vector data.

    Args:
        bounds (list/Geopandas Bounds, optional): Bounding box for clipping the basemap. Defaults to None.
        landcolor (str, optional): Color of land. Defaults to "#f1e9d7".
        watercolor (str, optional): Color of water. Defaults to "#7ae2ff".
        gridlinescolor (str, optional): Color of gridlines. Defaults to "grey".
        gridlines_alpha (float, optional): Opacity of gridlines. Defaults to 0.5.
        gridlines_width (float, optional): Linewidth of gridlines. Defaults to 0.5.
        figsize (tuple, optional): Figure size. Defaults to (15, 15).
        title (str, optional): Title of the map. Defaults to None.
        title_kwds (dict, optional): Keyword arguments to matplotlib.pyplot.title. Defaults to {}.
        facecolor (str, optional): Figure's face color. Defaults to "white".
        edgecolor (str, optional): Map's edge color. Defaults to "black".
        edgewidth (int, optional): Width of edges. Defaults to 0.
        linewidth (int, optional): Width of boundaries. Defaults to 0.
        ax (matplotlib axis, optional): axis must be passed if plotting needs to be done on an existing axis. Defaults to None.
        axis_on (bool, optional): If True, axes will be visible. Defaults to False.
        **geopandas_plot_kwds: Geopandas plot keyword arguments

    Returns:
        ax: matplotlib axis object
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize, facecolor=facecolor)

    if title is not None:
        plt.title(title, **title_kwds)

    ax.axis("off")

    if axis_on == True:
        ax.axis("on")

    if bounds is not None:
        xlim = [bounds[0], bounds[2]]
        ylim = [bounds[1], bounds[3]]
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)

    ax = countries.plot(
        ax=ax,
        figsize=figsize,
        color=landcolor,
        linewidth=edgewidth,
        edgecolor=edgecolor,
        **geopandas_plot_kwds,
    )
    ocean.plot(
        ax=ax,
        figsize=figsize,
        color=watercolor,
        linewidth=linewidth,
        edgecolor=edgecolor,
        **geopandas_plot_kwds,
    )
    gridlines.plot(
        ax=ax,
        figsize=figsize,
        color=gridlinescolor,
        alpha=gridlines_alpha,
        linewidth=gridlines_width,
        **geopandas_plot_kwds,
    )
    rivers.plot(
        ax=ax,
        figsize=figsize,
        color=watercolor,
        linewidth=linewidth,
        **geopandas_plot_kwds,
    )
    lakes.plot(
        ax=ax,
        figsize=figsize,
        color=watercolor,
        linewidth=linewidth,
        edgecolor=edgecolor,
        **geopandas_plot_kwds,
    )

    return ax


def offline_folium_basemap(
    location=[0, 0],
    landcolor="#f1e9d7",
    watercolor="#32d2ff",
    gridlinescolor="grey",
    gridlines_opacity=0.5,
    gridlines_weight=0.5,
    dash_array="5, 5",
    edgecolor="black",
    borders=0,
    linewidth=0.5,
    zoom_start=2,
    max_zoom=5,
    style_function=None,
    **folium_kwds,
):
    """
    Generates a interactive folium basemap that can be used as base for other plots.
    This function can be used without internet as the map is generated using naturalearth vector data.

    Args:
        location (list, optional): Location to center the basemap. Defaults to [0, 0].
        landcolor (str, optional): Color of land. Defaults to "#f1e9d7".
        watercolor (str, optional): Color of water. Defaults to "#32d2ff".
        gridlinescolor (str, optional): Color of gridlines. Defaults to "grey".
        gridlines_opacity (float, optional): Opacity of gridlines. Defaults to 0.5.
        gridlines_weight (float, optional): Linewidth of gridlines. Defaults to 0.5.
        dash_array (str, optional): Dash array parameter of folium map. Defaults to "5, 5".
        edgecolor (str, optional): Color of edges. Defaults to "black".
        borders (int, optional): Line width of borders. Defaults to 0.
        linewidth (float, optional): Linewidth of shapes. Defaults to 0.5.
        zoom_start (int, optional): Zoom start parameter of folium map. Defaults to 2.
        max_zoom (int, optional): Max zoom paraperter f folium map. Defaults to 5.
        style_function (_type_, optional): Folium style function. Defaults to None.
        **folium_kwds: Folium keywords

    Returns:
        m: Folium map object
    """
    m = folium.Map(
        location=location,
        tiles=None,
        zoom_start=zoom_start,
        max_zoom=max_zoom,
        **folium_kwds,
    )

    if style_function is None:
        land_json = folium.GeoJson(
            data=countries.to_json(),
            style_function=lambda x: {
                "fillColor": landcolor,
                "color": edgecolor,
                "weight": borders,
            },
        )
        ocean_json = folium.GeoJson(
            data=ocean.to_json(),
            style_function=lambda x: {
                "fillColor": watercolor,
                "color": edgecolor,
                "weight": linewidth,
            },
        )
        lines_json = folium.GeoJson(
            data=gridlines.to_json(),
            style_function=lambda x: {
                "color": gridlinescolor,
                "weight": gridlines_weight,
                "opacity": gridlines_opacity,
                "dashArray": dash_array,
            },
        )
        rivers_json = folium.GeoJson(
            data=rivers.to_json(),
            style_function=lambda x: {
                "fillColor": watercolor,
                "color": watercolor,
                "weight": linewidth,
            },
        )
        lakes_json = folium.GeoJson(
            data=lakes.to_json(),
            style_function=lambda x: {
                "fillColor": watercolor,
                "color": watercolor,
                "weight": linewidth,
            },
        )
    else:
        land_json = folium.GeoJson(
            data=countries.to_json(),
            style_function=style_function,
        )
        ocean_json = folium.GeoJson(data=ocean.to_json(), style_function=style_function)
        lines_json = folium.GeoJson(
            data=gridlines.to_json(),
            style_function=lambda x: style_function,
        )
        rivers_json = folium.GeoJson(
            data=rivers.to_json(),
            style_function=style_function,
        )
        lakes_json = folium.GeoJson(
            data=lakes.to_json(),
            style_function=style_function,
        )

    land_json.add_to(m)
    ocean_json.add_to(m)
    lines_json.add_to(m)
    rivers_json.add_to(m)
    lakes_json.add_to(m)

    return m


def plot_xarray_raster(
    data,
    field=None,
    title=None,
    title_kwds={},
    figsize=(15, 15),
    cmap="YlOrRd",
    clip_bbox=False,
    bounds=None,
    bounds_crs=None,
    clip_gdf=False,
    gdf=None,
    lower_limit=None,
    upper_limit=None,
    facecolor="white",
    robust=True,
    legend_kwds={},
    ax=None,
    axis_on=False,
    **xarray_plot_kwds,
):
    """Plots raster xarray data and returns axis. This is a wrapper around xarray plot function.

    Args:
        data (xarray Dataset/DataArray): Xarray raster data to plot
        field (str, optional): The field of Dataset to plot. This is only applicable for Dataset. Defaults to None.
        title (str, optional): Title for the plot. Defaults to None.
        title_kwds (dict, optional): title_kwds (dict, optional): Keyword arguments to matplotlib.pyplot.title. Defaults to {}.
        figsize (tuple, optional): Figure size. Defaults to (15, 15).
        cmap (str, optional): Colormap for the plot. Defaults to "YlOrRd".
        clip_bbox (bool, optional): Clips to bounds if True. Defaults to False.
        bounds (list, optional): Bounding box for clipping. Defaults to None.
        bounds_crs (str, optional): CRS for Bounding Box. Defaults to None.
        clip_gdf (bool, optional): Clips to a GeoDataFrame if True. Defaults to False.
        gdf (GeoDataFrame, optional): GeoDataFrame to clip the raster. Defaults to None.
        lower_limit (float, optional): Lower limit for the scale. Defaults to None.
        upper_limit (float, optional):  Upper limit for the scale. Defaults to None.
        facecolor (str, optional): Figure's face color. Defaults to "white".
        robust (bool, optional): Uses data between 2% to 98% for figure scale if True. Defaults to True.
        legend_kwds (dict, optional): Keywords for colorbar/legend. Defaults to {}.
        ax (matplotlib axis, optional): axis must be passed if plotting needs to be done on an existing axis. Defaults to None.
        axis_on (bool, optional): If True, axes will be visible. Defaults to False.
        **xarray_plot_kwds: Keywords for xarray plot.

    Returns:
        ax: matplotlib axis object
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize, facecolor=facecolor)

    ax.axis("off")

    if axis_on == True:
        ax.axis("on")
    if field is not None:
        data = data[field]
    if clip_bbox == True:
        if bounds_crs is not None:
            data = data.rio.clip_box(
                bounds[0], bounds[1], bounds[2], bounds[3], crs=bounds_crs
            )
        else:
            data = data.rio.clip_box(bounds[0], bounds[1], bounds[2], bounds[3])
    if clip_gdf == True:
        data = data.rio.clip(gdf.geometry.values, gdf.crs, drop=True)
    if lower_limit is not None:
        data = data.where(data >= lower_limit)
    if upper_limit is not None:
        data = data.where(data <= upper_limit)
    if len(legend_kwds) > 0:
        data.plot(
            ax=ax,
            cmap=cmap,
            robust=robust,
            cbar_kwargs=legend_kwds,
            **xarray_plot_kwds,
        )
    else:
        data.plot(
            ax=ax,
            cmap=cmap,
            robust=robust,
            **xarray_plot_kwds,
        )
    if title is not None:
        ax.set_title(title, **title_kwds)
    return ax


def show_raster(
    data,
    title=None,
    title_kwds={},
    figsize=(15, 15),
    cmap="YlOrRd",
    facecolor="white",
    colorbar=False,
    legend_kwds={},
    ax=None,
    axis_on=False,
    **show_kwds,
):
    """Wrapper around rasterio show with additional functionalities like better defaults and colorbar.

    Args:
        data (rasterio DatasetReader): Data to plot
        title (str, optional): Title for the plot. Defaults to None.
        title_kwds (dict, optional): title_kwds (dict, optional): Keyword arguments to matplotlib.pyplot.title. Defaults to {}.
        figsize (tuple, optional): Figure size. Defaults to (15, 15).
        cmap (str, optional): Colormap for the plot. Defaults to "YlOrRd".
        facecolor (str, optional): Figure's face color. Defaults to "white".
        colorbar (bool, optional): Inserts colorbar if True. Defaults to False.
        legend_kwds (dict, optional): Keywords for colorbar/legend. Defaults to {}.
        ax (matplotlib axis, optional): axis must be passed if plotting needs to be done on an existing axis. Defaults to None.
        axis_on (bool, optional): If True, axes will be visible. Defaults to False.
        **show_kwds: Additional keywords for rasterio show function
    Returns:
        ax: matplotlib axis object
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize, facecolor=facecolor)

    if title is not None:
        plt.title(title, **title_kwds)

    ax.axis("off")
    if axis_on == True:
        ax.axis("on")

    plot = show(data, ax=ax, cmap=cmap, **show_kwds)
    if colorbar == True:
        im = plot.get_images()[0]
        fig.colorbar(im, ax=ax, **legend_kwds)
    return ax
