"""
Contains settings for 

\author Bertram Richter
\date 2024
"""

class Rule():
	pass
class TopRule(Rule):
	pass
class HeadRule(Rule):
	pass
class MidRule(Rule):
	pass
class ExtraRule(Rule):
	pass
class BotRule(Rule):
	pass

class Engine():
	"""
	\todo
	"""
	def __init__(self,
			linestart,
			firstsep,
			itemsep,
			lineend
			):
		self.linestart = linestart
		self.firstsep = firstsep
		self.itemsep = itemsep
		self.lineend = lineend
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
		return self.linestart + row[0] + self.firstsep + self.itemsep.join(row[1::]) + self.lineend

class csv(Engine):
	"""
	Character separated table.
	Default is the 
	"""
	def __init__(self, itemsep: str = ",",):
		super().__init__(
			linestart = "",
			firstsep = itemsep,
			itemsep = itemsep,
			lineend = "",
			)
	def rule(self, widths: list, align: str, rule_type: str):
		"""
		\todo
		"""
		if isinstance(rule_type, ExtraRule):
			return ""
		else:
			return None

class tsv(csv):
	def __init__(self, itemsep: str = "\t",):
		super().__init__(itemsep)

class latex(Engine):
	def __init__(self):
		super().__init__(linestart="",
			firstsep="&",
			itemsep="&",
			lineend=r"\\")
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
	def __init__(self):
		super().__init__(
			linestart = "|",
			firstsep = "|",
			itemsep = "|",
			lineend = "|",
			)
		self.rulestart = "|"
		self.firstrulesep = "|"
		self.rulesep = "|"
		self.ruleend = "|"
	def rule(self, widths: list, align: str, rule_type: str):
		"""
		\todo
		"""
		if isinstance(rule_type, HeadRule):
			rule = []
			for w, alignment in zip(widths, align):
				if alignment == "l": 
					rule.append(":" + "-"*max(3, w-1))
				elif alignment == "c": 
					rule.append(":" + "-"*max(3, w-2) + ":")
				elif alignment == "r": 
					rule.append("-"*max(3, w-1) + ":")
			return self.row(rule)

#class custom(Engine):
#	def __init__(self, row_sep):
#		self.row_sep = row_sep
#	def rule(self, w: list, align: str, rule_type: str):
#		"""
#		\todo
#		"""
#		if isinstance(rule_type, ExtraRule):
#			return ""
#		else:
#			return None

def typeset(table, engine):
	row_count = len(table)
	widths=[len(str(i)) for i in table[0]]
	align=["l"]*len(table[0])
	prepared = [TopRule()]
	prepared.append(table[0])
	prepared.append(HeadRule())
	for row_nr, row in enumerate(table[1::]):
		prepared.append(row)
		if not isinstance(row, Rule) or not row_nr == row_count-1:
			prepared.append(MidRule())
	prepared.append(BotRule())
	for row in prepared:
		if not isinstance(row, Rule):
			formatted = engine.row(row)
		else:
			formatted = engine.rule(
				widths=widths,
				align=align,
				rule_type=row)
		if formatted is not None:
				print(formatted)
	