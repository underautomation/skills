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

```csharp
using UnderAutomation.UniversalRobots;
using UnderAutomation.UniversalRobots.Common;
using UnderAutomation.UniversalRobots.PrimaryInterface;

class PrimaryInterfaceVariable
{
  static void Main(string[] args)
  {
    var robot = new UR();

    // The Primary Interface is enabled by default
    robot.Connect("192.168.0.1");

    // Raised when the list of variables changes
    robot.PrimaryInterface.GlobalVariables.ListUpdated += (sender, e) =>
    {
      GlobalVariable[] variables = e.Variables;
    };

    // Raised when at least one value changes
    robot.PrimaryInterface.GlobalVariables.ValuesUpdated += (sender, e) =>
    {
      GlobalVariable[] variables = e.Variables;
    };

    // Last values received
    GlobalVariable[] all = robot.PrimaryInterface.GlobalVariables.GetAll();
    GlobalVariable myVar = robot.PrimaryInterface.GlobalVariables.GetByName("myVar");

    if (myVar != null)
    {
      // Typed value, according to myVar.Type
      switch (myVar.Type)
      {
        case GlobalVariableTypes.Bool: bool b = myVar.ToBool(); break;
        case GlobalVariableTypes.Int: int i = myVar.ToInt(); break;
        case GlobalVariableTypes.Float: float f = myVar.ToFloat(); break;
        case GlobalVariableTypes.String: string s = myVar.ToString(); break;
        case GlobalVariableTypes.Pose: Pose p = myVar.ToPose(); break;
        case GlobalVariableTypes.List: GlobalVariableValue[] l = myVar.ToList(); break;
        case GlobalVariableTypes.Matrix: Array m = myVar.ToMatrix(); break;
      }
    }
  }
}
```

The robot sends the variables when they change. If your application connects while a program runs, the list stays empty until a value changes. The decoding depends on the PolyScope version (up to 3.2, up to 5.9, later versions): the SDK selects it, and `FirmwareVersion` gives it.

## Read with the Dashboard Server

`GetVariable` asks the robot for one variable of the running program. The type is deduced from the value.

```csharp
using UnderAutomation.UniversalRobots;
using UnderAutomation.UniversalRobots.Common;

class DashboardVariable
{
  static void Main(string[] args)
  {
    var robot = new UR();

    // The Dashboard Server is enabled by default
    robot.Connect("192.168.0.1");

    // Read the variable "myVar" of the running program
    var response = robot.Dashboard.GetVariable("myVar");

    if (response.Succeed)
    {
      GlobalVariable variable = response.Value;

      Console.WriteLine($"{variable.Name} = {variable.Value} ({variable.Type})");

      // Typed conversions, according to variable.Type
      if (variable.Type == GlobalVariableTypes.Pose)
      {
        Pose pose = variable.ToPose();
      }
    }
  }
}
```

## Write a variable

No interface of the robot writes a variable while a program runs. Two ways remain:

### Before the program

Send URScript that sets the variable. The running program stops, so do it when no program runs, for example to initialize an installation variable. To make PolyScope save the new value of an installation variable, also set `_hidden_verificationVariable` to `0`:

```csharp
using UnderAutomation.UniversalRobots;

class PrimaryInterfaceSetVariable
{
  static void Main(string[] args)
  {
    var robot = new UR();

    robot.Connect("192.168.0.1");

    // Set the installation variable i_var_1 to 6.
    // The running program stops: send it when no program runs.
    // _hidden_verificationVariable = 0 makes PolyScope save the new value
    robot.PrimaryInterface.Script.Send(
      "def SetInstallationVariable():\n" +
      "  global _hidden_verificationVariable = 0\n" +
      "  global i_var_1 = 6\n" +
      "end\n");
  }
}
```

A secondary program (`sec`) does not stop the program, but it cannot write a global variable.

### While the program runs

Use the registers: the program reads them with `read_input_integer_register`, `read_input_float_register` or `read_input_boolean_register`, and your application writes them with RTDE up to 500 Hz. See [Read and write registers](registers.md).

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**GlobalVariable** ([reference](../api/UnderAutomation.UniversalRobots.Common.md#globalvariable))

- `GlobalVariable()`
- `string Name { get; }`: Variable name
- `TimeSpan Time { get; }`: Last time the variable was sampled
- Inherited from [GlobalVariableValue](../api/UnderAutomation.UniversalRobots.Common.md#globalvariablevalue): `ToList`, `ToPose`, `ToBool`, `ToInt`, `ToFloat`, `ToMatrix`, `Parse`, `Type`, `Value`

**GlobalVariableValue** ([reference](../api/UnderAutomation.UniversalRobots.Common.md#globalvariablevalue))

- `GlobalVariableValue()`
- `static GlobalVariableValue Parse(string message)`: Estimate variable value from its string representation
- `bool ToBool()`: Returns variable value if type is Bool. Il type is Float or Int, it returns True if value is not 0. Else, it returns false
- `float ToFloat()`: Returns variable value if type is Float. Il type is int, it casts it to float. If Type is bool, it returns 1 or 0. Else it returns NaN
- `int ToInt()`: Returns variable value if type is Int. Il type is Float, it tries to cast it to int. If Type is bool, it returns 1 or 0. Else it returns 0
- `GlobalVariableValue[] ToList()`: Returns an array of GlobalVariableValue if Type is List. Else, null is returned
- `Array ToMatrix()`: Return variable value GlobalVariable[,] if variable is a matrix. First dimension is row index and second dimension is column index. Use GetLength(0) to get row number and GetLength(1) to get column count
- `Pose ToPose()`: Returns a Pose if Type is Pose. Else, null is returned
- `GlobalVariableTypes Type { get; }`: Type of a variable
- `object Value { get; }`: Value of the variable

**GlobalVariableTypes** ([reference](../api/UnderAutomation.UniversalRobots.Common.md#globalvariabletypes))

- Bool: Variable value is bool
- Float: Variable value is float
- Int: Variable value is int
- List: Variable value is an array : GlobalVariableValue[]
- Matrix: Variable value is a matrix
- None: Variable value is null, the value has not been assigned yet
- Pose: Variable value is a UnderAutomation.UniversalRobots.Pose
- String: Variable value is a System.String

**GlobalVariables** ([reference](../api/UnderAutomation.UniversalRobots.PrimaryInterface.md#globalvariables-robotprimaryinterfaceglobalvariables))

- `GlobalVariablesFirmwareVersion FirmwareVersion { get; }`: Indicates which decoder is used used to read variables according to firmware version
- `GlobalVariable[] GetAll()`: Returns a list of all variables declared in the robot
- `GlobalVariable GetByName(string name)`: Get a variable by its name. Null is returned if the variable doesn't exist
- `event EventHandler<GlobalVariablesEventArgs> ListUpdated`: Event raised whan the variable list changed. For example, after a program starts
- `event EventHandler<GlobalVariablesEventArgs> ValuesUpdated`: Event raised at 10Hz when variable values are updated

## What to read next

- [Read and write registers](registers.md): exchange values with a running program.
- [Send URScript](remote-send-script.md): the forms of URScript and their effect on the program.
