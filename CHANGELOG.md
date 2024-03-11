# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]


## [v0.2.1] – 2024-03-10

### Changed
- Fix bug where `print_table_LaTeX()` disrespects `transpose_data`
- Documentation and type hint improvements

## [v0.2] – 2024-03-10

### Added
- New table engines for different layout styles.
	This should make adding furter table styles easier.
	Available engines are:
	- `csv`: character separated values,
		the itemsep ist configurable, but defaults to comma),
	- `tsv`: tab separated values,
		a special instance of `csv` with the tab as itemsep
	- `latex`: Typesets the body that is usually inside a tabular environment.
		I you want to inculde the environment too, use `print_tableLaTeX()`.
	- `markdown`
- Values of cells can now be padded to both sides individually.
	This functionality is provided by the `engine` constructor or the
	`engine_kwargs` attribute.
- Extra rules (horizontal lines) can now be put into the table (although
	of the current engines, only `"latex"` will respect them.
- Alignment option `""` (empty string) to align the table, but omit
	alignment indication in some table styles.

### Changed
- `table.print_table()` now expects the `engine` as second parameter.
	This `engine` takes care of the look and feel of the 
- Replacement is now a dictionary, which makes replacing values both more
	flexible and more powerful.
- Refactored many internal functions to be more error-tolerant

### Fixed
- Fixed the issue, where data was silently dropped, when a row contained
	fewer cells that others. Instead, those missing cells are now filled
	in with empty strings.
- Minor documentation inconsistencies

## [v0.1.1] – 2023-02-12

### Fixed

- Added an optional argument `return_lines`, which defaults to `False`.
	This helps with interactive sessions, where the table previously was printed twice:
	1. once nice as expected and
	2. once the list of lines by the Python interpreter: list of lines as is 


## [v0.1] – 2023-01-12

First published version.


[unreleased]: https://github.com/bertramrichter/brplotviz/compare/v0.2.1..master
[v0.2.1]: https://github.com/bertramrichter/brplotviz/compare/v0.2..v0.2.1
[v0.2]: https://github.com/bertramrichter/brplotviz/compare/v0.1.1..v0.2
[v0.1.1]: https://github.com/bertramrichter/brplotviz/releases/compare/v0.1..v0.1.1
[v0.1]: https://github.com/bertramrichter/brplotviz/releases/tag/v0.1
