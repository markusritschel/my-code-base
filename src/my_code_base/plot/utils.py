# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Author: Markus Ritschel
# eMail:  git@markusritschel.de
# Date:   2024-03-04
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
import logging
from mpl_axes_aligner import align
import pytest


log = logging.getLogger(__name__)


def align_curves(ax1, y1, ax2, y2):
    """Align two axes based on two curves that share the same qualitative profile.

    Parameters
    ----------
    ax1 : matplotlib.axes.Axes.axis
        The first of two axis to be aligned
    y1 : numpy.ndarray
        The line on the first axis which will be used for alignment
    ax2 : matplotlib.axes.Axes.axis
        The second of two axis to be aligned
    y2 : numpy.ndarray
        The line on the second axis which will be used for alignment

    Example
    -------
    Create some dummy time series.
    `y1` and `y2` will be on `ax1`,
    `y3` will be on the twinx axis of `ax1` and share the qualitative profile of `y1`.
    
    >>> pytest.skip()
    >>> x = np.linspace(0, 4*np.pi, 100)
    >>> y1 = np.sin(x) + 10
    >>> y2 = np.sin(x)*1.4 + .3*x + 9
    >>> y3 = 1.6*np.sin(x) + 3
    >>> 
    >>> fig, (ax1, ax2) = plt.subplots(1,2, figsize=(10,4))
    >>> ax1.plot(x, y1, lw=4, alpha=.7, zorder=-1, color='blue')
    >>> ax1.plot(x, y2, lw=1.5, color='steelblue')
    >>> ax1.tick_params(colors='b')
    >>> 
    >>> ax12 = ax1.twinx()
    >>> ax12.plot(x, y3, alpha=.7, marker='+', color='red', lw=1)
    >>> ax12.tick_params(colors='r')
    >>>
    >>> ax2.plot(x, y1, lw=4, alpha=.7, zorder=-1, color='blue')
    >>> ax2.plot(x, y2, lw=1.5, color='steelblue')
    >>> ax2.tick_params(colors='b')
    >>>
    >>> ax22 = ax2.twinx()
    >>> ax22.plot(x, y3, alpha=.7, marker='+', color='red', lw=1)
    >>> ax22.tick_params(colors='r')

    Align the limits such that the blue and the red curve match again

    >>> align_curves(ax2, y1, ax22, y3)

    """
    ax1_ylim_lower, ax1_ylim_upper = ax1.get_ylim()
    ax1_extent = ax1_ylim_upper - ax1_ylim_lower
    y1_amplitude = y1.max() - y1.min()
    y1_relative_amplitude = y1_amplitude/ax1_extent

    ax1_min_offset = y1.min() - ax1_ylim_lower
    ax1_min_relative_offset = ax1_min_offset/ax1_extent

    ax2_ylim_lower, ax2_ylim_upper = ax2.get_ylim()
    y2_amplitude = y2.max() - y2.min()
    ax2_extent = ax2_ylim_upper - ax2_ylim_lower

    ax2_new_ylim_lower = y2.min() - ax1_min_relative_offset*ax2_extent
    ax2_new_ylim_upper = ax2_new_ylim_lower + y2_amplitude/y1_relative_amplitude
    ax2.set_ylim(ax2_new_ylim_lower, ax2_new_ylim_upper)

    align.yaxes(ax1, y1.mean(), ax2, y2.mean())

    return
