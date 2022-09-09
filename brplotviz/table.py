
## \file
## Contains table printing functionalities.
## \author Bertram Richter
## \date 2022
## \package brplotviz.table \copydoc table.py

import codecs
import os

def print_table(table: list,
					head_row: list = None,
					head_col: list = None,
					top_left: str = "",
					itemsep: str = "\t",
					lineend: str = "",
					caption: str = None,
					formatter = None,
					head_sep: str = None,
					transpose_data: bool = False,
					file: str = None,
					show: bool = None,
					*args, **kwargs) -> list:
	"""
	Prints the table in a nice format.
	\param table List of lists (array-like, but can have different data types).
	\param head_row List of column heads, if specified, printed before the rest of the table.
	\param head_col This is put infront of the rows, if not left `None` (default).
	\param top_left This is put in the top-left cell, if both `head_row` and `head_col` are provided. Defaults to `""`.
	\param itemsep String, that is put in-between items of the same line. Defaults to `"\t"`.
	\param lineend String that is put at the end of the line. Defaults to `""`.
	\param caption Title of the table. Will be printed on a separate line directly above the table, if not `None` (default).
	\param formatter Format options. This is flexible with the following options:
		- `None` (default): No formatting is done and all entries are printed, as Python does by default.
		- String according to the Format Specification Mini-Language: The specified format is applied to all cells.
		- List of format strings: The formatting is assumed to be applicable to all rows.
		- List of list of format strings: It is assumed, that each cell is provided with an individual format string.
	\param head_sep If not `None` (default), this is put on an additional line between the head_row and the body of the table.
		This has only an effect, if `head_row` is not `None` aswell.
	\param transpose_data If set to `True`, the content of `table` will be transposed before typesetting. Defaults to `False`.
		Note, that `head_row` and `head_col` will not be swapped.
	\param file Path to the file in which the table is written to. Defaults to `None`, which means the table is printed on screen instead of saved to disk.
		If a valid path is given, the tables is written to this file. Overwrites the content of the file without further questions.
	\param show Switch, whether the formatted table should be printed to the default output. If set to `None` (default), it is shown, if `file is None`.
	\param *args Positional arguments, will be ignored.
	\param *kwargs Keyword arguments, will be ignored.
	
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
	# Default to show only, if file is None,
	show = show if show is not None else (file is None)
	if transpose_data:
		table = _transpose_data(table)
	# Get the formatter table
	format_table = _get_formatter_table(formatter, table)
	formatted_lines = []
	# Print caption
	if caption is not None:
		formatted_lines.append("{}".format(caption))
	# Format table head
	if head_row is not None:
		formatted_line = "{}{}".format(top_left, itemsep) if head_col is not None else ""
		for col_num, item in enumerate(head_row):
			formatted_line += "{}".format(item)
			if col_num == len(head_row)-1:
				formatted_line += "{}".format(lineend)
			else:
				formatted_line += "{}".format(itemsep)
		formatted_lines.append(formatted_line)
		# Optionally add a head separation
		if head_sep is not None:
			formatted_lines.append(head_sep)
	# Format table body
	for row_num, (row, row_format) in enumerate(zip(table, format_table)):
		formatted_line = ""
		if len(row) != len(row_format):
			raise ValueError("Numbers of entries in data and format do not match: data: {}; format: {}!".format(len(row), len(row_format)))
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
	if file is not None:
		if not os.path.exists(os.path.dirname(file)):
			os.makedirs(os.path.dirname(file))
		with codecs.open(file, "w", "utf-8") as f:
			for line in formatted_lines:
				f.write(line + "\n")
	if show:
		for line in formatted_lines:
			print(line)
	return formatted_lines

def print_table_LaTeX(table: list,
					head_row: list = None,
					head_col: list = None,
					top_left: str = "",
					file: str = None,
					formatter = None,
					caption: str = None,
					LaTeX_label: str = None,
					LaTeX_format: str = "l",
					table_head: str = None,
					table_notes: str = None,
					transpose_data: bool = False,
					show: bool = None,
					*args, **kwargs) -> list:
	"""
	Prints the table in a LaTeX format, and it can be copied or input directly into a TeX file.
	\param table List of lists (array-like, but can have different data types).
	\param head_row List of column heads, if specified, printed before the rest of the table.
	\param head_col This is put infront of the rows, if not left `None` (default).
	\param top_left This is put in the top-left cell, if both `head_row` and `head_col` are provided. Defaults to `""`.
	\param file Path to the file in which the table is written to. Defaults to `None`, which means the table is printed on screen instead of saved to disk.
		If a valid path is given, the tables is written to this file. Overwrites the content of the file without further questions.
	\param formatter Format options. This is flexible with the following options:
		- `None` (default): No formatting is done and all entries are printed, as Python does by default.
		- String according to the Format Specification Mini-Language: The specified format is applied to all cells.
		- List of format strings: The formatting is assumed to be applicable to all rows.
		- List of list of format strings: It is assumed, that each cell is provided with an individual format string.
	\param caption Caption of the table. Will used as the content of LaTeX's `\caption{<caption>}` above the table.
	\param LaTeX_label LaTeX lable of the table. Will result in: `\label{tab:<LaTeX_label>}`.
	\param LaTeX_format Column format specification according to the LaTeX specification. This is flexible with the following options:
		- String: The format is apllied to all data coloumns. By default, ll data columns will be left-aligned, which is equivalent to `"l"`.
		- List of strings: I is assumed, that each data column has an individual format. Make sure, the number of rows is in sync with the data to avoid compilation errors.
	\param table_head This option can be used to add content between the `\toprule` and `head_row`, e.g. for multi-line table heads.
		Defaults to `None`, which means no effect.
	\param table_notes This option can be used to add content between the `\end{tabular}` and `\end{table}`, e.g. for additional notes, which should be included in the float.
		This content is set left-aligned.
		Defaults to `None`, which means no effect.
	\param transpose_data If set to `True`, the content of `table` will be transposed before typesetting. Defaults to `False`.
		Note, that `head_row` and `head_col` will not be swapped.
	\param show Switch, whether the formatted table should be printed to the default output. If set to `None` (default), it is shown, if `file is None`.
	\param *args Positional arguments, will be ignored.
	\param *kwargs Keyword arguments, will be ignored.
	
	To use the generated table, add the following code to your preamble:
	```
	\newcommand{\thfl}[1]{\multicolumn{1}{@{}l}{#1}}	% top row format, left most column
	\newcommand{\thfm}[1]{\multicolumn{1}{c}{#1}}		% top row format, middle coloumn
	\newcommand{\thfr}[1]{\multicolumn{1}{c@{}}{#1}}	% top row format, right most column
	```
	If specifies the formatting of the cells in the header row for the whole document.
	To actually print the table, use the following code snippet:
	```
	\begin{table}[hbtp]
	\centering
	% <copy table content here> or \input{<filename>}
	\end{table}
	```
	"""
	# Preparation of 
	show = show if show is not None else (file is None)
	LaTeX_label = LaTeX_label if LaTeX_label is not None else file
	if head_row is not None:
		if head_col is not None:
			top_left = "\\thfl{"+"{}".format(top_left)+r"}"
			if len(head_row) > 1:
				head_row = ["\\thfm{"+"{}".format(head_row[0])+r"}"] + ["\\thfm{"+"{}".format(entry)+r"}" for entry in head_row[1:-1]] + ["\\thfr{"+"{}".format(head_row[-1])+r"}"]
			else:
				head_row = ["\\thfr{"+"{}".format(head_row[0])+r"}"]
		else:
			if len(head_row) > 1:
				head_row = ["\\thfl{"+"{}".format(head_row[0])+r"}"] + ["\\thfm{"+"{}".format(entry)+r"}" for entry in head_row[1:-1]] + ["\\thfr{"+"{}".format(head_row[-1])+r"}"]
			else:
				head_row = ["\\thfl{"+"{}".format(head_row[0])+r"}"]
	# Preamble
	formatted_table = []
	formatted_table.append(r"\caption{" + "{}".format(caption) + r"}")
	formatted_table.append(r"\label{tab:" + "{}".format(LaTeX_label) + r"}")
	formatted_table.append(r"\begin{tabular}{@{}")
	if head_col is not None:
		formatted_table.append(r"*{1}{l}")
	if isinstance(LaTeX_format, str):
		formatted_table.append(r"*{" + "{}".format(len(table[0])) + "}{" + "{}".format(LaTeX_format) + "}")
	elif isinstance(LaTeX_format, (list, tuple)):
		for col in LaTeX_format:
			formatted_table.append(r"*{1}{" + "{}".format(col) + "}")
	else:
		raise ValueError("LaTeX-format needs to be a str or iterable, not {}".format(type(LaTeX_format)))
	formatted_table.append(r"@{}}")
	formatted_table.append(r"\toprule")
	# Add optional head
	if table_head is not None:
		formatted_table.append(table_head)
	# Table content
	content = print_table(table=table,
			head_row=head_row,
			head_col=head_col,
			top_left=top_left,
			caption=None,
			formatter=formatter,
			itemsep=r" & ",
			lineend=r" \\",
			head_sep=r"\midrule",
			file=None,
			show=False,
			transpose_data=transpose_data,
			)
	formatted_table.extend(content)
	# Postamble
	formatted_table.append(r"\bottomrule")
	# Add optional table notes
	if table_notes is not None:
		formatted_table.append(r"{\raggedright " + table_notes + r"\par}")
	formatted_table.append(r"\end{tabular}")
	# Output
	if file is not None:
		if not os.path.exists(os.path.dirname(file)):
			os.makedirs(os.path.dirname(file))
		with codecs.open(file, "w", "utf-8") as f:
			for line in formatted_table:
				f.write(line + "\n")
	if show:
		for line in formatted_table:
			print(line)
	return formatted_table

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

def _transpose_data(table: list):
	"""
	Transposes the given table.
	Columns will become rows and rows will become columns.
	"""	
	return list(map(list, zip(*table)))

if __name__ == "__main__":
	pass
