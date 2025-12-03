# Design Documentation for `Attr`

## Overview
The `Attr` class is a Cython-based descriptor class within the `StateLogic` module, designed to provide dynamic, type-safe attribute management for Python applications, particularly within Finite State Machines (FSMs). It enables runtime addition of properties to a class, supporting both single values and lists with features like validation, autostripping, readonly protection, and callback triggers. Integrated into the `StateLogic` framework, `Attr` is optimized for performance via Cython compilation and supports Python 2/3 compatibility. It is primarily used in stateful applications (e.g., CLI tools, installers) on Ubuntu 24.04 with Python 3.12, leveraging standard library modules (`os`, `re`, `datetime`, `signal`) without external dependencies. The class is designed for extensibility, allowing subclasses to define custom attributes while maintaining a fluent API through method chaining. Within the FSM, `Attr` manages state attributes and supports the `Transition` class by storing event names, target states, and associated metadata.

## Purpose
The `Attr` class serves as a flexible mechanism to:
- Dynamically add attributes to a class at runtime, reducing boilerplate in stateful FSM applications.
- Manage single values or lists with validation (e.g., restricting event names or target states to a predefined set).
- Support features like autostripping for strings, readonly protection, and sorting for lists.
- Trigger callbacks on value changes, enabling reactive behavior in FSM state transitions.
- Ensure cross-platform compatibility (Linux, Windows, macOS) with fallbacks for Python 2/3.
- Optimize performance through Cython compilation, suitable for high-frequency attribute access in FSM loops.
- Support the `Transition` class by managing attributes like event names and target states, ensuring robust state transitions.

## Functionality
The `Attr` class provides the following key features:

### Descriptor Protocol
- **Role**: Acts as a descriptor, implementing `__get__` and `__set__` to manage attribute access and modification.
- **Access**: Attributes are accessed via `instance.attrName()` (get) and `instance.attrName(value)` (set), returning the value/list or the parent class for chaining.
- **Internal Storage**: Stores state in `fromClass._[attrName]`, containing a dictionary with keys: `value`, `list`, `readonly`, `autostrip`, `sorting`, `onChange`, `valueChoice`, and `class` (the `Attr` instance).

### Attribute Management
- **Dynamic Attributes**: Adds properties to a class via `setattr(fromClass, attrName, self)`, allowing runtime attribute creation.
- **Single Values**: Managed via the descriptor's `__call__` method, supporting strings (e.g., event names, target states), numbers, or other types with optional autostripping and validation against `valueChoice`.
- **Lists**: Managed via the descriptor's `__call__` method, supporting assignment of lists (e.g., multiple events triggering a transition), with sorting and autostripping options. Lists are initialized with `value=[]` for list attributes.
- **Readonly Protection**: Prevents changes to `value` or `list` if `readonly=True`, retaining the initial value (e.g., `[]` for lists) for subsequent set attempts, useful for immutable state or transition metadata.
- **Validation**: Restricts `value` to a predefined `valueChoice` list (e.g., valid state names in an FSM), ignoring invalid assignments.
- **Callbacks**: Invokes an `onChange` callback when `value` changes, enabling reactive updates in FSM transitions (e.g., logging state changes).

### Compatibility
- **Python 2/3**: Handles differences via try-except fallbacks for `basestring`, `input`, and `__file__`.
- **Cross-Platform**: Supports Linux (Ubuntu 24.04), Windows, and macOS, with considerations for shell detection and path handling (via `os.path` and `re` for normalization).

### Performance
- **Cython Optimization**: Compiled as part of `StateLogic.pyx`, benefiting from C-level performance for attribute access in FSM loops.
- **Minimal Overhead**: Simple initialization and method calls ensure low computational cost, suitable for FSMs with frequent attribute access during state transitions.

### Test Case Findings
The design of the `Attr` class, used by `Transition` and `FSM`, ensures robustness:
- **Invalid Input Handling**: Tests confirm that reserved or empty names result in an `Attr` instance being created, but the attribute is not set on the class, and it is not added to `attrList`, ensuring FSM continuity.
- **Error Avoidance**: Readonly attributes ignore modifications, and invalid value assignments (outside `valueChoice`, e.g., invalid state names) are ignored, preventing FSM interruptions. Readonly lists retain their initial empty list (`[]`) when changes are attempted.
- **Encapsulation Issues**: Direct `_` access raises `AttributeError` on `Attr` descriptors (e.g., `attrName._`), enforcing public interface use.
- **Descriptor Interface**: All interactions must use `instance.attrName()`, as internal state access causes errors, critical for `Transition` attribute consistency.
- **Transition Testing**: Tests verify that `Attr` correctly handles `Transition` attributes (e.g., `onEvent`, `targetState`), ignoring invalid assignments (e.g., non-existent states) and maintaining readonly properties.

