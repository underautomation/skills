# Connect to your robot

Configure the connection to an IRC5 or OmniCore controller, choose the Robot Web Services version, and use the synchronous or asynchronous API.

Web page: https://underautomation.com/abb/documentation/connect

The SDK talks to the robot controller over Robot Web Services (RWS), the HTTP interface that ABB controllers expose on the network. Nothing has to be installed on the robot.

Two classes can open a connection:

- `AbbController` : the main entry point. It holds the connection parameters and gives access to every protocol.
- `RwsClient` : a standalone RWS client, when you only need RWS and prefer a smaller object.

## Quick connection

Pass an IP address and you are connected. The default parameters match an OmniCore controller with its factory user account.

```csharp
using UnderAutomation.ABB;

public class ConnectQuick
{
    static void Main()
    {
        // Connect to an OmniCore controller with the default RWS parameters
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // Every RWS service is reachable from robot.Rws
        Console.WriteLine(robot.Rws.Controller.GetIdentity().Name);

        robot.Disconnect();
    }
}
```

Do not know the address yet? [Discover the controllers of the network](discover-controllers.md) instead of typing one.

## Full connection parameters

`ConnectionParameters` gives access to every option. Use it when the controller is not on its default port, uses HTTPS, or runs RobotWare 6.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws;

public class Connect
{
    static void Main()
    {
        ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");

        // Ping the controller first, so an unreachable robot fails immediately
        parameters.PingBeforeConnect = true;

        parameters.Rws.Enable = true;
        parameters.Rws.Username = "Default User";
        parameters.Rws.Password = "robotics";
        parameters.Rws.UseHttps = false;
        parameters.Rws.Port = 0; // 0 means 80 for HTTP and 443 for HTTPS
        parameters.Rws.Timeout = 10000;
        parameters.Rws.Version = RwsVersion.OmniCore_V2_0;

        AbbController robot = new AbbController();
        robot.Connect(parameters);

        robot.Disconnect();
    }
}
```

When `PingBeforeConnect` is `true` (default), the SDK sends an ICMP ping before the first HTTP request. An unreachable robot then fails in a few milliseconds instead of waiting for the HTTP timeout. Set it to `false` when ICMP is blocked on your network.

The default user account of an ABB controller is `Default User` with the password `robotics`. Change it if your controller uses a dedicated account. The account must have the User Authorization System (UAS) grants for what you want to do: reading is always allowed, writing needs the matching grant.

## IRC5 or OmniCore

One API covers the two generations of controllers. Only the `Version` property changes.

| Controller | RobotWare     | RWS version | `RwsVersion` value |
| ---------- | ------------- | ----------- | ------------------ |
| IRC5       | 6 and earlier | RWS 1.0     | `Irc5_V1_0`        |
| OmniCore   | 7 and later   | RWS 2.0     | `OmniCore_V2_0`    |

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws;

public class ConnectVersion
{
    static void Main()
    {
        // IRC5 controller, RobotWare 6 : RWS 1.0
        ConnectionParameters irc5 = new ConnectionParameters("192.168.0.1");
        irc5.Rws.Version = RwsVersion.Irc5_V1_0;

        // OmniCore controller, RobotWare 7 : RWS 2.0
        ConnectionParameters omniCore = new ConnectionParameters("192.168.0.2");
        omniCore.Rws.Version = RwsVersion.OmniCore_V2_0;

        // UseHttps is independent of the version. Set it to match how this
        // particular controller is configured on the network, not its generation.
        omniCore.Rws.UseHttps = true;

        AbbController robot = new AbbController();
        robot.Connect(omniCore);

        // The same code then works on both controllers
        Console.WriteLine(robot.Rws.System.GetInfo().Version);
    }
}
```

`OmniCore_V2_0` is the default. If you connect to an IRC5 without setting the version, the first request fails with a 404 status code.

`UseHttps` is a separate setting from `Version`. Both generations can be configured for HTTP or for HTTPS, this depends on how the controller itself is set up, not on which RWS version it speaks. Check your controller's own network configuration and set `UseHttps` to match. When the controller answers on HTTPS with a self-signed certificate, the SDK accepts it, you do not have to install anything in the certificate store.

The details of both versions are described in [IRC5 or OmniCore: which RWS version](irc5-vs-omnicore.md).

## Standalone RWS client

`RwsClient` connects without `AbbController`. The services are then directly on the client, `client.Controller` instead of `robot.Rws.Controller`.

```csharp
using UnderAutomation.ABB.Rws;

public class ConnectStandalone
{
    static void Main()
    {
        // RwsClient talks to the controller without going through AbbController
        RwsClient client = new RwsClient();
        client.Connect("192.168.0.1", "Default User", "robotics", 0, 10000, false, RwsVersion.OmniCore_V2_0);

        Console.WriteLine(client.Controller.GetIdentity().Name);

        client.Disconnect();
    }
}
```

## Synchronous and asynchronous

Every service method exists twice: a synchronous version, and an asynchronous one with the same name followed by `Async` and an optional `CancellationToken`.

```csharp
using UnderAutomation.ABB;

public class ConnectAsync
{
    static async Task Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // Every service method has an asynchronous twin, with a cancellation token
        var identity = await robot.Rws.Controller.GetIdentityAsync();
        var tasks = await robot.Rws.Rapid.GetTasksAsync();

        using (var cts = new CancellationTokenSource(TimeSpan.FromSeconds(5)))
        {
            var state = await robot.Rws.Panel.GetControllerStateAsync(cts.Token);
            Console.WriteLine(state);
        }

        Console.WriteLine($"{identity.Name} runs {tasks.Length} RAPID tasks");
    }
}
```

