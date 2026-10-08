# Registers & variables

Read and write numeric, position, and string registers, system variables, and perform batch operations via CGTP.

Web page: https://underautomation.com/fanuc/documentation/cgtp-registers-variables

CGTP lets you read and write any system variable, program variable, and register (numeric, position, string) on your Fanuc robot.

## Read a variable

`ReadVariable` returns a typed `CgtpVariableValue` with automatic parsing:

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Cgtp;

public class CgtpRegistersVariablesRead
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        robot.Connect("192.168.0.1");

        // Read as typed value
        CgtpVariableValue var1 = robot.Cgtp.ReadVariable("$RMT_MASTER");
        int intVal = var1.IntegerValue;
        CgtpVariableType type = var1.Type;

        // Read as raw string
        string raw = robot.Cgtp.ReadVariableAsString("$MCR.$GENOVERRIDE");

        // Write a variable
        robot.Cgtp.WriteVariable("$RMT_MASTER", 1);
        robot.Cgtp.WriteVariable("$MCR.$GENOVERRIDE", 50.0);

        // Program-scoped variables (Karel)
        CgtpVariableValue karelVar = robot.Cgtp.ReadVariable("my_variable", progName: "MY_KAREL");
        robot.Cgtp.WriteVariable("my_variable", 42, progName: "MY_KAREL");
    }
}
```

### Supported types

The variable type is auto-detected. You can access the appropriate typed property:

| Type | Property |
|------|----------|
| Integer | `IntegerValue` |
| Real | `RealValue` |
| Boolean | `BooleanValue` |
| String | `StringValue` |
| CartesianPosition | `CartesianPositionValue` |
| JointPosition | `JointPositionValue` |
| Vector | `VectorValue` |
| Config | `ConfigurationValue` |

## Read and Write registers

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Cgtp;
using UnderAutomation.Fanuc.Common;

public class CgtpRegistersVariablesRegs
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        robot.Connect("192.168.0.1");

        // Numeric registers
        NumericRegisterWithComment reg = robot.Cgtp.ReadNumericRegisterWithComment(1);
        Console.WriteLine($"R[1] = {reg.RealValue}, Comment: {reg.Comment}");
        NumericRegisterWithComment[] allRegs = robot.Cgtp.ReadNumericRegistersWithComment();
        robot.Cgtp.WriteNumericRegisterAsDouble(5, 123.45);
        robot.Cgtp.WriteNumericRegisterAsInteger(5, 100);

        // Position registers
        PositionRegisterWithComment posReg = robot.Cgtp.ReadPositionRegisterWithComment(1);
        robot.Cgtp.WritePositionRegisterAsCartesian(1, new CartesianPosition(100, 200, 300, 0, 90, 0));
        robot.Cgtp.WritePositionRegisterAsJoint(1, new JointsPosition { J1 = 0, J2 = 0, J3 = 0, J4 = 0, J5 = 0, J6 = 0 });

        // String registers
        StringRegisterWithComment[] allStr = robot.Cgtp.ReadStringRegistersWithComment();
        robot.Cgtp.WriteStringRegister(1, "Hello from CGTP");
    }
}
```


## Batch variables

Read or write multiple registers and variables in a single HTTP request:

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Cgtp;
using UnderAutomation.Fanuc.Cgtp.BatchVariables;

