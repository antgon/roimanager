from PyQt4.QtCore import (QString, Qt, QVariant, QModelIndex, SIGNAL)
from PyQt4.QtCore import (QAbstractListModel)
import h5py
import bisect
from matplotlib.patches import Polygon

class Roi(object):
    def __init__(self, xy, name, colour, linewidth=None):
        '''
        A ROI is defined by its vertices (xy coords), a name,
        and a colour.

        Input:

          xy       Coordinates of the ROI as a numpy array of
                   shape (2, N).
          name     Name of the ROI, string.
          colour   Colour definition in any format acceptable
                   to matplotlib, ie named (e.g. 'white') or
                   RGBA format (e,g. (1.0, 1.0, 1.0, 1.0)).
        '''
        super(Roi, self).__init__()
        self.polygon = Polygon(xy, lw=linewidth)
        self.polygon.set_facecolor('none')
        self.name = name
        self.set_colour(colour)

    def set_colour(self, colour):
        self.polygon.set_edgecolor(colour)

    def get_colour(self):
        return self.polygon.get_edgecolor()

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_xy(self):
        return self.polygon.set_xy()

    def get_xy(self):
        return self.polygon.get_xy()

    def get_polygon(self):
        return self.polygon

class RoiListModel(QAbstractListModel):
    def __init__(self):
        super(RoiListModel, self).__init__()
        # '_rois' will hold the list of all ROIs. Each
        # element in the list will in turn be a list
        # with two elements, the name (used for sorting)
        # and the roi itself.
        self._rois = []
        # A flag to keep track of unsaved changes.
        self.is_dirty = False

    def clear(self):
        while len(self._rois) > 0:
            roi = self._rois.pop()
            roi[1].polygon.remove()
        self._rois = []
        self.is_dirty = False
        #self.listRoi.clearSelection()

    def rowCount(self, index=QModelIndex):
        return len(self._rois)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or \
                not (0 <= index.row() < len(self._rois)):
                    return QVariant()
        name = self._rois[index.row()][0]
        if role==Qt.DisplayRole:
            return QVariant(name)
        return QVariant()

    def __iter__(self):
        for roi in self._rois:
            yield roi[1]

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return Qt.ItemFlags(QAbstractListModel.flags(self, index) |
                Qt.ItemIsEditable)

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and 0 <= index.row() < len(self._rois):
            # Do not allow blank names.
            if len(value.toString()) == 0: return False
            # Make sure new name is unique.
            name = self.get_unique_name(value.toString())
            roi_item = self._rois[index.row()]
            # Change name in ROI collection.
            roi_item[0] = name
            # Rename roi object.
            roi_item[1].set_name(name)
            # If ROIs are sorted, then that item has now to be 
            # the one selcted/highlighted.
            #self._rois = sorted(self._rois)
            #newrow = bisect.bisect_left(self._rois, [name])
            #self.emit(SIGNAL("dataChanged(QModelIndex, QModelIndex)"),
                    #index, self.index(newrow))
            self.is_dirty = True
            return True
        return False

    def removeRow(self, position, index=QModelIndex()):
        if len(self._rois) == 0: return False
        self.beginRemoveRows(QModelIndex(), position, position)
        roi = self._rois.pop(position)
        roi[1].polygon.remove()
        self.endRemoveRows()
        self.is_dirty = True
        return True

    def get_unique_name(self, name):
        '''
        Ensure that a ROI name is unique.
        
        If 'name' is already in use by a ROI, an underscore
        and a number are appended to that name to make it
        unique.
        '''
        # Names currently in use.
        names = [roi[0] for roi in self._rois]
        # If 'name' does not already exist return that name
        # and exit.
        if name not in names: return name
        # If it does exist, iterate until we create one which
        # does not exist.
        newname = name
        n = 1
        while newname in names:
            newname = '{}_{}'.format(name, n)
            n += 1
        return newname

    #def insertRows(self, position, row=1, index=QModelIndex()):
        #self.beginInsertRows(index, position, position+row-1)
        #self.endInsertRows()
        #self.emit(SIGNAL("rowsInserted(QModelIndex, int, int)"),\
                #index, position, position+row-1)
        #return True

    #def insertRow(self, position, index=QModelIndex()):
        #self.beginInsertRows(index, position, position)
        #self.endInsertRows()
        #self.emit(SIGNAL("rowInserted(QModelIndex, int)"),\
                #index, position)
        #return True

    def insertRow(self, roi):
        # New roi name should be unique.
        name = self.get_unique_name(roi.name)
        roi.set_name(name)
        # Add roi to list.
        position = self.rowCount()
        #position = bisect.bisect_left(self._rois, [name, roi])
        self.beginInsertRows(QModelIndex(), position, position)
        self._rois.insert(position, [name, roi])
        self.endInsertRows()
        index = self.index(position)
        self.emit(SIGNAL("rowInserted(QModelIndex, int)"),
                index, position)
        # Set flag.
        self.is_dirty = True
        #return True
        return roi

    def set_visible(self, b):
        if len(self._rois) > 0:
            [r[1].polygon.set_visible(b) for r in self._rois]

