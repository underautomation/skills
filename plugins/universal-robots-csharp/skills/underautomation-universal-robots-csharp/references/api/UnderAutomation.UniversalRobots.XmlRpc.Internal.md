# UnderAutomation.UniversalRobots.XmlRpc.Internal

## XmlRpcParametersBase

`abstract class XmlRpcParametersBase`

Base class for XML-RPC connection parameters.

- `int Port { get; set; }`: Choose local port to start XML-RPC server Default value is 50000

## XmlRpcServerBase.XmlRpcServerRequestEventHandler

`delegate void XmlRpcServerBase.XmlRpcServerRequestEventHandler(object sender, XmlRpcEventArg request)`

Event raised when a XML-RPC request is sent by the robot and received.

- `XmlRpcServerRequestEventHandler(object @object, nint method)`
- `IAsyncResult BeginInvoke(object sender, XmlRpcEventArg request, AsyncCallback callback, object @object)`
- `void EndInvoke(IAsyncResult result)`
- `void Invoke(object sender, XmlRpcEventArg request)`

## XmlRpcServerBase (robot.XmlRpc)

`abstract class XmlRpcServerBase : URServiceBase`

Base class providing XML-RPC server functionality for receiving remote procedure calls from a Universal Robots controller.

- `bool Enabled { get; }`: Is the XML-RPC server enabled
- `int Port { get; }`: Local port on which the XML-RPC server is running. 0 if server is disabled
- `void Start(int port)`: Enable the local XML-RPC server to receive commands from the robot
- `void Stop()`: Disable and close the socket used for the XML-RPC server
- `event XmlRpcServerBase.XmlRpcServerRequestEventHandler XmlRpcServerRequest`: Event raised when a XML-RPC request has been sent from the robot to this machine. You should answer to the robot in this event via the property request.Answer
- Inherited from [URServiceBase](UnderAutomation.UniversalRobots.Internal.md#urservicebase-robot): `InternalErrorOccured`
