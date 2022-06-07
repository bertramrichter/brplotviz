
## \file
## Contains functions for plotting.
## \author Bertram Richter
## \package plot \copydoc plot.py

from matplotlib import pyplot as plt
import numpy as np
import warnings
import styleselect

def single_line(x_values: list, y_values: list, record_name: str = None, *args, **kwargs):
	"""
	This function plots a single line graph. It's just a wrapper around \ref mixed_graphs().
	\param x_values List of floats for the x-axis values. Will be wrapped for \ref mixed_graphs(): `[x_values]` &rarr; `x_table`.
	\param y_values List of floats for the y-axis values. Will be wrapped for \ref mixed_graphs(): `[y_values]` &rarr; `y_table`.
	\param record_name Will be passed to to the `record_names` in \ref mixed_graphs().
	\param *args Positional arguments, will be passed to \ref mixed_graphs().
	\param *kwargs Keyword arguments, will be passed to \ref mixed_graphs().
	\return Returns the the figure and the axis objects: `fig, ax`.
	"""
	if record_name is None:
		kwargs["show_legend"] = False
	return mixed_graphs([(x_values, y_values, record_name, "line")], *args, **kwargs)

def single_scatter(x_values: list, y_values: list, record_name: str = None, *args, **kwargs):
	"""
	This function plots a single scatter graph. It's just a wrapper around \ref mixed_graphs().
	\param x_values List of floats for the x-axis values. Will be wrapped for \ref mixed_graphs(): `[x_values]` &rarr; `x_table`.
	\param y_values List of floats for the y-axis values. Will be wrapped for \ref mixed_graphs(): `[y_values]` &rarr; `y_table`.
	\param record_name Will be passed to to the `record_names` in \ref mixed_graphs().
	\param *args Positional arguments, will be passed to \ref mixed_graphs().
	\param *kwargs Keyword arguments, will be passed to \ref mixed_graphs().
	\return Returns the the figure and the axis objects: `fig, ax`.
	"""
	if record_name is None:
		kwargs["show_legend"] = False
	return mixed_graphs([(x_values, y_values, record_name, "scatter")], *args, **kwargs)

def multi_line(x_table, y_table, record_names: list = None, *args, **kwargs):
	"""
	This function plots multiple line graphs in a single figure. It's just a wrapper around \ref mixed_graphs().
	\param x_table List of lists, where each entry (line) is a data record for the x values.
	\param y_table List of lists, where each entry (line) is a data record for the y values.
	\param record_names List with the names of the table rows (records). If left `None`, no legend is shown.
	\param *args Positional arguments, will be passed to \ref mixed_graphs().
	\param *kwargs Keyword arguments, will be passed to \ref mixed_graphs().
	\return Returns the the figure and the axis objects: `fig, ax`.
	"""
	if record_names is None:
		record_names = ["Record {}".format(i) for i in range(len(y_table))]
		kwargs["show_legend"] = False
	assert len(x_table) == len(y_table) == len(record_names)
	record_list = list(zip(x_table, y_table, record_names, ["line"]*len(x_table)))
	return mixed_graphs(record_list, *args, **kwargs)

def multi_scatter(x_table, y_table, record_names: list = None, *args, **kwargs):
	"""
	This function plots  multiple scatter graphs in a single figure. It's just a wrapper around \ref mixed_graphs().
	\param x_table List of lists, where each entry (line) is a data record for the x values.
	\param y_table List of lists, where each entry (line) is a data record for the y values.
	\param record_names List with the names of the table rows (records).  If left `None`, no legend is shown.
	\param *args Positional arguments, will be passed to \ref mixed_graphs().
	\param *kwargs Keyword arguments, will be passed to \ref mixed_graphs().
	\return Returns the the figure and the axis objects: `fig, ax`.
	"""
	if record_names is None:
		record_names = ["Record {}".format(i) for i in range(len(y_table))]
		kwargs["show_legend"] = False
	assert len(x_table) == len(y_table) == len(record_names)
	record_list = list(zip(x_table, y_table, record_names, ["scatter"]*len(x_table)))
	return mixed_graphs(record_list, *args, **kwargs)

