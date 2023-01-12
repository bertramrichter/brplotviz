
"""
\file
Contains functions for plotting.
\author Bertram Richter
\date 2022
\package brplotviz.plot \copydoc plot.py
"""

import os
import warnings

from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np

from . import styleselect

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
	return multi_line([x_values], [y_values], [record_name], *args, **kwargs)

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
	return multi_scatter([x_values], [y_values], [record_name], *args, **kwargs)

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
	if not (len(x_table) == len(y_table) == len(record_names)):
			raise ValueError("Number of x-records ({}) != Number of y-records ({}) != Number of record names ({})".format(len(x_table), len(y_table), len(record_names)))
	record_list = []
	for x, y, name in zip(x_table, y_table, record_names):
		record_list.append((x, y, "line", {"label": name}))
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
	if not (len(x_table) == len(y_table) == len(record_names)):
			raise ValueError("Number of x-records ({}) != Number of y-records ({}) != Number of record names ({})".format(len(x_table), len(y_table), len(record_names)))
	record_list = []
	for x, y, name in zip(x_table, y_table, record_names):
		record_list.append((x, y, "scatter", {"label": name}))
	return mixed_graphs(record_list, *args, **kwargs)

def mixed_graphs(record_list: list,
				xlabel: str = None,
				ylabel: str = None,
				x_tick_pos: list = None,
				x_tick_labels: list = None,
				y_tick_pos: list = None,
				y_tick_labels: list = None,
				show_legend: bool = True,
				pltrcParams: dict = None,
				pltsettings: dict = None,
				file: str = None,
				closeafter: bool = True,
				show: bool = None,
				fig = None,
				ax = None,
				*args, **kwargs):
	"""
	This function plots a number of mixed_graphs, either as line or scatter plot.
	\param record_list List tuples, with entries like `(<x_values>, <y_values>, <style>, <graphsettings>)`.
		- `x_values`: List of x-axis values.
		- `y_values`: List of y-axis values.
		- `style`: Specifies, how the record should be shown. Available options are:
			- `"plot"`: Generates a line plot.
			- `"scatter"`: Generates a scatter plot.
		- `graphsettings` Dictionary with settings according to `matplotlib.Axes.ax.plot()`, which will be applied to this specific graph.
	\param xlabel Description of the x-axis. Defaults to `None`.
	\param ylabel Description of the y-axis. Defaults to `None`.
	\param x_tick_pos Postions, where ticks should appear. Defaults to `None`, which means, that the default axis ticks are used.
		Both `x_tick_pos` and `x_tick_labels` need to be specified and of the same length for this to take effect.
	\param x_tick_labels Labels for the manually specified ticks. Defaults to `None`, which means, that the default axis ticks are used.
		Both `x_tick_pos` and `x_tick_labels` need to be specified and of the same length for this to take effect.
	\param y_tick_pos Postions, where ticks should appear. Defaults to `None`, which means, that the default axis ticks are used.
		Both `y_tick_pos` and `y_tick_labels` need to be specified and of the same length for this to take effect.
	\param y_tick_labels Labels for the manually specified ticks. Defaults to `None`, which means, that the default axis ticks are used.
		Both `y_tick_pos` and `y_tick_labels` need to be specified and of the same length for this to take effect.
	\param show_legend Switch, whether the legend should be shown. Defaults to `True`.
	\param pltrcParams Dictionary of settings to be passed to `plt.rcParams`.
	\param pltsettings Dictionary of settings that will be applied to every graph in `record_list`.
	\param file See \ref show_save_fig().
	\param show See \ref show_save_fig().
	\param closeafter See \ref show_save_fig().
	\param fig `matplotlib.figure.Figure`, if `fig` or `ax` is `None` (default), a fresh one is generated.
	\param ax `matplotlib.axes.Axes`, if `fig` or `ax` is `None` (default), a fresh one is generated.
	\param *args Positional arguments, will be ignored.
	\param *kwargs Keyword arguments, will be ignored.
	
	The hierarchy in settings is in ascending (latest takes precedence over previous ones): `brplotviz` default style -> `pltrcParams`-> `pltsettings` -> `graphsettings`.
	
	\return Returns the the figure and the axis objects: `fig, ax`.
	"""
	pltrcParams = pltrcParams if pltrcParams is not None else {}
	pltsettings = pltsettings if pltsettings is not None else {}
	# show_legend = show_legend if show_legend is not None else (record_names is not None)
	# record_names = record_names if record_names is not None else [ "Record {}".format(i) for i in range(1, len(x_table)+1) ]
	fig, ax = get_figure(fig, ax, **pltrcParams)
	# Draw the mixed_graphs
	for i, (x_record, y_record, style, graphsettings) in enumerate(record_list):
		if len(x_record) != len(y_record):
			raise ValueError("Number of x-data ({}) != Number of y-data ({}) for record {}".format(len(x_record), len(y_record), i))
		if style == "line":
			settings = next(ax.line_style)
		elif style == "scatter":
			settings = next(ax.scatter_style)
		else:
			raise ValueError("Option '{}' is not known for plotting in record {}.".format(style, i))
		settings.update(pltsettings)
		settings.update(graphsettings)
		ax.plot(x_record, y_record, **settings)
	# Appearance
	if x_tick_pos is not None and x_tick_labels is not None:
		ax.set_xticks(ticks=x_tick_pos, labels=x_tick_labels)
	if y_tick_pos is not None and y_tick_labels is not None:
		ax.set_yticks(ticks=y_tick_pos, labels=y_tick_labels)
	if xlabel is not None:
		ax.set_xlabel(xlabel)
	if ylabel is not None:
		ax.set_ylabel(ylabel)
	if show_legend:
		ax.legend(loc="best")
	show_save_fig(fig, file=file, closeafter=closeafter, show=show)
	return fig, ax

