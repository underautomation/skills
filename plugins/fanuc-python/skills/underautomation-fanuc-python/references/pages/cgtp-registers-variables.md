# Registers & variables

Read and write numeric, position, and string registers, system variables, and perform batch operations via CGTP.

Web page: https://underautomation.com/fanuc/documentation/cgtp-registers-variables

CGTP lets you read and write any system variable, program variable, and register (numeric, position, string) on your Fanuc robot.

## Read a variable

`ReadVariable` returns a typed `CgtpVariableValue` with automatic parsing:

```python
from underautomation.fanuc.fanuc_robot import FanucRobot

robot = FanucRobot()
robot.connect("192.168.0.1")

# Read as typed value
var1 = robot.cgtp.read_variable("$RMT_MASTER")
int_val = var1.integer_value
var_type = var1.type

# Read as raw string
raw = robot.cgtp.read_variable_as_string("$MCR.$GENOVERRIDE")

# Write a variable
robot.cgtp.write_variable("$RMT_MASTER", 1)
robot.cgtp.write_variable("$MCR.$GENOVERRIDE", 50.0)

# Program-scoped variables (Karel)
karel_var = robot.cgtp.read_variable("my_variable", prog_name="MY_KAREL")
robot.cgtp.write_variable("my_variable", 42, prog_name="MY_KAREL")
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

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.common.cartesian_position import CartesianPosition
from underautomation.fanuc.common.joints_position import JointsPosition

robot = FanucRobot()
robot.connect("192.168.0.1")

# Numeric registers
reg = robot.cgtp.read_numeric_register_with_comment(1)
print(f"R[1] = {reg.real_value}, Comment: {reg.comment}")
all_regs = robot.cgtp.read_numeric_registers_with_comment()
robot.cgtp.write_numeric_register_as_double(5, 123.45)
robot.cgtp.write_numeric_register_as_integer(5, 100)

# Position registers
pos_reg = robot.cgtp.read_position_register_with_comment(1)
robot.cgtp.write_position_register_as_cartesian(1, CartesianPosition(100, 200, 300, 0, 90, 0))
robot.cgtp.write_position_register_as_joint(1, JointsPosition(j1=0, j2=0, j3=0, j4=0, j5=0, j6=0))

# String registers
all_str = robot.cgtp.read_string_registers_with_comment()
robot.cgtp.write_string_register(1, "Hello from CGTP")
```


## Batch variables

Read or write multiple registers and variables in a single HTTP request:

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.cgtp.batch_variables.cgtp_batch_variables import CgtpBatchVariables

robot = FanucRobot()
robot.connect("192.168.0.1")

# Create a batch
batch = CgtpBatchVariables()
batch.add_numeric_register(1)
batch.add_numeric_register(2)
batch.add_string_register(1)
batch.add_position_register(1)
batch.add_variable("$RMT_MASTER")
batch.add_variable("$MCR.$GENOVERRIDE")

# Read all at once
result = robot.cgtp.read_batch_variables(batch)

# Write batch with values
write_batch = CgtpBatchVariables()
write_batch.add_numeric_register_as_real(1, "Speed", 50.0)
write_batch.add_numeric_register_as_integer(2, "Counter", 0)
write_batch.add_string_register_with_value(1, "Status", "Running")
robot.cgtp.write_batch_variables(write_batch)
```

## Complete example

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters
from underautomation.fanuc.common.cartesian_position import CartesianPosition
from underautomation.fanuc.common.joints_position import JointsPosition
from underautomation.fanuc.cgtp.batch_variables.cgtp_batch_variables import CgtpBatchVariables

# Create a robot instance
robot = FanucRobot()

# Configure connection parameters
parameters = ConnectionParameters("192.168.0.1")
parameters.cgtp.enable = True

# Connect to the robot
robot.connect(parameters)

# --- Read variables ---
var = robot.cgtp.read_variable("$RMT_MASTER")
int_val = var.integer_value
var_type = var.type

# Read as raw string
raw = robot.cgtp.read_variable_as_string("$MCR.$GENOVERRIDE")

# Write a variable
robot.cgtp.write_variable("$RMT_MASTER", 1)
robot.cgtp.write_variable("$MCR.$GENOVERRIDE", 50.0)

# --- Program-scoped variables ---
karel_var = robot.cgtp.read_variable("my_variable", prog_name="MY_KAREL")
robot.cgtp.write_variable("my_variable", 42, prog_name="MY_KAREL")

# --- Numeric registers ---
reg = robot.cgtp.read_numeric_register_with_comment(1)
robot.cgtp.write_numeric_register_as_double(5, 123.45)
robot.cgtp.write_numeric_register_as_integer(5, 100)

# --- Position registers ---
pos_reg = robot.cgtp.read_position_register_with_comment(1)
robot.cgtp.write_position_register_as_cartesian(1, CartesianPosition(100, 200, 300, 0, 90, 0))
robot.cgtp.write_position_register_as_joint(1, JointsPosition(j1=0, j2=0, j3=0, j4=0, j5=0, j6=0))

# --- String registers ---
all_str = robot.cgtp.read_string_registers_with_comment()
robot.cgtp.write_string_register(1, "Hello from CGTP")

# --- Batch read ---
batch = CgtpBatchVariables()
batch.add_numeric_register(1)
batch.add_numeric_register(2)
batch.add_string_register(1)
batch.add_position_register(1)
batch.add_variable("$RMT_MASTER")
result = robot.cgtp.read_batch_variables(batch)

# --- Batch write ---
write_batch = CgtpBatchVariables()
write_batch.add_numeric_register_as_real(1, "Speed", 50.0)
write_batch.add_numeric_register_as_integer(2, "Counter", 0)
write_batch.add_string_register_with_value(1, "Status", "Running")
robot.cgtp.write_batch_variables(write_batch)
```

