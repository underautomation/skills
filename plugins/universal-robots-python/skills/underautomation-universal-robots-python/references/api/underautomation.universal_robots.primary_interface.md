# underautomation.universal_robots.primary_interface

## AdditionalInfoPackageEventArgs (robot.primary_interface.additional_info)

`from underautomation.universal_robots.primary_interface.additional_info_package_event_args import AdditionalInfoPackageEventArgs`

Additional information

- `AdditionalInfoPackageEventArgs()`
- `freedrive_button_pressed: bool`: The free drive button is pressed
- `freedrive_button_enabled: bool`: The free drive button is enabled
- `io_enabled_freedrive: bool`: Free drive is enable via IO
- Inherited from [PackageEventArgs](underautomation.universal_robots.common.md#packageeventargs-robotprimary_interfacerobot_mode_data): `receive_date`

## CalibrationDataPackageEventArgs (robot.primary_interface.calibration_data)

`from underautomation.universal_robots.primary_interface.calibration_data_package_event_args import CalibrationDataPackageEventArgs`

Calibration data

- `CalibrationDataPackageEventArgs()`
- `fx: float`: Fx calibration data
- `fy: float`: Fy calibration data
- `fz: float`: Fz calibration data
- `frx: float`: Frx calibration data
- `fry: float`: Fry calibration data
- `frz: float`: Frz calibration data
- Inherited from [PackageEventArgs](underautomation.universal_robots.common.md#packageeventargs-robotprimary_interfacerobot_mode_data): `receive_date`

## CartesianInfoPackageEventArgs (robot.primary_interface.cartesian_info)

`from underautomation.universal_robots.primary_interface.cartesian_info_package_event_args import CartesianInfoPackageEventArgs`

Contains current cartesian position of the robot, including its TCP offset

- `CartesianInfoPackageEventArgs()`
- `as_pose() -> Pose`: Returns the current cartesian position as a Pose object
- `as_tcp_offset_pose() -> Pose`: Returns the TCP offset as a Pose object
- `x: float`: X axis coordinate in meter of the TCP in the current frame
- `y: float`: Y axis coordinate in meter of the TCP in the current frame
- `z: float`: Z axis coordinate in meter of the TCP in the current frame
- `rx: float`: RX axis coordinate in rad of the TCP in the current frame
- `ry: float`: RY axis coordinate in rad of the TCP in the current frame
- `rz: float`: RZ axis coordinate in rad of the TCP in the current frame
- `tcp_offset_x: float`: X position of the TCP in the flange frame in meter
- `tcp_offset_y: float`: Y position of the TCP in the flange frame in meter
- `tcp_offset_z: float`: Z position of the TCP in the flange frame in meter
- `tcp_offset_rx: float`: RX position of the TCP in the flange frame in rad
- `tcp_offset_ry: float`: RY position of the TCP in the flange frame in rad
- `tcp_offset_rz: float`: RZ position of the TCP in the flange frame in rad
- Inherited from [PackageEventArgs](underautomation.universal_robots.common.md#packageeventargs-robotprimary_interfacerobot_mode_data): `receive_date`

## ConfigurationDataPackageEventArgs (robot.primary_interface.configuration_data)

`from underautomation.universal_robots.primary_interface.configuration_data_package_event_args import ConfigurationDataPackageEventArgs`

Joint configuration

- `ConfigurationDataPackageEventArgs()`
- `v_joint_default: float`: Default joint angular speed in rad/s
- `a_joint_default: float`: Default joint acceleration speed in rad/s²
- `v_tool_default: float`: Default TCP speed speed in m/s
- `a_tool_default: float`: Default TCP acceleration speed in m/s²
- `eq_radius: float`: Equipment radius in meter
- `masterboard_version: int`: Masterboard version
- `controller_box_type: ControllerBoxTypes`: Controller box type
- `robot_type: RobotModels`: Model of the robot (UR3, UR5, UR10, UR16, ...)
- `robot_sub_type: RobotSubTypes`: Robot series (e-Series, CB-Series, etc.)
- `base: JointConfiguration`: Base joint configuration
- `shoulder: JointConfiguration`: Shoulder joint configuration
- `elbow: JointConfiguration`: Elbow joint configuration
- `wrist1: JointConfiguration`: Wrist1 joint configuration
- `wrist2: JointConfiguration`: Wrist2 joint configuration
- `wrist3: JointConfiguration`: Wrist3 (Tool) joint configuration
- `a2: float (read only)`: DH parameter a2 (Shoulder.DHa)
- `a3: float (read only)`: DH parameter a3 (Elbow.DHa)
- `d1: float (read only)`: DH parameter d1 (Base.DHd)
- `d4: float (read only)`: DH parameter d4 (Wrist1.DHd)
- `d5: float (read only)`: DH parameter d5 (Wrist2.DHd)
- `d6: float (read only)`: DH parameter d6 (Wrist3.DHd)
- Inherited from [PackageEventArgs](underautomation.universal_robots.common.md#packageeventargs-robotprimary_interfacerobot_mode_data): `receive_date`

## ForceModeDataPackageEventArgs (robot.primary_interface.force_mode_data)

`from underautomation.universal_robots.primary_interface.force_mode_data_package_event_args import ForceModeDataPackageEventArgs`

Force mode data

- `ForceModeDataPackageEventArgs()`
- `x: float`: X force in tool frame in N
- `y: float`: Y force in tool frame in N
- `z: float`: Z force in tool frame in N
- `rx: float`: Rx torque in tool frame in Nm
- `ry: float`: Ry torque in tool frame in Nm
- `rz: float`: Rz torque in tool frame in Nm
- `robot_dexterity: float`: Dexterity of the robot
- Inherited from [PackageEventArgs](underautomation.universal_robots.common.md#packageeventargs-robotprimary_interfacerobot_mode_data): `receive_date`

## GlobalVariables (robot.primary_interface.global_variables)

`from underautomation.universal_robots.primary_interface.global_variables import GlobalVariables`

List of all global variables

- `values_updated(handler)`: Event raised at 10Hz when variable values are updated
- `list_updated(handler)`: Event raised whan the variable list changed. For example, after a program starts
- `get_all() -> typing.List[GlobalVariable]`: Returns a list of all variables declared in the robot
- `get_by_name(name: str) -> GlobalVariable`: Get a variable by its name. Null is returned if the variable doesn't exist
- `firmware_version: GlobalVariablesFirmwareVersion (read only)`: Indicates which decoder is used used to read variables according to firmware version

## GlobalVariablesEventArgs

`from underautomation.universal_robots.primary_interface.global_variables_event_args import GlobalVariablesEventArgs`

Event args of variable update events

- `variables: typing.List[GlobalVariable] (read only)`: New list of all up to date variables

## GlobalVariablesFirmwareVersion (robot.primary_interface.global_variables.firmware_version)

`from underautomation.universal_robots.primary_interface.global_variables_firmware_version import GlobalVariablesFirmwareVersion`

Firmware version for variable decoding

- UpTo32: FW up to 3.2
- UpTo59: FW up to 5.9
- Latest: Recent firmware

## Interfaces (robot.primary_interface.port)

`from underautomation.universal_robots.primary_interface.interfaces import Interfaces`

TCP ports to communicate with an UR controller

- PrimaryInterface: The default port that allow reading data and sending URScript
- SecondaryInterface: The secondary port with same features as PrimaryClient
- PrimaryInterfaceReadOnly: This port can only read data. It is unable to send URScript.
- SecondaryInterfaceReadOnly: A secondary port that can only read data. It is unable to send URScript.

## JointConfiguration (robot.primary_interface.configuration_data.base)

`from underautomation.universal_robots.primary_interface.joint_configuration import JointConfiguration`

Joint configuration

- `JointConfiguration()`
- `joint_min_limit: float`: Minimum angular position in rad
- `joint_max_limit: float`: Maximum angular position in rad
- `joint_max_speed: float`: Maximum rotation speed in rad/s
- `joint_max_acceleration: float`: Maximum rotation speed in rad/s²
- `d_ha: float`: a parameter of Denavit–Hartenberg (DH) convention
- `d_hd: float`: d parameter of Denavit–Hartenberg (DH) convention
- `d_halpha: float`: Alpha parameter of Denavit–Hartenberg (DH) convention
- `d_htheta: float`: Theta parameter of Denavit–Hartenberg (DH) convention

## JointData (robot.primary_interface.joint_data.base)

`from underautomation.universal_robots.primary_interface.joint_data import JointData`

Joint data

- `JointData()`
- `position: float`: Angular joint position in radian
- `target_position: float`: Angular target position in radian
- `actual_speed: float`: Joint rotation speed in rad/s
- `current: float`: Motor current in Amps
- `voltage: float`: Motor voltage in Volts
- `temperature: float`: Joint temperature in °C
- `joint_mode: JointModes`: Joint mode

## JointDataPackageEventArgs (robot.primary_interface.joint_data)

`from underautomation.universal_robots.primary_interface.joint_data_package_event_args import JointDataPackageEventArgs`

Status of each joints

- `JointDataPackageEventArgs()`
- `base: JointData`: Base joint data
- `shoulder: JointData`: Shoulder joint data
- `elbow: JointData`: Elbow joint data
- `wrist1: JointData`: Wrist1 joint data
- `wrist2: JointData`: Wrist2 joint data
- `wrist3: JointData`: Wrist3 (Tool) joint data
- Inherited from [PackageEventArgs](underautomation.universal_robots.common.md#packageeventargs-robotprimary_interfacerobot_mode_data): `receive_date`

## JointKinematicsInfo (robot.primary_interface.kinematics_info.base)

`from underautomation.universal_robots.primary_interface.joint_kinematics_info import JointKinematicsInfo`

Joint kinematics info, Denavit–Hartenberg (DH) parameters

- `JointKinematicsInfo()`
- `checksum: int`: Joint checksum
- `d_htheta: float`: DH convention theta parameter
- `d_ha: float`: DH convention a parameter
- `d_hd: float`: DH convention d parameter
- `dhalpha: float`: DH convention alpha parameter

## KeyMessageEventArgs (robot.primary_interface.key_message)

`from underautomation.universal_robots.primary_interface.key_message_event_args import KeyMessageEventArgs`

Internal robot events (such as starting or stopping a program)

- `KeyMessageEventArgs()`
- `robot_message_code: int`: Message code
- `robot_message_argument: int`: Message argument
- `robot_message_title: str`: Message title
- `key_text_message: str`: Message key
- Inherited from [PackageEventArgs](underautomation.universal_robots.common.md#packageeventargs-robotprimary_interfacerobot_mode_data): `receive_date`

## KinematicsInfoPackageEventArgs (robot.primary_interface.kinematics_info)

`from underautomation.universal_robots.primary_interface.kinematics_info_package_event_args import KinematicsInfoPackageEventArgs`

Kinematics info

- `KinematicsInfoPackageEventArgs()`
- `calibration_status: int`: Calibration status (0 : OK)
- `base: JointKinematicsInfo`: Base kinematics info
- `shoulder: JointKinematicsInfo`: Shoulder kinematics info
- `elbow: JointKinematicsInfo`: Elbow kinematics info
- `wrist1: JointKinematicsInfo`: Wrist1 kinematics info
- `wrist2: JointKinematicsInfo`: Wrist2 kinematics info
- `wrist3: JointKinematicsInfo`: Wrist3 (Tool) kinematics info
- `a2: float (read only)`: DH parameter a2 (Shoulder.DHa)
- `a3: float (read only)`: DH parameter a3 (Elbow.DHa)
- `d1: float (read only)`: DH parameter d1 (Base.DHd)
- `d4: float (read only)`: DH parameter d4 (Wrist1.DHd)
- `d5: float (read only)`: DH parameter d5 (Wrist2.DHd)
- `d6: float (read only)`: DH parameter d6 (Wrist3.DHd)
- Inherited from [PackageEventArgs](underautomation.universal_robots.common.md#packageeventargs-robotprimary_interfacerobot_mode_data): `receive_date`

## MasterboardDataPackageEventArgs (robot.primary_interface.masterboard_data)

`from underautomation.universal_robots.primary_interface.masterboard_data_package_event_args import MasterboardDataPackageEventArgs`

Masterboard data

- `MasterboardDataPackageEventArgs()`
- `analog_input_range0: AnalogRanges`: Unit of analog input 0 (analog_in[0])
- `analog_input_range1: AnalogRanges`: Unit of analog input 1 (analog_in[1])
- `analog_input0: float`: Value of analog input 0 (analog_in[0])
- `analog_input1: float`: Value of analog input 1 (analog_in[1])
- `analog_output_domain0: AnalogRanges`: Unit of analog output 0 (analog_out[0])
- `analog_output_domain1: AnalogRanges`: Unit of analog output 1 (analog_out[1])
- `analog_output0: float`: Value of analog output 0 (analog_out[0])
- `analog_output1: float`: Value of analog output 1 (analog_out[1])
- `masterboard_temperature: float`: Temperature of masterboard in °C
- `robot_voltage48_v: float`: Voltage of internal 48V power supply
- `robot_current: float`: Robot current consumption in Amps
- `master_io_current: float`: Current of all digital and analog inputs and outputs
- `safetymode: SafetyStatus`: Masterboard safety mode
- `in_reduced_mode: int`: Robot is in reduced speed mode
- `operational_mode_selector_input: int`: Position of operational mode selector input switch
- `three_position_enabling_device_input: int`: Position of the 3-position enabling device
- `digital_inputs: MasterboardDigitalIO`: Register where each bit is a digital input value
- `digital_outputs: MasterboardDigitalIO`: Register where each bit is a digital output value
- `euromap67_installed: int`: The robot is interfaced to injection molding machines Euromap 67
- `euromap_input_bits: int`: Register where each bit is a digital Euromap input
- `euromap_output_bits: int`: Register where each bit is a digital Euromap output
- `euromap_voltage: float`: Euromap voltage
- `euromap_current: float`: Euromap current
- Inherited from [PackageEventArgs](underautomation.universal_robots.common.md#packageeventargs-robotprimary_interfacerobot_mode_data): `receive_date`

## MasterboardDigitalIO (robot.primary_interface.masterboard_data.digital_inputs)

`from underautomation.universal_robots.primary_interface.masterboard_digital_io import MasterboardDigitalIO`

Represents the state of digital I/O pins on the UR controller masterboard, including standard digital, configurable, and tool digital pins.

- `value: int (read only)`: Register value
- `bit_array: typing.Any (read only)`: Register value seen as a bool array
- `digital0: bool (read only)`: State of standard digital I/O pin 0.
- `digital1: bool (read only)`: State of standard digital I/O pin 1.
- `digital2: bool (read only)`: State of standard digital I/O pin 2.
- `digital3: bool (read only)`: State of standard digital I/O pin 3.
- `digital4: bool (read only)`: State of standard digital I/O pin 4.
- `digital5: bool (read only)`: State of standard digital I/O pin 5.
- `digital6: bool (read only)`: State of standard digital I/O pin 6.
- `digital7: bool (read only)`: State of standard digital I/O pin 7.
- `configurable0: bool (read only)`: State of configurable digital I/O pin 0.
- `configurable1: bool (read only)`: State of configurable digital I/O pin 1.
- `configurable2: bool (read only)`: State of configurable digital I/O pin 2.
- `configurable3: bool (read only)`: State of configurable digital I/O pin 3.
- `configurable4: bool (read only)`: State of configurable digital I/O pin 4.
- `configurable5: bool (read only)`: State of configurable digital I/O pin 5.
- `configurable6: bool (read only)`: State of configurable digital I/O pin 6.
- `configurable7: bool (read only)`: State of configurable digital I/O pin 7.
- `tool_digital0: bool (read only)`: State of tool digital I/O pin 0.
- `tool_digital1: bool (read only)`: State of tool digital I/O pin 1.

## PackageDescriptionAttribute

`from underautomation.universal_robots.primary_interface.package_description_attribute import PackageDescriptionAttribute`

Describes a field of a received package

- `PackageDescriptionAttribute(description: str, unit: PackageUnit)`: Initializes a new instance with a specified physical unit.
- `unit: PackageUnit (read only)`: Physical unit of the field

## PackageUnit

`from underautomation.universal_robots.primary_interface.package_unit import PackageUnit`

Physical units of receives measures

- NoUnit: No unit
- Radian: rad
- RadianPerSecond: rad/s
- RadianPerSecondSquared: rad/s²
- Meter: m
- MeterPerSecond: m/s
- MetersPerSecondSquared: m/s²
- CelsiusDegree: °C
- Volt: V
- Amp: A

## PopupMessageEventArgs (robot.primary_interface.popup_message)

`from underautomation.universal_robots.primary_interface.popup_message_event_args import PopupMessageEventArgs`

Popup message that appears with the Assignment instruction or the URScript popup() function

- `PopupMessageEventArgs()`
- `request_id: int`: Each popup has a unique ID
- `requested_type: RequestedTypes`: Type for assignment popups
- `warning: bool`: Popup is a warning
- `error: bool`: Popup is an error
- `blocking: bool`: Popup is blocking script execution
- `popup_message_title: str`: Popup title
- `popup_text_message: str`: Popup message, null for assignment popups
- Inherited from [PackageEventArgs](underautomation.universal_robots.common.md#packageeventargs-robotprimary_interfacerobot_mode_data): `receive_date`

## PrimaryInterfaceClient

`from underautomation.universal_robots.primary_interface.primary_interface_client import PrimaryInterfaceClient`

Primary / Secondary interface implementation

- `PrimaryInterfaceClient()`: Creates a new Primary Interface client
- `connect(ip: str, port: Interfaces) -> None`: Connect to a specific port
- `connect(ip: str) -> None`: Connect to primary interface
- Inherited from [PrimaryInterfaceClientBase](underautomation.universal_robots.primary_interface.internal.md#primaryinterfaceclientbase-robotprimary_interface): `disconnect`, `robot_mode_data`, `joint_data`, `tool_data`, `masterboard_data`, `cartesian_info`, `kinematics_info`, `configuration_data`, `force_mode_data`, `additional_info`, `calibration_data`, `safety_data`, `tool_communication_info`, `tool_mode_info`, `singularity_info`, `program_threads`, `version`, `key_message`, `popup_message`, `text_message`, `runtime_exception_message`, `global_variables`, `script`, `commands`, `ip`, `port`, `connected`, `local_end_point`, `robot_mode_data_received`, `joint_data_received`, `tool_data_received`, `masterboard_data_received`, `cartesian_info_received`, `kinematics_info_received`, `configuration_data_received`, `force_mode_data_received`, `additional_info_received`, `calibration_data_received`, `safety_data_received`, `tool_communication_info_received`, `tool_mode_info_received`, `singularity_info_received`, `package_received`, `raw_package_received`, `program_threads_received`, `version_received`, `key_message_received`, `popup_message_received`, `text_message_received`, `runtime_exception_message_received`
- Inherited from [URServiceBase](underautomation.universal_robots.internal.md#urservicebase-robot): `internal_error_occured`

## ProgramThread

`from underautomation.universal_robots.primary_interface.program_thread import ProgramThread`

Represents a single running thread in a UR program.

- `ProgramThread()`
- `line_number: int`: Current line number being executed in the program.
- `line_name: str`: Name of the program line being executed.
- `thread_name: str`: Name of the thread.

## ProgramThreadsEventArgs (robot.primary_interface.program_threads)

`from underautomation.universal_robots.primary_interface.program_threads_event_args import ProgramThreadsEventArgs`

Event data containing information about currently running program threads.

- `ProgramThreadsEventArgs()`
- `threads: typing.List[ProgramThread]`: Array of currently running program threads.
- Inherited from [PackageEventArgs](underautomation.universal_robots.common.md#packageeventargs-robotprimary_interfacerobot_mode_data): `receive_date`

## RequestValueMessageEventArgs

`from underautomation.universal_robots.primary_interface.request_value_message_event_args import RequestValueMessageEventArgs`

Event data for a request value message received from the robot (assignment popup requesting user input).

- `RequestValueMessageEventArgs()`
- `request_id: int`: Unique identifier of the request.
- `requested_type: RequestedTypes`: Data type requested from the user.
- `request_text_message: str`: Message displayed to the user in the request popup.
- Inherited from [PackageEventArgs](underautomation.universal_robots.common.md#packageeventargs-robotprimary_interfacerobot_mode_data): `receive_date`

## RequestedTypes (robot.primary_interface.popup_message.requested_type)

`from underautomation.universal_robots.primary_interface.requested_types import RequestedTypes`

Types for popup assignment

- Boolean: Popup for boolean value assignment
- Integer: Popup for integer number value assignment
- Float: Popup for float number value assignment
- String: Popup for string value assignment
- Pose: Popup for pose value assignment
- JointVector: Popup for joint vector value assignment
- Waypoint: Unused
- Expression: Unused
- None_: It's a simple popup message

## RobotModeDataPackageEventArgs (robot.primary_interface.robot_mode_data)

`from underautomation.universal_robots.primary_interface.robot_mode_data_package_event_args import RobotModeDataPackageEventArgs`

Information about current robot mode

- `RobotModeDataPackageEventArgs()`
- `timestamp: typing.Any`: Timespan since the robot controller has started
- `physical_robot_connected: bool`: Robot is connected to its controller
- `real_robot_enabled: bool`: Real robot mode active. False if robot is in simulation
- `robot_power_on: bool`: Robot is powered on and boot is completed. If false, you need to press "ON" button to power it on
- `emergency_stopped: bool`: The button Emergency Stop is pressed
- `protective_stopped: bool`: A stop occured due to a fault detection
- `program_running: bool`: A program is running
- `program_paused: bool`: The running program is paused
- `robot_mode: RobotModes`: Current robot running mode
- `control_mode: ControlModes`: Current robot control mode
- `target_speed_fraction: float`: Overriden speed ratio between 0 (0%) and 1 (100%)
- `speed_scaling: float`: Speed scaling
- `target_speed_fraction_limit: float`: Maximum target speed fraction
- Inherited from [PackageEventArgs](underautomation.universal_robots.common.md#packageeventargs-robotprimary_interfacerobot_mode_data): `receive_date`

## RuntimeExceptionMessageEventArgs (robot.primary_interface.runtime_exception_message)

`from underautomation.universal_robots.primary_interface.runtime_exception_message_event_args import RuntimeExceptionMessageEventArgs`

Reports an error in the execution of the program

- `RuntimeExceptionMessageEventArgs()`
- `script_line_number: int`: Execution error line number
- `script_column_number: int`: Execution error column number
- `runtime_exception_text_message: str`: Information about exception
- Inherited from [PackageEventArgs](underautomation.universal_robots.common.md#packageeventargs-robotprimary_interfacerobot_mode_data): `receive_date`

## SafetyDataPackageEventArgs (robot.primary_interface.safety_data)

`from underautomation.universal_robots.primary_interface.safety_data_package_event_args import SafetyDataPackageEventArgs`

Safety internal data

- `SafetyDataPackageEventArgs()`
- `data: typing.List[int]`: Irrelevant (Internal use only)
- Inherited from [PackageEventArgs](underautomation.universal_robots.common.md#packageeventargs-robotprimary_interfacerobot_mode_data): `receive_date`

## SingularityInfoPackageEventArgs (robot.primary_interface.singularity_info)

`from underautomation.universal_robots.primary_interface.singularity_info_package_event_args import SingularityInfoPackageEventArgs`

Singularity info

- `SingularityInfoPackageEventArgs()`
- `singularity_severity: int`: Severity of the singularity
- `singularity_type: int`: Type of the singularity
- Inherited from [PackageEventArgs](underautomation.universal_robots.common.md#packageeventargs-robotprimary_interfacerobot_mode_data): `receive_date`

## TextMessageEventArgs (robot.primary_interface.text_message)

`from underautomation.universal_robots.primary_interface.text_message_event_args import TextMessageEventArgs`

Describes a log message sent with URScript instruction textmsg()

- `TextMessageEventArgs()`
- `text_message: str`: Log message sent with URScript instruction textmsg()
- Inherited from [PackageEventArgs](underautomation.universal_robots.common.md#packageeventargs-robotprimary_interfacerobot_mode_data): `receive_date`

## ToolCommunicationInfoPackageEventArgs (robot.primary_interface.tool_communication_info)

`from underautomation.universal_robots.primary_interface.tool_communication_info_package_event_args import ToolCommunicationInfoPackageEventArgs`

Tool communication info

- `ToolCommunicationInfoPackageEventArgs()`
- `tool_communication_is_enabled: bool`: Is the tool communication interface enabled
- `baud_rate: int`: Baud rate for tool serial communication
- `parity: int`: Parity
- `stop_bits: int`: Stop bits
- `rx_idle_chars: float`: RX Idle Chars
- `tx_idle_chars: float`: TX Idle Chars
- Inherited from [PackageEventArgs](underautomation.universal_robots.common.md#packageeventargs-robotprimary_interfacerobot_mode_data): `receive_date`

## ToolDataPackageEventArgs (robot.primary_interface.tool_data)

`from underautomation.universal_robots.primary_interface.tool_data_package_event_args import ToolDataPackageEventArgs`

Tool data

- `ToolDataPackageEventArgs()`
- `analog_input_range2: AnalogRanges`: Unit of analog input 2 (analog_in[2])
- `analog_input_range3: AnalogRanges`: Unit of analog input 3 (analog_in[3])
- `analog_input2: float`: Value of Analog input 2 (analog_in[2])
- `analog_input3: float`: Value of Analog input 3 (analog_in[3])
- `tool_voltage48_v: float`: Actual robot voltage power supply
- `tool_output_voltage: int`: Tool output voltage
- `tool_current: float`: Tool current in Amps
- `tool_temperature: float`: Tool Temperature in °C
- `tool_mode: ToolModes`: Tool mode
- Inherited from [PackageEventArgs](underautomation.universal_robots.common.md#packageeventargs-robotprimary_interfacerobot_mode_data): `receive_date`

## ToolModeInfoPackageEventArgs (robot.primary_interface.tool_mode_info)

`from underautomation.universal_robots.primary_interface.tool_mode_info_package_event_args import ToolModeInfoPackageEventArgs`

Tool mode info

- `ToolModeInfoPackageEventArgs()`
- `output_mode: OutputModes`: Digital output mode
- `digital_output_mode0: DigitalOutputConfigurations`: Digital output 0 configuration
- `digital_output_mode1: DigitalOutputConfigurations`: Digital output 1 configuration
- Inherited from [PackageEventArgs](underautomation.universal_robots.common.md#packageeventargs-robotprimary_interfacerobot_mode_data): `receive_date`

## VersionEventArgs (robot.primary_interface.version)

`from underautomation.universal_robots.primary_interface.version_event_args import VersionEventArgs`

Version information from the robot controller firmware

- `VersionEventArgs()`
- `project_name: str`: URControl project
- `major_version: int`: Major version number, for example 5 in 5.6.1.1234
- `minor_version: int`: Minor firmware version number, for example 6 in 5.6.1.1234
- `bugfix_version: int`: Firmware bugfix number, for example 1 in 5.6.1.1234
- `build_number: int`: Firmware build number, for example 1234 in 5.6.1.1234
- `build_date: str`: Build date of the firmware, for example "DEC 2020"
- `version: typing.Any (read only)`: Version of the firmware
- Inherited from [PackageEventArgs](underautomation.universal_robots.common.md#packageeventargs-robotprimary_interfacerobot_mode_data): `receive_date`
