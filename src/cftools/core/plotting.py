import os

import matplotlib.colors as mcolors
import matplotlib.dates as dates
import matplotlib.pyplot as plt
LinearSegmentedColormap = mcolors.LinearSegmentedColormap
from matplotlib.patches import Circle
from matplotlib import colormaps
import numpy as np
import pandas as pd
from scipy.interpolate import griddata
import yaml

from cftools.util import get_cftools_path

def plume_rose(chm_data, met_data, product: str, lat: int | str, lon: int | str, start_date: str, end_date: str, grid_res=0.1, show_bounds=True):
        """
        Return a plot of wind speed with pollutant concentration as the colormap.

            Parameters:
                    product (str): Chemical species available in CFAPI
                    lat (int | str): Latitude value
                    lon (int | str): Longitude value
                    start_date (str): Start of selected time window (format: YYYYMMDD)
                    end_date (str): End of selected time window (format: YYYYMMDD)
                    grid_res (float): Resolution of grid interpolation
                    show_bounds (bool): Boolean to toggle wind speed boundaries on plot

            Returns:
                    fig (matplotlib.figure.Figure): Requested plot
        """

        # Select and clean values for easier gridding and plotting.
        u = np.array(met_data['values']['U10M'])
        v = np.array(met_data['values']['V10M'])
        u = u.reshape((-1,1)).round(2)
        v = v.reshape((-1,1)).round(2)
        Z = np.array(chm_data['values'][product])
        Z = Z.reshape((-1,1))
        points = np.concat((u,v),axis=1)

        grid_res = grid_res
        show_bounds = show_bounds

        grid_x, grid_y = np.mgrid[np.min(u):np.max(u):grid_res,np.min(v):np.max(v):grid_res]
        z = griddata(points, Z,(grid_x,grid_y),method='linear')

        grid_x1D = grid_x.ravel()
        grid_y1D = grid_y.ravel()
        z1D = z.ravel()

        poslim, neglim = get_plot_bounds(grid_x, grid_y)

        fig, ax = plt.subplots()
        c = ax.scatter(grid_x1D,grid_y1D,c=z1D, zorder=0)
        ax.set_xlim(neglim, poslim)
        ax.set_ylim(neglim, poslim)
        for s in [[poslim-1, 0], [0,poslim-1], [neglim+1, 0], [0, neglim+1]]:
                ax.arrow(0,0, s[0], s[1],width=0.1, head_width=0.2, fc='k',zorder=1)
        cbar = fig.colorbar(c, ax=ax, extend='both', label=f'{product}')
        if show_bounds:
                circle_rad = get_radii(poslim)
                for r in circle_rad:
                        p = Circle((0,0), radius=r,ls='--',ec='k',fc=(0,0,0,0),zorder=(3))
                        ax.annotate(str(r)+' m/s', (((2**0.5)/2*r),((2**0.5)/2*r)),c=(.7,.7,.7)) # Multiplation of radius by sqrt(2)/2 moves annotation to circle edge
                        ax.add_patch(p)
        else:
              pass
        return fig

def vertical_profile(product, data):
        cftools_path = get_cftools_path()
        with open((cftools_path + '/config/config_plots.yml'), 'r') as ymlfile:
                config_plot = yaml.safe_load(ymlfile)

        p23_dict = data['values'][product]
        time_arr = data['time']

        for x in list(p23_dict.keys()):
                p23_dict[float(x)] = p23_dict.pop(x)

        time_arr = np.array([pd.to_datetime(x) for x in time_arr])

        plevs = [x for x in list(p23_dict.keys()) if x >= 500. and x <= 1000.]
        plevs.sort()

        X, Y = np.meshgrid(time_arr, plevs)
        Z = np.empty(shape = (len(plevs), len(time_arr)))
        for i in np.arange(len(time_arr)):
                for j, k in enumerate(plevs):
                        Z[j, i] = p23_dict[k][i]

        # Plotting specifications
        color_map = eval(config_plot['colors'][product])
        if isinstance(color_map, dict):
                color_map = mcolors.LinearSegmentedColormap('color_map', color_map)
                try:
                        colormaps.register(cmap=color_map)
                except:
                       pass
        else:
                pass
        mcmap = color_map
        cmaplist = [mcmap(i) for i in range(mcmap.N)]
        mcmap = mcolors.LinearSegmentedColormap.from_list('Custom cmap', cmaplist, mcmap.N)

        mcmap.set_under('w')
        mcmap.set_over('k')
        bounds = eval(config_plot['scale'][product])
        norm = eval(config_plot['contour']['norm'][product])

        title = config_plot['title'][product]
        units = config_plot['units'][product]
        l_width = 0.8
        ls = 9.0
        als = 10.0

        # Create subplots
        fig = plt.figure(figsize = (12, 8), linewidth = 0, edgecolor = 'w')
        ax = plt.subplot()

        CS = ax.contourf(X, Y, Z, levels = bounds, cmap=mcmap, norm=norm, extend='both')
        CS2 = ax.contour(X, Y, Z, levels = bounds, colors = ('k',), linewidths = (l_width,))
        ax.set_ylim(1000.0, 500.0)
        ax.set_ylabel('Pressure (hPa)', fontsize = als)
        ax.tick_params(axis='both', direction='out', labelsize = ls)
        ax.xaxis.set_major_formatter(dates.DateFormatter('%Hz'))
        ax.xaxis.set_major_locator(dates.HourLocator(byhour=list(range(0,24,12))))

        values_list = [500, 600, 700, 800, 900, 1000]

        ax.yaxis.set_ticks(values_list)
        ax.yaxis.set_ticklabels(values_list)

        cbar = fig.colorbar(CS, ax=ax, orientation = 'vertical', format=config_plot['contour']['cbar_form'][product], ticks = bounds)
        cbar.ax.yaxis.set_tick_params(pad=20)
        cbar.ax.set_ylabel('Concentration of {} ({})'.format(title, units), labelpad = 15, rotation = 270.0, fontsize = als)
        cbar.ax.set_yticklabels(bounds, ha='right', fontsize = ls)    

        try:
                plt.setp(CS.collections, linewidth=0.4)
                plt.setp(CS.collections, linestyle='-')
                tl = ax.clabel(CS2, fmt = config_plot['contour']['clab_form'][product], colors = 'k', fontsize = ls)
                for te in tl:
                        te.set_bbox(dict(color='w', alpha=0.8, pad=0.1))
        except:
                pass
                ax.patch.set_facecolor('silver')

        return fig

def get_plot_bounds(x, y):
    lim = max(abs(x).max(), abs(y).max())
    lim = lim + 1
    pos = lim
    neg = -lim
    return pos, neg

def get_radii(lim):
    if lim > 10:
        step = 5
    else:
        step = 1
    radii = np.arange(0,lim,step).tolist()[1:-1]
    return radii