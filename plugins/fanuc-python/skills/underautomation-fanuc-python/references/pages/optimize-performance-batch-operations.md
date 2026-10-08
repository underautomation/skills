# Optimize with batch operations

Maximize read/write performance using SNPX batch assignments and CGTP batch variables for high-frequency data exchange.

Web page: https://underautomation.com/fanuc/documentation/optimize-performance-batch-operations

Batch operations let you group multiple register or variable reads/writes into a single network request, dramatically improving throughput.

## SNPX batch : 80x faster

SNPX batch assignments read or write groups of data in a single command with constant ~2 ms execution time, regardless of how many items are in the batch.

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters

# Create a robot instance
robot = FanucRobot()

# Configure connection parameters
parameters = ConnectionParameters("192.168.0.1")
parameters.snpx.enable = True

# Connect to the robot
robot.connect(parameters)

# --- Numeric registers batch ---
num_batch = robot.snpx.numeric_registers.create_batch_assignment(1, 100)
num_values = num_batch.read()

# --- Position registers batch ---
pos_batch = robot.snpx.position_registers.create_batch_assignment(1, 50)
positions = pos_batch.read()

# --- String registers batch ---
str_batch = robot.snpx.string_registers.create_batch_assignment(1, 20)
strings = str_batch.read()

# --- Flag registers batch ---
flag_batch = robot.snpx.flags.create_batch_assignment(1, 100)
flags = flag_batch.read()

# --- Integer system variables batch ---
int_batch = robot.snpx.integer_system_variables.create_batch_assignment(
    ["$RMT_MASTER", "$MCR.$GENOVERRIDE", "$SCR.$NUM_GROUP"])
int_values = int_batch.read()

# --- Digital signals batch ---
sdi_values = robot.snpx.sdi.read(1, 200)

# --- Numeric I/O batch ---
gi_values = robot.snpx.gi.read(1, 50)

# --- Re-read the same batch (reusable) ---
num_values2 = num_batch.read()
```

### Performance comparison

| Method | 80 position registers | Time |
|--------|----------------------|------|
| Individual reads | 80 × `PositionRegisters.Read()` | ~160 ms |
| Batch read | 1 × `BatchAssignment.Read()` | ~2 ms |

See also: [SNPX Batch reading](snpx-batch.md)

## CGTP batch : Multiple types in one request

CGTP batch variables combine registers, strings, positions, and system variables in a single HTTP request:

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.cgtp.batch_variables.cgtp_batch_variables import CgtpBatchVariables

robot = FanucRobot()
robot.connect("192.168.0.1")

# Create a batch
batch = CgtpBatchVariables()

# Add different types
batch.add_numeric_register(1)
batch.add_numeric_register(2)
batch.add_string_register(1)
batch.add_position_register(1)
batch.add_variable("$RMT_MASTER")

# Read all at once
result = robot.cgtp.read_batch_variables(batch)

# Write batch with values
write_batch = CgtpBatchVariables()
write_batch.add_numeric_register_as_real(1, "Speed", 50.0)
write_batch.add_numeric_register_as_integer(2, "Counter", 0)
write_batch.add_string_register_with_value(1, "Status", "Running")
robot.cgtp.write_batch_variables(write_batch)
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
