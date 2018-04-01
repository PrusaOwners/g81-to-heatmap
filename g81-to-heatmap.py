import numpy as np
import re
import matplotlib

# Tell matplotlib to not worry about DISPLAY
matplotlib.use('Agg')

# Import pyplot as plt for ease of use
import matplotlib.pyplot as plt

# This is the raw G81 output from Pronterface,
# Your regex replace rules below will clean it
# and make it ready for conversion to a list of
# float values.
g81_output_raw = """  0.10667  0.18056  0.22583  0.24250  0.23056  0.19000  0.12083
  0.09296  0.12148  0.14083  0.15102  0.15204  0.14389  0.12657
    0.08685  0.08265  0.08321  0.08852  0.09858  0.11340  0.13296
      0.08833  0.06407  0.05296  0.05500  0.07019  0.09852  0.14000
        0.09741  0.06574  0.05009  0.05046  0.06685  0.09926  0.14769
          0.11407  0.08765  0.07460  0.07491  0.08858  0.11562  0.15602
            0.13833  0.12981  0.12648  0.12833  0.13537  0.14759  0.16500"""

# Define your regex rules here depending on how
# your raw output looks. Ultimately, you want to
# arrive at several lines of comma separated
# float values, so split() works well later.
g81_output_parsed = re.sub(r"^[ ]+", "", g81_output_raw)
g81_output_parsed = re.sub(r"\n[ ]+", "\n", g81_output_parsed)
g81_output_parsed = re.sub(r"[ ]+", ",", g81_output_parsed)

# We're about to convert these strings into floats,
# this list will hold onto those.
g81_list_of_lists = []

# Split our regex corrected output by line, then
# split each line by its commas and convert the
# string values to floats.
for line in g81_output_parsed.splitlines():
    g81_list_of_lists.append([float(i) for i in line.split(",")])

# Let's take our list of lists and make it into
# a numpy array that matplotlib can do something
# with.
g81_array = np.array(g81_list_of_lists)

# Set figure and gca objects, this will let us
# adjust things about our heatmap image as well
# as adjust axes label locations.
fig = plt.figure()
ax = plt.gca()

# Calculate our heatmap. Interpolation is used
# to create the smooth looks. At this point you
# can still adjust some visual elements later.
# "cmap" controls the matplotlib colormap scheme.
plt.imshow(g81_array, interpolation='spline16', cmap='plasma')

# Set various options about the graph image before
# we generate it. Things like labeling the axes and
# colorbar, and setting the X axis label/ticks to
# the top to better match the G81 output.
plt.xlabel("X Axis")
plt.ylabel("Y Axis")
plt.colorbar(label="Bed Variance (in mm)")
ax.xaxis.set_ticks_position('top')
ax.xaxis.set_label_position('top')

# Save our graph as an image in the current directory.
fig.savefig('g81_heatmap.png')
