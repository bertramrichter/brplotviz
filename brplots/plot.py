
## \file
## Contains functions for plotting.
## \author Bertram Richter
## \package plot \copydoc plot.py

from matplotlib import pyplot as plt
import numpy as np
import styleselect

def get_figure():
	"""
	Generate the figure and axes objects and apply the general setting using \ref set_plot_style_fig().
	\return `fig, ax` Figure and Axis object.
	"""
	styleselect.set_plot_style_fig()
	fig, ax = plt.subplots()
	ax.grid(True)
	ax.set_axisbelow(True)
	fig.set_tight_layout("tight")
	return fig, ax

def graph(x_values: list,
					y_values: list,
					record_name: list = None,
					xlabel: str = None,
					ylabel: str = None,
					tick_pos: list = None,
					tick_labels: list = None,
					style: str = "line",
					show_legend: bool = None,
					file: str = None):
	"""
	This function plots a single graph, either as line or scatter plot.
	\param x_values List of the x values.
	\param y_values List of the y values.
	\param xlabel Description of the x-axis. Defaults to `None`.
	\param ylabel Description of the y-axis. Defaults to `None`.
	\param record_name Names of the data record.
		If left `None` (Default), no legend is plot.
		\todo Default to no legend, if set to `None`.
	\param tick_pos Postions, where ticks should appear. Defaults to `None`, which means, that the default axis ticks are used.
		Both `tick_pos` and `tick_labels` need to be specified and of the same length for this to take effect.
	\param tick_labels Labels for the manually specified ticks. Defaults to `None`, which means, that the default axis ticks are used.
		Both `tick_pos` and `tick_labels` need to be specified and of the same length for this to take effect.
	\param style Plotting style. Available options:
		- `"plot"` Generates a line plot.
		- `"scatter"` Generates a scatter plot.
	\param show_legend Switch, whether the legend should be shown.
		Defaults to `None`, which will show a legend, if `record_names is not None`.
		Thus, if both `show_legend` and `record_names` are unspecified, no legend is shown.
	\param file See \ref show_save_fig().
	"""
	show_legend = show_legend if show_legend is not None else (record_name is not None)
	assert len(x_values) == len(y_values)
	fig, ax = get_figure()
	# Get the correct plot style
	if style == "line":
		plot_style = styleselect.get_plot_style_line()
	elif style == "scatter":
		plot_style = styleselect.get_plot_style_scatter()
	ax.set_prop_cycle(plot_style)
	# Draw the graphs
	ax.plot(x_values, y_values, label=record_name)
	# Appearance
	if tick_pos is not None and tick_labels is not None:
		ax.set_xticks(ticks=tick_pos, labels=tick_labels, rotation=45)
	if xlabel is not None:
		ax.set_xlabel(xlabel)
	if ylabel is not None:
		ax.set_ylabel(ylabel)
	if show_legend:
		ax.legend(loc="best")
	show_save_fig(fig, file)
	
def multi_graph(x_table: list,
					y_table: list,
					record_names: list = None,
					xlabel: str = None,
					ylabel: str = None,
					tick_pos: list = None,
					tick_labels: list = None,
					style: str = "line",
					show_legend: bool = None,
					file: str = None):
	"""
	This function plots a number of graphs, either as line or scatter plot.
	\param x_table List of lists, where each entry (line) is a data record for the x values.
	\param y_table List of lists, where each entry (line) is a data record for the y values.
	\param xlabel Description of the x-axis. Defaults to `None`.
	\param ylabel Description of the y-axis. Defaults to `None`.
	\param record_names Names of the table rows (records).
		If left `None` (Default), then each record is named `Record <n>` with n as a serial number.
		\todo Default to no legend, if set to `None`.
	\param tick_pos Postions, where ticks should appear. Defaults to `None`, which means, that the default axis ticks are used.
		Both `tick_pos` and `tick_labels` need to be specified and of the same length for this to take effect.
	\param tick_labels Labels for the manually specified ticks. Defaults to `None`, which means, that the default axis ticks are used.
		Both `tick_pos` and `tick_labels` need to be specified and of the same length for this to take effect.
	\param style Plotting style. Available options:
		- `"plot"` Generates a line plot.
		- `"scatter"` Generates a scatter plot.
	\param show_legend Switch, whether the legend should be shown.
		Defaults to `None`, which will show a legend, if `record_names is not None`.
		Thus, if both `show_legend` and `record_names` are unspecified, no legend is shown.
	\param file See \ref show_save_fig().
	"""
	show_legend = show_legend if show_legend is not None else (record_names is not None)
	record_names = record_names if record_names is not None else [ "Record {}".format(i) for i in range(1, len(x_table)+1) ]
	assert len(x_table) == len(y_table) == len(record_names)
	fig, ax = get_figure()
	# Get the correct plot style
	if style == "line":
		plot_style = styleselect.get_plot_style_line()
	elif style == "scatter":
		plot_style = styleselect.get_plot_style_scatter()
	ax.set_prop_cycle(plot_style)
	# Draw the graphs
	for x_record, y_record, record_name in zip(x_table, y_table, record_names):
		assert len(x_record) == len(y_record)
		ax.plot(x_record, y_record, label=record_name)
	# Appearance
	if tick_pos is not None and tick_labels is not None:
		ax.set_xticks(ticks=tick_pos, labels=tick_labels, rotation=45)
	if xlabel is not None:
		ax.set_xlabel(xlabel)
	if ylabel is not None:
		ax.set_ylabel(ylabel)
	if show_legend:
		ax.legend(loc="best")
	show_save_fig(fig, file)

