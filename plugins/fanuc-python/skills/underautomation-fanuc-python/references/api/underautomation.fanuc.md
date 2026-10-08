# underautomation.fanuc

## ConnectionParameters

`from underautomation.fanuc.connection_parameters import ConnectionParameters`

Connection parameters

- `ConnectionParameters(address: str)`: Instanciate a new connection parameters with a specified address
- `address: str`: Address of the robot (IP, host name, or path to ROBOGUIDE project folder)
- `ping_before_connect: bool`: Send a ping command before initializing any connections
- `language: Languages`: Controller language (default: English)
- `telnet: TelnetConnectParameters`: Sends commands to the robot for remote control
- `ftp: FtpConnectParameters`: Access controller internal memory to read variables, IO, positions, diagnosis, ...
- `snpx: SnpxConnectParameters`: Read and write IOs, read and clear alarms, read current program tasks
- `rmi: RmiConnectParameters`: Parameters for RMI (Remote Motion Interface)
- `stream_motion: StreamMotionConnectParameters`: Parameters for Stream Motion (J519 option) - real-time streaming motion control over UDP
- `cgtp: CgtpConnectParameters`: Parameters for CGTP Web Server (HTTP-based COMET RPC interface)

## FanucRobot

`from underautomation.fanuc.fanuc_robot import FanucRobot`

Main class of the SDK that represents a connection to a Fanuc robot

- `FanucRobot()`: Instanciate a new Fanuc robot connection
- `connect(ip_or_parameters: str | ConnectionParameters) -> None`: Connect to robot by IP with default connection parameters Initialize a conenction to the robot with specified parameters
- `disconnect() -> None`: Disconnect all services connected to the robot
- `static register_license(licensee: str, key: str) -> LicenseInfo`: If you have a license And a key, please call this static method to register the product And exit the trial period ou can register a product even if the trial period has ended
- `address: str (read only)`: IP or robot name
- `enabled: bool (read only)`: Indicates whether any service is currently connected to the robot
- `telnet: TelnetClientInternal (read only)`: Telnet client for remote command execution
- `ftp: FtpClientInternal (read only)`: FTP client for memory and file access
- `snpx: SnpxClientInternal (read only)`: SNPX client for IO, alarms and task reading
- `rmi: RmiClientInternal (read only)`: RMI client for remote motion interface
- `stream_motion: StreamMotionClientInternal (read only)`: Stream Motion client for real-time motion control
- `cgtp: CgtpClientInternal (read only)`: CGTP Web Server client for HTTP-based COMET RPC interface
- `static license_info: LicenseInfo (read only)`: Return information about your license
