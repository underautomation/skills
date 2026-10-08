# underautomation.universal_robots.socket_communication.internal

## SocketCommunicationParametersBase

`from underautomation.universal_robots.socket_communication.internal.socket_communication_parameters_base import SocketCommunicationParametersBase`

Base parameters for socket communication server configuration

- `SocketCommunicationParametersBase()`
- `port: int`: Local port for socket server (default : 50001)

## SocketCommunicationServerBase (robot.socket_communication)

`from underautomation.universal_robots.socket_communication.internal.socket_communication_server_base import SocketCommunicationServerBase`

Base for Socket communication server

- `SocketCommunicationServerBase()`
- `socket_client_connection(handler)`: Event raised when a robot connects with URScript function socket_open()
- `socket_get_var(handler)`: Event raised when the robot calls socket_get_var()
- `socket_request(handler)`: Event raised when a message is received from robot
- `socket_client_disconnection(handler)`: Event raised when the robot socket disconnects
- `start(port: int) -> None`: Starts socket server. Robot can connect with URScript function socket_open()
- `stop() -> None`: Disable local socket server and disconnect all connected clients
- `socket_write(message: str) -> None`: Write a socket message to the robot. The robot should be connected with socket_open()
- `connected_clients: typing.List[SocketClient] (read only)`: List of all connected clients. One robot can open multiple sockets.
- `enabled: bool (read only)`: Is the socket server enabled
- `port: int (read only)`: Socket server local port
- Inherited from [URServiceBase](underautomation.universal_robots.internal.md#urservicebase-robot): `internal_error_occured`