def bar_variable(bins: list, y_values: tuple):
	"""
	Plots a bar plot with a variable number of bins.
	\todo Is it really necessary to be able use a variable number of bars per bin?
	\param bins Names of data classes. e.g. ["a", "b", "c"]
	\param y_values List of lists. For each entry in `classes` there should be list of y_values. e.g. [[1],[2,3],[4,5,6,7]]
		They are grouped around symmetrically around the position of the class location.
	"""
	fig, ax = get_figure()
	plot_style = styleselect.get_plot_style_hatch()
	hatch_list = list(plot_style)
	if len(table) > len(hatch_list):
		print("Warning: too many records, some will not be printed")
	#set_custom_style(custom_style)
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
	show_save_fig(fig)

def bar_categories(table: list,
					xlabel: str = None,
					ylabel: str = None,
					category_names: list = None,
					record_names: list = None,
					show_legend: bool = None,
					file: str = None):
	"""
	Plots a bar plot, that groups several data sets according to the given categories.
	\param table List of lists, where each entry (line) is a data record.
	\param xlabel Description of the x-axis. Defaults to `None`.
	\param ylabel Description of the y-axis. Defaults to `None`.
	\param category_names Names of data classes. e.g. ["a", "b", "c"]. This corresponds to table column names.
	\param record_names Names of the table rows (records).
		\todo Default to no legend, if set to `None`.
	\param show_legend Switch, whether the legend should be shown.
		Defaults to `None`, which will show a legend, if `record_names is not None`.
		Thus, if both `show_legend` and `record_names` are unspecified, no legend is shown.
	\param file See \ref show_save_fig().
	"""
	# Setup: set, if the legend should be shown or not, set default labels for categories and records
	show_legend = show_legend if show_legend is not None else (record_names is not None)
	category_names = category_names if category_names is not None else [ "Category {}".format(i) for i in range(1, len(table[0])+1) ]
	record_names = record_names if record_names is not None else [ "Record {}".format(i) for i in range(1, len(table)+1) ]
	assert len(table) == len(record_names)
	
	fig, ax = get_figure()
	plot_style = styleselect.get_plot_style_hatch()
	hatch_list = list(plot_style)
	if len(table) > len(hatch_list):
		print("Warning: too many records, some will not be printed")
	width = .8					# width of the bars
	n_bars = len(table)
	d_x = width/n_bars
	bin_position_list = np.arange(len(category_names))	# position of the bin centers
	for i, (heights, record_name, hatch_pattern) in enumerate(zip(table, record_names, hatch_list)):
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
	show_save_fig(fig, file=file)

def show_save_fig(fig, file: str = None):
	"""
	Shows or saves the plot.
	\param fig Figure to be shown or saved.
	\param file Path to the file in which the graph is saved. Defaults to `None`, which means the graph is shown on screen instead of saved to disk.
		If a valid path is given, the graph is saved to this file. Overwrites the content of the file without further questions.
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
	plt.close(fig)

if __name__ == "__main__":
	table = [[1,2,3], [4,5,6]]
	x_table = [[1,2,3,4],[1,2,3,4,5]]
	y_table = [[1,2,3,4],[7,6,5,4,7]]
	tick_pos = [2,3,5]
	tick_labels = ["ja", "nein", "vllt"]
	bar_categories(table)
	bar_categories(table, category_names=["A", "B", "C"], record_names=["erstens", "zweitens"])
	multi_graph(x_table, y_table, style="line")
	multi_graph(x_table, y_table, style="scatter")
