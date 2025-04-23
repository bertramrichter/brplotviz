`brplotviz` – utilities for nicely formatted tables and plots

# Installation and Building documentation

Install this package via `pip install -U brplotviz`.
To build the documentation, download the source code and unpack it.
Then, run `doxygen` in `brplotviz`'s root directory (this one).
How to install `doxygen`, see on their website ([doxygen.nl](https://doxygen.nl)).
The documentation will be assing it to the directory `./Documentation`

# Getting started

`brplotviz` consists of two packages, `table` and `plot`.

## Table

`brplotviz.plot.table` provides functions to format and output tabular data.
This tabular data is expected to be a sequence of sequences (list of lists ect.).
When a row (or column) is shorter than the others the missing cells are added as empty ones.
Multi-line cells (containing newline characters) are supported,
additional lines are inserted in the output plain text table a required.

### Styles

`brplotviz.table` comes with a few table styles.
To showcase the different styles, the script is used, where only the
`<style>` is replaced with the following options.

Some finer, advanced tuning of the style can be done with the `style_kwargs` dictionary.
For example, padding of the cells on the left or right side is possible.

```py
table_data = [
	["a",123.456, 12],
	["bc\nde", 23.34, 345],
	["and f", 45.],
	]

table.print_table(
	table=table_data,
	style=<style>,
	)
```

`"csv"` is a simple character-separated value style.
The separator character is configurable, but defaults to the comma (`","`).

```
a    ,123.456,12 
bc   ,23.34  ,345
de   ,       ,   
and f,45.0   ,   
```

`"tsv"` is a special case of `csv` with tab (`"\t"`) as separator charater.

```
a    	123.456	12 
bc   	23.34  	345
de   	       	   
and f	45.0   	   
```

`"latex"`
A table using the LaTeX markup with `booktabs` rules.
This only sets the content that goes into the body of a `tabular` environment.

```
\toprule
a    &123.456&12 \\
\midrule
bc   &23.34  &345\\
de   &       &   \\
and f&45.0   &   \\
\bottomrule
```

A complete LaTeX environment is output the wrapper function `brplotviz.table.print_table_LaTeX()`.
This function accepts the same (and some more) arguments than `brplotviz.table.print_table()`

```py
brplotviz.table.print_table_LaTeX(
	table=table,
	caption="This is the caption",
	LaTeX_label="example",
	)
```

The result is the following LaTeX code.
Note, that `brplotviz` will try to fill in the column alignment based on `align`.
To overwrite the default, use the argument `LaTeX_format`.
`LaTeX_format` works in analogy to `align`.

```
\begin{table}[!htbp]
\centering
\caption{This is the caption}
\label{tab:example}
\begin{tabular}{@{}
*{3}{l}
@{}}
\toprule
a    &123.456&12 \\
\midrule
bc   &23.34  &345\\
de   &       &   \\
and f&45.0   &   \\
\bottomrule
\end{tabular}
\end{table}
```

"markdown"`outputs a Markdown table.

```
|a    |123.456|12  |
|:----|:------|:---|
|bc   |23.34  |345 |
|de   |       |    |
|and f|45.0   |    |
```

`"test"` is for testing purposes.

```
---TopRule---
^> a     <||> 123.456 <|> 12  <$
---HeadRule---
^> bc    <||> 23.34   <|> 345 <$
---NoRule---
^> de    <||>         <|>     <$
---MidRule---
^> and f <||> 45.0    <|>     <$
---BotRule---
```

Custom styles are possible by sub-classing `brplotviz.tables.styles.Style`.

### Headers

`brplotviz.table` provides the option to add headers, to both columns and rows.
The `example_table`, that we plotted could be only the body of the table.

```py
head_row = ["Col 1", "Col 2", "Col 3"]
head_col = ["Row 1", "Row 2", "Row 3"]
top_left = "Top left"
align = ["l", "c", "r", "r"]

table.print_table(
	table=table_data,
	style="markdown",
	head_col=head_col,
	head_row=head_row,
	top_left=top_left,
	)
```

Note, that both the header row `head_row` and header column `head_col`
can be set independently of each other.

```
|Top left|Col 1|Col 2  |Col 3|
|:-------|:----|:------|:----|
|Row 1   |a    |123.456|12   |
|Row 2   |bc   |23.34  |345  |
|        |de   |       |     |
|Row 3   |and f|45.0   |     |
```

Table rows are numbered automatically when setting `head_col="enumerate"`.
The numbering starts after the header row.
Note, that rows with multiline cells are taken into account.

```
|Top left|Col 1|Col 2  |Col 3|
|:-------|:----|:------|:----|
|1       |a    |123.456|12   |
|2       |bc   |23.34  |345  |
|        |de   |       |     |
|3       |and f|45.0   |     |
```

### Formatting

The formatting of the table's cells can be set table-global, column-wise or for each cell individually.
If the `formatter` is a string, this formatter is applied to all cells of the table.
If the `formatter` is a list of strings, the formatting is applied column-wise (without the `head_col`).
If the `formatter` is a list of list strings, the formatting is applied for each cell individually.
The `formatter` is expected in the [Format Specification Mini-Language](https://docs.python.org/3/library/string.html#formatspec).
Here, it is shown for a column-wise formatting:

```py
table.print_table(
	table=table_data,
	style="markdown",
	formatter=["", ":.2f", ":.1f"],
	)
```

```
|Top left|Col 1|Col 2 |Col 3|
|:-------|:----|:-----|:----|
|1       |a    |123.46|12.0 |
|2       |bc   |23.34 |345.0|
|        |de   |      |     |
|3       |and f|45.00 |     |
```

### Alignment

Columns are alined by adding whitespace to make all cells in a column to the same width.
By default, all cells are printed left-aligned.
Similar to the formatting, the alignment can be set for all columns or for each column separately.
Alignment can be turned off by setting `align=None`.

```py
table.print_table(
	table=table_data,
	style="markdown",
	align=["l", "c", "r", "r"],
	)
```

```
|Top left|Col 1| Col 2 |Col 3|
|:-------|:---:|------:|----:|
|1       |  a  |123.456|   12|
|2       | bc  |  23.34|  345|
|        | de  |       |     |
|3       |and f|   45.0|     |
```


### Rules

The horizontal lines in the table ar ecalled rules.
To add an extra rule include a `brplotviz.table.rules.ExtraRule` in the `table`.
Note, that not all styles support `ExtraLines`.
The rule separating the header column from the body can be suppressed by `omit_head_rule=True`.

### Additional options for table output

To transpose the `table` (switch columns with rows), use `transpose=True`.
Note, that this will not switch `head_col` and `head_row`.

With `replacement`, a dictionary can be passed to replace cell content.
If a cell's content is found in the replacement`'s keys, the content is replaced with the associated value.
Note, that the replacement takes place after formatting.

By default `brplotviz.table.print_table()`, prints the typeset table and returns nothing (`None`).
To return the lines, set `return_lines=True`.
Set `show=False` to turn off the printing.

## Plot

`brplotviz.plot` provides functions to simplify the output of nicely formatted graphs.
The focus is on a graphical style suited for printing.
Thus, a monochrome (black-white) style is used.

Let's start plotting.
First, we need some data:

```py
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
Each one is shown on separately.

```py
brplotviz.plot.single_line(x_list, y_list_sin)
brplotviz.plot.single_scatter(x_list, y_list_sin)
```

Plotting several line plots or mutliple scatter plots is:

```py
brplotviz.plot.multi_line(x_table, y_table, record_names)
brplotviz.plot.multi_scatter(x_table, y_table, record_names)

```

To mix line and scatter plot we need to construct a list of data record tuples first:

```py
record_list = [(x_list, y_list_sin, "scatter", {"label": "sine"}), (x_list, y_list_cos, "line", {"label": "cosine"})]
brplotviz.plot.mixed_graphs(record_list)
```

Finally, let's plot a bar chart first with one data record, then with multiple records:

```py
brplotviz.plot.bar_categories([y_list_sin], category_names=x_list)
brplotviz.plot.bar_categories(y_table, category_names=x_list)
```

## Output

By default, plots are shown on screen and tables are printed to the standard output.
Plots and tables can be written to disk with the keyword argument `file=<file path here>`.
If `file` is set, the nothing shown (neither plots or tables), unless `show=True` is set explicitely.

**Warning**: the file is overwritten without further questions.

# Licence and Copyright

**Author:** Bertram Richter  
**Copyright:** Copyright by the author, 2024.  
**License:** This software is released under GPLv3, see [LICENSE](./LICENSE) for details

# Dependencies

- `Python >=3.?` (Developed under Python 3.9)
- `matplotlib >=3.5.0` for plotting and drawing graphs. See [matplotlib.org](https://matplotlib.org) for the documentation.
- `numpy` for array operations. See [numpy.org](https://numpy.org) for the documentation.
