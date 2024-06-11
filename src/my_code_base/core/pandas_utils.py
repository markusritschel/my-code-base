# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2024-06-11
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
import logging
import numpy as np
import pandas as pd
from .utils import centered_bins


log = logging.getLogger(__name__)


def grid_dataframe(points, vals, xi, export_grid=False):
    """Bin the values with `points` coordinates by the given target coordinates `xi` and put the average of each bin onto the target grid.

    Parameters
    ----------
    points : tuple[list, list]
        A tuple `(x, y)` consisting of two lists holding the respective x and y coordinates of the source data.
    values : list
        The actual data values that are meant to be regridded
    xi : tuple[list, list]
        A tuple `(x, y)` consisting of two lists holding the target coordinates.

    Example
    -------
    >>> pytest.skip()
    >>> df = pd.DataFrame({'lon': np.linspace(0, 40, 100),
    >>>                    'lat': np.sin(np.linspace(0, 3, 100))*10 + 40,
    >>>                    'data': np.linspace(240,200,100)})
    >>> xi = np.linspace(-5, 45, 40)
    >>> yi = np.linspace(35, 53, 50)
    >>> gridded = grid_dataframe((df.lon, df.lat), df.data, (xi, yi))
    >>> plt.pcolormesh(xi, yi, gridded, shading='auto', cmap='Greens_r')
    >>> plt.scatter(df.lon, df.lat, c=df.data, marker='.', lw=.75, cmap='Reds', label='raw data')
    >>> plt.xlabel('Longitude')
    >>> plt.ylabel('Latitude')
    >>> plt.legend()
    >>> plt.show()

    .. image:: /_static/grid_dataframe_plot.png
       :width: 450px
       :alt: example plot
       :align: left
    """
    x, y = points
    X, Y = xi
    xx, yy = np.meshgrid(*xi)
    target = np.empty(xx.shape) * np.nan

    # flatten target and grid components
    xx_ = xx.ravel()
    yy_ = yy.ravel()
    target_ = target.ravel()

    df = pd.DataFrame({'vals': vals, 'x': x, 'y': y})

    df['x_binned'] = pd.cut(df.x, bins=centered_bins(X), labels=X)
    df['y_binned'] = pd.cut(df.y, bins=centered_bins(Y), labels=Y)

    df['points'] = df[['x_binned', 'y_binned']].apply(tuple, axis=1)

    df_points_avg = df.groupby('points').mean()

    for idx, row in df_points_avg.iterrows():
        target_[(xx_ == idx[0]) & (yy_ == idx[1])] = row.vals

    target = target_.reshape(xx.shape)

    return (xx, yy, target) if export_grid else target
