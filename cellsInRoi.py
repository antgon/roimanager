
'''
Lots of hdf5 files in a directory.
Each has ROIs and coords for each cell in a brain section.
This script should read each hdf5 file in turn, extract info on 
cell number per region, put all together into one data frame,
then save.
'''

from __future__ import division
import numpy as np
import pandas as pd
import h5py
import os
#from matplotlib.pylab import plt
from matplotlib.nxutils import points_inside_poly
from allen_brain_atlas.allen_api import (Ontology)
#from allen_brain_atlas.allen_api import (read_structures,
#        Ontology)
import matplotlib.pyplot as plt

class DataFile:
    '''
    This is one hdf5 file with info from one brain section.

    Files have two groups: 'markers' and 'roiset'.

    'roiset' group has one subgroups for each ROI found in that
    brain section. The name of the dataset is the acronym for the
    brain region, and it willhave a dataset 'xy' which is are the
    vertices of the ROI.

    'markers' is a group with 3 datasets, each of which with one row
    per marker in the brain section:
        'c'    [string] colour name of the marker.
        'm'    [string] mpl marker character.
        'xy'   [integer] x, y coordinates of the marker.

    attributes of '/' include image size, resolution, name, atlas_ref.


    Thus, the object that will result from reading a hdf5 file will
    contain these atrtibutes:
        self.rois --> {dict}
        self.markers --> [array]
        self.(other attrs)
    '''
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
            for key, val in h5file.attrs.iteritems():
                self.__dict__[key] = val
        except IOError as error:
            print 'File {}: {}'.format(fname, error)
        finally:
            if h5file is not None: h5file.close()
        self.nrois = len(self.rois)
        self.nmarkers = len(self.markers)

    def plot(self):
        '''
        Plot all ROIs and markers. This function is intended mostly
        for debugging.
        '''
        # Trick to select colours from:
        # http://stackoverflow.com/questions/4805048/how-to-get-
        # different-colored-lines-for-different-plots-in-a-single-
        # figure/4805456#4805456
        cmap = plt.cm.gist_ncar
        #cmap = plt.cm.Set3
        ncolours = self.nrois
        colours = [cmap(i) for i in np.linspace(0, 0.9, ncolours)]
        for (i, roi) in enumerate(self.rois.itervalues()):
            x, y = roi.T
            plt.plot(x, y, c=colours[i])
        x, y = self.markers.T
        plt.plot(x, y, 'o')
        plt.show()

    def get_markers_per_structure(self):
        ontology = Ontology()
        sorted_markers = pd.DataFrame(index=np.arange(self.nmarkers))
        for roi_name, roi_xy in self.rois.iteritems():
            sorted_markers[roi_name] = points_inside_poly(\
                    self.markers, roi_xy)

        # Raise an error if a marker is not assigned to at least one
        # ROI.
        if not np.all(sorted_markers.sum(axis=1) > 0):
            raise ValueError,\
                    "There are markers with no ROI assigned ({})".\
                    format(os.path.split(self.fname)[-1])

        # Remove from analysis those structures without markers.
        sorted_markers = sorted_markers[\
                sorted_markers.columns[sorted_markers.sum(0)>0]]

        # Verify that all structure names in the set do exist as
        # acronyms in the ontology.
        structs = [ontology(name) for name in sorted_markers.columns.values]
        if None in structs:
            indices = np.where(structs)
            iswrong = np.ones(sorted_markers.columns.size, bool)
            iswrong[indices] = False
            iswrong = sorted_markers.columns.values[iswrong]
            raise ValueError,\
                    'Non-existent acronym(s) {} in file {}'\
                    .format(iswrong, self.fname)

        # Some markers may fall inside more than one structure. In
        # those cases the sum per row (i.e. sum of True values per
        # marker) will be more than one: sorted_mrk[sorted_mrk.sum(1)
        # > 1]. We must decide which structure to assign the marker to
        # on a case-by-case basis. Each series in the following
        # iteration is a marker with boolean values of the structure it
        # falls into.
        for indx, ser in sorted_markers[sorted_markers.sum(1) > 1].\
                iterrows():
            # Use only the True values in the series.
            ser = ser[ser]
            # Create a list of structures that all contain the same
            # marker.
            isin = [ontology[key] for key in ser.keys()]
            # 'None' will be returned from ontology if the key is not
            # in it, ie if the acronym does not exist in the ontology
            # database (as would happen when typing wrong
            # capitalisation, not naming roi, etc).
            if None in isin:
                raise ValueError,\
                        'Non-existent acronym {} in file {}'.\
                        format(ser.index.values, self.fname)
            # I have not decided how to deal with cases where the
            # marker falls inside more that 2 structures.
            assert len(isin) == 2,\
                    "One marker in more than one structure {}".\
                    format(isin)
            # Sort list of structures. The order will increase as each
            # structure becomes deeper in the ontology tree, so that we
            # expect the last structure in the list to be within the
            # first one.
            isin.sort()
            assert isin[-1] in isin[0],\
                    'Structure {} is not part of structure {}'.\
                    format(isin[-1], isin[0])
            # If the above assumptions are true (ie that, compared to
            # the first structure, the second structure in the list is
            # deeper in the ontology and it is its subset), then we
            # can set the membership of the marker to the topmost
            # structure to false. That is, the marker is assigned to
            # the deeper structure of the two.
            sorted_markers.loc[indx][isin[0].acronym] = False

        # Confirm that now each marker belongs to only one structure.
        assert np.all(sorted_markers.sum(axis=1) == 1)

        # Finally, quantify and return the number of markers per
        # structure.
        return sorted_markers.sum(axis=0)

fname = "/home/antgon/projects/MCH-inputs/MCH-tracing/A20/tif/20-0224.hdf5"
f = DataFile(fname)

