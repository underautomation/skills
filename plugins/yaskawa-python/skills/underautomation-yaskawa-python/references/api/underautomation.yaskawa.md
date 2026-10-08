# underautomation.yaskawa

## ConnectParameters

`from underautomation.yaskawa.connect_parameters import ConnectParameters`

Contains a set of connection parameters for robot communication. Supports High Speed Ethernet Server and Host Control protocols.

- `ConnectParameters(ip: str)`: Creates a new set of connect parameters and defines IP property
- `ping_before_connect: bool`: Send a ping command before connecting
- `ip: str`: IP Adress or robot host name
- `high_speed_e_server: HighSpeedEServerConnectParametersInternal`: High Speed Ethernet Server connect parameters
- `e_server: EServerConnectParametersInternal`: Ethernet Server connect parameters. Used for TCP-based Host Control communication via Ethernet Server.
- `http: HttpConnectParametersInternal`: HTTP connect parameters. Used for file listing and file content retrieval via the robot's built-in web server.
- `ftp: FtpConnectParametersInternal`: FTP connect parameters. Used for file upload, download, listing and management via the robot's built-in FTP server.

## YaskawaRobot

`from underautomation.yaskawa.yaskawa_robot import YaskawaRobot`

Main entry point for communicating with Yaskawa Motoman robots. This class provides methods to connect, monitor, and control the robot through multiple interfaces: High Speed Ethernet Server, Ethernet Server (Host Control over TCP), HTTP and FTP.

- `YaskawaRobot()`: Creates a new Yaskawa robot instance
- `connect(ip_or_parameters: str | ConnectParameters) -> None`: Connects to the robot by its IP address. Establishes the connection of each protocol enabled by default in ConnectParameters. Connects to the robot using the specified parameters. Establishes the connection of each protocol enabled in the parameters.
- `disconnect() -> None`: Disconnects all active connections to the robot controller.
- `static register_license(Licensee: str, key: str) -> LicenseInfo`: If you have a license And a key, please call this static method to register the product And exit the trial period ou can register a product even if the trial period has ended
- `connected: bool (read only)`: Indicates whether any communication interface (High Speed Ethernet Server, Ethernet Server, HTTP or FTP) is currently connected.
- `high_speed_e_server: HighSpeedEServerClientInternal (read only)`: Access High Speed Ethernet Server features. Provides high-speed UDP-based communication for real-time robot monitoring and control.
- `e_server: EServerClientInternal (read only)`: Access Host Control features via Ethernet Server (TCP). Supports YRC1000 and compatible controllers. Connected automatically when calling Connect() with EServer.Enable = true.
- `http: HttpClientInternal (read only)`: Access HTTP features for file listing and file content retrieval. Communicates with the robot controller's built-in web server. Connected automatically when calling Connect() with Http.Enable = true.
- `ftp: FtpClientInternal (read only)`: Access FTP features for file upload, download, listing, and management. Communicates with the robot controller's built-in FTP server. Connected automatically when calling Connect() with Ftp.Enable = true.
- `static license_info: LicenseInfo (read only)`: Return information about your license
