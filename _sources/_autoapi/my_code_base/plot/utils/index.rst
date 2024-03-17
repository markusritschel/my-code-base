:py:mod:`my_code_base.plot.utils`
=================================

.. py:module:: my_code_base.plot.utils


Module Contents
---------------

.. py:function:: align_curves(ax1, y1, ax2, y2)

   Align two axes based on two curves that share the same qualitative profile.

   :param ax1:
   :type ax1: matplotlib.Axes.axis
   :param y1:
   :type y1: np.ndarray
   :param ax2:
   :type ax2: matplotlib.Axes.axis
   :param y2:
   :type y2: np.ndarray

   .. rubric:: Example

   Create some dummy time series
   y1 and y2 will be on ax1
   y3 will be on the twinx axis of ax1 and share the qualitative profile of y1
   >>> pytest.skip()
   >>> x = np.linspace(0, 4*np.pi, 100)
   >>> y1 = np.sin(x) + 10
   >>> y2 = np.sin(x)*1.4 + .3*x + 9
   >>> y3 = 1.6*np.sin(x) + 3

   >>> fig, (ax1, ax2) = plt.subplots(1,2, figsize=(10,4))
   >>> ax1.plot(x, y1, lw=4, alpha=.7, zorder=-1, color='blue')
   >>> ax1.plot(x, y2, lw=1.5, color='steelblue')
   >>> ax1.tick_params(colors='b')

   >>> ax12 = ax1.twinx()
   >>> ax12.plot(x, y3, alpha=.7, marker='+', color='red', lw=1)
   >>> ax12.tick_params(colors='r')

   >>> ax2.plot(x, y1, lw=4, alpha=.7, zorder=-1, color='blue')
   >>> ax2.plot(x, y2, lw=1.5, color='steelblue')
   >>> ax2.tick_params(colors='b')

   >>> ax22 = ax2.twinx()
   >>> ax22.plot(x, y3, alpha=.7, marker='+', color='red', lw=1)
   >>> ax22.tick_params(colors='r')

   Align the limits such that the blue and the red curve match again

   >>> align_curves(ax2, y1, ax22, y3)


.. py:function:: center_xticklabels_between(ax)

   Center x-ticklabels at the middle of the month
   From https://matplotlib.org/3.5.0/gallery/ticks/centered_ticklabels.html


