
"""
Contains table printing functionalities.

\author Bertram Richter
\date 2024
"""

import codecs
import copy
import itertools
import os

from . import engines
from .engines import *
from . import rules
from .rules import *

def get_engine(engine, **kwargs: dict):
	"""
	Return the engine or retrieve an engine object by its class name.
	\param engine
	This can be either an instance of the a subclass of \ref engines.Engine or a `str`.
	If `engine` is an instance of a subclass, it is returned unchanged.
	If `engine` is a string it is assumed to be a class name, and an
	instance of that class with default settings is returned.
	Note that the class name is case-insensitive.
	\param kwargs Keyword arguments, passed to the constructor of the engine.
	"""
	if isinstance(engine, Engine):
		return engine
	elif isinstance(engine, type) and issubclass(engine, Engine):
		return engine(**kwargs)
	elif isinstance(engine, str):
		try: 
			return getattr(engines, engine.lower())(**kwargs)
		except:
			raise RuntimeError("Unknown table layout engine: {}".format(engine))

def print_table(table: list,
		engine: engines.Engine = "csv",
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
		engine_kwargs: dict = None,
		*args, **kwargs):
	"""
	Prints the table in a nice format.
	\param table List of lists (array-like, but can have different data types).
	\param engine This is the engine specifying the table's style.
		Defaults to `"csv"`, see \ref engines for available options.
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
	\param file Path to the file in which the table is written to.
		Defaults to `None`, which means the table is printed on screen instead of saved to disk.
		If a valid path is given, the tables is written to this file.
		Overwrites the content of the file without further questions.
	\param formatter Format options. This is flexible with the following options:
		- `None` (default): No formatting is done and all entries are printed, as Python does by default.
		- String according to the Format Specification Mini-Language: The specified format is applied to all cells.
		- List of format strings: The formatting is assumed to be applicable to all rows.
		- List of list of format strings: It is assumed, that each cell is provided with an individual format string.
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
	\param engine_kwargs Keyword arguments, passed to the constructor of the engine.
		This can be used to influence some aspects of the table.
		See \ref engines.Engine.__init__() for more details.
	\param *args Positional arguments, will be ignored.
	\param **kwargs Keyword arguments, will be ignored.
	
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
	engine_kwargs = engine_kwargs if engine_kwargs is not None else {}
	engine = get_engine(engine, **engine_kwargs)
	# Make a deepcopy to not modify the original data
	head_col = copy.deepcopy(head_col)
	head_row = copy.deepcopy(head_row)
	# Convert the table to a list of lists (e.g., from numpy arrays) and
	# extract extra rules
	clean_table = []
	rule_dict = {}
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
	table = clean_table
	# Transpose the body data, if requested
	if transpose_data:
		table = _transpose(table)
	# Convert to table of str
	table = _apply_format(table, formatter)
	if head_row is not None:
		table.insert(0, head_row)
	if head_row is not None and head_col is not None:
		head_col.insert(0, top_left)
	# Transpose and operate column wise
	table = _transpose(table)
	# Add header column
	if head_col is not None:
		table.insert(0, head_col)
	if replacement is not None:
		table = replace(table, replacement)
	col_widths = _find_col_width(table)
	alignments = _get_alignments(table, align)
	col_widths = engine.modify_col_widths(col_widths, alignments)
	table =_align(table, alignments, col_widths)
	# Transpose again
	table = _transpose(table)
	# Insert extra rules again
	if not transpose_data:
		# but only if the data was now extra transposed
		for i, rule in rule_dict.items():
			if head_row is None:
				table.insert(i, rule)
			else:
				table.insert(i+1, rule)
	# Compose table as lines of text
	formatted_lines = []
	if caption is not None:
		formatted_lines.append(caption)
	_rule(formatted_lines, TopRule(), engine, col_widths, alignments)
	formatted_lines.append(engine.row(table[0]))
	_rule(formatted_lines, HeadRule(), engine, col_widths, alignments)
	row_count = len(table)
	for row_nr, row in enumerate(table[1::]):
		if not isinstance(row, Rule):
			formatted_lines.append(engine.row(row))
			rule = engine.rule(col_widths, alignments, MidRule)
			if rule is not None:
				formatted_lines.append(rule)
			if not row_nr == row_count-1:
				_rule(formatted_lines, MidRule(), engine, col_widths, alignments)
		else:
			_rule(formatted_lines, row, engine, col_widths, alignments)
	rule = engine.rule(col_widths, alignments, BotRule())
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
		Missing entries are filled up with left-alignment (`"l"`).
		Available options:
		- `"l"` (default): All columns are left-aligned.
		- `"c"`: All columns are centered.
		- `"r"`: All columns are right-aligned.
		- `""` (empty strin): Behaves like `"l"`, but might result in
			omission of alignment indication in some table styles.
		- `None`: Alignment of columns is deactivated.
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

def _align(table, alignments, col_widths) -> list:
	"""
	Brings the cells in a column to the same width for all columns in table.
	The content in the cell is aligned according to `alignments`.
	\param table A list of columns (the table is transposed by \ref _transpose()).
		Table cells are converted to `str` by \ref _apply_format().
	\param alignments The list of aligmnent as completed by \ref _get_alignments().
	\param col_widths List of columns' widths.
	\return Returns table where each cell in a column has the same width.
	"""
	align_dict = {"l": "<", "c": "^", "r": ">", "": ""}
	align_code = [align_dict.get(a, "") for a in alignments]
	aligned = []
	for align, col, width in zip(align_code, table, col_widths):
		aligned_col = [("{:" + align + str(width) + "}").format(str(entry)) for entry in col]
		aligned.append(aligned_col)
	return aligned

def _find_col_width(table) -> list:
	"""
	For each column in the table, the width of the column is determined
	by the widest cell in the respective column.
	\param table Table for which the column widths should be determined.
		It is assumed, that:
		- the original table is transposed (each entry is a column) and
		- everything is converted by \ref _apply_format().
	"""
	return [max([len(entry) for entry in col]) for col in table]

def _get_alignments(table, align) -> list:
	"""
	The the aligment codes form the table's columns.
	Potentially missing column alignment are filled up with left alignment.
	\param table List of lists. An entry of `table` is a column.
	\param align See parameter description in \ref print_table()
	"""
	if align is None:
		return align
	else:
		if isinstance(align, str):
			alignment = [align]*len(table)
		elif isinstance(align, (list, tuple)):
			alignment = [a for col, a in itertools.zip_longest(table, align, fillvalue="l")]
		else:
			raise ValueError("Wrong alignment type.")
	return alignment

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

def _rule(formatted_lines, rule, engine, col_widths, alignments):
	"""
	Add a rule.
	\param formatted_lines The alread fully typeset lines of the table.
	\param rule A \ref rules.Rule, for which the engine is requested to
		draw a rule.
	\param engine The engine to draw a rule.
	\param col_widths A list of the columns' widths.
	\param alignments A full aligment list (see \ref _get_alignments()).
	"""
	rule = engine.rule(col_widths, alignments, rule)
	if rule is not None:
		formatted_lines.append(rule)

def _transpose(table: list) -> list:
	"""
	Transposes the given table, columns become rows and rows become columns.
	Missing cells (if a row has fewer entries than other rows) will be
	fill up with empty strings (`""`).
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
