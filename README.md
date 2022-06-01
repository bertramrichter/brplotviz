`brplotviz` are plot utitilies for outputting plots using `matplotlib` and nicely formatted tables according to the personal taste of Bertram Richter.

# Getting started
This package provides functions to simplify the output of nicely fomatted graphs.
The main focus is to enable consistent graphical style suited for printing.
Thus, a monochrome (black-white) style is used.

Let's start plotting.
First, we need some data:
```
import numpy as np
import brplotviz
x_list = np.linspace(0, 2, 17)
y_list_sin = np.sin(x_list)
y_list_cos = np.cos(x_list)
x_table = [x_list, x_list]
y_table = [y_list_sin, y_list_cos]
record_names = ["sine", "cosine"]
```
Plotting a single line-graph and a scatter plot is as simple as:
```
brplotviz.plot.single_line(x_list, y_list_sin)
brplotviz.plot.single_scatter(x_list, y_list_sin)
```
Plotting several line plots or mutliple scatter plots is:
```
brplotviz.plot.multi_line(x_table, y_table, record_names)
brplotviz.plot.multi_scatter(x_table, y_table, record_names)
```
To mix line and scatter plot we need to construct a list of data record tuples first:
```
record_list = [(x_list, y_list_sin, "sine", "scatter"), (x_list, y_list_cos, "cosine", "line")]
brplotviz.plot.mixed_graphs(record_list)
```
Finally, let's plot a bar chart first with one data record, then with multiple records:
```
brplotviz.plot.bar_categories([y_list_sin], category_names=x_list)
brplotviz.plot.bar_categories(y_table, category_names=x_list)
```
This script ready to run is provided in \ref example.py.

# Installation and Building documentation
In order to use this framework, make sure, that:
- the dependencies as stated below are correctly installed (follow the instruction of the packages),
- this `brplotviz` directory is in your `$PYTHONPATH`, for the modules to be importable.

To build the documentation, run `doxygen` in this directory to generate it to the directory `./Documentation`

# Licence and Copyright
\author Bertram Richter
\copyright GPLv3 or later
\date 2022

# Dependencies
- `Python >=3.?` (Developend under Python 3.9)
- `matplotlib >=3.5.0` for plotting and drawing graphs. See [matplotlib.org](https://matplotlib.org) for the documentation.
