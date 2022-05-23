
## \file
## Contains functions for setting the plot style.
## \author Bertram Richter
## \package styleselect \copydoc styleselect.py

from cycler import cycler, concat
from matplotlib import pyplot as plt

def set_plot_style_fig(**pltsettings):
	"""
	Set the general style for the background and grid.
	\param **pltsettings Dictionary of settings to be passed to `plt.rcParams`.
	"""
	settings = {"svg.fonttype": "none", "font.size": 10}
	settings.update(pltsettings)
	plt.rcParams.update(settings)

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

if __name__ == "__main__":
	pass
