
"""
This module contains the class definitions for table engines, each of
which in turn define the look of the table.

\author Bertram Richter
\date 2024
"""

import itertools
from .rules import *

class Engine():
	"""
	Base class for a table engine.
	An engine simply stores the style and look of the table, that is the
	how the rows and columns are separated and how the frame around the
	tabular data looks like.
	For defining a custom table look, implement it as subclass to this one.
	"""
	def __init__(self,
			linestart: str,
			firstsep: str,
			itemsep: str,
			lineend: str,
			pad_left: str = "",
			pad_right: str = "",
			*args, **kwargs):
		"""
		Construct the engine object.
		\param linestart \copydoc linestart
		\param firstsep \copydoc firstsep
		\param itemsep \copydoc itemsep
		\param lineend \copydoc lineend
		\param pad_left \copydoc pad_left
		\param pad_right \copydoc pad_right
		\param *args Additional positional arguments, ignored.
		\param **kwargs Additional keyword arguments, ignored.
		"""
		## Each line is prepended with this.
		self.linestart = linestart
		## Separator between the first (head) column and second column.
		self.firstsep = firstsep
		## Column separator between all normal columns.
		self.itemsep = itemsep
		## This is appended to the end of each line.
		self.lineend = lineend
		## This in each cell put between the content and the \ref itemsep to the left. 
		self.pad_left = pad_left
		## This in each cell put between the content and the \ref itemsep to the right. 
		self.pad_right = pad_right
	def rule(self, widths: list, align: list, rule_type: Rule) -> str:
		"""
		Return a `str` looking like the table rule, based on the type (\ref rules).
		`None` is returned if no rule should be drawn. 
		\param widths List of `int` containing the column widths.
		\param align List of `str` containing the column alignments.
		\param rule_type \ref rules.Rule object which indicates, which rule is used.
		"""
		return None
	def row(self, row: list) -> str:
		"""
		Assemble the row from the already formatted and aligned cell
		contents are interwoven with the column separators and the final,
		formatted table line ready to print is returned.
		\param row List of `str`, which are the already converted and aligned.
		"""
		line = self.linestart + self.pad_right \
			+ row[0] \
			+ self.pad_left + self.firstsep + self.pad_right \
			+ (self.pad_left + self.itemsep + self.pad_right).join(row[1::]) \
			+ self.pad_left + self.lineend
		return line
	def modify_col_widths(self, col_widths: list, align: list):
		"""
		This method is used to modify the determined column widths, as
		some engines require a minimum column width (e.g., \ref markdown).
		But most engines will just return the list of column widths.
		\param col_widths List of `int`, which are the column widths in charaters.
		\param align List of `str`, specifying the aligment of each column.
		"""
		return col_widths

class csv(Engine):
	"""
	Character separated table, defaulting to the comma (`","`).
	
	This engine has no built table rules.
	The \ref rules.ExtraRule is used to insert a blank line.
	
	Start th 
	"""
	def __init__(self, itemsep: str = ",", **kwargs):
		"""
		Construct the csv engine.
		\param itemsep \copydoc itemsep
			This defaults to the comma (`","`).
		\param kwargs Additional keyword arguments, passed to the
			superclass' constructor.
		"""
		super().__init__(
			linestart = "",
			firstsep = itemsep,
			itemsep = itemsep,
			lineend = "",
			**kwargs)
	def rule(self, widths: list, align: str, rule_type: str):
		"""
		\copydoc Engine.rule()
		
		This engine has no built table rules.
		The \ref rules.ExtraRule is used to insert a blank line. 
		"""
		if isinstance(rule_type, ExtraRule):
			return ""
		else:
			return None

class tsv(csv):
	"""
	A variation of the \ref csv, but with the tab (`"\t"`) as column separator.
	
	\copydetails csv
	"""
	def __init__(self, itemsep: str = "\t", **kwargs):
		"""
		Construct the tsv engine.
		\param itemsep \copydoc itemsep
			This defaults to the tab (`"\t"`).
		\param kwargs Additional keyword arguments, passed to the
			superclass' constructor.
		"""
		super().__init__(itemsep, **kwargs)

class latex(Engine):
	"""
	A LaTeX table, columns are separated by the ampersand (`"&"`) and the
	the lines are ended with double backslash (`"\\"`).
	
	The table rules use the rules provided by [booktabs](https://ctan.org/pkg/booktabs/).
	Before the tabular part, the table is started with `"\topule"`, the
	header line is separated by `"\midrule"` and the tabular part is
	closed with `"\bottomrule"`.
	The \ref rules.ExtraRule is translated into `"\addlinespace"`, which
	results in a small vertical space between two rows.
	"""
	def __init__(self, **kwargs):
		"""
		Construct the latex engine.
		"""
		super().__init__(linestart="",
			firstsep="&",
			itemsep="&",
			lineend=r"\\",
			**kwargs)
	def rule(self, widths: list, align: list, rule_type: str):
		"""
		\copydoc Engine.rule()
		
		The table rules use the rules provided by[booktabs](https://ctan.org/pkg/booktabs/).
		Before the tabular part, the table is started with `"\topule"`,
		the header line is separated by `"\midrule"` and the tabular part
		is closed with `"\bottomrule"`.
		The \ref rules.ExtraRule is translated into `"\addlinespace"`,
		which results in a small vertical space between two rows.
		"""
		if isinstance(rule_type, TopRule):
			return r"\toprule"
		elif isinstance(rule_type, HeadRule):
			return r"\midrule"
		elif isinstance(rule_type, BotRule):
			return r"\bottomrule"
		elif isinstance(rule_type, ExtraRule):
			return r"\addlinespace"
		else:
			return None

class markdown(Engine):
	"""
	A Markdown table.
	"""
	def __init__(self, **kwargs):
		"""
		\todo
		"""
		super().__init__(
			linestart = "|",
			firstsep = "|",
			itemsep = "|",
			lineend = "|",
			**kwargs
			)
		self.rulestart = "|",
		self.firstrulesep = "|",
		self.rulesep = "|",
		self.ruleend = "|",
	def rule(self, widths: list, align: str, rule_type: str):
		"""
		\todo
		"""
		if isinstance(rule_type, HeadRule):
			if align is None or isinstance(align, str):
				align = [align] * len(widths)
			rule = []
			for w, alignment in itertools.zip_longest(widths, align, fillvalue=""):
				if alignment is None:
					rule.append("-"*max(3, w))
				if alignment == "l": 
					rule.append(":" + "-"*max(3, w-1))
				elif alignment == "c": 
					rule.append(":" + "-"*max(3, w-2) + ":")
				elif alignment == "r": 
					rule.append("-"*max(3, w-1) + ":")
			return self.row(rule)
	def modify_col_widths(self, col_widths, align):
		"""
		\todo Document
		"""
		if align is None or isinstance(align, str):
			align = [align] * len(col_widths)
		new_col_widths = []
		for w, alignment in zip(col_widths, align):
			if alignment is None:
				new_col_widths.append(max(3, w))
			elif alignment == "c": 
				new_col_widths.append(max(5, w))
			else: 
				new_col_widths.append(max(4, w))
		return new_col_widths
