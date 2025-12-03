# Design Documentation for `FSM`

## Overview
The `FSM` (Finite State Machine) class is a core component of the `StateLogic` module, designed to manage state transitions and events in stateful applications, such as CLI tools or installers. Implemented in Python and integrated with the Cython-compiled `StateLogic.pyx`, it inherits from the `Reflection` class and uses the `Attr` and `Transition` classes to manage states, transitions, events, and methods dynamically. The `FSM` class ensures robust operation by ignoring invalid inputs (e.g., reserved names, invalid transitions) without raising exceptions, allowing uninterrupted execution. It is optimized for use on Ubuntu 24.04 with Python 3.12, supporting cross-platform compatibility (Linux, Windows, macOS) with no external dependencies beyond `cython` for compilation.

## Purpose
The `FSM` class serves to:
- Manage a finite state machine with dynamic states, transitions, events, and methods.
- Provide a flexible interface for defining transitions, attaching event handlers (`before`, `on`, `after`), and executing state changes.
- Ensure robustness by ignoring invalid inputs (e.g., reserved names, duplicate transitions) without raising errors, maintaining FSM continuity.
- Integrate with `Attr` for attribute management and `Transition` for state transition definitions.
- Optimize performance through Cython compilation, suitable for high-frequency state transitions in CLI applications.

## Functionality
The `FSM` class provides the following key features:

### State and Transition Management
- **Attributes** (via `Attr` descriptors):
  - `state`: The current state of the FSM (readonly, string).
  - `nextState`: The target state during a transition (readonly, string, defaults to `""`).
  - `methods`: A list of method names registered with the FSM (read/write, list).
  - `events`: A list of event names (read/write, list).
  - `transitions`: A list of `Transition` objects (read/write, list, non-sorting).
  - `states`: A list of valid state names (read/write, list).
- **Transitions**:
  - Defined via `transition(name, fromState, toState)`, which creates a `Transition` object and a corresponding method (`name`) to execute the transition.
  - Validates `name` against `Attr.RESERVED` and existing events, ignoring duplicates or invalid names.
  - Executes transitions with `before`, `on`, and `after` event handlers, updating `state` and logging changes if enabled.

### Event Handling
- **Methods**:
  - `before(name, foo)`: Registers a `before` event handler for a transition or event (e.g., `beforeStart()`).
  - `on(name, foo)`: Registers an `on` event handler for an event or state (e.g., `onStart()`, `onSTATE()`).
  - `after(name, foo)`: Registers an `after` event handler for a transition or event (e.g., `afterStart()`).
  - `method(name, foo)`: Registers a custom method on the FSM.
  - `fire(transition)`: Executes a transition method if it exists.
- **Dynamic Naming**: Uses naming conventions like `beforeName`, `onName`, `afterName`, with capitalization for events and uppercase for states (e.g., `onSTATE`).

### State Execution
- **State Change**:
  - The `transition` method creates a callable that checks the current state (`fromState`), executes `before`, `on`, and `after` handlers, updates `state`, and calls `onState(toState)`.
  - `stateChanged()` logs transitions if `STATE=show` or `state=show` is set in the environment or if `logTo()` is defined.
- **State Access**:
  - `fromState()`: Returns the source state of the current transition.
  - `toState()`: Returns the target state of the current transition.
  - `nextState()`: Returns the next state during a transition.
  - `transitionName()`: Returns the current transition name.

### Robustness
- **Error Avoidance**: Ignores invalid inputs (e.g., reserved names, duplicate transitions, invalid event handlers) without raising exceptions, ensuring uninterrupted FSM execution.
- **Encapsulation**: Uses `Attr` for attribute management, with `self._` access raising `AttributeError` in Cython for `Attr` descriptors, though `FSM._` is accessible (discouraged).
- **Initialization**: Supports both standalone (`FSM()`) and class-bound (`FSM(fromClass)`) usage, dynamically attaching methods and attributes.

### Compatibility
- **Python 2/3**: Uses `basestring` fallbacks for string handling.
- **Cross-Platform**: Supports Linux (Ubuntu 24.04), Windows, and macOS via standard library (`os`, `re`, `datetime`, `signal`).
- **No Dependencies**: Requires only `cython` for compilation.

### Performance
- **Cython Optimization**: Benefits from C-level performance for attribute access and method execution.
- **Dynamic Binding**: Uses `__get__` for method binding, minimizing overhead while supporting flexibility.

## Design Considerations
- **Attr and Transition Integration**: Leverages `Attr` for type-safe, readonly attribute management and `Transition` for defining state transitions, reducing `FSM` complexity.
- **Error-Free Operation**: Ignores invalid inputs (e.g., reserved names, duplicate transitions) by skipping or using safe defaults (e.g., `""` for names), ensuring robustness.
- **Encapsulation**: Relies on `Attr` to prevent direct `_` access (e.g., `fsm.state._` raises `AttributeError`), though `fsm._` is accessible in Cython (discouraged).
- **Flexibility**: Supports dynamic method and event registration, allowing customization for various FSM use cases.
- **Logging**: Provides optional state change logging via `stateChanged()`, configurable through environment variables or `logTo()`.

## Implementation Details
- **Constructor (`__init__`)**:
  - **Parameters**:
    - `fromClass`: Optional class to bind the FSM to; defaults to `self` if `None`.
  - **Behavior**:
    - Initializes `Attr` descriptors for `state`, `nextState`, `methods`, `events`, `transitions`, and `states`.
    - Dynamically binds methods (`transition`, `before`, `on`, `after`, `method`, `fire`, `stateChanged`, `hasFunc`, `transitionName`, `onState`) to `fromClass`.
    - Sets `fromClass` for method delegation if provided.
  - **Returns**: An `FSM` instance or `fromClass` with bound methods.

- **Key Methods**:
  - **`__name_convert__(input_string)`**: Converts snake_case to CamelCase (e.g., `my_state` to `MyState`) for state event names.
  - **`fire(transition)`**: Executes a transition method if it exists in `methods`.
  - **`before(name, foo)`**, **`on(name, foo)`**, **`after(name, foo)`**: Register event handlers for transitions or states, ignoring duplicates.
  - **`method(name, foo)`**: Registers a custom method, ignoring duplicates.
  - **`transition(name, fromState, toState)`**: Creates a `Transition` object and a method to execute the transition, handling `before`, `on`, `after`, and state updates.
  - **`stateChanged(func="")`**: Logs state changes if enabled, using `infoMsg` if available.
  - **`fromState()`**, **`toState()`**, **`