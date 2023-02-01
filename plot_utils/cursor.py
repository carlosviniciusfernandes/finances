##############################################################################
# Snapping to data points
# """""""""""""""""""""""
# The following cursor snaps its position to the data points of a `.Line2D`
# object.
#
# To save unnecessary redraws, the index of the last indicated data point is
# saved in ``self._last_index``. A redraw is only triggered when the mouse
# moves far enough so that another data point must be selected. This reduces
# the lag due to many redraws. Of course, blitting could still be added on top
# for additional speedup.
#
# original source: https://matplotlib.org/stable/gallery/event_handling/cursor_demo.html

import numpy as np

from matplotlib.pyplot import Axes
from matplotlib.backend_bases import MouseEvent

from .plot_data import PlotData
class SnappingCursor:
    """
    A cross hair cursor that snaps to the data point of a line, which is
    closest to the *x* position of the cursor.

    For simplicity, this assumes that *x* values of the data are sorted.
    """
    default_text_settings = {'x': 0.8, 'y': 1.01, 's':'', 'color': 'k'}

    # def __init__(self, ax, line, params = {}):
    def __init__(self, ax:Axes , data: PlotData, params: dict = {}):
        self.ax = ax
        self.horizontal_line = ax.axhline(color='k', lw=0.8, ls='--')
        self.vertical_line = ax.axvline(color='k', lw=0.8, ls='--')
        self.data = data
        self._last_index = None
        self.text = ax.text(
            **{**self.default_text_settings, **params},
            transform=ax.transAxes
        )

    def set_cross_hair_visible(self, visible: bool) -> bool:
        need_redraw = self.horizontal_line.get_visible() != visible
        self.horizontal_line.set_visible(visible)
        self.vertical_line.set_visible(visible)
        self.text.set_visible(visible)
        return need_redraw

    def on_mouse_move(self, event: MouseEvent):
        if not event.inaxes:
            self._last_index = None
            need_redraw = self.set_cross_hair_visible(False)
            if need_redraw:
                self.ax.figure.canvas.draw()
        else:
            self.set_cross_hair_visible(True)
            x, y = event.xdata, event.ydata
            index = min(np.searchsorted(self.data.x, x), len(self.data.x) - 1)
            if index == self._last_index:
                return  # still on the same data point. Nothing to do.
            self._last_index = index
            x = self.data.x[index]
            y = self.data.y[index]
            # update the line positions
            self.horizontal_line.set_ydata(y)
            self.vertical_line.set_xdata(x)
            self.text.set_text(self.data.get_index_data(index))
            # self.text.set_text('x=%1.2f, y=%1.2f' % (x, y))
            self.ax.figure.canvas.draw()
