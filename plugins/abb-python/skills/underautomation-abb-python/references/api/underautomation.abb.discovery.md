# underautomation.abb.discovery

## DiscoveredController

`from underautomation.abb.discovery.discovered_controller import DiscoveredController`

An ABB robot controller found on the local network. Returned by .

- `to_connection_parameters() -> ConnectionParameters`: Build connection parameters pointing at this controller, ready for connect(). The address, the port, the scheme and the RWS version come from the discovery. The user name and the password keep their default values, change them if the controller needs other ones.
- `system_name: str (read only)`: Name of the robot system, as configured on the controller. Null when the controller was found by testing the ports of this machine rather than by hearing it announce itself, because a port tells nothing about the name.
- `instance_name: str (read only)`: Full name the controller publishes on the network. It contains system_name. Null when the controller did not announce itself.
- `address: str (read only)`: IPv4 address of the controller
- `port: int (read only)`: Port the Robot Web Services interface listens on. A virtual controller gets a new port from RobotStudio at every start, so this value is the reason to discover the controller instead of writing the port down.
- `robot_ware_version: str (read only)`: RobotWare version of the controller, for example "7.21.0". Null when the controller does not publish it. Only OmniCore controllers do.
- `system_id: str (read only)`: Unique identifier of the robot system. Null when the controller does not publish it. Only OmniCore controllers do.
- `pc_sdk_port: int (read only)`: Port of the PC SDK interface of the controller, or 0 when the controller does not publish it. This SDK does not use that interface, the value is given for information.
- `probable_version: RwsVersion (read only)`: RWS version this controller most probably speaks. This is deduced from what the controller publishes, not from a request sent to it. Check before relying on it.
- `is_version_detected: bool (read only)`: True when probable_version is more than a guess. It is always true for a controller found by testing the ports of this machine, because the controller was asked. For a controller heard announcing itself, it is false when the announcement did not carry what the version is deduced from, and then ho...
- `use_https: bool (read only)`: True when the controller serves Robot Web Services over HTTPS. OmniCore controllers use HTTPS, IRC5 controllers use HTTP.