## API reference

**CgtpVariableValue** ([reference](../api/underautomation.fanuc.cgtp.md#cgtpvariablevalue))

- `type: CgtpVariableType (read only)`: Data type of the variable
- `string_value: str (read only)`: Raw string value of the variable
- `string_length: int (read only)`: Maximum string length if the variable type is String
- `cartesian_position_value: CartesianPositionVariable (read only)`: Value interpreted as a Cartesian position.
- `joint_position_value: JointPositionVariable (read only)`: Value interpreted as a joint position.
- `integer_value: int (read only)`: Value interpreted as an integer.
- `real_value: float (read only)`: Value interpreted as a double-precision floating-point number.
- `boolean_value: bool (read only)`: Value interpreted as a boolean (TRUE/FALSE).
- `vector_value: VectorVariable (read only)`: Value interpreted as a 3D vector.
- `configuration_value: Configuration (read only)`: Value interpreted as a robot configuration.

**CgtpVariableType** ([reference](../api/underautomation.fanuc.cgtp.md#cgtpvariabletype))

- CartesianPosition: Cartesian position (X, Y, Z, W, P, R with configuration).
- JointPosition: Joint position (J1..J9).
- Integer: 32-bit integer value.
- Real: Double-precision floating-point value.
- Boolean: Boolean value (TRUE or FALSE).
- Vector: 3D vector (X, Y, Z).
- Short: 16-bit short integer value.
- Byte: 8-bit byte value.
- Config: Robot configuration string.
- Numeric: Numeric value that can be either integer or real.
- XYZWPR: XYZWPR position type.
- POSITION: Full position type.
- XYZWPRExt: Extended XYZWPR position with additional axes.
- String: String value. The actual type code encodes the maximum string length.
- JointPose9: Joint position with up to 9 axes.

**CgtpBatchVariables** ([reference](../api/underautomation.fanuc.cgtp.batch_variables.md#cgtpbatchvariables))

- `CgtpBatchVariables()`
- `add(item: ICgtpBatchVariable) -> None`
- `clear() -> None`
- `contains(item: ICgtpBatchVariable) -> bool`
- `copy_to(array: typing.List[ICgtpBatchVariable], arrayIndex: int) -> None`
- `index_of(item: ICgtpBatchVariable) -> int`
- `insert(index: int, item: ICgtpBatchVariable) -> None`
- `remove(item: ICgtpBatchVariable) -> bool`
- `remove_at(index: int) -> None`
- `add_numeric_register(index: int) -> CgtpNumericRegister`: Add a numeric register for reading. The value and comment will be populated after a batch read.
- `add_numeric_register_as_integer(index: int, comment: str, value: int) -> CgtpNumericRegister`: Add a numeric register with an integer value and comment for writing.
- `add_numeric_register_as_real(index: int, comment: str, value: float) -> CgtpNumericRegister`: Add a numeric register with a real (double) value and comment for writing.
- `add_string_register(index: int) -> CgtpStringRegister`: Add a string register for reading. The value and comment will be populated after a batch read.
- `add_string_register_with_value(index: int, comment: str, value: str) -> CgtpStringRegister`: Add a string register with a value and comment for writing.
- `add_position_register(index: int, group: int=1) -> CgtpPositionRegister`: Add a position register for reading. The position data will be populated after a batch read.
- `add_position_register_as_cartesian(index: int, position: CartesianPosition, group: int=1, comment: str=None) -> CgtpPositionRegister`: Add a position register with a Cartesian position for writing.
- `add_position_register_as_joint(index: int, position: JointsPosition, group: int=1, comment: str=None) -> CgtpPositionRegister`: Add a position register with a joint position for writing.
- `add_variable(name: str, programName: str=None) -> CgtpVariable`: Add a generic variable for reading or writing. For system variables, leave programName null. Set the desired value on the returned object before performing a batch write.
- `count: int (read only)`
- `is_read_only: bool (read only)`

**NumericRegisterWithComment** ([reference](../api/underautomation.fanuc.common.md#numericregisterwithcomment))

- `NumericRegisterWithComment(value: int, comment: str)`: Creates a numeric register with an integer value and comment.
- `comment: str`: Comment associated with this register.
- Inherited from [NumericRegister](../api/underautomation.fanuc.common.md#numericregister): `is_integer`, `integer_value`, `real_value`

**PositionRegisterWithComment** ([reference](../api/underautomation.fanuc.common.md#positionregisterwithcomment))

- `PositionRegisterWithComment()`: Default constructor.
- `static parse(value: str) -> 'PositionRegisterWithComment'`: Parses a position register with comment from its string representation.
- `comment: str`: Comment associated with this position register.
- Inherited from [PositionRegister](../api/underautomation.fanuc.common.md#positionregister): `joints_position`, `cartesian_position`
