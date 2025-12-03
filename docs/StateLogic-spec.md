# Design Document for `StateLogic`

## Overview
The `StateLogic` class is a comprehensive Cython-based foundation module for building stateful applications in Python, integrating attribute management, finite state machines (FSM), signal handling, shell detection, and colored terminal messaging. It combines multiple base classes (`AppData`, `Sh`) to provide a robust framework for self-managing apps, such as installers or CLI tools that need dynamic attributes, state transitions, error states, and user feedback. Designed for performance via Cython compilation (`.pyx` file), it supports Python 2/3 compatibility through try-except fallbacks and targets environments like Ubuntu 24.04 with Python 3.12 (no venv by default), where behaviors like path normalization (e.g., `/\./` regex) and shell detection (e.g., `/bin/bash`) are optimized for Linux filesystems—note that on Windows or macOS, shellCmd() and username() may vary due to pwd module availability and os.getuid() limitations, so test cross-platform . No pip dependencies are required in the core code, but for building the Cython extension, install Cython via pyenv for isolation: Run `curl https://pyenv.run | bash` (add to `~/.bashrc` and source it), then `pyenv install 3.12.0` and `pyenv shell 3.12.0` before `pip install cython`—this ensures flexibility without affecting the system Python on Ubuntu . The module promotes clean, modular code by dynamically injecting methods (e.g., via `__get__`) and using Attr for lazy attributes, reducing boilerplate in subclasses like installers .

## The folder structure for the project: StateLogic
 * Project: StateLogic is a Cython (CyMaster type) project!
     ```
    Statelogic/
    ├── .gitignore
    ├── CHANGELOG.md
    ├── LICENSE
    ├── README.md
    ├── build.sh
    ├── docs/
    │   ├── Attr-design.md
    │   ├── CHANGELOG.md
    │   ├── FSM-design.md
    │   ├── Reflection-design.md
    │   ├── StateLogic-spec.md
    │   ├── Transition-design.md
    │   ├── folder-structure.md
    │   └── spec.md
    ├── setup.py
    ├── src/
    │   └── statelogic/
    │       ├── AppData.py
    │       ├── Attr.py
    │       ├── FSM.py
    │       ├── Reflection.py
    │       ├── Sh.py
    │       ├── Signal.py
    │       ├── StateLogic.py
    │       ├── Transition.py
    │       └── __init__.py
    └── test/
        ├── testMatter.py
        ├── testStateLogic.py
        ├── testStateLogicExtends.py
        └── testStateLogicIndependent.py
    ```
    
### cy-master.ini
 * The cy-master.ini file serves as the primary configuration file for CyMaster-type Cython projects:
    ```
    [project]
    srcFolder = src
    buildFolder = build
    targetName = StateLogic
    targetType = so
    ```
## Target Operating System
Primarily optimized for Ubuntu 24.04 LTS (default) with Python 3.12, leveraging Unix-like features such as `os.getuid()`, `pwd` module for usernames, and signal handling (e.g., SIGINT for Ctrl+C). It includes cross-platform adaptations: shell detection covers Linux shells (`/bin/bash`, `/bin/zsh`), Windows (`cmd.exe`, PowerShell, GitBash), and handles GitBash specially for color disabling (useColor=False). Path handling uses `os.path` implicitly via re for normalization, but filesystem differences (e.g., Windows drive letters) may require adjustments—use `pyenv` for testing multiple Python versions without affecting the system Python .

## Required Classes

### Attr Class
- **Description**: Descriptor class for dynamic attribute management, supporting values, lists, readonly, autostrip, sorting, onChange callbacks, and valueChoice validation. Used in `FSM` and `Transition` for state attributes.
- **Key Features**: Chaining API (e.g., `attr.value('val')`), error-free operation (ignores invalid assignments).
- **Usage in FSM**: Manages `state`, `methods`, `events`, `transitions`, and `states` as `Attr` descriptors.

### Transition Class
- **Description**: Represents FSM transitions with readonly attributes (`name`, `fromState`, `toState`) via `Attr`. Handles invalid names by setting `name = ""`.
- **Key Features**: Simple initialization, encapsulation (prevents `_` access in Cython).
- **Usage in FSM**: Stored in `transitions` list, used to define FSM transitions.

