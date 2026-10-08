# UnderAutomation.UniversalRobots.Internal

## DashboardClientInternal (robot.Dashboard)

`class DashboardClientInternal : DashboardClientBase`

Internal implementation of the Dashboard Server client that delegates connection to the parent UniversalRobots.UR instance.

- `void Enable(int port = 29999, int receiveTimeoutMs = 2000, int sendTimeoutMs = 500)`: Enable Dashboard client connection
- Inherited from [DashboardClientBase](UnderAutomation.UniversalRobots.Dashboard.Internal.md#dashboardclientbase-robotdashboard): `BeforeShutdown`, `Disable`, `LoadProgram`, `Play`, `Stop`, `Pause`, `SendCustomDashboardCommand`, `GetVariable`, `Shutdown`, `IsProgramRunning`, `GetRobotMode`, `GetLoadedProgram`, `ShowPopup`, `ClosePopup`, `AddToLog`, `IsProgramSaved`, `GetProgramState`, `GetPolyscopeVersion`, `SetUserRole`, `SetOperationalMode`, `ClearOperationalMode`, `GetOperationalMode`, `IsInRemoteControl`, `PowerOn`, `PowerOff`, `ReleaseBrake`, `UnlockProtectiveStop`, `CloseSafetyPopup`, `LoadInstallation`, `RestartSafety`, `GetSafetyStatus`, `GetSerialNumber`, `GetRobotModel`, `IP`, `Port`, `ReceiveTimeoutMs`, `SendTimeoutMs`, `Initialized`
- Inherited from [URServiceBase](UnderAutomation.UniversalRobots.Internal.md#urservicebase-robot): `InternalErrorOccured`

## InterpreterModeClientInternal (robot.InterpreterMode)

`class InterpreterModeClientInternal : InterpreterModeClientBase`

Internal implementation of the Interpreter Mode client that delegates connection to the parent UniversalRobots.UR instance.

- `void Connect(int port = 30020)`: Enable Interpreter Mode client connection
- Inherited from [InterpreterModeClientBase](UnderAutomation.UniversalRobots.InterpreterMode.Internal.md#interpretermodeclientbase-robotinterpretermode): `ExecuteCommand`, `EndInterpreter`, `ClearInterpreter`, `Abort`, `SkipBuffer`, `StateLastExecuted`, `StateLastInterpreted`, `StateLastCleared`, `StateLastUnexecuted`, `Disconnect`, `IP`, `Port`, `Connected`
- Inherited from [URServiceBase](UnderAutomation.UniversalRobots.Internal.md#urservicebase-robot): `InternalErrorOccured`

## PrimaryInterfaceClientInternal (robot.PrimaryInterface)

`class PrimaryInterfaceClientInternal : PrimaryInterfaceClientBase`

Internal implementation of the Primary Interface client that delegates connection to the parent UniversalRobots.UR instance.

- `void Connect()`: Connect to primary interface
- `void Connect(Interfaces port)`: Connect to a specific interface
- Inherited from [PrimaryInterfaceClientBase](UnderAutomation.UniversalRobots.PrimaryInterface.Internal.md#primaryinterfaceclientbase-robotprimaryinterface): `Disconnect`, `RobotModeData`, `JointData`, `ToolData`, `MasterboardData`, `CartesianInfo`, `KinematicsInfo`, `ConfigurationData`, `ForceModeData`, `AdditionalInfo`, `CalibrationData`, `SafetyData`, `ToolCommunicationInfo`, `ToolModeInfo`, `SingularityInfo`, `ProgramThreads`, `Version`, `KeyMessage`, `PopupMessage`, `TextMessage`, `RuntimeExceptionMessage`, `GlobalVariables`, `Script`, `Commands`, `IP`, `Port`, `Connected`, `LocalEndPoint`, `RobotModeDataReceived`, `JointDataReceived`, `ToolDataReceived`, `MasterboardDataReceived`, `CartesianInfoReceived`, `KinematicsInfoReceived`, `ConfigurationDataReceived`, `ForceModeDataReceived`, `AdditionalInfoReceived`, `CalibrationDataReceived`, `SafetyDataReceived`, `ToolCommunicationInfoReceived`, `ToolModeInfoReceived`, `SingularityInfoReceived`, `PackageReceived`, `RawPackageReceived`, `ProgramThreadsReceived`, `VersionReceived`, `KeyMessageReceived`, `PopupMessageReceived`, `TextMessageReceived`, `RuntimeExceptionMessageReceived`
- Inherited from [URServiceBase](UnderAutomation.UniversalRobots.Internal.md#urservicebase-robot): `InternalErrorOccured`

## RestClientInternal (robot.Rest)

`class RestClientInternal : RestClientBase`

Internal REST client for use within the UR class

- `void Enable(int port = 80, RestApiVersion version = RestApiVersion.Latest, int timeoutMs = 5000)`: Enable REST client connection using the IP from the parent UR instance
- Inherited from [RestClientBase](UnderAutomation.UniversalRobots.Rest.Internal.md#restclientbase-robotrest): `Disable`, `ChangeRobotState`, `UnlockProtectiveStop`, `RestartSafety`, `PowerOff`, `PowerOn`, `BrakeRelease`, `LoadProgram`, `ChangeProgramState`, `Play`, `Pause`, `Stop`, `Resume`, `GetProgramState`, `IP`, `Port`, `Version`, `TimeoutMs`, `Initialized`
- Inherited from [URServiceBase](UnderAutomation.UniversalRobots.Internal.md#urservicebase-robot): `InternalErrorOccured`

## RtdeClientInternal (robot.Rtde)

`class RtdeClientInternal : RtdeClientBase`

Internal implementation of the Real-Time Data Exchange (RTDE) client that delegates connection to the parent UniversalRobots.UR instance.

- `void Connect(RtdeOutputSetup outputSetup, RtdeInputSetup inputSetup, RtdeVersions version, double frequency, int port)`: Connects to the RTDE interface on the robot controller.
- Inherited from [RtdeClientBase](UnderAutomation.UniversalRobots.Rtde.Internal.md#rtdeclientbase-robotrtde): `Pause`, `Resume`, `WriteInputs`, `Disconnect`, `LastTextMessage`, `State`, `Connected`, `IP`, `AppliedFrequency`, `Version`, `OutputSetup`, `InputSetup`, `OutputRecipeId`, `InputRecipeId`, `InputRecipeIsValid`, `MeasuredFrequency`, `OutputDataValues`, `ProtocolVersionReceived`, `TextMessageReceived`, `OutputDataReceived`, `SetupOutputsReceived`, `SetupInputsReceived`, `StartReceived`, `PauseReceived`, `PackageReceived`
- Inherited from [URServiceBase](UnderAutomation.UniversalRobots.Internal.md#urservicebase-robot): `InternalErrorOccured`

## RtdeOverrunException

`class RtdeOverrunException : Exception, ISerializable`

Exception thrown when RTDE data cannot be consumed fast enough, causing the input buffer to fill up. This typically occurs when the OutputDataReceived event handler takes longer to execute than the interval between RTDE messages.

- `RtdeOverrunException()`: Initializes a new instance of the Internal.RtdeOverrunException class with a default diagnostic message.

## SftpClientInternal (robot.Sftp)

`class SftpClientInternal : SftpClientBase`

Implementation of the SSH File Transfer Protocol (SFTP) over SSH for transfering files to the robot controller

- `void Connect(int port, string username, string password)`: Connects to Sftp robot server
- Inherited from [SftpClientBase](UnderAutomation.UniversalRobots.Ssh.Internal.md#sftpclientbase-robotsftp): `Disconnect`, `ChangeDirectory`, `ChangePermissions`, `CreateDirectory`, `DeleteDirectory`, `DeleteFile`, `RenameFile`, `SymbolicLink`, `ListDirectory`, `EnumeratePrograms`, `EnumerateInstallations`, `BeginListDirectory`, `EndListDirectory`, `Get`, `Exists`, `DownloadFile`, `BeginDownloadFile`, `EndDownloadFile`, `UploadFile`, `BeginUploadFile`, `EndUploadFile`, `GetStatus`, `AppendAllLines`, `AppendAllText`, `AppendText`, `Create`, `CreateText`, `Delete`, `GetLastAccessTime`, `GetLastAccessTimeUtc`, `GetLastWriteTime`, `GetLastWriteTimeUtc`, `Open`, `OpenRead`, `OpenText`, `OpenWrite`, `ReadAllBytes`, `ReadAllLines`, `ReadAllText`, `ReadLines`, `WriteAllBytes`, `WriteAllLines`, `WriteAllText`, `GetAttributes`, `SetAttributes`, `SynchronizeDirectories`, `BeginSynchronizeDirectories`, `EndSynchronizeDirectories`, `Connected`, `OperationTimeout`, `BufferSize`, `WorkingDirectory`, `ProtocolVersion`
- Inherited from [URServiceBase](UnderAutomation.UniversalRobots.Internal.md#urservicebase-robot): `InternalErrorOccured`

## SocketCommunicationServerInternal (robot.SocketCommunication)

`class SocketCommunicationServerInternal : SocketCommunicationServerBase, ISocketHandler`

Internal implementation of the socket communication server used for bidirectional data exchange with UR scripts.

- Inherited from [SocketCommunicationServerBase](UnderAutomation.UniversalRobots.SocketCommunication.Internal.md#socketcommunicationserverbase-robotsocketcommunication): `Start`, `Stop`, `SocketWrite`, `ConnectedClients`, `Enabled`, `Port`, `SocketClientConnection`, `SocketGetVar`, `SocketRequest`, `SocketClientDisconnection`
- Inherited from [URServiceBase](UnderAutomation.UniversalRobots.Internal.md#urservicebase-robot): `InternalErrorOccured`

## SshClientInternal (robot.Ssh)

`class SshClientInternal : SshClientBase`

Provides a client connection to SSH server

- `void Connect(int port, string username, string password)`: Connects to the SSH robot server
- Inherited from [SshClientBase](UnderAutomation.UniversalRobots.Ssh.Internal.md#sshclientbase-robotssh): `Disconnect`, `CreateCommand`, `RunCommand`, `CreateShell`, `CreateShellStream`, `Connected`
- Inherited from [URServiceBase](UnderAutomation.UniversalRobots.Internal.md#urservicebase-robot): `InternalErrorOccured`

## URServiceBase (robot)

`abstract class URServiceBase`

Base class of all UR services implemented in this SDK

- `event EventHandler<InternalErrorEventArgs> InternalErrorOccured`: Event raised when an error occured

## XmlRpcServerInternal (robot.XmlRpc)

`class XmlRpcServerInternal : XmlRpcServerBase`

Internal implementation of the XML-RPC server used to expose methods callable by URScript programs on the robot.

- Inherited from [XmlRpcServerBase](UnderAutomation.UniversalRobots.XmlRpc.Internal.md#xmlrpcserverbase-robotxmlrpc): `Start`, `Stop`, `Enabled`, `Port`, `XmlRpcServerRequest`
- Inherited from [URServiceBase](UnderAutomation.UniversalRobots.Internal.md#urservicebase-robot): `InternalErrorOccured`
