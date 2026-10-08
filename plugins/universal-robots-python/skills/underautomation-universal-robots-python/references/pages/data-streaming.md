# Primary Interface: data streaming

Receive the state of a UR cobot at 10 Hz with the Primary Interface: robot mode, joints, tool, I/O, Cartesian position, kinematics and configuration.

Web page: https://underautomation.com/universal-robots/documentation/data-streaming

The Primary Interface of a Universal Robots cobot sends the state of the robot 10 times per second: modes, joints, tool, I/O, Cartesian position, kinematics, configuration and messages. This page shows how to connect to it and read its data. The same connection sends URScript: see [Send URScript](remote-send-script.md).

## Connect

The Primary Interface is enabled by default: `Connect("192.168.0.1")` opens it. With a `ConnectParameters`, you can also choose the port:

| Port  | `Interfaces`                 | Data          | URScript |
| ----- | ---------------------------- | ------------- | -------- |
| 30001 | `PrimaryInterface` (default) | All packages  | yes      |
| 30002 | `SecondaryInterface`         | All packages  | yes      |
| 30011 | `PrimaryInterfaceReadOnly`   | All packages  | no       |
| 30012 | `SecondaryInterfaceReadOnly` | All packages  | no       |

```python
from underautomation.universal_robots.ur import UR
from underautomation.universal_robots.connect_parameters import ConnectParameters
from underautomation.universal_robots.primary_interface.interfaces import Interfaces

robot = UR()

parameters = ConnectParameters("192.168.0.1")

# The Primary Interface is enabled by default
parameters.primary_interface.enable = True

# Port 30001 (default) accepts URScript. The read only ports do not
parameters.primary_interface.port = Interfaces.PrimaryInterface

robot.connect(parameters)

# The last values received are in the properties of the client
base_speed = robot.primary_interface.joint_data.base.actual_speed

# Close the Primary Interface only
robot.primary_interface.disconnect()

# Close every service
robot.disconnect()
```

The same client works without `UR`:

```python
from underautomation.universal_robots.primary_interface.primary_interface_client import PrimaryInterfaceClient
from underautomation.universal_robots.primary_interface.interfaces import Interfaces

# A Primary Interface client, without a UR instance
client = PrimaryInterfaceClient()

client.connect("192.168.0.1", Interfaces.PrimaryInterface)

base_speed = client.joint_data.base.actual_speed

client.disconnect()
```