### Reflection Class
- **Description**: Base class for method introspection (e.g., `hasFunc`, `func`).
- **Key Features**: Checks and calls methods on `fromClass` or `self`.
- **Usage in FSM**: Inherited by `FSM` for dynamic method calls (e.g., `hasFunc` for event handlers).

## Core Functionalities

1. **Attribute Management (via Attr)**:
   - Dynamic attributes for states, events, methods, and transitions.
   - Readonly protection and validation for FSM consistency.

2. **State Transitions**:
   - Define transitions via `transition(name, fromState, toState)`, creating callable methods and `Transition` objects.
   - Execute transitions with `fire(name)`, handling `before`, `on`, `after` hooks.
   - Ignore invalid or duplicate transitions without errors.

3. **Event Handlers**:
   - Register `before(name, foo)`, `on(name, foo)`, `after(name, foo)` for transitions or states.
   - Supports state-specific handlers (e.g., `onSTATE`) via `onState(state)`.

4. **State Access**:
   - `fromState()`, `toState()`, `nextState()`, `transitionName()` for current transition details.
   - `state()` for current FSM state.

5. **Method Registration**:
   - `method(name, foo)` for custom methods.
   - Dynamic naming (e.g., `beforeName`, `onSTATE`) for consistency.

6. **Logging**:
   - `stateChanged(func="")` logs transitions if `STATE=show` or `logTo()` is set.

### FSM Robustness
- **Error Avoidance**: Ignores invalid inputs (e.g., reserved names, duplicate transitions, invalid handlers) without raising exceptions, ensuring uninterrupted execution.
- **Encapsulation**: Uses `Attr` to prevent direct `_` access on attributes, though `fsm._` is accessible (discouraged).

## Design Considerations
- **Attr and Transition Integration**: Uses `Attr` for attribute encapsulation and `Transition` for transition objects, simplifying FSM logic.
- **Error-Free Operation**: Aligns with FSM principles by ignoring invalid options (e.g., reserved names set to `""`), preventing interruptions in CLI tools.
- **Dynamic Binding**: Injects methods (e.g., `transition`, `fire`) and handlers at runtime, supporting extensibility.
- **Reflection**: Inherits `Reflection` for introspection, enabling dynamic calls.
- **Simplicity**: Focuses on core FSM features, leaving advanced logic (e.g., conditions, actions) to user-defined handlers.

## Implementation Details
- **Constructor (`__init__`)**:
  - **Parameters**: `fromClass` (optional target class).
  - **Behavior**: Initializes `Attr` descriptors for FSM attributes, binds methods to `fromClass`, sets `self.fromClass`.
  - **Returns**: The `FSM` instance or `fromClass` with bound methods.

- **Key Methods**:
  - **`__name_convert__(input_string)`**: Converts snake_case to CamelCase (e.g., `my_state` to `MyState`) for state handlers.
  - **`transition(name, fromState, toState)`**: Validates `name`, creates `Transition`, defines callable for execution, adds to `transitions`.
  - **`fire(transition)`**: Calls the transition method if it exists.
  - **`before(name, foo)`**, **`on(name, foo)`**, **`after(name, foo)`**: Register handlers, ignoring duplicates.
  - **`method(name, foo)`**: Registers custom methods, ignoring duplicates.
  - **`stateChanged(func="")`**: Logs state changes if enabled.
  - **`fromState()`**, **`toState()`**, **`nextState()`**, **`transitionName()`**: Return current transition details from `self._`.
  - **`onState(state)`**: Calls the `onSTATE` handler for a state.

- **Internal State**:
  - `self._`: Stores `transitionName`, `fromState`, `toState`, `nextState` (accessible in Cython but discouraged).
  - `Attr` descriptors for `state`, `methods`, `events`, `transitions`, `states`.

