# UnderAutomation.UniversalRobots.PrimaryInterface.Internal

## PrimaryInterfaceClientBase (robot.PrimaryInterface)

`class PrimaryInterfaceClientBase : URServiceBase`

Base class for the Primary/Secondary Interface client. Manages the TCP connection, decodes incoming binary data packets, and raises events for each decoded sub-package.

- `AdditionalInfoPackageEventArgs AdditionalInfo { get; }`: Last additional information received
- `event EventHandler<AdditionalInfoPackageEventArgs> AdditionalInfoReceived`: Additional (Raised every 100ms)
- `CalibrationDataPackageEventArgs CalibrationData { get; }`: Last calibration data received
- `event EventHandler<CalibrationDataPackageEventArgs> CalibrationDataReceived`: Calibration data (Raised every 100ms)
- `CartesianInfoPackageEventArgs CartesianInfo { get; }`: Last cartesian information received
- `event EventHandler<CartesianInfoPackageEventArgs> CartesianInfoReceived`: Cartesian inforlation (Raised every 100ms)
- `PrimaryInterfaceCommands Commands { get; }`: Contains methods to send commands to the robot
- `ConfigurationDataPackageEventArgs ConfigurationData { get; }`: Last configuration data received
- `event EventHandler<ConfigurationDataPackageEventArgs> ConfigurationDataReceived`: Configuration data (Raised when connection opened)
- `bool Connected { get; }`: Return True if the connection to the robot is active
- `void Disconnect()`: Stops data streaming and the possibility to send scripts to the robot.
- `ForceModeDataPackageEventArgs ForceModeData { get; }`: Last force mode data received
- `event EventHandler<ForceModeDataPackageEventArgs> ForceModeDataReceived`: Force mode data (Raised every 100ms)
- `GlobalVariables GlobalVariables { get; }`: List of all variables in current robot program
- `string IP { get; }`: IP address of the connected robot
- `JointDataPackageEventArgs JointData { get; }`: Last joint data received
- `event EventHandler<JointDataPackageEventArgs> JointDataReceived`: Joint data (Raised every 100ms)
- `KeyMessageEventArgs KeyMessage { get; }`: Internal robot events (such as starting or stopping a program)
- `event EventHandler<KeyMessageEventArgs> KeyMessageReceived`: Internal robot events (such as starting or stopping a program)
- `KinematicsInfoPackageEventArgs KinematicsInfo { get; }`: Last kinematics information received
- `event EventHandler<KinematicsInfoPackageEventArgs> KinematicsInfoReceived`: Kinematics information data (Raised when connection opened)
- `IPEndPoint LocalEndPoint { get; }`: Indicates the current local endpoint (i.e. IP Address) used to communicate with the robot. You can use this IP in your UR script in the function rpc_factory()
- `MasterboardDataPackageEventArgs MasterboardData { get; }`: Last masterboard data received
- `event EventHandler<MasterboardDataPackageEventArgs> MasterboardDataReceived`: Masterboard data (Raised every 100ms)
- `event EventHandler<PackageEventArgs> PackageReceived`: Generic event raised each time a package is received
- `PopupMessageEventArgs PopupMessage { get; }`: Popup message that appears with the Assignment instruction or the URScript popup() function
- `event EventHandler<PopupMessageEventArgs> PopupMessageReceived`: Popup message that appears with the Assignment instruction or the URScript popup() function
- `Interfaces Port { get; }`: Interface used for the connected robot
- `ProgramThreadsEventArgs ProgramThreads { get; }`: Last program thread information received
- `event EventHandler<ProgramThreadsEventArgs> ProgramThreadsReceived`: Program threads changed
- `event EventHandler<RawPackageReceivedEventArgs> RawPackageReceived`: Generic event raised for each raw package received
- `RobotModeDataPackageEventArgs RobotModeData { get; }`: Last Robot mode data received
- `event EventHandler<RobotModeDataPackageEventArgs> RobotModeDataReceived`: Robot mode data (Raised every 100ms)
- `RuntimeExceptionMessageEventArgs RuntimeExceptionMessage { get; }`: Reports an error in the execution of the program
- `event EventHandler<RuntimeExceptionMessageEventArgs> RuntimeExceptionMessageReceived`: Reports an error in the execution of the program
- `SafetyDataPackageEventArgs SafetyData { get; }`: Last safety data received
- `event EventHandler<SafetyDataPackageEventArgs> SafetyDataReceived`: Safety data (Raised every 100ms)
- `PrimaryInterfaceScript Script { get; }`: Contains methods to send custom URScript to the robot
- `SingularityInfoPackageEventArgs SingularityInfo { get; }`: Last singularity information information received
- `event EventHandler<SingularityInfoPackageEventArgs> SingularityInfoReceived`: Singularity information (Raised every 100ms)
- `TextMessageEventArgs TextMessage { get; }`: Log message sent with URScript instruction textmsg()
- `event EventHandler<TextMessageEventArgs> TextMessageReceived`: Log message sent with URScript instruction textmsg()
- `ToolCommunicationInfoPackageEventArgs ToolCommunicationInfo { get; }`: Last tool communication information received
- `event EventHandler<ToolCommunicationInfoPackageEventArgs> ToolCommunicationInfoReceived`: Tool communication information (Raised every 100ms)
- `ToolDataPackageEventArgs ToolData { get; }`: Last tool data received
- `event EventHandler<ToolDataPackageEventArgs> ToolDataReceived`: Tool data (Raised every 100ms)
- `ToolModeInfoPackageEventArgs ToolModeInfo { get; }`: Last tool mode information received
- `event EventHandler<ToolModeInfoPackageEventArgs> ToolModeInfoReceived`: Tool mode information (Raised every 100ms)
- `VersionEventArgs Version { get; }`: Version of the robot and FW
- `event EventHandler<VersionEventArgs> VersionReceived`: Robot information and FW version
- Inherited from [URServiceBase](UnderAutomation.UniversalRobots.Internal.md#urservicebase-robot): `InternalErrorOccured`

## PrimaryInterfaceCommands (robot.PrimaryInterface.Commands)

`class PrimaryInterfaceCommands`

Handles Primary interface commands

- `StatusCode AddBreakpoint(int line, string program)`: Add a new breakpoint
- `StatusCode ClearBreakpoints()`: Clear all breakpoints
- `StatusCode ClosePopup(uint id)`: Close popup
- `StatusCode DisableFreedriveMode()`: Disable freedrive mode
- `StatusCode DisableTeachButton()`: Disable teach button
- `StatusCode EnableFreedriveMode()`: Enable freedrive mode
- `StatusCode EnableTeachButton()`: Enable teach button
- `StatusCode IncreaseSpeedLimit()`: Increase speed limit
- `StatusCode PauseProgram()`: Pause running program
- `StatusCode PowerOff()`: Power off the robot
- `StatusCode PowerOn()`: Power on the robot
- `StatusCode ReleaseBrakes()`: Release brakes
- `StatusCode RemoveBreakpoint(int line, string program)`: Remove an existing breakpoint
- `StatusCode ReplyPopup(uint id, bool value)`: Reply popup
- `StatusCode ReplyPopup(uint id, double value)`: Reply popup
- `StatusCode ReplyPopup(uint id, int value)`: Reply popup
- `StatusCode ReplyPopup(uint id, string value)`: Reply popup
- `StatusCode ReplyPopup(uint id, string value, RequestedTypes type)`: Reply popup
- `StatusCode ResumeProgram()`: Resume paused program
- `StatusCode RunProgram()`: Run program from start
- `StatusCode SetOperationalMode(OperationalModes mode)`: Set robot operational mode
- `StatusCode SetReal()`: Set robot to real robot (disable simulation)
- `StatusCode SetSimulated()`: Simulate robot
- `StatusCode SetSpeed(double value)`: Set speed
- `StatusCode SetSpeedLimit(double value)`: Set speed limit
- `StatusCode StepProgram()`: Step program execution. Should be followed by ResumeProgram() to move to next instruction
- `StatusCode StopProgram()`: Stop running program
- `void Test()`: Sends a test HMC expression parse command to the robot (for internal debugging).
- `StatusCode UnlockProtectiveStop()`: Unlock protective stop

## PrimaryInterfaceParametersBase

`abstract class PrimaryInterfaceParametersBase`

Parameters to setup a Primary/secondary interface connection

- `Interfaces Port { get; set; }`: Interface on which to connect

## PrimaryInterfaceScript (robot.PrimaryInterface.Script)

`class PrimaryInterfaceScript`

Handles Primary interface send script feature

- `StatusCode Send(string script)`: Remotely execute script.Please see the Universal Robot Script documentation : https://www.universal-robots.com/download/.

## RawPackageReceivedEventArgs

`class RawPackageReceivedEventArgs : PackageEventArgs`

Event args for raw package received

- `RawPackageReceivedEventArgs(byte[] data, DateTime receiveDate, byte type)`: Initializes a new instance with the raw packet data, receive timestamp, and package type.
- `byte[] Data { get; }`: Full raw packet data (including header)
- `byte Type { get; }`: Package Type
- Inherited from [PackageEventArgs](UnderAutomation.UniversalRobots.Common.md#packageeventargs-robotprimaryinterfacerobotmodedata): `ReceiveDate`
