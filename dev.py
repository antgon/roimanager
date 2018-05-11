'''
Sort cells into ROIs
'''


import numpy as np
import pandas as pd
import h5py
import os
from matplotlib.pylab import plt
from matplotlib.nxutils import points_inside_poly
from allen_brain_atlas.allen_api import (read_structures,
        Ontology)


def from_file(fname):
    assert os.path.splitext(fname)[-1] == '.hdf5'
    f = None
    try:
        f = h5py.File(fname, 'r')
        rois, attrs = {}, {}
        for name in f['roiset']:
            xy = f['roiset/'+name+'/xy']
            colour = xy.attrs['colour']
            rois[name] = xy[...]
        markers = f['markers/xy'][...]
        for key, val in f.attrs.items():
            attrs[key] = val
        return markers, rois, attrs
    except IOError as error:
        print('File {}: {}'.format(fname, error))
        return
    finally:
        if f is not None: f.close()

def markers_per_struct(markers, rois, ontology):
    sorted_mrk = pd.DataFrame(index=np.arange(len(markers)))
    for name, xy in rois.items():
        sorted_mrk[name] = points_inside_poly(markers, xy)
    # If a marker is not assigned to at least one ROI, raise a warning.
    assert np.all(sorted_mrk.sum(axis=1) > 0),\
            "Some markers are not designated to any structure".\
            format(os.path.split(fname)[-1])
    # Remove from analysis those structures without markers.
    sorted_mrk = sorted_mrk[sorted_mrk.columns[sorted_mrk.sum(0)>0]]
    # Verify that all structure names in the set do exist as acronyms
    # in the ontology.
    structs = [ontology(name) for name in sorted_mrk.columns.values]
    if None in structs:
        indices = np.where(structs)
        iswrong = np.ones(sorted_mrk.columns.size, bool)
        iswrong[indices] = False
        iswrong = sorted_mrk.columns.values[iswrong]
        raise ValueError('Non-existent acronym(s) {} in file {}'\
                .format(iswrong, fname))
    # Some markers may fall inside more than one structure. In those
    # cases the sum per row (i.e. sum of True values per marker) will
    # be more than one: sorted_mrk[sorted_mrk.sum(1) > 1]. We must
    # decide which structure to assign the marker to on a case-by-case
    # basis. Each series in the following iteration is a marker with
    # boolean values of the structure it falls into.
    for indx, ser in sorted_mrk[sorted_mrk.sum(1) > 1].iterrows():
        # Use only the True values in the series.
        ser = ser[ser]
        # Create a list of structures that all contain the same marker.
        isin = [ontology[key] for key in list(ser.keys())]
        # 'None' will be returned from ontology if the key is not in it,
        # ie if the acronym does not exist in the ontology database (as
        # would happen when typing wrong capitalisation, not naming roi,
        # etc).
        if None in isin:
            raise ValueError('Non-existent acronym {} in file {}'.\
                    format(ser.index.values, fname))
        # I have not decided how to deal with cases where the marker falls
        # inside more that 2 structures.
        assert len(isin) == 2, "One marker in more than one structure {}".format(isin)
        # Sort list of structures. The order will increase as each structure
        # becomes deeper in the ontology tree, so that we expect the last
        # structure in the list to be within the first one.
        isin.sort()
        assert isin[-1] in isin[0],\
                'Structure {} is not part of structure {}'.format(isin[-1],
                        isin[0])
        # If the above assumptions are true (ie that, compared to the first
        # structure, the second structure in the list is deeper in the ontology
        # and it is its subset), then we can set the membership of the marker
        # to the topmost structure to false. That is, the marker is assigned to 
        # the deeper structure of the two.
        sorted_mrk.loc[indx][isin[0].acronym] = False
    # Confirm that now each marker belongs to only one structure.
    assert np.all(sorted_mrk.sum(axis=1) == 1)
    # Finally, quantify and return the number of markers per structure.
    return sorted_mrk #.sum(axis=0)

datadir = '/home/antgon/projects/MCH-inputs'
#strain = 'MCH-tracing'
strain = 'MCH-tracing'
a = 'A22'
#a = 'A116'
#a = 'A219'
#a = 'A221'

WORKINGPATH = os.path.join(datadir, strain, a, 'tif/')