## Test Case Findings (From `Transition` Testing)
Testing the `Transition` class revealed insights into FSM robustness:
- **Invalid Input Handling**: Reserved or empty names result in `transition.name() == ""`, ignoring errors to maintain execution.
- **Error Avoidance**: Readonly modifications are ignored, ensuring no interruptions—tests verified no `TypeError` for invalid names.
- **Encapsulation Issues**: `Attr` descriptors raise `AttributeError` for `_` access, enforcing public interface; `Transition._` is accessible (potential weakness).
- **Descriptor Interface**: All interactions use `transition.name()`, avoiding `_` access, as it causes errors in Cython.

### Importance of Avoiding Errors
The FSM design prioritizes uninterrupted execution:
- **Robustness**: Ignores invalid options (e.g., reserved names, duplicate transitions) with safe defaults (`""`), preventing crashes in production.
- **Graceful Degradation**: Maintains FSM functionality even with misconfigurations.
- **User Experience**: No abrupt errors enhance usability in interactive tools.
- **Test Implications**: Tests verify ignored operations (e.g., reserved names return `""`), confirming FSM continuity.

## Usage Example
### Example 1: Basic FSM Transition
```python
from StateLogic import FSM

fsm = FSM()
fsm.transition("startToEnd", "start", "end")
fsm.state("start")  # Set initial state
fsm.fire("startToEnd")
print(fsm.state())  # Output: end
```

### Example 2: Event Handlers
```python
def before_startToEnd():
    print("Before transition")
def on_end():
    print("Entered end state")
fsm.before("startToEnd", before_startToEnd)
fsm.on("end", on_end)
fsm.state("start")
fsm.fire("startToEnd")  # Prints: Before transition, Entered end state
print(fsm.state())      # Output: end
```

### Example 3: Invalid Transition Name
```python
fsm.transition("if", "start", "end")  # Ignored due to reserved name
fsm.state("start")
fsm.fire("if")  # No effect
print(fsm.state())  # Output: start
```

## Constraints and Limitations
- **Cython Compilation**: Requires `cython` for building (`pip install cython` via `pyenv`). Methods like `__call__` for `Attr` must be `cpdef`.
- **Internal State Access**: Direct access to `fsm._` is possible in Cython but discouraged; `fsm.state._` raises `AttributeError`.
- **No Validation for States**: `fromState` and `toState` accept any values; future enhancements could add validation.
- **Logging Dependency**: `stateChanged` relies on environment variables or `infoMsg` for output, which may not always be configured.

## Testing
The `FSM` class is tested via `tests/test_fsm.py`, covering:
- Initialization (attribute and method binding).
- Transition creation (valid, invalid, duplicate).
- Event handler registration and execution.
- State changes and logging.
- Reflection methods (`hasFunc`, `func`).

Run tests with:
```bash
cd StateLogic/src
python3 setup.py build_ext --inplace
python3 -m unittest tests/test_fsm.py
```

## Future Enhancements
- **Condition/Action in Transitions**: Add support for conditions and actions in `transition` for more complex FSMs.
- **State Validation**: Use `Attr`’s `valueChoice` for `state` to restrict valid states.
- **Error Handling Options**: Allow configurable error modes (e.g., raise exceptions for invalid names).
- **Visualization**: Add methods to visualize FSM states and transitions.

## Dependencies
- **Build**: `cython` (install via `pyenv install 3.12.0; pyenv shell 3.12.0; pip install cython`).
- **Runtime**: None (uses standard library: `os`, `re`, `datetime`, `signal`).
- **Environment**: Optimized for Ubuntu 24.04, Python 3.12. Use `pyenv` for isolation.

## Folder Structure
The `FSM` class is part of the `StateLogic` project:
```
StateLogic/
├── src/
│   ├── StateLogic.pyx  # Contains Attr, Transition, FSM classes
│   └── setup.py
├── tests/
│   ├── test_attr.py
│   ├── test_transition.py
│   └── test_fsm.py
├── docs/
│   ├── FSM-design.md  # This document
│   ├── Attr-design.md
│   └── Transition-design.md
├── build/
│   └── lib/
│       ├── StateLogic.cpython-312-x86_64-linux-gnu.so
├── cy-master.ini
└── README.md
```