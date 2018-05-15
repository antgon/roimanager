
==========
roimanager
==========

Facilitates counting cells in micrographs from brain tissue and sorting
them into different anatomical regions of interest (ROIs).

This package displays an imageJ tiff image and provides tools to
navigate the image, draw and name ROIs, and mark cells. The ROIs and
markers are saved into individual hdf5 files. At a later stage these
files can be read and the counted cells are sorted into their respective
ROIs.

The package was originally developed to count projection neurones in
sections of mouse brain, and sort those cells into anatomical regions;
see:

González *et al* (2016). Awake dynamics and brain-wide direct inputs of
hypothalamic MCH and orexin networks. *Nature Communications* 7:11395
(DOI: 10.1038/ncomms11395).

(C) 2015-2018 [Antonio González](mailto:antgon@cantab.net)

Links
=====

* The code is licensed under the `GNU General Public License`_.
* The `source code`_ is in GitHub.

.. _`GNU General Public License`: http://www.gnu.org/licenses/gpl.html
.. _`source code`: https://github.com/antgon/roimanager