def mixed_graphs(record_list: list,
					xlabel: str = None,
					ylabel: str = None,
					tick_pos: list = None,
					tick_labels: list = None,
					show_legend: bool = True,
					closeafter: bool = True,
					file: str = None,
					pltsettings: dict = None):
	"""
	This function plots a number of mixed_graphs, either as line or scatter plot.
	\param record_list List tuples, with entries like `(<x_values>, <y_values>, <record_name>, <style>)`.
		- `x_values`: List of x-axis values.
		- `y_values`: List of y-axis values.
		- `record_name`: Name of the record. Is used in the legend.
		- `style`: Specifies, how the record should be shown. Available options are:
			- `"plot"` Generates a line plot.
			- `"scatter"` Generates a scatter plot.
	\param xlabel Description of the x-axis. Defaults to `None`.
	\param ylabel Description of the y-axis. Defaults to `None`.
	\param tick_pos Postions, where ticks should appear. Defaults to `None`, which means, that the default axis ticks are used.
		Both `tick_pos` and `tick_labels` need to be specified and of the same length for this to take effect.
	\param tick_labels Labels for the manually specified ticks. Defaults to `None`, which means, that the default axis ticks are used.
		Both `tick_pos` and `tick_labels` need to be specified and of the same length for this to take effect.
	\param show_legend Switch, whether the legend should be shown. Defaults to `True`.
	\param closeafter See \ref show_save_fig().
	\param file See \ref show_save_fig().
	\param pltsettings Dictionary of settings to be passed to `plt.rcParams`.
	\return Returns the the figure and the axis objects: `fig, ax`.
	"""
	pltsettings = pltsettings if pltsettings is not None else {}
	#show_legend = show_legend if show_legend is not None else (record_names is not None)
	#record_names = record_names if record_names is not None else [ "Record {}".format(i) for i in range(1, len(x_table)+1) ]
	fig, ax = get_figure(**pltsettings)
	# Draw the mixed_graphs
	for x_record, y_record, record_name, style in record_list:
		assert len(x_record) == len(y_record)
		if style == "line":
			ax.plot(x_record, y_record, label=record_name, **next(ax.line_style))
		elif style == "scatter":
			ax.plot(x_record, y_record, label=record_name, **next(ax.scatter_style))
	# Appearance
	if tick_pos is not None and tick_labels is not None:
		ax.set_xticks(ticks=tick_pos, labels=tick_labels, rotation=45)
	if xlabel is not None:
		ax.set_xlabel(xlabel)
	if ylabel is not None:
		ax.set_ylabel(ylabel)
	if show_legend:
		ax.legend(loc="best")
	show_save_fig(fig, file=file, closeafter=closeafter)
	return fig, ax

def bar_variable(bins: list,
					y_values: tuple,
					closeafter: bool = True,
					file: str = None,
					pltsettings: dict = None):
	"""
	Plots a bar plot with a variable number of bins.
	\todo Is it really necessary to be able use a variable number of bars per bin?
	\param bins Names of data classes e.g. `["a", "b", "c"]`.
	\param y_values List of lists. For each entry in `classes` there should be list of y_values. e.g. [[1],[2,3],[4,5,6,7]]
		They are grouped around symmetrically around the position of the class location.
	\param closeafter See \ref show_save_fig().
	\param file See \ref show_save_fig().
	\param pltsettings Dictionary of settings to be passed to `plt.rcParams`.
	\return Returns the the figure and the axis objects: `fig, ax`.
	"""
	pltsettings = pltsettings if pltsettings is not None else {}
	fig, ax = get_figure(**pltsettings)
	plot_style = styleselect.get_plot_style_hatch()
	hatch_list = list(plot_style)
	if len(y_values) > len(hatch_list):
		warnings.warn("Warning: too many records, some will not be printed")
	width = .5					# width of the bars
	bin_position_list = np.arange(len(bins))	# position of the bin centers
	for bin_pos, y_list in enumerate(bin_position_list, y_values):
		n_bars = len(y_list)
		d_x = width/n_bars
		pos_x = bin_pos - width/2 + d_x/2
		for j, h in enumerate(y_list):
			ax.bar(x=pos_x+j*d_x, height=h, width=d_x, **hatch_list[j])
	ax.set_xticks(ticks=bin_position_list, labels=bins, rotation=45)
	ax.legend(loc="best")
	show_save_fig(fig, file=file,  closeafter=closeafter)
	return fig, ax

