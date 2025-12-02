# StateLogic

**StateLogic doesn’t just manage state. It protects it.**

**A pure, safe, and elegant finite state machine for Python — with colored terminal logging.**

[![PyPI](https://img.shields.io/pypi/v/statelogic?color=success)](https://pypi.org/project/statelogic/)
[![Tests](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Wilgat/Statelogic/main/.badges/tests.json)](https://github.com/Wilgat/Statelogic/actions)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

StateLogic is a lightweight, dependency-free finite state machine library that enforces **correctness by design**.

It was born from frustration with existing FSM libraries that allow invalid states, silent failures, or require complex boilerplate. StateLogic fixes all of that — and adds beautiful colored logging as a bonus.


## Design Philosophy — Why StateLogic Is Different (and Better)

> **"A state machine must never lie about its state."**

StateLogic is built on four unbreakable principles:

### 1. **The current state can only be changed via a valid, registered transition**
Direct assignment like `fsm.state("HACKED")` is **silently ignored** if the state is not part of a defined transition.  
This prevents bugs, race conditions, and security issues in critical systems.

### 2. **You cannot set an initial state before defining transitions**
```python
fsm = StateLogic()
fsm.state("SOLID")        # → Does nothing (no transitions defined yet)
fsm.state()               # → None
```
Only after you define at least one transition are states considered "valid":
```python
fsm.transition("melts", "SOLID", "LIQUID")
fsm.state("SOLID")        # → Now allowed
```

### 3. **Invalid transitions are impossible — not just undetected**
If you try to go from `GAS` → `SOLID` without defining that path, nothing happens.  
No exception (unless you want one), no silent success — just **correctness**.

### 4. **Hooks are first-class: before, on, and after**
```python
fsm.before("melts", lambda: input("Melt? ") == "Y")
fsm.on("melts", lambda: print("Melting started..."))
fsm.after("melts", lambda: print("Now it's water!"))
```

This isn't just convenience — it's **enforced lifecycle safety**.

These rules make StateLogic ideal for:
- Embedded systems
- Game logic
- Workflow engines
- Protocol implementations
- Any domain where state corruption is unacceptable

---

## Installation

```bash
pip install statelogic
```

## Quick Example

```python
from statelogic import StateLogic

s = StateLogic()
s.author("Wilgat").appName("WaterFSM").majorVersion(1)

# Define valid physics
s.transition("freeze",     "LIQUID", "SOLID")
s.transition("melts",      "SOLID",  "LIQUID")
s.transition("evaporate",  "LIQUID", "GAS")
s.transition("condense",   "GAS",    "LIQUID")

# Try to cheat physics
s.state("PLASMA")          # → Ignored. Still None.
print(s.state())           # → None

# Now play by the rules
s.transition("sublimate", "SOLID", "GAS")  # Define the edge case
s.state("SOLID")           # → Now allowed
s.sublimate()
print(s.state())           # → GAS

s.infoMsg("Sublimation complete!", "SCIENCE")
```

Output (with colors):
```
2025-12-02 10:30:45.123456 WaterFSM(v1.0.0)  [SCIENCE]: 
  Sublimation complete!
```

---

## Features

- Zero dependencies
- Python 2.7 and 3.6+ compatible
- Beautiful colored terminal logging (`infoMsg`, `safeMsg`, `criticalMsg`)
- Full hook system: `before`, `on`, `after`
- Dynamic attributes via `Attr` class
- Signal handling (`Ctrl+C` → graceful exit)
- Shell & environment utilities
- 100% test coverage

## Hook Examples

### `before` — Guard transitions
```python
def confirm():
    return input("Proceed? (y/n): ").lower() == "y"

s.before("launch", confirm)
s.launch()   # Only runs if user says yes
```

### `on` — React immediately
```python
s.on("error", lambda: s.criticalMsg("System failure!", "ALERT"))
```

### `after` — Cleanup or notify
```python
s.after("shutdown", lambda: s.safeMsg("System offline.", "BYE"))
```

## Project Links

- Python: https://github.com/Wilgat/Statelogic
- PyPI: https://pypi.org/project/statelogic/
- TypeScript version: https://github.com/Wilgat/StateSafe
- npm: https://www.npmjs.com/package/statesafe

## License

MIT © Wilgat

---

**StateLogic doesn’t just manage state. It protects it.**
```