public class CgtpRegistersVariablesBatch
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        robot.Connect("192.168.0.1");

        // Create a batch
        var batch = new CgtpBatchVariables();
        batch.AddNumericRegister(1);
        batch.AddNumericRegister(2);
        batch.AddStringRegister(1);
        batch.AddPositionRegister(1);
        batch.AddVariable("$RMT_MASTER");
        batch.AddVariable("$MCR.$GENOVERRIDE");

        // Read all at once
        CgtpBatchReadResult result = robot.Cgtp.ReadBatchVariables(batch);

        // Write batch with values
        var writeBatch = new CgtpBatchVariables();
        writeBatch.AddNumericRegisterAsReal(1, "Speed", 50.0);
        writeBatch.AddNumericRegisterAsInteger(2, "Counter", 0);
        writeBatch.AddStringRegisterWithValue(1, "Status", "Running");
        robot.Cgtp.WriteBatchVariables(writeBatch);
    }
}
```

## Complete example

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common;
using UnderAutomation.Fanuc.Cgtp;
using UnderAutomation.Fanuc.Cgtp.BatchVariables;

public class CgtpRegistersVariables
{
  public static void Main()
  {
    FanucRobot robot = new FanucRobot();

    ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");
    parameters.Cgtp.Enable = true;

    robot.Connect(parameters);

    // --- Read variables ---
    CgtpVariableValue var = robot.Cgtp.ReadVariable("$RMT_MASTER");
    int intVal = var.IntegerValue;
    CgtpVariableType type = var.Type;

    // Read as raw string
    string raw = robot.Cgtp.ReadVariableAsString("$MCR.$GENOVERRIDE");

    // Write a variable
    robot.Cgtp.WriteVariable("$RMT_MASTER", 1);
    robot.Cgtp.WriteVariable("$MCR.$GENOVERRIDE", 50.0);

    // --- Program-scoped variables ---
    CgtpVariableValue karelVar = robot.Cgtp.ReadVariable("my_variable", progName: "MY_KAREL");
    robot.Cgtp.WriteVariable("my_variable", 42, progName: "MY_KAREL");

    // --- Numeric registers ---
    NumericRegisterWithComment reg = robot.Cgtp.ReadNumericRegisterWithComment(1);
    robot.Cgtp.WriteNumericRegisterAsDouble(5, 123.45);
    robot.Cgtp.WriteNumericRegisterAsInteger(5, 100);

    // --- Position registers ---
    PositionRegisterWithComment posReg = robot.Cgtp.ReadPositionRegisterWithComment(1);
    robot.Cgtp.WritePositionRegisterAsCartesian(1, new CartesianPosition(100, 200, 300, 0, 90, 0));
    robot.Cgtp.WritePositionRegisterAsJoint(1, new JointsPosition { J1 = 0, J2 = 0, J3 = 0, J4 = 0, J5 = 0, J6 = 0 });

    // --- String registers ---
    StringRegisterWithComment[] allStr = robot.Cgtp.ReadStringRegistersWithComment();
    robot.Cgtp.WriteStringRegister(1, "Hello from CGTP");

    // --- Batch read ---
    var batch = new CgtpBatchVariables();
    batch.AddNumericRegister(1);
    batch.AddNumericRegister(2);
    batch.AddStringRegister(1);
    batch.AddPositionRegister(1);
    batch.AddVariable("$RMT_MASTER");
    CgtpBatchReadResult result = robot.Cgtp.ReadBatchVariables(batch);

    // --- Batch write ---
    var writeBatch = new CgtpBatchVariables();
    writeBatch.AddNumericRegisterAsReal(1, "Speed", 50.0);
    writeBatch.AddNumericRegisterAsInteger(2, "Counter", 0);
    writeBatch.AddStringRegisterWithValue(1, "Status", "Running");
    robot.Cgtp.WriteBatchVariables(writeBatch);
  }
}
```

## API reference

