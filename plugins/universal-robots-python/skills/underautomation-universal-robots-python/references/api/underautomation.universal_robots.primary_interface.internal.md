# underautomation.universal_robots.primary_interface.internal

## PrimaryInterfaceClientBase (robot.primary_interface)

`from underautomation.universal_robots.primary_interface.internal.primary_interface_client_base import PrimaryInterfaceClientBase`

Base class for the Primary/Secondary Interface client. Manages the TCP connection, decodes incoming binary data packets, and raises events for each decoded sub-package.

- `robot_mode_data_received(handler)`: Robot mode data (Raised every 100ms)
- `joint_data_received(handler)`: Joint data (Raised every 100ms)
- `tool_data_received(handler)`: Tool data (Raised every 100ms)
- `masterboard_data_received(handler)`: Masterboard data (Raised every 100ms)
- `cartesian_info_received(handler)`: Cartesian inforlation (Raised every 100ms)
- `kinematics_info_received(handler)`: Kinematics information data (Raised when connection opened)
- `configuration_data_received(handler)`: Configuration data (Raised when connection opened)
- `force_mode_data_received(handler)`: Force mode data (Raised every 100ms)
- `additional_info_received(handler)`: Additional (Raised every 100ms)
- `calibration_data_received(handler)`: Calibration data (Raised every 100ms)
- `safety_data_received(handler)`: Safety data (Raised every 100ms)
- `tool_communication_info_received(handler)`: Tool communication information (Raised every 100ms)
- `tool_mode_info_received(handler)`: Tool mode information (Raised every 100ms)
- `singularity_info_received(handler)`: Singularity information (Raised every 100ms)
- `package_received(handler)`: Generic event raised each time a package is received
- `raw_package_received(handler)`: Generic event raised for each raw package received
- `program_threads_received(handler)`: Program threads changed
- `version_received(handler)`: Robot information and FW version
- `key_message_received(handler)`: Internal robot events (such as starting or stopping a program)
- `popup_message_received(handler)`: Popup message that appears with the Assignment instruction or the URScript popup() function
- `text_message_received(handler)`: Log message sent with URScript instruction textmsg()
- `runtime_exception_message_received(handler)`: Reports an error in the execution of the program
- `disconnect() -> None`: Stops data streaming and the possibility to send scripts to the robot.
- `robot_mode_data: RobotModeDataPackageEventArgs (read only)`: Last Robot mode data received
- `joint_data: JointDataPackageEventArgs (read only)`: Last joint data received
- `tool_data: ToolDataPackageEventArgs (read only)`: Last tool data received
- `masterboard_data: MasterboardDataPackageEventArgs (read only)`: Last masterboard data received
- `cartesian_info: CartesianInfoPackageEventArgs (read only)`: Last cartesian information received
- `kinematics_info: KinematicsInfoPackageEventArgs (read only)`: Last kinematics information received
- `configuration_data: ConfigurationDataPackageEventArgs (read only)`: Last configuration data received
- `force_mode_data: ForceModeDataPackageEventArgs (read only)`: Last force mode data received
- `additional_info: AdditionalInfoPackageEventArgs (read only)`: Last additional information received
- `calibration_data: CalibrationDataPackageEventArgs (read only)`: Last calibration data received
- `safety_data: SafetyDataPackageEventArgs (read only)`: Last safety data received
- `tool_communication_info: ToolCommunicationInfoPackageEventArgs (read only)`: Last tool communication information received
- `tool_mode_info: ToolModeInfoPackageEventArgs (read only)`: Last tool mode information received
- `singularity_info: SingularityInfoPackageEventArgs (read only)`: Last singularity information information received
- `program_threads: ProgramThreadsEventArgs (read only)`: Last program thread information received
- `version: VersionEventArgs (read only)`: Version of the robot and FW
- `key_message: KeyMessageEventArgs (read only)`: Internal robot events (such as starting or stopping a program)
- `popup_message: PopupMessageEventArgs (read only)`: Popup message that appears with the Assignment instruction or the URScript popup() function
- `text_message: TextMessageEventArgs (read only)`: Log message sent with URScript instruction textmsg()
- `runtime_exception_message: RuntimeExceptionMessageEventArgs (read only)`: Reports an error in the execution of the program
- `global_variables: GlobalVariables (read only)`: List of all variables in current robot program
- `script: PrimaryInterfaceScript (read only)`: Contains methods to send custom URScript to the robot
- `commands: PrimaryInterfaceCommands (read only)`: Contains methods to send commands to the robot
- `ip: str (read only)`: IP address of the connected robot
- `port: Interfaces (read only)`: Interface used for the connected robot
- `connected: bool (read only)`: Return True if the connection to the robot is active
- `local_end_point: typing.Any (read only)`: Indicates the current local endpoint (i.e. IP Address) used to communicate with the robot. You can use this IP in your UR script in the function rpc_factory()
- Inherited from [URServiceBase](underautomation.universal_robots.internal.md#urservicebase-robot): `internal_error_occured`

## PrimaryInterfaceCommands (robot.primary_interface.commands)

`from underautomation.universal_robots.primary_interface.internal.primary_interface_commands import PrimaryInterfaceCommands`

Handles Primary interface commands

- `test() -> None`: Sends a test HMC expression parse command to the robot (for internal debugging).
- `power_on() -> StatusCode`: Power on the robot
- `power_off() -> StatusCode`: Power off the robot
- `set_operational_mode(mode: OperationalModes) -> StatusCode`: Set robot operational mode
- `pause_program() -> StatusCode`: Pause running program
- `set_real() -> StatusCode`: Set robot to real robot (disable simulation)
- `set_simulated() -> StatusCode`: Simulate robot
- `stop_program() -> StatusCode`: Stop running program
- `resume_program() -> StatusCode`: Resume paused program
- `step_program() -> StatusCode`: Step program execution. Should be followed by ResumeProgram() to move to next instruction
- `run_program() -> StatusCode`: Run program from start
- `enable_teach_button() -> StatusCode`: Enable teach button
- `disable_teach_button() -> StatusCode`: Disable teach button
- `enable_freedrive_mode() -> StatusCode`: Enable freedrive mode
- `disable_freedrive_mode() -> StatusCode`: Disable freedrive mode
- `close_popup(id: int) -> StatusCode`: Close popup
- `reply_popup(id: int, value: str, type: RequestedTypes) -> StatusCode`: Reply popup
- `reply_popup(id: int, value: bool | float | int | str) -> StatusCode`: Reply popup
- `release_brakes() -> StatusCode`: Release brakes
- `unlock_protective_stop() -> StatusCode`: Unlock protective stop
- `increase_speed_limit() -> StatusCode`: Increase speed limit
- `set_speed_limit(value: float) -> StatusCode`: Set speed limit
- `set_speed(value: float) -> StatusCode`: Set speed
- `clear_breakpoints() -> StatusCode`: Clear all breakpoints
- `add_breakpoint(line: int, program: str) -> StatusCode`: Add a new breakpoint
- `remove_breakpoint(line: int, program: str) -> StatusCode`: Remove an existing breakpoint

## PrimaryInterfaceParametersBase

`from underautomation.universal_robots.primary_interface.internal.primary_interface_parameters_base import PrimaryInterfaceParametersBase`

Parameters to setup a Primary/secondary interface connection

- `port: Interfaces`: Interface on which to connect

## PrimaryInterfaceScript (robot.primary_interface.script)

`from underautomation.universal_robots.primary_interface.internal.primary_interface_script import PrimaryInterfaceScript`

Handles Primary interface send script feature

- `send(script: str) -> StatusCode`: Remotely execute script.Please see the Universal Robot Script documentation : https://www.universal-robots.com/download/.

## RawPackageReceivedEventArgs

`from underautomation.universal_robots.primary_interface.internal.raw_package_received_event_args import RawPackageReceivedEventArgs`

Event args for raw package received

- `RawPackageReceivedEventArgs(data: typing.List[int], receiveDate: datetime, type: int)`: Initializes a new instance with the raw packet data, receive timestamp, and package type.
- `data: typing.List[int] (read only)`: Full raw packet data (including header)
- `type: int (read only)`: Package Type
- Inherited from [PackageEventArgs](underautomation.universal_robots.common.md#packageeventargs-robotprimary_interfacerobot_mode_data): `receive_date`
