
"""
Generate an overview over all available table styles.

\author Bertram Richter
\date 2024
"""

from brplotviz import table
from brplotviz.table.rules import ExtraRule

table_data = [
	["a",123.4, 12],
	["bc", 23, 345],
	ExtraRule,
	["def"],
	]

head_row = ["Col 1", "Col 2", "Col 3"]
head_col = ["Row 1", "Row 2", "Row 3"]
top_left = "Top left"
align = ["l", "c", "r"]

preface ="""
# Table engine overview

This document contains an overview over the available table styles.
Note, that the engine selection is case-insensitive.

"""

file_content=[
	preface
	]

engines = [
	"CSV",
	"TSV",
	"LaTex",
	"Markdown",
	]
for engine in engines:
	file_content.append("{}:".format(engine))
	file_content.append("")
	file_content.append("```")
	formatted = table.print_table(table=table_data,
					engine=engine,
					head_col=head_col,
					head_row=head_row,
					top_left=top_left,
					align=align,
					show=False,
					transpose_data=True,
					return_lines=True)
	file_content.extend(formatted)
	file_content.append("```")
	file_content.append("")
	
table._output_table(
	formatted_lines=file_content,
	file="./doc/engine_overview.md",
	show=True)
