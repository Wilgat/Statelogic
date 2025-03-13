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

## Using the FSM Class
```
from statelogic import FSM

class MyFSM(FSM):
    def __init__(self):
        super().__init__(self)
        self.state("INITIAL")
        self.transition("start", "INITIAL", "RUNNING")
    
    def onSTART(self):
        print("Transitioning to RUNNING state")

fsm_instance = MyFSM()
fsm_instance.start()
```

## Using the AppData Class
```
from statelogic import AppData

app_data = AppData()
app_data.appName("My Application")
app_data.author("Your Name")

print(app_data.appName())  # Output: My Application
print(app_data.author())    # Output: Your Name
```

Addition methods in AppData


```
app_data.majorVersion(1)
app_data.minorVersion(0)

print(app_data.version())  # Output: 1.0
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

## Using Transition Class
```
from statelogic import Transition
transition = Transition(name="Start to End", fromState="START", toState="END")
print(transition.name)        # Output: Start to End
print(transition.fromState)   # Output: START
print(transition.toState)     # Output: END
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