def bar_variable(bins: list,
				y_values: tuple,
				pltrcParams: dict = None,
				file: str = None,
				closeafter: bool = True,
				show: bool = None,
				fig = None,
				ax = None,
				):
	"""
	Plots a bar plot with a variable number of bins.
	\todo Is it really necessary to be able use a variable number of bars per bin?
	\param bins Names of data classes e.g. `["a", "b", "c"]`.
	\param y_values List of lists. For each entry in `classes` there should be list of y_values. e.g. [[1],[2,3],[4,5,6,7]]
		They are grouped around symmetrically around the position of the class location.
	\param pltrcParams Dictionary of settings to be passed to `plt.rcParams`.
	\param file See \ref show_save_fig().
	\param show See \ref show_save_fig().
	\param closeafter See \ref show_save_fig().
	\param fig `matplotlib.figure.Figure`, if `fig` or `ax` is `None` (default), a fresh one is generated.
	\param ax `matplotlib.axes.Axes`, if `fig` or `ax` is `None` (default), a fresh one is generated.
	\return Returns the the figure and the axis objects: `fig, ax`.
	"""
	pltrcParams = pltrcParams if pltrcParams is not None else {}
	fig, ax = get_figure(fig, ax, **pltrcParams)
	plot_style = styleselect.get_plot_style_hatch()
	hatch_list = list(plot_style)
	if len(y_values) > len(hatch_list):
		warnings.warn("Warning: too many records, some will not be printed")
	width = .5					# width of the bars
	bin_position_array = np.arange(len(bins))	# position of the bin centers
	for bin_pos, y_list in enumerate(bin_position_array, y_values):
		n_bars = len(y_list)
		d_x = width/n_bars
		pos_x = bin_pos - width/2 + d_x/2
		for j, h in enumerate(y_list):
			ax.bar(x=pos_x + j * d_x, height=h, width=d_x, **hatch_list[j])
	ax.set_xticks(ticks=bin_position_array, labels=bins, rotation=45)
	ax.legend(loc="best")
	show_save_fig(fig, file=file, closeafter=closeafter, show=show)
	return fig, ax

