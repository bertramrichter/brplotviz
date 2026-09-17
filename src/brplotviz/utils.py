
r"""
Contains some useful standalone functions.

\author Bertram Richter
\date 2026
"""


import matplotlib


def blend_colors_by_transparency(fg, bg, alpha: float) -> tuple:
	r"""
	Calculate the equivalent RGB value of a translucent color against a solid colored background.
	All color formats supported by matplotlib are supported, see https://matplotlib.org/stable/users/explain/colors/colors.html#colors-def
	\param fg Foreground color.
	\param bg Background color.
	\param alpha Transparency of the foreground colorin the range of 0 (fully transparent) to 1 (fully opaque).
	\return Returns the numerical RGB representation of the resulting color (3-tuple of float values).
	"""
	fg = matplotlib.colors.to_rgb(fg)
	bg = matplotlib.colors.to_rgb(bg)
	return tuple(alpha * cf + (1 - alpha) * cb for (cf, cb) in zip(fg, bg))


if __name__ == "__main__":
	pass