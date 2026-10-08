# UnderAutomation.UniversalRobots

## ConnectParameters

`class ConnectParameters`

Contains parameters to connect to the robot

- `ConnectParameters()`: Initializes a new instance of UniversalRobots.ConnectParameters with default values.
- `ConnectParameters(string ip)`: Initializes a new instance of UniversalRobots.ConnectParameters with the specified robot IP address.
- `DashboardConnectParameters Dashboard { get; set; }`: Dashboard Server connection parameters (port 29999).
- `string IP { get; set; }`: IP address of the Universal Robots controller.
- `InterpreterModeConnectParameters InterpreterMode { get; set; }`: Interpreter Mode connection parameters for sending URScript lines interactively.
- `bool PingBeforeConnecting { get; set; }`: If true, a ping is sent to the robot before attempting connection. Default is true.
- `PrimaryInterfaceConnectParameters PrimaryInterface { get; set; }`: Primary Interface connection parameters (port 30001/30002).
- `RestConnectParameters Rest { get; set; }`: REST API connection parameters (PolyscopeX only)
- `RtdeConnectParameters Rtde { get; set; }`: Real-Time Data Exchange (RTDE) connection parameters (port 30004).
- `SocketCommunicationConnectParameters SocketCommunication { get; set; }`: Socket communication connection parameters for exchanging data with URScript programs.
- `SshConnectParameters Ssh { get; set; }`: SSH and SFTP connection parameters for file transfer and remote shell access.
- `XmlRpcConnectParameters XmlRpc { get; set; }`: XML-RPC connection parameters for remote procedure calls.

## UR

`class UR : URServiceBase`

Main entry point for connecting to and interacting with a Universal Robots controller. Provides access to all communication interfaces: Primary Interface, Dashboard, RTDE, SSH, SFTP, XML-RPC, Socket Communication, Interpreter Mode, and REST API.

- `UR()`: Initializes a new instance of the UniversalRobots.UR class and creates all communication clients.
- `void Connect(string ip)`: Connects to a robot with default parameters
- `void Connect(ConnectParameters parameters)`: Connects to a robot with specific parameters
- `DashboardClientInternal Dashboard { get; }`: Interact with robot via Dashboard
- `void Disconnect()`: Disconnects all clients and disable all services
- `bool Enabled { get; }`: Indicates that at least one of the implemented services is enabled
- `string IP { get; }`: Robot IP address, null is robot is disconnected
- `InterpreterModeClientInternal InterpreterMode { get; }`: Interact with robot via Interpreter Mode
- `static LicenseInfo LicenseInfo { get; }`: Return information about your license
- `PrimaryInterfaceClientInternal PrimaryInterface { get; }`: Interact with robot via Primary Interface
- `static LicenseInfo RegisterLicense(string licensee, string key)`: If you have a license and a key, please call this static method to register the product and exit the trial period You can register a product even if the trial period has ended
- `RestClientInternal Rest { get; }`: Interact with robot via REST API (PolyscopeX only)
- `RtdeClientInternal Rtde { get; }`: Interact with robot via RTDE
- `SftpClientInternal Sftp { get; }`: Interact with robot via SFTP
- `SocketCommunicationServerInternal SocketCommunication { get; }`: Interact with robot via Socket communication
- `SshClientInternal Ssh { get; }`: Interact with robot via SSH
- `XmlRpcServerInternal XmlRpc { get; }`: Interact with robot via XML-RPC
- Inherited from [URServiceBase](UnderAutomation.UniversalRobots.Internal.md#urservicebase-robot): `InternalErrorOccured`
