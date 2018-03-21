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
g81_output_raw = """  0.16417  0.17111  0.17528  0.17667  0.17528  0.17111  0.16417
  0.16213  0.16579  0.16805  0.16889  0.16832  0.16635  0.16296
  0.15991  0.16129  0.16224  0.16278  0.16289  0.16258  0.16185
  0.15750  0.15759  0.15787  0.15833  0.15898  0.15981  0.16083
  0.15491  0.15471  0.15493  0.15556  0.15659  0.15805  0.15991
  0.15213  0.15264  0.15342  0.15444  0.15573  0.15727  0.15907
  0.14917  0.15139  0.15333  0.15500  0.15639  0.15750  0.15833"""

# Define your regex rules here depending on how
# your raw output looks. Ultimately, you want to
# arrive at several lines of comma separated
# float values, so split() works well later.
g81_output_parsed = re.sub(r"^  ", "", g81_output_raw)
g81_output_parsed = re.sub(r"\n  ", "\n", g81_output_parsed)
g81_output_parsed = re.sub(r"  ", ",", g81_output_parsed)

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