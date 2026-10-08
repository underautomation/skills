# RAPID variables & symbols

Read and write RAPID variables, persistents and constants, search symbols in the loaded program, and validate a value before writing it.

Web page: https://underautomation.com/abb/documentation/rws-rapid-symbols

A RAPID symbol is anything the program declares: a variable, a persistent, a constant, a routine, a type, a module, a task. `robot.Rws.Rapid` reads and writes them by their path, with the same two methods for every RAPID type.

Reading a value needs nothing more than a connection. Writing one needs the `Rapid` [mastership](rws-mastership.md).

## The path of a symbol

> **Available on** RWS 1.0 (IRC5) : yes | RWS 2.0 (OmniCore) : yes. The paths, the methods and the text of the values are the same on an IRC5 and on an OmniCore.

Every symbol has a path. It starts with `RAPID`, then the task, then the module, then the name. This path is what `GetSymbolValue` and `SetSymbolValue` take.

```python
from underautomation.abb.abb_controller import AbbController

robot = AbbController()
robot.connect("192.168.0.1")

# A variable declared in the module MainModule of the task T_ROB1
robot.rws.rapid.get_symbol_value("RAPID/T_ROB1/MainModule/myCounter")

# reg1 and the other predefined registers live in the built-in module "user"
robot.rws.rapid.get_symbol_value("RAPID/T_ROB1/user/reg1")

# A leading slash is accepted, it is removed by the SDK
robot.rws.rapid.get_symbol_value("/RAPID/T_ROB1/user/reg1")

# A module of the task, and the task itself, are symbols too
robot.rws.rapid.get_symbol_properties("RAPID/T_ROB1/MainModule")
robot.rws.rapid.get_symbol_properties("RAPID/T_ROB1")

# A RAPID type has a path of its own, without any task
robot.rws.rapid.get_symbol_properties("RAPID/robtarget")

robot.disconnect()
```

| Path                                | What it names                                              |
| ----------------------------------- | ---------------------------------------------------------- |
| `RAPID/T_ROB1/MainModule/myCounter` | A variable, a persistent or a constant of a module         |
| `RAPID/T_ROB1/user/reg1`            | `reg1` to `reg5`, which live in the built-in module `user` |
| `RAPID/T_ROB1/MainModule`           | The module itself                                          |
| `RAPID/T_ROB1`                      | The task itself                                            |
| `RAPID/robtarget`                   | A RAPID type, which belongs to no task                     |

The path is case sensitive on the name of the module and on the name of the symbol. A leading slash is accepted, the SDK removes it. When no symbol has that path, the controller answers 404 and the SDK throws an `RwsException`.

If you do not know where a variable is declared, do not guess the path, search for it with `SearchSymbols`.

## Read a value

`GetSymbolValue` returns the value as the text RAPID writes it with, plus where the declaration sits in the module. There is no typed overload, a `num`, a `bool` and a `robtarget` all come back as a string.

```python
from underautomation.abb.abb_controller import AbbController

robot = AbbController()
robot.connect("192.168.0.1")

# A value always comes back as the text RAPID writes it with. Reading needs no mastership.
value = robot.rws.rapid.get_symbol_value("RAPID/T_ROB1/user/reg1")
print(value.value)                 # "42"
print(value.declaration_position)  # where the declaration sits in the module

# num and dnum: float() reads the dot RAPID uses as decimal separator
number = float(robot.rws.rapid.get_symbol_value("RAPID/T_ROB1/user/reg1").value)

# bool: the controller writes TRUE or FALSE
flag = robot.rws.rapid.get_symbol_value("RAPID/T_ROB1/MainModule/myFlag").value.strip().upper() == "TRUE"

# string: the value carries the RAPID quotes, remove them
text = robot.rws.rapid.get_symbol_value("RAPID/T_ROB1/MainModule/myText").value.strip('"')

print(number, flag, text)

robot.disconnect()
```

| RAPID type                     | What `Value` holds                                                  |
| ------------------------------ | ------------------------------------------------------------------- |
| `num`, `dnum`                  | `42`, `1.5`, `9E+09`. Always a dot as decimal separator.            |
| `bool`                         | `TRUE` or `FALSE`, in capitals                                      |
| `string`                       | The RAPID quotes are part of the value, `"hello"`                   |
| `robtarget`, `pos`, any record | The bracketed form, `[[515,0,712],[1,0,0,0],[0,0,0,0],[9E+09,...]]` |
| An array                       | One value too, `[1,2,3]`                                            |

Parse the numbers with `CultureInfo.InvariantCulture`. On a machine configured with a French or a German locale, `double.Parse("1.5")` without it gives 15.

## Write a value

`SetSymbolValue` takes the same text form. The controller checks the value against the type of the symbol and answers 400 when it does not match.

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.mastership_domain import MastershipDomain

