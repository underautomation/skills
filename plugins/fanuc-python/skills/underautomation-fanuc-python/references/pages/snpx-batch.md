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

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.snpx.enable = True
robot.connect(parameters)

# Numeric registers batch: read R[1] through R[100]
num_batch = robot.snpx.numeric_registers.create_batch_assignment(1, 100)
values = num_batch.read()

# Position registers batch: read PR[1] through PR[50]
pos_batch = robot.snpx.position_registers.create_batch_assignment(1, 50)
positions = pos_batch.read()

# String registers batch
str_batch = robot.snpx.string_registers.create_batch_assignment(1, 20)
strings = str_batch.read()

# Flag registers batch
flag_batch = robot.snpx.flags.create_batch_assignment(1, 100)
flags = flag_batch.read()

# System variables batch
int_batch = robot.snpx.integer_system_variables.create_batch_assignment(
    ["$RMT_MASTER", "$MCR.$GENOVERRIDE", "$SCR.$NUM_GROUP"])
int_values = int_batch.read()
```

## Performance comparison

| Method | 80 position registers | Time |
|--------|----------------------|------|
| Individual reads | 80 × `PositionRegisters.Read()` | ~160 ms |
| Batch read | 1 × `BatchAssignment.Read()` | ~2 ms |

Batch reading is **80x faster** for this example.

## Complete example

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

## API reference

**NumericRegistersBatchAssignment** ([reference](../api/underautomation.fanuc.snpx.assignment.md#numericregistersbatchassignment))

- `NumericRegistersBatchAssignment()`: Initializes a new instance of the NumericRegistersBatchAssignment class.
- `read() -> typing.List[float]`: Read all numeric registers assigned in this batch assignment.
- `assignments: typing.List[Assignment1]`: The assignments included in this batch.

**PositionRegistersBatchAssignment** ([reference](../api/underautomation.fanuc.snpx.assignment.md#positionregistersbatchassignment))

- `PositionRegistersBatchAssignment()`: Initializes a new instance of the PositionRegistersBatchAssignment class.
- `read() -> typing.List[Position]`: Reads all position registers assigned in this batch.
- `assignments: typing.List[Assignment1]`: The assignments included in this batch.
