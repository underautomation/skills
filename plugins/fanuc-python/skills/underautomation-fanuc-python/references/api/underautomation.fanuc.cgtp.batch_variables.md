# underautomation.fanuc.cgtp.batch_variables

## CgtpBatchReadResult

`from underautomation.fanuc.cgtp.batch_variables.cgtp_batch_read_result import CgtpBatchReadResult`

Result of a batch read operation.

- `version: str (read only)`: Firmware version string returned by the controller

## CgtpBatchVariables

`from underautomation.fanuc.cgtp.batch_variables.cgtp_batch_variables import CgtpBatchVariables`

Collection of batch variables to read from or write to the controller in a single operation. Provides convenience methods to add typed variables.

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

## CgtpBatchWriteResult

`from underautomation.fanuc.cgtp.batch_variables.cgtp_batch_write_result import CgtpBatchWriteResult`

Result of a batch write operation.

## CgtpNumericRegister

`from underautomation.fanuc.cgtp.batch_variables.cgtp_numeric_register import CgtpNumericRegister`

Represents a numeric register (R[]) for batch read/write operations. A numeric register always has a comment and a numeric value (integer or real).

- `index: int (read only)`: 1-based index of the numeric register
- `name: str (read only)`
- `program: str (read only)`
- `string_value: str (read only)`
- `exists: bool (read only)`
- `is_uninitialized: bool (read only)`
- `is_read_only: bool (read only)`
- Inherited from [NumericRegisterWithComment](underautomation.fanuc.common.md#numericregisterwithcomment): `comment`
- Inherited from [NumericRegister](underautomation.fanuc.common.md#numericregister): `is_integer`, `integer_value`, `real_value`

## CgtpPositionRegister

`from underautomation.fanuc.cgtp.batch_variables.cgtp_position_register import CgtpPositionRegister`

Represents a position register (PR[]) for batch read/write operations.

- `index: int`: 1-based index of the position register (second dimension of POSREG[group,index])
- `group: int`: Motion group number (first dimension of POSREG[group,index])
- `u_tool: int`: User tool number. -1 means unset (stored as 255 on the controller).
- `u_frame: int`: User frame number. -1 means unset (stored as 255 on the controller).
- `axes: int`: Number of axes
- `name: str (read only)`
- `program: str (read only)`
- `string_value: str (read only)`
- `exists: bool (read only)`
- `is_uninitialized: bool (read only)`
- `is_read_only: bool (read only)`
- Inherited from [PositionRegisterWithComment](underautomation.fanuc.common.md#positionregisterwithcomment): `parse`, `comment`
- Inherited from [PositionRegister](underautomation.fanuc.common.md#positionregister): `joints_position`, `cartesian_position`

## CgtpStringRegister

`from underautomation.fanuc.cgtp.batch_variables.cgtp_string_register import CgtpStringRegister`

Represents a string register (SR[]) for batch read/write operations. A string register always has a comment and a string value.

- `index: int (read only)`: 1-based index of the string register
- `name: str (read only)`
- `program: str (read only)`
- `string_value: str (read only)`
- `exists: bool (read only)`
- `is_uninitialized: bool (read only)`
- `is_read_only: bool (read only)`
- Inherited from [StringRegisterWithComment](underautomation.fanuc.common.md#stringregisterwithcomment): `comment`, `value`

## CgtpStructureField

`from underautomation.fanuc.cgtp.batch_variables.cgtp_structure_field import CgtpStructureField`

Represents a FIELD or ARRAY node inside a structured variable response.

- `CgtpStructureField()`
- `name: str`: Field or array element name
- `string_value: str`: Text content of this node. Null if this node has children.
- `is_read_only: bool`: Whether this node is read-only on the controller
- `is_array: bool`: True if this node was an ARRAY element, false if it was a FIELD
- `children: typing.List['CgtpStructureField']`: Child nodes (FIELD and ARRAY elements). Null if this is a leaf node.

## CgtpVariable

`from underautomation.fanuc.cgtp.batch_variables.cgtp_variable import CgtpVariable`

Represents a generic controller variable for batch read/write operations. Supports scalar values (integer, real, boolean, string, position, vector, configuration) and structured values (FIELD/ARRAY hierarchies).

- `name: str (read only)`
- `program: str (read only)`
- `string_value: str`
- `exists: bool (read only)`
- `is_uninitialized: bool (read only)`
- `is_read_only: bool (read only)`
- `structure_value: CgtpStructureField`: Structured value returned for complex variables (with FIELD/ARRAY children). Null for scalar variables. When writing, if this is not null each leaf field is written independently.
- `cartesian_position_value: CartesianPositionVariable`: Gets or sets the value as a Cartesian position. Setting this property updates string_value.
- `joint_position_value: JointPositionVariable`: Gets or sets the value as a joint position. Setting this property updates string_value.
- `integer_value: int`: Gets or sets the value as an integer. Setting this property updates string_value.
- `real_value: float`: Gets or sets the value as a double. Setting this property updates string_value.
- `boolean_value: bool`: Gets or sets the value as a boolean. Setting this property updates string_value.
- `vector_value: VectorVariable`: Gets or sets the value as a 3D vector. Setting this property updates string_value.
- `configuration_value: Configuration`: Gets or sets the value as a robot configuration. Setting this property updates string_value.

## ICgtpBatchVariable

`from underautomation.fanuc.cgtp.batch_variables.i_cgtp_batch_variable import ICgtpBatchVariable`

Common interface for all batch variable types used with batch read/write operations.

- `name: str (read only)`: Full variable name (e.g. "$NUMREG[1]", "$POSREG[1,2]", "$RMT_MASTER")
- `program: str (read only)`: Program name that owns this variable
- `string_value: str (read only)`: Raw string value as read from or to be written to the controller
- `exists: bool (read only)`: Indicates whether a value was returned by the controller during a batch read. False if the variable was not found.
- `is_uninitialized: bool (read only)`: Indicates whether the variable is uninitialized on the controller
- `is_read_only: bool (read only)`: Indicates whether the variable is read-only on the controller and cannot be written with CGTP
