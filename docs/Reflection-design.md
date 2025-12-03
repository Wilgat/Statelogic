# Design Document for `Reflection`

## Overview
The `Reflection` class is a foundational component of the `StateLogic` module, designed to facilitate method introspection and dynamic method calls in stateful applications, particularly within Finite State Machines (FSMs). Implemented in Python and optimized through Cython compilation, the `Reflection` class enhances the flexibility and adaptability of applications by allowing runtime inspection and invocation of methods. It supports both Python 2 and 3, ensuring compatibility across various environments, including Ubuntu 24.04 with Python 3.12. The class is integral to the operation of FSMs, providing essential functionality for checking and invoking event handlers, enabling robust application behavior without the need for extensive boilerplate code.

## Purpose
The `Reflection` class serves to:
- Enable dynamic method checking and invocation, enhancing the flexibility of stateful applications.
- Provide a mechanism to verify the existence of methods in a target class, allowing for safe dynamic calls.
- Support the integration of event handlers within FSMs, ensuring that state transitions can trigger appropriate actions.
- Ensure cross-platform compatibility and optimize performance through Cython compilation, making it suitable for high-frequency method calls in CLI applications.

## Functionality
The `Reflection` class provides the following key features:

### Method Introspection
- **Dynamic Method Checking**: Implements `hasFunc(name)` to verify if a method with the specified name exists in the target class.
- **Method Invocation**: Provides a `func(name, *args, **kwargs)` method that safely calls the specified method if it exists, allowing for flexible event handling.

### Integration with FSM
- **Event Handling**: Facilitates the registration and invocation of event handlers, enabling FSM to execute specific actions during state transitions.
- **Method Binding**: Supports dynamic binding of event handlers to states and transitions within the FSM, reducing boilerplate and enhancing code maintainability.

### Compatibility
- **Cross-Platform Support**: Ensures compatibility with Linux, Windows, and macOS, leveraging standard library modules for environment detection and method invocation.
- **Python 2/3 Compatibility**: Uses try-except fallbacks for method access to maintain functionality across different Python versions.

### Performance
- **Cython Optimization**: Compiled as part of the `StateLogic.pyx`, benefiting from C-level performance for method access and invocation, minimizing overhead during runtime.

## Design Considerations
### Robustness in Finite State Machines
The design of the `Reflection` class emphasizes robustness, particularly in the context of Finite State Machines (FSMs). This is achieved through the following mechanisms:

- **Error Avoidance**: The `Reflection` class is structured to ignore invalid method invocations gracefully. When a method is not found (e.g., due to incorrect naming or absence), the `func(name, *args, **kwargs)` method does not raise exceptions. Instead, it can return a default value or simply do nothing, ensuring that the FSM continues its operation without interruption.

- **Safe Method Checking**: The `hasFunc(name)` method allows the FSM to determine whether a method exists before attempting to invoke it. This preemptive check prevents execution halts that could arise from calling non-existent methods. Such a design pattern is crucial in maintaining the flow of control within state transitions.

- **Flexible Event Handling**: By supporting dynamic binding of event handlers to states and transitions, the `Reflection` class allows FSMs to adapt to various conditions without hardcoding specific behaviors. This flexibility helps in managing unexpected scenarios, as the system can continue to function even if certain expected methods are not available.

- **Encapsulation of State Logic**: The methods provided by the `Reflection` class are designed to be invoked through a public interface, which helps encapsulate the internal workings of the FSM. This ensures that incorrect settings or configurations do not lead to system failures, as the class maintains a clear separation between internal logic and external usage.

## Implementation Details
- **Constructor (`__init__`)**:
  - **Parameters**: `fromClass` (the target class to reflect upon).
  - **Behavior**: Initializes the `Reflection` instance for the specified class and sets up the necessary internal state for method introspection.
  - **Returns**: An instance of `Reflection`.

- **Key Methods**:
  - **`hasFunc(name)`**: Checks if the method `name` exists in `fromClass`, returning a boolean.
  - **`func(name, *args, **kwargs)`**: Attempts to invoke the method `name` with provided arguments, returning the result or a default value if the method does not exist.

## Testing
The `Reflection` class is tested via `tests/test_reflection.py`, covering:
- Method existence checks (valid and invalid method names).
- Method invocation with valid arguments.
- Graceful handling of non-existent methods.

Run tests with:
```bash
cd StateLogic/src
python3 setup.py build_ext --inplace
python3 -m unittest tests/test_reflection.py
```

## Future Enhancements
- **Enhanced Error Reporting**: Introduce detailed logging or exceptions for failed method calls to assist in debugging.
- **Support for Method Overloading**: Allow for more flexible method resolution based on argument types or counts.
- **Documentation Improvements**: Provide more comprehensive usage examples and documentation to facilitate user understanding.

## Dependencies
- **Build**: Requires `cython` for compilation (`pip install cython` via `pyenv`).
- **Runtime**: None; utilizes standard library modules (`os`, `re`).
- **Environment**: Optimized for Ubuntu 24.04, Python 3.12, with cross-platform compatibility.

## Folder Structure
The `Reflection` class is part of the `StateLogic` project:
```
StateLogic/
├── src/
│   ├── StateLogic.pyx  # Contains Attr, Transition, FSM, and Reflection classes
│   └── setup.py
├── tests/
│   └── test_reflection.py
├── docs/
│   └── Reflection-design.md  # This document
├── build/
│   └── lib/
│       ├── StateLogic.cpython-312-x86_64-linux-gnu.so
├── cy-master.ini
└── README.md
```

This document outlines the design and functionality of the `Reflection` class within the `StateLogic` framework, emphasizing its role in enhancing the flexibility and robustness of stateful applications.