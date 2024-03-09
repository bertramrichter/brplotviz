
"""
Contains table printing functionalities.
\author Bertram Richter
\date 2022
"""

import codecs
import copy
import itertools
import os

from . import engines
from .engines import *
from . import rules
from .rules import *

def get_engine(engine):
	"""
	Return the engine or retrieve an engine object by its class name.
	This can be either an instance of the a subclass of \ref engines.Engine or a `str`.
	If `engine` is an instance of a subclass, it is returned unchanged.
	If `engine` is a string it is assumed to be a class name, and an
	instance of that class with default settings is returned.
	Note that the class name is case-insensitive.
	"""
	if isinstance(engine, Engine):
		return engine
	elif isinstance(engine, str):
		try: 
			return getattr(engines, engine.lower())()
		except:
			raise RuntimeError("Unknown table layout engine: {}".format(engine))

def print_table(table: list,
		engine,
		head_col: list = None,
		head_row: list = None,
		top_left: str = "",
		align = "l",
		caption: str = None,
		file: str = None,
		formatter = None,
		replacement: tuple = None,
		show: bool = None,
		transpose_data: bool = False,
		return_lines: bool = False,
		*args, **kwargs):
	"""
	Prints the table in a nice format.
	\param table List of lists (array-like, but can have different data types).
	\param head_col List of row heads, printed as a column infront of rest of the columns, if not left `None` (default).
	\param head_row List of column heads, printed as a line before the rest of the rows, if not left `None` (default).
	\param top_left This is put in the top-left cell, if both `head_row` and `head_col` are provided. Defaults to `""`.
	\param align Specifies the alignment options of the columns.
		Available options:
		- `"l"` (default): All columns are left-aligned.
		- `"c"`: All columns are centered.
		- `"r"`: All columns are right-aligned.
		- `None`: No alignment of columns is done.
		- List of afforementioned options: Each column can have it's own alignment.
			An alignment for `head_col` needs to be included as well, if `head_col` is provided.
	\param caption Title of the table.
		Will be printed on a separate line directly above the table, if not `None` (default).
	\param itemsep String, that is put in-between items of the same line. Defaults to `"\t"`.
	\param lineend String that is put at the end of the line. Defaults to `""`.
	\param file Path to the file in which the table is written to.
		Defaults to `None`, which means the table is printed on screen instead of saved to disk.
		If a valid path is given, the tables is written to this file.
		Overwrites the content of the file without further questions.
	\param formatter Format options. This is flexible with the following options:
		- `None` (default): No formatting is done and all entries are printed, as Python does by default.
		- String according to the Format Specification Mini-Language: The specified format is applied to all cells.
		- List of format strings: The formatting is assumed to be applicable to all rows.
		- List of list of format strings: It is assumed, that each cell is provided with an individual format string.
	\param head_sep If not `None` (default), this is put on an additional line between the head_row and the body of the table.
		This has only an effect, if `head_row` is not `None` aswell.
	\param replacement This dictionary contains the source values (to replace) as keys and the target values (to be replaced by) as values.
		Example: to replace all `NaN` (not a number) by em-dashes and all 0 by `"nothing"`: `{"nan": "---", 0: "nothing"}`
		Defaults to `None` (no replacement is attempted).
		If activated, the replacement in carried out after converting the cells to `str`, but before alignment.
		If you want to replace (raw) content before the formatting, use \ref replace() before passing the table to \ref print_table().
	\param show Switch, whether the formatted table should be printed to the default output.
		If set to `None` (default), it is shown, if `file is None`.
	\param transpose_data If set to `True`, the content of `table` will be transposed before typesetting.
		Defaults to `False`.
		Note, that `head_row` and `head_col` will not be swapped.
	\param return_lines Switch, whether the list of formatted lines should be returned. Defaults to `False`.
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
	engine = get_engine(engine)
	# Make a deepcopy to not modify the original data
	# Convert the table to a list of lists (e.g., from numpy arrays)
	# Extract extra rules
	rule_dict = {}
	clean_table = []
	for i, row in enumerate(copy.deepcopy(table)):
		if isinstance(row, Rule):
			rule_dict[i] = row
		elif isinstance(row, type) and issubclass(row, Rule):
			rule_dict[i] = row()
		else:
			try:
				clean_table.append(list(row))
			except:
				raise ValueError("Cannot convert {}th entry to list: {}".format(i, row))
	# Transpose and operate column wise
	table = clean_table
	#table = _transpose_data(clean_table)
	
	# Sanity checks
	#clean_table = [list(row) for row in table if not isinstance(row, Rule)]
	#if head_col is not None:
	#	assert len(head_col) == len(clean_table), "Length of head_col ({}) and lines in table ({}) do not match".format(len(head_col), len(clean_table))
	#if head_row is not None:
	#	lengths = set([len(row) for row in clean_table if not isinstance(row, Rule)])
		#assert len(lengths) == 1
		#assert len(head_row) in lengths, "Length of head_row ({}) and lines in table ({}) do not match".format(len(head_row), lengths)
	# 
	table = _apply_format(table, formatter)
	table = _include_head(table, head_row, head_col, top_left)
	if replacement is not None:
		table = replace(table, replacement)
	col_widths = _find_col_width(table)
	col_widths = engine.modify_col_widths(col_widths, align)
	
	# Insert extra rules again
	#if not transpose_data:
	#	table = _transpose_data(table)
	for i, rule in rule_dict.items():
		if head_row is None:
			table.insert(i, rule)
		else:
			table.insert(i+1, rule)
	
	# Compose table as lines of text
	formatted_lines = []
	if caption is not None:
		formatted_lines.append(caption)
	_rule(formatted_lines, TopRule(), engine, col_widths, align)
	row = _align(table[0], align, col_widths)
	formatted_lines.append(engine.row(row))
	_rule(formatted_lines, HeadRule(), engine, col_widths, align)
	row_count = len(table)
	for row_nr, row in enumerate(table[1::]):
		if not isinstance(row, Rule):
			row = _align(row, align, col_widths)
			formatted_lines.append(engine.row(row))
			rule = engine.rule(col_widths, align, row)
			if rule is not None:
				formatted_lines.append(rule)
			if not row_nr == row_count-1:
				_rule(formatted_lines, MidRule(), engine, col_widths, align)
		else:
			_rule(formatted_lines, row, engine, col_widths, align)
	rule = engine.rule(col_widths, align, BotRule())
	if rule is not None:
		formatted_lines.append(rule)
	# Output
	_output_table(formatted_lines, file, show)
	if return_lines:
		return formatted_lines

def print_table_LaTeX(table: list,
					head_row: list = None,
					head_col: list = None,
					top_left: str = "",
					align = "l",
					caption: str = None,
					file: str = None,
					formatter = None,
					LaTeX_label: str = None,
					LaTeX_format: str = "l",
					show: bool = None,
					replacement: tuple = None,
					table_head: str = None,
					transpose_data: bool = False,
					return_lines: bool = False,
					*args, **kwargs):
	"""
	Prints the table in a LaTeX format, and it can be copied or input directly into a TeX file.
	This is a convenience wrapper around \ref print_table().
	\param table List of lists (array-like, but can have different data types).
	\param head_col List of row heads, printed as a column infront of rest of the columns, if not left `None` (default).
	\param head_row List of column heads, printed as a line before the rest of the rows, if not left `None` (default).
	\param top_left This is put in the top-left cell, if both `head_row` and `head_col` are provided.
		Defaults to `""`.
	\param align Specifies the alignment options of the columns.
		Available options:
		- `"l"` (default): All columns are left-aligned.
		- `"c"`: All columns are centered.
		- `"r"`: All columns are right-aligned.
		- `None`: No alignment of columns is done.
		- List of afforementioned options: Each column can have it's own alignment.
			An alignment for `head_col` needs to be included as well, if `head_col` is provided.
	\param caption Caption of the table. Will used as the content of LaTeX's `\caption{<caption>}` above the table.
	\param file Path to the file in which the table is written to.
		Defaults to `None`, which means the table is printed on screen instead of saved to disk.
		If a valid path is given, the tables is written to this file.
		Overwrites the content of the file without further questions.
	\param formatter Format options. This is flexible with the following options:
		- `None` (default): No formatting is done and all entries are printed, as Python does by default.
		- String according to the Format Specification Mini-Language: The specified format is applied to all cells.
		- List of format strings: The formatting is assumed to be applicable to all rows.
		- List of list of format strings: It is assumed, that each cell is provided with an individual format string.
	\param LaTeX_label LaTeX lable of the table. Will result in: `\label{tab:<LaTeX_label>}`.
		If given `None`, the `file` is used as fallback.
	\param LaTeX_format Column format specification according to the LaTeX specification.
		This is flexible with the following options:
		- String: The format is applied to all data columns.
			By default, all data columns will be left-aligned, which is equivalent to `"l"`.
		- List of strings: I is assumed, that each data column has an individual format.
			Make sure, the number of rows is in sync with the data to avoid compilation errors.
	\param replacement  This dictionary contains the source values (to replace) as keys and the target values (to be replaced by) as values.
		Example: to replace all `NaN` (not a number) by em-dashes and all 0 by `"nothing"`: `{"nan": "---", 0: "nothing"}`
		Defaults to `None` (no replacement is attempted).
		If activated, the replacement in carried out after converting the cells to `str`, but before alignment.
		If you want to replace (raw) content before the formatting, use \ref replace() before passing the table to \ref print_table().
	\param show Switch, whether the formatted table should be printed to the default output.
		If set to `None` (default), it is shown, if `file is None`.
	\param table_head This option can be used to add content between the `\toprule` and `head_row`, e.g. for multi-line table heads.
		Defaults to `None`, which means no effect.
	\param transpose_data If set to `True`, the content of `table` will be transposed before typesetting.
		Defaults to `False`.
		Note, that `head_row` and `head_col` will not be swapped.
	\param return_lines Switch, whether the list of formatted lines should be returned. Defaults to `False`.
	\param *args Positional arguments, will be ignored.
	\param *kwargs Keyword arguments, will be ignored.
	
	To use the generated table, add the following code to your preamble:
	```
	\newcommand{\thfl}[1]{\multicolumn{1}{@{}l}{#1}}	% table head format, left most column
	\newcommand{\thfm}[1]{\multicolumn{1}{c}{#1}}		% table head format, middle column
	\newcommand{\thfr}[1]{\multicolumn{1}{c@{}}{#1}}	% table head format, right most column
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
	# Preparation
	LaTeX_label = LaTeX_label if LaTeX_label is not None else file
	if head_row is not None:
		top_left = r"\thfl{"+"{}".format(top_left)+r"}"
		head_row_format = [r"\thfm{"+"{}".format(entry)+r"}" for entry in head_row]
		if head_col is None:
			head_row_format[0] = r"\thfl{"+"{}".format(head_row[0])+r"}"
		head_row_format[-1] = r"\thfr{"+"{}".format(head_row[-1])+r"}"
		head_row = head_row_format
	# Preamble
	formatted_lines = []
	formatted_lines.append(r"\caption{" + "{}".format(caption) + r"}")
	formatted_lines.append(r"\label{tab:" + "{}".format(LaTeX_label) + r"}")
	formatted_lines.append(r"\begin{tabular}{@{}")
	if head_col is not None:
		formatted_lines.append(r"*{1}{l}")
	if isinstance(LaTeX_format, str):
		formatted_lines.append(r"*{" + "{}".format(len(table[0])) + "}{" + "{}".format(LaTeX_format) + "}")
	elif isinstance(LaTeX_format, (list, tuple)):
		for col in LaTeX_format:
			formatted_lines.append(r"*{1}{" + "{}".format(col) + "}")
	else:
		raise ValueError("LaTeX-format needs to be a str or iterable, not {}".format(type(LaTeX_format)))
	formatted_lines.append(r"@{}}")
	formatted_lines.append(r"\toprule")
	# Add optional head
	if table_head is not None:
		formatted_lines.append(table_head)
	# Table content
	content = print_table(table=table,
			engine="latex",
			align=align,
			head_row=head_row,
			head_col=head_col,
			top_left=top_left,
			caption=None,
			formatter=formatter,
			file=None,
			replacement=replacement,
			show=False,
			transpose_data=False,
			return_lines=True,
			)
	formatted_lines.extend(content)
	# Postamble
	formatted_lines.append(r"\bottomrule")
	formatted_lines.append(r"\end{tabular}")
	# Output
	_output_table(formatted_lines, file, show)
	if return_lines:
		return formatted_lines

def replace(table: list, replacement: dict) -> list:
	"""
	Replace specific values by something else in all cells.
	\param table Table, for which the content of all cells should be replaced, if they contain something in `source`.
	\param replacement This dictionary contains the source values (to replace) as keys and the target values (to be replaced by) as values.
		Example: to replace all `NaN` (not a number) by em-dashes and all `0` by `"nothing"`: `{"nan": "---", 0: "nothing"}`
	"""
	if replacement is None:
		return table
	for row in table:
		if not isinstance(row, Rule):
			for i, entry in enumerate(row):
				row[i] = replacement[entry] if entry in replacement else entry
	return table

def _apply_format(table, formatter) -> list:
	"""
	Converts the entries of the given table into `str`.
	\param table Table with the original content to be converted.
	\param formatter Format option, see \ref _get_formatter_table().
	\return Returns a table of the same dimensions sasdf
	"""
	if formatter is None:
		formatter = ""
	if isinstance(formatter, str):
		formatter = itertools.repeat(formatter)
	str_table = []
	for row in table:
		if not isinstance(row, Rule):
			str_row = []
			for format_entry, entry in zip(formatter, row):
				try:
					str_row.append("{}".format("{"+format_entry+"}").format(entry))
				except:
					str_row.append(str(entry))
			str_table.append(str_row)
		else:
			str_table.append(row)
	return str_table

def _align(row, align, col_widths) -> list:
	"""
	Brings the cells of a column to the same width for all columns.
	The content in the cell is aligned according to `align`.
	\param table A list of lists of str.
		It is assumed, that the original table is converted by \ref _apply_format() prior to it.
	\param align Specifies the alignment options of the columns. Available options:
		- `"l"` (default): All columns are left-aligned.
		- `"c"`: All columns are centered.
		- `"r"`: All columns are right-aligned.
		- `None`: No alignment of columns is done.
		- List of afforementioned options: Each column can have it's own alignment.
			An alignment for `head_col` needs to be included as well, if `head_col` is provided.
	\return Returns a ist of lists of str, where each column has the same width.
	"""
	align_dict = {"l": "<", "c": "^", "r": ">"}
	if align is None:
		return row
	else:
		if isinstance(align, str):
			alignment = [align_dict[align]]*len(row)
		elif isinstance(align, list):
			alignment = [align_dict[col] for col in align]
		else:
			raise ValueError("Wrong alignment type.")
		aligned = [("{:" + align + str(width) + "}").format(str(entry)) for align, entry, width in itertools.zip_longest(alignment, row, col_widths, fillvalue="")]
		return aligned

def _find_col_width(table) -> list:
	"""
	For each column in the table, width of the column is determined by the widest cell in the respective column.
	\param table Table for which the column widths should be determined.
		It is assumed, that the original table is converted by \ref _apply_format() prior to it.
	"""
	table_tmp = [row for row in table if not isinstance(row, Rule)]
	col_list = _transpose_data(table_tmp)
	return [max([len(entry) for entry in col]) for col in col_list]

def _get_formatter_table(table, formatter) -> list:
	"""
	Get the table of formatting strings.
	\param formatter Format options. This is flexible with the following options:
		- `None` (default) No formatting is done and all entries are printed, as Python does by default.
		- String according to the Format Specification Mini-Language: The specified format is applied to all cells.
		- List of format strings: The formatting is assumed to be applicable to all rows.
		- List of list of format strings: It is assumed, that each cell is provided with an individual format string.
	\param table The table, for which the formatting is to generated.
		Only dimension of the table is of interest here.
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

def _include_head(table, head_row, head_col, top_left) -> list:
	"""
	Insert the header row and header column into the table. 
	\param table Data, of the table.
	\param head_row First row, of the table, which holds the column names.
	\param head_col First column, of the table, which holds the row names.
	\param top_left Content of the cell, which appears in the top left corner of the table, when both `head_row` and `head_col` is added.
	"""
	if head_col is not None:
		head_col_gen = iter(copy.deepcopy(head_col))
		for row in table:
			if not isinstance(row, Rule):
				row.insert(0, str(next(head_col_gen)))
	
	if head_row is not None:
		if head_col is not None:
			table.insert(0, [str(top_left)] + [str(entry) for entry in head_row])
		else:
			table.insert(0, [str(entry) for entry in head_row])
	return table

def _output_table(formatted_lines, file, show):
	"""
	Depending on the options, the list of lines is either written to a file on disk or printed on the screen (or neither).
	\param formatted_lines List of table lines to be outputted.
	\param file Path to the file in which the table is written to.
		Defaults to `None`, which means the table is printed on screen instead of saved to disk.
		If a valid path is given, the table is written to this file.
		The content of the file is overwritten without further questions.
	\param show Switch, whether the formatted table should be printed to the default output.
		By default (`None`), it is only shown, if no file is provided (`file is None`).
	"""
	show = show if show is not None else (file is None)
	if file is not None:
		file = os.path.join(os.getcwd(), file)
		try:
			if not os.path.exists(os.path.dirname(file)):
				os.makedirs(os.path.dirname(file))
			with codecs.open(file, "w", "utf-8") as f:
				for line in formatted_lines:
					f.write(line + "\n")
		except:
			print('Failed to save table to file "{}"'.format(file))
	if show:
		for line in formatted_lines:
			print(line)

def _rule(formatted_lines, rule, engine, col_widths, align):
	"""
	Add a rule.
	\todo Document
	"""
	rule = engine.rule(col_widths, align, rule)
	if rule is not None:
		formatted_lines.append(rule)

def _transpose_data(table: list) -> list:
	"""
	Transposes the given table.
	Columns will become rows and rows will become columns.
	"""	
	return list(map(list, itertools.zip_longest(*table, fillvalue="")))

def _typeset_lines(table, itemsep, lineend) -> list:
	"""
	The cells in a row are joined to a single`str`, using the `itemsep` and finished by `lineend`.
	\param table List of list of str, that will be joined to a list of str, one str per row.
	\param itemsep String, that is put in-between items of the same line.
	\param lineend String that is put at the end of the line.
	"""
	return [itemsep.join(row) + lineend for row in table]

if __name__ == "__main__":
	pass
