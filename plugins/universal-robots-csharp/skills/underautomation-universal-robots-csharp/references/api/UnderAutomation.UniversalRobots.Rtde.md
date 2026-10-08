# UnderAutomation.UniversalRobots.Rtde

## IRtdeRegistersValue

`interface IRtdeRegistersValue`

Interface for accessing individual register values within a register array by index.

- `object GetValue(int index)`: Gets the value at the specified register index.
- `int LowerRangeIndex { get; }`: Gets the lower-bound register index for this register range.
- `void SetValue(int index, object value)`: Sets the value at the specified register index.

## RTDEStates (robot.Rtde.State)

`enum RTDEStates`

Represents the current state of the RTDE connection lifecycle.

- Connecting: RTDE connection and recipe setup are in progress.
- Disabled: RTDE is not connected.
- Paused: RTDE streaming is paused but the connection remains open.
- Started: RTDE is actively streaming data.

## RtdeBaseValues<T>

`abstract class RtdeBaseValues<T> : RtdeBaseValues where T : Enum`

Generic abstract base class for getting and setting RTDE variable values identified by enum T.

- `object GetValue(T data)`: Gets the current value of the specified RTDE variable.
- `object GetValue(T data, int index)`: Gets the current value of the specified RTDE variable at a given register index.
- Inherited from [RtdeBaseValues](UnderAutomation.UniversalRobots.Rtde.md#rtdebasevalues-robotrtdeoutputdatavalues): `Values`

## RtdeBaseValues (robot.Rtde.OutputDataValues)

`abstract class RtdeBaseValues`

Abstract base class holding a collection of Rtde.RtdeValue instances representing RTDE variable values.

- `RtdeValue[] Values { get; }`: Gets a copy of all RTDE values held by this instance.

## RtdeBasicRequestEventArgs

`class RtdeBasicRequestEventArgs : PackageEventArgs`

Event arguments for a basic RTDE request/response exchange indicating whether the request was accepted by the robot controller.

- `RtdeBasicRequestEventArgs()`
- `bool Accepted { get; set; }`: Gets or sets a value indicating whether the request was accepted by the robot.
- Inherited from [PackageEventArgs](UnderAutomation.UniversalRobots.Common.md#packageeventargs-robotprimaryinterfacerobotmodedata): `ReceiveDate`

## RtdeBitRegistersValue (robot.Rtde.OutputDataValues.InputBitRegisters)

`class RtdeBitRegistersValue : RtdeRegistersValue<bool>, IRtdeRegistersValue`

RTDE bit register array (64 registers, indices 64–127) for exchanging boolean flags with the robot.

- `int LowerRangeIndex { get; }`: Gets the lower-bound register index for this register range.
- `bool X100 { get; set; }`: Register n°100
- `bool X101 { get; set; }`: Register n°101
- `bool X102 { get; set; }`: Register n°102
- `bool X103 { get; set; }`: Register n°103
- `bool X104 { get; set; }`: Register n°104
- `bool X105 { get; set; }`: Register n°105
- `bool X106 { get; set; }`: Register n°106
- `bool X107 { get; set; }`: Register n°107
- `bool X108 { get; set; }`: Register n°108
- `bool X109 { get; set; }`: Register n°109
- `bool X110 { get; set; }`: Register n°110
- `bool X111 { get; set; }`: Register n°111
- `bool X112 { get; set; }`: Register n°112
- `bool X113 { get; set; }`: Register n°113
- `bool X114 { get; set; }`: Register n°114
- `bool X115 { get; set; }`: Register n°115
- `bool X116 { get; set; }`: Register n°116
- `bool X117 { get; set; }`: Register n°117
- `bool X118 { get; set; }`: Register n°118
- `bool X119 { get; set; }`: Register n°119
- `bool X120 { get; set; }`: Register n°120
- `bool X121 { get; set; }`: Register n°121
- `bool X122 { get; set; }`: Register n°122
- `bool X123 { get; set; }`: Register n°123
- `bool X124 { get; set; }`: Register n°124
- `bool X125 { get; set; }`: Register n°125
- `bool X126 { get; set; }`: Register n°126
- `bool X127 { get; set; }`: Register n°127
- `bool X64 { get; set; }`: Register n°64
- `bool X65 { get; set; }`: Register n°65
- `bool X66 { get; set; }`: Register n°66
- `bool X67 { get; set; }`: Register n°67
- `bool X68 { get; set; }`: Register n°68
- `bool X69 { get; set; }`: Register n°69
- `bool X70 { get; set; }`: Register n°70
- `bool X71 { get; set; }`: Register n°71
- `bool X72 { get; set; }`: Register n°72
- `bool X73 { get; set; }`: Register n°73
- `bool X74 { get; set; }`: Register n°74
- `bool X75 { get; set; }`: Register n°75
- `bool X76 { get; set; }`: Register n°76
- `bool X77 { get; set; }`: Register n°77
- `bool X78 { get; set; }`: Register n°78
- `bool X79 { get; set; }`: Register n°79
- `bool X80 { get; set; }`: Register n°80
- `bool X81 { get; set; }`: Register n°81
- `bool X82 { get; set; }`: Register n°82
- `bool X83 { get; set; }`: Register n°83
- `bool X84 { get; set; }`: Register n°84
- `bool X85 { get; set; }`: Register n°85
- `bool X86 { get; set; }`: Register n°86
- `bool X87 { get; set; }`: Register n°87
- `bool X88 { get; set; }`: Register n°88
- `bool X89 { get; set; }`: Register n°89
- `bool X90 { get; set; }`: Register n°90
- `bool X91 { get; set; }`: Register n°91
- `bool X92 { get; set; }`: Register n°92
- `bool X93 { get; set; }`: Register n°93
- `bool X94 { get; set; }`: Register n°94
- `bool X95 { get; set; }`: Register n°95
- `bool X96 { get; set; }`: Register n°96
- `bool X97 { get; set; }`: Register n°97
- `bool X98 { get; set; }`: Register n°98
- `bool X99 { get; set; }`: Register n°99
- `void SetValue(int index, bool value)`: Sets the value at the specified absolute register index.
- `bool GetValue(int index)`: Gets the value at the specified absolute register index.
- `bool[] Value { get; }`: Gets the current strongly-typed value.
- Inherited from [RtdeValue](UnderAutomation.UniversalRobots.Rtde.md#rtdevalue-robotrtdeoutputdatavaluesinputbitregisters): `Value`

## RtdeClient

`class RtdeClient : RtdeClientBase`

Standalone RTDE client for exchanging real-time data with a Universal Robots controller on TCP port 30004.

- `RtdeClient()`
- `static readonly RtdeInputsDescription AllInputsDescription`: Static description of all available RTDE input variables.
- `static readonly RtdeOutputsDescription AllOutputsDescription`: Static description of all available RTDE output variables.
- `void Connect(string ip, RtdeOutputSetup outputSetup, RtdeInputSetup inputSetup, RtdeVersions version, double frequency, int port = 30004)`: Connects to the robot's RTDE interface, sets up the specified input/output recipes, and starts data streaming.
- Inherited from [RtdeClientBase](UnderAutomation.UniversalRobots.Rtde.Internal.md#rtdeclientbase-robotrtde): `Pause`, `Resume`, `WriteInputs`, `Disconnect`, `LastTextMessage`, `State`, `Connected`, `IP`, `AppliedFrequency`, `Version`, `OutputSetup`, `InputSetup`, `OutputRecipeId`, `InputRecipeId`, `InputRecipeIsValid`, `MeasuredFrequency`, `OutputDataValues`, `ProtocolVersionReceived`, `TextMessageReceived`, `OutputDataReceived`, `SetupOutputsReceived`, `SetupInputsReceived`, `StartReceived`, `PauseReceived`, `PackageReceived`
- Inherited from [URServiceBase](UnderAutomation.UniversalRobots.Internal.md#urservicebase-robot): `InternalErrorOccured`

## RtdeClientParameters

`class RtdeClientParameters`

Parameters for configuring the standalone Rtde.RtdeClient connection to a Universal Robots controller via the RTDE protocol.

- `RtdeClientParameters()`

## RtdeControlPackageSetupInputsEventArgs

`class RtdeControlPackageSetupInputsEventArgs : PackageEventArgs`

Event arguments raised when the robot acknowledges the RTDE input recipe setup.

- `RtdeControlPackageSetupInputsEventArgs()`
- `byte InputRecipeId { get; set; }`: Recipe Identifier of input sent data
- `bool InputRecipeIsValid { get; }`: Indicates that the recipe is valid, i.e. that all the registers have been found and are not already reserved for writing by another RTDE client. Check event SetupInputsReceived to see which registers are NOT_FOUND or IN_USE
- `string[] VariableTypes { get; set; }`: Status of each registers. Contains the type or the status IN_USE / NOT_FOUND
- Inherited from [PackageEventArgs](UnderAutomation.UniversalRobots.Common.md#packageeventargs-robotprimaryinterfacerobotmodedata): `ReceiveDate`

## RtdeControlPackageSetupOutputsEventArgs

`class RtdeControlPackageSetupOutputsEventArgs : PackageEventArgs`

Event arguments raised when the robot acknowledges the RTDE output recipe setup.

- `RtdeControlPackageSetupOutputsEventArgs()`
- `byte OutputRecipeId { get; set; }`: Gets or sets the recipe identifier assigned by the robot for output data.
- `string[] VariableTypes { get; set; }`: Gets or sets the status of each subscribed output variable. Each entry contains the RTDE type name, or "IN_USE" / "NOT_FOUND".
- Inherited from [PackageEventArgs](UnderAutomation.UniversalRobots.Common.md#packageeventargs-robotprimaryinterfacerobotmodedata): `ReceiveDate`

## RtdeDataDescription<T>

`abstract class RtdeDataDescription<T> where T : Enum`

Abstract base class that describes a single RTDE variable, including its name, data type, and array layout.

- `int ArraySize { get; }`: Gets the size of the register array this variable belongs to; otherwise 0.
- `T Data { get; }`: Gets the enum value identifying the RTDE variable.
- `string Description { get; }`: Gets a human-readable description of this variable.
- `bool IsArray { get; }`: Gets a value indicating whether this variable is an element of a register array.
- `int LowerIndex { get; }`: Gets the lower bound index when this variable represents an element of a register array; otherwise 0.
- `string Name { get; }`: Gets the protocol name of this variable as defined in the UR RTDE specification.
- `RtdeTypes Type { get; }`: Gets the RTDE wire type of this variable.

## RtdeDataPackageEventArgs

`class RtdeDataPackageEventArgs : PackageEventArgs`

Event arguments for an RTDE output data package received from the robot at the subscribed frequency.

- `RtdeDataPackageEventArgs()`
- `double MeasuredFrequency { get; set; }`: Gets or sets the measured frequency in Hz, computed from successive RtdeOutputData.Timestamp values.
- `RtdeOutputValues OutputDataValues { get; set; }`: Gets or sets the decoded output values contained in this data package.
- `byte OutputRecipeId { get; set; }`: Gets or sets the recipe identifier for the received output data (RTDE v2 only; 0 for v1).
- Inherited from [PackageEventArgs](UnderAutomation.UniversalRobots.Common.md#packageeventargs-robotprimaryinterfacerobotmodedata): `ReceiveDate`

## RtdeDoubleRegistersValue (robot.Rtde.OutputDataValues.InputDoubleRegisters)

`class RtdeDoubleRegistersValue : RtdeRegistersValue<double>, IRtdeRegistersValue`

RTDE double register array (48 registers, indices 0–47) for exchanging 64-bit floating-point values with the robot.

- `int LowerRangeIndex { get; }`: Gets the lower-bound register index for this register range.
- `double X0 { get; set; }`: Register n°0
- `double X1 { get; set; }`: Register n°1
- `double X10 { get; set; }`: Register n°10
- `double X11 { get; set; }`: Register n°11
- `double X12 { get; set; }`: Register n°12
- `double X13 { get; set; }`: Register n°13
- `double X14 { get; set; }`: Register n°14
- `double X15 { get; set; }`: Register n°15
- `double X16 { get; set; }`: Register n°16
- `double X17 { get; set; }`: Register n°17
- `double X18 { get; set; }`: Register n°18
- `double X19 { get; set; }`: Register n°19
- `double X2 { get; set; }`: Register n°2
- `double X20 { get; set; }`: Register n°20
- `double X21 { get; set; }`: Register n°21
- `double X22 { get; set; }`: Register n°22
- `double X23 { get; set; }`: Register n°23
- `double X24 { get; set; }`: Register n°24
- `double X25 { get; set; }`: Register n°25
- `double X26 { get; set; }`: Register n°26
- `double X27 { get; set; }`: Register n°27
- `double X28 { get; set; }`: Register n°28
- `double X29 { get; set; }`: Register n°29
- `double X3 { get; set; }`: Register n°3
- `double X30 { get; set; }`: Register n°30
- `double X31 { get; set; }`: Register n°31
- `double X32 { get; set; }`: Register n°32
- `double X33 { get; set; }`: Register n°33
- `double X34 { get; set; }`: Register n°34
- `double X35 { get; set; }`: Register n°35
- `double X36 { get; set; }`: Register n°36
- `double X37 { get; set; }`: Register n°37
- `double X38 { get; set; }`: Register n°38
- `double X39 { get; set; }`: Register n°39
- `double X4 { get; set; }`: Register n°4
- `double X40 { get; set; }`: Register n°40
- `double X41 { get; set; }`: Register n°41
- `double X42 { get; set; }`: Register n°42
- `double X43 { get; set; }`: Register n°43
- `double X44 { get; set; }`: Register n°44
- `double X45 { get; set; }`: Register n°45
- `double X46 { get; set; }`: Register n°46
- `double X47 { get; set; }`: Register n°47
- `double X5 { get; set; }`: Register n°5
- `double X6 { get; set; }`: Register n°6
- `double X7 { get; set; }`: Register n°7
- `double X8 { get; set; }`: Register n°8
- `double X9 { get; set; }`: Register n°9
- `void SetValue(int index, double value)`: Sets the value at the specified absolute register index.
- `double GetValue(int index)`: Gets the value at the specified absolute register index.
- `double[] Value { get; }`: Gets the current strongly-typed value.
- Inherited from [RtdeValue](UnderAutomation.UniversalRobots.Rtde.md#rtdevalue-robotrtdeoutputdatavaluesinputbitregisters): `Value`

## RtdeInputData

`enum RtdeInputData`

- ConfigurableDigitalOutput: Configurable digital outputs
- ConfigurableDigitalOutputMask: Configurable digital output bit mask
- ExternalForceTorque: Input external wrench when using ft_rtde_input_enable builtin.
- InputBitRegisters: 64 general purpose bits. X: [64..127] - The upper range of the boolean input registers can be used by external RTDE clients (i.e URCAPS).
- InputBtRegisters0To31: General purpose bits. This range of the boolean input registers is reserved for FieldBus/PLC interface usage.
- InputBtRegisters32To63: General purpose bits. This range of the boolean input registers is reserved for FieldBus/PLC interface usage.
- InputDoubleRegisters: 48 general purpose double registers. X: [0..23] - The lower range of the double input registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the double input registers can be used by external RTDE clients (i.e URCAPS).
- InputIntRegisters: 48 general purpose integer registers. X: [0..23] - The lower range of the integer input registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the integer input registers can be used by external RTDE clients (i.e URCAPS).
- SpeedSliderFraction: new speed slider value
- SpeedSliderMask: 0 = don't change speed slider with this input, 1 = use speed_slider_fraction to set speed slider value
- StandardAnalogOutput0: Standard analog output 0 (ratio) [0..1]
- StandardAnalogOutput1: Standard analog output 1 (ratio) [0..1]
- StandardAnalogOutputMask: Standard analog output mask
- StandardAnalogOutputType: Output domain {0=current[mA], 1=voltage[V]}. Bits 0-1: standard_analog_output_0 | standard_analog_output_1
- StandardDigitalOutput: Standard digital outputs
- StandardDigitalOutputMask: Standard digital output bit mask

## RtdeInputDataDescription

`class RtdeInputDataDescription : RtdeDataDescription<RtdeInputData>`

Describes a single RTDE input variable (client-to-robot), including its protocol name, type, and array information.

- `RtdeInputData Data { get; }`: Gets the enum value identifying the RTDE variable.
- `RtdeTypes Type { get; }`: Gets the RTDE wire type of this variable.
- `string Name { get; }`: Gets the protocol name of this variable as defined in the UR RTDE specification.
- `string Description { get; }`: Gets a human-readable description of this variable.
- `int LowerIndex { get; }`: Gets the lower bound index when this variable represents an element of a register array; otherwise 0.
- `int ArraySize { get; }`: Gets the size of the register array this variable belongs to; otherwise 0.
- `bool IsArray { get; }`: Gets a value indicating whether this variable is an element of a register array.

## RtdeInputSetup

`class RtdeInputSetup : RtdeSetup<RtdeInputSetupItem, RtdeInputData>, IList<RtdeInputSetupItem>, ICollection<RtdeInputSetupItem>, IList, ICollection, IReadOnlyList<RtdeInputSetupItem>, IReadOnlyCollection<RtdeInputSetupItem>, IEnumerable<RtdeInputSetupItem>, IEnumerable`

Defines the set of RTDE input variables (client-to-robot) to subscribe to as a recipe.

- `RtdeInputSetup()`
- `RtdeInputSetupItem Add(RtdeInputData data)`: Adds a variable to the recipe with register index 0.
- `RtdeInputSetupItem Add(RtdeInputData data, int index = 0)`: Adds a variable to the recipe with the specified register index.
- `int Remove(RtdeInputData data, int index = -1)`: Removes all items matching the specified variable and optionally a specific register index.
- `bool Contains(RtdeInputData data, int index = 0)`: Determines whether the recipe contains the specified variable at the given register index.
- `bool Contains(RtdeInputData data)`: Determines whether the recipe contains the specified variable at any register index.
- `RtdeInputSetupItem[] ToDistinctList()`: Returns a deduplicated array of setup items, removing duplicates by RtdeSetupItem%601.Data and RtdeSetupItem%601.Index.

## RtdeInputSetupItem

`class RtdeInputSetupItem : RtdeSetupItem<RtdeInputData>`

Represents a single RTDE input variable (client-to-robot) in an input recipe.

- `RtdeInputSetupItem()`: Initializes a new empty instance.
- `RtdeInputSetupItem(RtdeInputData data)`: Initializes a new instance for the specified input variable.
- `RtdeInputSetupItem(RtdeInputData data, int index)`: Initializes a new instance for the specified input variable and register index.
- `RtdeDataDescription<RtdeInputData> Description { get; }`: Gets the description metadata for this input variable.
- `int Index { get; set; }`: Gets or sets the register index for array/register RTDE variables. Defaults to 0.
- `RtdeInputData Data { get; set; }`: Gets or sets the enum value identifying the RTDE variable.
- `string Name { get; }`: Gets the RTDE protocol name for this variable, including the register index suffix for array variables.
- `RtdeTypes Type { get; }`: Gets the RTDE wire type of this variable.
- `string ProtocolType { get; }`: Gets the uppercase RTDE protocol type string sent on the wire during setup.

## RtdeInputValues

`class RtdeInputValues : RtdeBaseValues<RtdeInputData>`

Holds the current values for all RTDE input variables (client-to-robot). Use this to prepare data before calling Rtde.RtdeInputValues).

- `RtdeInputValues()`: Initializes a new instance with default values for all input variables.
- `byte ConfigurableDigitalOutput { get; set; }`: Configurable digital outputs
- `byte ConfigurableDigitalOutputMask { get; set; }`: Configurable digital output bit mask
- `CartesianCoordinates ExternalForceTorque { get; set; }`: Input external wrench when using ft_rtde_input_enable builtin.
- `object GetValue(RtdeInputSetupItem item)`: Gets the current value for the input variable described by a setup item.
- `RtdeBitRegistersValue InputBitRegisters { get; }`: 64 general purpose bits. X: [64..127] - The upper range of the boolean input registers can be used by external RTDE clients (i.e URCAPS).
- `uint InputBtRegisters0To31 { get; set; }`: General purpose bits. This range of the boolean input registers is reserved for FieldBus/PLC interface usage.
- `uint InputBtRegisters32To63 { get; set; }`: General purpose bits. This range of the boolean input registers is reserved for FieldBus/PLC interface usage.
- `RtdeDoubleRegistersValue InputDoubleRegisters { get; }`: 48 general purpose double registers. X: [0..23] - The lower range of the double input registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the double input registers can be used by external RTDE clients (i.e URCAPS).
- `RtdeIntRegistersValue InputIntRegisters { get; }`: 48 general purpose integer registers. X: [0..23] - The lower range of the integer input registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the integer input registers can be used by external RTDE clients (i.e URCAPS).
- `void Reset()`: Resets all input values to their defaults.
- `void SetValue(RtdeInputData data, int index, object value)`: Sets the value for the specified RTDE input variable at a given register index.
- `void SetValue(RtdeInputData data, object value)`: Sets the value for the specified RTDE input variable.
- `void SetValue(RtdeInputSetupItem item, object value)`: Sets the value for the input variable described by a setup item.
- `double SpeedSliderFraction { get; set; }`: new speed slider value
- `uint SpeedSliderMask { get; set; }`: 0 = don't change speed slider with this input, 1 = use speed_slider_fraction to set speed slider value
- `double StandardAnalogOutput0 { get; set; }`: Standard analog output 0 (ratio) [0..1]
- `double StandardAnalogOutput1 { get; set; }`: Standard analog output 1 (ratio) [0..1]
- `byte StandardAnalogOutputMask { get; set; }`: Standard analog output mask
- `byte StandardAnalogOutputType { get; set; }`: Output domain {0=current[mA], 1=voltage[V]}. Bits 0-1: standard_analog_output_0 | standard_analog_output_1
- `byte StandardDigitalOutput { get; set; }`: Standard digital outputs
- `byte StandardDigitalOutputMask { get; set; }`: Standard digital output bit mask
- Inherited from [RtdeBaseValues](UnderAutomation.UniversalRobots.Rtde.md#rtdebasevalues-robotrtdeoutputdatavalues): `Values`

## RtdeInputsDescription

`class RtdeInputsDescription`

- `RtdeInputsDescription()`
- `RtdeInputDataDescription ConfigurableDigitalOutput { get; }`: Configurable digital outputs
- `RtdeInputDataDescription ConfigurableDigitalOutputMask { get; }`: Configurable digital output bit mask
- `RtdeInputDataDescription ExternalForceTorque { get; }`: Input external wrench when using ft_rtde_input_enable builtin.
- `RtdeInputDataDescription Get(RtdeInputData data)`
- `RtdeInputDataDescription InputBitRegisters { get; }`: 64 general purpose bits. X: [64..127] - The upper range of the boolean input registers can be used by external RTDE clients (i.e URCAPS).
- `RtdeInputDataDescription InputBtRegisters0To31 { get; }`: General purpose bits. This range of the boolean input registers is reserved for FieldBus/PLC interface usage.
- `RtdeInputDataDescription InputBtRegisters32To63 { get; }`: General purpose bits. This range of the boolean input registers is reserved for FieldBus/PLC interface usage.
- `RtdeInputDataDescription InputDoubleRegisters { get; }`: 48 general purpose double registers. X: [0..23] - The lower range of the double input registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the double input registers can be used by external RTDE clients (i.e URCAPS).
- `RtdeInputDataDescription InputIntRegisters { get; }`: 48 general purpose integer registers. X: [0..23] - The lower range of the integer input registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the integer input registers can be used by external RTDE clients (i.e URCAPS).
- `ReadOnlyCollection<RtdeInputDataDescription> Items { get; }`
- `RtdeInputDataDescription SpeedSliderFraction { get; }`: new speed slider value
- `RtdeInputDataDescription SpeedSliderMask { get; }`: 0 = don't change speed slider with this input, 1 = use speed_slider_fraction to set speed slider value
- `RtdeInputDataDescription StandardAnalogOutput0 { get; }`: Standard analog output 0 (ratio) [0..1]
- `RtdeInputDataDescription StandardAnalogOutput1 { get; }`: Standard analog output 1 (ratio) [0..1]
- `RtdeInputDataDescription StandardAnalogOutputMask { get; }`: Standard analog output mask
- `RtdeInputDataDescription StandardAnalogOutputType { get; }`: Output domain {0=current[mA], 1=voltage[V]}. Bits 0-1: standard_analog_output_0 | standard_analog_output_1
- `RtdeInputDataDescription StandardDigitalOutput { get; }`: Standard digital outputs
- `RtdeInputDataDescription StandardDigitalOutputMask { get; }`: Standard digital output bit mask

## RtdeIntRegistersValue (robot.Rtde.OutputDataValues.InputIntRegisters)

`class RtdeIntRegistersValue : RtdeRegistersValue<int>, IRtdeRegistersValue`

RTDE integer register array (48 registers, indices 0–47) for exchanging 32-bit integer values with the robot.

- `int LowerRangeIndex { get; }`: Gets the lower-bound register index for this register range.
- `int X0 { get; set; }`: Register n°0
- `int X1 { get; set; }`: Register n°1
- `int X10 { get; set; }`: Register n°10
- `int X11 { get; set; }`: Register n°11
- `int X12 { get; set; }`: Register n°12
- `int X13 { get; set; }`: Register n°13
- `int X14 { get; set; }`: Register n°14
- `int X15 { get; set; }`: Register n°15
- `int X16 { get; set; }`: Register n°16
- `int X17 { get; set; }`: Register n°17
- `int X18 { get; set; }`: Register n°18
- `int X19 { get; set; }`: Register n°19
- `int X2 { get; set; }`: Register n°2
- `int X20 { get; set; }`: Register n°20
- `int X21 { get; set; }`: Register n°21
- `int X22 { get; set; }`: Register n°22
- `int X23 { get; set; }`: Register n°23
- `int X24 { get; set; }`: Register n°24
- `int X25 { get; set; }`: Register n°25
- `int X26 { get; set; }`: Register n°26
- `int X27 { get; set; }`: Register n°27
- `int X28 { get; set; }`: Register n°28
- `int X29 { get; set; }`: Register n°29
- `int X3 { get; set; }`: Register n°3
- `int X30 { get; set; }`: Register n°30
- `int X31 { get; set; }`: Register n°31
- `int X32 { get; set; }`: Register n°32
- `int X33 { get; set; }`: Register n°33
- `int X34 { get; set; }`: Register n°34
- `int X35 { get; set; }`: Register n°35
- `int X36 { get; set; }`: Register n°36
- `int X37 { get; set; }`: Register n°37
- `int X38 { get; set; }`: Register n°38
- `int X39 { get; set; }`: Register n°39
- `int X4 { get; set; }`: Register n°4
- `int X40 { get; set; }`: Register n°40
- `int X41 { get; set; }`: Register n°41
- `int X42 { get; set; }`: Register n°42
- `int X43 { get; set; }`: Register n°43
- `int X44 { get; set; }`: Register n°44
- `int X45 { get; set; }`: Register n°45
- `int X46 { get; set; }`: Register n°46
- `int X47 { get; set; }`: Register n°47
- `int X5 { get; set; }`: Register n°5
- `int X6 { get; set; }`: Register n°6
- `int X7 { get; set; }`: Register n°7
- `int X8 { get; set; }`: Register n°8
- `int X9 { get; set; }`: Register n°9
- `void SetValue(int index, int value)`: Sets the value at the specified absolute register index.
- `int GetValue(int index)`: Gets the value at the specified absolute register index.
- `int[] Value { get; }`: Gets the current strongly-typed value.
- Inherited from [RtdeValue](UnderAutomation.UniversalRobots.Rtde.md#rtdevalue-robotrtdeoutputdatavaluesinputbitregisters): `Value`

## RtdeOutputData

`enum RtdeOutputData`

- ActualCurrent: Actual joint currents
- ActualDigitalInputBits: Current state of the digital inputs. 0-7: Standard, 8-15: Configurable, 16-17: Tool
- ActualDigitalOutputBits: Current state of the digital outputs. 0-7: Standard, 8-15: Configurable, 16-17: Tool
- ActualExecutionTime: Controller real-time thread execution time
- ActualJointVoltage: Actual joint voltages
- ActualMainVoltage: Safety Control Board: Main voltage
- ActualMomentum: Norm of Cartesian linear momentum
- ActualQ: Actual joint positions
- ActualQd: Actual joint velocities
- ActualRobotCurrent: Safety Control Board: Robot current
- ActualRobotVoltage: Safety Control Board: Robot voltage (48V)
- ActualTcpForce: Generalized forces in the TCP. It compensates the measurement for forces and torques generated by the payload
- ActualTcpPose: Actual Cartesian coordinates of the tool: (x,y,z,rx,ry,rz), where rx, ry and rz is a rotation vector representation of the tool orientation
- ActualTcpSpeed: Actual speed of the tool given in Cartesian coordinates. The speed is given in [m/s] and the rotational part of the TCP speed (rx, ry, rz) is the angular velocity given in [rad/s]
- ActualToolAccelerometer: Tool x, y and z accelerometer values
- AnalogIOTypes: Bits 0-3: analog input 0 | analog input 1 | analog output 0 | analog output 1, {0=current[mA], 1=voltage[V]}
- ElbowPosition: Position of robot elbow in Cartesian Base Coordinates
- ElbowVelocity: Velocity of robot elbow in Cartesian Base Coordinates
- Euromap67InputBits: Euromap67 input bits
- Euromap67OutputBits: Euromap67 output bits
- Euromap67_24VCurrent: Euromap 24V current [mA]
- Euromap67_24VVoltage: Euromap 24V voltage [V]
- FTRawWrench: Raw force and torque measurement, not compensated for forces and torques caused by the payload
- IOCurrent: I/O current [mA]
- InputBitRegisters: 64 general purpose bits, X: [64..127] - The upper range of the boolean output registers can be used by external RTDE clients (i.e URCAPS).
- InputBitRegisters0To31: General purpose bits (input read back). This range of the boolean output registers is reserved for FieldBus/PLC interface usage.
- InputBitRegisters32To63: General purpose bits (input read back), This range of the boolean output registers is reserved for FieldBus/PLC interface usage.
- InputDoubleRegisters: 48 general purpose double registers. X: [0..23] - The lower range of the double input registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the double input registers can be used by external RTDE clients (i.e URCAPS).
- InputIntRegisters: 48 general purpose integer registers. X: [0..23] - The lower range of the integer input registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the integer input registers can be used by external RTDE clients (i.e URCAPS).
- JointControlOutput: Joint control currents
- JointMode: Joint control modes
- JointTemperatures: Temperature of each joint in degrees Celsius
- OutputBitRegisters: 64 general purpose bits. X: [64..127] - The upper range of the boolean output registers can be used by external RTDE clients (i.e URCAPS).
- OutputBitRegisters0To31: General purpose bits
- OutputBitRegisters32To63: General purpose bits
- OutputDoubleRegisters: 48 general purpose double registers. X: [0..23] - The lower range of the double output registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the double output registers can be used by external RTDE clients (i.e URCAPS).
- OutputIntRegisters: 48 general purpose integer registers. X: [0..23] - The lower range of the integer output registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the integer output registers can be used by external RTDE clients (i.e URCAPS).
- Payload: Payload mass Kg
- PayloadCOG: Payload Center of Gravity (CoGx, CoGy, CoGz) m
- PayloadInertia: Payload inertia matrix elements (Ixx,Iyy,Izz,Ixy,Ixz,Iyz] expressed in kg*m^2
- RobotMode: Robot mode
- RobotStatusBits: Bits 0-3:Is power on | Is program running | Is teach button pressed | Is power button pressed
- RuntimeState: Program state
- SafetyMode: Safety mode
- SafetyStatus: Safety status
- SafetyStatusBits: Bits 0-10: Is normal mode | Is reduced mode | Is protective stopped | Is recovery mode | Is safeguard stopped | Is system emergency stopped | Is robot emergency stopped | Is emergency stopped | Is violation | Is fault | Is stopped due to safety
- ScriptControlLine: Script line number that is actually in control of the robot given the robot is locked by one of the threads in the script. If no thread is locking the robot this field is set to '0'. Script line number should not be confused with program tree line number displayed on polyscope.
- SpeedScaling: Speed scaling of the trajectory limiter
- StandardAnalogInput0: Standard analog input 0 [mA or V]
- StandardAnalogInput1: Standard analog input 1 [mA or V]
- StandardAnalogOutput0: Standard analog output 0 [mA or V]
- StandardAnalogOutput1: Standard analog output 1 [mA or V]
- TargetCurrent: Target joint currents
- TargetMoment: Target joint moments (torques)
- TargetQ: Target joint positions
- TargetQd: Target joint velocities
- TargetQdd: Target joint accelerations
- TargetSpeedFraction: Target speed fraction
- TargetTcpPose: Target Cartesian coordinates of the tool: (x,y,z,rx,ry,rz), where rx, ry and rz is a rotation vector representation of the tool orientation
- TargetTcpSpeed: Target speed of the tool given in Cartesian coordinates. The speed is given in [m/s] and the rotational part of the TCP speed (rx, ry, rz) is the angular velocity given in [rad/s]
- TcpForceScalar: TCP force scalar [N]
- Timestamp: Time elapsed since the controller was started [s]
- ToolAnalogInput0: Tool analog input 0 [mA or V]
- ToolAnalogInput1: Tool analog input 1 [mA or V]
- ToolAnalogInputTypes: Output domain {0=current[mA], 1=voltage[V]} Bits 0-1: tool_analog_input_0 | tool_analog_input_1
- ToolDigitalOutput0mode: The current mode of digital output 0
- ToolDigitalOutput1Mode: The current mode of digital output 1
- ToolMode: Tool mode
- ToolOutputCurrent: Tool current [mA]
- ToolOutputMode: The current output mode
- ToolOutputVoltage: Tool output voltage [V]
- ToolTemperature: Tool temperature in degrees Celsius

## RtdeOutputDataDescription

`class RtdeOutputDataDescription : RtdeDataDescription<RtdeOutputData>`

Describes a single RTDE output variable (robot-to-client), including its protocol name, type, and array information.

- `RtdeOutputData Data { get; }`: Gets the enum value identifying the RTDE variable.
- `RtdeTypes Type { get; }`: Gets the RTDE wire type of this variable.
- `string Name { get; }`: Gets the protocol name of this variable as defined in the UR RTDE specification.
- `string Description { get; }`: Gets a human-readable description of this variable.
- `int LowerIndex { get; }`: Gets the lower bound index when this variable represents an element of a register array; otherwise 0.
- `int ArraySize { get; }`: Gets the size of the register array this variable belongs to; otherwise 0.
- `bool IsArray { get; }`: Gets a value indicating whether this variable is an element of a register array.

## RtdeOutputSetup

`class RtdeOutputSetup : RtdeSetup<RtdeOutputSetupItem, RtdeOutputData>, IList<RtdeOutputSetupItem>, ICollection<RtdeOutputSetupItem>, IList, ICollection, IReadOnlyList<RtdeOutputSetupItem>, IReadOnlyCollection<RtdeOutputSetupItem>, IEnumerable<RtdeOutputSetupItem>, IEnumerable`

Defines the set of RTDE output variables (robot-to-client) to subscribe to as a recipe. The RtdeOutputData.Timestamp variable is added by default.

- `RtdeOutputSetup()`: Initializes a new instance with the default RtdeOutputData.Timestamp variable.
- `RtdeOutputSetupItem Add(RtdeOutputData data)`: Adds a variable to the recipe with register index 0.
- `RtdeOutputSetupItem Add(RtdeOutputData data, int index = 0)`: Adds a variable to the recipe with the specified register index.
- `int Remove(RtdeOutputData data, int index = -1)`: Removes all items matching the specified variable and optionally a specific register index.
- `bool Contains(RtdeOutputData data, int index = 0)`: Determines whether the recipe contains the specified variable at the given register index.
- `bool Contains(RtdeOutputData data)`: Determines whether the recipe contains the specified variable at any register index.
- `RtdeOutputSetupItem[] ToDistinctList()`: Returns a deduplicated array of setup items, removing duplicates by RtdeSetupItem%601.Data and RtdeSetupItem%601.Index.

## RtdeOutputSetupItem

`class RtdeOutputSetupItem : RtdeSetupItem<RtdeOutputData>`

Represents a single RTDE output variable (robot-to-client) in an output recipe.

- `RtdeOutputSetupItem()`: Initializes a new empty instance.
- `RtdeOutputSetupItem(RtdeOutputData data)`: Initializes a new instance for the specified output variable.
- `RtdeOutputSetupItem(RtdeOutputData data, int index)`: Initializes a new instance for the specified output variable and register index.
- `RtdeDataDescription<RtdeOutputData> Description { get; }`: Gets the description metadata for this output variable.
- `int Index { get; set; }`: Gets or sets the register index for array/register RTDE variables. Defaults to 0.
- `RtdeOutputData Data { get; set; }`: Gets or sets the enum value identifying the RTDE variable.
- `string Name { get; }`: Gets the RTDE protocol name for this variable, including the register index suffix for array variables.
- `RtdeTypes Type { get; }`: Gets the RTDE wire type of this variable.
- `string ProtocolType { get; }`: Gets the uppercase RTDE protocol type string sent on the wire during setup.

## RtdeOutputValues (robot.Rtde.OutputDataValues)

`class RtdeOutputValues : RtdeBaseValues<RtdeOutputData>`

Holds the current values for all RTDE output variables (robot-to-client). Updated automatically when data is received from the robot.

- `JointsDoubleValues ActualCurrent { get; set; }`: Actual joint currents
- `ulong ActualDigitalInputBits { get; set; }`: Current state of the digital inputs. 0-7: Standard, 8-15: Configurable, 16-17: Tool
- `ulong ActualDigitalOutputBits { get; set; }`: Current state of the digital outputs. 0-7: Standard, 8-15: Configurable, 16-17: Tool
- `double ActualExecutionTime { get; set; }`: Controller real-time thread execution time
- `JointsDoubleValues ActualJointVoltage { get; set; }`: Actual joint voltages
- `double ActualMainVoltage { get; set; }`: Safety Control Board: Main voltage
- `double ActualMomentum { get; set; }`: Norm of Cartesian linear momentum
- `JointsDoubleValues ActualQ { get; set; }`: Actual joint positions
- `JointsDoubleValues ActualQd { get; set; }`: Actual joint velocities
- `double ActualRobotCurrent { get; set; }`: Safety Control Board: Robot current
- `double ActualRobotVoltage { get; set; }`: Safety Control Board: Robot voltage (48V)
- `CartesianCoordinates ActualTcpForce { get; set; }`: Generalized forces in the TCP. It compensates the measurement for forces and torques generated by the payload
- `Pose ActualTcpPose { get; set; }`: Actual Cartesian coordinates of the tool: (x,y,z,rx,ry,rz), where rx, ry and rz is a rotation vector representation of the tool orientation
- `Pose ActualTcpSpeed { get; set; }`: Actual speed of the tool given in Cartesian coordinates. The speed is given in [m/s] and the rotational part of the TCP speed (rx, ry, rz) is the angular velocity given in [rad/s]
- `Vector3D ActualToolAccelerometer { get; set; }`: Tool x, y and z accelerometer values
- `uint AnalogIOTypes { get; set; }`: Bits 0-3: analog input 0 | analog input 1 | analog output 0 | analog output 1, {0=current[mA], 1=voltage[V]}
- `Vector3D ElbowPosition { get; set; }`: Position of robot elbow in Cartesian Base Coordinates
- `Vector3D ElbowVelocity { get; set; }`: Velocity of robot elbow in Cartesian Base Coordinates
- `uint Euromap67InputBits { get; set; }`: Euromap67 input bits
- `uint Euromap67OutputBits { get; set; }`: Euromap67 output bits
- `double Euromap67_24VCurrent { get; set; }`: Euromap 24V current [mA]
- `double Euromap67_24VVoltage { get; set; }`: Euromap 24V voltage [V]
- `CartesianCoordinates FTRawWrench { get; set; }`: Raw force and torque measurement, not compensated for forces and torques caused by the payload
- `object GetValue(RtdeOutputSetupItem item)`: Gets the current value for the output variable described by a setup item.
- `double IOCurrent { get; set; }`: I/O current [mA]
- `RtdeBitRegistersValue InputBitRegisters { get; }`: 64 general purpose bits, X: [64..127] - The upper range of the boolean output registers can be used by external RTDE clients (i.e URCAPS).
- `uint InputBitRegisters0To31 { get; set; }`: General purpose bits (input read back). This range of the boolean output registers is reserved for FieldBus/PLC interface usage.
- `uint InputBitRegisters32To63 { get; set; }`: General purpose bits (input read back), This range of the boolean output registers is reserved for FieldBus/PLC interface usage.
- `RtdeDoubleRegistersValue InputDoubleRegisters { get; }`: 48 general purpose double registers. X: [0..23] - The lower range of the double input registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the double input registers can be used by external RTDE clients (i.e URCAPS).
- `RtdeIntRegistersValue InputIntRegisters { get; }`: 48 general purpose integer registers. X: [0..23] - The lower range of the integer input registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the integer input registers can be used by external RTDE clients (i.e URCAPS).
- `JointsDoubleValues JointControlOutput { get; set; }`: Joint control currents
- `JointsIntValues JointMode { get; set; }`: Joint control modes
- `JointsDoubleValues JointTemperatures { get; set; }`: Temperature of each joint in degrees Celsius
- `RtdeBitRegistersValue OutputBitRegisters { get; }`: 64 general purpose bits. X: [64..127] - The upper range of the boolean output registers can be used by external RTDE clients (i.e URCAPS).
- `uint OutputBitRegisters0To31 { get; set; }`: General purpose bits
- `uint OutputBitRegisters32To63 { get; set; }`: General purpose bits
- `RtdeDoubleRegistersValue OutputDoubleRegisters { get; }`: 48 general purpose double registers. X: [0..23] - The lower range of the double output registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the double output registers can be used by external RTDE clients (i.e URCAPS).
- `RtdeIntRegistersValue OutputIntRegisters { get; }`: 48 general purpose integer registers. X: [0..23] - The lower range of the integer output registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the integer output registers can be used by external RTDE clients (i.e URCAPS).
- `double Payload { get; set; }`: Payload mass Kg
- `Vector3D PayloadCOG { get; set; }`: Payload Center of Gravity (CoGx, CoGy, CoGz) m
- `CartesianCoordinates PayloadInertia { get; set; }`: Payload inertia matrix elements (Ixx,Iyy,Izz,Ixy,Ixz,Iyz] expressed in kg*m^2
- `int RobotMode { get; set; }`: Robot mode
- `uint RobotStatusBits { get; set; }`: Bits 0-3:Is power on | Is program running | Is teach button pressed | Is power button pressed
- `uint RuntimeState { get; set; }`: Program state
- `int SafetyMode { get; set; }`: Safety mode
- `int SafetyStatus { get; set; }`: Safety status
- `uint SafetyStatusBits { get; set; }`: Bits 0-10: Is normal mode | Is reduced mode | Is protective stopped | Is recovery mode | Is safeguard stopped | Is system emergency stopped | Is robot emergency stopped | Is emergency stopped | Is violation | Is fault | Is stopped due to safety
- `uint ScriptControlLine { get; set; }`: Script line number that is actually in control of the robot given the robot is locked by one of the threads in the script. If no thread is locking the robot this field is set to '0'. Script line number should not be confused with program tree line number displayed on polyscope.
- `double SpeedScaling { get; set; }`: Speed scaling of the trajectory limiter
- `double StandardAnalogInput0 { get; set; }`: Standard analog input 0 [mA or V]
- `double StandardAnalogInput1 { get; set; }`: Standard analog input 1 [mA or V]
- `double StandardAnalogOutput0 { get; set; }`: Standard analog output 0 [mA or V]
- `double StandardAnalogOutput1 { get; set; }`: Standard analog output 1 [mA or V]
- `JointsDoubleValues TargetCurrent { get; set; }`: Target joint currents
- `JointsDoubleValues TargetMoment { get; set; }`: Target joint moments (torques)
- `JointsDoubleValues TargetQ { get; set; }`: Target joint positions
- `JointsDoubleValues TargetQd { get; set; }`: Target joint velocities
- `JointsDoubleValues TargetQdd { get; set; }`: Target joint accelerations
- `double TargetSpeedFraction { get; set; }`: Target speed fraction
- `Pose TargetTcpPose { get; set; }`: Target Cartesian coordinates of the tool: (x,y,z,rx,ry,rz), where rx, ry and rz is a rotation vector representation of the tool orientation
- `Pose TargetTcpSpeed { get; set; }`: Target speed of the tool given in Cartesian coordinates. The speed is given in [m/s] and the rotational part of the TCP speed (rx, ry, rz) is the angular velocity given in [rad/s]
- `double TcpForceScalar { get; set; }`: TCP force scalar [N]
- `double Timestamp { get; set; }`: Time elapsed since the controller was started [s]
- `double ToolAnalogInput0 { get; set; }`: Tool analog input 0 [mA or V]
- `double ToolAnalogInput1 { get; set; }`: Tool analog input 1 [mA or V]
- `uint ToolAnalogInputTypes { get; set; }`: Output domain {0=current[mA], 1=voltage[V]} Bits 0-1: tool_analog_input_0 | tool_analog_input_1
- `byte ToolDigitalOutput0mode { get; set; }`: The current mode of digital output 0
- `byte ToolDigitalOutput1Mode { get; set; }`: The current mode of digital output 1
- `uint ToolMode { get; set; }`: Tool mode
- `double ToolOutputCurrent { get; set; }`: Tool current [mA]
- `byte ToolOutputMode { get; set; }`: The current output mode
- `int ToolOutputVoltage { get; set; }`: Tool output voltage [V]
- `double ToolTemperature { get; set; }`: Tool temperature in degrees Celsius
- Inherited from [RtdeBaseValues](UnderAutomation.UniversalRobots.Rtde.md#rtdebasevalues-robotrtdeoutputdatavalues): `Values`

## RtdeOutputsDescription

`class RtdeOutputsDescription`

- `RtdeOutputsDescription()`
- `RtdeOutputDataDescription ActualCurrent { get; }`: Actual joint currents
- `RtdeOutputDataDescription ActualDigitalInputBits { get; }`: Current state of the digital inputs. 0-7: Standard, 8-15: Configurable, 16-17: Tool
- `RtdeOutputDataDescription ActualDigitalOutputBits { get; }`: Current state of the digital outputs. 0-7: Standard, 8-15: Configurable, 16-17: Tool
- `RtdeOutputDataDescription ActualExecutionTime { get; }`: Controller real-time thread execution time
- `RtdeOutputDataDescription ActualJointVoltage { get; }`: Actual joint voltages
- `RtdeOutputDataDescription ActualMainVoltage { get; }`: Safety Control Board: Main voltage
- `RtdeOutputDataDescription ActualMomentum { get; }`: Norm of Cartesian linear momentum
- `RtdeOutputDataDescription ActualQ { get; }`: Actual joint positions
- `RtdeOutputDataDescription ActualQd { get; }`: Actual joint velocities
- `RtdeOutputDataDescription ActualRobotCurrent { get; }`: Safety Control Board: Robot current
- `RtdeOutputDataDescription ActualRobotVoltage { get; }`: Safety Control Board: Robot voltage (48V)
- `RtdeOutputDataDescription ActualTcpForce { get; }`: Generalized forces in the TCP. It compensates the measurement for forces and torques generated by the payload
- `RtdeOutputDataDescription ActualTcpPose { get; }`: Actual Cartesian coordinates of the tool: (x,y,z,rx,ry,rz), where rx, ry and rz is a rotation vector representation of the tool orientation
- `RtdeOutputDataDescription ActualTcpSpeed { get; }`: Actual speed of the tool given in Cartesian coordinates. The speed is given in [m/s] and the rotational part of the TCP speed (rx, ry, rz) is the angular velocity given in [rad/s]
- `RtdeOutputDataDescription ActualToolAccelerometer { get; }`: Tool x, y and z accelerometer values
- `RtdeOutputDataDescription AnalogIOTypes { get; }`: Bits 0-3: analog input 0 | analog input 1 | analog output 0 | analog output 1, {0=current[mA], 1=voltage[V]}
- `RtdeOutputDataDescription ElbowPosition { get; }`: Position of robot elbow in Cartesian Base Coordinates
- `RtdeOutputDataDescription ElbowVelocity { get; }`: Velocity of robot elbow in Cartesian Base Coordinates
- `RtdeOutputDataDescription Euromap67InputBits { get; }`: Euromap67 input bits
- `RtdeOutputDataDescription Euromap67OutputBits { get; }`: Euromap67 output bits
- `RtdeOutputDataDescription Euromap67_24VCurrent { get; }`: Euromap 24V current [mA]
- `RtdeOutputDataDescription Euromap67_24VVoltage { get; }`: Euromap 24V voltage [V]
- `RtdeOutputDataDescription FTRawWrench { get; }`: Raw force and torque measurement, not compensated for forces and torques caused by the payload
- `RtdeOutputDataDescription Get(RtdeOutputData data)`
- `RtdeOutputDataDescription IOCurrent { get; }`: I/O current [mA]
- `RtdeOutputDataDescription InputBitRegisters { get; }`: 64 general purpose bits, X: [64..127] - The upper range of the boolean output registers can be used by external RTDE clients (i.e URCAPS).
- `RtdeOutputDataDescription InputBitRegisters0To31 { get; }`: General purpose bits (input read back). This range of the boolean output registers is reserved for FieldBus/PLC interface usage.
- `RtdeOutputDataDescription InputBitRegisters32To63 { get; }`: General purpose bits (input read back), This range of the boolean output registers is reserved for FieldBus/PLC interface usage.
- `RtdeOutputDataDescription InputDoubleRegisters { get; }`: 48 general purpose double registers. X: [0..23] - The lower range of the double input registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the double input registers can be used by external RTDE clients (i.e URCAPS).
- `RtdeOutputDataDescription InputIntRegisters { get; }`: 48 general purpose integer registers. X: [0..23] - The lower range of the integer input registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the integer input registers can be used by external RTDE clients (i.e URCAPS).
- `ReadOnlyCollection<RtdeOutputDataDescription> Items { get; }`
- `RtdeOutputDataDescription JointControlOutput { get; }`: Joint control currents
- `RtdeOutputDataDescription JointMode { get; }`: Joint control modes
- `RtdeOutputDataDescription JointTemperatures { get; }`: Temperature of each joint in degrees Celsius
- `RtdeOutputDataDescription OutputBitRegisters { get; }`: 64 general purpose bits. X: [64..127] - The upper range of the boolean output registers can be used by external RTDE clients (i.e URCAPS).
- `RtdeOutputDataDescription OutputBitRegisters0To31 { get; }`: General purpose bits
- `RtdeOutputDataDescription OutputBitRegisters32To63 { get; }`: General purpose bits
- `RtdeOutputDataDescription OutputDoubleRegisters { get; }`: 48 general purpose double registers. X: [0..23] - The lower range of the double output registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the double output registers can be used by external RTDE clients (i.e URCAPS).
- `RtdeOutputDataDescription OutputIntRegisters { get; }`: 48 general purpose integer registers. X: [0..23] - The lower range of the integer output registers is reserved for FieldBus/PLC interface usage. X: [24..47] - The upper range of the integer output registers can be used by external RTDE clients (i.e URCAPS).
- `RtdeOutputDataDescription Payload { get; }`: Payload mass Kg
- `RtdeOutputDataDescription PayloadCOG { get; }`: Payload Center of Gravity (CoGx, CoGy, CoGz) m
- `RtdeOutputDataDescription PayloadInertia { get; }`: Payload inertia matrix elements (Ixx,Iyy,Izz,Ixy,Ixz,Iyz] expressed in kg*m^2
- `RtdeOutputDataDescription RobotMode { get; }`: Robot mode
- `RtdeOutputDataDescription RobotStatusBits { get; }`: Bits 0-3:Is power on | Is program running | Is teach button pressed | Is power button pressed
- `RtdeOutputDataDescription RuntimeState { get; }`: Program state
- `RtdeOutputDataDescription SafetyMode { get; }`: Safety mode
- `RtdeOutputDataDescription SafetyStatus { get; }`: Safety status
- `RtdeOutputDataDescription SafetyStatusBits { get; }`: Bits 0-10: Is normal mode | Is reduced mode | Is protective stopped | Is recovery mode | Is safeguard stopped | Is system emergency stopped | Is robot emergency stopped | Is emergency stopped | Is violation | Is fault | Is stopped due to safety
- `RtdeOutputDataDescription ScriptControlLine { get; }`: Script line number that is actually in control of the robot given the robot is locked by one of the threads in the script. If no thread is locking the robot this field is set to '0'. Script line number should not be confused with program tree line number displayed on polyscope.
- `RtdeOutputDataDescription SpeedScaling { get; }`: Speed scaling of the trajectory limiter
- `RtdeOutputDataDescription StandardAnalogInput0 { get; }`: Standard analog input 0 [mA or V]
- `RtdeOutputDataDescription StandardAnalogInput1 { get; }`: Standard analog input 1 [mA or V]
- `RtdeOutputDataDescription StandardAnalogOutput0 { get; }`: Standard analog output 0 [mA or V]
- `RtdeOutputDataDescription StandardAnalogOutput1 { get; }`: Standard analog output 1 [mA or V]
- `RtdeOutputDataDescription TargetCurrent { get; }`: Target joint currents
- `RtdeOutputDataDescription TargetMoment { get; }`: Target joint moments (torques)
- `RtdeOutputDataDescription TargetQ { get; }`: Target joint positions
- `RtdeOutputDataDescription TargetQd { get; }`: Target joint velocities
- `RtdeOutputDataDescription TargetQdd { get; }`: Target joint accelerations
- `RtdeOutputDataDescription TargetSpeedFraction { get; }`: Target speed fraction
- `RtdeOutputDataDescription TargetTcpPose { get; }`: Target Cartesian coordinates of the tool: (x,y,z,rx,ry,rz), where rx, ry and rz is a rotation vector representation of the tool orientation
- `RtdeOutputDataDescription TargetTcpSpeed { get; }`: Target speed of the tool given in Cartesian coordinates. The speed is given in [m/s] and the rotational part of the TCP speed (rx, ry, rz) is the angular velocity given in [rad/s]
- `RtdeOutputDataDescription TcpForceScalar { get; }`: TCP force scalar [N]
- `RtdeOutputDataDescription Timestamp { get; }`: Time elapsed since the controller was started [s]
- `RtdeOutputDataDescription ToolAnalogInput0 { get; }`: Tool analog input 0 [mA or V]
- `RtdeOutputDataDescription ToolAnalogInput1 { get; }`: Tool analog input 1 [mA or V]
- `RtdeOutputDataDescription ToolAnalogInputTypes { get; }`: Output domain {0=current[mA], 1=voltage[V]} Bits 0-1: tool_analog_input_0 | tool_analog_input_1
- `RtdeOutputDataDescription ToolDigitalOutput0mode { get; }`: The current mode of digital output 0
- `RtdeOutputDataDescription ToolDigitalOutput1Mode { get; }`: The current mode of digital output 1
- `RtdeOutputDataDescription ToolMode { get; }`: Tool mode
- `RtdeOutputDataDescription ToolOutputCurrent { get; }`: Tool current [mA]
- `RtdeOutputDataDescription ToolOutputMode { get; }`: The current output mode
- `RtdeOutputDataDescription ToolOutputVoltage { get; }`: Tool output voltage [V]
- `RtdeOutputDataDescription ToolTemperature { get; }`: Tool temperature in degrees Celsius

## RtdeProtocolVersionEventArgs

`class RtdeProtocolVersionEventArgs : RtdeBasicRequestEventArgs`

Event arguments indicating which RTDE protocol version was negotiated with the robot.

- `RtdeProtocolVersionEventArgs()`
- `RtdeVersions Version { get; set; }`: Gets or sets the negotiated RTDE protocol version.
- Inherited from [RtdeBasicRequestEventArgs](UnderAutomation.UniversalRobots.Rtde.md#rtdebasicrequesteventargs): `Accepted`
- Inherited from [PackageEventArgs](UnderAutomation.UniversalRobots.Common.md#packageeventargs-robotprimaryinterfacerobotmodedata): `ReceiveDate`

## RtdeRegistersValue<T>

`abstract class RtdeRegistersValue<T> : RtdeValue<T[]>, IRtdeRegistersValue`

Abstract base for a fixed-size register array of type T exchanged through RTDE.

- `T GetValue(int index)`: Gets the value at the specified absolute register index.
- `abstract int LowerRangeIndex { get; }`: Gets the lower-bound register index for this register range.
- `void SetValue(int index, T value)`: Sets the value at the specified absolute register index.
- `T[] Value { get; }`: Gets the current strongly-typed value.
- Inherited from [RtdeValue](UnderAutomation.UniversalRobots.Rtde.md#rtdevalue-robotrtdeoutputdatavaluesinputbitregisters): `Value`

## RtdeTextMessageEventArgs (robot.Rtde.LastTextMessage)

`class RtdeTextMessageEventArgs : PackageEventArgs`

Event arguments for a text message received from the robot via the RTDE interface.

- `RtdeTextMessageEventArgs()`
- `string Message { get; set; }`: Gets or sets the text content of the message.
- `string Source { get; set; }`: Gets or sets the source module that generated the message on the robot.
- `byte WarningLevel { get; set; }`: Gets or sets the warning level of the message (0 = exception/error, 1 = warning, 2 = info).
- Inherited from [PackageEventArgs](UnderAutomation.UniversalRobots.Common.md#packageeventargs-robotprimaryinterfacerobotmodedata): `ReceiveDate`

## RtdeTypes

`enum RtdeTypes`

RTDE data types used to describe the wire format of each RTDE variable.

- Bool: Boolean value (1 byte on the wire).
- BoolArray: Boolean value stored as part of a register array.
- CartesianCoordinates: 6-element double vector representing Cartesian coordinates.
- Double: 64-bit floating-point number.
- DoubleArray: 64-bit double value stored as part of a register array.
- Int32: Signed 32-bit integer.
- Int32Array: 32-bit integer value stored as part of a register array.
- JointsDoubleValues: 6-element double vector with one value per robot joint.
- JointsIntValues: 6-element 32-bit integer vector with one value per robot joint.
- Pose: 6-element double vector representing a TCP pose (X, Y, Z, Rx, Ry, Rz).
- Uint32: Unsigned 32-bit integer.
- Uint64: Unsigned 64-bit integer.
- Uint8: Unsigned 8-bit integer.
- Vector3D: 3-element double vector (X, Y, Z).

## RtdeValue<T>

`class RtdeValue<T> : RtdeValue`

Strongly-typed RTDE variable value of type T.

- `T Value { get; }`: Gets the current strongly-typed value.

## RtdeValue (robot.Rtde.OutputDataValues.InputBitRegisters)

`abstract class RtdeValue`

Abstract base class for a single RTDE variable value exchanged between the client and the robot.

- `object Value { get; protected set; }`: Gets or sets the current value as an untyped object.

## RtdeVersions (robot.Rtde.Version)

`enum RtdeVersions`

RTDE version numbers

- V1: Rtde version 1
- V2: Rtde version 2
