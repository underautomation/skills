# UnderAutomation.ABB

## AbbController

`class AbbController`

Main class of the SDK that represents a connection to an ABB robot controller

- `AbbController()`: Instantiate a new ABB robot controller connection
- `string Address { get; }`: IP or robot name
- `void Connect(string ip)`: Connect to robot by IP with default connection parameters
- `void Connect(ConnectionParameters parameters)`: Initialize a connection to the robot with specified parameters
- `void Disconnect()`: Disconnect from the robot controller
- `static DiscoveredController[] Discover(int timeoutMilliseconds = 2000)`: Search the local network for ABB robot controllers, during the given time. Two ways of finding a controller run together: the announcements the controllers of the network send, and a test of the ports this machine serves, which is what finds the virtual controllers of RobotStudio whatever port th...
  - async: `static Task<DiscoveredController[]> DiscoverAsync(int timeoutMilliseconds = 2000, CancellationToken cancellationToken = default)`
- `bool Enabled { get; }`: Check if the robot controller is connected
- `static LicenseInfo LicenseInfo { get; }`: Return information about your license
- `static LicenseInfo RegisterLicense(string licensee, string key)`: If you have a license and a key, please call this static method to register the product and exit the trial period. You can register a product even if the trial period has ended.
- `RwsClientInternal Rws { get; }`: RWS client providing access to Robot Web Services API (controller, panel, IO, RAPID, file system, subscriptions)

## ConnectionParameters

`class ConnectionParameters`

Connection parameters for an ABB robot controller

- `ConnectionParameters()`: Instantiate new connection parameters with default values
- `ConnectionParameters(string address)`: Instantiate new connection parameters with a specified address
- `string Address { get; set; }`: Address of the robot controller (IP or host name), default value is 127.0.0.1
- `bool PingBeforeConnect { get; set; }`: Send a ping command before initializing any connections
- `RwsConnectParameters Rws { get; set; }`: RWS2 (Robot Web Services 2) connection parameters
