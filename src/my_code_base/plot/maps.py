# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2024-03-04
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
from abc import ABC, abstractmethod
import functools
import cartopy
import cartopy.mpl.geoaxes
import logging
import pytest

log = logging.getLogger(__name__)


def register_geoaxes_accessor(accessor_name):
    """
    A decorator to register an accessor for a :class:`cartopy.mpl.geoaxes.GeoAxes` object.

    Example
    -------
    >>> pytest.skip()
    >>> @register_geoaxes_accessor("my_accessor")
    >>> class MyCustomAccessor:
    >>>     def some_method(self):
    >>>         pass
    >>>
    >>> ax = plt.subplot(projection=cartopy.crs.NorthPolarStereo())
    >>> ax.my_accessor.some_method()
    """
    def actual_decorator(cls):
        @functools.wraps(cls)
        def accessor(geo_axes):
            log.debug("`accessor` func")
            if not hasattr(geo_axes, '_'+accessor_name):
                log.debug("No instance of accessor found. Add as attribute.")
                setattr(geo_axes, '_'+accessor_name, cls(geo_axes))
            return getattr(geo_axes, '_'+accessor_name)

        setattr(cartopy.mpl.geoaxes.GeoAxes, accessor_name, property(accessor))

        return cls

    return actual_decorator


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


@register_geoaxes_accessor("polar")
class StereographicAxisAccessor(GeoAxesAccessor):
    """An accessor to handle features and finishing of stereographic plots produced with `cartopy`.
    Can handle both :class:`~cartopy.crs.NorthPolarStereo` and :class:`~cartopy.crs.SouthPolarStereo` projections."""

    def __init__(self, ax):
        super().__init__(ax)
        self._pole = {cartopy.crs.SouthPolarStereo: 'south',
                      cartopy.crs.NorthPolarStereo: 'north'}[self._projection]

    @property
    def lat_limits(self):
        """Get and set the latitude limits for the plot."""
        pass

    @lat_limits.setter
    def lat_limits(self, lat_lim):
        self._lat_limits = lat_lim

    @lat_limits.getter
    def lat_limits(self):
        default_lat_lims = {'south': [-90, -50],
                            'north': [50, 90]}[self._pole]
        return getattr(self, '_lat_limits', default_lat_lims)

    def make_circular(self):
        """Make the plot boundary circular."""
        set_circular_boundary(self.geo_axes)


def set_circular_boundary(ax):
    """Compute a circle in axes coordinates, which we can use as a boundary for the map.
    We can pan/zoom as much as we like – the boundary will be permanently circular."""
    theta = np.linspace(0, 2*np.pi, 100)
    center, radius = [0.5, 0.5], 0.5
    vertices = np.vstack([np.sin(theta), np.cos(theta)]).T
    circle = mpath.Path(vertices*radius + center)
    ax.set_boundary(circle, transform=ax.transAxes)
    return

