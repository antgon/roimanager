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
from tifffile import TiffFile
from matplotlib.colors import LinearSegmentedColormap, ListedColormap


def std_cmap(colour):
    '''
    Standard LUTs in fluorescence microscopy use just one colour and
    set the background in black.
    '''
    if colour in ['green', 'g']:
        return LinearSegmentedColormap.from_list(
                'green', ['black', 'green'])
    elif colour in ['blue', 'b']:
        return LinearSegmentedColormap.from_list(
                'blue', ['black', 'blue'])
    elif colour in ['red', 'r']:
        return LinearSegmentedColormap.from_list(
                'red', ['black', 'red'])
    elif colour in ['magenta', 'm']:
        return LinearSegmentedColormap.from_list(
                'magenta', ['black', 'magenta'])
    elif colour in ['cyan', 'c']:
        return LinearSegmentedColormap.from_list(
                'cyan', ['black', 'cyan'])
    else:
        # If no colour is defined here, returning None will set the
        # default colormap in imshow.
        return None


def lut_to_cmap(lut):
    '''
    Converts an ImageJ LUT into a matplotlib colormap.

    LUTs (as read from an ImageJ tiff tag) are of size = 768, which is
    256 * 3, ie they code values of red, green and blue in a 0-255
    scale for each channel.

    Input:
        lut    An (uint8) array of length 768. This array is a sequence
               of 8-bit RGB values (thus size is 256*3 = 768).

    Returns:
        A matplotlib colormap.
    '''
    # LUT input is in range 0-255 but matplotlib's RGB range should
    # be 0-1.
    rgb = lut/255.
    # Reshape to sort RGB channels.
    rgb = rgb.reshape(3, -1).T
    # Return as a matplotlib colormap.
    return ListedColormap(rgb)


class Channel:
    def __init__(self, n, yx, cmap, rnge):
        self.yx = yx
        self.cmap = cmap
        self.shape = yx.shape
        self.range = rnge
        self.n = n


class IJTiff(object):
    '''
    -----------
    ImageJ tiff
    -----------

    Reads tiff images created with ImageJ. LUTs are read from
    the file's tiff tags and converted into Matplotlib's
    colormaps.


    Example:
    -------

      > tif = Tiff(fname)
      > for channel in tif:
      >     im = plt.imshow(channel.im, cmap=channel.cm)
      >     im.set_clim(channel.range)


    Colormaps:
    ---------

    There are two ways of setting up a colormap for ImageJ tiffs.

    1) Define an arbitrary colormap. To create a typical, one-colour
       LUT as used in ImageJ use
       matplotlib.colors.LinearSegmentedColormap, see function
       'lut_to_cm'.

    2) Read LUTs from the tiff tags and convert them into mpl
       colormaps. This is achieved with
       matplotlib.colors.ListedColormap, see function 'std_cm' above.

    '''
    def __init__(self, fname):
        tif = TiffFile(fname)
        # This class is only for ImageJ tiffs.
        assert tif.is_imagej is True

        # 'axes' defines the data arrangement in the image array, e.g.
        # 'ZCYX' for mutliple-stacks, mulitple-channels images,
        # 'CYX' for multiple-channels, single stack images, etc.
        axes = tif.series[0].axes

        # Images with z-stacks are not yet supported.
        if 'Z' in axes:
            raise NotImplementedError("Z-stacks are not supported")

        # Shape of file will only reflect (x, y) dimensions. Number
        # of channels is stored elsewhere.
        x_indx = axes.find('X')
        y_indx = axes.find('Y')
        shape = tif.series[0].shape
        self.shape = (shape[y_indx], shape[x_indx])

        # Read tags and extract relevant information.
        self.fname = tif.filename
        self.fpath = tif.filehandle.path
        self.nchannels = tif.imagej_metadata['channels']
        # If the image contains its own luts, use them. (Is this the
        # case with all images where 'mode' is 'composite'?)
        if 'luts'in tif.imagej_metadata:
            luts = tif.imagej_metadata['luts']
            cmaps = [lut_to_cmap(lut) for lut in luts]
        # If there are no luts, use a standard colours for each
        # channel. (Is this the case with all images
        # tif.imagej_metadata['mode'] == 'color'?)
        else:
            colours = ('b', 'g', 'r', 'm', 'c')[:self.nchannels]
            cmaps = [std_cmap(colour) for colour in colours]
        ranges = tif.imagej_metadata['Ranges']
        ranges = np.array(ranges).reshape(self.nchannels, -1)

        # Read image data.
        im = tif.asarray()
        # Single-channel images.
        if im.ndim == 2:
            self.__dict__['chan1'] = Channel(1, im, cmaps, ranges)
        # Multi-channel images.
        elif im.ndim == 3:
            for n in range(self.nchannels):
                # Multi-channel images are of type 'CYX' (first
                # dimension of the data array is 'channel'), where each
                # channel is in its own tiff page, or of type 'YXS'
                # (third dimension is 'sample per pixel', in practice
                # equivalent to channel), where all channels are
                # contained in the same tiff page and the page's
                # 'samples_per_pixel' is > 1.
                if axes == 'YXS':
                    yx = im[:, :, n]
                elif axes == 'CYX':
                    yx = im[n, :, :]
                # Create the channel. A unit is added to the channel
                # number's name to keep in line with the way channels
                # are displayed/named in ImageJ (i.e first channel is
                # number one, not 0.
                self.__dict__['chan%i' % (n+1)] = Channel(
                        n+1, yx, cmaps[n], ranges[n])
        else:
            raise NotImplementedError("Images with more than " +
                                      "3 dimensions are not supported.")

        # A 'tags' dictionary will hold relevant data.
        self.tags = {
                'image_name': tif.filename,
                'image_width': tif.pages[0].imagewidth,
                'image_length': tif.pages[0].imagelength,
                'unit': tif.imagej_metadata['unit'],
                'x_resolution': tif.pages[0].tags['XResolution'].value,
                'y_resolution': tif.pages[0].tags['YResolution'].value
                }

    def __iter__(self):
        keys = list(self.__dict__.keys())
        keys.sort()
        for key in keys:
            if key.startswith('chan'):
                yield self.__dict__[key]
