# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),  
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.1] - 2025-12-03

**Build tools & compilation enhancements**

### Added
- `cy-master.py`: Tool for compiling the project to a CPython .so shared library.
- `dependency-merge.py`: Script to merge dependencies and generate an all-in-one `src/statelogic_combined.pyx` file for Cython compilation.
- `./build.sh test`: New command in build script to run the pytest test suite, with support for passing options (e.g., `./build.sh test -v` or `./build.sh test -k test_name`).

## [1.2.0] - 2025-12-02

**Major architecture & quality upgrade — now a serious Python library**

### Added
- Full **src/ layout** (`src/statelogic`) — modern, explicit, PyPI-best-practice packaging
- Split monolithic code into clean, logical modules:
  - `Attr.py` — dynamic attribute system
  - `Transition.py` — transition metadata
  - `Reflection.py` — introspection helpers
  - `FSM.py` — core finite state machine engine
  - `StateLogic.py` — public facade and logging layer
  - `AppData.py`, `Sh.py`, `Signal.py` — utilities
- `__init__.py` now cleanly re-exports only the public API
- Added `__version__ = "1.2.0"` in package
- Comprehensive test suite preserved and now runs cleanly in new layout

### Changed
- **State safety enforced via `useChoiceOnly=True` + `stateChoice`**  
  → Direct `fsm.state("invalid")` is now **silently ignored** unless the state was registered via `.transition()`
  → First valid state can only be set **after** defining transitions
  → This is now the **core philosophy**: *“A state machine must never lie about its state.”*
- `Attr.value()` now respects `useChoiceOnly` flag — enables secure enum-like behavior
- Improved internal consistency and hook reliability

### Fixed
- Eliminated stale `__pycache__` import issues by adopting proper src layout
- Resolved `StateLogic` being imported as module instead of class
- Fixed edge cases in `fire()` vs direct method calls
- All 49 tests now pass reliably in clean environments

### Security
- State integrity is now **guaranteed by design** — impossible to enter undefined states
- Direct state manipulation is blocked — only valid transitions allowed

---

## [1.1.0] - 2025-03-28

More aligned with TypeScript version (StateSafe)

### Added
- More examples in `README.md`
- Added `patchVersion`
- Added unittest suite
- Allow extension of existing objects with StateLogic behavior
- `on`, `after`, `before` hooks can now access:
  - `transitionName()`
  - `fromState()`, `toState()`, `nextState()`

### Fixed
- Fixed `__this__` error in unittest context

---

## [1.0.0] - 2025-03-20

Initial public release

- Pure Python finite state machine with colored terminal logging
- Dynamic attributes via `Attr`
- Hook system: `before`, `on`, `after`
- Signal handling, shell utilities, app metadata
- MIT licensed