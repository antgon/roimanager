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

"""Summarise cell counts from a roimanager hdf5 file.

After counting cells with roimanager and creating a hdf5 file, this
module can be used to read the file and sort cells into ROIs.

Each hdf5 file created with roimanager has the paths of the ROIs
identified and the coordinates of each cell in a brain section. The
class RoiFile in this module load such a hdf5 file and allows to
extract the number of cells per region (ROI), put it all together into
one data frame, and save the data.

Example
-------

>>> fname = "demodata/20-0224.hdf5"
>>> f = RoiFile(fname)
>>> f.get_markers_per_structure()
ACB    1
ORB    2
PIR    1
dtype: int64
"""

import os
import h5py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.path import Path
from allen_brain_atlas.allen_api import (Ontology)


class RoiFile:
    """Encapsulates a hdf5 file created with roimanager.

    A hdf5 file from roimanager contains information from one brain
    section about cell counts, their location, and ROIs created. The
    file has two groups: 'markers' and 'roiset'.

    'roiset' group has one subgroup for each ROI found in that
    brain section. The name of the dataset is the acronym for the
    brain region, and it willhave a dataset 'xy' which is are the
    vertices of the ROI.

    'markers' is a group with 3 datasets, each row corresponds to a
    marker (i.e. a cell) in the brain section:
        'c'    [string] colour name of the marker.
        'm'    [string] mpl marker character.
        'xy'   [integer] x, y coordinates of the marker.

    attributes of '/' include image size, resolution, name, atlas_ref.


    Thus, the object that will result from reading a hdf5 file with
    this class will contain these atrtibutes:
        rois    <dict> key is ROI name, value is array of polygon
        markers <array> x, y coordinates for each marker
        (other attrs)
    """

    def __init__(self, fname):
        assert os.path.splitext(fname)[-1] == '.hdf5'
        self.fname = fname
        h5file = None
        try:
            h5file = h5py.File(fname, 'r')
            self.rois = {}
            for roiName in h5file['roiset']:
                xy = h5file['roiset/'+roiName+'/xy']
                self.rois[roiName] = xy[...]
            self.markers = h5file['markers/xy'][...]
            for key, val in h5file.attrs.items():
                self.__dict__[key] = val
            self.nrois = len(self.rois)
            self.nmarkers = len(self.markers)
        except (IOError, OSError) as error:
            print('File {}: {}'.format(fname, error))
        finally:
            if h5file is not None:
                h5file.close()

    def plot(self):
        """Plot all ROIs and markers.

        Uses matplotlib to display a graph of the ROIs and markers
        in the roi hdf5 file. This function is intended mostly for
        debugging and as a quick visual check of the file contents.
        """
        # Trick to select colours from:
        # http://stackoverflow.com/questions/4805048/how-to-get-
        # different-colored-lines-for-different-plots-in-a-single-
        # figure/4805456#4805456
        cmap = plt.cm.gist_ncar
        ncolours = self.nrois
        colours = [cmap(i) for i in np.linspace(0, 0.9, ncolours)]

        # Plot ROIs.
        ax = plt.figure().add_subplot(111)
        for (i, roi) in enumerate(self.rois.values()):
            x, y = roi.T
            ax.plot(x, y, c=colours[i])

        # Plot markers.
        x, y = self.markers.T
        ax.plot(x, y, 'o')

        # Invert y-axis so that origin is on top (as with images), set
        # equal aspect, remove ticks. Add a title.
        ax.set_ylim(ax.get_ylim()[::-1])
        ax.set_aspect("equal")
        ax.tick_params(bottom=False, labelbottom=False,
                       labelleft=False, left=False)
        ax.set_title(self.fname)
        plt.show()

    def get_markers_per_structure(self):
        """Sort markers into ROIs.

        The markers in the hdf5 file will be sorted into each identified
        ROI and a table with counts per ROI is returned.

        Returns
        -------
        pandas.Series
            A pandas table with ROI name and cell counts
        """
        ontology = Ontology()
        sorted_markers = pd.DataFrame(index=np.arange(self.nmarkers))
        for roi_name, roi_xy in self.rois.items():
            path = Path(roi_xy)
            sorted_markers[roi_name] = path.contains_points(
                    self.markers)

        # Raise an error if a marker is not assigned to at least one
        # ROI.
        if not np.all(sorted_markers.sum(axis=1) > 0):
            msg = "There are markers with no ROI ({})".format(
                    os.path.split(self.fname)[-1])
            raise ValueError(msg)

        # Remove the structures without markers from analysis.
        sorted_markers = sorted_markers[
                sorted_markers.columns[sorted_markers.sum(0) > 0]]

        # Verify that all structure names in the set do exist as
        # acronyms in the Allen ontology.
        structs = [ontology(name) for name in
                   sorted_markers.columns.values]
        if None in structs:
            indices = np.where(structs)
            iswrong = np.ones(sorted_markers.columns.size, bool)
            iswrong[indices] = False
            iswrong = sorted_markers.columns.values[iswrong]
            msg = '{}: invalid acronym(s) {}'.format(
                        self.fname, iswrong)
            self.ISW = iswrong
            raise ValueError(msg)

        # Some markers may fall inside more than one structure. In
        # those cases the sum per row (i.e. sum of True values per
        # marker) will be more than one: sorted_mrk[sorted_mrk.sum(1)
        # > 1]. We must decide which structure to assign the marker to
        # on a case-by-case basis. Each series in the following
        # iteration is a marker with boolean values of the structure it
        # falls into.
        is_repeated = sorted_markers.sum(1) > 1
        for indx, ser in sorted_markers[is_repeated].iterrows():
            # Use only the True values in the series.
            ser = ser[ser]

            # Create a list of structures that all contain the same
            # marker.
            isin = [ontology[key] for key in list(ser.keys())]

            # 'None' will be returned from ontology if the key is not
            # in it, ie if the acronym does not exist in the ontology
            # database (as would happen when typing wrong
            # capitalisation, not naming roi, etc).
            if None in isin:
                msg = 'File {}: {} is not a valid acronym'.format(
                        self.fname, ser.index.values)
                raise ValueError(msg)

            # I have not decided how to deal with cases where the
            # marker falls inside more that 2 structures.
            msg = 'One marker in more than one structure {}'.format(
               isin)
            assert len(isin) == 2, msg

            # Sort list of structures. The order will increase with
            # depth in the ontology tree, so we expect the last
            # structure in the list to be within the first one.
            isin.sort()
            if isin[-1] not in isin[0]:
                msg = 'Structure {} is not part of structure {}'.format(
                        isin[-1], isin[0])
                raise ValueError(msg)

            # If the above assumptions are true (ie that, compared to
            # the first structure, the second structure in the list is
            # deeper in the ontology and it is its subset), then we can
            # set the membership of the marker to the topmost structure
            # to false. That is, of the two structures, the marker is
            # assigned to the deeper one.
            sorted_markers.loc[indx][isin[0].acronym] = False

        # Confirm that now each marker belongs to only one structure.
        assert np.all(sorted_markers.sum(axis=1) == 1)

        # Finally, quantify and return the number of markers per
        # structure.
        return sorted_markers.sum(axis=0)


if __name__ == '__main__':
    fname = "demodata/219-0418.hdf5"
    # fname = 'demodata/22-0618.hdf5'
    f = RoiFile(fname)
    f.plot()
    print(f.get_markers_per_structure())
