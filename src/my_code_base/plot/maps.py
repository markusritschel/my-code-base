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
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import numpy as np
import pytest
from .z_overlap import fix_overlap

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
        log.debug('Initialize accessor')
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
        log.debug('Add ocean to axis')
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
        log.debug('Add land to axis')
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
        log.debug('Add coastlines to axis')
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
        log.debug('Set axis extent to %s', extent)
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
        self._lat_limits = None
        self._lon_grid_spacing = 30
        self._draw_labels = True  # or should this rather be an attribute of self.geo_axes._draw_labels ?

    @property
    def lat_limits(self):
        """Get and set the latitude limits for the plot."""
        if self._lat_limits is None:
            self._lat_limits = {'south': [-90, -50],
                            'north': [50, 90]}[self._pole]
        return self._lat_limits

    @lat_limits.setter
    def lat_limits(self, lat_lim):
        self._lat_limits = lat_lim

    # @lat_limits.getter
    # def lat_limits(self):
    #     default_lat_lims = {'south': [-90, -50],
    #                         'north': [50, 90]}[self._pole]
    #     return getattr(self, '_lat_limits', default_lat_lims)

    def make_circular(self):
        """Make the plot boundary circular."""
        set_circular_boundary(self.geo_axes)

    def add_ruler(self, **kwargs):
        """Add a circular ruler to the plot.
        
        See :func:`add_circular_ruler` for customization arguments.
        The `ax` argument is not needed to be handed over when using the accessor's method.

        Args:
            kwargs: Additional keyword arguments for customization.
        """
        kwargs.setdefault('segment_length', self._lon_grid_spacing)
        add_circular_ruler(self.geo_axes, **kwargs)

    def add_gridlines(self, **kwargs):
        """
        Add gridlines to the plot.

        Parameters
        ----------
        **kwargs : dict
            Additional keyword arguments for customization.

        Returns
        -------
        cartopy.mpl.gridliner.Gridliner
            The gridliner object.

        Notes
        -----
        This method adds gridlines to the plot using the specified keyword arguments for customization.
        The default values for the keyword arguments are:
        - 'zorder': 1
        - 'linestyle': '-'
        - 'linewidth': 0.5
        - 'color': 'gray'
        - 'alpha': 0.7

        The gridlines are added based on the latitude limits of the plot.
        The latitude grid spacing is set to 10 degrees.
        The longitude grid spacing is determined by the latitude grid spacing and the x_spacing_factor.
        The gridlines are created using the `gridlines` method of the `geo_axes` object.
        The `draw_labels` argument is set to True for the first set of gridlines and False for the second set.
        """
        kwargs.setdefault('zorder', 1)
        kwargs.setdefault('linestyle', '-')
        kwargs.setdefault('linewidth', 0.5)
        kwargs.setdefault('color', 'gray')
        kwargs.setdefault('alpha', 0.7)

        lat0, lat1 = self.lat_limits
        lat_grid_spacing = 10
        ygrid_locs = np.arange(lat0, lat1 + 1, lat_grid_spacing)
        fac1, fac2 = {'north': [1, 2],
                      'south': [2, 1]}[self._pole]

        def draw_gridlines(x_spacing_factor, ylim):
            return self.geo_axes.gridlines(
                xlocs=np.arange(-180, 180, x_spacing_factor * self._lon_grid_spacing),
                ylim=ylim,
                ylocs=ygrid_locs,
                draw_labels=self._draw_labels if x_spacing_factor == 1 else False,
                **kwargs
            )

        lat_breakpoint = {'south': -80,
                          'north': +80}[self._pole]

        gl1 = draw_gridlines(fac1, [lat0, lat_breakpoint])
        gl2 = draw_gridlines(fac2, [lat_breakpoint, lat1])

        self._gl = {'north': gl1, 'south': gl2}[self._pole]

        return self._gl

    def add_features(self, gridlines=True, ruler=True, **kwargs):
        """Apply various features to the plot.

        Parameters
        ----------
        gridlines : bool, optional
            Whether to add gridlines. Defaults to True.
        ruler : bool, optional
            Whether to add a ruler. Defaults to True.
        **kwargs
            Additional keyword arguments for customization.

        Returns
        -------
        None

        Notes
        -----
        This method applies the following features to the plot:
        - add ocean
        - add land
        - add coastlines
        - add ruler
        - make the boundary circular
        - add gridlines


        :glue:`/examples/stereographic_maps.ipynb::polar_plot_features`
        """
        coastlines_kwargs = kwargs.pop('coastlines_kwargs', {})
        gridlines_kwargs = kwargs.pop('gridlines_kwargs', {})
        land_kwargs = kwargs.pop('land_kwargs', {})
        ocean_kwargs = kwargs.pop('ocean_kwargs', {})
        ruler_kwargs = kwargs.pop('ruler_kwargs', {})
        self._lon_grid_spacing = ruler_kwargs.get('segment_length', 30)

        self.set_extent([-180, 180, *self.lat_limits])
        self.add_ocean(**ocean_kwargs)
        self.add_land(**land_kwargs)
        self.add_coastlines(**coastlines_kwargs)
        self.make_circular()
        if ruler:
            self.add_ruler(**ruler_kwargs)
        if gridlines:
            gl = self.add_gridlines(**gridlines_kwargs)
            self.rotate_lat_labels(target_lon=118)
            self.rotate_lon_labels()
        
        return

    def rotate_lat_labels(self, target_lon=118, orig_lon=150):
        """Move the latitude labels to another longitude.

        Parameters
        ----------
        target_lon : int
            The longitude to which the labels should be moved.
        orig_lon : int
            The longitude at which the labels are located per default [default: 150].

        Source: https://stackoverflow.com/a/66587492/5925453 with minor adaptions.
        """
        plt.draw()
        for tx in self._gl.label_artists:
            xy = tx.get_position()
            if xy[0]==orig_lon:
                tx.set_position([target_lon, xy[1]])
                tx.set_size('small')
        return

    def rotate_lon_labels(self):
        """
        Rotate the longitude labels of a stereographic plot for better readability and nicer look.
        """
        self._gl.rotate_labels = False
        plt.gcf().canvas.draw()

        all_label_artists = [label for label in self._gl.label_artists if label.get_text()[-1] 
                            in ['E', 'W', '°']]
        for label in all_label_artists:
            alphanumeric_label = label.get_text()
            longitude = _str2float(alphanumeric_label)
            rot_degree = _lon2rot(longitude, self._pole)
            _rotate_and_align_label(label, longitude, rot_degree, pole=self._pole)
        return


