import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import folium
from sklearn.neighbors import KNeighborsRegressor
from geopandas.plotting import _PolygonPatch
from shapely.affinity import scale
from shapely.geometry import shape, mapping
from shapely.validation import make_valid
from config import colors, countries, ocean, gridlines, rivers, lakes, us_states


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
    edgecolor="black",
    linewidth=0.5,
    color="grey",
    annot=False,
    annot_column=None,
    annot_align="center",
    annot_kwds={},
    ax=None,
    axis_on=False,
    **geopandas_plot_kwds,
):
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
    figsize=(15, 15),
    color="#ffb536",
    edgecolor="black",
    basecolor="grey",
    baseboundarycolor="black",
    base_boundary=True,
    boundary_linewidth=0.5,
    linewidth=0.5,
    title_kwds={},
    annot=False,
    annot_column=None,
    annot_align="center",
    annot_kwds={},
    ax=None,
    axis_on=False,
    facecolor="white",
    **geopandas_plot_kwds,
):
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
    scale_colorbar=False,
    legend=True,
    annot=False,
    annot_column=None,
    annot_align="center",
    annot_kwds={},
    ax=None,
    axis_on=False,
    **geopandas_plot_kwds,
):
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize, facecolor=facecolor)

    if title is not None:
        plt.title(title, **title_kwds)

    ax.axis("off")

    if axis_on == True:
        ax.axis("on")

    ax = data.boundary.plot(color=boundarycolor, linewidth=boundary_linewidth, ax=ax)

    if scale_colorbar == True:
        legend = False

    data.plot(
        ax=ax,
        column=column,
        cmap=cmap,
        scheme=scheme,
        legend=legend,
        **geopandas_plot_kwds,
    )

    if scale_colorbar == True:
        ax.figure.colorbar(ax.collections[1], fraction=0.023, ax=ax)

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
    scale_colorbar=False,
    legend=True,
    annot=False,
    annot_column=None,
    annot_align="center",
    annot_kwds={},
    ax=None,
    axis_on=False,
    **geopandas_plot_kwds,
):
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
        ax = data.boundary.plot(
            color=boundarycolor, linewidth=boundary_linewidth, ax=ax
        )
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

    if scale_colorbar == True:
        legend = False

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

    if scale_colorbar == True:
        ax.figure.colorbar(ax.collections[1], fraction=0.023, ax=ax)

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
    scale_colorbar=False,
    legend=True,
    annot=False,
    annot_column=None,
    annot_align="center",
    annot_kwds={},
    ax=None,
    axis_on=False,
    **geopandas_plot_kwds,
):
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

    ax = data.boundary.plot(color=boundarycolor, linewidth=boundary_linewidth, ax=ax)

    if scale_colorbar == True:
        legend = False

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

    if scale_colorbar == True:
        ax.figure.colorbar(ax.collections[1], fraction=0.023, ax=ax)

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
    scale_colorbar=False,
    ax=None,
    axis_on=False,
    **geopandas_plot_kwds,
):
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

    if point_data == False:
        plot_data = data.copy()
        plot_data["geometry"] = plot_data.representative_point()

    if scale_colorbar == True:
        legend = False

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
        else:
            patches = _PolygonPatch(clip, facecolor="white", edgecolor="white")

        for patch in patches:
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
    scale_colorbar=False,
    legend=True,
    ax=None,
    annot=False,
    annot_column=None,
    annot_align="center",
    annot_kwds={},
    axis_on=False,
    **geopandas_plot_kwds,
):
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
    else:
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

    if scale_colorbar == True:
        legend = False

    plot_data.plot(
        ax=ax,
        column=column,
        cmap=cmap,
        scheme=scheme,
        legend=legend,
        **geopandas_plot_kwds,
    )

    if scale_colorbar == True:
        ax.figure.colorbar(ax.collections[1], fraction=0.023, ax=ax)

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
        else:
            patches = _PolygonPatch(clip, facecolor="white", edgecolor="white")

        for patch in patches:
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