The asynchronous methods are not available on .NET Framework 3.5 and 4.0, which have no `async` / `await`. Everything else in the SDK works on those versions.

## Errors

Every RWS failure is reported as an `RwsException`. It carries the HTTP status code and, when the controller sends one, the ABB error code and message.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws;

public class ConnectErrors
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        try
        {
            robot.Rws.Panel.SetSpeedRatio(50);
        }
        catch (RwsException ex)
        {
            // StatusCode is the HTTP status returned by the controller
            // 403 usually means that another client holds the mastership
            Console.WriteLine($"RWS error {ex.StatusCode} : {ex.RwsErrorMessage}");
            Console.WriteLine($"ABB error code : {ex.RwsErrorCode}");
            Console.WriteLine($"Raw response : {ex.ResponseBody}");
        }
    }
}
```

Common status codes:

| Status | Meaning                                                                                                           |
| ------ | ----------------------------------------------------------------------------------------------------------------- |
| 400    | The controller refused the value, for example a speed ratio out of range                                          |
| 403    | Another client holds the [mastership](rws-mastership.md), or the user account lacks the UAS grant |
| 404    | The resource does not exist on this controller, often a wrong `RwsVersion`                                        |
| 500    | The controller could not run the operation in its current state                                                   |

## Disconnect

```csharp
using UnderAutomation.ABB;

public class ConnectDisconnect
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // Always disconnect : the controller keeps a limited number of sessions open
        robot.Disconnect();

        Console.WriteLine(robot.Enabled); // False
    }
}
```

A controller accepts a limited number of simultaneous sessions, around 70 on OmniCore. An application that connects in a loop without disconnecting exhausts them, and every following request answers 503.

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## API reference

**ConnectionParameters** ([reference](../api/UnderAutomation.ABB.md#connectionparameters))

- `ConnectionParameters()`: Instantiate new connection parameters with default values
- `ConnectionParameters(string address)`: Instantiate new connection parameters with a specified address
- `string Address { get; set; }`: Address of the robot controller (IP or host name), default value is 127.0.0.1
- `bool PingBeforeConnect { get; set; }`: Send a ping command before initializing any connections
- `RwsConnectParameters Rws { get; set; }`: RWS2 (Robot Web Services 2) connection parameters

**RwsConnectParameters** ([reference](../api/UnderAutomation.ABB.Rws.md#rwsconnectparameters))

- `RwsConnectParameters()`
- `const string DEFAULT_PASSWORD = "robotics"`: Default password for Digest Authentication
- `const int DEFAULT_PORT = 80`: Default RWS port (80 for HTTP, 443 for HTTPS)
- `const int DEFAULT_TIMEOUT = 10000`: Default timeout in milliseconds
- `const string DEFAULT_USERNAME = "Default User"`: Default username for Digest Authentication
- `bool Enable { get; set; }`: Enable or disable the RWS client connection
- Inherited from [RwsConnectParametersBase](../api/UnderAutomation.ABB.Rws.Internal.md#rwsconnectparametersbase): `Port`, `Username`, `Password`, `Timeout`, `UseHttps`, `Version`

**RwsConnectParametersBase** ([reference](../api/UnderAutomation.ABB.Rws.Internal.md#rwsconnectparametersbase))

- `string Password { get; set; }`: Password for Digest Authentication (Default is "robotics")
- `int Port { get; set; }`: RWS service port (if set to 0, the SDK will use 80 for HTTP, 443 for HTTPS)
- `int Timeout { get; set; }`: HTTP request timeout in milliseconds (default: 1000ms)
- `bool UseHttps { get; set; }`: Whether to use HTTPS instead of HTTP (default: false)
- `string Username { get; set; }`: Username for Digest Authentication (Default is "Default User")
- `RwsVersion Version { get; set; }`: RWS protocol version to use. If not specified, RwsVersion.OmniCore_V2_0 (RWS 2.0) is used. RWS 2.0 is available in RobotWare &gt;= 7, which ships the new OmniCore controller generation. For older RobotWare versions running on IRC5 controllers, use RwsVersion.Irc5_V1_0 (RWS 1.0).

**RwsVersion** ([reference](../api/UnderAutomation.ABB.Rws.md#rwsversion-robotrwsversion))

- Irc5_V1_0: RWS 1.0, exposed by IRC5 controllers running RobotWare 6 and earlier.
- OmniCore_V2_0: RWS 2.0, exposed by OmniCore controllers running RobotWare 7 and later. This is the default when no version is specified.

**RwsException** ([reference](../api/UnderAutomation.ABB.Rws.md#rwsexception))

- `RwsException(string message)`: Creates a new RWS exception with a message
- `RwsException(string message, Exception innerException)`: Creates a new RWS exception with a message and inner exception
- `RwsException(string message, int statusCode, string responseBody)`: Creates a new RWS exception with a message, status code and response body
- `RwsException(string message, string responseBody)`: Creates a new RWS exception with a message and the raw response body
- `RwsException(string message, RwsException innerException)`: Creates a new RWS exception that explains the failure of another one, keeping its diagnostics
- `string ReasonPhrase { get; }`: HTTP reason phrase returned by the server (e.g. "Forbidden", "Method Not Allowed"), if available
- `string ResponseBody { get; }`: Raw response body from the server, if available
- `string RwsErrorCode { get; }`: ABB internal error code extracted from the RWS error payload (e.g. "-1073445865"), if present
- `string RwsErrorMessage { get; }`: Human readable error text extracted from the RWS error payload, if present
- `int? StatusCode { get; }`: HTTP status code returned by the server
