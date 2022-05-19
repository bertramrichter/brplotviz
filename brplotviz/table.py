
## \file
## Contains table printing function
## \author Bertram Richter
## \package table \copydoc table.py

def print_table(table: list,
					head_row: list = None,
					head_col: list = None,
					top_left: str = "",
					itemsep: str = "\t",
					lineend: str = "",
					title: str  = None,
					file: str = None,
					formatter = None,
					):
	"""
	Prints the table in a nice format.
	\param table List of lists (array-like, but can have different data types).
	\param head_row List of column heads, if specified, printed before the rest of the table.
	\param head_col This is put infront of the rows, if not left `None` (default).
	\param top_left This is put in the top-left cell, if both `head_row` and `head_col` are provided. Defaults to `""`.
	\param itemsep String, that is put in-between items of the same line. Defaults to `"\t"`.
	\param lineend String that is put at the end of the line. Defaults to `""`.
	\param title Title of the table. Will be printed on a separate line directly above the table, if not `None` (default).
	\param file Path to the file in which the table is written to. Defaults to `None`, which means the table is printed on screen instead of saved to disk.
		If a valid path is given, the tables is written to this file. Overwrites the content of the file without further questions.
	\param formatter Format options. This is flexible with the following options:
		- `None` (default) No formatting is done and all entries are printed, as Python does by default.
		- String according to the Format Specification Mini-Language: The specified format is applied to all cells.
		- List of format strings: The formatting is assumed to be applicable to all rows.
		- List of list of format strings: It is assumed, that each cell is provided with an individual format string.
	
	The layout with both `head_row` and `head_col` specified will be:
	| `top_left`	| `head_row 0`	| `head_row 1`	|
	|:---			| :---:			| :---:			|
	| `head_col 0`	| `0,0`			| `0,1`			|
	| `head_col 1`	| `1,0`			| `1,1`			|
	
	Without `head_col`:
	| `head_row 0`	| `head_row 1`	|
	|:---			| :---:			|
	| `0,0`			| `0,1`			|
	| `1,0`			| `1,1`			|
	
	Without `head_row`:
	|				|		|		|
	| :---			| :---:	| :---:	|
	| `head_col 0`	| `0,0`	| `0,1`	|
	| `head_col 1`	| `1,0`	| `1,1`	|
	"""
	# Get the formatter table
	format_table = _get_formatter_table(formatter, table)
	# Format table head
	formatted_lines = []
	if title is not None:
		formatted_lines.append("{}".format(title))
	if head_row is not None:
		formatted_line = "{}".format(top_left)
		formatted_line += "{}".format(itemsep)
		for col_num, item in enumerate(head_row):
			formatted_line += "{}".format(item)
			if col_num == len(head_row)-1:
				formatted_line += "{}".format(lineend)
			else:
				formatted_line += "{}".format(itemsep)
		formatted_lines.append(formatted_line)
	# Format table body
	for row_num, (row, row_format) in enumerate(zip(table, format_table)):
		formatted_line = ""
		if head_col is not None:
			formatted_line = "{}{}".format(head_col[row_num], itemsep)
		for col_num, (entry, entry_format) in enumerate(zip(row, row_format)):
			formatted_line += "{}".format("{"+entry_format+"}").format(entry)
			if col_num == len(row)-1:
				formatted_line += "{}".format(lineend)
			else:
				formatted_line += "{}".format(itemsep)
		formatted_lines.append(formatted_line)
	# Output
	if file is None:
		for line in formatted_lines:
			print(line)
	else:
		with open(file, "w") as f:
			for line in formatted_lines:
				f.writelines(line + "\n")

def _get_formatter_table(formatter, table):
	"""
	Get the table of formatting strings.
	\param formatter Format options. This is flexible with the following options:
		- `None` (default) No formatting is done and all entries are printed, as Python does by default.
		- String according to the Format Specification Mini-Language: The specified format is applied to all cells.
		- List of format strings: The formatting is assumed to be applicable to all rows.
		- List of list of format strings: It is assumed, that each cell is provided with an individual format string.
	\param table The table, for which the formatting is to generated.
	"""
	if formatter is None:
		# Assume no formatting
		formatter = ""
	if isinstance(formatter, list):
		if isinstance(formatter[0], list):
			# Assume per-cell formatting
			return formatter
		else:
			# Assume per-row formatting
			return [formatter for row in table]
	elif isinstance(formatter, str):
		# Assume same formatting for each cell
		return [[formatter]*len(row) for row in table]
	else:
		raise ValueError("Please provide a string with a Format Specification Mini-Language!")

if __name__ == "__main__":
	pass
