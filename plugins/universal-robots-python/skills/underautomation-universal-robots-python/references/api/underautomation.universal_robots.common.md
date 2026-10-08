# underautomation.universal_robots.common

## AnalogRanges (robot.primary_interface.tool_data.analog_input_range2)

`from underautomation.universal_robots.common.analog_ranges import AnalogRanges`

Analog units of analog inputs and outputs

- Current: The analog value is in Amps (A)
- Voltage: The analog value is in Volts (V)

## CartesianCoordinates (robot.rtde.output_data_values.actual_tcp_force)

`from underautomation.universal_robots.common.cartesian_coordinates import CartesianCoordinates`

Represents a cartesian pose with 3 translations and 3 rotations

- `CartesianCoordinates(x: float, y: float, z: float, rx: float, ry: float, rz: float)`: Creates a new pose with translations and rotations information
- `x: float`: X coordinate in meters or m/s
- `y: float`: Y coordinate in meters or m/s
- `z: float`: Z coordinate in meters or m/s
- `rx: float`: RX rotation in radians or radians/s
- `ry: float`: RY rotation in radians or radians/s
- `rz: float`: RZ rotation in radians or radians/s
- `values: typing.List[float]`: Underlying array of 6 double values storing X, Y, Z, Rx, Ry, Rz in that order.

## ConnectException

`from UnderAutomation.UniversalRobots.Common import ConnectException`

Exception thrown when connection to the robot fails

The SDK raises this .NET type: catch it with `except ConnectException as e` after the import above. Its members keep their .NET names. The class `ConnectException` of the module `underautomation.universal_robots.common.connect_exception` is not a Python exception and cannot be caught.

- `Service: str (read only)`: Name of the robot service that failed to connect (e.g. Dashboard, RTDE, PrimaryInterface).
- `RobotIp: str (read only)`: IP address of the robot that the connection was attempted to.
- Inherited from System.Exception: `Message`, `InnerException`

## ControlModes (robot.primary_interface.robot_mode_data.control_mode)

`from underautomation.universal_robots.common.control_modes import ControlModes`

Robot control modes

- Position: Robot is position controlled
- Teach: The robot is hand guided by pushing teached button
- Force: Robot is force controlled. (For example : URScript force_mode() function is called)
- Torque: Robot is torque controlled

## ControllerBoxTypes (robot.primary_interface.configuration_data.controller_box_type)

`from underautomation.universal_robots.common.controller_box_types import ControllerBoxTypes`

Controller box types

- UR3: UR3 controller box
- UR5: UR5 controller box
- UR10: UR10 controller box
- UR16: UR16 controller box
- UR20: UR20 controller box
- UR30: UR30 controller box

## DashboardConnectParameters

`from underautomation.universal_robots.common.dashboard_connect_parameters import DashboardConnectParameters`

Setup Dashboard Client

