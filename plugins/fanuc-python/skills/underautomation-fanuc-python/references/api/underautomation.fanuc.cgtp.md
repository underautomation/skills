# underautomation.fanuc.cgtp

## CgtpAsciiFileItem

`from underautomation.fanuc.cgtp.cgtp_ascii_file_item import CgtpAsciiFileItem`

Represents a file entry that has both a binary and an ASCII format.

- `CgtpAsciiFileItem()`
- `ascii_file: str (read only)`: ASCII format file name, or null if not available.
- Inherited from [CgtpFileItem](underautomation.fanuc.cgtp.md#cgtpfileitem): `file`, `comment`

## CgtpClient

`from underautomation.fanuc.cgtp.cgtp_client import CgtpClient`

Standalone CGTP Web Server client for direct use without FanucRobot.

- `CgtpClient()`: Creates a new instance of the CGTP Web Server client.
- `connect(ip: str, port: int=3080, requestTimeoutMs: int=3000, login: str=None, password: str=None) -> None`: Connect to the CGTP Web Server on the controller.
- Inherited from [CgtpClientBase](underautomation.fanuc.cgtp.internal.md#cgtpclientbase-robotcgtp): `disconnect`, `abort_task`, `select_program`, `delete_program`, `get_program_comment`, `set_program_comment`, `get_program_owner`, `set_program_owner`, `get_program_stack_size`, `set_program_stack_size`, `get_program_ignore_pause`, `set_program_ignore_pause`, `get_program_write_protect`, `set_program_write_protect`, `get_program_sub_type`, `set_program_sub_type`, `create_program`, `rename_program`, `list_programs`, `list_tp_programs`, `delete_source_lines`, `insert_source_line`, `replace_source_line`, `set_program_position_to_current_cartesian_position`, `set_program_position`, `run_program`, `change_active_program`, `pause_all_programs`, `read_variable_as_string`, `read_variable`, `write_variable`, `set_comment`, `write_numeric_register_as_double`, `write_numeric_register_as_integer`, `write_string_register`, `set_user_alarm_severity`, `read_numeric_registers_with_comment`, `read_string_registers_with_comment`, `read_user_alarms`, `get_io_comments`, `get_comments`, `read_numeric_register_with_comment`, `read_position_register_with_comment`, `read_batch_variables`, `write_position_register_as_cartesian`, `write_position_register_as_joint`, `write_batch_variables`, `read_io`, `write_io`, `get_io_simulation_status`, `simulate_io`, `unsimulate_io`, `read_cartesian_position`, `read_joint_position`, `invert_kinematics`, `forward_kinematics`, `list_files`, `get_file_as_string`, `kcl`, `http`, `language`, `enabled`

## CgtpCommentIoType

`from underautomation.fanuc.cgtp.cgtp_comment_io_type import CgtpCommentIoType`

Type of I/O pair whose comments can be read via CGTP.

- RobotIO: Robot I/O (RI/RO).
- DigitalIO: Digital I/O (DI/DO).
- GroupIO: Group I/O (GI/GO).
- AnalogIO: Analog I/O (AI/AO).

## CgtpCommentType

`from underautomation.fanuc.cgtp.cgtp_comment_type import CgtpCommentType`

Type of element whose comment can be read or written via CGTP.

- NumericRegister: Numeric register (R[]).
- PositionRegister: Position register (PR[]).
- UserAlarm: User alarm.
- RI: Robot input.
- RO: Robot output.
- DI: Digital input.
- DO: Digital output.
- GI: Group input.
- GO: Group output.
- AI: Analog input.
- AO: Analog output.
- StringRegister: String register (SR[]).
- Flag: Flag (F[]).

## CgtpException

`from UnderAutomation.Fanuc.Cgtp import CgtpException`

Represents an error returned by the FANUC controller via CGTP.

The SDK raises this .NET type: catch it with `except CgtpException as e` after the import above. Its members keep their .NET names. The class `CgtpException` of the module `underautomation.fanuc.cgtp.cgtp_exception` is not a Python exception and cannot be caught.

- `Status: int (read only)`: The RPC status code returned by the controller when available.
- Inherited from System.Exception: `Message`, `InnerException`

## CgtpFileItem

`from underautomation.fanuc.cgtp.cgtp_file_item import CgtpFileItem`

Represents a file entry returned by the controller's index pages.

- `CgtpFileItem()`
- `file: str (read only)`: File name on the controller.
- `comment: str (read only)`: Comment associated with the file, if any.

## CgtpIoPortType

`from underautomation.fanuc.cgtp.cgtp_io_port_type import CgtpIoPortType`

Type of I/O port on the controller.

- DI: Digital input.
- DO: Digital output.
- AI: Analog input.
- AO: Analog output.
- RI: Robot input.
- RO: Robot output.
- GI: Group input.
- GO: Group output.
- Flag: Flag.

## CgtpProgramSubType

`from underautomation.fanuc.cgtp.cgtp_program_sub_type import CgtpProgramSubType`

Sub-type of a TP program on the controller.

- None_: No specific sub-type.
- Job: Job program.
- Process: Process program.
- Macro: Macro program.
- Condition: Condition handler program.

## CgtpProgramType

`from underautomation.fanuc.cgtp.cgtp_program_type import CgtpProgramType`

Type of a TP program on the controller.

- Tp: TP program
- Karel: Karel program

## CgtpVariableType

`from underautomation.fanuc.cgtp.cgtp_variable_type import CgtpVariableType`

Data types that can be returned when reading a controller variable.

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

## CgtpVariableValue

`from underautomation.fanuc.cgtp.cgtp_variable_value import CgtpVariableValue`

Represents the value of a controller variable with its data type.

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
