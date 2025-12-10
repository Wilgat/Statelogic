# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- Python 2.7 compatibility layer for the entire `statelogic` module
- Full backward compatibility with Python 2.7 syntax and standard library limitations
- Updated all core classes to support both Python 2.7 and Python 3.6+

### Changed
- `src/statelogic/AppData.py` – refactored for 2.7 string/unicode handling
- `src/statelogic/Attr.py` – replaced f-strings and type annotations with 2.7-compatible code
- `src/statelogic/FSM.py` – adjusted exception handling and super() calls
- `src/statelogic/Reflection.py` – reworked dynamic attribute access for old-style classes
- `src/statelogic/Sh.py` – replaced subprocess calls using 2.7-compatible patterns
- `src/statelogic/Signal.py` – updated signal handling for Python 2.7
- `src/statelogic/StateLogic.py` – major compatibility refactor (dict methods, string handling, etc.)
- `src/statelogic/Transition.py` – adjusted lambda and default argument behavior

### Fixed
- Various Python 2.7 syntax errors and runtime incompatibilities

### Testing
- Added/updated comprehensive Python 2.7 test coverage:
  - `test/testMatter.py`
  - `test/testStateLogic.py`
  - `test/testStateLogicExtends.py`
  - `test/testStateLogicIndependent.py`

### Housekeeping
- Added proper `.gitignore` rules for `__pycache__/`, `*.pyc` and temporary files
- Removed all bytecode files from version control

*Branch*: `feature/python-2.7-compat` → merged into `main` on 2025-12-10