The service `Primary Client Interface` must be enabled on the robot: see [Prepare the robot](connect.md#prepare_the_robot). For the data of the interface, see [Remote control via TCP/IP](https://www.universal-robots.com/articles/ur/interface-communication/remote-control-via-tcpip/) by Universal Robots.

## Read the data

Each package of the robot has a property, which holds the last values received, and an event, raised when the package arrives. A property is `null` until its first package: wait about 100 ms after the connection.

```python
from underautomation.universal_robots.ur import UR

robot = UR()

robot.connect("192.168.0.1")

# Last package received, read at any time
joints = robot.primary_interface.joint_data
shoulder = joints.shoulder.position  # rad

tool = robot.primary_interface.cartesian_info
x = tool.x  # m

# Or an event, raised when a package arrives (10 Hz).
# Read the values in the properties of the client
def on_joint_data(sender, e):
    wrist3_speed = robot.primary_interface.joint_data.wrist3.actual_speed  # rad/s

robot.primary_interface.joint_data_received(on_joint_data)

def on_robot_mode(sender, e):
    program_running = robot.primary_interface.robot_mode_data.program_running

robot.primary_interface.robot_mode_data_received(on_robot_mode)
```

The sections below list the content of each package.

## State of the connection

`Connected` becomes `false` when the connection is lost (robot stopped, cable unplugged). No event is raised and there is no automatic reconnection: call `Connect` again. `InternalErrorOccured` is raised when the SDK meets an error.

```python
from underautomation.universal_robots.ur import UR
from underautomation.universal_robots.common.internal_error_event_args import InternalErrorEventArgs

robot = UR()

robot.connect("192.168.0.1")

# False after a loss of the connection. There is no automatic reconnection
connected = robot.primary_interface.connected

if not connected:
    robot.connect("192.168.0.1")

# Raised when an error happens in the background
def on_error(sender, e):
    error = InternalErrorEventArgs(e._instance)
    print(error.status, error.message, error.exception)

robot.primary_interface.internal_error_occured(on_error)
```

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Packages

### Robot mode

**RobotModeDataPackageEventArgs** ([reference](../api/underautomation.universal_robots.primary_interface.md#robotmodedatapackageeventargs-robotprimary_interfacerobot_mode_data))

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
- Inherited from [PackageEventArgs](../api/underautomation.universal_robots.common.md#packageeventargs-robotprimary_interfacerobot_mode_data): `receive_date`

**ControlModes** ([reference](../api/underautomation.universal_robots.common.md#controlmodes-robotprimary_interfacerobot_mode_datacontrol_mode))

- Position: Robot is position controlled
- Teach: The robot is hand guided by pushing teached button
- Force: Robot is force controlled. (For example : URScript force_mode() function is called)
- Torque: Robot is torque controlled

**RobotModes** ([reference](../api/underautomation.universal_robots.common.md#robotmodes-robotprimary_interfacerobot_mode_datarobot_mode))

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

### Joint data

**JointDataPackageEventArgs** ([reference](../api/underautomation.universal_robots.primary_interface.md#jointdatapackageeventargs-robotprimary_interfacejoint_data))

- `JointDataPackageEventArgs()`
- `base: JointData`: Base joint data
- `shoulder: JointData`: Shoulder joint data
- `elbow: JointData`: Elbow joint data
- `wrist1: JointData`: Wrist1 joint data
- `wrist2: JointData`: Wrist2 joint data
- `wrist3: JointData`: Wrist3 (Tool) joint data
- Inherited from [PackageEventArgs](../api/underautomation.universal_robots.common.md#packageeventargs-robotprimary_interfacerobot_mode_data): `receive_date`

![Joints of a UR robot](https://underautomation.com/universal-robots/joints.png)

**JointData** ([reference](../api/underautomation.universal_robots.primary_interface.md#jointdata-robotprimary_interfacejoint_database))

- `JointData()`
- `position: float`: Angular joint position in radian
- `target_position: float`: Angular target position in radian
- `actual_speed: float`: Joint rotation speed in rad/s
- `current: float`: Motor current in Amps
- `voltage: float`: Motor voltage in Volts
- `temperature: float`: Joint temperature in °C
- `joint_mode: JointModes`: Joint mode

**JointModes** ([reference](../api/underautomation.universal_robots.common.md#jointmodes-robotprimary_interfacejoint_databasejoint_mode))

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

### Tool data

**ToolDataPackageEventArgs** ([reference](../api/underautomation.universal_robots.primary_interface.md#tooldatapackageeventargs-robotprimary_interfacetool_data))

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
- Inherited from [PackageEventArgs](../api/underautomation.universal_robots.common.md#packageeventargs-robotprimary_interfacerobot_mode_data): `receive_date`

**AnalogRanges** ([reference](../api/underautomation.universal_robots.common.md#analogranges-robotprimary_interfacetool_dataanalog_input_range2))

- Current: The analog value is in Amps (A)
- Voltage: The analog value is in Volts (V)

**ToolModes** ([reference](../api/underautomation.universal_robots.common.md#toolmodes-robotprimary_interfacetool_datatool_mode))

- Bootloader: Bootloader
- Running: Running
- Idle: Idle

### Masterboard data

**MasterboardDataPackageEventArgs** ([reference](../api/underautomation.universal_robots.primary_interface.md#masterboarddatapackageeventargs-robotprimary_interfacemasterboard_data))

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
- Inherited from [PackageEventArgs](../api/underautomation.universal_robots.common.md#packageeventargs-robotprimary_interfacerobot_mode_data): `receive_date`

**MasterboardDigitalIO** ([reference](../api/underautomation.universal_robots.primary_interface.md#masterboarddigitalio-robotprimary_interfacemasterboard_datadigital_inputs))

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

**SafetyStatus** ([reference](../api/underautomation.universal_robots.common.md#safetystatus-robotprimary_interfacemasterboard_datasafetymode))

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

### Cartesian information

**CartesianInfoPackageEventArgs** ([reference](../api/underautomation.universal_robots.primary_interface.md#cartesianinfopackageeventargs-robotprimary_interfacecartesian_info))

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
- Inherited from [PackageEventArgs](../api/underautomation.universal_robots.common.md#packageeventargs-robotprimary_interfacerobot_mode_data): `receive_date`

![Flange frame](https://underautomation.com/universal-robots/flange-frame-3d.png)

![Flange frame, projection](https://underautomation.com/universal-robots/flange-frame-projection.png)

### Kinematics information

**KinematicsInfoPackageEventArgs** ([reference](../api/underautomation.universal_robots.primary_interface.md#kinematicsinfopackageeventargs-robotprimary_interfacekinematics_info))

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
- Inherited from [PackageEventArgs](../api/underautomation.universal_robots.common.md#packageeventargs-robotprimary_interfacerobot_mode_data): `receive_date`

**JointKinematicsInfo** ([reference](../api/underautomation.universal_robots.primary_interface.md#jointkinematicsinfo-robotprimary_interfacekinematics_infobase))

- `JointKinematicsInfo()`
- `checksum: int`: Joint checksum
- `d_htheta: float`: DH convention theta parameter
- `d_ha: float`: DH convention a parameter
- `d_hd: float`: DH convention d parameter
- `dhalpha: float`: DH convention alpha parameter

These are the Denavit-Hartenberg parameters of the robot, with its calibration. See [Kinematics](kinematics.md) and the [DH parameters](https://www.universal-robots.com/articles/ur/application-installation/dh-parameters-for-calculations-of-kinematics-and-dynamics/) of each model.

### Configuration data

**ConfigurationDataPackageEventArgs** ([reference](../api/underautomation.universal_robots.primary_interface.md#configurationdatapackageeventargs-robotprimary_interfaceconfiguration_data))

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
- Inherited from [PackageEventArgs](../api/underautomation.universal_robots.common.md#packageeventargs-robotprimary_interfacerobot_mode_data): `receive_date`

**ControllerBoxTypes** ([reference](../api/underautomation.universal_robots.common.md#controllerboxtypes-robotprimary_interfaceconfiguration_datacontroller_box_type))

- UR3: UR3 controller box
- UR5: UR5 controller box
- UR10: UR10 controller box
- UR16: UR16 controller box
- UR20: UR20 controller box
- UR30: UR30 controller box

**JointConfiguration** ([reference](../api/underautomation.universal_robots.primary_interface.md#jointconfiguration-robotprimary_interfaceconfiguration_database))

- `JointConfiguration()`
- `joint_min_limit: float`: Minimum angular position in rad
- `joint_max_limit: float`: Maximum angular position in rad
- `joint_max_speed: float`: Maximum rotation speed in rad/s
- `joint_max_acceleration: float`: Maximum rotation speed in rad/s²
- `d_ha: float`: a parameter of Denavit–Hartenberg (DH) convention
- `d_hd: float`: d parameter of Denavit–Hartenberg (DH) convention
- `d_halpha: float`: Alpha parameter of Denavit–Hartenberg (DH) convention
- `d_htheta: float`: Theta parameter of Denavit–Hartenberg (DH) convention

**RobotSubTypes** ([reference](../api/underautomation.universal_robots.common.md#robotsubtypes-robotprimary_interfaceconfiguration_datarobot_sub_type))

- CB2Serie: CB2-series (Firmware 1.x)
- CB3Serie: CB3-series (Firmware 3.x)
- ESerie: e-series (Firmware 5.x)

**RobotModels** ([reference](../api/underautomation.universal_robots.common.md#robotmodels-robotprimary_interfaceconfiguration_datarobot_type))

- UR5: UR5 robot model.
- UR10: UR10 robot model.
- UR3: UR3 robot model.
- UR16: UR16 robot model.
- UR20: UR20 robot model.
- UR30: UR30 robot model.
- UR8L: UR8 Long robot model.
- UR18: UR18 robot model.

### Force mode data

**ForceModeDataPackageEventArgs** ([reference](../api/underautomation.universal_robots.primary_interface.md#forcemodedatapackageeventargs-robotprimary_interfaceforce_mode_data))

- `ForceModeDataPackageEventArgs()`
- `x: float`: X force in tool frame in N
- `y: float`: Y force in tool frame in N
- `z: float`: Z force in tool frame in N
- `rx: float`: Rx torque in tool frame in Nm
- `ry: float`: Ry torque in tool frame in Nm
- `rz: float`: Rz torque in tool frame in Nm
- `robot_dexterity: float`: Dexterity of the robot
- Inherited from [PackageEventArgs](../api/underautomation.universal_robots.common.md#packageeventargs-robotprimary_interfacerobot_mode_data): `receive_date`

### Additional information

**AdditionalInfoPackageEventArgs** ([reference](../api/underautomation.universal_robots.primary_interface.md#additionalinfopackageeventargs-robotprimary_interfaceadditional_info))

- `AdditionalInfoPackageEventArgs()`
- `freedrive_button_pressed: bool`: The free drive button is pressed
- `freedrive_button_enabled: bool`: The free drive button is enabled
- `io_enabled_freedrive: bool`: Free drive is enable via IO
- Inherited from [PackageEventArgs](../api/underautomation.universal_robots.common.md#packageeventargs-robotprimary_interfacerobot_mode_data): `receive_date`

### Calibration data

**CalibrationDataPackageEventArgs** ([reference](../api/underautomation.universal_robots.primary_interface.md#calibrationdatapackageeventargs-robotprimary_interfacecalibration_data))

- `CalibrationDataPackageEventArgs()`
- `fx: float`: Fx calibration data
- `fy: float`: Fy calibration data
- `fz: float`: Fz calibration data
- `frx: float`: Frx calibration data
- `fry: float`: Fry calibration data
- `frz: float`: Frz calibration data
- Inherited from [PackageEventArgs](../api/underautomation.universal_robots.common.md#packageeventargs-robotprimary_interfacerobot_mode_data): `receive_date`

### Safety data

**SafetyDataPackageEventArgs** ([reference](../api/underautomation.universal_robots.primary_interface.md#safetydatapackageeventargs-robotprimary_interfacesafety_data))

- `SafetyDataPackageEventArgs()`
- `data: typing.List[int]`: Irrelevant (Internal use only)
- Inherited from [PackageEventArgs](../api/underautomation.universal_robots.common.md#packageeventargs-robotprimary_interfacerobot_mode_data): `receive_date`

### Tool communication information

**ToolCommunicationInfoPackageEventArgs** ([reference](../api/underautomation.universal_robots.primary_interface.md#toolcommunicationinfopackageeventargs-robotprimary_interfacetool_communication_info))

- `ToolCommunicationInfoPackageEventArgs()`
- `tool_communication_is_enabled: bool`: Is the tool communication interface enabled
- `baud_rate: int`: Baud rate for tool serial communication
- `parity: int`: Parity
- `stop_bits: int`: Stop bits
- `rx_idle_chars: float`: RX Idle Chars
- `tx_idle_chars: float`: TX Idle Chars
- Inherited from [PackageEventArgs](../api/underautomation.universal_robots.common.md#packageeventargs-robotprimary_interfacerobot_mode_data): `receive_date`

### Tool mode

**ToolModeInfoPackageEventArgs** ([reference](../api/underautomation.universal_robots.primary_interface.md#toolmodeinfopackageeventargs-robotprimary_interfacetool_mode_info))

- `ToolModeInfoPackageEventArgs()`
- `output_mode: OutputModes`: Digital output mode
- `digital_output_mode0: DigitalOutputConfigurations`: Digital output 0 configuration
- `digital_output_mode1: DigitalOutputConfigurations`: Digital output 1 configuration
- Inherited from [PackageEventArgs](../api/underautomation.universal_robots.common.md#packageeventargs-robotprimary_interfacerobot_mode_data): `receive_date`

**DigitalOutputConfigurations** ([reference](../api/underautomation.universal_robots.common.md#digitaloutputconfigurations-robotprimary_interfacetool_mode_infodigital_output_mode0))

- SinkingNPN: Sinking (NOPN)
- SourcingPNP: Sourcing (PNP)
- PushPull: Push / Pull

**OutputModes** ([reference](../api/underautomation.universal_robots.common.md#outputmodes-robotprimary_interfacetool_mode_infooutput_mode))

- StandardOutput: Standard output
- DualPinPower: Dual Pin Power

## What to read next

- [Send URScript](remote-send-script.md): run URScript from the PC.
- [Read and write variables](variables.md): the program and installation variables.
- [RTDE](rtde.md): the same data, up to 500 Hz.