**CgtpVariableValue** ([reference](../api/UnderAutomation.Fanuc.Cgtp.md#cgtpvariablevalue))

- `bool BooleanValue { get; }`: Value interpreted as a boolean (TRUE/FALSE).
- `CartesianPositionVariable CartesianPositionValue { get; }`: Value interpreted as a Cartesian position.
- `Configuration ConfigurationValue { get; }`: Value interpreted as a robot configuration.
- `int IntegerValue { get; }`: Value interpreted as an integer.
- `JointPositionVariable JointPositionValue { get; }`: Value interpreted as a joint position.
- `double RealValue { get; }`: Value interpreted as a double-precision floating-point number.
- `int StringLength { get; }`: Maximum string length if the variable type is String
- `string StringValue { get; }`: Raw string value of the variable
- `CgtpVariableType Type { get; }`: Data type of the variable
- `VectorVariable VectorValue { get; }`: Value interpreted as a 3D vector.

**CgtpVariableType** ([reference](../api/UnderAutomation.Fanuc.Cgtp.md#cgtpvariabletype))

- Boolean: Boolean value (TRUE or FALSE).
- Byte: 8-bit byte value.
- CartesianPosition: Cartesian position (X, Y, Z, W, P, R with configuration).
- Config: Robot configuration string.
- Integer: 32-bit integer value.
- JointPose9: Joint position with up to 9 axes.
- JointPosition: Joint position (J1..J9).
- Numeric: Numeric value that can be either integer or real.
- POSITION: Full position type.
- Real: Double-precision floating-point value.
- Short: 16-bit short integer value.
- String: String value. The actual type code encodes the maximum string length.
- Vector: 3D vector (X, Y, Z).
- XYZWPR: XYZWPR position type.
- XYZWPRExt: Extended XYZWPR position with additional axes.

**CgtpBatchVariables** ([reference](../api/UnderAutomation.Fanuc.Cgtp.BatchVariables.md#cgtpbatchvariables))

- `CgtpBatchVariables()`
- `void Add(ICgtpBatchVariable item)`
- `CgtpNumericRegister AddNumericRegister(int index)`: Add a numeric register for reading. The value and comment will be populated after a batch read.
- `CgtpNumericRegister AddNumericRegisterAsInteger(int index, string comment, int value)`: Add a numeric register with an integer value and comment for writing.
- `CgtpNumericRegister AddNumericRegisterAsReal(int index, string comment, double value)`: Add a numeric register with a real (double) value and comment for writing.
- `CgtpPositionRegister AddPositionRegister(int index, int group = 1)`: Add a position register for reading. The position data will be populated after a batch read.
- `CgtpPositionRegister AddPositionRegisterAsCartesian(int index, CartesianPosition position, int group = 1, string comment = null)`: Add a position register with a Cartesian position for writing.
- `CgtpPositionRegister AddPositionRegisterAsJoint(int index, JointsPosition position, int group = 1, string comment = null)`: Add a position register with a joint position for writing.
- `void AddRange(IEnumerable<ICgtpBatchVariable> items)`: Add multiple variables at once.
- `CgtpStringRegister AddStringRegister(int index)`: Add a string register for reading. The value and comment will be populated after a batch read.
- `CgtpStringRegister AddStringRegisterWithValue(int index, string comment, string value)`: Add a string register with a value and comment for writing.
- `CgtpVariable AddVariable(string name, string programName = null)`: Add a generic variable for reading or writing. For system variables, leave programName null. Set the desired value on the returned object before performing a batch write.
- `void Clear()`
- `bool Contains(ICgtpBatchVariable item)`
- `void CopyTo(ICgtpBatchVariable[] array, int arrayIndex)`
- `int Count { get; }`
- `IEnumerator<ICgtpBatchVariable> GetEnumerator()`
- `int IndexOf(ICgtpBatchVariable item)`
- `void Insert(int index, ICgtpBatchVariable item)`
- `bool IsReadOnly { get; }`
- `ICgtpBatchVariable this[int index] { get; set; }`
- `bool Remove(ICgtpBatchVariable item)`
- `void RemoveAt(int index)`

**NumericRegisterWithComment** ([reference](../api/UnderAutomation.Fanuc.Common.md#numericregisterwithcomment))

- `NumericRegisterWithComment()`: Default constructor.
- `NumericRegisterWithComment(double value, string comment)`: Creates a numeric register with a real value and comment.
- `NumericRegisterWithComment(int value, string comment)`: Creates a numeric register with an integer value and comment.
- `NumericRegisterWithComment(string comment)`: Creates a numeric register with a comment.
- `string Comment { get; set; }`: Comment associated with this register.
- Inherited from [NumericRegister](../api/UnderAutomation.Fanuc.Common.md#numericregister): `IsInteger`, `IntegerValue`, `RealValue`

**PositionRegisterWithComment** ([reference](../api/UnderAutomation.Fanuc.Common.md#positionregisterwithcomment))

- `PositionRegisterWithComment()`: Default constructor.
- `string Comment { get; set; }`: Comment associated with this position register.
- `static PositionRegisterWithComment Parse(string value)`: Parses a position register with comment from its string representation.
- Inherited from [PositionRegister](../api/UnderAutomation.Fanuc.Common.md#positionregister): `JointsPosition`, `CartesianPosition`