robot = AbbController()
robot.connect("192.168.0.1")

# Writing needs the RAPID mastership. Take it, write, give it back.
robot.rws.mastership.request(MastershipDomain.Rapid)
try:
    # num: RAPID wants a dot as decimal separator, which is what repr of a float gives
    speed = 1.5
    robot.rws.rapid.set_symbol_value("RAPID/T_ROB1/user/reg1", str(speed))

    # bool: TRUE or FALSE, in capitals
    robot.rws.rapid.set_symbol_value("RAPID/T_ROB1/MainModule/myFlag", "TRUE")

    # string: the RAPID quotes are part of the value
    robot.rws.rapid.set_symbol_value("RAPID/T_ROB1/MainModule/myText", '"hello"')
finally:
    robot.rws.mastership.release(MastershipDomain.Rapid)

robot.disconnect()
```

What readers get wrong, in order:

- **The mastership.** Without the `Rapid` [mastership](rws-mastership.md) the controller answers 403. In manual mode it also wants the write access an operator grants from the FlexPendant.
- **The culture.** `speed.ToString()` on a French machine writes `1,5`, which the controller refuses. Always format with `CultureInfo.InvariantCulture`.
- **The quotes of a string.** The value of a RAPID `string` carries them, `"\"hello\""` and not `"hello"`.
- **A constant.** A `CONST` cannot be written while the program runs. `GetSymbolProperties` reports it, its `ReadOnly` property is `true`.
- **A local variable.** A variable declared inside a routine only exists while the routine runs.

Writing a variable does not change the declaration. After a program reset the symbol goes back to the value written in its source, see below.



**RapidSymbolValue** ([reference](../api/underautomation.abb.rws.data.md#rapidsymbolvalue))

- `RapidSymbolValue()`: Initializes a new instance of the RapidSymbolValue class
- `value: str`: Value of the symbol, written the way RAPID writes it
- `declaration_position: RapidTextRange`: Where the symbol is declared, null when the controller did not report it
- `initial_value_position: RapidTextRange`: Where the initial value of the symbol is written, null when the controller did not report it. The controller reports zeros when the declaration carries no initial value.

**RapidTextRange** ([reference](../api/underautomation.abb.rws.data.md#rapidtextrange))

- `RapidTextRange()`: Initializes a new instance of the RapidTextRange class
- `begin_row: int | None`: Line the range begins at, null when the controller did not report it
- `begin_column: int | None`: Column the range begins at, null when the controller did not report it
- `end_row: int | None`: Line the range ends at, null when the controller did not report it
- `end_column: int | None`: Column the range ends at, null when the controller did not report it

## Records, arrays and the initial value

A record is not taken apart by the SDK. You get the bracketed text, in the same order as the components of the type, and you write it back the same way.

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.mastership_domain import MastershipDomain

robot = AbbController()
robot.connect("192.168.0.1")

# A record comes back in the bracketed form RAPID writes it with. The SDK does not
# take it apart, you get the text and parse what you need.
target = robot.rws.rapid.get_symbol_value("RAPID/T_ROB1/MainModule/pHome")
print(target.value)
# [[515,0,712],[0,0,1,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]]

# An array is one value too, its elements separated by commas
print(robot.rws.rapid.get_symbol_value("RAPID/T_ROB1/MainModule/myArray").value)  # [1,2,3]

# Build the text with a dot as decimal separator, a comma is refused
x, y, z = 515.5, 0, 712
pose = f"[[{x},{y},{z}],[0,0,1,0],[0,0,0,0],[9E9,9E9,9E9,9E9,9E9,9E9]]"

robot.rws.mastership.request(MastershipDomain.Rapid)
try:
    # The value has to carry every component the type declares
    robot.rws.rapid.set_symbol_value("RAPID/T_ROB1/MainModule/pHome", pose)
finally:
    robot.rws.mastership.release(MastershipDomain.Rapid)

robot.disconnect()
```

`SetSymbolInitialValue` writes the value the declaration carries, the one the symbol goes back to when the program is reset. It rewrites the source of the module, so the module counts as changed afterwards. `SetSymbolValue` only changes what the symbol holds right now.

`InitialValuePosition` of `RapidSymbolValue` says where that initial value sits in the source. The controller reports zeros when the declaration carries none.

## Check a value before writing it

`ValidateSymbolValue` asks the controller whether it would accept a value for a given type, without writing it anywhere. It returns `false` for a refused value instead of throwing, so it is what an editor uses to tell an operator that what they typed is wrong.

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.mastership_domain import MastershipDomain

robot = AbbController()
robot.connect("192.168.0.1")

# Ask the controller whether it would take the value, without writing it anywhere
print(robot.rws.rapid.validate_symbol_value("T_ROB1", "num", "1.5"))    # True

