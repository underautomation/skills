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

```csharp
using UnderAutomation.UniversalRobots;
using UnderAutomation.UniversalRobots.SocketCommunication;

class Socket
{
  static void Main(string[] args)
  {
    var robot = new UR();

    var parameters = new ConnectParameters("192.168.0.1");

    // The socket server is disabled by default
    parameters.SocketCommunication.Enable = true;
    parameters.SocketCommunication.Port = 50001;

    robot.Connect(parameters);

    // URScript: socket_open("192.168.0.10", 50001)
    robot.SocketCommunication.SocketClientConnection += (sender, e) =>
    {
      e.Client.SocketWrite("Welcome");
    };

    // URScript: socket_send_string("Hello")
    robot.SocketCommunication.SocketRequest += (sender, e) =>
    {
      Console.WriteLine(e.Client.EndPoint.Address + " says " + e.Message);
    };

    // URScript: value := socket_get_var("COUNTER")
    robot.SocketCommunication.SocketGetVar += (sender, e) =>
    {
      if (e.Name == "COUNTER") e.Value = 12; // integer only
    };

    // URScript: socket_close()
    robot.SocketCommunication.SocketClientDisconnection += (sender, e) =>
    {
      Console.WriteLine(e.Client.EndPoint + " disconnected");
    };

    // Send a message to every connected robot
    robot.SocketCommunication.SocketWrite("Start");

    // Or to one robot
    foreach (SocketClient client in robot.SocketCommunication.ConnectedClients)
      client.SocketWrite("Hello " + client.EndPoint.Address);
  }
}
```

The same server works without `UR`:

```csharp
using UnderAutomation.UniversalRobots.SocketCommunication;

class SocketDirect
{
  static void Main(string[] args)
  {
    // A socket server, without a UR instance
    var server = new SocketCommunicationServer();

    server.SocketRequest += (sender, e) =>
    {
      Console.WriteLine(e.Client.EndPoint.Address + " says " + e.Message);
    };

    server.Start(50001);

    // ...

    server.Stop();
  }
}
```

Several robots can connect to the same server: `ConnectedClients` lists them, and each `SocketClient` has its own `SocketWrite`. Allow the port of the server in the firewall of the PC.

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**SocketCommunicationServerBase** ([reference](../api/UnderAutomation.UniversalRobots.SocketCommunication.Internal.md#socketcommunicationserverbase-robotsocketcommunication))

- `SocketCommunicationServerBase()`
- `SocketClient[] ConnectedClients { get; }`: List of all connected clients. One robot can open multiple sockets.
- `bool Enabled { get; }`: Is the socket server enabled
- `int Port { get; }`: Socket server local port
- `event SocketCommunicationServerBase.SocketClientConnectionEventHandler SocketClientConnection`: Event raised when a robot connects with URScript function socket_open()
- `event SocketCommunicationServerBase.SocketClientDisconnectionEventHandler SocketClientDisconnection`: Event raised when the robot socket disconnects
- `event SocketCommunicationServerBase.SocketGetVarEventHandler SocketGetVar`: Event raised when the robot calls socket_get_var()
- `event SocketCommunicationServerBase.SocketRequestEventHandler SocketRequest`: Event raised when a message is received from robot
- `void SocketWrite(string message)`: Write a socket message to the robot. The robot should be connected with socket_open()
- `void Start(int port)`: Starts socket server. Robot can connect with URScript function socket_open()
- `void Stop()`: Disable local socket server and disconnect all connected clients
- Inherited from [URServiceBase](../api/UnderAutomation.UniversalRobots.Internal.md#urservicebase-robot): `InternalErrorOccured`

**SocketClient** ([reference](../api/UnderAutomation.UniversalRobots.SocketCommunication.md#socketclient))

- `bool Connected { get; }`: Indicates that robot socket is still active
- `void Disconnect()`: Closes socket communication to robot
- `readonly IPEndPoint EndPoint`: IP address and remote port used by the robot for socket communication
- `event SocketCommunicationServerBase.SocketClientDisconnectionEventHandler SocketClientDisconnection`: Event handler when the robot socket disconnects
- `event SocketCommunicationServerBase.SocketGetVarEventHandler SocketGetVar`: Event raised when the robot calls socket_get_var()
- `event SocketCommunicationServerBase.SocketRequestEventHandler SocketRequest`: Event raised when a message is received from robot
- `void SocketWrite(string message)`: Write a socket message to the robot. The robot should be connected with socket_open()

**SocketClientConnectionEventArgs** ([reference](../api/UnderAutomation.UniversalRobots.SocketCommunication.md#socketclientconnectioneventargs))

- `readonly SocketClient Client`: Robot remote endpoint

**SocketRequestEventArgs** ([reference](../api/UnderAutomation.UniversalRobots.SocketCommunication.md#socketrequesteventargs))

- `readonly SocketClient Client`: Robot IP information
- `readonly string Message`: Message content received from robot

**SocketGetVarEventArgs** ([reference](../api/UnderAutomation.UniversalRobots.SocketCommunication.md#socketgetvareventargs))

- `readonly SocketClient Client`: Robot remote endpoint
- `readonly string Name`: Name of requested variable
- `int? Value`: Variable value to send to the robot. If value is null, no messsage is replied to the robot

**SocketClientDisconnectionEventArgs** ([reference](../api/UnderAutomation.UniversalRobots.SocketCommunication.md#socketclientdisconnectioneventargs))

- `readonly SocketClient Client`: Robot remote endpoint

## What to read next

- [XML-RPC](xml-rpc.md): the robot program calls a function of the PC and waits for its answer.
- [Read and write registers](registers.md): exchange numbers without a server.
