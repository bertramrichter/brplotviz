
"""
Contains settings 
\todo 

\author Bertram Richter
\date 2024
"""

from .rules import *

class Engine():
	"""
	\todo
	"""
	def __init__(self,
			linestart: str,
			firstsep: str,
			itemsep: str,
			lineend: str,
			pad_left: str = "",
			pad_right: str = "",
			):
		self.linestart = linestart
		self.firstsep = firstsep
		self.itemsep = itemsep
		self.lineend = lineend
		self.pad_left = pad_left
		self.pad_right = pad_right
	def rule(self, widths: list, align: list, rule_type: str):
		"""
		\todo
		\param w List of `int` containing the column widths.
		\param align List of `str` containing the column alignments.
		\param rule_type \ref Rule object which indicates, which rule is used.
		"""
		return None
	def row(self, row: list):
		"""
		\todo
		"""
		line = self.linestart + self.pad_right \
			+ row[0] \
			+ self.pad_left + self.firstsep + self.pad_right \
			+ (self.pad_left + self.itemsep + self.pad_right).join(row[1::]) \
			+ self.pad_left + self.lineend
		return line
	def modify_col_widths(self, col_widths, align):
		return col_widths

class csv(Engine):
	"""
	Character separated table.
	Default is the 
	"""
	def __init__(self, itemsep: str = ",", **kwargs):
		super().__init__(
			linestart = "",
			firstsep = itemsep,
			itemsep = itemsep,
			lineend = "",
			**kwargs)
	def rule(self, widths: list, align: str, rule_type: str):
		"""
		\todo
		"""
		if isinstance(rule_type, ExtraRule):
			return ""
		else:
			return None

class tsv(csv):
	"""
	\todo
	"""
	def __init__(self, itemsep: str = "\t", **kwargs):
		super().__init__(itemsep, **kwargs)

class latex(Engine):
	"""
	\todo
	"""
	def __init__(self, **kwargs):
		"""
		\todo
		"""
		super().__init__(linestart="",
			firstsep="&",
			itemsep="&",
			lineend=r"\\",
			**kwargs)
	def rule(self, widths: list, align: list, rule_type: str):
		"""
		\todo
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
	def __init__(self, **kwargs):
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
			for w, alignment in zip(widths, align):
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
