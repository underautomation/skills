# underautomation.universal_robots

## ConnectParameters

`from underautomation.universal_robots.connect_parameters import ConnectParameters`

Contains parameters to connect to the robot

- `ConnectParameters(ip: str)`: Initializes a new instance of ConnectParameters with the specified robot IP address.
- `ip: str`: IP address of the Universal Robots controller.
- `ping_before_connecting: bool`: If true, a ping is sent to the robot before attempting connection. Default is true.
- `primary_interface: PrimaryInterfaceConnectParameters`: Primary Interface connection parameters (port 30001/30002).
- `dashboard: DashboardConnectParameters`: Dashboard Server connection parameters (port 29999).
- `socket_communication: SocketCommunicationConnectParameters`: Socket communication connection parameters for exchanging data with URScript programs.
- `ssh: SshConnectParameters`: SSH and SFTP connection parameters for file transfer and remote shell access.
- `rtde: RtdeConnectParameters`: Real-Time Data Exchange (RTDE) connection parameters (port 30004).
- `xml_rpc: XmlRpcConnectParameters`: XML-RPC connection parameters for remote procedure calls.
- `interpreter_mode: InterpreterModeConnectParameters`: Interpreter Mode connection parameters for sending URScript lines interactively.
- `rest: RestConnectParameters`: REST API connection parameters (PolyscopeX only)

## UR

`from underautomation.universal_robots.ur import UR`

Main entry point for connecting to and interacting with a Universal Robots controller. Provides access to all communication interfaces: Primary Interface, Dashboard, RTDE, SSH, SFTP, XML-RPC, Socket Communication, Interpreter Mode, and REST API.

- `UR()`: Initializes a new instance of the UR class and creates all communication clients.
- `connect(ip_or_parameters: str | ConnectParameters) -> None`: Connects to a robot with default parameters Connects to a robot with specific parameters
- `disconnect() -> None`: Disconnects all clients and disable all services
- `static register_license(licensee: str, key: str) -> LicenseInfo`: If you have a license and a key, please call this static method to register the product and exit the trial period You can register a product even if the trial period has ended
- `primary_interface: PrimaryInterfaceClientInternal (read only)`: Interact with robot via Primary Interface
- `xml_rpc: XmlRpcServerInternal (read only)`: Interact with robot via XML-RPC
- `dashboard: DashboardClientInternal (read only)`: Interact with robot via Dashboard
- `socket_communication: SocketCommunicationServerInternal (read only)`: Interact with robot via Socket communication
- `rtde: RtdeClientInternal (read only)`: Interact with robot via RTDE
- `ssh: SshClientInternal (read only)`: Interact with robot via SSH
- `sftp: SftpClientInternal (read only)`: Interact with robot via SFTP
- `interpreter_mode: InterpreterModeClientInternal (read only)`: Interact with robot via Interpreter Mode
- `rest: RestClientInternal (read only)`: Interact with robot via REST API (PolyscopeX only)
- `ip: str (read only)`: Robot IP address, null is robot is disconnected
- `enabled: bool (read only)`: Indicates that at least one of the implemented services is enabled
- `static license_info: LicenseInfo (read only)`: Return information about your license
- Inherited from [URServiceBase](underautomation.universal_robots.internal.md#urservicebase-robot): `internal_error_occured`
