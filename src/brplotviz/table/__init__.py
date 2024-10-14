
r"""
Contains table printing functionalities.

\author Bertram Richter
\date 2024
"""

import codecs
import copy
import itertools
import os

from . import styles
from .styles import *
from . import rules

def get_style(
		style,
		**kwargs: dict,
		) -> styles.Style:
	r"""
	Return the style or retrieve an style object by its class name.
	\param style
	This can be either an instance of the a subclass of \ref styles.Style or a `str`.
	If `style` is an instance of a subclass, it is returned unchanged.
	If `style` is a string it is assumed to be a class name, and an
	instance of that class with default settings is returned.
	Note that the class name is case-insensitive.
	\param kwargs Keyword arguments, passed to the constructor of the style.
	"""
	if isinstance(style, Style):
		return style
	elif isinstance(style, type) and issubclass(style, Style):
		return style(**kwargs)
	elif isinstance(style, str):
		try: 
			return getattr(styles, style.lower())(**kwargs)
		except:
			raise RuntimeError("Unknown table layout style: {}".format(style))

def print_table(table: list,
		style = "csv",
		head_col: list = None,
		head_row: list = None,
		top_left: str = "",
		align = "l",
		caption: str = None,
		file: str = None,
		formatter = None,
		omit_headrule: bool = False,
		replacement: dict = None,
		show: bool = None,
		transpose_data: bool = False,
		return_lines: bool = False,
		style_kwargs: dict = None,
		*args, **kwargs):
	r"""
	Prints the table in a nice format.
	\param table List of lists (array-like, but can have different data types).
	\param style This is the style specifying the table's style.
		Defaults to `"csv"`, see \ref styles for available options.
	\param head_col Row heads printed as a column infront of rest of the columns.
		Following options are available:
		- `None` (default): The table is not prepended with an extra column.
		- `list`: A list, each entry is a cell.
		- `"enumerate"`: the rows of the table body are enumerated.
			The counting starts at 1 after the `head_row` (if present).
	\param head_row List of column heads, printed as a line before the rest of the rows, if not left `None` (default).
	\param top_left This is put in the top-left cell, if both `head_row` and `head_col` are provided. Defaults to `""`.
	\param omit_headrule Switch to turn off the style-specific \ref rules.HeadRule.
		Defaults to `False` (show the rule, if the style support that).
		If the style does not show \ref rules.HeadRule, this setting has no effect.
		Keep in mind, that this could can invalidate the table format
		(e.g., Markdown).
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
	\param style_kwargs Keyword arguments, passed to the constructor of the style.
		This can be used to influence some aspects of the table.
		See \ref styles.Style.__init__() for more details.
	\param *args Additional positional arguments, will be ignored.
	\param **kwargs Additional keyword arguments, will be ignored.
	
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
	style_kwargs = style_kwargs if style_kwargs is not None else {}
	style = get_style(style, **style_kwargs)
	# Transpose the body data, if requested
	if transpose_data:
		table, _ = _clean_table(table)
		table = _transpose(table)
	# Convert to table of str
	clean_table, _ = _clean_table(table)
	table = _apply_format(table, formatter)
	top_left = "{}".format(top_left)
	# Enumerate tabele body lines, if requested
	if isinstance(head_col, str) and head_col.lower() == "enumerate":
		head_col = list(range(1, len(clean_table)+1))
	# Add the head_col to the table
	if head_col is not None:
		head_col = _apply_format([head_col], formatter=None)[0]
		head_col_iter = iter(head_col)
		for line in table:
			if not _rule_check(line):
				line.insert(0, next(head_col_iter))
	# Add the head_row to the table
	if head_row is not None:
		head_row = _apply_format([head_row], formatter=None)[0]
		if head_col is not None:
			head_row.insert(0, top_left)
		table.insert(0, head_row)
	if not omit_headrule:
		table.insert(1, rules.HeadRule())
	# New line treatment
	table_lines = []
	for i, row in enumerate(table):
		rule = _rule_check(row)
		if rule:
			# Check if the previous rule must be overwritten, the rule
			# with the lower priority value wins.
			if i > 0 and _rule_check(table_lines[-1]):
				last = table_lines.pop()
				rule = rule if rule.priority < last.priority else last
			table_lines.append(rule)
		else:
			row = _newline_split(row)
			table_lines.extend(row)
			table_lines.append(rules.MidRule())
	table_lines.pop()
	# Temporarily remove rules to prepare for columnwise operation
	table, rule_dict = _clean_table(table_lines)
	# Transpose and operate column wise
	table = _transpose(table)
	if replacement is not None:
		table = replace(table, replacement)
	col_widths = _find_col_width(table)
	alignments = _get_alignments(table, align)
	col_widths = style.modify_col_widths(col_widths, alignments)
	table =_align(table, alignments, col_widths)
	# Transpose again operate row wise again
	table = _transpose(table)
	# Insert extra rules again
	for i, rule in rule_dict.items():
		table.insert(i, rule)
	# Compose table as lines of text
	formatted_lines = []
	if caption is not None:
		formatted_lines.append(caption)
	rule = style.rule(col_widths, alignments, rules.TopRule())
	if rule is not None:
		formatted_lines.append(rule)
	for row in table:
		if not isinstance(row, rules.Rule):
			formatted_lines.append(style.row(row))
		else:
			rule = style.rule(col_widths, alignments, row)
			if rule is not None:
				formatted_lines.append(rule)
	rule = style.rule(col_widths, alignments, rules.BotRule())
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
		omit_headrule: bool = False,
		replacement: dict = None,
		show: bool = None,
		table_head: str = None,
		transpose_data: bool = False,
		return_lines: bool = False,
		*args, **kwargs):
	r"""
	Prints the table in a LaTeX format, and it can be copied or input directly into a TeX file.
	This is a convenience wrapper around \ref print_table().
	\param table List of lists (array-like, but can have different data types).
	\param head_col Row heads printed as a column infront of rest of the columns.
		Following options are available:
		- `None` (default): The table is not prepended with an extra column.
		- `list`: A list, each entry is a cell.
		- `"enumerate"`: the rows of the table body are enumerated.
			The counting starts at 1 after the `head_row` (if present).
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
	\param omit_headrule Switch to turn off the style-specific \ref rules.HeadRule.
		Defaults to `False`, show the rule.
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
	\param *args Additional positional arguments, will be ignored.
	\param **kwargs Additional keyword arguments, will be ignored.
	
	To use the generated table, add the following code to your preamble:
	```
	\newcommand{\thfl}[1]{\multicolumn{1}{@{}l}{#1}}	% table head format, left most column
	\newcommand{\thfm}[1]{\multicolumn{1}{c}{#1}}		% table head format, middle column
	\newcommand{\thfr}[1]{\multicolumn{1}{c@{}}{#1}}	% table head format, right most column
	```
	If specifies the formatting of the cells in the header row for the whole document.
	Then, you can copy the table into your TeX file or use `\input{<filename>}`.
	"""
	# Preparation
	LaTeX_label = LaTeX_label if LaTeX_label is not None else file
	top_left = r"\thfl{"+"{}".format(top_left)+r"}"
	if head_row is not None and len(head_row):
		head_row_format = [r"\thfm{"+"{}".format(entry)+r"}" for entry in head_row]
		if head_col is None:
			head_row_format[0] = r"\thfl{"+"{}".format(head_row[0])+r"}"
		head_row_format[-1] = r"\thfr{"+"{}".format(head_row[-1])+r"}"
		head_row = head_row_format
	# Preamble
	formatted_lines = [r"\begin{table}[!htbp]", r"\centering"]
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
	# Add optional head
	if table_head is not None:
		formatted_lines.append(table_head)
	# Table content
	content = print_table(table=table,
			style="latex",
			align=align,
			head_row=head_row,
			head_col=head_col,
			top_left=top_left,
			caption=None,
			formatter=formatter,
			file=None,
			omit_headrule=omit_headrule,
			replacement=replacement,
			show=False,
			transpose_data=transpose_data,
			return_lines=True,
			*args, **kwargs
			)
	formatted_lines.extend(content)
	# Postamble
	formatted_lines.append(r"\end{tabular}")
	formatted_lines.append(r"\end{table}")
	# Output
	_output_table(formatted_lines, file, show)
	if return_lines:
		return formatted_lines

def replace(table: list, replacement: dict) -> list:
	r"""
	Replace specific values by something else in all cells.
	\param table Table, for which the content of all cells should be replaced, if they contain something in `source`.
	\param replacement This dictionary contains the source values (to replace) as keys and the target values (to be replaced by) as values.
		Example: to replace all `NaN` (not a number) by em-dashes and all `0` by `"nothing"`: `{"nan": "---", 0: "nothing"}`
	"""
	if replacement is None:
		return table
	for row in table:
		if not isinstance(row, rules.Rule):
			for i, entry in enumerate(row):
				row[i] = replacement[entry] if entry in replacement else entry
	return table

def _apply_format(table: list, formatter) -> list:
	r"""
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
		if not _rule_check(row):
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

