# underautomation.universal_robots.socket_communication

## ISocketHandler

`from underautomation.universal_robots.socket_communication.i_socket_handler import ISocketHandler`

Interface for classes that support socket messages

- `socket_get_var(handler)`: Event raised when the robot calls socket_get_var()
- `socket_request(handler)`: Event raised when a message is received from robot
- `socket_client_disconnection(handler)`: Event raised when the robot socket disconnects
- `socket_write(message: str) -> None`: Write a socket message to the robot. The robot should be connected with socket_open()

## SocketClient

`from underautomation.universal_robots.socket_communication.socket_client import SocketClient`

Represent a UR robot connected with URScript function socket_open()

- `socket_get_var(handler)`: Event raised when the robot calls socket_get_var()
- `socket_request(handler)`: Event raised when a message is received from robot
- `socket_client_disconnection(handler)`: Event handler when the robot socket disconnects
- `disconnect() -> None`: Closes socket communication to robot
- `socket_write(message: str) -> None`: Write a socket message to the robot. The robot should be connected with socket_open()
- `connected: bool (read only)`: Indicates that robot socket is still active
- `end_point: typing.Any`: IP address and remote port used by the robot for socket communication

## SocketClientConnectionEventArgs

`from underautomation.universal_robots.socket_communication.socket_client_connection_event_args import SocketClientConnectionEventArgs`

Event args raised when a socket client is connected with socket_open()

- `client: SocketClient`: Robot remote endpoint

## SocketClientDisconnectionEventArgs

`from underautomation.universal_robots.socket_communication.socket_client_disconnection_event_args import SocketClientDisconnectionEventArgs`

Event args raised when a socket client disconnects

- `client: SocketClient`: Robot remote endpoint

## SocketCommunicationServer

`from underautomation.universal_robots.socket_communication.socket_communication_server import SocketCommunicationServer`

Represents a Socket Communication server to which the robot can connect

- `SocketCommunicationServer()`
- Inherited from [SocketCommunicationServerBase](underautomation.universal_robots.socket_communication.internal.md#socketcommunicationserverbase-robotsocket_communication): `start`, `stop`, `socket_write`, `connected_clients`, `enabled`, `port`, `socket_client_connection`, `socket_get_var`, `socket_request`, `socket_client_disconnection`
- Inherited from [URServiceBase](underautomation.universal_robots.internal.md#urservicebase-robot): `internal_error_occured`

## SocketGetVarEventArgs

`from underautomation.universal_robots.socket_communication.socket_get_var_event_args import SocketGetVarEventArgs`

Event args raised when a socket message sent with socket_get_var() is received

- `client: SocketClient`: Robot remote endpoint
- `name: str`: Name of requested variable
- `value: int | None`: Variable value to send to the robot. If value is null, no messsage is replied to the robot

## SocketRequestEventArgs

`from underautomation.universal_robots.socket_communication.socket_request_event_args import SocketRequestEventArgs`

Event args raised when a socket message is received

- `message: str`: Message content received from robot
- `client: SocketClient`: Robot IP information
