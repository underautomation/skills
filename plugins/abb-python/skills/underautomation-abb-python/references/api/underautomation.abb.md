# underautomation.abb

## AbbController

`from underautomation.abb.abb_controller import AbbController`

Main class of the SDK that represents a connection to an ABB robot controller

- `AbbController()`: Instantiate a new ABB robot controller connection
- `connect(ip_or_parameters: str | ConnectionParameters) -> None`: Connect to robot by IP with default connection parameters Initialize a connection to the robot with specified parameters
- `disconnect() -> None`: Disconnect from the robot controller
- `static discover(timeoutMilliseconds: int=2000) -> typing.List[DiscoveredController]`: Search the local network for ABB robot controllers, during the given time. Two ways of finding a controller run together: the announcements the controllers of the network send, and a test of the ports this machine serves, which is what finds the virtual controllers of RobotStudio whatever port th...
- `static register_license(licensee: str, key: str) -> LicenseInfo`: If you have a license and a key, please call this static method to register the product and exit the trial period. You can register a product even if the trial period has ended.
- `address: str (read only)`: IP or robot name
- `enabled: bool (read only)`: Check if the robot controller is connected
- `rws: RwsClientInternal (read only)`: RWS client providing access to Robot Web Services API (controller, panel, IO, RAPID, file system, subscriptions)
- `static license_info: LicenseInfo (read only)`: Return information about your license

## ConnectionParameters

`from underautomation.abb.connection_parameters import ConnectionParameters`

Connection parameters for an ABB robot controller

- `ConnectionParameters(address: str)`: Instantiate new connection parameters with a specified address
- `address: str`: Address of the robot controller (IP or host name), default value is 127.0.0.1
- `ping_before_connect: bool`: Send a ping command before initializing any connections
- `rws: RwsConnectParameters`: RWS2 (Robot Web Services 2) connection parameters
