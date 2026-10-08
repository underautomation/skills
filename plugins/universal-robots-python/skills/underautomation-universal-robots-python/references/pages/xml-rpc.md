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

```python
from underautomation.universal_robots.ur import UR
from underautomation.universal_robots.connect_parameters import ConnectParameters
from underautomation.universal_robots.common.pose import Pose
from underautomation.universal_robots.xml_rpc.xml_rpc_event_arg import XmlRpcEventArg
from underautomation.universal_robots.xml_rpc.xml_rpc_pose_value import XmlRpcPoseValue
from underautomation.universal_robots.xml_rpc.xml_rpc_string_value import XmlRpcStringValue

robot = UR()

parameters = ConnectParameters("192.168.0.1")

# The XML-RPC server is disabled by default
parameters.xml_rpc.enable = True
parameters.xml_rpc.port = 50000

robot.connect(parameters)

# The robot program connects with:
#   rpc := rpc_factory("xmlrpc", "http://192.168.0.10:50000")
# where 192.168.0.10 is the address of this PC
def on_request(sender, e):
    request = XmlRpcEventArg(e._instance)
    print(request.end_point, "calls", request.method_name)

    # URScript: answer := rpc.get_pose()
    if request.method_name == "get_pose":
        request.answer = XmlRpcPoseValue(Pose(0.4, -0.1, 0.3, 0, 3.14, 0))  # m and rad

    # URScript: answer := rpc.say_hello("UR5e")
    elif request.method_name == "say_hello":
        request.answer = XmlRpcStringValue("Hello " + str(request.arguments[0]))

    # Without an answer, the variable of the robot is not assigned

# Raised for each call of the robot program
robot.xml_rpc.xml_rpc_server_request(on_request)
```

The same server works without `UR`:

```python
from underautomation.universal_robots.xml_rpc.xml_rpc_server import XmlRpcServer
from underautomation.universal_robots.xml_rpc.xml_rpc_event_arg import XmlRpcEventArg
from underautomation.universal_robots.xml_rpc.xml_rpc_integer_value import XmlRpcIntegerValue

# An XML-RPC server, without a UR instance
server = XmlRpcServer()

def on_request(sender, e):
    request = XmlRpcEventArg(e._instance)
    if request.method_name == "get_counter":
        request.answer = XmlRpcIntegerValue(42)

server.xml_rpc_server_request(on_request)

server.start(50000)

# ...

server.stop()
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

**XmlRpcEventArg** ([reference](../api/underautomation.universal_robots.xml_rpc.md#xmlrpceventarg))

- `xml_request: typing.Any`: The XML document received via HTTP
- `method_name: str`: The method called by the robot
- `arguments: typing.List[XmlRpcValue]`: The arguments of the method called
- `end_point: typing.Any`: IP address of the robot
- `answer: XmlRpcValue`: Response to be provided to the robot by the user

**XmlRpcValue** ([reference](../api/underautomation.universal_robots.xml_rpc.md#xmlrpcvalue))

- `type: XmlRpcType (read only)`: Determines the class of this message
- `xml: typing.Any (read only)`: The XML description of the message that has been received from the robot or will be sent to the robot

## What to read next

- [Socket communication](socket-communication.md): exchange your own messages with the robot program.
- [Read and write registers](registers.md): exchange numbers with the robot program, without waiting.
