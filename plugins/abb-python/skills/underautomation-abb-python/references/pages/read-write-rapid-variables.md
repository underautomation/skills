# Read & write RAPID variables

Read and write a RAPID num, bool, string, robtarget or a custom record from C#, on IRC5 and on OmniCore.

Web page: https://underautomation.com/abb/documentation/read-write-rapid-variables

To read a RAPID variable from C#, call `robot.Rws.Rapid.GetSymbolValue(path)`. To write one, take the RAPID mastership and call `SetSymbolValue(path, value)`. Values travel as text, written the way RAPID writes them: a `num` is `"42"`, a `bool` is `"TRUE"`, a `robtarget` is one bracketed line.

> **Available on** RWS 1.0 (IRC5) : yes | RWS 2.0 (OmniCore) : yes.

## The path of a variable

A variable is named by its path in the RAPID tree: the task, the module, then the name of the symbol. `reg1` and the other predefined registers live in the built-in module `user`.

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

Variables, persistents and constants are read the same way. A persistent is the usual choice for data exchanged with a PC, because its value survives a program restart.

## Read a num, a bool or a string

Reading needs no mastership. The value comes back in `RapidSymbolValue.Value`, as text.

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

Two details cost time when they are discovered late:

- RAPID writes numbers with a dot as decimal separator. Parse with `CultureInfo.InvariantCulture`, otherwise a French or German machine reads `1.5` as `15`.
- A `string` carries its RAPID quotes. Trim them.

## Write a value

Writing needs the RAPID mastership. Take it, write, give it back in a `finally` block.

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

A value the controller refuses, a text where a number is expected for example, fails with the HTTP status code 400. A write attempted without the mastership fails with 403.

`SetSymbolValue` changes the value the program uses now. `SetSymbolInitialValue` changes the value written in the declaration, which is what the variable goes back to when the module is reloaded.

## Check a value before writing it

`ValidateSymbolValue` asks the controller whether it would accept a text for a given RAPID type, without writing anything. It answers `false` instead of throwing, so it fits well after a user input.

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

## Arrays and records

An array and a record are both one value, written between brackets. An array of three `num` is `[1,2,3]`. A `robtarget` is `[trans, rot, robconf, extax]`, where the first two fields are records themselves. There is no partial write: you read the whole value, change what you need, and write the whole value back.

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

## Parse a record into an object

The SDK gives the text as the controller wrote it and does not take it apart, because a record can be any type you declared. Splitting the top level of a bracketed value is enough to read an array, a `robtarget`, or your own record.

```python
from underautomation.abb.abb_controller import AbbController

robot = AbbController()
robot.connect("192.168.0.1")

# Splits the top level of a RAPID value : "[[1,2],3]" gives "[1,2]" and "3".
# A value that is not bracketed is returned as a single element.
def split_rapid_value(value):
    text = "" if value is None else value.strip()

    if not text.startswith("[") or not text.endswith("]"):
        return [text]

    text = text[1:-1]

    parts = []
    current = ""
    depth = 0
    in_string = False

    for c in text:
        if c == '"':
            in_string = not in_string

        if not in_string and c == "[":
            depth += 1
        if not in_string and c == "]":
            depth -= 1

        if not in_string and c == "," and depth == 0:
            parts.append(current.strip())
            current = ""
        else:
            current += c

    if len(current) > 0:
        parts.append(current.strip())

    return parts

# An array of num arrives as one bracketed text : [1,2.5,3]
array_text = robot.rws.rapid.get_symbol_value("RAPID/T_ROB1/MainModule/myArray").value
items = split_rapid_value(array_text)

numbers = [float(item) for item in items]

# Writing takes the same text back. The whole array is written at once.
robot.rws.rapid.set_symbol_value("RAPID/T_ROB1/MainModule/myArray", "[1,2.5,3]")

# A record is bracketed too, and its fields can be records themselves.
# A robtarget is [trans, rot, robconf, extax].
target_text = robot.rws.rapid.get_symbol_value("RAPID/T_ROB1/MainModule/pHome").value
fields = split_rapid_value(target_text)

trans = split_rapid_value(fields[0])  # [515,0,712]
rot = split_rapid_value(fields[1])    # [0.707107,0,0.707107,0]

x = float(trans[0])
y = float(trans[1])
z = float(trans[2])

print(f"pHome is at X={x} Y={y} Z={z}")

# Writing the record back : move it 10 mm up and rebuild the text.
# The two last fields are kept as they were read.
z += 10
new_value = f"[[{x},{y},{z}],[{rot[0]},{rot[1]},{rot[2]},{rot[3]}],{fields[2]},{fields[3]}]"

# Ask the controller whether it accepts the text before writing it
if robot.rws.rapid.validate_symbol_value("T_ROB1", "robtarget", new_value):
    robot.rws.rapid.set_symbol_value("RAPID/T_ROB1/MainModule/pHome", new_value)

robot.disconnect()
```

To read the current position of the robot as a `RobTarget` object rather than as text, use the motion system instead. See [Get the robot position](get-robot-position.md).

## Find the variables of a program

You do not always know the module a variable is declared in. `SearchSymbols` walks the loaded program and returns the symbols matching a criteria: a name pattern, a data type, a kind of symbol, one block or the whole task.

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

## Reading many values

There is no batch read, one variable is one request. A loop over 200 variables is 200 requests, which is slow on a controller that also has a program to run. When a lot of data has to be published, group it in one RAPID record or one array and read that in a single call.

## Going further

- [RAPID variables & symbols](rws-rapid-symbols.md), the complete reference of the symbol methods
- [Mastership](rws-mastership.md), when and how to take the write lock
- [Start & stop a RAPID program](start-stop-rapid-program.md)
- [RAPID modules & program files](rws-rapid-modules.md), to load a module that declares your variables

**Methods of RapidService** ([reference](../api/underautomation.abb.rws.services.md#rapidservice-robotrwsrapid))

- `get_module_symbol(task: str, module: str, row: int, column: int) -> RapidModuleSymbol`: Gets the declaration the controller finds at a position of a module (synchronous)
- `get_symbol_properties(symbolUrl: str) -> RapidSymbolProperties`: Gets what a RAPID symbol is declared as (synchronous)
- `get_symbol_value(symbolUrl: str) -> RapidSymbolValue`: Gets the value of a RAPID symbol and where it is declared (synchronous)
- `set_symbol_value(symbolUrl: str, value: str) -> None`: Sets the value a RAPID symbol currently holds (synchronous)
- `set_symbol_initial_value(symbolUrl: str, value: str) -> None`: Sets the value a RAPID symbol is declared with, which is the one it goes back to when the program is reset (synchronous)
- `search_symbols(criteria: RapidSymbolSearchCriteria) -> typing.List[RapidSymbolProperties]`: Finds the RAPID symbols matching a set of criteria (synchronous)
- `validate_symbol_value(task: str, dataType: str, value: str) -> bool`: Asks the controller whether a value would be accepted for a given RAPID type, without writing it anywhere (synchronous) This is what an editor uses to tell an operator that what they typed is wrong before the write is attempted.

**RapidSymbolValue** ([reference](../api/underautomation.abb.rws.data.md#rapidsymbolvalue))

- `RapidSymbolValue()`: Initializes a new instance of the RapidSymbolValue class
- `value: str`: Value of the symbol, written the way RAPID writes it
- `declaration_position: RapidTextRange`: Where the symbol is declared, null when the controller did not report it
- `initial_value_position: RapidTextRange`: Where the initial value of the symbol is written, null when the controller did not report it. The controller reports zeros when the declaration carries no initial value.

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