def bar_categories(record_list: list,
					category_names: list = None,
					record_names: list = None,
					xlabel: str = None,
					ylabel: str = None,
					show_legend: bool = None,
					closeafter: bool = True,
					file: str = None,
					pltsettings: dict = None):
	"""
	Plots a bar plot, that groups several data sets according to the given categories.
	\param record_list List of lists, where each entry (line) is a data record.
	\param category_names Names of data classes e.g. `["a", "b", "c"]`. This corresponds to record_list column names.
	\param record_names Names of the record_list rows (records).
	\param xlabel Description of the x-axis. Defaults to `None`.
	\param ylabel Description of the y-axis. Defaults to `None`.
	\param show_legend Switch, whether the legend should be shown.
		Defaults to `None`, which will show a legend, if `record_names is not None`.
		Thus, if both `show_legend` and `record_names` are unspecified, no legend is shown.
	\param closeafter See \ref show_save_fig().
	\param file See \ref show_save_fig().
	\param pltsettings Dictionary of settings to be passed to `plt.rcParams`.
	\return Returns the the figure and the axis objects: `fig, ax`.
	"""
	# Setup: set, if the legend should be shown or not, set default labels for categories and records
	pltsettings = pltsettings if pltsettings is not None else {}
	show_legend = show_legend if show_legend is not None else (record_names is not None)
	category_names = category_names if category_names is not None else [ "Category {}".format(i) for i in range(1, len(record_list[0])+1) ]
	record_names = record_names if record_names is not None else [ "Record {}".format(i) for i in range(1, len(record_list)+1) ]
	assert len(record_list) == len(record_names)
	
	fig, ax = get_figure(**pltsettings)
	plot_style = styleselect.get_plot_style_hatch()
	hatch_list = list(plot_style)
	if len(record_list) > len(hatch_list):
		warnings.warn("Warning: too many records, some will not be printed")
	width = .8					# width of the bars
	n_bars = len(record_list)
	d_x = width/n_bars
	bin_position_list = np.arange(len(category_names))	# position of the bin centers
	for i, (heights, record_name, hatch_pattern) in enumerate(zip(record_list, record_names, hatch_list)):
		assert len(heights) == len(category_names)
		# Sanitize None entries
		heights = [entry if entry is not None else 0 for entry in heights]
		pos_x = bin_position_list - width/2 + d_x/2 + i*d_x
		ax.bar(x=pos_x, height=heights, width=d_x, label=record_name, **hatch_pattern)
	# Appearance
	ax.set_xticks(ticks=bin_position_list, labels=category_names, rotation=90)
	if xlabel is not None:
		ax.set_xlabel(xlabel)
	if ylabel is not None:
		ax.set_ylabel(ylabel)
	if show_legend:
		ax.legend(loc="best")
	show_save_fig(fig, file=file, closeafter=closeafter)
	return fig, ax

def get_figure(**pltsettings):
	"""
	Generate the figure and axes objects and apply the general setting using \ref set_plot_style_fig().
	\param pltsettings Dictionary of settings to be passed to `plt.rcParams`.
	\return `fig, ax` Figure and Axis object.
	The `ax` object is assigned three additional attributes:
		- `ax.line_style`: This style is used, when a line plot is done, see \ref single_line(), \ref multi_line() or `style=line` is passed to \ref mixed_graphs().
		- `ax.scatter_style`: This style is used, when a scatter plot is done, see \ref single_scatter(), \ref multi_scatter() or `style=scatter` is passed to \ref mixed_graphs().
		- `ax.hatch_style`: This style is used, when a bar plot is done, see \ref bar_categories().
	
	If it is desired to add plots afterwards, use the following snippets:
	- `ax.plot(x, y, label=<name>, **next(ax.line_style))` for a line plot
	- `ax.plot(x, y, label=<name>, **next(ax.scatter_style))` for a scatter plot
	"""
	styleselect.set_plot_style_fig(**pltsettings)
	fig, ax = plt.subplots()
	ax.grid(True)
	ax.set_axisbelow(True)
	ax.line_style = styleselect.get_plot_style_line()()
	ax.scatter_style = styleselect.get_plot_style_scatter()()
	ax.hatch_style = styleselect.get_plot_style_hatch()()
	fig.set_tight_layout("tight")
	return fig, ax

def show_save_fig(fig, file: str = None, closeafter: bool = True):
	"""
	Shows or saves the figure.
	\param fig Figure to be shown or saved.
	\param file Path to the file in which the graph is saved. Defaults to `None`, which means the graph is shown on screen instead of saved to disk.
		If a valid path is given, the graph is saved to this file. Overwrites the content of the file without further questions.
	\param closeafter Switch, whether the figure should be closed after showing or saving. Defaults to `True`.
	"""
	if file is None:
		# use `plt.show()` for staying open figure_handling the window is closed. It manages the event loop, which `fig.show()` does not.
		# `fig.show()` does not block and closes imediately, if not in an interactive mode.
		# For more, see https://matplotlib.org/stable/api/figure_api.html#matplotlib.figure.Figure.show  
		plt.show(block=True)
	else:
		try: fig.savefig(file)
		except: print('Failed to save plot to file "{}"'.format(file))
	# close the current figure, cleans the memory.
	if closeafter:
		plt.close(fig)

if __name__ == "__main__":
	pass