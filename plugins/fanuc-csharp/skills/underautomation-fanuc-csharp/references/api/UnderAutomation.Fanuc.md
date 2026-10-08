# UnderAutomation.Fanuc

## ConnectionParameters

`class ConnectionParameters`

Connection parameters

- `ConnectionParameters()`: Instanciate a new connection parameters
- `ConnectionParameters(string address)`: Instanciate a new connection parameters with a specified address
- `string Address { get; set; }`: Address of the robot (IP, host name, or path to ROBOGUIDE project folder)
- `CgtpConnectParameters Cgtp { get; set; }`: Parameters of the CGTP client, which uses the web server of the controller (HTTP)
- `FtpConnectParameters Ftp { get; set; }`: Access controller internal memory to read variables, IO, positions, diagnosis, ...
- `Languages Language { get; set; }`: Controller language (default: English)
- `bool PingBeforeConnect { get; set; }`: Send a ping command before initializing any connections
- `RmiConnectParameters Rmi { get; set; }`: Parameters for RMI (Remote Motion Interface)
- `SnpxConnectParameters Snpx { get; set; }`: Read and write IOs, read and clear alarms, read current program tasks
- `StreamMotionConnectParameters StreamMotion { get; set; }`: Parameters for Stream Motion (J519 option) - real-time streaming motion control over UDP
- `TelnetConnectParameters Telnet { get; set; }`: Parameters of the Telnet KCL client, which sends commands to the robot for remote control. Telnet KCL is a legacy protocol: it is not secured (password and commands are sent in clear text), and its behavior changes with the firmware version and on ROBOGUIDE. The same KCL commands are available on...

## FanucRobot

`class FanucRobot`

Main class of the SDK that represents a connection to a Fanuc robot

- `FanucRobot()`: Instanciate a new Fanuc robot connection
- `string Address { get; }`: IP or robot name
- `CgtpClientInternal Cgtp { get; }`: CGTP client, which uses the web server of the controller (HTTP)
- `void Connect(string ip)`: Connect to robot by IP with default connection parameters
- `void Connect(ConnectionParameters parameters)`: Initialize a conenction to the robot with specified parameters
- `void Disconnect()`: Disconnect all services connected to the robot
- `bool Enabled { get; }`: Indicates whether any service is currently connected to the robot
- `FtpClientInternal Ftp { get; }`: FTP client for memory and file access
- `static LicenseInfo LicenseInfo { get; }`: Return information about your license
- `static LicenseInfo RegisterLicense(string licensee, string key)`: If you have a license And a key, please call this static method to register the product And exit the trial period ou can register a product even if the trial period has ended
- `RmiClientInternal Rmi { get; }`: RMI client for remote motion interface
- `SnpxClientInternal Snpx { get; }`: SNPX client for IO, alarms and task reading
- `StreamMotionClientInternal StreamMotion { get; }`: Stream Motion client for real-time motion control
- `TelnetClientInternal Telnet { get; }`: Telnet KCL client for remote command execution. Telnet KCL is a legacy protocol: it is not secured (password and commands are sent in clear text), and its behavior changes with the firmware version and on ROBOGUIDE. The same KCL commands are available on the web server of the controller with robo...
