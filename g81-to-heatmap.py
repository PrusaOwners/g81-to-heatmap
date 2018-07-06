import datetime
import numpy as np
import re
import matplotlib
import matplotlib.image as mpimg

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

g81_xyz_list_of_lists = []
row_count = 0
col_count = 0
x_size = 250
y_size = 210
x_probe_offset = 23
y_probe_offset = 5
pinda_diameter = 8
left_probe_bed_position = 13.0 + x_probe_offset
right_probe_bed_position = 216.0 + x_probe_offset
back_probe_bed_position = 204.4 + y_probe_offset - pinda_diameter/2
front_probe_bed_position = 8.4 + y_probe_offset - pinda_diameter/2
x_inc = (right_probe_bed_position - left_probe_bed_position) / 6 
y_inc = (back_probe_bed_position - front_probe_bed_position) / 6
x_vals = np.zeros(7)
y_vals = np.zeros(7)
z_vals = np.zeros(shape=(7,7))
for col in g81_list_of_lists:
  for val in col:
    x_vals[col_count] = col_count*x_inc + left_probe_bed_position
    y_vals[row_count] = row_count*y_inc + front_probe_bed_position
    z_vals[col_count][row_count] = val
    row_count = row_count + 1
  col_count = col_count + 1
  row_count = 0

# Set figure and gca objects, this will let us
# adjust things about our heatmap image as well
# as adjust axes label locations.
fig = plt.figure(dpi=96, figsize=(12, 9))
ax = plt.gca()

for x in x_vals:
  for y in y_vals:
    plt.plot(x, y, '.', color='k')
for x in [0, 3, 6]:
  for y in [0, 3, 6]:
    plt.plot(x_vals[x], y_vals[y], 'o', color='m')

plt.contourf(x_vals, y_vals[::-1], z_vals, alpha=.5, antialiased=True)
img = mpimg.imread('mk42_full-pcb.png')
plt.imshow(img, extent=[x_vals[0]-37, x_vals[6]+14, y_vals[0]-16.4, y_vals[6]+37], interpolation="lanczos")
ax.set_xlim(left=0, right=x_size)
ax.set_ylim(bottom=0, top=y_size)

# Set various options about the graph image before
# we generate it. Things like labeling the axes and
# colorbar, and setting the X axis label/ticks to
# the top to better match the G81 output.
plt.title("Mesh Level: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
plt.axis('image')
ax.axes.get_xaxis().set_visible(False)
ax.axes.get_yaxis().set_visible(False)
plt.colorbar(label="Bed Variance: " + str(round(z_vals.max() - z_vals.min(), 3)) + "mm")

# Save our graph as an image in the current directory.
fig.savefig('g81_heatmap.png', bbox_inches="tight")
