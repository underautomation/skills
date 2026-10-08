# underautomation.universal_robots.internal

## DashboardClientInternal (robot.dashboard)

`from underautomation.universal_robots.internal.dashboard_client_internal import DashboardClientInternal`

Internal implementation of the Dashboard Server client that delegates connection to the parent UR instance.

- `enable(port: int=29999, receiveTimeoutMs: int=2000, sendTimeoutMs: int=500) -> None`: Enable Dashboard client connection
- Inherited from [DashboardClientBase](underautomation.universal_robots.dashboard.internal.md#dashboardclientbase-robotdashboard): `before_shutdown`, `disable`, `load_program`, `play`, `stop`, `pause`, `send_custom_dashboard_command`, `get_variable`, `shutdown`, `is_program_running`, `get_robot_mode`, `get_loaded_program`, `show_popup`, `close_popup`, `add_to_log`, `is_program_saved`, `get_program_state`, `get_polyscope_version`, `set_user_role`, `set_operational_mode`, `clear_operational_mode`, `get_operational_mode`, `is_in_remote_control`, `power_on`, `power_off`, `release_brake`, `unlock_protective_stop`, `close_safety_popup`, `load_installation`, `restart_safety`, `get_safety_status`, `get_serial_number`, `get_robot_model`, `ip`, `port`, `receive_timeout_ms`, `send_timeout_ms`, `initialized`
- Inherited from [URServiceBase](underautomation.universal_robots.internal.md#urservicebase-robot): `internal_error_occured`

## InterpreterModeClientInternal (robot.interpreter_mode)

`from underautomation.universal_robots.internal.interpreter_mode_client_internal import InterpreterModeClientInternal`

Internal implementation of the Interpreter Mode client that delegates connection to the parent UR instance.

- `connect(port: int=30020) -> None`: Enable Interpreter Mode client connection
- Inherited from [InterpreterModeClientBase](underautomation.universal_robots.interpreter_mode.internal.md#interpretermodeclientbase-robotinterpreter_mode): `execute_command`, `end_interpreter`, `clear_interpreter`, `abort`, `skip_buffer`, `state_last_executed`, `state_last_interpreted`, `state_last_cleared`, `state_last_unexecuted`, `disconnect`, `ip`, `port`, `connected`
- Inherited from [URServiceBase](underautomation.universal_robots.internal.md#urservicebase-robot): `internal_error_occured`

## PrimaryInterfaceClientInternal (robot.primary_interface)

`from underautomation.universal_robots.internal.primary_interface_client_internal import PrimaryInterfaceClientInternal`

Internal implementation of the Primary Interface client that delegates connection to the parent UR instance.

- `connect(port: Interfaces) -> None`: Connect to a specific interface
- `connect() -> None`: Connect to primary interface
- Inherited from [PrimaryInterfaceClientBase](underautomation.universal_robots.primary_interface.internal.md#primaryinterfaceclientbase-robotprimary_interface): `disconnect`, `robot_mode_data`, `joint_data`, `tool_data`, `masterboard_data`, `cartesian_info`, `kinematics_info`, `configuration_data`, `force_mode_data`, `additional_info`, `calibration_data`, `safety_data`, `tool_communication_info`, `tool_mode_info`, `singularity_info`, `program_threads`, `version`, `key_message`, `popup_message`, `text_message`, `runtime_exception_message`, `global_variables`, `script`, `commands`, `ip`, `port`, `connected`, `local_end_point`, `robot_mode_data_received`, `joint_data_received`, `tool_data_received`, `masterboard_data_received`, `cartesian_info_received`, `kinematics_info_received`, `configuration_data_received`, `force_mode_data_received`, `additional_info_received`, `calibration_data_received`, `safety_data_received`, `tool_communication_info_received`, `tool_mode_info_received`, `singularity_info_received`, `package_received`, `raw_package_received`, `program_threads_received`, `version_received`, `key_message_received`, `popup_message_received`, `text_message_received`, `runtime_exception_message_received`
- Inherited from [URServiceBase](underautomation.universal_robots.internal.md#urservicebase-robot): `internal_error_occured`

## RestClientInternal (robot.rest)

`from underautomation.universal_robots.internal.rest_client_internal import RestClientInternal`

Internal REST client for use within the UR class

- `enable(port: int=80, version: RestApiVersion=RestApiVersion.V1, timeoutMs: int=5000) -> None`: Enable REST client connection using the IP from the parent UR instance
- Inherited from [RestClientBase](underautomation.universal_robots.rest.internal.md#restclientbase-robotrest): `disable`, `change_robot_state`, `unlock_protective_stop`, `restart_safety`, `power_off`, `power_on`, `brake_release`, `load_program`, `change_program_state`, `play`, `pause`, `stop`, `resume`, `get_program_state`, `ip`, `port`, `version`, `timeout_ms`, `initialized`
- Inherited from [URServiceBase](underautomation.universal_robots.internal.md#urservicebase-robot): `internal_error_occured`

## RtdeClientInternal (robot.rtde)

`from underautomation.universal_robots.internal.rtde_client_internal import RtdeClientInternal`

Internal implementation of the Real-Time Data Exchange (RTDE) client that delegates connection to the parent UR instance.

- `connect(outputSetup: RtdeOutputSetup, inputSetup: RtdeInputSetup, version: RtdeVersions, frequency: float, port: int) -> None`: Connects to the RTDE interface on the robot controller.
- Inherited from [RtdeClientBase](underautomation.universal_robots.rtde.internal.md#rtdeclientbase-robotrtde): `pause`, `resume`, `write_inputs`, `disconnect`, `last_text_message`, `state`, `connected`, `ip`, `applied_frequency`, `version`, `output_setup`, `input_setup`, `output_recipe_id`, `input_recipe_id`, `input_recipe_is_valid`, `measured_frequency`, `output_data_values`, `protocol_version_received`, `text_message_received`, `output_data_received`, `setup_outputs_received`, `setup_inputs_received`, `start_received`, `pause_received`, `package_received`
- Inherited from [URServiceBase](underautomation.universal_robots.internal.md#urservicebase-robot): `internal_error_occured`

## RtdeOverrunException

`from UnderAutomation.UniversalRobots.Internal import RtdeOverrunException`

Exception thrown when RTDE data cannot be consumed fast enough, causing the input buffer to fill up. This typically occurs when the OutputDataReceived event handler takes longer to execute than the interval between RTDE messages.

The SDK raises this .NET type: catch it with `except RtdeOverrunException as e` after the import above. Its members keep their .NET names. The class `RtdeOverrunException` of the module `underautomation.universal_robots.internal.rtde_overrun_exception` is not a Python exception and cannot be caught.

- Inherited from System.Exception: `Message`, `InnerException`

## SftpClientInternal (robot.sftp)

`from underautomation.universal_robots.internal.sftp_client_internal import SftpClientInternal`

Implementation of the SSH File Transfer Protocol (SFTP) over SSH for transfering files to the robot controller

- `connect(port: int, username: str, password: str) -> None`: Connects to Sftp robot server
- Inherited from [SftpClientBase](underautomation.universal_robots.ssh.internal.md#sftpclientbase-robotsftp): `disconnect`, `change_directory`, `change_permissions`, `create_directory`, `delete_directory`, `delete_file`, `rename_file`, `symbolic_link`, `list_directory`, `enumerate_programs`, `enumerate_installations`, `get`, `exists`, `download_file`, `upload_file`, `get_status`, `append_all_lines`, `append_all_text`, `create`, `delete`, `get_last_access_time`, `get_last_access_time_utc`, `get_last_write_time`, `get_last_write_time_utc`, `open_read`, `open_write`, `read_all_bytes`, `read_all_lines`, `read_all_text`, `read_lines`, `write_all_bytes`, `write_all_lines`, `write_all_text`, `get_attributes`, `set_attributes`, `connected`, `operation_timeout`, `buffer_size`, `working_directory`, `protocol_version`
- Inherited from [URServiceBase](underautomation.universal_robots.internal.md#urservicebase-robot): `internal_error_occured`

## SocketCommunicationServerInternal (robot.socket_communication)

`from underautomation.universal_robots.internal.socket_communication_server_internal import SocketCommunicationServerInternal`

Internal implementation of the socket communication server used for bidirectional data exchange with UR scripts.

- Inherited from [SocketCommunicationServerBase](underautomation.universal_robots.socket_communication.internal.md#socketcommunicationserverbase-robotsocket_communication): `start`, `stop`, `socket_write`, `connected_clients`, `enabled`, `port`, `socket_client_connection`, `socket_get_var`, `socket_request`, `socket_client_disconnection`
- Inherited from [URServiceBase](underautomation.universal_robots.internal.md#urservicebase-robot): `internal_error_occured`

## SshClientInternal (robot.ssh)

`from underautomation.universal_robots.internal.ssh_client_internal import SshClientInternal`

Provides a client connection to SSH server

- `connect(port: int, username: str, password: str) -> None`: Connects to the SSH robot server
- Inherited from [SshClientBase](underautomation.universal_robots.ssh.internal.md#sshclientbase-robotssh): `disconnect`, `create_command`, `run_command`, `create_shell_stream`, `connected`
- Inherited from [URServiceBase](underautomation.universal_robots.internal.md#urservicebase-robot): `internal_error_occured`

## URServiceBase (robot)

`from underautomation.universal_robots.internal.ur_service_base import URServiceBase`

Base class of all UR services implemented in this SDK

- `internal_error_occured(handler)`: Event raised when an error occured

## XmlRpcServerInternal (robot.xml_rpc)

`from underautomation.universal_robots.internal.xml_rpc_server_internal import XmlRpcServerInternal`

Internal implementation of the XML-RPC server used to expose methods callable by URScript programs on the robot.

- Inherited from [XmlRpcServerBase](underautomation.universal_robots.xml_rpc.internal.md#xmlrpcserverbase-robotxml_rpc): `start`, `stop`, `enabled`, `port`, `xml_rpc_server_request`
- Inherited from [URServiceBase](underautomation.universal_robots.internal.md#urservicebase-robot): `internal_error_occured`
