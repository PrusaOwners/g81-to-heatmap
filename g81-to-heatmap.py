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
g81_output_raw = """  0.13083  0.13491  0.13713  0.13750  0.13602  0.13269  0.12750
  0.12806  0.13072  0.13214  0.13231  0.13124  0.12893  0.12537
  0.12667  0.12803  0.12871  0.12870  0.12800  0.12662  0.12454
  0.12667  0.12685  0.12685  0.12667  0.12630  0.12574  0.12500
  0.12806  0.12717  0.12655  0.12620  0.12612  0.12631  0.12676
  0.13083  0.12899  0.12782  0.12731  0.12748  0.12831  0.12981
  0.13500  0.13231  0.13065  0.13000  0.13037  0.13176  0.13417"""

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
