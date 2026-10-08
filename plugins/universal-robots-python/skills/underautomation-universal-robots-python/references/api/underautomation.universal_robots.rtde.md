# underautomation.universal_robots.rtde

## IRtdeRegistersValue

`from underautomation.universal_robots.rtde.i_rtde_registers_value import IRtdeRegistersValue`

Interface for accessing individual register values within a register array by index.

- `lower_range_index: int (read only)`: Gets the lower-bound register index for this register range.

## RTDEStates (robot.rtde.state)

`from underautomation.universal_robots.rtde.rtde_states import RTDEStates`

Represents the current state of the RTDE connection lifecycle.

- Disabled: RTDE is not connected.
- Connecting: RTDE connection and recipe setup are in progress.
- Started: RTDE is actively streaming data.
- Paused: RTDE streaming is paused but the connection remains open.

## RtdeBaseValues1

`from underautomation.universal_robots.rtde.rtde_base_values_1 import RtdeBaseValues1`

Generic abstract base class for getting and setting RTDE variable values identified by enum T.

- Inherited from [RtdeBaseValues](underautomation.universal_robots.rtde.md#rtdebasevalues-robotrtdeoutput_data_values): `values`

## RtdeBaseValues (robot.rtde.output_data_values)

`from underautomation.universal_robots.rtde.rtde_base_values import RtdeBaseValues`

Abstract base class holding a collection of RtdeValue instances representing RTDE variable values.

- `values: typing.List[RtdeValue] (read only)`: Gets a copy of all RTDE values held by this instance.

## RtdeBasicRequestEventArgs

`from underautomation.universal_robots.rtde.rtde_basic_request_event_args import RtdeBasicRequestEventArgs`

Event arguments for a basic RTDE request/response exchange indicating whether the request was accepted by the robot controller.

- `RtdeBasicRequestEventArgs()`
- `accepted: bool`: Gets or sets a value indicating whether the request was accepted by the robot.
- Inherited from [PackageEventArgs](underautomation.universal_robots.common.md#packageeventargs-robotprimary_interfacerobot_mode_data): `receive_date`

## RtdeBitRegistersValue (robot.rtde.output_data_values.input_bit_registers)

`from underautomation.universal_robots.rtde.rtde_bit_registers_value import RtdeBitRegistersValue`

RTDE bit register array (64 registers, indices 64–127) for exchanging boolean flags with the robot.

- `x64: bool`: Register n°64
- `x65: bool`: Register n°65
- `x66: bool`: Register n°66
- `x67: bool`: Register n°67
- `x68: bool`: Register n°68
- `x69: bool`: Register n°69
- `x70: bool`: Register n°70
- `x71: bool`: Register n°71
- `x72: bool`: Register n°72
- `x73: bool`: Register n°73
- `x74: bool`: Register n°74
- `x75: bool`: Register n°75
- `x76: bool`: Register n°76
- `x77: bool`: Register n°77
- `x78: bool`: Register n°78
- `x79: bool`: Register n°79
- `x80: bool`: Register n°80
- `x81: bool`: Register n°81
- `x82: bool`: Register n°82
- `x83: bool`: Register n°83
- `x84: bool`: Register n°84
- `x85: bool`: Register n°85
- `x86: bool`: Register n°86
- `x87: bool`: Register n°87
- `x88: bool`: Register n°88
- `x89: bool`: Register n°89
- `x90: bool`: Register n°90
- `x91: bool`: Register n°91
- `x92: bool`: Register n°92
- `x93: bool`: Register n°93
- `x94: bool`: Register n°94
- `x95: bool`: Register n°95
- `x96: bool`: Register n°96
- `x97: bool`: Register n°97
- `x98: bool`: Register n°98
- `x99: bool`: Register n°99
- `x100: bool`: Register n°100
- `x101: bool`: Register n°101
- `x102: bool`: Register n°102
- `x103: bool`: Register n°103
- `x104: bool`: Register n°104
- `x105: bool`: Register n°105
- `x106: bool`: Register n°106
- `x107: bool`: Register n°107
- `x108: bool`: Register n°108
- `x109: bool`: Register n°109
- `x110: bool`: Register n°110
- `x111: bool`: Register n°111
- `x112: bool`: Register n°112
- `x113: bool`: Register n°113
- `x114: bool`: Register n°114
- `x115: bool`: Register n°115
- `x116: bool`: Register n°116
- `x117: bool`: Register n°117
- `x118: bool`: Register n°118
- `x119: bool`: Register n°119
- `x120: bool`: Register n°120
- `x121: bool`: Register n°121
- `x122: bool`: Register n°122
- `x123: bool`: Register n°123
- `x124: bool`: Register n°124
- `x125: bool`: Register n°125
- `x126: bool`: Register n°126
- `x127: bool`: Register n°127
- `lower_range_index: int (read only)`
- `set_value(index: int, value: bool) -> None`: Sets the value at the specified absolute register index.
- `get_value(index: int) -> bool`: Gets the value at the specified absolute register index.
- `value: typing.List[bool] (read only)`: Gets the current strongly-typed value.
- Inherited from [RtdeValue](underautomation.universal_robots.rtde.md#rtdevalue-robotrtdeoutput_data_valuesinput_bit_registers): `value`

## RtdeClient

`from underautomation.universal_robots.rtde.rtde_client import RtdeClient`

Standalone RTDE client for exchanging real-time data with a Universal Robots controller on TCP port 30004.

- `RtdeClient()`
- `connect(ip: str, outputSetup: RtdeOutputSetup, inputSetup: RtdeInputSetup, version: RtdeVersions, frequency: float, port: int=30004) -> None`: Connects to the robot's RTDE interface, sets up the specified input/output recipes, and starts data streaming.
- `static AllOutputsDescription: RtdeOutputsDescription`: Static description of all available RTDE output variables.
- `static AllInputsDescription: RtdeInputsDescription`: Static description of all available RTDE input variables.
- Inherited from [RtdeClientBase](underautomation.universal_robots.rtde.internal.md#rtdeclientbase-robotrtde): `pause`, `resume`, `write_inputs`, `disconnect`, `last_text_message`, `state`, `connected`, `ip`, `applied_frequency`, `version`, `output_setup`, `input_setup`, `output_recipe_id`, `input_recipe_id`, `input_recipe_is_valid`, `measured_frequency`, `output_data_values`, `protocol_version_received`, `text_message_received`, `output_data_received`, `setup_outputs_received`, `setup_inputs_received`, `start_received`, `pause_received`, `package_received`
- Inherited from [URServiceBase](underautomation.universal_robots.internal.md#urservicebase-robot): `internal_error_occured`

## RtdeClientParameters

`from underautomation.universal_robots.rtde.rtde_client_parameters import RtdeClientParameters`

Parameters for configuring the standalone RtdeClient connection to a Universal Robots controller via the RTDE protocol.

- `RtdeClientParameters()`

## RtdeControlPackageSetupInputsEventArgs

`from underautomation.universal_robots.rtde.rtde_control_package_setup_inputs_event_args import RtdeControlPackageSetupInputsEventArgs`

Event arguments raised when the robot acknowledges the RTDE input recipe setup.

- `RtdeControlPackageSetupInputsEventArgs()`
- `input_recipe_id: int`: Recipe Identifier of input sent data
- `variable_types: typing.List[str]`: Status of each registers. Contains the type or the status IN_USE / NOT_FOUND
- `input_recipe_is_valid: bool (read only)`: Indicates that the recipe is valid, i.e. that all the registers have been found and are not already reserved for writing by another RTDE client. Check event SetupInputsReceived to see which registers are NOT_FOUND or IN_USE
- Inherited from [PackageEventArgs](underautomation.universal_robots.common.md#packageeventargs-robotprimary_interfacerobot_mode_data): `receive_date`

## RtdeControlPackageSetupOutputsEventArgs

`from underautomation.universal_robots.rtde.rtde_control_package_setup_outputs_event_args import RtdeControlPackageSetupOutputsEventArgs`

Event arguments raised when the robot acknowledges the RTDE output recipe setup.

- `RtdeControlPackageSetupOutputsEventArgs()`
- `output_recipe_id: int`: Gets or sets the recipe identifier assigned by the robot for output data.
- `variable_types: typing.List[str]`: Gets or sets the status of each subscribed output variable. Each entry contains the RTDE type name, or "IN_USE" / "NOT_FOUND".
- Inherited from [PackageEventArgs](underautomation.universal_robots.common.md#packageeventargs-robotprimary_interfacerobot_mode_data): `receive_date`

## RtdeDataDescription1

`from underautomation.universal_robots.rtde.rtde_data_description_1 import RtdeDataDescription1`

Abstract base class that describes a single RTDE variable, including its name, data type, and array layout.

- `data: T (read only)`: Gets the enum value identifying the RTDE variable.
- `type: RtdeTypes (read only)`: Gets the RTDE wire type of this variable.
- `name: str (read only)`: Gets the protocol name of this variable as defined in the UR RTDE specification.
- `description: str (read only)`: Gets a human-readable description of this variable.
- `lower_index: int (read only)`: Gets the lower bound index when this variable represents an element of a register array; otherwise 0.
- `array_size: int (read only)`: Gets the size of the register array this variable belongs to; otherwise 0.
- `is_array: bool (read only)`: Gets a value indicating whether this variable is an element of a register array.

## RtdeDataPackageEventArgs

`from underautomation.universal_robots.rtde.rtde_data_package_event_args import RtdeDataPackageEventArgs`

Event arguments for an RTDE output data package received from the robot at the subscribed frequency.

- `RtdeDataPackageEventArgs()`
- `output_recipe_id: int`: Gets or sets the recipe identifier for the received output data (RTDE v2 only; 0 for v1).
- `output_data_values: RtdeOutputValues`: Gets or sets the decoded output values contained in this data package.
- `measured_frequency: float`: Gets or sets the measured frequency in Hz, computed from successive Timestamp values.
- Inherited from [PackageEventArgs](underautomation.universal_robots.common.md#packageeventargs-robotprimary_interfacerobot_mode_data): `receive_date`

## RtdeDoubleRegistersValue (robot.rtde.output_data_values.input_double_registers)

`from underautomation.universal_robots.rtde.rtde_double_registers_value import RtdeDoubleRegistersValue`

RTDE double register array (48 registers, indices 0–47) for exchanging 64-bit floating-point values with the robot.

- `x0: float`: Register n°0
- `x1: float`: Register n°1
- `x2: float`: Register n°2
- `x3: float`: Register n°3
- `x4: float`: Register n°4
- `x5: float`: Register n°5
- `x6: float`: Register n°6
- `x7: float`: Register n°7
- `x8: float`: Register n°8
- `x9: float`: Register n°9
- `x10: float`: Register n°10
- `x11: float`: Register n°11
- `x12: float`: Register n°12
- `x13: float`: Register n°13
- `x14: float`: Register n°14
- `x15: float`: Register n°15
- `x16: float`: Register n°16
- `x17: float`: Register n°17
- `x18: float`: Register n°18
- `x19: float`: Register n°19
- `x20: float`: Register n°20
- `x21: float`: Register n°21
- `x22: float`: Register n°22
- `x23: float`: Register n°23
- `x24: float`: Register n°24
- `x25: float`: Register n°25
- `x26: float`: Register n°26
- `x27: float`: Register n°27
- `x28: float`: Register n°28
- `x29: float`: Register n°29
- `x30: float`: Register n°30
- `x31: float`: Register n°31
- `x32: float`: Register n°32
- `x33: float`: Register n°33
- `x34: float`: Register n°34
- `x35: float`: Register n°35
- `x36: float`: Register n°36
- `x37: float`: Register n°37
- `x38: float`: Register n°38
- `x39: float`: Register n°39
- `x40: float`: Register n°40
- `x41: float`: Register n°41
- `x42: float`: Register n°42
- `x43: float`: Register n°43
- `x44: float`: Register n°44
- `x45: float`: Register n°45
- `x46: float`: Register n°46
- `x47: float`: Register n°47
- `lower_range_index: int (read only)`
- `set_value(index: int, value: float) -> None`: Sets the value at the specified absolute register index.
- `get_value(index: int) -> float`: Gets the value at the specified absolute register index.
- `value: typing.List[float] (read only)`: Gets the current strongly-typed value.
- Inherited from [RtdeValue](underautomation.universal_robots.rtde.md#rtdevalue-robotrtdeoutput_data_valuesinput_bit_registers): `value`

## RtdeInputData

`from underautomation.universal_robots.rtde.rtde_input_data import RtdeInputData`

- SpeedSliderMask: 0 = don't change speed slider with this input, 1 = use speed_slider_fraction to set speed slider value
- SpeedSliderFraction: new speed slider value
- StandardDigitalOutputMask: Standard digital output bit mask
- ConfigurableDigitalOutputMask: Configurable digital output bit mask
- StandardDigitalOutput: Standard digital outputs
- ConfigurableDigitalOutput: Configurable digital outputs
- StandardAnalogOutputMask: Standard analog output mask
- StandardAnalogOutputType: Output domain {0=current[mA], 1=voltage[V]}. Bits 0-1: standard_analog_output_0 | standard_analog_output_1
- StandardAnalogOutput0: Standard analog output 0 (ratio) [0..1]
- StandardAnalogOutput1: Standard analog output 1 (ratio) [0..1]
- InputBtRegisters0To31: General purpose bits. This range of the boolean input registers is reserved for FieldBus/PLC interface usage.
- InputBtRegisters32To63: General purpose bits. This range of the boolean input registers is reserved for FieldBus/PLC interface usage.
- InputBitRegisters: 64 general purpose bits. X: [64..127] - The upper range of the boolean input registers can be used by external RTDE clients (i.e URCAPS).
- InputIntRegisters: 48 general purpose integer registers. X: [0..23] - The lower range of the integer input registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the integer input registers can be used by external RTDE clients (i.e URCAPS).
- InputDoubleRegisters: 48 general purpose double registers. X: [0..23] - The lower range of the double input registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the double input registers can be used by external RTDE clients (i.e URCAPS).
- ExternalForceTorque: Input external wrench when using ft_rtde_input_enable builtin.

## RtdeInputDataDescription

`from underautomation.universal_robots.rtde.rtde_input_data_description import RtdeInputDataDescription`

Describes a single RTDE input variable (client-to-robot), including its protocol name, type, and array information.

- `data: RtdeInputData (read only)`: Gets the enum value identifying the RTDE variable.
- `type: RtdeTypes (read only)`: Gets the RTDE wire type of this variable.
- `name: str (read only)`: Gets the protocol name of this variable as defined in the UR RTDE specification.
- `description: str (read only)`: Gets a human-readable description of this variable.
- `lower_index: int (read only)`: Gets the lower bound index when this variable represents an element of a register array; otherwise 0.
- `array_size: int (read only)`: Gets the size of the register array this variable belongs to; otherwise 0.
- `is_array: bool (read only)`: Gets a value indicating whether this variable is an element of a register array.

## RtdeInputSetup

`from underautomation.universal_robots.rtde.rtde_input_setup import RtdeInputSetup`

Defines the set of RTDE input variables (client-to-robot) to subscribe to as a recipe.

- `RtdeInputSetup()`
- `add(data: RtdeInputData) -> RtdeInputSetupItem`: Adds a variable to the recipe with register index 0.
- `add(data: RtdeInputData, index: int=0) -> RtdeInputSetupItem`: Adds a variable to the recipe with the specified register index.
- `remove(data: RtdeInputData, index: int=-1) -> int`: Removes all items matching the specified variable and optionally a specific register index.
- `contains(data: RtdeInputData, index: int=0) -> bool`: Determines whether the recipe contains the specified variable at the given register index.
- `contains(data: RtdeInputData) -> bool`: Determines whether the recipe contains the specified variable at any register index.
- `to_distinct_list() -> typing.List[RtdeInputSetupItem]`: Returns a deduplicated array of setup items, removing duplicates by RtdeSetupItem%601.Data and RtdeSetupItem%601.Index.

## RtdeInputSetupItem

`from underautomation.universal_robots.rtde.rtde_input_setup_item import RtdeInputSetupItem`

Represents a single RTDE input variable (client-to-robot) in an input recipe.

- `RtdeInputSetupItem(data: RtdeInputData, index: int)`: Initializes a new instance for the specified input variable and register index.
- `description: RtdeDataDescription1[RtdeInputData] (read only)`: Gets the description metadata for this input variable.
- `index: int`: Gets or sets the register index for array/register RTDE variables. Defaults to 0.
- `data: RtdeInputData`: Gets or sets the enum value identifying the RTDE variable.
- `name: str (read only)`: Gets the RTDE protocol name for this variable, including the register index suffix for array variables.
- `type: RtdeTypes (read only)`: Gets the RTDE wire type of this variable.
- `protocol_type: str (read only)`: Gets the uppercase RTDE protocol type string sent on the wire during setup.

## RtdeInputValues

`from underautomation.universal_robots.rtde.rtde_input_values import RtdeInputValues`

Holds the current values for all RTDE input variables (client-to-robot). Use this to prepare data before calling write_inputs().

- `RtdeInputValues()`: Initializes a new instance with default values for all input variables.
- `reset() -> None`: Resets all input values to their defaults.
- `speed_slider_mask: int`: 0 = don't change speed slider with this input, 1 = use speed_slider_fraction to set speed slider value
- `speed_slider_fraction: float`: new speed slider value
- `standard_digital_output_mask: int`: Standard digital output bit mask
- `configurable_digital_output_mask: int`: Configurable digital output bit mask
- `standard_digital_output: int`: Standard digital outputs
- `configurable_digital_output: int`: Configurable digital outputs
- `standard_analog_output_mask: int`: Standard analog output mask
- `standard_analog_output_type: int`: Output domain {0=current[mA], 1=voltage[V]}. Bits 0-1: standard_analog_output_0 | standard_analog_output_1
- `standard_analog_output0: float`: Standard analog output 0 (ratio) [0..1]
- `standard_analog_output1: float`: Standard analog output 1 (ratio) [0..1]
- `input_bt_registers0_to31: int`: General purpose bits. This range of the boolean input registers is reserved for FieldBus/PLC interface usage.
- `input_bt_registers32_to63: int`: General purpose bits. This range of the boolean input registers is reserved for FieldBus/PLC interface usage.
- `input_bit_registers: RtdeBitRegistersValue (read only)`: 64 general purpose bits. X: [64..127] - The upper range of the boolean input registers can be used by external RTDE clients (i.e URCAPS).
- `input_int_registers: RtdeIntRegistersValue (read only)`: 48 general purpose integer registers. X: [0..23] - The lower range of the integer input registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the integer input registers can be used by external RTDE clients (i.e URCAPS).
- `input_double_registers: RtdeDoubleRegistersValue (read only)`: 48 general purpose double registers. X: [0..23] - The lower range of the double input registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the double input registers can be used by external RTDE clients (i.e URCAPS).
- `external_force_torque: CartesianCoordinates`: Input external wrench when using ft_rtde_input_enable builtin.
- Inherited from [RtdeBaseValues](underautomation.universal_robots.rtde.md#rtdebasevalues-robotrtdeoutput_data_values): `values`

## RtdeInputsDescription

`from underautomation.universal_robots.rtde.rtde_inputs_description import RtdeInputsDescription`

- `RtdeInputsDescription()`
- `get(data: RtdeInputData) -> RtdeInputDataDescription`
- `items: typing.Any (read only)`
- `speed_slider_mask: RtdeInputDataDescription (read only)`: 0 = don't change speed slider with this input, 1 = use speed_slider_fraction to set speed slider value
- `speed_slider_fraction: RtdeInputDataDescription (read only)`: new speed slider value
- `standard_digital_output_mask: RtdeInputDataDescription (read only)`: Standard digital output bit mask
- `configurable_digital_output_mask: RtdeInputDataDescription (read only)`: Configurable digital output bit mask
- `standard_digital_output: RtdeInputDataDescription (read only)`: Standard digital outputs
- `configurable_digital_output: RtdeInputDataDescription (read only)`: Configurable digital outputs
- `standard_analog_output_mask: RtdeInputDataDescription (read only)`: Standard analog output mask
- `standard_analog_output_type: RtdeInputDataDescription (read only)`: Output domain {0=current[mA], 1=voltage[V]}. Bits 0-1: standard_analog_output_0 | standard_analog_output_1
- `standard_analog_output0: RtdeInputDataDescription (read only)`: Standard analog output 0 (ratio) [0..1]
- `standard_analog_output1: RtdeInputDataDescription (read only)`: Standard analog output 1 (ratio) [0..1]
- `input_bt_registers0_to31: RtdeInputDataDescription (read only)`: General purpose bits. This range of the boolean input registers is reserved for FieldBus/PLC interface usage.
- `input_bt_registers32_to63: RtdeInputDataDescription (read only)`: General purpose bits. This range of the boolean input registers is reserved for FieldBus/PLC interface usage.
- `input_bit_registers: RtdeInputDataDescription (read only)`: 64 general purpose bits. X: [64..127] - The upper range of the boolean input registers can be used by external RTDE clients (i.e URCAPS).
- `input_int_registers: RtdeInputDataDescription (read only)`: 48 general purpose integer registers. X: [0..23] - The lower range of the integer input registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the integer input registers can be used by external RTDE clients (i.e URCAPS).
- `input_double_registers: RtdeInputDataDescription (read only)`: 48 general purpose double registers. X: [0..23] - The lower range of the double input registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the double input registers can be used by external RTDE clients (i.e URCAPS).
- `external_force_torque: RtdeInputDataDescription (read only)`: Input external wrench when using ft_rtde_input_enable builtin.

## RtdeIntRegistersValue (robot.rtde.output_data_values.input_int_registers)

`from underautomation.universal_robots.rtde.rtde_int_registers_value import RtdeIntRegistersValue`

RTDE integer register array (48 registers, indices 0–47) for exchanging 32-bit integer values with the robot.

- `x0: int`: Register n°0
- `x1: int`: Register n°1
- `x2: int`: Register n°2
- `x3: int`: Register n°3
- `x4: int`: Register n°4
- `x5: int`: Register n°5
- `x6: int`: Register n°6
- `x7: int`: Register n°7
- `x8: int`: Register n°8
- `x9: int`: Register n°9
- `x10: int`: Register n°10
- `x11: int`: Register n°11
- `x12: int`: Register n°12
- `x13: int`: Register n°13
- `x14: int`: Register n°14
- `x15: int`: Register n°15
- `x16: int`: Register n°16
- `x17: int`: Register n°17
- `x18: int`: Register n°18
- `x19: int`: Register n°19
- `x20: int`: Register n°20
- `x21: int`: Register n°21
- `x22: int`: Register n°22
- `x23: int`: Register n°23
- `x24: int`: Register n°24
- `x25: int`: Register n°25
- `x26: int`: Register n°26
- `x27: int`: Register n°27
- `x28: int`: Register n°28
- `x29: int`: Register n°29
- `x30: int`: Register n°30
- `x31: int`: Register n°31
- `x32: int`: Register n°32
- `x33: int`: Register n°33
- `x34: int`: Register n°34
- `x35: int`: Register n°35
- `x36: int`: Register n°36
- `x37: int`: Register n°37
- `x38: int`: Register n°38
- `x39: int`: Register n°39
- `x40: int`: Register n°40
- `x41: int`: Register n°41
- `x42: int`: Register n°42
- `x43: int`: Register n°43
- `x44: int`: Register n°44
- `x45: int`: Register n°45
- `x46: int`: Register n°46
- `x47: int`: Register n°47
- `lower_range_index: int (read only)`
- `set_value(index: int, value: int) -> None`: Sets the value at the specified absolute register index.
- `get_value(index: int) -> int`: Gets the value at the specified absolute register index.
- `value: typing.List[int] (read only)`: Gets the current strongly-typed value.
- Inherited from [RtdeValue](underautomation.universal_robots.rtde.md#rtdevalue-robotrtdeoutput_data_valuesinput_bit_registers): `value`

## RtdeOutputData

`from underautomation.universal_robots.rtde.rtde_output_data import RtdeOutputData`

- Timestamp: Time elapsed since the controller was started [s]
- TargetQ: Target joint positions
- TargetQd: Target joint velocities
- TargetQdd: Target joint accelerations
- TargetCurrent: Target joint currents
- TargetMoment: Target joint moments (torques)
- ActualQ: Actual joint positions
- ActualQd: Actual joint velocities
- ActualCurrent: Actual joint currents
- JointControlOutput: Joint control currents
- ActualTcpPose: Actual Cartesian coordinates of the tool: (x,y,z,rx,ry,rz), where rx, ry and rz is a rotation vector representation of the tool orientation
- ActualTcpSpeed: Actual speed of the tool given in Cartesian coordinates. The speed is given in [m/s] and the rotational part of the TCP speed (rx, ry, rz) is the angular velocity given in [rad/s]
- ActualTcpForce: Generalized forces in the TCP. It compensates the measurement for forces and torques generated by the payload
- TargetTcpPose: Target Cartesian coordinates of the tool: (x,y,z,rx,ry,rz), where rx, ry and rz is a rotation vector representation of the tool orientation
- TargetTcpSpeed: Target speed of the tool given in Cartesian coordinates. The speed is given in [m/s] and the rotational part of the TCP speed (rx, ry, rz) is the angular velocity given in [rad/s]
- ActualDigitalInputBits: Current state of the digital inputs. 0-7: Standard, 8-15: Configurable, 16-17: Tool
- JointTemperatures: Temperature of each joint in degrees Celsius
- ActualExecutionTime: Controller real-time thread execution time
- RobotMode: Robot mode
- JointMode: Joint control modes
- SafetyMode: Safety mode
- SafetyStatus: Safety status
- ActualToolAccelerometer: Tool x, y and z accelerometer values
- SpeedScaling: Speed scaling of the trajectory limiter
- TargetSpeedFraction: Target speed fraction
- ActualMomentum: Norm of Cartesian linear momentum
- ActualMainVoltage: Safety Control Board: Main voltage
- ActualRobotVoltage: Safety Control Board: Robot voltage (48V)
- ActualRobotCurrent: Safety Control Board: Robot current
- ActualJointVoltage: Actual joint voltages
- ActualDigitalOutputBits: Current state of the digital outputs. 0-7: Standard, 8-15: Configurable, 16-17: Tool
- RuntimeState: Program state
- ElbowPosition: Position of robot elbow in Cartesian Base Coordinates
- ElbowVelocity: Velocity of robot elbow in Cartesian Base Coordinates
- RobotStatusBits: Bits 0-3:Is power on | Is program running | Is teach button pressed | Is power button pressed
- SafetyStatusBits: Bits 0-10: Is normal mode | Is reduced mode | Is protective stopped | Is recovery mode | Is safeguard stopped | Is system emergency stopped | Is robot emergency stopped | Is emergency stopped | Is violation | Is fault | Is stopped due to safety
- AnalogIOTypes: Bits 0-3: analog input 0 | analog input 1 | analog output 0 | analog output 1, {0=current[mA], 1=voltage[V]}
- StandardAnalogInput0: Standard analog input 0 [mA or V]
- StandardAnalogInput1: Standard analog input 1 [mA or V]
- StandardAnalogOutput0: Standard analog output 0 [mA or V]
- StandardAnalogOutput1: Standard analog output 1 [mA or V]
- IOCurrent: I/O current [mA]
- Euromap67InputBits: Euromap67 input bits
- Euromap67OutputBits: Euromap67 output bits
- Euromap67_24VVoltage: Euromap 24V voltage [V]
- Euromap67_24VCurrent: Euromap 24V current [mA]
- ToolMode: Tool mode
- ToolAnalogInputTypes: Output domain {0=current[mA], 1=voltage[V]} Bits 0-1: tool_analog_input_0 | tool_analog_input_1
- ToolAnalogInput0: Tool analog input 0 [mA or V]
- ToolAnalogInput1: Tool analog input 1 [mA or V]
- ToolOutputVoltage: Tool output voltage [V]
- ToolOutputCurrent: Tool current [mA]
- ToolTemperature: Tool temperature in degrees Celsius
- TcpForceScalar: TCP force scalar [N]
- OutputBitRegisters0To31: General purpose bits
- OutputBitRegisters32To63: General purpose bits
- OutputBitRegisters: 64 general purpose bits. X: [64..127] - The upper range of the boolean output registers can be used by external RTDE clients (i.e URCAPS).
- OutputIntRegisters: 48 general purpose integer registers. X: [0..23] - The lower range of the integer output registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the integer output registers can be used by external RTDE clients (i.e URCAPS).
- OutputDoubleRegisters: 48 general purpose double registers. X: [0..23] - The lower range of the double output registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the double output registers can be used by external RTDE clients (i.e URCAPS).
- InputBitRegisters0To31: General purpose bits (input read back). This range of the boolean output registers is reserved for FieldBus/PLC interface usage.
- InputBitRegisters32To63: General purpose bits (input read back), This range of the boolean output registers is reserved for FieldBus/PLC interface usage.
- InputBitRegisters: 64 general purpose bits, X: [64..127] - The upper range of the boolean output registers can be used by external RTDE clients (i.e URCAPS).
- InputIntRegisters: 48 general purpose integer registers. X: [0..23] - The lower range of the integer input registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the integer input registers can be used by external RTDE clients (i.e URCAPS).
- InputDoubleRegisters: 48 general purpose double registers. X: [0..23] - The lower range of the double input registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the double input registers can be used by external RTDE clients (i.e URCAPS).
- ToolOutputMode: The current output mode
- ToolDigitalOutput0mode: The current mode of digital output 0
- ToolDigitalOutput1Mode: The current mode of digital output 1
- Payload: Payload mass Kg
- PayloadCOG: Payload Center of Gravity (CoGx, CoGy, CoGz) m
- PayloadInertia: Payload inertia matrix elements (Ixx,Iyy,Izz,Ixy,Ixz,Iyz] expressed in kg*m^2
- ScriptControlLine: Script line number that is actually in control of the robot given the robot is locked by one of the threads in the script. If no thread is locking the robot this field is set to '0'. Script line number should not be confused with program tree line number displayed on polyscope.
- FTRawWrench: Raw force and torque measurement, not compensated for forces and torques caused by the payload

## RtdeOutputDataDescription

`from underautomation.universal_robots.rtde.rtde_output_data_description import RtdeOutputDataDescription`

Describes a single RTDE output variable (robot-to-client), including its protocol name, type, and array information.

- `data: RtdeOutputData (read only)`: Gets the enum value identifying the RTDE variable.
- `type: RtdeTypes (read only)`: Gets the RTDE wire type of this variable.
- `name: str (read only)`: Gets the protocol name of this variable as defined in the UR RTDE specification.
- `description: str (read only)`: Gets a human-readable description of this variable.
- `lower_index: int (read only)`: Gets the lower bound index when this variable represents an element of a register array; otherwise 0.
- `array_size: int (read only)`: Gets the size of the register array this variable belongs to; otherwise 0.
- `is_array: bool (read only)`: Gets a value indicating whether this variable is an element of a register array.

## RtdeOutputSetup

`from underautomation.universal_robots.rtde.rtde_output_setup import RtdeOutputSetup`

Defines the set of RTDE output variables (robot-to-client) to subscribe to as a recipe. The Timestamp variable is added by default.

- `RtdeOutputSetup()`: Initializes a new instance with the default Timestamp variable.
- `add(data: RtdeOutputData) -> RtdeOutputSetupItem`: Adds a variable to the recipe with register index 0.
- `add(data: RtdeOutputData, index: int=0) -> RtdeOutputSetupItem`: Adds a variable to the recipe with the specified register index.
- `remove(data: RtdeOutputData, index: int=-1) -> int`: Removes all items matching the specified variable and optionally a specific register index.
- `contains(data: RtdeOutputData, index: int=0) -> bool`: Determines whether the recipe contains the specified variable at the given register index.
- `contains(data: RtdeOutputData) -> bool`: Determines whether the recipe contains the specified variable at any register index.
- `to_distinct_list() -> typing.List[RtdeOutputSetupItem]`: Returns a deduplicated array of setup items, removing duplicates by RtdeSetupItem%601.Data and RtdeSetupItem%601.Index.

## RtdeOutputSetupItem

`from underautomation.universal_robots.rtde.rtde_output_setup_item import RtdeOutputSetupItem`

Represents a single RTDE output variable (robot-to-client) in an output recipe.

- `RtdeOutputSetupItem(data: RtdeOutputData, index: int)`: Initializes a new instance for the specified output variable and register index.
- `description: RtdeDataDescription1[RtdeOutputData] (read only)`: Gets the description metadata for this output variable.
- `index: int`: Gets or sets the register index for array/register RTDE variables. Defaults to 0.
- `data: RtdeOutputData`: Gets or sets the enum value identifying the RTDE variable.
- `name: str (read only)`: Gets the RTDE protocol name for this variable, including the register index suffix for array variables.
- `type: RtdeTypes (read only)`: Gets the RTDE wire type of this variable.
- `protocol_type: str (read only)`: Gets the uppercase RTDE protocol type string sent on the wire during setup.

## RtdeOutputValues (robot.rtde.output_data_values)

`from underautomation.universal_robots.rtde.rtde_output_values import RtdeOutputValues`

Holds the current values for all RTDE output variables (robot-to-client). Updated automatically when data is received from the robot.

- `timestamp: float`: Time elapsed since the controller was started [s]
- `target_q: JointsDoubleValues`: Target joint positions
- `target_qd: JointsDoubleValues`: Target joint velocities
- `target_qdd: JointsDoubleValues`: Target joint accelerations
- `target_current: JointsDoubleValues`: Target joint currents
- `target_moment: JointsDoubleValues`: Target joint moments (torques)
- `actual_q: JointsDoubleValues`: Actual joint positions
- `actual_qd: JointsDoubleValues`: Actual joint velocities
- `actual_current: JointsDoubleValues`: Actual joint currents
- `joint_control_output: JointsDoubleValues`: Joint control currents
- `actual_tcp_pose: Pose`: Actual Cartesian coordinates of the tool: (x,y,z,rx,ry,rz), where rx, ry and rz is a rotation vector representation of the tool orientation
- `actual_tcp_speed: Pose`: Actual speed of the tool given in Cartesian coordinates. The speed is given in [m/s] and the rotational part of the TCP speed (rx, ry, rz) is the angular velocity given in [rad/s]
- `actual_tcp_force: CartesianCoordinates`: Generalized forces in the TCP. It compensates the measurement for forces and torques generated by the payload
- `target_tcp_pose: Pose`: Target Cartesian coordinates of the tool: (x,y,z,rx,ry,rz), where rx, ry and rz is a rotation vector representation of the tool orientation
- `target_tcp_speed: Pose`: Target speed of the tool given in Cartesian coordinates. The speed is given in [m/s] and the rotational part of the TCP speed (rx, ry, rz) is the angular velocity given in [rad/s]
- `actual_digital_input_bits: int`: Current state of the digital inputs. 0-7: Standard, 8-15: Configurable, 16-17: Tool
- `joint_temperatures: JointsDoubleValues`: Temperature of each joint in degrees Celsius
- `actual_execution_time: float`: Controller real-time thread execution time
- `robot_mode: int`: Robot mode
- `joint_mode: JointsIntValues`: Joint control modes
- `safety_mode: int`: Safety mode
- `safety_status: int`: Safety status
- `actual_tool_accelerometer: Vector3D`: Tool x, y and z accelerometer values
- `speed_scaling: float`: Speed scaling of the trajectory limiter
- `target_speed_fraction: float`: Target speed fraction
- `actual_momentum: float`: Norm of Cartesian linear momentum
- `actual_main_voltage: float`: Safety Control Board: Main voltage
- `actual_robot_voltage: float`: Safety Control Board: Robot voltage (48V)
- `actual_robot_current: float`: Safety Control Board: Robot current
- `actual_joint_voltage: JointsDoubleValues`: Actual joint voltages
- `actual_digital_output_bits: int`: Current state of the digital outputs. 0-7: Standard, 8-15: Configurable, 16-17: Tool
- `runtime_state: int`: Program state
- `elbow_position: Vector3D`: Position of robot elbow in Cartesian Base Coordinates
- `elbow_velocity: Vector3D`: Velocity of robot elbow in Cartesian Base Coordinates
- `robot_status_bits: int`: Bits 0-3:Is power on | Is program running | Is teach button pressed | Is power button pressed
- `safety_status_bits: int`: Bits 0-10: Is normal mode | Is reduced mode | Is protective stopped | Is recovery mode | Is safeguard stopped | Is system emergency stopped | Is robot emergency stopped | Is emergency stopped | Is violation | Is fault | Is stopped due to safety
- `analog_io_types: int`: Bits 0-3: analog input 0 | analog input 1 | analog output 0 | analog output 1, {0=current[mA], 1=voltage[V]}
- `standard_analog_input0: float`: Standard analog input 0 [mA or V]
- `standard_analog_input1: float`: Standard analog input 1 [mA or V]
- `standard_analog_output0: float`: Standard analog output 0 [mA or V]
- `standard_analog_output1: float`: Standard analog output 1 [mA or V]
- `io_current: float`: I/O current [mA]
- `euromap67_input_bits: int`: Euromap67 input bits
- `euromap67_output_bits: int`: Euromap67 output bits
- `euromap67_24_v_voltage: float`: Euromap 24V voltage [V]
- `euromap67_24_v_current: float`: Euromap 24V current [mA]
- `tool_mode: int`: Tool mode
- `tool_analog_input_types: int`: Output domain {0=current[mA], 1=voltage[V]} Bits 0-1: tool_analog_input_0 | tool_analog_input_1
- `tool_analog_input0: float`: Tool analog input 0 [mA or V]
- `tool_analog_input1: float`: Tool analog input 1 [mA or V]
- `tool_output_voltage: int`: Tool output voltage [V]
- `tool_output_current: float`: Tool current [mA]
- `tool_temperature: float`: Tool temperature in degrees Celsius
- `tcp_force_scalar: float`: TCP force scalar [N]
- `output_bit_registers0_to31: int`: General purpose bits
- `output_bit_registers32_to63: int`: General purpose bits
- `output_bit_registers: RtdeBitRegistersValue (read only)`: 64 general purpose bits. X: [64..127] - The upper range of the boolean output registers can be used by external RTDE clients (i.e URCAPS).
- `output_int_registers: RtdeIntRegistersValue (read only)`: 48 general purpose integer registers. X: [0..23] - The lower range of the integer output registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the integer output registers can be used by external RTDE clients (i.e URCAPS).
- `output_double_registers: RtdeDoubleRegistersValue (read only)`: 48 general purpose double registers. X: [0..23] - The lower range of the double output registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the double output registers can be used by external RTDE clients (i.e URCAPS).
- `input_bit_registers0_to31: int`: General purpose bits (input read back). This range of the boolean output registers is reserved for FieldBus/PLC interface usage.
- `input_bit_registers32_to63: int`: General purpose bits (input read back), This range of the boolean output registers is reserved for FieldBus/PLC interface usage.
- `input_bit_registers: RtdeBitRegistersValue (read only)`: 64 general purpose bits, X: [64..127] - The upper range of the boolean output registers can be used by external RTDE clients (i.e URCAPS).
- `input_int_registers: RtdeIntRegistersValue (read only)`: 48 general purpose integer registers. X: [0..23] - The lower range of the integer input registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the integer input registers can be used by external RTDE clients (i.e URCAPS).
- `input_double_registers: RtdeDoubleRegistersValue (read only)`: 48 general purpose double registers. X: [0..23] - The lower range of the double input registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the double input registers can be used by external RTDE clients (i.e URCAPS).
- `tool_output_mode: int`: The current output mode
- `tool_digital_output0mode: int`: The current mode of digital output 0
- `tool_digital_output1_mode: int`: The current mode of digital output 1
- `payload: float`: Payload mass Kg
- `payload_cog: Vector3D`: Payload Center of Gravity (CoGx, CoGy, CoGz) m
- `payload_inertia: CartesianCoordinates`: Payload inertia matrix elements (Ixx,Iyy,Izz,Ixy,Ixz,Iyz] expressed in kg*m^2
- `script_control_line: int`: Script line number that is actually in control of the robot given the robot is locked by one of the threads in the script. If no thread is locking the robot this field is set to '0'. Script line number should not be confused with program tree line number displayed on polyscope.
- `ft_raw_wrench: CartesianCoordinates`: Raw force and torque measurement, not compensated for forces and torques caused by the payload
- Inherited from [RtdeBaseValues](underautomation.universal_robots.rtde.md#rtdebasevalues-robotrtdeoutput_data_values): `values`

## RtdeOutputsDescription

`from underautomation.universal_robots.rtde.rtde_outputs_description import RtdeOutputsDescription`

- `RtdeOutputsDescription()`
- `get(data: RtdeOutputData) -> RtdeOutputDataDescription`
- `items: typing.Any (read only)`
- `timestamp: RtdeOutputDataDescription (read only)`: Time elapsed since the controller was started [s]
- `target_q: RtdeOutputDataDescription (read only)`: Target joint positions
- `target_qd: RtdeOutputDataDescription (read only)`: Target joint velocities
- `target_qdd: RtdeOutputDataDescription (read only)`: Target joint accelerations
- `target_current: RtdeOutputDataDescription (read only)`: Target joint currents
- `target_moment: RtdeOutputDataDescription (read only)`: Target joint moments (torques)
- `actual_q: RtdeOutputDataDescription (read only)`: Actual joint positions
- `actual_qd: RtdeOutputDataDescription (read only)`: Actual joint velocities
- `actual_current: RtdeOutputDataDescription (read only)`: Actual joint currents
- `joint_control_output: RtdeOutputDataDescription (read only)`: Joint control currents
- `actual_tcp_pose: RtdeOutputDataDescription (read only)`: Actual Cartesian coordinates of the tool: (x,y,z,rx,ry,rz), where rx, ry and rz is a rotation vector representation of the tool orientation
- `actual_tcp_speed: RtdeOutputDataDescription (read only)`: Actual speed of the tool given in Cartesian coordinates. The speed is given in [m/s] and the rotational part of the TCP speed (rx, ry, rz) is the angular velocity given in [rad/s]
- `actual_tcp_force: RtdeOutputDataDescription (read only)`: Generalized forces in the TCP. It compensates the measurement for forces and torques generated by the payload
- `target_tcp_pose: RtdeOutputDataDescription (read only)`: Target Cartesian coordinates of the tool: (x,y,z,rx,ry,rz), where rx, ry and rz is a rotation vector representation of the tool orientation
- `target_tcp_speed: RtdeOutputDataDescription (read only)`: Target speed of the tool given in Cartesian coordinates. The speed is given in [m/s] and the rotational part of the TCP speed (rx, ry, rz) is the angular velocity given in [rad/s]
- `actual_digital_input_bits: RtdeOutputDataDescription (read only)`: Current state of the digital inputs. 0-7: Standard, 8-15: Configurable, 16-17: Tool
- `joint_temperatures: RtdeOutputDataDescription (read only)`: Temperature of each joint in degrees Celsius
- `actual_execution_time: RtdeOutputDataDescription (read only)`: Controller real-time thread execution time
- `robot_mode: RtdeOutputDataDescription (read only)`: Robot mode
- `joint_mode: RtdeOutputDataDescription (read only)`: Joint control modes
- `safety_mode: RtdeOutputDataDescription (read only)`: Safety mode
- `safety_status: RtdeOutputDataDescription (read only)`: Safety status
- `actual_tool_accelerometer: RtdeOutputDataDescription (read only)`: Tool x, y and z accelerometer values
- `speed_scaling: RtdeOutputDataDescription (read only)`: Speed scaling of the trajectory limiter
- `target_speed_fraction: RtdeOutputDataDescription (read only)`: Target speed fraction
- `actual_momentum: RtdeOutputDataDescription (read only)`: Norm of Cartesian linear momentum
- `actual_main_voltage: RtdeOutputDataDescription (read only)`: Safety Control Board: Main voltage
- `actual_robot_voltage: RtdeOutputDataDescription (read only)`: Safety Control Board: Robot voltage (48V)
- `actual_robot_current: RtdeOutputDataDescription (read only)`: Safety Control Board: Robot current
- `actual_joint_voltage: RtdeOutputDataDescription (read only)`: Actual joint voltages
- `actual_digital_output_bits: RtdeOutputDataDescription (read only)`: Current state of the digital outputs. 0-7: Standard, 8-15: Configurable, 16-17: Tool
- `runtime_state: RtdeOutputDataDescription (read only)`: Program state
- `elbow_position: RtdeOutputDataDescription (read only)`: Position of robot elbow in Cartesian Base Coordinates
- `elbow_velocity: RtdeOutputDataDescription (read only)`: Velocity of robot elbow in Cartesian Base Coordinates
- `robot_status_bits: RtdeOutputDataDescription (read only)`: Bits 0-3:Is power on | Is program running | Is teach button pressed | Is power button pressed
- `safety_status_bits: RtdeOutputDataDescription (read only)`: Bits 0-10: Is normal mode | Is reduced mode | Is protective stopped | Is recovery mode | Is safeguard stopped | Is system emergency stopped | Is robot emergency stopped | Is emergency stopped | Is violation | Is fault | Is stopped due to safety
- `analog_io_types: RtdeOutputDataDescription (read only)`: Bits 0-3: analog input 0 | analog input 1 | analog output 0 | analog output 1, {0=current[mA], 1=voltage[V]}
- `standard_analog_input0: RtdeOutputDataDescription (read only)`: Standard analog input 0 [mA or V]
- `standard_analog_input1: RtdeOutputDataDescription (read only)`: Standard analog input 1 [mA or V]
- `standard_analog_output0: RtdeOutputDataDescription (read only)`: Standard analog output 0 [mA or V]
- `standard_analog_output1: RtdeOutputDataDescription (read only)`: Standard analog output 1 [mA or V]
- `io_current: RtdeOutputDataDescription (read only)`: I/O current [mA]
- `euromap67_input_bits: RtdeOutputDataDescription (read only)`: Euromap67 input bits
- `euromap67_output_bits: RtdeOutputDataDescription (read only)`: Euromap67 output bits
- `euromap67_24_v_voltage: RtdeOutputDataDescription (read only)`: Euromap 24V voltage [V]
- `euromap67_24_v_current: RtdeOutputDataDescription (read only)`: Euromap 24V current [mA]
- `tool_mode: RtdeOutputDataDescription (read only)`: Tool mode
- `tool_analog_input_types: RtdeOutputDataDescription (read only)`: Output domain {0=current[mA], 1=voltage[V]} Bits 0-1: tool_analog_input_0 | tool_analog_input_1
- `tool_analog_input0: RtdeOutputDataDescription (read only)`: Tool analog input 0 [mA or V]
- `tool_analog_input1: RtdeOutputDataDescription (read only)`: Tool analog input 1 [mA or V]
- `tool_output_voltage: RtdeOutputDataDescription (read only)`: Tool output voltage [V]
- `tool_output_current: RtdeOutputDataDescription (read only)`: Tool current [mA]
- `tool_temperature: RtdeOutputDataDescription (read only)`: Tool temperature in degrees Celsius
- `tcp_force_scalar: RtdeOutputDataDescription (read only)`: TCP force scalar [N]
- `output_bit_registers0_to31: RtdeOutputDataDescription (read only)`: General purpose bits
- `output_bit_registers32_to63: RtdeOutputDataDescription (read only)`: General purpose bits
- `output_bit_registers: RtdeOutputDataDescription (read only)`: 64 general purpose bits. X: [64..127] - The upper range of the boolean output registers can be used by external RTDE clients (i.e URCAPS).
- `output_int_registers: RtdeOutputDataDescription (read only)`: 48 general purpose integer registers. X: [0..23] - The lower range of the integer output registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the integer output registers can be used by external RTDE clients (i.e URCAPS).
- `output_double_registers: RtdeOutputDataDescription (read only)`: 48 general purpose double registers. X: [0..23] - The lower range of the double output registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the double output registers can be used by external RTDE clients (i.e URCAPS).
- `input_bit_registers0_to31: RtdeOutputDataDescription (read only)`: General purpose bits (input read back). This range of the boolean output registers is reserved for FieldBus/PLC interface usage.
- `input_bit_registers32_to63: RtdeOutputDataDescription (read only)`: General purpose bits (input read back), This range of the boolean output registers is reserved for FieldBus/PLC interface usage.
- `input_bit_registers: RtdeOutputDataDescription (read only)`: 64 general purpose bits, X: [64..127] - The upper range of the boolean output registers can be used by external RTDE clients (i.e URCAPS).
- `input_int_registers: RtdeOutputDataDescription (read only)`: 48 general purpose integer registers. X: [0..23] - The lower range of the integer input registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the integer input registers can be used by external RTDE clients (i.e URCAPS).
- `input_double_registers: RtdeOutputDataDescription (read only)`: 48 general purpose double registers. X: [0..23] - The lower range of the double input registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the double input registers can be used by external RTDE clients (i.e URCAPS).
- `tool_output_mode: RtdeOutputDataDescription (read only)`: The current output mode
- `tool_digital_output0mode: RtdeOutputDataDescription (read only)`: The current mode of digital output 0
- `tool_digital_output1_mode: RtdeOutputDataDescription (read only)`: The current mode of digital output 1
- `payload: RtdeOutputDataDescription (read only)`: Payload mass Kg
- `payload_cog: RtdeOutputDataDescription (read only)`: Payload Center of Gravity (CoGx, CoGy, CoGz) m
- `payload_inertia: RtdeOutputDataDescription (read only)`: Payload inertia matrix elements (Ixx,Iyy,Izz,Ixy,Ixz,Iyz] expressed in kg*m^2
- `script_control_line: RtdeOutputDataDescription (read only)`: Script line number that is actually in control of the robot given the robot is locked by one of the threads in the script. If no thread is locking the robot this field is set to '0'. Script line number should not be confused with program tree line number displayed on polyscope.
- `ft_raw_wrench: RtdeOutputDataDescription (read only)`: Raw force and torque measurement, not compensated for forces and torques caused by the payload

## RtdeProtocolVersionEventArgs

`from underautomation.universal_robots.rtde.rtde_protocol_version_event_args import RtdeProtocolVersionEventArgs`

Event arguments indicating which RTDE protocol version was negotiated with the robot.

- `RtdeProtocolVersionEventArgs()`
- `version: RtdeVersions`: Gets or sets the negotiated RTDE protocol version.
- Inherited from [RtdeBasicRequestEventArgs](underautomation.universal_robots.rtde.md#rtdebasicrequesteventargs): `accepted`
- Inherited from [PackageEventArgs](underautomation.universal_robots.common.md#packageeventargs-robotprimary_interfacerobot_mode_data): `receive_date`

## RtdeRegistersValue1

`from underautomation.universal_robots.rtde.rtde_registers_value_1 import RtdeRegistersValue1`

Abstract base for a fixed-size register array of type T exchanged through RTDE.

- `set_value(index: int, value: T) -> None`: Sets the value at the specified absolute register index.
- `get_value(index: int) -> T`: Gets the value at the specified absolute register index.
- `lower_range_index: int (read only)`: Gets the lower-bound register index for this register range.
- `value: typing.List[T] (read only)`: Gets the current strongly-typed value.
- Inherited from [RtdeValue](underautomation.universal_robots.rtde.md#rtdevalue-robotrtdeoutput_data_valuesinput_bit_registers): `value`

## RtdeTextMessageEventArgs (robot.rtde.last_text_message)

`from underautomation.universal_robots.rtde.rtde_text_message_event_args import RtdeTextMessageEventArgs`

Event arguments for a text message received from the robot via the RTDE interface.

- `RtdeTextMessageEventArgs()`
- `message: str`: Gets or sets the text content of the message.
- `source: str`: Gets or sets the source module that generated the message on the robot.
- `warning_level: int`: Gets or sets the warning level of the message (0 = exception/error, 1 = warning, 2 = info).
- Inherited from [PackageEventArgs](underautomation.universal_robots.common.md#packageeventargs-robotprimary_interfacerobot_mode_data): `receive_date`

## RtdeTypes

`from underautomation.universal_robots.rtde.rtde_types import RtdeTypes`

RTDE data types used to describe the wire format of each RTDE variable.

- Bool: Boolean value (1 byte on the wire).
- Uint8: Unsigned 8-bit integer.
- Uint32: Unsigned 32-bit integer.
- Int32: Signed 32-bit integer.
- Uint64: Unsigned 64-bit integer.
- Double: 64-bit floating-point number.
- Vector3D: 3-element double vector (X, Y, Z).
- Pose: 6-element double vector representing a TCP pose (X, Y, Z, Rx, Ry, Rz).
- CartesianCoordinates: 6-element double vector representing Cartesian coordinates.
- JointsDoubleValues: 6-element double vector with one value per robot joint.
- JointsIntValues: 6-element 32-bit integer vector with one value per robot joint.
- BoolArray: Boolean value stored as part of a register array.
- Int32Array: 32-bit integer value stored as part of a register array.
- DoubleArray: 64-bit double value stored as part of a register array.

## RtdeValue1

`from underautomation.universal_robots.rtde.rtde_value_1 import RtdeValue1`

Strongly-typed RTDE variable value of type T.

- `value: T (read only)`: Gets the current strongly-typed value.

## RtdeValue (robot.rtde.output_data_values.input_bit_registers)

`from underautomation.universal_robots.rtde.rtde_value import RtdeValue`

Abstract base class for a single RTDE variable value exchanged between the client and the robot.

- `value: typing.Any (read only)`: Gets or sets the current value as an untyped object.

## RtdeVersions (robot.rtde.version)

`from underautomation.universal_robots.rtde.rtde_versions import RtdeVersions`

RTDE version numbers

- V1: Rtde version 1
- V2: Rtde version 2
