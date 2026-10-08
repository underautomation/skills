# UnderAutomation.UniversalRobots.SocketCommunication

## ISocketHandler

`interface ISocketHandler`

Interface for classes that support socket messages

- `event SocketCommunicationServerBase.SocketClientDisconnectionEventHandler SocketClientDisconnection`: Event raised when the robot socket disconnects
- `event SocketCommunicationServerBase.SocketGetVarEventHandler SocketGetVar`: Event raised when the robot calls socket_get_var()
- `event SocketCommunicationServerBase.SocketRequestEventHandler SocketRequest`: Event raised when a message is received from robot
- `void SocketWrite(string message)`: Write a socket message to the robot. The robot should be connected with socket_open()

## SocketClient

`class SocketClient : ISocketHandler`

Represent a UR robot connected with URScript function socket_open()

- `bool Connected { get; }`: Indicates that robot socket is still active
- `void Disconnect()`: Closes socket communication to robot
- `readonly IPEndPoint EndPoint`: IP address and remote port used by the robot for socket communication
- `event SocketCommunicationServerBase.SocketClientDisconnectionEventHandler SocketClientDisconnection`: Event handler when the robot socket disconnects
- `event SocketCommunicationServerBase.SocketGetVarEventHandler SocketGetVar`: Event raised when the robot calls socket_get_var()
- `event SocketCommunicationServerBase.SocketRequestEventHandler SocketRequest`: Event raised when a message is received from robot
- `void SocketWrite(string message)`: Write a socket message to the robot. The robot should be connected with socket_open()

## SocketClientConnectionEventArgs

`class SocketClientConnectionEventArgs : EventArgs`

Event args raised when a socket client is connected with socket_open()

- `readonly SocketClient Client`: Robot remote endpoint

## SocketClientDisconnectionEventArgs

`class SocketClientDisconnectionEventArgs : EventArgs`

Event args raised when a socket client disconnects

- `readonly SocketClient Client`: Robot remote endpoint

## SocketCommunicationServer

`class SocketCommunicationServer : SocketCommunicationServerBase, ISocketHandler`

Represents a Socket Communication server to which the robot can connect

- `SocketCommunicationServer()`
- Inherited from [SocketCommunicationServerBase](UnderAutomation.UniversalRobots.SocketCommunication.Internal.md#socketcommunicationserverbase-robotsocketcommunication): `Start`, `Stop`, `SocketWrite`, `ConnectedClients`, `Enabled`, `Port`, `SocketClientConnection`, `SocketGetVar`, `SocketRequest`, `SocketClientDisconnection`
- Inherited from [URServiceBase](UnderAutomation.UniversalRobots.Internal.md#urservicebase-robot): `InternalErrorOccured`

## SocketGetVarEventArgs

`class SocketGetVarEventArgs : EventArgs`

Event args raised when a socket message sent with socket_get_var() is received

- `readonly SocketClient Client`: Robot remote endpoint
- `readonly string Name`: Name of requested variable
- `int? Value`: Variable value to send to the robot. If value is null, no messsage is replied to the robot

## SocketRequestEventArgs

`class SocketRequestEventArgs : EventArgs`

Event args raised when a socket message is received

- `readonly SocketClient Client`: Robot IP information
- `readonly string Message`: Message content received from robot