def _align(table: list, alignments: list, col_widths: list) -> list:
	r"""
	Brings the cells in a column to the same width for all columns in table.
	The content in the cell is aligned according to `alignments`.
	\param table A list of columns (the table is transposed by \ref _transpose()).
		Table cells are converted to `str` by \ref _apply_format().
	\param alignments The list of aligmnent as completed by \ref _get_alignments().
	\param col_widths List of columns' widths.
	\return Returns table where each cell in a column has the same width.
	"""
	if alignments is None:
		return table
	align_dict = {"l": "<", "c": "^", "r": ">", "": ""}
	align_code = [align_dict.get(a, "") for a in alignments]
	aligned = []
	for align, col, width in zip(align_code, table, col_widths):
		aligned_col = [("{:" + align + str(width) + "}").format(str(entry)) for entry in col]
		aligned.append(aligned_col)
	return aligned

def _clean_table(table):
	clean_table = []
	rule_dict = {}
	for i, row in enumerate(copy.deepcopy(table)):
		rule = _rule_check(row)
		if rule:
			rule_dict[i] = row
		else:
			try:
				clean_table.append(list(row))
			except:
				raise ValueError("Cannot convert {}th entry to list: {}".format(i, row))
	return clean_table, rule_dict

def _find_col_width(table: list) -> list:
	r"""
	For each column in the table, the width of the column is determined
	by the widest cell in the respective column.
	\param table Table for which the column widths should be determined.
		It is assumed, that:
		- the original table is transposed (each entry is a column) and
		- everything is converted by \ref _apply_format().
	"""
	return [max([len(entry) for entry in col]) for col in table]

