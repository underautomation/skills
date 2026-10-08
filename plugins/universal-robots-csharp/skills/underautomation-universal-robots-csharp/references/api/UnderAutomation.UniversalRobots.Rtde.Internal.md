# UnderAutomation.UniversalRobots.Rtde.Internal

## RtdeClientBase (robot.Rtde)

`abstract class RtdeClientBase : URServiceBase`

Base class common to all RTDE clients

- `double AppliedFrequency { get; }`: Output data frequency requested to the robot, only for RTDE version 2
- `bool Connected { get; }`: Gets a value indicating if RTDE client is connected to the robot
- `void Disconnect()`: Close the RTDE connection to the robot
- `string IP { get; }`: IP address of the robot
- `byte InputRecipeId { get; }`: Recipe Identifier of input sent data
- `bool InputRecipeIsValid { get; }`: Indicates that the recipe is valid, i.e. that all the registers have been found and are not already reserved for writing by another RTDE client. Check event SetupInputsReceived to see which registers are NOT_FOUND or IN_USE
- `RtdeInputSetupItem[] InputSetup { get; }`: List of all data the PC can write to the robot (robot point of view)
- `RtdeTextMessageEventArgs LastTextMessage { get; }`: Last text received from the robot
- `double MeasuredFrequency { get; }`: Measured output data packet frequency. "Timestamp" output data shoud be part of output setup to measure frequency.
- `event EventHandler<RtdeDataPackageEventArgs> OutputDataReceived`: Event raised when data from the robot is comming at specified frequency
- `RtdeOutputValues OutputDataValues { get; }`: Last data received from the robot
- `byte OutputRecipeId { get; }`: Recipe Identifier of output received data
- `RtdeOutputSetupItem[] OutputSetup { get; }`: List of all data sent from the robot to the PC (robot point of view)
- `event EventHandler<PackageEventArgs> PackageReceived`: Generic event raised each time a RTDE package is received
- `void Pause()`: Pause data streaming without disconnecting client
- `event EventHandler<RtdeBasicRequestEventArgs> PauseReceived`: Event raised when streaming is paused
- `event EventHandler<RtdeProtocolVersionEventArgs> ProtocolVersionReceived`: Event raised during connection when the robot specifies if asked protocol version is supported
- `void Resume()`: Restart data streaming after a Pause
- `event EventHandler<RtdeControlPackageSetupInputsEventArgs> SetupInputsReceived`: Event raised during connection when the robot acknowledges input setup
- `event EventHandler<RtdeControlPackageSetupOutputsEventArgs> SetupOutputsReceived`: Event raised during connection when the robot acknowledges output setup
- `event EventHandler<RtdeBasicRequestEventArgs> StartReceived`: Event raised as soon as data streaming starts
- `RTDEStates State { get; }`: Current RTDE state
- `event EventHandler<RtdeTextMessageEventArgs> TextMessageReceived`: Event raised when a RTDE message is received
- `RtdeVersions Version { get; }`: Current protocol version used to stream data
- `void WriteInputs(RtdeInputValues inputValues)`: Write data to controller. Data must be those selected in connect parameters
- Inherited from [URServiceBase](UnderAutomation.UniversalRobots.Internal.md#urservicebase-robot): `InternalErrorOccured`

## RtdeParametersBase

`abstract class RtdeParametersBase`

Base parameters to set up RTDE

- `const int DEFAULT_PORT = 30004`: Default RTDE TCP port used (30004)
- `double Frequency { get; set; }`: For RTDE version 2, you can specify a frequency for output received data. Maximum frequency depends on your robot version. If you set frequency to 0, maximum frequency will be choosen Default value is 10Hz
- `RtdeInputSetup InputSetup { get; set; }`: List of all input data you can send to the robot
- `RtdeOutputSetup OutputSetup { get; set; }`: List of all output data the robot will send to your application
- `int Port { get; set; }`: TCP port used for RTDE connection. Default : 30004
- `RtdeVersions Version { get; set; }`: RTDE version. If set to Auto, the most recent version will be choosen according to your robot version Default value is V2

## RtdeSetup<T, U>

`abstract class RtdeSetup<T, U> : List<T>, IList<T>, ICollection<T>, IList, ICollection, IReadOnlyList<T>, IReadOnlyCollection<T>, IEnumerable<T>, IEnumerable where T : RtdeSetupItem<U>, new() where U : Enum`

Base class for an RTDE recipe, a collection of T setup items that describe which RTDE variables to exchange.

- `T Add(U data)`: Adds a variable to the recipe with register index 0.
- `T Add(U data, int index = 0)`: Adds a variable to the recipe with the specified register index.
- `bool Contains(U data)`: Determines whether the recipe contains the specified variable at any register index.
- `bool Contains(U data, int index = 0)`: Determines whether the recipe contains the specified variable at the given register index.
- `int Remove(U data, int index = -1)`: Removes all items matching the specified variable and optionally a specific register index.
- `T[] ToDistinctList()`: Returns a deduplicated array of setup items, removing duplicates by RtdeSetupItem%601.Data and RtdeSetupItem%601.Index.

## RtdeSetupItem<T>

`abstract class RtdeSetupItem<T> where T : Enum`

Abstract base class representing a single RTDE variable in a recipe, identified by an enum value of type T and an optional register index.

- `RtdeSetupItem()`: Initializes a new empty instance.
- `RtdeSetupItem(T data)`: Initializes a new instance for the specified RTDE variable.
- `RtdeSetupItem(T data, int index)`: Initializes a new instance for the specified RTDE variable and register index.
- `T Data { get; set; }`: Gets or sets the enum value identifying the RTDE variable.
- `abstract RtdeDataDescription<T> Description { get; }`: Gets the description metadata for this variable (name, type, array info).
- `int Index { get; set; }`: Gets or sets the register index for array/register RTDE variables. Defaults to 0.
- `string Name { get; }`: Gets the RTDE protocol name for this variable, including the register index suffix for array variables.
- `string ProtocolType { get; }`: Gets the uppercase RTDE protocol type string sent on the wire during setup.
- `RtdeTypes Type { get; }`: Gets the RTDE wire type of this variable.
