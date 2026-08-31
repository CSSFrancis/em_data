"""
Finding a Dataset
=================

``em_database`` ships an index of every dataset it knows about, and three
functions for querying it: :func:`~em_database.datasets`,
:func:`~em_database.search` and :func:`~em_database.filter`. All three return
dataset objects, so anything they hand back can be downloaded directly.

Nothing here touches the network - the index is metadata that ships with the
package, and querying it never opens a file.
"""

import em_database

# %%
# Every dataset in the index.
print(len(em_database.list_datasets()), "datasets")

# %%
# ``search`` is the browser widget's search box, callable. It matches a
# lowercased blob of every field - name, description, technique, detector,
# microscope, tags, authors and their affiliations - and every whitespace
# separated term has to appear somewhere, though not in the same field.
for ds in em_database.search("amorphous"):
    print(f"{type(ds).__name__:24s} {ds.metadata.technique:8s} {ds.size:>9s}")

# %%
# Because terms may land in different fields, a query can combine what an
# instrument is with what the technique was.
for ds in em_database.search("jeol eels"):
    print(type(ds).__name__)

# %%
# ``filter`` matches named fields instead. Strings compare exactly but
# case-insensitively, ``tags`` and ``authors`` test membership, and a list
# means any of its values.
for ds in em_database.filter(technique="4D-STEM", tags="Strain"):
    print(ds, "·", ", ".join(ds.metadata.tags))

# %%
for ds in em_database.filter(microscope_vendor=["JEOL", "Hitachi"]):
    print(ds)

# %%
# ``downloaded`` and ``location`` describe this machine rather than the
# dataset, which makes "what do I already have" a one-liner.
for ds in em_database.filter(downloaded=True):
    print(f"{type(ds).__name__:24s} {ds.filepath()}")

# %%
# An unknown field raises rather than being ignored - a typo that quietly
# returned the whole index would be worse than an error.
try:
    em_database.filter(techniqu="4D-STEM")
except TypeError as error:
    print(error)

# %%
# The result is a dataset, so it is ready to use. Sizes are integers
# (``size_bytes``), so they sort; ``size`` is the same number for reading.
smallest = min(em_database.filter(technique="EELS"), key=lambda ds: ds.size_bytes or 0)
print(smallest)
print()
print(smallest.metadata)
