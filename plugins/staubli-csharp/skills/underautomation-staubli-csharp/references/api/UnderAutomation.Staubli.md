# UnderAutomation.Staubli

## ConnectionParameters

`class ConnectionParameters`

Connection parameters

- `ConnectionParameters()`: Instanciate a new connection parameters
- `ConnectionParameters(string address)`: Instanciate a new connection parameters with a specified address
- `string Address { get; set; }`: Address of the robot: IP or host name of a real controller. For a controller emulated by Staubli Robotics Suite, path of the .controller file of the controller in the cell (for example C:\...\MyCell\Controller1\Controller1.controller): the SOAP client then connects to the local computer, and the...
- `FileConnectParameters File { get; set; }`: File client connection parameters (upload, download, listing and management of the files of the controller)
- `bool PingBeforeConnect { get; set; }`: Send a ping command before initializing any connections
- `SoapConnectParameters Soap { get; set; }`: Soap connection parameters

## StaubliController

`class StaubliController`

Main class of the SDK that represents a connection to a Staubli robot controller

- `StaubliController()`: Instanciate a new Staubli robot controller connection
- `string Address { get; }`: IP or robot name, or path of the .controller file of a controller emulated by Staubli Robotics Suite
- `void Connect(string ip)`: Connect to robot by IP with default connection parameters
- `void Connect(ConnectionParameters parameters)`: Initialize a conenction to the robot with specified parameters
- `void Disconnect()`: Disconnect all services connected to the robot
- `bool Enabled { get; }`: Check if the robot is connected
- `FileClientInternal File { get; }`: File client: upload, download, listing and management of the files of the controller. Uses the FTP server of a real controller, or the folder of the .controller file of a controller emulated by Staubli Robotics Suite. The VAL 3 applications are in the folder "/usr/usrapp": robot.File.UploadApplic...
- `static LicenseInfo LicenseInfo { get; }`: Return information about your license
- `static LicenseInfo RegisterLicense(string licensee, string key)`: If you have a license And a key, please call this static method to register the product And exit the trial period ou can register a product even if the trial period has ended
- `SoapClientInternal Soap { get; }`: Internal SOAP client used to communicate with the robot controller.
