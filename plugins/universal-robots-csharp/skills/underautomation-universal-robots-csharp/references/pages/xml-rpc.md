# XML-RPC

Answer the XML-RPC calls of a UR robot program from your application: positions, numbers, text. The SDK is the server.

Web page: https://underautomation.com/universal-robots/documentation/xml-rpc

With XML-RPC, a program that runs on a Universal Robots cobot calls a function of your application and uses its answer: a position computed by a vision system, a number, a text. This page shows how to answer these calls with the SDK. The SDK is the server: it listens on a port of the PC, 50000 by default.

## How it works

1. The robot program creates a connection to the PC with `rpc_factory`.
2. It calls a function of this connection. The robot waits for the answer.
3. The SDK raises `XmlRpcServerRequest` with the name of the function and its arguments. Your code sets `Answer`.
4. The robot assigns the answer to its variable, and the program continues.

URScript of the robot, where `192.168.0.10` is the address of the PC:

```ruby
rpc := rpc_factory("xmlrpc", "http://192.168.0.10:50000")

pose := rpc.get_pose()
text := rpc.say_hello("UR5e")
total := rpc.sum([1, 3.5, -2])
```

See [XML-RPC communication](https://www.universal-robots.com/articles/ur/interface-communication/xml-rpc-communication/) by Universal Robots. The address of the PC on the network of the robot is also in `robot.PrimaryInterface.LocalEndPoint`.

## Example

The XML-RPC server is disabled by default: set `XmlRpc.Enable` in `ConnectParameters`.

```csharp
using UnderAutomation.UniversalRobots;
using UnderAutomation.UniversalRobots.Common;
using UnderAutomation.UniversalRobots.XmlRpc;

class XmlRpc
{
  static void Main(string[] args)
  {
    var robot = new UR();

    var parameters = new ConnectParameters("192.168.0.1");

    // The XML-RPC server is disabled by default
    parameters.XmlRpc.Enable = true;
    parameters.XmlRpc.Port = 50000;

    robot.Connect(parameters);

    // Raised for each call of the robot program
    robot.XmlRpc.XmlRpcServerRequest += OnRequest;
  }

  // The robot program connects with:
  //   rpc := rpc_factory("xmlrpc", "http://192.168.0.10:50000")
  // where 192.168.0.10 is the address of this PC
  static void OnRequest(object sender, XmlRpcEventArg request)
  {
    Console.WriteLine(request.EndPoint.Address + " calls " + request.MethodName);

    switch (request.MethodName)
    {
      // URScript: answer := rpc.get_pose()
      case "get_pose":
        request.Answer = new Pose(0.4, -0.1, 0.3, 0, 3.14, 0); // m and rad
        break;

      // URScript: answer := rpc.say_hello("UR5e")
      case "say_hello":
        request.Answer = "Hello " + request.Arguments[0];
        break;

      // URScript: answer := rpc.sum([1, 3.5, -2])
      case "sum":
        double[] values = request.Arguments[0];
        request.Answer = values.Sum();
        break;

      // Without an answer, the variable of the robot is not assigned
      default:
        break;
    }
  }
}
```

The same server works without `UR`:

```csharp
using UnderAutomation.UniversalRobots.XmlRpc;

class XmlRpcDirect
{
  static void Main(string[] args)
  {
    // An XML-RPC server, without a UR instance
    var server = new XmlRpcServer();

    server.XmlRpcServerRequest += (sender, request) =>
    {
      if (request.MethodName == "get_counter")
        request.Answer = 42;
    };

    server.Start(50000);

    // ...

    server.Stop();
  }
}
```

Allow the port of the server in the firewall of the PC.

## Values

`Answer` and `Arguments` are `XmlRpcValue`. In C#, implicit conversions accept and return the native types: `request.Answer = 12`, `= 3.5`, `= true`, `= "text"`, `= new Pose(...)`, `= new double[] {...}`, and `double[] values = request.Arguments[0]`.

| URScript type | .NET class            | Python class                                    |
| ------------- | --------------------- | ----------------------------------------------- |
| integer       | `XmlRpcIntegerValue`  | `XmlRpcIntegerValue(12)`                        |
| float         | `XmlRpcDoubleValue`   | `XmlRpcDoubleValue(3.5)`                        |
| boolean       | `XmlRpcBooleanValue`  | `XmlRpcBooleanValue(True)`                      |
| string        | `XmlRpcStringValue`   | `XmlRpcStringValue("text")`                     |
| pose          | `XmlRpcPoseValue`     | `XmlRpcPoseValue(Pose(x, y, z, rx, ry, rz))`    |
| array         | `XmlRpcArrayValue`    | `XmlRpcArrayValue`                              |
| struct        | `XmlRpcStructValue`   | `XmlRpcStructValue`                             |

A value that the SDK cannot read is an `XmlRpcUnknownValue`: its `AdditionalInformation` says why.

Without an answer, the function returns nothing to the robot and its variable is not assigned.

## Example programs

### PolyScope

[xml_rpc_sample.urp](https://github.com/underautomation/UniversalRobots.NET/raw/main/UnderAutomation.UniversalRobots.Showcase.Forms/Samples/xml_rpc_sample.urp) calls several functions. The demo application shows each call and lets you choose the answer.

![XML-RPC program in PolyScope](https://underautomation.com/universal-robots/xml_rpc_sample.jpg)

![Answer of the demo application](https://underautomation.com/universal-robots/xml_rpc_winforms.jpg)

### LabVIEW

The LabVIEW example answers `GetPose()` with the position of its front panel, and a text to the other functions:

![LabVIEW front panel](https://underautomation.com/universal-robots/xmlrpc_labview_frontpanel.jpg)

![LabVIEW diagram](https://underautomation.com/universal-robots/xmlrpc_labview_diagram.jpg)

![LabVIEW callback VI](https://underautomation.com/universal-robots/xmlrpc_labview_callback.jpg)

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**XmlRpcEventArg** ([reference](../api/UnderAutomation.UniversalRobots.XmlRpc.md#xmlrpceventarg))

- `XmlRpcValue Answer`: Response to be provided to the robot by the user
- `readonly XmlRpcValue[] Arguments`: The arguments of the method called
- `readonly IPEndPoint EndPoint`: IP address of the robot
- `readonly string MethodName`: The method called by the robot
- `readonly XDocument XmlRequest`: The XML document received via HTTP

**XmlRpcValue** ([reference](../api/UnderAutomation.UniversalRobots.XmlRpc.md#xmlrpcvalue))

- `abstract XmlRpcType Type { get; }`: Determines the class of this message
- `XElement Xml { get; }`: The XML description of the message that has been received from the robot or will be sent to the robot
- `static implicit operator XmlRpcValue(bool value)`: Implicitly converts a System.Boolean to an XmlRpc.XmlRpcBooleanValue.
- `static implicit operator XmlRpcValue(bool[] value)`: Implicitly converts a System.Boolean array to an XmlRpc.XmlRpcArrayValue.
- `static implicit operator XmlRpcValue(double value)`: Implicitly converts a System.Double to an XmlRpc.XmlRpcDoubleValue.
- `static implicit operator XmlRpcValue(double[] value)`: Implicitly converts a System.Double array to an XmlRpc.XmlRpcArrayValue.
- `static implicit operator XmlRpcValue(int value)`: Implicitly converts an System.Int32 to an XmlRpc.XmlRpcIntegerValue.
- `static implicit operator XmlRpcValue(int[] value)`: Implicitly converts an System.Int32 array to an XmlRpc.XmlRpcArrayValue.
- `static implicit operator XmlRpcValue(string value)`: Implicitly converts a System.String to an XmlRpc.XmlRpcStringValue.
- `static implicit operator XmlRpcValue(string[] value)`: Implicitly converts a System.String array to an XmlRpc.XmlRpcArrayValue.
- `static implicit operator XmlRpcValue(Pose value)`: Implicitly converts a Common.Pose to an XmlRpc.XmlRpcPoseValue.
- `static implicit operator XmlRpcValue(Pose[] value)`: Implicitly converts a Common.Pose array to an XmlRpc.XmlRpcArrayValue.
- `static implicit operator bool(XmlRpcValue value)`: Implicitly converts an XmlRpc.XmlRpcValue to a System.Boolean.
- `static implicit operator bool[](XmlRpcValue value)`: Implicitly converts an XmlRpc.XmlRpcValue to a System.Boolean array.
- `static implicit operator double(XmlRpcValue value)`: Implicitly converts an XmlRpc.XmlRpcValue to a System.Double.
- `static implicit operator double[](XmlRpcValue value)`: Implicitly converts an XmlRpc.XmlRpcValue to a System.Double array.
- `static implicit operator int(XmlRpcValue value)`: Implicitly converts an XmlRpc.XmlRpcValue to an System.Int32.
- `static implicit operator int[](XmlRpcValue value)`: Implicitly converts an XmlRpc.XmlRpcValue to an System.Int32 array.
- `static implicit operator string(XmlRpcValue value)`: Implicitly converts an XmlRpc.XmlRpcValue to a System.String.
- `static implicit operator string[](XmlRpcValue value)`: Implicitly converts an XmlRpc.XmlRpcValue to a System.String array.
- `static implicit operator Pose(XmlRpcValue value)`: Implicitly converts an XmlRpc.XmlRpcValue to a Common.Pose.
- `static implicit operator Pose[](XmlRpcValue value)`: Implicitly converts an XmlRpc.XmlRpcValue to a Common.Pose array.
- `static implicit operator XmlRpcValue(XmlRpcValue[] value)`: Implicitly converts an array of XmlRpc.XmlRpcValue to an XmlRpc.XmlRpcArrayValue.

## What to read next

- [Socket communication](socket-communication.md): exchange your own messages with the robot program.
- [Read and write registers](registers.md): exchange numbers with the robot program, without waiting.
