# System variables

Read and write integer, real, position, and string system variables on the Fanuc controller via SNPX.

Web page: https://underautomation.com/fanuc/documentation/snpx-variables

SNPX lets you read and write system variables by name, including integer, real (float), position, and string types. You can also access Karel program variables using the `$[ProgramName]VariableName` syntax.

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common;

public class SnpxVariablesReadWrite
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        var parameters = new ConnectionParameters("192.168.0.1");
        parameters.Snpx.Enable = true;
        robot.Connect(parameters);

        // Integer variables
        int rmtMaster = robot.Snpx.IntegerSystemVariables.Read("$RMT_MASTER");
        robot.Snpx.IntegerSystemVariables.Write("$RMT_MASTER", 1);

        // Real (float) variables
        float overr = robot.Snpx.RealSystemVariables.Read("$MCR.$GENOVERRIDE");
        robot.Snpx.RealSystemVariables.Write("$MCR.$GENOVERRIDE", 50.0f);

        // Position variables
        Position cellFloor = robot.Snpx.PositionSystemVariables.Read("$CELL_FLOOR");
        robot.Snpx.PositionSystemVariables.Write("$CELL_FLOOR", cellFloor);

        // String variables
        string lastAlm = robot.Snpx.StringSystemVariables.Read("$ALM_IF.$LAST_ALM");

        // Karel program variables
        int karelVar = robot.Snpx.IntegerSystemVariables.Read("$[MyKarelProg]my_variable");
        robot.Snpx.IntegerSystemVariables.Write("$[MyKarelProg]my_variable", 42);

        // Set variable by name (auto-typed)
        robot.Snpx.SetVariable("$RMT_MASTER", 1);
    }
}
```

## Complete example

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common;

public class SnpxVariables
{
  public static void Main()
  {
    FanucRobot robot = new FanucRobot();

    ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");
    parameters.Snpx.Enable = true;

    robot.Connect(parameters);

    // --- Integer system variables ---
    int rmtMaster = robot.Snpx.IntegerSystemVariables.Read("$RMT_MASTER");
    robot.Snpx.IntegerSystemVariables.Write("$RMT_MASTER", 1);

    // --- Real (float) system variables ---
    float genOverride = robot.Snpx.RealSystemVariables.Read("$MCR.$GENOVERRIDE");
    robot.Snpx.RealSystemVariables.Write("$MCR.$GENOVERRIDE", 50.0f);

    // --- Position system variables ---
    Position cellFloor = robot.Snpx.PositionSystemVariables.Read("$CELL_FLOOR");
    robot.Snpx.PositionSystemVariables.Write("$CELL_FLOOR", cellFloor);

    // --- String system variables ---
    string lastAlm = robot.Snpx.StringSystemVariables.Read("$ALM_IF.$LAST_ALM");
    robot.Snpx.StringSystemVariables.Write("$ALM_IF.$LAST_ALM", "No alarms");

    // --- Karel program variables ---
    int karelVar = robot.Snpx.IntegerSystemVariables.Read("$[MyKarelProg]my_variable");
    robot.Snpx.IntegerSystemVariables.Write("$[MyKarelProg]my_variable", 42);

    // --- Set variable (auto-detects type) ---
    robot.Snpx.SetVariable("$RMT_MASTER", 1);
  }
}
```

## API reference

**PositionSystemVariables** ([reference](../api/UnderAutomation.Fanuc.Snpx.Internal.md#positionsystemvariables-robotsnpxpositionsystemvariables))

- `Position Read(string index)`: Reads the position at the specified system variable.
- `void Write(string variable, CartesianPosition cartesianPosition)`: Writes a Cartesian position to the specified system variable.
- `void Write(string variable, ExtendedCartesianPosition extendedCartesianPosition)`: Writes an extended Cartesian position to the specified system variable.
- `void Write(string variable, JointsPosition jointsPosition)`: Writes a joints position to the specified system variable.
- `PositionSystemVariablesBatchAssignment CreateBatchAssignment(string[] indexes)`: Creates a batch assignment for the specified indices.
- `Assignment<string> GetOrCreateAssignment(string index)`: Gets or creates an assignment for the specified index.

**StringSystemVariables** ([reference](../api/UnderAutomation.Fanuc.Snpx.Internal.md#stringsystemvariables-robotsnpxstringsystemvariables))

- `void Write(string index, string value)`: Write value at a certain index.
- `StringSystemVariablesBatchAssignment CreateBatchAssignment(string[] indexes)`: Creates a batch assignment for the specified indices.
- `string Read(string index)`: Reads the value at the specified index.
- `Assignment<string> GetOrCreateAssignment(string index)`: Gets or creates an assignment for the specified index.
