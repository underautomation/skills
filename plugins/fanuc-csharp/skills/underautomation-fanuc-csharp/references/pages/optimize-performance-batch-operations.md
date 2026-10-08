# Optimize with batch operations

Maximize read/write performance using SNPX batch assignments and CGTP batch variables for high-frequency data exchange.

Web page: https://underautomation.com/fanuc/documentation/optimize-performance-batch-operations

Batch operations let you group multiple register or variable reads/writes into a single network request, dramatically improving throughput.

## SNPX batch : 80x faster

SNPX batch assignments read or write groups of data in a single command with constant ~2 ms execution time, regardless of how many items are in the batch.

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

### Performance comparison

| Method | 80 position registers | Time |
|--------|----------------------|------|
| Individual reads | 80 × `PositionRegisters.Read()` | ~160 ms |
| Batch read | 1 × `BatchAssignment.Read()` | ~2 ms |

See also: [SNPX Batch reading](snpx-batch.md)

## CGTP batch : Multiple types in one request

CGTP batch variables combine registers, strings, positions, and system variables in a single HTTP request:

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Cgtp;
using UnderAutomation.Fanuc.Cgtp.BatchVariables;

public class OptimizePerformanceBatchOperationsCgtp
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        robot.Connect("192.168.0.1");

        // Create a batch
        var batch = new CgtpBatchVariables();

        // Add different types
        batch.AddNumericRegister(1);
        batch.AddNumericRegister(2);
        batch.AddStringRegister(1);
        batch.AddPositionRegister(1);
        batch.AddVariable("$RMT_MASTER");

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

See also: [CGTP Registers & variables](cgtp-registers-variables.md)

## Best practices

1. **Reuse batch assignments**: Create them once, call `Read()` repeatedly
2. **Group related data**: Combine registers, I/O, and variables that you always need together
3. **Use SNPX for speed-critical paths**: ~2 ms vs ~50 ms for CGTP
4. **Use CGTP for mixed types**: CGTP batch can combine registers, variables, and positions in one request
5. **Monitor polling cycles**: Batch reads enable sub-10ms polling cycles with SNPX

## Protocol comparison

| Feature | SNPX Batch | CGTP Batch |
|---------|-----------|------------|
| **Execution time** | ~2 ms (constant) | ~50 ms |
| **Numeric registers** | Yes | Yes |
| **Position registers** | Yes | Yes |
| **String registers** | Yes | Yes |
| **Flags** | Yes | No |
| **System variables** | Yes | Yes |
| **Digital I/O** | Yes | No |
| **Numeric I/O** | Yes | No |
| **Read + Write** | Read only | Read + Write |
| **Mixed types** | One type per batch | Multiple types |
