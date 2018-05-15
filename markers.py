#! /usr/bin/env python3
# coding=utf-8
#
# Copyright (c) 2015-2018 Antonio González
#
# This file is part of roimanager.
#
# Roimanager is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# Roimanager is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with roimanager. If not, see <http://www.gnu.org/licenses/>.

import numpy as np


class MarkerManager(object):
    MARKERFACECOLOUR = 'yellow'
    MARKEREDGECOLOUR = 'black'
    MARKEREDGEWIDTH = 1.5
    MARKERSIZE = 4.5
    MARKER = 'o'

    def __init__(self, parent):
        self.ax = parent.ax
        self.canvas = parent.canvas
        self.is_dirty = False

    def connect_add(self):
        self.cid = self.canvas.mpl_connect('button_press_event',
                                           self.on_add)

    def disconnect(self):
        if hasattr(self, 'cid'):
            self.canvas.mpl_disconnect(self.cid)

    def on_add(self, event):
        if self.canvas.widgetlock.locked():
            return
        if event.inaxes is None:
            return
        x, y = event.xdata, event.ydata
        self.add(x, y)
        self.canvas.draw()

    def clear(self):
        self.ax.lines = []
        self.is_dirty = False

    def add(self, x, y, marker=MARKER, mec=MARKEREDGECOLOUR,
            mfc=MARKERFACECOLOUR, picker=5, ms=MARKERSIZE,
            mew=MARKEREDGEWIDTH):
        self.ax.plot([x], [y], marker=marker, mec=mec, mfc=mfc,
                     picker=picker, ms=ms, mew=mew)
        self.is_dirty = True

    def connect_remove(self):
        self.disconnect()
        self.cid = self.canvas.mpl_connect('pick_event', self.on_remove)

    def on_remove(self, event):
        if self.canvas.widgetlock.locked():
            return
        event.artist.remove()
        self.canvas.draw()
        self.is_dirty = True

    def get_xy(self):
        # There is no point in keeping data as floats since image
        # pixels are integers. Thus, round and convert to integers
        # to match to image coordinates.
        xy = [l.get_xydata().flatten() for l in self.ax.lines]
        xy = np.array(xy)
        xy = xy.round().astype(int)
        return xy

    def get_markers(self):
        markers = [l.get_marker() for l in self.ax.lines]
        # h5py requires ascii, not Unicode. Converting to an array of
        # type "S" avoids TypeErrors in h5py.
        markers = np.array(markers, dtype="S")
        return markers

    def get_colours(self):
        colours = [l.get_mfc() for l in self.ax.lines]
        # h5py requires ascii, not Unicode. Converting to an array of
        # type "S" avoids TypeErrors in h5py.
        colours = np.array(colours, dtype="S")
        return colours

    def get_labels(self):
        labels = [l.get_label() for l in self.ax.lines]
        return labels


class MarkerSet(object):
    '''
    A class to manage a group of markers with common attributes.
    '''
    def __init__(self, name):
        self.name = name
        self.colour = 'colour'
        self.xy = []
        self.marker = 'o'
        self.label = ''

    def append(self, x, y):
        self.xy.append([x, y])

    def size(self):
        return self.xy.size
