# underautomation.fanuc.cgtp.internal

## CgtpClientBase (robot.cgtp)

`from underautomation.fanuc.cgtp.internal.cgtp_client_base import CgtpClientBase`

Base implementation for the CGTP Web Server client.

- `disconnect() -> None`: Disconnect from the CGTP Web Server. After calling this method, the client must be reconnected before it can be used again.
- `abort_task(progName: str=None) -> None`: Abort the task specified by progName. Set to null to abort all user tasks. From firmware 9.10
- `select_program(progName: str, lineNum: int=1) -> None`: Open the TP program progName and move cursor to lineNum. From firmware 9.10
- `delete_program(progName: str) -> None`: Delete the program progName from the controller. From firmware 9.10
- `get_program_comment(progName: str) -> str`: Get the comment of program progName. From firmware 9.10
- `set_program_comment(progName: str, comment: str) -> None`: Set the comment of program progName. From firmware 9.10
- `get_program_owner(progName: str) -> str`: Get the owner of program progName. From firmware 9.10
- `set_program_owner(progName: str, owner: str) -> None`: Set the owner of program progName. From firmware 9.10
- `get_program_stack_size(progName: str) -> int`: Get the stack size of program progName. From firmware 9.10
- `set_program_stack_size(progName: str, stackSize: int) -> None`: Set the stack size of program progName. From firmware 9.10
- `get_program_ignore_pause(progName: str) -> bool`: Get whether program progName ignores pause requests. From firmware 9.10
- `set_program_ignore_pause(progName: str, ignorePause: bool) -> None`: Set whether program progName ignores pause requests. From firmware 9.10
- `get_program_write_protect(progName: str) -> bool`: Get whether program progName is write-protected. From firmware 9.10
- `set_program_write_protect(progName: str, writeProtect: bool) -> None`: Set whether program progName is write-protected. From firmware 9.10
- `get_program_sub_type(progName: str) -> CgtpProgramSubType`: Get the sub-type of program progName. From firmware 9.10
- `set_program_sub_type(progName: str, subType: CgtpProgramSubType) -> None`: Set the sub-type of program progName. From firmware 9.10
- `create_program(progName: str, owner: str=None, comment: str=None, defaultGroup: int=0, subType: CgtpProgramSubType=CgtpProgramSubType.None_) -> None`: Create a new TP program on the controller. From firmware 9.10
- `rename_program(sourceName: str, newName: str) -> None`: Rename program sourceName to newName. From firmware 9.10
- `list_programs(type: CgtpProgramType, subType: CgtpProgramSubType) -> typing.List[str]`: List all TP or Karel programs on the controller
- `list_tp_programs() -> typing.List[str]`: List all TP programs on the controller, regardless of their sub-type.
- `delete_source_lines(progName: str, lineNum: int, count: int=1) -> None`: Delete count lines starting at lineNum in program progName. From firmware 9.10
- `insert_source_line(progName: str, lineContent: str, lineNum: int) -> None`: Insert a source line before lineNum in program progName. From firmware 9.10
- `replace_source_line(progName: str, lineContent: str, lineNum: int) -> None`: Replace the source line at lineNum in program progName. From firmware 9.10
- `set_program_position_to_current_cartesian_position(progName: str, positionIndex: int, groupNumber: int=1) -> CartesianPosition`: Set position at index positionIndex to the current Cartesian position in program progName and return the updated position.
- `set_program_position(progName: str, positionIndex: int, position: Position) -> None`: Set position at index positionIndex in program progName to the given position. Supports both joint and Cartesian representations. Only the first motion group is supported via CGTP. From firmware 9.10
- `run_program(progName: str, lineNum: int=1) -> None`: Run the specified program starting at lineNum. From firmware 9.30
- `change_active_program(progName: str) -> None`: Change the active TP program to progName. From firmware 9.10
- `pause_all_programs() -> None`: Pause program execution on the controller. From firmware 9.10
- `read_variable_as_string(varName: str, progName: str=None) -> str`: Read the value of variable varName in program progName. From firmware 9.10
- `read_variable(varName: str, progName: str=None) -> CgtpVariableValue`: Read the typed value of variable varName in program progName. From firmware 9.10
- `write_variable(varName: str, value: float | int | str, progName: str=None) -> None`: Write a real (double) value to variable varName in program progName. From firmware 8.30 Write an integer value to variable varName in program progName. From firmware 8.30 Write value to variable varName in program progName. From firmware 8.30
- `set_comment(type: CgtpCommentType, index: int, comment: str) -> None`: Set the comment of a register or I/O port identified by type and index.
- `write_numeric_register_as_double(index: int, value: float) -> None`: Write a real (double) value to numeric register R[index].
- `write_numeric_register_as_integer(index: int, value: int) -> None`: Write an integer value to numeric register R[index].
- `write_string_register(index: int, value: str) -> None`: Write a string value to string register SR[index].
- `set_user_alarm_severity(index: int, severity: int) -> None`: Set the severity of a user alarm.
- `read_numeric_registers_with_comment() -> typing.List[NumericRegisterWithComment]`: Read all numeric registers (R[]) with their comments and values.
- `read_string_registers_with_comment() -> typing.List[StringRegisterWithComment]`: Read all string registers (SR[]) with their comments and values.
- `read_user_alarms() -> typing.List[UserAlarmDefinition]`: Read all user alarm definitions with their comments and severity.
- `get_io_comments(type: CgtpCommentIoType) -> IOComments`: Read all I/O comments for the specified I/O type.
- `get_comments(type: CgtpCommentType) -> typing.List[str]`: Read all comments for the specified element type. For I/O types (RI, RO, DI, DO, GI, GO, AI, AO), returns the input or output comments accordingly.
- `read_numeric_register_with_comment(index: int) -> NumericRegisterWithComment`: Read the numeric register (R[]) at index. From firmware 9.10
- `read_position_register_with_comment(index: int, groupNum: int=1) -> PositionRegisterWithComment`: Read the position register (PR[]) at index for motion group groupNum. From firmware 9.10
- `read_batch_variables(variables: CgtpBatchVariables) -> CgtpBatchReadResult`: Read multiple variables from the controller in a single batch operation. Each variable in variables will be updated with the value read from the controller.
- `write_position_register_as_cartesian(index: int, value: CartesianPosition, groupNum: int=1) -> None`: Write a cartesian position value to a position register (PR[])
- `write_position_register_as_joint(index: int, value: JointsPosition, groupNum: int=1) -> None`: Write a joint position value to a position register (PR[])
- `write_batch_variables(variables: CgtpBatchVariables) -> CgtpBatchWriteResult`: Write multiple variables to the controller in a single batch operation.
- `read_io(portType: CgtpIoPortType, index: int) -> int`: Read the value of I/O port at index of type portType. From firmware 8.30
- `write_io(portType: CgtpIoPortType, index: int, value: int) -> None`: Set the value of I/O port at index of type portType. From firmware 8.30
- `get_io_simulation_status(portType: CgtpIoPortType, index: int) -> bool`: Check whether I/O port at index of type portType is simulated. From firmware 8.30
- `simulate_io(portType: CgtpIoPortType, index: int) -> None`: Set I/O port at index of type portType to simulated. From firmware 8.30
- `unsimulate_io(portType: CgtpIoPortType, index: int) -> None`: Remove simulation from I/O port at index of type portType. From firmware 8.30
- `read_cartesian_position(groupNum: int=1) -> CartesianPosition`: Read the current Cartesian position of motion group groupNum. From firmware 9.10
- `read_joint_position(groupNum: int=1) -> JointsPosition`: Read the current joint angles of motion group groupNum. From firmware 9.10
- `invert_kinematics(group: int, cartesianPosition: CartesianPosition, userTool: int=-1, userFrame: int=-1) -> JointsPosition`: Compute the inverse kinematics on the controller: convert a Cartesian position to joint angles.
- `forward_kinematics(group: int, jointPosition: JointsPosition, userTool: int=-1, userFrame: int=-1) -> CartesianPosition`: Compute the forward kinematics on the controller: convert joint angles to a Cartesian position.
- `list_files(pathName: str="MD:") -> typing.List[str]`: List files at the specified path on the controller. From firmware 9.40
- `get_file_as_string(pathName: str) -> str`: Download the content of a file from the controller as a string. From firmware 9.10
- `kcl: CgtpKclClient (read only)`: KCL client for executing KCL commands over CGTP.
- `http: CgtpHttpClient (read only)`: Provides methods to download and decode files from the controller via HTTP.
- `language: Languages`: Controller language (default is English)
- `enabled: bool (read only)`: Indicates whether the client is currently connected to the CGTP Web Server.

