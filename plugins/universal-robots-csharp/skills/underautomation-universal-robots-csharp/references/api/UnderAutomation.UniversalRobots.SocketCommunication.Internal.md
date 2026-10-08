# UnderAutomation.UniversalRobots.SocketCommunication.Internal

## SocketCommunicationParametersBase

`class SocketCommunicationParametersBase`

Base parameters for socket communication server configuration

- `SocketCommunicationParametersBase()`
- `int Port { get; set; }`: Local port for socket server (default : 50001)

## SocketCommunicationServerBase.SocketClientConnectionEventHandler

`delegate void SocketCommunicationServerBase.SocketClientConnectionEventHandler(object sender, SocketClientConnectionEventArgs request)`

Event handler of a robot that connects with socket_open()

- `SocketClientConnectionEventHandler(object @object, nint method)`
- `IAsyncResult BeginInvoke(object sender, SocketClientConnectionEventArgs request, AsyncCallback callback, object @object)`
- `void EndInvoke(IAsyncResult result)`
- `void Invoke(object sender, SocketClientConnectionEventArgs request)`

## SocketCommunicationServerBase.SocketClientDisconnectionEventHandler

`delegate void SocketCommunicationServerBase.SocketClientDisconnectionEventHandler(object sender, SocketClientDisconnectionEventArgs request)`

Event handler when the robot socket disconnects

- `SocketClientDisconnectionEventHandler(object @object, nint method)`
- `IAsyncResult BeginInvoke(object sender, SocketClientDisconnectionEventArgs request, AsyncCallback callback, object @object)`
- `void EndInvoke(IAsyncResult result)`
- `void Invoke(object sender, SocketClientDisconnectionEventArgs request)`

## SocketCommunicationServerBase.SocketGetVarEventHandler

`delegate void SocketCommunicationServerBase.SocketGetVarEventHandler(object sender, SocketGetVarEventArgs request)`

Event handler of a socket message sent with socket_get_var()

- `SocketGetVarEventHandler(object @object, nint method)`
- `IAsyncResult BeginInvoke(object sender, SocketGetVarEventArgs request, AsyncCallback callback, object @object)`
- `void EndInvoke(IAsyncResult result)`
- `void Invoke(object sender, SocketGetVarEventArgs request)`

## SocketCommunicationServerBase.SocketRequestEventHandler

`delegate void SocketCommunicationServerBase.SocketRequestEventHandler(object sender, SocketRequestEventArgs request)`

Event handler of a socket message received from robot

- `SocketRequestEventHandler(object @object, nint method)`
- `IAsyncResult BeginInvoke(object sender, SocketRequestEventArgs request, AsyncCallback callback, object @object)`
- `void EndInvoke(IAsyncResult result)`
- `void Invoke(object sender, SocketRequestEventArgs request)`

## SocketCommunicationServerBase (robot.SocketCommunication)

`class SocketCommunicationServerBase : URServiceBase, ISocketHandler`

Base for Socket communication server

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
- Inherited from [URServiceBase](UnderAutomation.UniversalRobots.Internal.md#urservicebase-robot): `InternalErrorOccured`
