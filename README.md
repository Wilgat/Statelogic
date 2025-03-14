# StateLogic

StateLogic is a Python library for finite state machine with colored messages in the terminal.

## Installation

You can install the package using pip3:

```bash
pip3 install statelogic
```

## Usage

Here’s a basic example of how to use StateLogic:

```python
from statelogic import StateLogic

# Create an instance of StateLogic
state_logic = StateLogic()
```

## Using it as Finite State Machine
```
>>> from statelogic import StateLogic
>>> s=StateLogic()
>>> s.transition("freeze","LIQUID","SOLID")
<statelogic.StateLogic object at 0x103188950>
>>> s.transition("melts","SOLID","LIQUID")
<statelogic.StateLogic object at 0x103188950>
>>> s.state("anything else")
<statelogic.StateLogic object at 0x103188950>
>>> s.state()
>>> s.state("SOLID")
<statelogic.StateLogic object at 0x103188950>
>>> s.state()
'SOLID'
>>> s.states()
['LIQUID', 'SOLID']
>>> s.transitions()
['freeze', 'melts']
```


## Using the Attr Class

```
from statelogic import Attr

class MyClass:
    def __init__(self):
        self.name = Attr(self, attrName="name", value="Default Name")

my_instance = MyClass()
print(my_instance.name())  # Output: Default Name

# Update the name
my_instance.name("New Name")
print(my_instance.name())  # Output: New Name
```


## Use the critical message method
```
state_logic.criticalMsg("This is a critical message", tag="ERROR")
```

## Features

- Colorful terminal messages
- Easy to use for state management
- Customizable message formatting
- Dynamic attribute management with Attr
- State transition definitions with Transition
- Reflection capabilities with Reflection
- Finite state machine functionality with FSM
- Application data management with AppData
- Signal handling with Signal
- Shell command and environment utilities with Sh

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
