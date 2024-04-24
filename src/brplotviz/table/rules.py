
r"""
Contains the class definition for the table rules (horizontal lines).
The rule objects themselves do nothing, but are used for signalling.

\author Bertram Richter
\date 2024
"""


class Rule():
	r"""
	Base class for all rules.
	"""
	## The priority value indicates, how important a rule type is, the
	## lower, the more important.
	## The priority is used as indicator, which line to keep if two (or
	## more) rules directly follow each other.
	## The most important rule is kept.
	priority = None

class TopRule(Rule):
	r"""
	The toprule is the rule above the tabular data.
	Above that, only the table's caption is printed.
	Hence, the top rule opens the table.
	A top rule is placed automatically during the typesetting.
	"""
	priority = 0

class BotRule(Rule):
	r"""
	The bottom rule is the rule below the table's body.
	Hence, bottom rule closes the table. 
	A bottom rule is placed automatically during the typesetting.
	"""
	priority = 1

class NoRule(Rule):
	r"""
	This rule prevents the engine to draw a rule.
	The use case is for multi-line cells.
	NoRules can be placed by manually or are used automatically, when
	mulit-line cells are encountered. 
	"""
	priority = 2

class HeadRule(Rule):
	r"""
	The head rule separates the table header row from the table's body.
	A head rule is placed automatically during the typesetting.
	"""
	priority = 3

class ExtraRule(Rule):
	r"""
	An extra rule can be placed between two rows to sep them further apart.
	This is the only rule, a user might sparingly place into the table.
	"""
	priority = 4

class MidRule(Rule):
	r"""
	Mid rules ared place between each row in the table's body.
	Most table styles do not actually draw them.
	Mid rules are placed automatically during the typesetting.
	"""
	priority = 5

