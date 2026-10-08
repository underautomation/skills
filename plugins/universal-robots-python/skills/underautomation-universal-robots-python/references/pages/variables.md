# Read and write variables

Read the program and installation variables of a UR cobot in C# or Python with the Primary Interface or the Dashboard Server, and how to change them.

Web page: https://underautomation.com/universal-robots/documentation/variables

This article shows how to read the global variables of a Universal Robots cobot from a PC, in C# or Python, and how to change them. A global variable is a program variable or an installation variable of PolyScope. To exchange values with a running program at high speed, use [registers](registers.md) instead.

## Which way to choose

| Way                | Reads                                           | Writes                       | When                                              |
| ------------------ | ----------------------------------------------- | ---------------------------- | ------------------------------------------------- |
| Primary Interface  | Every variable, updated when its value changes  | no                           | Follow the variables of a running program         |
| Dashboard Server   | One variable, by its name, when you ask         | no                           | Read one value from time to time (PolyScope 5)    |
| URScript           |                                                 | yes, the program stops       | Set an installation variable before a program     |
| Registers (RTDE)   | 0 to 47 numbers and 0 to 127 bits               | yes, while the program runs  | Exchange values with a running program            |

In the SDK, a variable is a `GlobalVariable`: its `Name`, its `Type` and its `Value`, with typed conversions (`ToInt`, `ToFloat`, `ToBool`, `ToPose`, `ToList`, `ToMatrix`).

## Read with the Primary Interface

The Primary Interface sends the list of the variables and their new values when they change. `GlobalVariables` keeps the last values received:

- `ListUpdated` is raised when the list of the variables changes;
- `ValuesUpdated` is raised when at least one value changes;
- `GetAll()` and `GetByName()` return the last values received.

```python
from underautomation.universal_robots.ur import UR
from underautomation.universal_robots.common.global_variable_types import GlobalVariableTypes

robot = UR()

# The Primary Interface is enabled by default
robot.connect("192.168.0.1")

# Raised when the list of variables changes
def on_list_updated(sender, e):
    variables = robot.primary_interface.global_variables.get_all()

robot.primary_interface.global_variables.list_updated(on_list_updated)

# Raised when at least one value changes
def on_values_updated(sender, e):
    variables = robot.primary_interface.global_variables.get_all()

robot.primary_interface.global_variables.values_updated(on_values_updated)

# Last values received
all_variables = robot.primary_interface.global_variables.get_all()
my_var = robot.primary_interface.global_variables.get_by_name("myVar")

if my_var is not None:
    # Typed value, according to my_var.type
    if my_var.type == GlobalVariableTypes.Bool:
        value = my_var.to_bool()
    elif my_var.type == GlobalVariableTypes.Int:
        value = my_var.to_int()
    elif my_var.type == GlobalVariableTypes.Float:
        value = my_var.to_float()
    elif my_var.type == GlobalVariableTypes.String:
        value = str(my_var)
    elif my_var.type == GlobalVariableTypes.Pose:
        value = my_var.to_pose()
    elif my_var.type == GlobalVariableTypes.List:
        value = my_var.to_list()
```

The robot sends the variables when they change. If your application connects while a program runs, the list stays empty until a value changes. The decoding depends on the PolyScope version (up to 3.2, up to 5.9, later versions): the SDK selects it, and `FirmwareVersion` gives it.

## Read with the Dashboard Server

`GetVariable` asks the robot for one variable of the running program. The type is deduced from the value.

```python
from underautomation.universal_robots.ur import UR
from underautomation.universal_robots.common.global_variable_types import GlobalVariableTypes

robot = UR()

# The Dashboard Server is enabled by default
robot.connect("192.168.0.1")

# Read the variable "myVar" of the running program
response = robot.dashboard.get_variable("myVar")

if response.succeed:
    variable = response.value

    print(f"{variable.name} = {variable.value} ({variable.type})")

    # Typed conversions, according to variable.type
    if variable.type == GlobalVariableTypes.Pose:
        pose = variable.to_pose()
```

