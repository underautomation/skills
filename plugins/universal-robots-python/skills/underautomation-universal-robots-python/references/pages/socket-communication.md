# Socket communication

Exchange your own messages with a UR robot program through the socket functions of URScript. The SDK is the socket server.

Web page: https://underautomation.com/universal-robots/documentation/socket-communication

With the socket functions of URScript, a program that runs on a Universal Robots cobot connects to your application and exchanges text and numbers with it. This page shows the socket server of the SDK: it listens on a port of the PC, 50001 by default, and raises an event for each message of a robot.

## How it works

The robot program opens the connection with `socket_open`, then sends and receives messages. On the PC, the SDK raises an event for each step:

| URScript of the robot                  | Event of the SDK             | Your code                                       |
| -------------------------------------- | ---------------------------- | ----------------------------------------------- |
| `socket_open("192.168.0.10", 50001)`   | `SocketClientConnection`     | Keep the client, send it a first message        |
| `socket_send_string("Hello")`          | `SocketRequest`              | Read `Message`                                  |
| `value := socket_get_var("COUNTER")`   | `SocketGetVar`               | Set `Value`, an integer, sent back to the robot |
| `socket_read_string()`                 | none                         | Send with `SocketWrite`                         |
| `socket_close()`                       | `SocketClientDisconnection`  |                                                 |

`192.168.0.10` is the address of the PC. See [TCP/IP socket communication via URScript](https://www.universal-robots.com/articles/ur/interface-communication/tcpip-socket-communication-via-urscript/) by Universal Robots.

```ruby
socket_open("192.168.0.10", 50001)
socket_send_string("Hello")
counter := socket_get_var("COUNTER")
reply := socket_read_string()
socket_close()
```

The program [socket_sample.urp](https://github.com/underautomation/UniversalRobots.NET/raw/main/UnderAutomation.UniversalRobots.Showcase.Forms/Samples/socket_sample.urp) uses these functions.

## Example

The socket server is disabled by default: set `SocketCommunication.Enable` in `ConnectParameters`.

```python
from underautomation.universal_robots.ur import UR
from underautomation.universal_robots.connect_parameters import ConnectParameters
from underautomation.universal_robots.socket_communication.socket_client_connection_event_args import SocketClientConnectionEventArgs
from underautomation.universal_robots.socket_communication.socket_request_event_args import SocketRequestEventArgs
from underautomation.universal_robots.socket_communication.socket_get_var_event_args import SocketGetVarEventArgs
from underautomation.universal_robots.socket_communication.socket_client_disconnection_event_args import SocketClientDisconnectionEventArgs

robot = UR()

parameters = ConnectParameters("192.168.0.1")

# The socket server is disabled by default
parameters.socket_communication.enable = True
parameters.socket_communication.port = 50001

robot.connect(parameters)

# URScript: socket_open("192.168.0.10", 50001)
def on_connection(sender, e):
    SocketClientConnectionEventArgs(e._instance).client.socket_write("Welcome")

# URScript: socket_send_string("Hello")
def on_request(sender, e):
    request = SocketRequestEventArgs(e._instance)
    print(request.client.end_point, "says", request.message)

# URScript: value := socket_get_var("COUNTER")
def on_get_var(sender, e):
    request = SocketGetVarEventArgs(e._instance)
    if request.name == "COUNTER":
        request.value = 12  # integer only

# URScript: socket_close()
def on_disconnection(sender, e):
    print(SocketClientDisconnectionEventArgs(e._instance).client.end_point, "disconnected")

robot.socket_communication.socket_client_connection(on_connection)
robot.socket_communication.socket_request(on_request)
robot.socket_communication.socket_get_var(on_get_var)
robot.socket_communication.socket_client_disconnection(on_disconnection)

# Send a message to every connected robot
robot.socket_communication.socket_write("Start")

# Or to one robot
for client in robot.socket_communication.connected_clients:
    client.socket_write(f"Hello {client.end_point}")
```

The same server works without `UR`:

```python
from underautomation.universal_robots.socket_communication.socket_communication_server import SocketCommunicationServer
from underautomation.universal_robots.socket_communication.socket_request_event_args import SocketRequestEventArgs

# A socket server, without a UR instance
server = SocketCommunicationServer()

def on_request(sender, e):
    request = SocketRequestEventArgs(e._instance)
    print(request.client.end_point, "says", request.message)

server.socket_request(on_request)

server.start(50001)

# ...

server.stop()
```

Several robots can connect to the same server: `ConnectedClients` lists them, and each `SocketClient` has its own `SocketWrite`. Allow the port of the server in the firewall of the PC.

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**SocketCommunicationServerBase** ([reference](../api/underautomation.universal_robots.socket_communication.internal.md#socketcommunicationserverbase-robotsocket_communication))

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
- Inherited from [URServiceBase](../api/underautomation.universal_robots.internal.md#urservicebase-robot): `internal_error_occured`

**SocketClient** ([reference](../api/underautomation.universal_robots.socket_communication.md#socketclient))

- `socket_get_var(handler)`: Event raised when the robot calls socket_get_var()
- `socket_request(handler)`: Event raised when a message is received from robot
- `socket_client_disconnection(handler)`: Event handler when the robot socket disconnects
- `disconnect() -> None`: Closes socket communication to robot
- `socket_write(message: str) -> None`: Write a socket message to the robot. The robot should be connected with socket_open()
- `connected: bool (read only)`: Indicates that robot socket is still active
- `end_point: typing.Any`: IP address and remote port used by the robot for socket communication

**SocketClientConnectionEventArgs** ([reference](../api/underautomation.universal_robots.socket_communication.md#socketclientconnectioneventargs))

- `client: SocketClient`: Robot remote endpoint

**SocketRequestEventArgs** ([reference](../api/underautomation.universal_robots.socket_communication.md#socketrequesteventargs))

- `message: str`: Message content received from robot
- `client: SocketClient`: Robot IP information

**SocketGetVarEventArgs** ([reference](../api/underautomation.universal_robots.socket_communication.md#socketgetvareventargs))

- `client: SocketClient`: Robot remote endpoint
- `name: str`: Name of requested variable
- `value: int | None`: Variable value to send to the robot. If value is null, no messsage is replied to the robot

**SocketClientDisconnectionEventArgs** ([reference](../api/underautomation.universal_robots.socket_communication.md#socketclientdisconnectioneventargs))

- `client: SocketClient`: Robot remote endpoint

## What to read next

- [XML-RPC](xml-rpc.md): the robot program calls a function of the PC and waits for its answer.
- [Read and write registers](registers.md): exchange numbers without a server.
