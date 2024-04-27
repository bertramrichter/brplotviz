
"""
Generate an overview over all available table styles.

\author Bertram Richter
\date 2024
"""

from brplotviz import table
from brplotviz.table.rules import ExtraRule
from brplotviz.table import print_table_LaTeX

table_data = [
	["a",123.456, 12],
	["bc\nde", 23.34, 345],
	["and f", 45.],
	]

head_row = ["Col 1", "Col 2", "Col 3"]
head_col = ["Row 1", "Row 2", "Row 3"]
top_left = "Top left"
align = ["l", "c", "r", "r"]

preface ="""
# Table engine overview

This document contains an overview over the available table styles.
Note, that the engine selection is case-insensitive.

"""

file_content=[
	preface
	]

styles = [
	"csv",
	"tsv",
	"latex",
	"markdown",
	"test"
	]
for style in styles:
	file_content.append("`{}`".format(style))
	file_content.append("")
	file_content.append("```")
	formatted = table.print_table(table=table_data,
					style=style,
					head_col="enumerate",
					head_row=head_row,
					top_left=top_left,
					formatter=["", ":.2f", ":.1f"],
					align=align,
					show=False,
					#transpose_data=True,
					return_lines=True)
	file_content.extend(formatted)
	file_content.append("```")
	file_content.append("")
	
table._output_table(
	formatted_lines=file_content,
	file=None,
	#file="./style_overview.md",
	show=True)

print("Full LaTeX table environment\n")
table.print_table_LaTeX(
	table=table_data,
	caption="This is the caption",
	LaTeX_label="example",
	)