# A value that does not fit the type gives False, it does not raise
print(robot.rws.rapid.validate_symbol_value("T_ROB1", "num", "hello"))  # False

robot.rws.mastership.request(MastershipDomain.Rapid)
try:
    if robot.rws.rapid.validate_symbol_value("T_ROB1", "num", "1.5"):
        robot.rws.rapid.set_symbol_value("RAPID/T_ROB1/user/reg1", "1.5")

    # The value written in the declaration, the one the symbol goes back to when the
    # program is reset. This rewrites the source of the module.
    robot.rws.rapid.set_symbol_initial_value("RAPID/T_ROB1/MainModule/myCounter", "0")
finally:
    robot.rws.mastership.release(MastershipDomain.Rapid)

robot.disconnect()
```

Any other failure, a type that does not exist for example, is still reported as an `RwsException`.



## Search symbols

`SearchSymbols` walks the program and returns the symbols matching a set of criteria. It is the way to list the `robtarget` of a module, to find every persistent of a task, or to check that a variable exists before writing it.

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.rapid_symbol_search_criteria import RapidSymbolSearchCriteria
from underautomation.abb.rws.data.rapid_symbol_search_view import RapidSymbolSearchView
from underautomation.abb.rws.data.rapid_symbol_type import RapidSymbolType

robot = AbbController()
robot.connect("192.168.0.1")

# Always give a starting point, a search without any criterion walks the whole system
criteria = RapidSymbolSearchCriteria()
criteria.view = RapidSymbolSearchView.Block
criteria.block_url = "RAPID/T_ROB1"
criteria.recursive = True
criteria.name_pattern = "^p[0-9]+$"        # regular expression on the name
criteria.data_type = "robtarget"

# Only the first entry is sent, search again for another kind
criteria.symbol_types = [RapidSymbolType.Persistent]

for symbol in robot.rws.rapid.search_symbols(criteria):
    print(f"{symbol.name} ({symbol.data_type})")

    # symbol_url is the path the other symbol methods take
    print(robot.rws.rapid.get_symbol_value(symbol.symbol_url).value)

# What one symbol is declared as, without reading its value
properties = robot.rws.rapid.get_symbol_properties("RAPID/T_ROB1/user/reg1")
print(properties.symbol_type)  # Variable, Persistent, Constant, ...
print(properties.data_type)    # num
print(properties.read_only)    # None when the controller did not report it

robot.disconnect()
```

Always set `BlockUrl`. A search with no criterion at all walks the whole system and takes seconds.

| `RapidSymbolSearchView` | Where the search looks                                                                           |
| ----------------------- | ------------------------------------------------------------------------------------------------ |
| `Block`                 | In the block named by `BlockUrl`, and in what it contains when `Recursive` is `true`             |
| `Scope`                 | In what is visible from a position of the source, which needs `PositionRow` and `PositionColumn` |
| `Stack`                 | In what is visible from a frame of the call stack, which needs the program pointer to be set     |
| `Undefined`             | Let the controller decide                                                                        |

`SymbolTypes` filters on the kind of symbol: `Variable`, `Persistent`, `Constant`, `Function`, `Procedure`, `Trap`, `Module`, and the others of `RapidSymbolType`. The controller keeps only one kind per search, so only the first entry of the array is sent. Search once per kind when you need several.

`NamePattern` is a regular expression, not a wildcard. `DataType` takes the name of a RAPID type, for example `robtarget`.

`GetSymbolProperties` returns the same information for one symbol: its kind, its type, whether it is local to its module, whether it is read only. A property the controller did not report comes back as `null`, so test the nullable properties before using them.