#### Importance of Avoiding Errors
The FSM design, including `Attr` and `Transition`, prioritizes robustness by avoiding exceptions during normal operation and ignoring incorrect options:
- **Uninterrupted Execution**: Invalid inputs (e.g., reserved event names, invalid target states) are ignored, allowing the FSM to continue without crashes, critical for CLI tools or installers.
- **Graceful Degradation**: Safe defaults (e.g., empty list for readonly lists) maintain functionality even with misconfigurations.
- **User Experience**: No abrupt errors enhance usability in interactive FSM-driven applications.
- **Test Implications**: Tests verify that invalid operations (e.g., reserved names, invalid states) are ignored, and valid operations execute correctly.

## Design Considerations
- **Descriptor-Based**: Uses the descriptor protocol to intercept attribute access, enabling centralized logic for validation and state management in FSMs.
- **Error-Free Operation**: Ignores invalid inputs (e.g., reserved names, duplicate list items, invalid value assignments) without raising exceptions, ensuring uninterrupted execution in stateful FSM applications.
- **Encapsulation**: Internal state is managed in `fromClass._[attrName]`, inaccessible directly (e.g., `instance.attrName._` raises `AttributeError`), enforcing the descriptor interface.
- **FSM Integration**: Designed for use in finite state machines, where `Attr` manages state attributes and supports the `Transition` class. Invalid operations (e.g., invalid event names or target states) are ignored to maintain FSM continuity, critical for CLI tools or installers.
- **Simplicity**: Focuses on attribute management, leaving higher-level FSM logic (e.g., state transitions, event handling) to classes like `FSM` and `Transition`.

## FSM Integration
The `Attr` class is tightly integrated with the `StateLogic` FSM framework:
- **State Attributes**: `Attr` manages state-specific attributes (e.g., current state name, event triggers) used by the `FSM` class to track state machine progress.
- **Transition Support**: The `Transition` class leverages `Attr` to store event names (e.g., `onEvent`), target states (e.g., `targetState`), and optional actions (e.g., callbacks via `onChange`). For example, a `Transition` might use `Attr` to define a readonly `targetState` to prevent unintended modifications during FSM execution.
- **Validation in Transitions**: The `valueChoice` feature ensures that only valid events or states are assigned, preventing invalid transitions (e.g., assigning a non-existent state is ignored).
- **Reactive Behavior**: The `onChange` callback supports reactive FSM behavior, such as logging or triggering side effects when a state attribute changes during a transition.
- **Encapsulation**: `Attr` ensures that transition-related attributes are only modified through the descriptor interface (`instance.attrName()`), maintaining FSM consistency.
- **Error Avoidance**: By ignoring invalid inputs (e.g., reserved event names, invalid target states), `Attr` ensures the FSM continues running without interruptions, aligning with the `Transition` class's error-free design.
- **Transition Addition**: The `FSM` class may support adding transitions via a method like `add_transition`, but tests conditionally handle its absence to ensure robustness.

## Implementation Details
- **Constructor (`__init__`)**:
  - **Parameters**: `fromClass` (target class), `attrName` (attribute name, e.g., `event` or `targetState`), `value` (initial value, e.g., string or `[]` for lists), `readonly` (bool), `autostrip` (bool), `sorting` (bool), `onChange` (callback), `valueChoice` (list of valid values, e.g., valid state names).
  - **Behavior**: Creates an `Attr` instance and validates `attrName` against `RESERVED` (Python keywords and `attrList`, `hasattr`). For invalid or empty `attrName`, the instance is created but the attribute is not set via `setattr`, and it is not added to `attrList`. Initializes `fromClass._[attrName]` with configuration for valid names.
  - **Returns**: An `Attr` instance, even for invalid `attrName`.

- **Methods**:
  - **`valueChoice(x=None)`**: Gets/sets the list of valid values in `fromClass._[attrName]["valueChoice"]`. Used for validation in single value assignments (e.g., restricting to valid FSM states).
  - **Descriptor `__call__`**: Handles both getting and setting values/lists:
    - **Get**: Returns `fromClass._[attrName]["list"]` if set, else `fromClass._[attrName]["value"]`.
    - **Set**: For single values, applies autostrip, `valueChoice` validation, and `onChange` callbacks. For lists, applies autostrip and sorting if enabled, storing in `fromClass._[attrName]["list"]`. Ignores changes if `readonly=True`.

