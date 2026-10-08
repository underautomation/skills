# underautomation.staubli

## ConnectionParameters

`from underautomation.staubli.connection_parameters import ConnectionParameters`

Connection parameters

- `ConnectionParameters(address: str)`: Instanciate a new connection parameters with a specified address
- `address: str`: Address of the robot: IP or host name of a real controller. For a controller emulated by Staubli Robotics Suite, path of the .controller file of the controller in the cell (for example C:\...\MyCell\Controller1\Controller1.controller): the SOAP client then connects to the local computer, and the...
- `ping_before_connect: bool`: Send a ping command before initializing any connections
- `soap: SoapConnectParameters`: Soap connection parameters
- `file: FileConnectParameters`: File client connection parameters (upload, download, listing and management of the files of the controller)

## StaubliController

`from underautomation.staubli.staubli_controller import StaubliController`

Main class of the SDK that represents a connection to a Staubli robot controller

- `StaubliController()`: Instanciate a new Staubli robot controller connection
- `connect(ip_or_parameters: str | ConnectionParameters) -> None`: Connect to robot by IP with default connection parameters Initialize a conenction to the robot with specified parameters
- `disconnect() -> None`: Disconnect all services connected to the robot
- `static register_license(licensee: str, key: str) -> LicenseInfo`: If you have a license And a key, please call this static method to register the product And exit the trial period ou can register a product even if the trial period has ended
- `address: str (read only)`: IP or robot name, or path of the .controller file of a controller emulated by Staubli Robotics Suite
- `enabled: bool (read only)`: Check if the robot is connected
- `soap: SoapClientInternal (read only)`: Internal SOAP client used to communicate with the robot controller.
- `file: FileClientInternal (read only)`: File client: upload, download, listing and management of the files of the controller. Uses the FTP server of a real controller, or the folder of the .controller file of a controller emulated by Staubli Robotics Suite. The VAL 3 applications are in the folder "/usr/usrapp": robot.File.UploadApplic...
- `static license_info: LicenseInfo (read only)`: Return information about your license