## Write a variable

No interface of the robot writes a variable while a program runs. Two ways remain:

### Before the program

Send URScript that sets the variable. The running program stops, so do it when no program runs, for example to initialize an installation variable. To make PolyScope save the new value of an installation variable, also set `_hidden_verificationVariable` to `0`:

```python
from underautomation.universal_robots.ur import UR

robot = UR()

robot.connect("192.168.0.1")

# Set the installation variable i_var_1 to 6.
# The running program stops: send it when no program runs.
# _hidden_verificationVariable = 0 makes PolyScope save the new value
robot.primary_interface.script.send(
    "def SetInstallationVariable():\n"
    "  global _hidden_verificationVariable = 0\n"
    "  global i_var_1 = 6\n"
    "end\n")
```

A secondary program (`sec`) does not stop the program, but it cannot write a global variable.

### While the program runs

Use the registers: the program reads them with `read_input_integer_register`, `read_input_float_register` or `read_input_boolean_register`, and your application writes them with RTDE up to 500 Hz. See [Read and write registers](registers.md).

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**GlobalVariable** ([reference](../api/underautomation.universal_robots.common.md#globalvariable))

- `GlobalVariable()`
- `name: str (read only)`: Variable name
- `time: typing.Any (read only)`: Last time the variable was sampled
- Inherited from [GlobalVariableValue](../api/underautomation.universal_robots.common.md#globalvariablevalue): `to_list`, `to_pose`, `to_bool`, `to_int`, `to_float`, `parse`, `type`, `value`

**GlobalVariableValue** ([reference](../api/underautomation.universal_robots.common.md#globalvariablevalue))

- `GlobalVariableValue()`
- `to_list() -> typing.List['GlobalVariableValue']`: Returns an array of GlobalVariableValue if Type is List. Else, null is returned
- `to_pose() -> Pose`: Returns a Pose if Type is Pose. Else, null is returned
- `to_bool() -> bool`: Returns variable value if type is Bool. Il type is Float or Int, it returns True if value is not 0. Else, it returns false
- `to_int() -> int`: Returns variable value if type is Int. Il type is Float, it tries to cast it to int. If Type is bool, it returns 1 or 0. Else it returns 0
- `to_float() -> float`: Returns variable value if type is Float. Il type is int, it casts it to float. If Type is bool, it returns 1 or 0. Else it returns NaN
- `static parse(message: str) -> 'GlobalVariableValue'`: Estimate variable value from its string representation
- `type: GlobalVariableTypes (read only)`: Type of a variable
- `value: typing.Any (read only)`: Value of the variable

**GlobalVariableTypes** ([reference](../api/underautomation.universal_robots.common.md#globalvariabletypes))

- None_: Variable value is null, the value has not been assigned yet
- String: Variable value is a System.String
- List: Variable value is an array : GlobalVariableValue[]
- Pose: Variable value is a UnderAutomation.UniversalRobots.Pose
- Bool: Variable value is bool
- Int: Variable value is int
- Float: Variable value is float
- Matrix: Variable value is a matrix

**GlobalVariables** ([reference](../api/underautomation.universal_robots.primary_interface.md#globalvariables-robotprimary_interfaceglobal_variables))

- `values_updated(handler)`: Event raised at 10Hz when variable values are updated
- `list_updated(handler)`: Event raised whan the variable list changed. For example, after a program starts
- `get_all() -> typing.List[GlobalVariable]`: Returns a list of all variables declared in the robot
- `get_by_name(name: str) -> GlobalVariable`: Get a variable by its name. Null is returned if the variable doesn't exist
- `firmware_version: GlobalVariablesFirmwareVersion (read only)`: Indicates which decoder is used used to read variables according to firmware version

## What to read next

- [Read and write registers](registers.md): exchange values with a running program.
- [Send URScript](remote-send-script.md): the forms of URScript and their effect on the program.