def bar_categories(record_list: list,
				category_names: list = None,
				record_names: list = None,
				xlabel: str = None,
				ylabel: str = None,
				show_legend: bool = None,
				pltrcParams: dict = None,
				file: str = None,
				show: bool = None,
				closeafter: bool = True,
				fig = None,
				ax = None,
				*args, **kwargs):
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
	\param pltrcParams Dictionary of settings to be passed to `plt.rcParams`.
	\param file See \ref show_save_fig().
	\param show See \ref show_save_fig().
	\param closeafter See \ref show_save_fig().
	\param fig `matplotlib.figure.Figure`, if `fig` or `ax` is `None` (default), a fresh one is generated.
	\param ax `matplotlib.axes.Axes`, if `fig` or `ax` is `None` (default), a fresh one is generated.
	\param *args Positional arguments, will be ignored.
	\param *kwargs Keyword arguments, will be ignored.
	\return Returns the the figure and the axis objects: `fig, ax`.
	"""
	# Setup: set, if the legend should be shown or not, set default labels for categories and records
	pltrcParams = pltrcParams if pltrcParams is not None else {}
	show_legend = show_legend if show_legend is not None else (record_names is not None)
	category_names = category_names if category_names is not None else [ "Category {}".format(i) for i in range(1, len(record_list[0]) + 1) ]
	record_names = record_names if record_names is not None else [ "Record {}".format(i) for i in range(1, len(record_list) + 1) ]
	if len(record_list) != len(record_names):
			raise ValueError("Number of records ({}) != Number of record names ({})".format(len(record_list), len(record_names)))
	
	fig, ax = get_figure(fig, ax, **pltrcParams)
	width = .8					# width of the bars
	n_bars = len(record_list)
	d_x = width/n_bars
	bin_position_array = np.arange(len(category_names))	# position of the bin centers
	bin_separation_array = bin_position_array[:-1] + 0.5
	for i, (heights, record_name) in enumerate(zip(record_list, record_names)):
		if len(heights) != len(category_names):
			raise ValueError("Number of y-values ({}) != Number of category names ({}) for record {}".format(len(heights), len(category_names), i))
		# Sanitize None entries
		heights = [entry if entry is not None else 0 for entry in heights]
		pos_x = bin_position_array - width/2 + d_x/2 + i * d_x
		ax.bar(x=pos_x, height=heights, width=d_x, label=record_name, **next(ax.hatch_style))
	# Appearance
	ax.set_xticks(ticks=bin_separation_array, labels=[""] * len(bin_separation_array), minor=False)
	ax.set_xticks(ticks=bin_position_array, labels=category_names, rotation=90, minor=True)
	ax.set_xlim(bin_separation_array[0] - 1, bin_separation_array[-1] + 1)
	if xlabel is not None:
		ax.set_xlabel(xlabel)
	if ylabel is not None:
		ax.set_ylabel(ylabel)
	if show_legend:
		ax.legend(loc="best")
	show_save_fig(fig, file=file, closeafter=closeafter, show=show)
	return fig, ax

def matrix_plot(matrix: list,
				xlabel: str = None,
				ylabel: str = None,
				colorbar_label: list = None,
				x_tick_pos: list = None,
				x_tick_labels: list = None,
				y_tick_pos: list = None,
				y_tick_labels: list = None,
				show_legend: bool = False,
				pltrcParams: dict = None,
				pltsettings: dict = None,
				file: str = None,
				closeafter: bool = True,
				show: bool = None,
				fig = None,
				ax = None,
				*args, **kwargs):
	"""
	This function visualizes a matrix, coloring the cells according to the value along with a colorbar.
	\param matrix An array like (e.g. list of lists), that will be shown. 
	\param xlabel Description of the x-axis. Defaults to `None`.
	\param ylabel Description of the y-axis. Defaults to `None`.
	\param colorbar_label Description of the colorbar (data range shown by the matrix).
	\param x_tick_pos Postions, where ticks should appear. Defaults to `None`, which means, that the default axis ticks are used.
		Both `x_tick_pos` and `x_tick_labels` need to be specified and of the same length for this to take effect.
	\param x_tick_labels Labels for the manually specified ticks. Defaults to `None`, which means, that the default axis ticks are used.
		Both `x_tick_pos` and `x_tick_labels` need to be specified and of the same length for this to take effect.
	\param y_tick_pos Postions, where ticks should appear. Defaults to `None`, which means, that the default axis ticks are used.
		Both `y_tick_pos` and `y_tick_labels` need to be specified and of the same length for this to take effect.
	\param y_tick_labels Labels for the manually specified ticks. Defaults to `None`, which means, that the default axis ticks are used.
		Both `y_tick_pos` and `y_tick_labels` need to be specified and of the same length for this to take effect.
	\param show_legend Switch, whether the legend should be shown. Defaults to `False`.
	\param pltrcParams Dictionary of settings to be passed to `plt.rcParams`.
	\param pltsettings Dictionary of settings that will be applied to the matrix.
		Defaults to `{"cmap": "viridis_r"}`.
	\param file See \ref show_save_fig().
	\param show See \ref show_save_fig().
	\param closeafter See \ref show_save_fig().
	\param fig `matplotlib.figure.Figure`, if `fig` or `ax` is `None` (default), a fresh one is generated.
	\param ax `matplotlib.axes.Axes`, if `fig` or `ax` is `None` (default), a fresh one is generated.
	\param *args Positional arguments, will be ignored.
	\param *kwargs Keyword arguments, will be ignored.
	\return Returns the the figure and the axis objects: `fig, ax`.
	"""
	pltrcParams = pltrcParams if pltrcParams is not None else {}
	pltsettings_tmp = pltsettings if pltsettings is not None else {}
	pltsettings = {"cmap": "viridis_r"}
	pltsettings.update(pltsettings_tmp)
	fig, ax = get_figure(fig, ax, **pltrcParams)
	mat = ax.matshow(matrix, **pltsettings)
	divider = make_axes_locatable(ax)
	cax = divider.append_axes("right", size="5%", pad=0.1)
	cbar = fig.colorbar(mat, cax=cax, label=colorbar_label)
	# Appearance
	if x_tick_pos is not None and x_tick_labels is not None:
		ax.set_xticks(ticks=x_tick_pos, labels=x_tick_labels, rotation=90)
	if y_tick_pos is not None and y_tick_labels is not None:
		ax.set_yticks(ticks=y_tick_pos, labels=y_tick_labels)
	if xlabel is not None:
		ax.set_xlabel(xlabel)
	if ylabel is not None:
		ax.set_ylabel(ylabel)
	if show_legend:
		ax.legend(loc="best")
	show_save_fig(fig, file=file, closeafter=closeafter, show=show)
	return fig, ax

def get_figure(fig = None, ax = None, **pltrcParams):
	"""
	Generate the figure and axes objects and apply the general setting using \ref set_plot_style_fig().
	\param fig `matplotlib.figure.Figure`, if `fig` or `ax` is `None` (default), a fresh one is generated.
	\param ax `matplotlib.axes.Axes`, if `fig` or `ax` is `None` (default), a fresh one is generated.
	\param pltrcParams Dictionary of settings to be passed to `plt.rcParams`.
	\return `fig, ax` Figure and Axis object.
	The `ax` object is assigned three additional attributes:
		- `ax.line_style`: This style is used, when a line plot is done, see \ref single_line(), \ref multi_line() or `style=line` is passed to \ref mixed_graphs().
		- `ax.scatter_style`: This style is used, when a scatter plot is done, see \ref single_scatter(), \ref multi_scatter() or `style=scatter` is passed to \ref mixed_graphs().
		- `ax.hatch_style`: This style is used, when a bar plot is done, see \ref bar_categories().
	
	If it is desired to add plots afterwards, use the following snippets:
	- `ax.plot(x, y, label=<name>, **next(ax.line_style))` for a line plot
	- `ax.plot(x, y, label=<name>, **next(ax.scatter_style))` for a scatter plot
	"""
	styleselect.set_plot_style_fig(**pltrcParams)
	if fig is None or ax is None:
		fig, ax = plt.subplots()
	ax.grid(True)
	ax.set_axisbelow(True)
	ax.line_style = styleselect.get_plot_style_line()()
	ax.scatter_style = styleselect.get_plot_style_scatter()()
	ax.hatch_style = styleselect.get_plot_style_hatch()()
	return fig, ax

def show_save_fig(fig,
				file: str = None,
				show: bool = None,
				closeafter: bool = True,
				):
	"""
	Shows or saves the figure.
	\param fig Figure to be shown or saved.
	\param file Path to the file in which the graph is saved.
		Defaults to `None`, which means the graph is shown on screen instead of saved to disk.
		If a valid path is given, the graph is saved to this file.
		The content of the file is overwritten without further questions.
	\param show Switch, whether the figure should be shown on screen.
		By default (`None`), it is only shown, if no file is provided (`file is None`). 
	\param closeafter Switch, whether the figure should be closed after showing or saving. Defaults to `True`.
	"""
	show = show if show is not None else (file is None)
	fig.tight_layout()
	if file is not None:
		file = os.path.join(os.getcwd(), file)
		try:
			if not os.path.exists(os.path.dirname(file)):
				os.makedirs(os.path.dirname(file))
			fig.savefig(file, bbox_inches='tight')
		except:
			print('Failed to save plot to file "{}"'.format(file))
	if show:
		# use `plt.show()` for staying open figure_handling the window is closed. It manages the event loop, which `fig.show()` does not.
		# `fig.show()` does not block and closes imediately, if not in an interactive mode.
		# For more, see https://matplotlib.org/stable/api/figure_api.html#matplotlib.figure.Figure.show  
		plt.show(block=True)
	# close the current figure, cleans the memory.
	if closeafter:
		plt.close(fig)

if __name__ == "__main__":
	pass
