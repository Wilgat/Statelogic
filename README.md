# StateLogic

StateLogic is a Python library for finite state machine with colored messages in the terminal. Please go to the homepage for details.

The StateLogic Python finite state machine library offers several key features that facilitate the management of state transitions and event handling. Here’s a summary of its main features:

## Project Locations

## Python version
 - The project StateLogic (python implementation) corresponding at https://github.com/Wilgat/Statelogic and,
 - the pypi package is at https://pypi.org/project/statelogic/

## Typescript implementation
 - The project StateSafe (typescript implementation) is located at https://github.com/Wilgat/StateSafe and,
 - the npmjs package is at https://www.npmjs.com/package/statesafe

## Key Features
1. State Transitions:
 - Allows the definition of transitions between various states using a simple syntax (e.g., s.transition("event", "from_state", "to_state")).
2. State Management:
 - Provides methods to set and retrieve the current state (e.g., s.state("STATE_NAME") to set, and s.state() to get the current state).
3. Event Handlers:
 - Supports on methods (e.g., onMelts, onFreeze) to define custom actions that occur when a specific transition is initiated.
 - Allows for before methods (e.g., beforeMelts) to prompt or validate conditions before a transition occurs.
 - Supports after methods (e.g., afterMelts) to execute actions immediately after a transition is completed.
4. Custom Behavior:
 - Users can define custom functions for each of the on, before, and after methods, allowing for flexible and dynamic behavior during state transitions.
5. User Input Handling:
 - The library can incorporate user input to decide whether to allow certain transitions (e.g., confirming a melt transition).
6. Error Handling:
 - Can handle invalid state transitions gracefully, providing feedback when an attempt is made to set an invalid state.
7. Intuitive API:
 - Provides an easy-to-use and intuitive API for managing complex state behaviors, making it suitable for various applications, such as simulations, games, and control systems.
8. Clear State Representation:
 - States and transitions can be easily listed, providing clarity on the current configuration of the state machine.

## Installation

You can install the package using pip3:

```bash
pip3 install statelogic
```

## Usage

Here’s a basic example of how to create an object from StateLogic:

```python
from statelogic import StateLogic

# Create an instance of StateLogic
state_logic = StateLogic()
```

To create a new object with project details: {author}, {application}, {majorVersion}, {minorVersion}, {patchVersion}
```python
from statelogic import StateLogic

# Create an instance of StateLogic
state_logic = StateLogic()
state_logic.author("Test Author").appName("TestApp").majorVersion(1).minorVersion(0).patchVersion(0)
```

### Using it as Finite State Machine
```
from statelogic import StateLogic

# Create an instance of StateLogic
s = StateLogic()

# Define transitions between states of water
s.transition("freeze", "LIQUID", "SOLID")      # Liquid to Solid
s.transition("melts", "SOLID", "LIQUID")       # Solid to Liquid
s.transition("evaporate", "LIQUID", "GAS")      # Liquid to Gas
s.transition("condense", "GAS", "LIQUID")       # Gas to Liquid
s.transition("sublimate", "SOLID", "GAS")       # Solid to Gas
s.transition("deposition", "GAS", "SOLID")       # Gas to Solid
s.transition("cool", "GAS", "LIQUID")            # Gas to Liquid (cooling)
s.transition("heat", "LIQUID", "GAS")            # Liquid to Gas (heating)

# Example usage
s.state("anything else")          # Attempt to set an invalid state
print(s.state())                  # Get current state (should be None initially)
s.state("SOLID")                  # Set current state to SOLID
print(s.state())                  # Get current state (should be 'SOLID')

s.state("GAS")                    # Attempt to set current state to GAS (should fail)
print(s.state())                  # Get current state (should still be 'SOLID')

s.melts()                         # Go through the melts transition
print(s.state())                  # Get current state (should be 'LIQUID')

s.evaporate()                     # Go through the evaporate transition
print(s.state())                  # Get current state (should be 'GAS')

s.condense()                      # Go through the condense transition
print(s.state())                  # Get current state (should be 'LIQUID')

s.sublimate()                     # Go through the sublimate transition
print(s.state())                  # Get current state (should be 'GAS')

# List all defined states and transitions
print(s.states()) # Should return # Should return with alphabetical order ['LIQUID', 'SOLID', 'GAS']
print(s.transitions()) # Should return with alphabetical order ['condense', 'cool', 'deposition', 'evaporate', 'freeze', 'heat', 'melts', 'sublimate']
```