- `enable: bool`: Enable Dashboard client communication. Default value is true.
- Inherited from [DashboardClientParametersBase](underautomation.universal_robots.dashboard.internal.md#dashboardclientparametersbase): `DEFAULT_PORT`, `DEFAULT_RECEIVE_TIMEOUT_MS`, `DEFAULT_SEND_TIMEOUT_MS`, `port`, `receive_timeout_ms`, `send_timeout_ms`

## DigitalOutputConfigurations (robot.primary_interface.tool_mode_info.digital_output_mode0)

`from underautomation.universal_robots.common.digital_output_configurations import DigitalOutputConfigurations`

Digital output configuration (NPN, PNP, Push/Pull)

- SinkingNPN: Sinking (NOPN)
- SourcingPNP: Sourcing (PNP)
- PushPull: Push / Pull

## GlobalVariable

`from underautomation.universal_robots.common.global_variable import GlobalVariable`

Describes a global variable

- `GlobalVariable()`
- `name: str (read only)`: Variable name
- `time: typing.Any (read only)`: Last time the variable was sampled
- Inherited from [GlobalVariableValue](underautomation.universal_robots.common.md#globalvariablevalue): `to_list`, `to_pose`, `to_bool`, `to_int`, `to_float`, `parse`, `type`, `value`

## GlobalVariableTypes

`from underautomation.universal_robots.common.global_variable_types import GlobalVariableTypes`

Possible types of a variable

- None_: Variable value is null, the value has not been assigned yet
- String: Variable value is a System.String
- List: Variable value is an array : GlobalVariableValue[]
- Pose: Variable value is a UnderAutomation.UniversalRobots.Pose
- Bool: Variable value is bool
- Int: Variable value is int
- Float: Variable value is float
- Matrix: Variable value is a matrix

## GlobalVariableValue

`from underautomation.universal_robots.common.global_variable_value import GlobalVariableValue`

Describes a typed variable value

- `GlobalVariableValue()`
- `to_list() -> typing.List['GlobalVariableValue']`: Returns an array of GlobalVariableValue if Type is List. Else, null is returned
- `to_pose() -> Pose`: Returns a Pose if Type is Pose. Else, null is returned
- `to_bool() -> bool`: Returns variable value if type is Bool. Il type is Float or Int, it returns True if value is not 0. Else, it returns false
- `to_int() -> int`: Returns variable value if type is Int. Il type is Float, it tries to cast it to int. If Type is bool, it returns 1 or 0. Else it returns 0
- `to_float() -> float`: Returns variable value if type is Float. Il type is int, it casts it to float. If Type is bool, it returns 1 or 0. Else it returns NaN
- `static parse(message: str) -> 'GlobalVariableValue'`: Estimate variable value from its string representation
- `type: GlobalVariableTypes (read only)`: Type of a variable
- `value: typing.Any (read only)`: Value of the variable

## IUrDhParameters

`from underautomation.universal_robots.common.i_ur_dh_parameters import IUrDhParameters`

Denavit–Hartenberg (DH) parameters for Universal Robots with only the relevant parameters

- `a2: float (read only)`: DH parameter a2 (Shoulder)
- `a3: float (read only)`: DH parameter a3 (Elbow)
- `d1: float (read only)`: DH parameter d1 (Base)
- `d4: float (read only)`: DH parameter d4 (Wrist1)
- `d5: float (read only)`: DH parameter d5 (Wrist2)
- `d6: float (read only)`: DH parameter d6 (Wrist3/Tool)

## InternalErrorEventArgs

`from underautomation.universal_robots.common.internal_error_event_args import InternalErrorEventArgs`

Describes an internal error

- `exception: typing.Any`: The exception thrown that causes an internal error
- `message: str`: Explicit message that explains what happened
- `status: StatusCode`: Context status associated to this internal error

## InterpreterModeConnectParameters

`from underautomation.universal_robots.common.interpreter_mode_connect_parameters import InterpreterModeConnectParameters`

Setup Interpreter Mode Client

- `enable: bool`: Enable Interpreter Mode client communication Default value is false
- Inherited from [InterpreterModeClientParametersBase](underautomation.universal_robots.interpreter_mode.internal.md#interpretermodeclientparametersbase): `DEFAULT_PORT`, `port`

## JointModes (robot.primary_interface.joint_data.base.joint_mode)

`from underautomation.universal_robots.common.joint_modes import JointModes`

Joint modes

- ShuttingDown: Joint is shutting down.
- PartDCalibration: Joint is in part D calibration mode.
- Backdrive: Joint is in backdrive mode.
- PowerOff: Joint is powered off.
- NotResponding: Joint is not responding.
- MotorInitialisation: Joint motor is initializing.
- Booting: Joint is booting.
- PartDCalibrationError: Joint part D calibration encountered an error.
- Bootloader: Joint is in bootloader mode.
- Calibration: Joint is calibrating.
- Fault: Joint is in a fault state.
- Running: Joint is running normally.
- Idle: Joint is idle.

## JointsDoubleValues (robot.rtde.output_data_values.actual_current)

`from underautomation.universal_robots.common.joints_double_values import JointsDoubleValues`

Represents a set of 6 double-precision values, one per robot joint. Typically used for angles (radians), velocities, currents, etc.

- `JointsDoubleValues()`
- `values: typing.List[float]`: Array of the 6 joint data
- `base: float`: Joint 1 out of 6
- `shoulder: float`: Joint 2 out of 6
- `elbow: float`: Joint 3 out of 6
- `wrist1: float`: Joint 4 out of 6
- `wrist2: float`: Joint 5 out of 6
- `wrist3: float`: Joint 6 out of 6

## JointsIntValues (robot.rtde.output_data_values.joint_mode)

`from underautomation.universal_robots.common.joints_int_values import JointsIntValues`

Represents a set of 6 integer values, one per robot joint. Typically used for joint modes, statuses, or other discrete joint data.

- `JointsIntValues()`
- `values: typing.List[int]`: Array of the 6 joint data
- `base: int`: Joint 1 out of 6
- `shoulder: int`: Joint 2 out of 6
- `elbow: int`: Joint 3 out of 6
- `wrist1: int`: Joint 4 out of 6
- `wrist2: int`: Joint 5 out of 6
- `wrist3: int`: Joint 6 out of 6

## JointsValues1

`from underautomation.universal_robots.common.joints_values_1 import JointsValues1`

Vector 6 of double values representing each robot joint

- `JointsValues1()`
- `base: T`: Joint 1 out of 6
- `shoulder: T`: Joint 2 out of 6
- `elbow: T`: Joint 3 out of 6
- `wrist1: T`: Joint 4 out of 6
- `wrist2: T`: Joint 5 out of 6
- `wrist3: T`: Joint 6 out of 6
- `values: typing.List[T]`: Array of the 6 joint data

## OutputModes (robot.primary_interface.tool_mode_info.output_mode)

`from underautomation.universal_robots.common.output_modes import OutputModes`

Digital output modes

- StandardOutput: Standard output
- DualPinPower: Dual Pin Power

## PackageEventArgs (robot.primary_interface.robot_mode_data)

`from underautomation.universal_robots.common.package_event_args import PackageEventArgs`

Base class of all received data packages

- `receive_date: datetime`: The date the data has been received

## Pose (robot.rtde.output_data_values.actual_tcp_pose)

`from underautomation.universal_robots.common.pose import Pose`

Represents a UR pose

- `Pose(x: float, y: float, z: float, rx: float, ry: float, rz: float)`: Creates a new pose with the specified translation and rotation.
- `from_rotation_vector_to_rpy() -> 'Pose'`: Consider this pose as a Rotation Vector And convert it to a new RPY position
- `from_rpy_to_rotation_vector() -> 'Pose'`: Consider this pose as RPY And convert it to a new Rotation Vector
- `static try_parse(value: str, pose: 'Pose') -> bool`: Parse a pose from its string representation
- `from_rotation_vector_to_quaternion(x: float, y: float, z: float, w: float) -> None`: Converts a rotation vector to quaternion
- `from_rpy_to4x4_matrix() -> typing.List[float]`: Consider this pose as a RPY (Roll-Pitch-Yaw) representation and return a 4x4 homogeneous transformation matrix.
- `from_rotation_vector_to4x4_matrix() -> typing.List[float]`: Consider this pose as a rotation vector and return a 4x4 homogeneous transformation matrix.
- `static from_quaternion_to_rotation_vector(x: float, y: float, z: float, w: float) -> 'Pose'`: Converts a quaternion to UR rotation vector
- `static from4x4_matrix_to_rotation_vector(matrixTransform: typing.List[float]) -> 'Pose'`: Convert a transformation 4x4 matrix to rotation vector
- `static from4x4_matrix_to_rpy(matrixTransform: typing.List[float]) -> 'Pose'`: Convert a transformation 4x4 matrix to RPY pose
- `rx_degrees: float`: RX rotation in degrees or °/s
- `ry_degrees: float`: RY rotation in degrees or °/s
- `rz_degrees: float`: RZ rotation in degrees or °/s
- Inherited from [CartesianCoordinates](underautomation.universal_robots.common.md#cartesiancoordinates-robotrtdeoutput_data_valuesactual_tcp_force): `values`, `x`, `y`, `z`, `rx`, `ry`, `rz`

## PrimaryInterfaceConnectParameters

`from underautomation.universal_robots.common.primary_interface_connect_parameters import PrimaryInterfaceConnectParameters`

Setup Primary Interface Client communication

- `enable: bool`: Choose to enable primary interface Default value is true
- Inherited from [PrimaryInterfaceParametersBase](underautomation.universal_robots.primary_interface.internal.md#primaryinterfaceparametersbase): `port`

## RestConnectParameters

`from underautomation.universal_robots.common.rest_connect_parameters import RestConnectParameters`

Configuration parameters for REST API connection (PolyscopeX only)

- `enable: bool`: Enable REST API client communication. Default value is false because REST API is only available on PolyscopeX robots.
- Inherited from [RestClientParametersBase](underautomation.universal_robots.rest.internal.md#restclientparametersbase): `DEFAULT_PORT`, `DEFAULT_TIMEOUT_MS`, `port`, `version`, `timeout_ms`

## RobotModels (robot.primary_interface.configuration_data.robot_type)

`from underautomation.universal_robots.common.robot_models import RobotModels`

Model of a UR robot

- UR5: UR5 robot model.
- UR10: UR10 robot model.
- UR3: UR3 robot model.
- UR16: UR16 robot model.
- UR20: UR20 robot model.
- UR30: UR30 robot model.
- UR8L: UR8 Long robot model.
- UR18: UR18 robot model.

## RobotModelsExtended

`from underautomation.universal_robots.common.robot_models_extended import RobotModelsExtended`

Model of a UR robot (including e-Series and extended payload models)

- UR3e: UR3e (e-Series).
- UR5e: UR5e (e-Series).
- UR7e: UR7e (e-Series).
- UR10e: UR10e (e-Series).
- UR12e: UR12e (e-Series).
- UR16e: UR16e (e-Series).
- UR15: UR15 robot model.
- UR18: UR18 robot model.
- UR20: UR20 robot model.
- UR30: UR30 robot model.
- UR8Long: UR8 Long robot model.
- UR3: UR3 (CB-Series).
- UR5: UR5 (CB-Series).
- UR10: UR10 (CB-Series).

## RobotModes (robot.primary_interface.robot_mode_data.robot_mode)

`from underautomation.universal_robots.common.robot_modes import RobotModes`

Robot running modes

- Other: Robot is in an obsolete CB2 mode
- Disconnected: Robot is not connected to its controller
- ConfirmSafety: Robot has stopped due to a Safety Stop
- Booting: The robot controller is booting
- PowerOff: The robot is powered off
- PowerOn: The robot is powered on
- Idle: Power is on but breaks are not released
- BackDrive: The robot is hand guided by pushing teached button
- Running: Robot is in normal mode
- UpdatingFirmware: Firmware is upgrading

## RobotSubTypes (robot.primary_interface.configuration_data.robot_sub_type)

`from underautomation.universal_robots.common.robot_sub_types import RobotSubTypes`

Robot sub type (e-Serie or CB-Serie)

- CB2Serie: CB2-series (Firmware 1.x)
- CB3Serie: CB3-series (Firmware 3.x)
- ESerie: e-series (Firmware 5.x)

## RtdeConnectParameters

`from underautomation.universal_robots.common.rtde_connect_parameters import RtdeConnectParameters`

Setup RTDE (Real-Time Data Exchange) client communication

- `enable: bool`: Choose to enable RTDE (Real-Time Data Exchange) Default value is false
- Inherited from [RtdeParametersBase](underautomation.universal_robots.rtde.internal.md#rtdeparametersbase): `DEFAULT_PORT`, `frequency`, `version`, `output_setup`, `input_setup`, `port`

## SafetyStatus (robot.primary_interface.masterboard_data.safetymode)

`from underautomation.universal_robots.common.safety_status import SafetyStatus`

Safety modes

- Normal: Safety is in normal operating conditions
- Reduced: Speed is reduced
- ProtectiveStop: Protective safeguard Stop. This safety function is triggeredby an external protective device using safety inputs which will trigger a Cat 2 stop3per IEC 60204-1.
- Recovery: When a safety limit is violated, the safety system must be restarted.
- SafeguardStop: (SI0 + SI1 + SBUS) Physical s-stop interface input
- SystemEmergencyStop: (EA + EB + SBUS->Euromap67) Physical e-stop interface input activated
- RobotEmergencyStop: (EA + EB + SBUS->Screen) Physical e-stop interface input activated
- Violation: Safety is in violation mode (for example, violation of the allowed delay between redundant signals)
- Fault: Safety is in fault mode
- AutomaticModeSafeguardStop: Automatic mode safeguard stop is active.
- SystemThreePositionEnablingStop: System three-position enabling device stop is active.

## SocketCommunicationConnectParameters

`from underautomation.universal_robots.common.socket_communication_connect_parameters import SocketCommunicationConnectParameters`

Setup socket communication server

- `enable: bool`: Choose to enable socket communication server Default value is false
- Inherited from [SocketCommunicationParametersBase](underautomation.universal_robots.socket_communication.internal.md#socketcommunicationparametersbase): `port`

## SshConnectParameters

`from underautomation.universal_robots.common.ssh_connect_parameters import SshConnectParameters`

Setup SSH client

- `SshConnectParameters()`
- `enable_ssh: bool`: Choose to enable SSH command line client Default value is false
- `enable_sftp: bool`: Choose to enable FTP Default value is false
- Inherited from [SshParametersBase](underautomation.universal_robots.ssh.internal.md#sshparametersbase): `DEFAULT_PORT`, `username`, `password`, `port`

## StatusCode

`from underautomation.universal_robots.common.status_code import StatusCode`

Status code that describes an internal error or an internal action

- OK: The action succeeded
- ReadThreadAborted: The read thread has stopped due to an internal exception. No more data event will be raised.
- DecodageError: The data received are inconsistent and it not possible to decode it.
- SendCommandInternalError: Unable to send URScript because of an internal error.
- SentCommandIsEmpty: Unable to send URScript because the script sent is empty.
- StreamingInterfaceNotConnected: Streaming interface is not connected
- XmlRpcInternalError: An error occured in the XML-RPC server
- GlobalVariablesError: An error occured while decoding global variables
- SocketInternalError: An error occured while handling socket packet
- RTDEThreadAborted: The RTDE read thread has stopped due to an internal exception. No more data event will be raised.
- WriteInputsRtdeError: Error occured while writing RTDE input data
- RTDEOverrun: RTDE Event handler takes longer to execute than the time between each RTDE packets

## ToolModes (robot.primary_interface.tool_data.tool_mode)

`from underautomation.universal_robots.common.tool_modes import ToolModes`

Tool modes

- Bootloader: Bootloader
- Running: Running
- Idle: Idle

## Vector3D (robot.rtde.output_data_values.actual_tool_accelerometer)

`from underautomation.universal_robots.common.vector3_d import Vector3D`

Represents a three-dimensional vector with X, Y, and Z components.

- `Vector3D()`
- `x: float`: X component of the vector.
- `y: float`: Y component of the vector.
- `z: float`: Z component of the vector.
- `values: typing.List[float]`: Underlying array of 3 double values storing X, Y, Z in that order.

## XmlRpcConnectParameters

`from underautomation.universal_robots.common.xml_rpc_connect_parameters import XmlRpcConnectParameters`

Setup XML-RPC server

- `XmlRpcConnectParameters()`
- `enable: bool`: Enable XML-RPC server
- Inherited from [XmlRpcParametersBase](underautomation.universal_robots.xml_rpc.internal.md#xmlrpcparametersbase): `port`