**RapidSymbolProperties** ([reference](../api/underautomation.abb.rws.data.md#rapidsymbolproperties))

- `RapidSymbolProperties()`: Initializes a new instance of the RapidSymbolProperties class
- `symbol_url: str`: Path of the symbol, which the other symbol methods take
- `name: str`: Name of the symbol, for example "reg1"
- `symbol_type: RapidSymbolType`: What kind of symbol this is
- `named: bool | None`: Whether the symbol is named, null when the controller did not report it
- `data_type: str`: Name of the type of the symbol, for example "num"
- `dimensions: int | None`: Number of array dimensions of the symbol, null when the controller did not report it
- `dimension: str`: Size of each array dimension as the controller worded it, empty when the symbol is not an array
- `heap: bool | None`: Whether the symbol is allocated on the heap, null when the controller did not report it
- `linked: bool | None`: Whether the declaration is complete, null when the controller did not report it
- `local: bool | None`: Whether the symbol is local to its module, null when the controller did not report it
- `read_only: bool | None`: Whether the symbol may not be written, null when the controller did not report it
- `task_variable: bool | None`: Whether the symbol is global within its task, null when the controller did not report it
- `storage: str`: How the controller stores the symbol, for example "loaded"
- `type_url: str`: Path of the type of the symbol, for example "RAPID/num"

**RapidSymbolSearchCriteria** ([reference](../api/underautomation.abb.rws.data.md#rapidsymbolsearchcriteria))

- `RapidSymbolSearchCriteria()`: Initializes a new instance of the RapidSymbolSearchCriteria class
- `view: RapidSymbolSearchView`: Which part of the system the search walks
- `variable_type: RapidSymbolVariableType`: Which variables the search keeps, by what may be done with them
- `block_url: str`: Path the search starts from, for example "RAPID/T_ROB1"
- `recursive: bool | None`: Whether the search also walks what the starting point contains, null to leave it to the controller
- `position_row: int | None`: Line the search starts from, used together with Scope
- `position_column: int | None`: Column the search starts from, used together with Scope
- `stack_frame: int | None`: Frame of the call stack the search starts from, used together with Stack
- `only_used: bool | None`: Whether only the symbols the program actually refers to are kept, null to leave it to the controller
- `skip_shared: bool | None`: Whether the symbols shared between tasks are skipped, null to leave it to the controller
- `name_pattern: str`: Regular expression the name of a symbol has to match to be kept
- `symbol_types: typing.List[RapidSymbolType]`: Kinds of symbol the search keeps, empty to keep every kind
- `data_type: str`: Name of the type a symbol has to have to be kept, for example "robtarget"

**RapidSymbolType** ([reference](../api/underautomation.abb.rws.data.md#rapidsymboltype))

- Unknown: The controller reported a type this library does not know
- Undefined: The type is not defined
- Atomic: A built-in type such as num or string
- Record: A record type
- Alias: An alias of another type
- RecordComponent: One component of a record
- Constant: A constant
- Variable: A variable
- Persistent: A persistent variable, whose value survives a restart
- Parameter: A parameter of a routine
- Label: A label
- ForVariable: The loop variable of a FOR statement
- Function: A function
- Procedure: A procedure
- Trap: A trap routine
- Module: A module
- Task: A task
- Any: Any of the other types, which a search uses to mean that it does not filter on the type

**RapidSymbolSearchView** ([reference](../api/underautomation.abb.rws.data.md#rapidsymbolsearchview))

- Undefined: Let the controller decide
- Block: Search the block the search path names, and optionally what it contains
- Scope: Search what is visible from a position of the source, which the search path and the position both have to be given for
- Stack: Search what is visible from a frame of the call stack, which needs the program pointer to be set

**RapidSymbolVariableType** ([reference](../api/underautomation.abb.rws.data.md#rapidsymbolvariabletype))

- Undefined: Let the controller decide
- ReadWrite: Only the variables that can be read and written
- ReadOnly: Only the variables that can be read but not written
- Loop: Only the loop variables
- Any: Any of them

## Persistent variables shared between tasks

A `PERS` declared in several tasks holds the same value in all of them, as long as the module is synchronized with the others. `GetSyncPersStatus` reports it, `SyncPersistentVariables` does the synchronization.

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.mastership_domain import MastershipDomain

robot = AbbController()
robot.connect("192.168.0.1")

# A persistent declared in several tasks holds the same value everywhere, as long as
# the module is synchronized with the other tasks declaring it
print(robot.rws.rapid.get_sync_pers_status("T_ROB1", "MainModule"))

robot.rws.mastership.request(MastershipDomain.Rapid)
try:
    robot.rws.rapid.sync_persistent_variables("T_ROB1", "MainModule")
finally:
    robot.rws.mastership.release(MastershipDomain.Rapid)

robot.disconnect()
```



## Errors you can expect

| Status | What happened                                                                                                                      |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| 400    | The value does not match the type of the symbol, or the number was formatted with a comma                                          |
| 403    | Your connection does not hold the `Rapid` [mastership](rws-mastership.md), or the user account lacks the UAS grant |
| 404    | No symbol has that path. Check the case of the module and of the name.                                                             |
| 500    | The controller cannot do it in its current state, for example writing a local variable of a routine that is not running            |

A complete example, with a `num`, a `bool`, a `string` and a `robtarget`, is given in [Read & write RAPID variables](read-write-rapid-variables.md).

The values of the RAPID symbols are the same on the two controller generations. The starting and stopping of the program that uses them is on [RAPID tasks & program execution](rws-rapid-tasks.md), and the source of the modules declaring them on [RAPID modules & program files](rws-rapid-modules.md).

## Try it in the demo application

The **RAPID (RWS)** page of the [demo application](demo-app.md) exercises these calls against a live controller, without writing any code. It is shown in [RAPID tasks & program execution](rws-rapid-tasks.md).
