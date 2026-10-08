# System variables

Read and write integer, real, position, and string system variables on the Fanuc controller via SNPX.

Web page: https://underautomation.com/fanuc/documentation/snpx-variables

SNPX lets you read and write system variables by name, including integer, real (float), position, and string types. You can also access Karel program variables using the `$[ProgramName]VariableName` syntax.

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.snpx.enable = True
robot.connect(parameters)

# Integer variables
rmt_master = robot.snpx.integer_system_variables.read("$RMT_MASTER")
robot.snpx.integer_system_variables.write("$RMT_MASTER", 1)

# Real (float) variables
overr = robot.snpx.real_system_variables.read("$MCR.$GENOVERRIDE")
robot.snpx.real_system_variables.write("$MCR.$GENOVERRIDE", 50.0)

# Position variables
cell_floor = robot.snpx.position_system_variables.read("$CELL_FLOOR")
robot.snpx.position_system_variables.write("$CELL_FLOOR", cell_floor)

# String variables
last_alm = robot.snpx.string_system_variables.read("$ALM_IF.$LAST_ALM")

# Karel program variables
karel_var = robot.snpx.integer_system_variables.read("$[MyKarelProg]my_variable")
robot.snpx.integer_system_variables.write("$[MyKarelProg]my_variable", 42)

# Set variable by name (auto-typed)
robot.snpx.set_variable("$RMT_MASTER", 1)
```

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

# --- Integer system variables ---
rmt_master = robot.snpx.integer_system_variables.read("$RMT_MASTER")
robot.snpx.integer_system_variables.write("$RMT_MASTER", 1)

# --- Real (float) system variables ---
gen_override = robot.snpx.real_system_variables.read("$MCR.$GENOVERRIDE")
robot.snpx.real_system_variables.write("$MCR.$GENOVERRIDE", 50.0)

# --- Position system variables ---
cell_floor = robot.snpx.position_system_variables.read("$CELL_FLOOR")
robot.snpx.position_system_variables.write("$CELL_FLOOR", cell_floor)

# --- String system variables ---
last_alm = robot.snpx.string_system_variables.read("$ALM_IF.$LAST_ALM")
robot.snpx.string_system_variables.write("$ALM_IF.$LAST_ALM", "No alarms")

# --- Karel program variables ---
karel_var = robot.snpx.integer_system_variables.read("$[MyKarelProg]my_variable")
robot.snpx.integer_system_variables.write("$[MyKarelProg]my_variable", 42)

# --- Set variable (auto-detects type) ---
robot.snpx.set_variable("$RMT_MASTER", 1)
```

## API reference

**PositionSystemVariables** ([reference](../api/underautomation.fanuc.snpx.internal.md#positionsystemvariables-robotsnpxposition_system_variables))

- `write(variable: str, cartesianPosition_or_extendedCartesianPosition_or_jointsPosition: CartesianPosition | ExtendedCartesianPosition | JointsPosition) -> None`: Writes a Cartesian position to the specified system variable. Writes an extended Cartesian position to the specified system variable. Writes a joints position to the specified system variable.
- `read(index: str) -> Position`: Reads the position at the specified system variable.
- `create_batch_assignment(indexes: typing.List[str]) -> PositionSystemVariablesBatchAssignment`: Creates a batch assignment for the specified indices.
- `get_or_create_assignment(index: str) -> Assignment1[str]`: Gets or creates an assignment for the specified index.

**StringSystemVariables** ([reference](../api/underautomation.fanuc.snpx.internal.md#stringsystemvariables-robotsnpxstring_system_variables))

- `write(index: str, value: str) -> None`: Write value at a certain index.
- `create_batch_assignment(indexes: typing.List[str]) -> StringSystemVariablesBatchAssignment`: Creates a batch assignment for the specified indices.
- `read(index: str) -> str`: Reads the value at the specified index.
- `get_or_create_assignment(index: str) -> Assignment1[str]`: Gets or creates an assignment for the specified index.