def _get_alignments(table: list, align) -> list:
	r"""
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

def _get_formatter_table(table: list, formatter) -> list:
	r"""
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
			# Assume per-row formattin
			return [formatter for row in table]
	elif isinstance(formatter, str):
		# Assume same formatting for each cell
		return [[formatter]*len(row) for row in table]
	else:
		raise ValueError("Please provide a string with a Format Specification Mini-Language!")

def _include_head(
		table: list,
		head_row: list,
		head_col: list,
		top_left: str,
		) -> list:
	r"""
	Insert the header row and header column into the table. 
	\param table Data, of the table.
	\param head_row First row, of the table, which holds the column names.
	\param head_col First column, of the table, which holds the row names.
	\param top_left Content of the cell, which appears in the top left corner of the table, when both `head_row` and `head_col` is added.
	"""
	if head_col is not None:
		head_col_gen = iter(copy.deepcopy(head_col))
		for row in table:
			if not isinstance(row, rules.Rule):
				row.insert(0, str(next(head_col_gen)))
	
	if head_row is not None:
		if head_col is not None:
			table.insert(0, [str(top_left)] + [str(entry) for entry in head_row])
		else:
			table.insert(0, [str(entry) for entry in head_row])
	return table

def _newline_split(row):
	max_new_lines = 0
	extra_lines = [[""]*len(row)]
	for col_number, cell in enumerate(row):
		if "\n" not in cell:
			extra_lines[0][col_number] = cell
			continue
		# A newline was found
		cell_lines = cell.split("\n")
		max_new_lines = max(len(extra_lines), len(cell_lines))
		for i in range(len(extra_lines), max_new_lines):
			extra_lines.append([""]*len(row))
		for extra_line_number, sub_cell in enumerate(cell_lines):
			extra_lines[extra_line_number][col_number] = sub_cell
	extra_lines_rules = []
	for line in extra_lines:
		if _rule_check(line):
			extra_lines_rules.append(line)
		else:
			extra_lines_rules.append(line)
			extra_lines_rules.append(rules.NoRule())
	extra_lines_rules.pop()
	return extra_lines_rules

def _output_table(formatted_lines: list, file: str, show: bool):
	r"""
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

def _rule_check(rule):
	"""
	Returns an instance of the \ref rules.Rule objects, of `rule`'s (sub)class.
	If `rule` is not a \ref rules.Rule object, `None` is returned.
	Apart from conversion to instances, this can be used to check whether
	`rule` is a \ref rules.Rule object, because \ref rules.Rule objects, when typecast
	boolean to result in `True`, but `None` typecast to boolean gives `False`. 
	"""
	if isinstance(rule, rules.Rule):
		return rule
	elif isinstance(rule, type) and issubclass(rule, rules.Rule):
		return rule()
	else:
		return None

def _transpose(table: list) -> list:
	r"""
	Transposes the given table, columns become rows and rows become columns.
	Missing cells (if a row has fewer entries than other rows) will be
	fill up with empty strings (`""`).
	"""
	return list(map(list, itertools.zip_longest(*table, fillvalue="")))

if __name__ == "__main__":
	pass