def add_circular_ruler(ax, segment_length=30, offset=0, primary_color='k', secondary_color='w', width=1):
    """Add a ruler around a polar stereographic plot.

    Parameters
    ----------
    ax : GeoAxes
        The GeoAxes object to which the ruler should be added
    segment_length : int
        The length of each segment in degrees
    offset : int
        An optional offset
    primary_color : str
        The color of the background ruler segments
    secondary_color : str
        The color of the top ruler segments
    width : float
        The scaled thickness of the ruler. Defaults to 1/80 of the axes' width.
    """
    def plot_circle(degrees, radius=0.5, **kwargs):
        """Plot a circle of given radius (based on Axis dimensions) 
        for a list of degree segments."""
        ax = kwargs.pop("ax", plt.gca())
        arc_angles = np.deg2rad(degrees)
        arc_xs = radius * np.cos(arc_angles) + 0.5
        arc_ys = radius * np.sin(arc_angles) + 0.5
        ax.plot(arc_xs, arc_ys, transform=ax.transAxes, solid_capstyle="butt", **kwargs)

    width = ax.bbox.width / 100 * width

    if (360 / segment_length) % 2 != 0:
        raise Warning(
            "`segment_length` must fit 2n times into 360 so that the segments of the "
            "ruler can be equally distributed on a circle."
        )

    # plot background circle (default: black, slightly broader)
    segments_array = np.linspace(0, 360, 361, endpoint=True)
    plot_circle(segments_array, color=primary_color, lw=width * 2 + 1, zorder=999, ax=ax)

    # plot white circle segments on top
    segment_bnds_array = (
        np.arange(0, 360, segment_length).reshape((-1, 2))
        + 90  # to start at the top instead of at the right
        + offset
    )
    segments_array = np.hstack(
        [
            np.hstack([np.linspace(*bnds, segment_length, endpoint=True), np.array(np.nan)])
            for bnds in segment_bnds_array
        ]
    )
    plot_circle(segments_array, color=secondary_color, lw=width * 2, zorder=1000, ax=ax)


def _str2float(label):
    """Turn geographic longitude grid labels into numeric values of degrees east."""
    # Extract the numbers from the label
    number = label.split('°')[0]
    number = float(number)
    # Turn longitudes west of the meridian into negative numbers
    if 'W' in label:
        number = -number
    return number


def _lon2rot(lon, pole):
    """Turn longitude value into rotation for polar stereographic plots."""
    rot_rad = lon
    if abs(lon) >= 90:
        rot_rad = lon - 180

    if pole == 'south':
        rot_rad = 0 - rot_rad
        if np.abs(lon) == 90:
            rot_rad -= 180

    return rot_rad


def _rotate_and_align_label(label, longitude, rot_degree, pole):
    """Rotate and align longitude labels."""
    label.set_rotation_mode('anchor')  # rotation_mode='anchor' aligns the unrotated text first and then rotates the text around the point of alignment.
    label.set_rotation(rot_degree)
    label.set_size('small')
    label.set_horizontalalignment('center')

    if pole=='north':
        alignment = 'top' if abs(longitude) < 90 else 'bottom'
    elif pole == 'south':
        alignment = 'top' if abs(longitude) > 90 else 'bottom'
    label.set_verticalalignment(alignment)

    return label


def set_circular_boundary(ax):
    """Compute a circle in axes coordinates, which we can use as a boundary for the map.
    We can pan/zoom as much as we like – the boundary will be permanently circular."""
    theta = np.linspace(0, 2*np.pi, 100)
    center, radius = [0.5, 0.5], 0.5
    vertices = np.vstack([np.sin(theta), np.cos(theta)]).T
    circle = mpath.Path(vertices*radius + center)
    ax.set_boundary(circle, transform=ax.transAxes)
    return

