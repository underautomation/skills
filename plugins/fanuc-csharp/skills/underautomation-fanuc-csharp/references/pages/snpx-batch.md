# Batch reading

Read groups of registers, variables, or signals in a single command for maximum performance using SNPX batch assignments.

Web page: https://underautomation.com/fanuc/documentation/snpx-batch

Batch assignments let you read a group of registers, variables, or signals in a single SNPX command instead of individual requests. This dramatically improves throughput for high-frequency data exchange.

## How it works

1. **Create** a batch assignment specifying the data range or variable names
2. **Read** the entire batch in a single call
3. **Repeat** the read call as often as needed : the assignment is reusable

The amount of data in a single command has no significant impact on execution time. Reading 80 position registers in batch takes the same ~2 ms as reading a single register.

## Batch reading

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common;

public class SnpxBatchRegisters
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        var parameters = new ConnectionParameters("192.168.0.1");
        parameters.Snpx.Enable = true;
        robot.Connect(parameters);

        // Numeric registers batch: read R[1] through R[100]
        var numBatch = robot.Snpx.NumericRegisters.CreateBatchAssignment(1, 100);
        float[] values = numBatch.Read();

        // Position registers batch: read PR[1] through PR[50]
        var posBatch = robot.Snpx.PositionRegisters.CreateBatchAssignment(1, 50);
        Position[] positions = posBatch.Read();

        // String registers batch
        var strBatch = robot.Snpx.StringRegisters.CreateBatchAssignment(1, 20);
        string[] strings = strBatch.Read();

        // Flag registers batch
        var flagBatch = robot.Snpx.Flags.CreateBatchAssignment(1, 100);
        bool[] flags = flagBatch.Read();

        // System variables batch
        var intBatch = robot.Snpx.IntegerSystemVariables.CreateBatchAssignment(
            new[] { "$RMT_MASTER", "$MCR.$GENOVERRIDE", "$SCR.$NUM_GROUP" });
        int[] intValues = intBatch.Read();
    }
}
```

## Performance comparison

| Method | 80 position registers | Time |
|--------|----------------------|------|
| Individual reads | 80 × `PositionRegisters.Read()` | ~160 ms |
| Batch read | 1 × `BatchAssignment.Read()` | ~2 ms |

Batch reading is **80x faster** for this example.

## Complete example

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common;
using UnderAutomation.Fanuc.Snpx.Assignment;

public class SnpxBatch
{
  public static void Main()
  {
    FanucRobot robot = new FanucRobot();

    ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");
    parameters.Snpx.Enable = true;

    robot.Connect(parameters);

    // --- Numeric registers batch ---
    var numBatch = robot.Snpx.NumericRegisters.CreateBatchAssignment(1, 100);
    float[] numValues = numBatch.Read();

    // --- Position registers batch ---
    var posBatch = robot.Snpx.PositionRegisters.CreateBatchAssignment(1, 50);
    Position[] positions = posBatch.Read();

    // --- String registers batch ---
    var strBatch = robot.Snpx.StringRegisters.CreateBatchAssignment(1, 20);
    string[] strings = strBatch.Read();

    // --- Flag registers batch ---
    var flagBatch = robot.Snpx.Flags.CreateBatchAssignment(1, 100);
    bool[] flags = flagBatch.Read();

    // --- Integer system variables batch ---
    var intBatch = robot.Snpx.IntegerSystemVariables.CreateBatchAssignment(
        new[] { "$RMT_MASTER", "$MCR.$GENOVERRIDE", "$SCR.$NUM_GROUP" });
    int[] intValues = intBatch.Read();

    // --- Digital signals batch ---
    bool[] sdiValues = robot.Snpx.SDI.Read(1, 200);

    // --- Numeric I/O batch ---
    ushort[] giValues = robot.Snpx.GI.Read(1, 50);

    // --- Re-read the same batch (reusable) ---
    float[] numValues2 = numBatch.Read();
  }
}
```

## API reference

**NumericRegistersBatchAssignment** ([reference](../api/UnderAutomation.Fanuc.Snpx.Assignment.md#numericregistersbatchassignment))

- `NumericRegistersBatchAssignment()`: Initializes a new instance of the Assignment.NumericRegistersBatchAssignment class.
- `float[] Read()`: Read all numeric registers assigned in this batch assignment.
- `Assignment<int>[] Assignments`: The assignments included in this batch.

**PositionRegistersBatchAssignment** ([reference](../api/UnderAutomation.Fanuc.Snpx.Assignment.md#positionregistersbatchassignment))

- `PositionRegistersBatchAssignment()`: Initializes a new instance of the Assignment.PositionRegistersBatchAssignment class.
- `Position[] Read()`: Reads all position registers assigned in this batch.
- `Assignment<int>[] Assignments`: The assignments included in this batch.
