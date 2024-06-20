# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2024-03-04
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
import logging
import cartopy.crs as ccrs
import numpy as np

log = logging.getLogger(__name__)


def fix_overlap(da, ax):
    """
    Fix overlapping geographic dimensions.
    This avoids artifacts when plotting contour lines of geographic data on a stereographic map
    projection.

    Calls :func:`z_masked_overlap` to perform the data transformation.

    Parameters
    ----------
    da:
        An :class:`xarray.DataArray` object with dimensions to be transformed.
    ax:
        A :class:`cartopy.mpl.geoaxes.GeoAxes` object with stereographic projection.
    """
    X, Y, masked_data = z_masked_overlap(ax,
                                         da['lon'].values,
                                         da['lat'].values,
                                         da.squeeze().values,
                                         source_projection=ccrs.Geodetic())
    da.data = masked_data
    da = da.assign_coords({'lon': (('y', 'x'), X),
                           'lat': (('y', 'x'), Y)})
    return da


def z_masked_overlap(axe, X, Y, Z, source_projection=None):
    """
    .. warning::
        Normally, one should avoid calling this function.
        Instead, use :func:`.fix_overlap` to fix the overlap.

    This function performs the actual transformation of the data for the :func:`.fix_overlap`
    function.

    It follows the solutions provided in the following issues:
        - https://github.com/SciTools/cartopy/issues/1225
        - https://github.com/SciTools/cartopy/issues/1421

    The function finds and masks the overlaps in the data that are more than half the
    range of the projection of the axes.

    Parameters
    ----------
    axe : cartopy.mpl.geoaxes.GeoAxes
        The axes object with the projection.
    X, Y : array_like
        The coordinates in the projection of the axes or the longitudes and latitudes.
    Z : array_like
        The data to be transformed.
    source_projection : cartopy.crs.CRS, optional
        If provided and is a geodetic CRS, the data is in geodetic coordinates and should
        first be projected in the projection of the axes.


    X and Y are 2D arrays with the same dimensions as Z for contour and contourf operations.
    They can also have an extra row and column for pcolor and pcolormesh operations.

    Returns
    -------
    ptx, pty, Z : list(numpy.ndarray)
        The transformed coordinates and data.
    """
    if not hasattr(axe, 'projection') or not isinstance(axe.projection, ccrs.Projection):
        return X, Y, Z

    if len(X.shape) != 2 or len(Y.shape) != 2:
        return X, Y, Z

    if source_projection is not None and isinstance(source_projection, ccrs.Geodetic):
        transformed_pts = axe.projection.transform_points(source_projection, X, Y)
        ptx, pty = transformed_pts[..., 0], transformed_pts[..., 1]
    else:
        ptx, pty = X, Y

    with np.errstate(invalid='ignore'):
        diagonal0_lengths = np.hypot(ptx[1:, 1:] - ptx[:-1, :-1], pty[1:, 1:] - pty[:-1, :-1])
        diagonal1_lengths = np.hypot(ptx[1:, :-1] - ptx[:-1, 1:], pty[1:, :-1] - pty[:-1, 1:])
        x_range = abs(axe.projection.x_limits[1] - axe.projection.x_limits[0])
        to_mask = (diagonal0_lengths > x_range / 2) | np.isnan(diagonal0_lengths) | (diagonal1_lengths > x_range / 2) | np.isnan(diagonal1_lengths)

        # TODO check if we need to do something about surrounding vertices

        # add one extra colum and row for contour and contourf
        if to_mask.shape[0] == Z.shape[0] - 1 and to_mask.shape[1] == Z.shape[1] - 1:
            to_mask_extended = np.zeros(Z.shape, dtype=bool)
            to_mask_extended[:-1, :-1] = to_mask
            to_mask_extended[-1, :] = to_mask_extended[-2, :]
            to_mask_extended[:, -1] = to_mask_extended[:, -2]
            to_mask = to_mask_extended

        if np.any(to_mask):
            Z_mask = getattr(Z, 'mask', None)
            to_mask = to_mask if Z_mask is None else to_mask | Z_mask
            Z = np.ma.masked_where(to_mask, Z)

        return ptx, pty, Z
