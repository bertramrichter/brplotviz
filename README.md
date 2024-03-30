`brplotviz` are plot utilities for outputting plots using `matplotlib` and nicely formatted tables according to the personal taste of Bertram Richter.

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
record_list = [(x_list, y_list_sin, "scatter", {"label": "sine"}), (x_list, y_list_cos, "line", {"label": "cosine"})]
brplotviz.plot.mixed_graphs(record_list)
```

Finally, let's plot a bar chart first with one data record, then with multiple records:

```
brplotviz.plot.bar_categories([y_list_sin], category_names=x_list)
brplotviz.plot.bar_categories(y_table, category_names=x_list)
```

Plotting graphs is not the only thing, which can be done with `brplotviz`.
Presenting data in tabular form is also supported.
The killer feature here are the possibilities to format the entries either alltogether or each one separately.

```
brplotviz.table.print_table(
	table=y_table,
	engine="csv",
	head_row=x_list,
	head_col=record_names,
	top_left="Values",
	caption="Sine and cosine Values",
	formatter=":.2f",
	)
```

We can put out the table formatted as a LaTeX table as well.
After copying into a `.tex` file and compiling it with LaTeX, it is typeset with professional quality.
For this to work, follow the additional steps as described in \ref brplotviz.table.print_table_LaTeX().

```
brplotviz.table.print_table_LaTeX(
	table=y_table,
	head_row=x_list,
	head_col=record_names,
	top_left="Values",
	formatter=":.2f",
	caption="Sine and cosine Values",
	LaTeX_label="sinecosine",
	)
```

The content can be written to disk, if the keyword argument `file=<file path here>` is passed, which works for all presented functions.
Warning: the file is overwritten without further questions.

All of the presented functions are compiled in \ref example.py ready to run.

# Installation and Building documentation
Install this package via `pip install -U brplotviz`.
To build the documentation, run `doxygen` in this directory to generate it to the directory `./Documentation`

# Licence and Copyright
**Author:** Bertram Richter  
**Copyright:** Copyright by the author, 2024.  
**License:** This software is released under GPLv3, see [LICENSE](./LICENSE) for details

# Dependencies
- `Python >=3.?` (Developed under Python 3.9)
- `matplotlib >=3.5.0` for plotting and drawing graphs. See [matplotlib.org](https://matplotlib.org) for the documentation.
- `numpy` for array operations. See [numpy.org](https://numpy.org) for the documentation.