## CgtpClientInternal (robot.cgtp)

`from underautomation.fanuc.cgtp.internal.cgtp_client_internal import CgtpClientInternal`

Internal CGTP Web Server client used by the library infrastructure.

- Inherited from [CgtpClientBase](underautomation.fanuc.cgtp.internal.md#cgtpclientbase-robotcgtp): `disconnect`, `abort_task`, `select_program`, `delete_program`, `get_program_comment`, `set_program_comment`, `get_program_owner`, `set_program_owner`, `get_program_stack_size`, `set_program_stack_size`, `get_program_ignore_pause`, `set_program_ignore_pause`, `get_program_write_protect`, `set_program_write_protect`, `get_program_sub_type`, `set_program_sub_type`, `create_program`, `rename_program`, `list_programs`, `list_tp_programs`, `delete_source_lines`, `insert_source_line`, `replace_source_line`, `set_program_position_to_current_cartesian_position`, `set_program_position`, `run_program`, `change_active_program`, `pause_all_programs`, `read_variable_as_string`, `read_variable`, `write_variable`, `set_comment`, `write_numeric_register_as_double`, `write_numeric_register_as_integer`, `write_string_register`, `set_user_alarm_severity`, `read_numeric_registers_with_comment`, `read_string_registers_with_comment`, `read_user_alarms`, `get_io_comments`, `get_comments`, `read_numeric_register_with_comment`, `read_position_register_with_comment`, `read_batch_variables`, `write_position_register_as_cartesian`, `write_position_register_as_joint`, `write_batch_variables`, `read_io`, `write_io`, `get_io_simulation_status`, `simulate_io`, `unsimulate_io`, `read_cartesian_position`, `read_joint_position`, `invert_kinematics`, `forward_kinematics`, `list_files`, `get_file_as_string`, `kcl`, `http`, `language`, `enabled`

## CgtpConnectParametersBase

`from underautomation.fanuc.cgtp.internal.cgtp_connect_parameters_base import CgtpConnectParametersBase`

Base class for CGTP Web Server connection parameters.

- `CgtpConnectParametersBase()`
- `port: int`: HTTP port number of the CGTP Web Server.
- `request_timeout_ms: int`: HTTP request timeout in milliseconds.
- `login: str`: Login for HTTP Basic authentication (optional).
- `password: str`: Password for HTTP Basic authentication (optional).
- `static DEFAULT_PORT: int`: Default HTTP port for CGTP Web Server.
- `static DEFAULT_REQUEST_TIMEOUT_MS: int`: Default request timeout in milliseconds.

## CgtpHttpClient (robot.cgtp.http)

`from underautomation.fanuc.cgtp.internal.cgtp_http_client import CgtpHttpClient`

Provides methods to download and list files from the controller via HTTP.

- `download_as_bytes(fileName: str) -> typing.List[int]`: Download a file from the controller and return its raw bytes.
- `download_as_string(fileName: str) -> str`: Download a file from the controller and return its content as a string.
- `list_variable_files() -> typing.List[CgtpAsciiFileItem]`: List variable files available on the controller.
- `list_tp_programs() -> typing.List[CgtpAsciiFileItem]`: List TP program files available on the controller.
- `list_diagnostic_files() -> typing.List[CgtpFileItem]`: List diagnostic and error files available on the controller.
- `list_other_files() -> typing.List[CgtpFileItem]`: List other files available on the controller.
- `enumerate_variable_file_names() -> typing.List[str]`
- `ip: str (read only)`
- `base_path: str`: Base path used to build the download URL. Default is "MD".
- Inherited from [FileClientBase](underautomation.fanuc.common.files.md#fileclientbase-robotftp): `get_summary_diagnostic`, `get_all_errors_list`, `get_current_position`, `get_io_state`, `get_safety_status`, `get_program_states`, `get_variables_from_file`, `get_all_variables`, `known_variable_files`

## CgtpKclClient (robot.cgtp.kcl)

`from underautomation.fanuc.cgtp.internal.cgtp_kcl_client import CgtpKclClient`

KCL client implementation using the CGTP Web Server. Provides KCL commands over HTTP endpoints.

- `send_custom_command_unsafe(command: str) -> CustomCommandResult`: Sends a custom KCL command in Unsafe mode. Success or failure cannot be determined from the result.
- `enabled: bool (read only)`: Indicates whether the KCL client is currently connected.
- Inherited from [KclClientBase](underautomation.fanuc.common.kcl.md#kclclientbase-robottelnet): `abort`, `abort_all`, `clear_all`, `clear_program`, `clear_vars`, `continue_`, `hold`, `pause`, `reset`, `run`, `set_port`, `set_variable`, `get_current_pose`, `get_variable`, `simulate`, `unsimulate_all`, `unsimulate`, `send_custom_command`, `get_task_information`, `add_breakpoint`, `remove_breakpoint`, `remove_all_breakpoints`, `get_breakpoints`, `step_on`, `step_off`
