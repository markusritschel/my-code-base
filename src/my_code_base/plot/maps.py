# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2024-03-04
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
from abc import ABC, abstractmethod
import cartopy
import logging

log = logging.getLogger(__name__)


class GeoAxesAccessor(ABC):
    def __init__(self, ax):
        self.geo_axes = ax
        self._projection = self._get_cartopy_projection()

    def _get_cartopy_projection(self):
        return type(self.geo_axes._projection_init[1]['projection'])

    def add_ocean(self, **kwargs):
        """
        Add ocean feature to the :class:`~cartopy.mpl.geoaxes.GeoAxes`.

        Parameters
        ----------
        kwargs : dict
            Keyword arguments to be passed to the :meth:`~cartopy.mpl.geoaxes.GeoAxes.add_feature` method of :class:`~cartopy.mpl.geoaxes.GeoAxes`.
        """
        kwargs.setdefault('zorder', 0)
        self.geo_axes.add_feature(cartopy.feature.OCEAN, **kwargs)

    def add_land(self, **kwargs):
        """
        Add land feature to the :class:`~cartopy.mpl.geoaxes.GeoAxes`.

        Parameters
        ----------
        kwargs : dict
            Keyword arguments to be passed to the :meth:`~cartopy.mpl.geoaxes.GeoAxes.add_feature` method of :class:`~cartopy.mpl.geoaxes.GeoAxes`.
        """
        kwargs.setdefault('zorder', 2)
        self.geo_axes.add_feature(cartopy.feature.LAND, **kwargs)

    def add_coastlines(self, *args, **kwargs):
        """
        Add coastlines to the :class:`~cartopy.mpl.geoaxes.GeoAxes`.

        Parameters
        ----------
        args : list
            Arguments to be passed to the :meth:`~cartopy.mpl.geoaxes.GeoAxes.coastlines` method of :class:`~cartopy.mpl.geoaxes.GeoAxes`.
        kwargs : dict
            Keyword arguments to be passed to the :meth:`~cartopy.mpl.geoaxes.GeoAxes.coastlines` method of :class:`~cartopy.mpl.geoaxes.GeoAxes`.
        """
        kwargs.setdefault('zorder', 3)
        self.geo_axes.coastlines(*args, **kwargs)

    def set_extent(self, extent, crs=cartopy.crs.PlateCarree()):
        """
        Set the extent of the :class:`~cartopy.mpl.geoaxes.GeoAxes`.

        Parameters
        ----------
        extent : tuple
            The extent of the :class:`~cartopy.mpl.geoaxes.GeoAxes`. It should be a tuple of the form (xmin, xmax, ymin, ymax).
        crs : cartopy.crs
            The coordinate reference system in which the extent is expressed. Default is :class:`~cartopy.crs.PlateCarree`.
        """
        self.geo_axes.set_extent(extent, crs)

    @abstractmethod
    def add_gridlines(self):
        pass

    @abstractmethod
    def add_features(self):
        pass
