# underautomation.universal_robots.xml_rpc.internal

## XmlRpcParametersBase

`from underautomation.universal_robots.xml_rpc.internal.xml_rpc_parameters_base import XmlRpcParametersBase`

Base class for XML-RPC connection parameters.

- `port: int`: Choose local port to start XML-RPC server Default value is 50000

## XmlRpcServerBase (robot.xml_rpc)

`from underautomation.universal_robots.xml_rpc.internal.xml_rpc_server_base import XmlRpcServerBase`

Base class providing XML-RPC server functionality for receiving remote procedure calls from a Universal Robots controller.

- `xml_rpc_server_request(handler)`: Event raised when a XML-RPC request has been sent from the robot to this machine. You should answer to the robot in this event via the property request.Answer
- `start(port: int) -> None`: Enable the local XML-RPC server to receive commands from the robot
- `stop() -> None`: Disable and close the socket used for the XML-RPC server
- `enabled: bool (read only)`: Is the XML-RPC server enabled
- `port: int (read only)`: Local port on which the XML-RPC server is running. 0 if server is disabled
- Inherited from [URServiceBase](underautomation.universal_robots.internal.md#urservicebase-robot): `internal_error_occured`