- **Internal State**:
  - Stored in `fromClass._[attrName]`, a dictionary with:
    - `value`: Single value (e.g., event name or target state, default `None` or `[]` for lists).
    - `list`: List of items (e.g., multiple events, default `None` or `[]` if initialized as a list).
    - `readonly`: Prevents changes if `True` (e.g., retains `[]` for lists).
    - `autostrip`: Strips strings if `True` (e.g., for clean event names or list items).
    - `sorting`: Sorts lists if `True` (e.g., for ordered event lists).
    - `onChange`: Callback function for value changes (e.g., logging transitions).
    - `valueChoice`: List of valid values for `value` (e.g., valid FSM states).
    - `class`: Reference to the `Attr` instance.

## Usage Example
### Example 1: Valid Attribute Access in FSM
```python
from StateLogic import Attr, Transition, FSM

class MyFSM(FSM):
    def __init__(self):
        super().__init__()
        Attr(self, 'currentState', value='idle', valueChoice=['idle', 'running', 'stopped'], readonly=False)
        Attr(self, 'event', value='start', valueChoice=['start', 'stop'], readonly=True)
        if hasattr(self, 'add_transition'):
            self.add_transition(Transition('idle', 'start', 'running'))

fsm = MyFSM()
print(fsm.currentState())  # Output: idle
fsm.event('stop')          # Ignored due to readonly
print(fsm.event())         # Output: start
fsm.currentState('running')
print(fsm.currentState())  # Output: running
```

### Example 2: List Management
```python
class MyFSM(FSM):
    def __init__(self):
        super().__init__()
        Attr(self, 'events', value=[], sorting=True)

fsm = MyFSM()
fsm.events(['stop', 'start'])
print(fsm.events())  # Output: ['start', 'stop'] (sorted)
```

### Example 3: Invalid Name in Transition
```python
class MyFSM(FSM):
    def __init__(self):
        super().__init__()
        Attr(self, 'if', value='start')  # Invalid name
        if hasattr(self, 'add_transition'):
            self.add_transition(Transition('idle', 'start', 'running'))

fsm = MyFSM()
print(hasattr(fsm, 'if'))  # Output: False
```

## Constraints and Limitations
- **Cython Compilation**: Requires `cython` for building (`pip install cython` via `pyenv`). Methods must be `cpdef` for Python accessibility.
- **Internal State Access**: Direct access to `fromClass._[attrName]` is discouraged and may fail in compiled modules (e.g., `TypeError: 'Attr' object is not subscriptable`).
- **Platform Differences**: Optimized for Ubuntu 24.04 with Python 3.12. Windows/macOS may require testing for path handling or shell detection fallbacks.
- **List vs. Value**: List attributes must be initialized with `value=[]` to ensure proper list handling, as single values and lists are managed through the same descriptor interface.
- **Transition Method**: The `FSM` class may use a method like `add_transition` for transitions, but its presence is not guaranteed, requiring conditional checks in applications.

## Testing
The `Attr` class is tested via `tests/test_attr.py`, covering:
- Initialization (valid, invalid, empty names).
- Single value management (set/get, autostrip, readonly, choices, callbacks).
- List management (set/get, autostrip, readonly, sorting).
- Descriptor behavior (chaining, value/list retrieval).
- FSM integration (attribute management for state transitions).

Run tests with:
```bash
cd StateLogic/src
python3 setup.py build_ext --inplace
python3 -m unittest tests/test_attr.py
```

## Future Enhancements
- Expose `valueChoice` through the descriptor interface for direct configuration (e.g., `instance.attrName.valueChoice(['option1', 'option2'])`).
- Add support for type validation beyond `valueChoice` (e.g., enforce `int` or `str` for transition attributes).
- Enhance error reporting for invalid inputs (e.g., raise exceptions instead of silent failures for debugging FSM issues).
- Provide a method to inspect attribute configuration (e.g., readonly status, sorting) for FSM debugging.
- Clarify `FSM` transition method (e.g., standardize `add_transition`) for consistent integration.

## Dependencies
- **Build**: `cython` (install via `pyenv install 3.12.0; pyenv shell 3.12.0; pip install cython`).
- **Runtime**: None (uses standard library: `os`, `re`, `datetime`, `signal`).
- **Environment**: Optimized for Ubuntu 24.04, Python 3.12. Use `pyenv` for isolation.

## Folder Structure
The `Attr` class is part of the `StateLogic` project:
```
StateLogic/
├── src/
│   ├── StateLogic.pyx  # Contains Attr, Transition, FSM classes
│   └── setup.py
├── tests/
│   └── test_attr.py
├── docs/
│   └── Attr-design.md  # This document
├── build/
│   └── lib/
│       ├── StateLogic.cpython-312-x86_64-linux-gnu.so
├── cy-master.ini
└── README.md
```