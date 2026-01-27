"""
Loading Data with HyperSpy
===========================

This example demonstrates how to load and visualize data using the HyperSpy library.
"""

import hyperspy.api as hs
from em_database.data import SPEDAg

# Load a dataset using HyperSpy
dataset = SPEDAg()
data_path = dataset.download()  # Download the dataset if not already available
data = hs.load(data_path)
data

# %%
# Display the dataset
data.plot()
