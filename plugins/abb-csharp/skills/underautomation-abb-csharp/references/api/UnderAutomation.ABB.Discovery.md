# UnderAutomation.ABB.Discovery

## DiscoveredController

`class DiscoveredController`

An ABB robot controller found on the local network. Returned by Discover(System.Int32).

- `string Address { get; }`: IPv4 address of the controller
- `string InstanceName { get; }`: Full name the controller publishes on the network. It contains DiscoveredController.SystemName. Null when the controller did not announce itself.
- `bool IsVersionDetected { get; }`: True when DiscoveredController.ProbableVersion is more than a guess. It is always true for a controller found by testing the ports of this machine, because the controller was asked. For a controller heard announcing itself, it is false when the announcement did not carry what the version is deduc...
- `int PcSdkPort { get; }`: Port of the PC SDK interface of the controller, or 0 when the controller does not publish it. This SDK does not use that interface, the value is given for information.
- `int Port { get; }`: Port the Robot Web Services interface listens on. A virtual controller gets a new port from RobotStudio at every start, so this value is the reason to discover the controller instead of writing the port down.
- `RwsVersion ProbableVersion { get; }`: RWS version this controller most probably speaks. This is deduced from what the controller publishes, not from a request sent to it. Check DiscoveredController.IsVersionDetected before relying on it.
- `string RobotWareVersion { get; }`: RobotWare version of the controller, for example "7.21.0". Null when the controller does not publish it. Only OmniCore controllers do.
- `string SystemId { get; }`: Unique identifier of the robot system. Null when the controller does not publish it. Only OmniCore controllers do.
- `string SystemName { get; }`: Name of the robot system, as configured on the controller. Null when the controller was found by testing the ports of this machine rather than by hearing it announce itself, because a port tells nothing about the name.
- `ConnectionParameters ToConnectionParameters()`: Build connection parameters pointing at this controller, ready for ABB.ConnectionParameters). The address, the port, the scheme and the RWS version come from the discovery. The user name and the password keep their default values, change them if the controller needs other ones.
- `bool UseHttps { get; }`: True when the controller serves Robot Web Services over HTTPS. OmniCore controllers use HTTPS, IRC5 controllers use HTTP.
