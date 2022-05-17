
## \file
## This is an example, how to use the `brplotviz` functions.
## \author Bertram Richter
## \date 2022
## \package example \copydoc example.py

import numpy as np
import brplotviz

## x-coordinates
x_list = np.linspace(0, 2, 17)
## y-coodinates for the sine function
y_list_sin = np.sin(x_list)
## y-coodinates for the cosine function
y_list_cos = np.cos(x_list)
## 2d array (list of list) for the x-coordinates. Each entry in the out list is a data record.
x_table = [x_list, x_list]
## 2d array (list of list) for the y-coordinates. Each entry in the out list is a data record.
y_table = [y_list_sin, y_list_cos]
## List with the names of the records
record_names = ["sine", "cosine"]

# Plotting a single line-graph and a scatter plot is as simple as:
brplotviz.plot.single_line(x_list, y_list_sin, record_name="sine")
brplotviz.plot.single_scatter(x_list, y_list_sin, record_name="cosine")
# Plotting several line plots or mutliple scatter plots is:
brplotviz.plot.multi_line(x_table, y_table, record_names)
brplotviz.plot.multi_scatter(x_table, y_table, record_names)
## To mix line and scatter plot we need to construct a list of data record tuples first:
record_list = [(x_list, y_list_sin, "sine", "scatter"), (x_list, y_list_cos, "cosine", "line")]
brplotviz.plot.mixed_graphs(record_list)
# Finally, let's plot a bar chart first with one data record, then with multiple records:
brplotviz.plot.bar_categories([y_list_sin], category_names=x_list)
brplotviz.plot.bar_categories(y_table, category_names=x_list, record_names=record_names)