tot = pd.DataFrame()
ontology = Ontology()

files = os.listdir(WORKINGPATH)
files = [f for f in files if f.endswith('.hdf5')]
for fname in files:
    markers, rois, attrs = from_file(WORKINGPATH+fname)
    try:
        t = markers_per_struct(markers, rois, ontology)
        tot = pd.concat([tot, t])
    except AssertionError as error:
        print('Error in file {}: {}'.format(fname, error))
tot = tot.sum(axis=0, skipna=True)
# To add results from several dataframes when indices differ,
# concatenate these *before* totalling cell counts, ie
# This works:
#   df = pd.contcat([df1, df2])
#   df = df.sum(axis=0)
# But this does not:
#   df = pd.contact([df1.sum(0), df2.sum(0)])
# because in the latter case same-name indices are duplicated instead
# of added together.

# To save data as tab-separated values, with count values
# saved as integers (not float).
#tot.to_csv('test.tab', float_format='%i', sep='\t')


# Main regions for grouping structures:
hpf = ontology('HPF') # hippocampus
ctx = ontology('CTX') # cortex
th  = ontology('TH')  # thalamus
mb  = ontology('MB')  # midbrain
hy  = ontology('HY')  # hypothalamus
my  = ontology('MY')  # medulla
cnu = ontology('CNU') # cerebral nuclei
p   = ontology('P')   # pons
cb  = ontology('CB')  # cerebellum

t = pd.DataFrame(columns=['counts', 'level'], index=tot.index)
t['counts'] = tot.astype(int)

for name in tot.index.values:
    s = ontology(name)
    if   s in cnu or s == cnu: level = 1
    # Hippocampus before cortex because all cells
    # in hippocampus will also be in cortex:
    # if a in hpf is True, a in ctx is also True.
    elif s in hpf or s == hpf: level = 2
    elif s in ctx or s == ctx: level = 0
    elif s in th  or s == th:  level = 3
    elif s in hy  or s == hy:  level = 4
    elif s in mb  or s == mb:  level = 5
    elif s in my  or s == my:  level = 6
    elif s in p   or s == p:   level = 7
    else:                      level = 8
    t['level'][t.index==name] = level

t = t.sort_index(by='level')

binlabels = t.index.values



binw = 0.8
figh = 6 # 7
#figw = binlabels.size * 0.4
figw = 18
dpi = 100
left = np.arange(len(binlabels))
#ax = plt.figure(figsize=(18, 6)).add_subplot(111)
fig = plt.figure(figsize=(figw, figh), dpi=dpi)
ax = fig.add_subplot(111)

bincolours = ["#"+ontology(name).colour for name in binlabels]


ax.bar(left, t['counts'].values, width=binw, color=bincolours)
ax.set_xlim(0, left.max()+1)
ax.set_xticks(left+binw/2.)
ax.set_xticklabels(binlabels, rotation='vertical')
ax.set_ylabel("Counts")
[tick.set_visible(False) for tick in ax.get_xticklines()]

#plt.subplots_adjust(bottom=0.1, top=0.95, left=0.04, right=0.99)

# Manually add a legend:
from matplotlib.patches import Rectangle
legendw = binw

figratio = figh/figw
legendh = (ax.get_data_ratio() * legendw) / figratio
x = ax.get_xlim()[-1] * 0.02
y = ax.get_ylim()[-1] * 0.92
for region in [ctx, cnu, hpf, th, hy, mb, my, p]:
    colour = '#'+region.colour
    r = Rectangle((x, y), legendw, legendh, fc=colour)
    ax.add_patch(r)
    ax.text(x+legendw*1.5, y+legendh/2., region.name, va='center')
    y -= legendh*1.3

ax.set_title(strain + ' ' + a)
#ax.set_ylim(0, t['counts'].max()*1.02)
plt.tight_layout()

#plt.show()

#fig.savefig(a + '.png', dpi=dpi)
t.to_csv(a + '-counts.tab', sep='\t')
fig.savefig(a + '.svg')
plt.close('all')


    

'''
DataFrames:

Select column                     df[col]       Series
Select row by label               df.loc[label] Series
Select row by integer location    df.iloc[loc]  Series
Slice rows                        df[5:10]      DataFrame
Select rows by boolean vector     df[bool_vec]  DataFrame
'''
