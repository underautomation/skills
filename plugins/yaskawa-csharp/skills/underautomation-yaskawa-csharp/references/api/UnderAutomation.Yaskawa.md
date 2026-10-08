# UnderAutomation.Yaskawa

## ConnectParameters

`class ConnectParameters`

Contains a set of connection parameters for robot communication. Supports High Speed Ethernet Server and Host Control protocols.

- `ConnectParameters()`: Creates a new set of connect parameters
- `ConnectParameters(string ip)`: Creates a new set of connect parameters and defines IP property
- `EServerConnectParametersInternal EServer { get; set; }`: Ethernet Server connect parameters. Used for TCP-based Host Control communication via Ethernet Server.
- `FtpConnectParametersInternal Ftp { get; set; }`: FTP connect parameters. Used for file upload, download, listing and management via the robot's built-in FTP server.
- `HighSpeedEServerConnectParametersInternal HighSpeedEServer { get; set; }`: High Speed Ethernet Server connect parameters
- `HttpConnectParametersInternal Http { get; set; }`: HTTP connect parameters. Used for file listing and file content retrieval via the robot's built-in web server.
- `string IP { get; set; }`: IP Adress or robot host name
- `bool PingBeforeConnect { get; set; }`: Send a ping command before connecting

## YaskawaRobot

`class YaskawaRobot`

Main entry point for communicating with Yaskawa Motoman robots. This class provides methods to connect, monitor, and control the robot through multiple interfaces: High Speed Ethernet Server, Ethernet Server (Host Control over TCP), HTTP and FTP.

- `YaskawaRobot()`: Creates a new Yaskawa robot instance
- `void Connect(string ip)`: Connects to the robot by its IP address. Establishes the connection of each protocol enabled by default in Yaskawa.ConnectParameters.
- `void Connect(ConnectParameters parameters)`: Connects to the robot using the specified parameters. Establishes the connection of each protocol enabled in the parameters.
- `bool Connected { get; }`: Indicates whether any communication interface (High Speed Ethernet Server, Ethernet Server, HTTP or FTP) is currently connected.
- `void Disconnect()`: Disconnects all active connections to the robot controller.
- `EServerClientInternal EServer { get; }`: Access Host Control features via Ethernet Server (TCP). Supports YRC1000 and compatible controllers. Connected automatically when calling Connect() with EServer.Enable = true.
- `FtpClientInternal Ftp { get; }`: Access FTP features for file upload, download, listing, and management. Communicates with the robot controller's built-in FTP server. Connected automatically when calling Connect() with Ftp.Enable = true.
- `HighSpeedEServerClientInternal HighSpeedEServer { get; }`: Access High Speed Ethernet Server features. Provides high-speed UDP-based communication for real-time robot monitoring and control.
- `HttpClientInternal Http { get; }`: Access HTTP features for file listing and file content retrieval. Communicates with the robot controller's built-in web server. Connected automatically when calling Connect() with Http.Enable = true.
- `static LicenseInfo LicenseInfo { get; }`: Return information about your license
- `static LicenseInfo RegisterLicense(string Licensee, string key)`: If you have a license And a key, please call this static method to register the product And exit the trial period ou can register a product even if the trial period has ended
