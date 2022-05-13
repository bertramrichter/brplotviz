
## \file
## Contains functions for setting the plot style.
## \author Bertram Richter
## \package styleselect \copydoc styleselect.py

from cycler import cycler, concat
from matplotlib import pyplot as plt

def set_custom_style(style: dict) -> None:
	"""
	This function copies the entries of the given dictionary to the `matplotlib` configuration.
	"""
	for entry in style:
		plt.rcParams[entry] = style[entry]

def set_plot_style_fig():
	"""
	Set the general style for the background and grid.
	"""
	plt.rcParams['svg.fonttype'] = 'none'
	plt.rcParams['font.size'] = '10'

def get_plot_style_line():
	"""
	Set the style for line plots.
	"""
	color = cycler('color', ["black", "gray"])
	linestyle = cycler('linestyle', ['-', '--', '-.', ':'])
	plot_style = color * linestyle
	return plot_style

def get_plot_style_scatter():
	"""
	Set the style for scatter plots.
	"""
	color = cycler('color', ["black"])
	linestyle = cycler("linestyle", [""])
	marker = cycler('marker', ["o", "+", "x", 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd', 'P', 'X'])
	plot_style = color * linestyle * marker
	return plot_style

def get_plot_style_hatch():
	"""
	Set the style for bar plots.
	"""
	edgecolor = cycler("edgecolor", ["k"])
	mono_fill = edgecolor * cycler('hatch', [""]) * cycler('color', ['w', "tab:gray","k"])
	mono_hatches = cycler('color', ['w', "tab:grey"]) * edgecolor * cycler('hatch', ['///', "\\\\\\", 'xxx', '--', '...','\///', "++", "o", "++.", ".o"])
	plot_style = concat(mono_fill, mono_hatches)
	return plot_style