### Using the after prefix method
```
from statelogic import StateLogic

# Create an instance of StateLogic
s = StateLogic()

# Define the afterMelts function
def afterMelts():
    print("After melting, the ice is now water.")

# Define transitions between states of water
s.transition("freeze", "LIQUID", "SOLID")      # Liquid to Solid
s.transition("melts", "SOLID", "LIQUID")       # Solid to Liquid
s.transition("evaporate", "LIQUID", "GAS")      # Liquid to Gas
s.transition("condense", "GAS", "LIQUID")       # Gas to Liquid

# Register the afterMelts function to the melts transition
s.after("melts", afterMelts)

# Example usage
print(s.state())                  # Get current state (should be None initially)
s.state("SOLID")                  # Set current state to SOLID
print(s.state())                  # Get current state (should be 'SOLID')

s.melts()                         # Go through the melts transition
print(s.state())                  # Get current state (should be 'LIQUID')
```

### Using the before prefix methods
```
from statelogic import StateLogic

# Create an instance of StateLogic
s = StateLogic()

# Define the beforeMelts function
def beforeMelts():
    ans = input("Do you want to melt? (Y/N) ")
    if ans.upper() == "Y":
        return True
    return False

# Define transitions between states of water
s.transition("freeze", "LIQUID", "SOLID")      # Liquid to Solid
s.transition("melts", "SOLID", "LIQUID")       # Solid to Liquid
s.transition("evaporate", "LIQUID", "GAS")      # Liquid to Gas
s.transition("condense", "GAS", "LIQUID")       # Gas to Liquid

# Register the beforeMelts function to the melts transition
s.before("melts", beforeMelts)

# Example usage
print(s.state())                  # Get current state (should be None initially)
s.state("SOLID")                  # Set current state to SOLID
print(s.state())                  # Get current state (should be 'SOLID')

# Attempt the melts transition, user input will dictate if it proceeds
s.melts()                         # User decides whether to melt
print(s.state())                  # Get current state (should be 'SOLID' or 'LIQUID' based on input)

# Attempt the melts transition again
s.melts()                         # User decides whether to melt
print(s.state())                  # Get current state (should be 'LIQUID' if user chose to melt)
```

### Using the on prefix methods
```
from statelogic import StateLogic

# Create an instance of StateLogic
s = StateLogic()

# Define the onMelts function
def onMelts():
    print("The melting process has started.")

# Define transitions between states of water
s.transition("freeze", "LIQUID", "SOLID")      # Liquid to Solid
s.transition("melts", "SOLID", "LIQUID")       # Solid to Liquid
s.transition("evaporate", "LIQUID", "GAS")      # Liquid to Gas
s.transition("condense", "GAS", "LIQUID")       # Gas to Liquid

# Register the onMelts function to the melts transition
s.on("melts", onMelts)

# Example usage
print(s.state())                  # Get current state (should be None initially)
s.state("SOLID")                  # Set current state to SOLID
print(s.state())                  # Get current state (should be 'SOLID')

s.melts()                         # Trigger the melts transition
print(s.state())                  # Get current state (should be 'LIQUID')
```

### Using the Attr Class

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

### Use the criticalMssg method
```
from statelogic import StateLogic

# Create an instance of StateLogic
s = StateLogic()

# Set author, application name, and versioning information
s.author("Wilgat").appName("TestApp").majorVersion("1").minorVersion("0")

# Define transitions between states of water
s.transition("freeze", "LIQUID", "SOLID")      # Liquid to Solid
s.transition("melts", "SOLID", "LIQUID")       # Solid to Liquid

# Example usage to log a critical message
s.criticalMsg("Critical situation", "Attention")
```
The result should look likes:
```
2025-03-14 22:22:20.267361 TestApp(v1.0)  [Attention]: 
  Critical situation
```

### Use the safeMsg method
```
from statelogic import StateLogic

# Create an instance of StateLogic
s = StateLogic()

# Set author, application name, and versioning information
s.author("Wilgat").appName("TestApp").majorVersion("1").minorVersion("0")

# Define transitions between states of water
s.transition("freeze", "LIQUID", "SOLID")      # Liquid to Solid
s.transition("melts", "SOLID", "LIQUID")       # Solid to Liquid

# Example usage to log a safe message
s.safeMsg("This is a safe message indicating normal operation.", "TITLE")
```

### Using the infoMsg method
```
from statelogic import StateLogic

# Create an instance of StateLogic
s = StateLogic()

# Set author, application name, and versioning information
s.author("Wilgat").appName("TestApp").majorVersion("1").minorVersion("0")

# Define transitions between states of water
s.transition("freeze", "LIQUID", "SOLID")      # Liquid to Solid
s.transition("melts", "SOLID", "LIQUID")       # Solid to Liquid

# Example usage to log an informational message
s.infoMsg("State machine initialized successfully.")
s.state("SOLID")  # Set current state to SOLID
s.infoMsg("Current state set to SOLID.")

# Trigger a state transition and log the information
s.melts()  # Transition from SOLID to LIQUID
s.infoMsg("Transition from SOLID to LIQUID completed.")
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
