# Connect to your robot

The protocols of the SDK, their options and setup on the controller, the connection parameters, and the connection to a real Fanuc robot or to ROBOGUIDE.

Web page: https://underautomation.com/fanuc/documentation/connect

This page explains how to connect the Fanuc SDK to a real controller or to a ROBOGUIDE virtual robot: the protocols to enable, their setup on the controller and the connection parameters. The `ConnectionParameters` class lists the protocols, and each protocol is enabled on its own.

## Prerequisites

### Network

The PC and the controller are on the same network, and the PC can ping the controller. Each protocol uses its own TCP port: allow it in the firewalls between the PC and the controller.

### Protocols and controller options

| Protocol      | What it gives                                                    | Controller option                                                     | Setup                                                         |
| ------------- | ---------------------------------------------------------------- | --------------------------------------------------------------------- | ------------------------------------------------------------- |
| CGTP          | Programs, variables, registers, I/O, position, kinematics, files | None, firmware V8.30 or later                                          | [CGTP overview](cgtp.md)                   |
| SNPX          | Fast access to registers, variables, I/O, position, alarms      | R553 with the FANUC America parameters (R650 FRA), none with R651 FRL | [SNPX overview](snpx.md)                   |
| Telnet KCL    | Program control, variables, ports, breakpoints                   | None                                                                  | [Enable Telnet](telnet-enable-on-robot.md) |
| FTP           | Files, variable files, diagnostics                               | None                                                                  | [FTP overview](ftp.md)                     |
| RMI           | Motion instructions sent from the PC                             | R912                                                                  | [RMI overview](rmi.md)                     |
| Stream Motion | A position at every communication cycle                          | J519                                                                  | [Stream Motion overview](stream-motion.md) |

## Connect

### Quick connection

The simplest way to connect is to pass an IP address. This enables only the CGTP protocol, which is enabled by default.

```csharp
using UnderAutomation.Fanuc;

public class ConnectQuick
{
    static void Main()
    {
        var robot = new FanucRobot();
        robot.Connect("192.168.0.1");
    }
}
```

### Several protocols

To use several protocols, create a `ConnectionParameters` object and enable each protocol you need.

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common;

public class Connect
{
  static void Main()
  {
    // Create a robot instance
    FanucRobot robot = new FanucRobot();

    // Configure connection parameters
    ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");

    // Enable Telnet KCL for remote commands
    parameters.Telnet.Enable = true;
    parameters.Telnet.TelnetKclPassword = "your_password";

    // Enable FTP for file and variable access
    parameters.Ftp.Enable = true;
    parameters.Ftp.FtpUser = "";
    parameters.Ftp.FtpPassword = "";

    // Enable SNPX for high-speed register and I/O access
    parameters.Snpx.Enable = true;

    // Enable CGTP Web Server (enabled by default)
    parameters.Cgtp.Enable = true;

    // Enable RMI for remote motion commands
    parameters.Rmi.Enable = true;

    // Connect to the robot
    robot.Connect(parameters);

    // Check connection status
    bool isConnected = robot.Enabled;

    // Disconnect when done
    robot.Disconnect();
  }
}
```

### ROBOGUIDE

Instead of an IP address, pass the folder of a robot of a ROBOGUIDE workcell. The SDK reads the file `services.txt` of that folder to find the TCP ports of the virtual robot. See [Test with ROBOGUIDE](simulator.md).

```csharp
using UnderAutomation.Fanuc;

public class ConnectRoboguide
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();

        var parameters = new ConnectionParameters(@"C:\Users\you\Documents\My Workcells\CRX 10iA L\Robot_1");
        parameters.Telnet.Enable = true;
        parameters.Telnet.TelnetKclPassword = "";
        parameters.Ftp.Enable = true;
        parameters.Ftp.FtpUser = "";
        parameters.Ftp.FtpPassword = "";
        robot.Connect(parameters);
    }
}
```

## Connection options

### Ping

When `PingBeforeConnect` is `true` (default), the SDK pings the controller before it opens any connection. If the controller does not answer within 100 ms, `Connect` throws an exception at once. Set it to `false` when ICMP is blocked on your network.

### Language of the controller

Set the `Language` property to the language of the controller, so that the strings read with SNPX, FTP and Telnet are decoded correctly: English (ASCII, default), Japanese (Shift-JIS) or Chinese (GB2312).

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common;

public class ConnectOptions
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");

        // Ping before connecting (default: true)
        parameters.PingBeforeConnect = true;
        // Set to false for ROBOGUIDE or when ICMP is blocked

        // Controller language for correct string decoding
        parameters.Language = Languages.English;   // default (ASCII)
                                                   // parameters.Language = Languages.Japanese; // Shift-JIS
                                                   // parameters.Language = Languages.Chinese;  // GB2312

        robot.Connect(parameters);
    }
}
```

## Standalone protocol clients

Each protocol can also be used without `FanucRobot`, when you only need one protocol:

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Snpx;
using UnderAutomation.Fanuc.Telnet;
using UnderAutomation.Fanuc.Cgtp;

public class ConnectStandalone
{
    static void Main()
    {
        // Standalone SNPX client
        var snpx = new SnpxClient();
        snpx.Connect("192.168.0.1");

        // Standalone Telnet client
        var telnet = new TelnetClient();
        telnet.Connect("192.168.0.1", "telnet_password");

        // Standalone CGTP client
        var cgtp = new CgtpClient();
        cgtp.Connect("192.168.0.1");
    }
}
```

## Disconnect

Always disconnect when you are done, to close the connections of every protocol.

```csharp
using UnderAutomation.Fanuc;

public class ConnectDisconnect
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        robot.Connect("192.168.0.1");

        robot.Disconnect();
    }
}
```

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**ConnectionParameters** ([reference](../api/UnderAutomation.Fanuc.md#connectionparameters))

- `ConnectionParameters()`: Instanciate a new connection parameters
- `ConnectionParameters(string address)`: Instanciate a new connection parameters with a specified address
- `string Address { get; set; }`: Address of the robot (IP, host name, or path to ROBOGUIDE project folder)
- `CgtpConnectParameters Cgtp { get; set; }`: Parameters of the CGTP client, which uses the web server of the controller (HTTP)
- `FtpConnectParameters Ftp { get; set; }`: Access controller internal memory to read variables, IO, positions, diagnosis, ...
- `Languages Language { get; set; }`: Controller language (default: English)
- `bool PingBeforeConnect { get; set; }`: Send a ping command before initializing any connections
- `RmiConnectParameters Rmi { get; set; }`: Parameters for RMI (Remote Motion Interface)
- `SnpxConnectParameters Snpx { get; set; }`: Read and write IOs, read and clear alarms, read current program tasks
- `StreamMotionConnectParameters StreamMotion { get; set; }`: Parameters for Stream Motion (J519 option) - real-time streaming motion control over UDP
- `TelnetConnectParameters Telnet { get; set; }`: Parameters of the Telnet KCL client, which sends commands to the robot for remote control. Telnet KCL is a legacy protocol: it is not secured (password and commands are sent in clear text), and its behavior changes with the firmware version and on ROBOGUIDE. The same KCL commands are available on...

**TelnetConnectParameters** ([reference](../api/UnderAutomation.Fanuc.Common.md#telnetconnectparameters))

- `TelnetConnectParameters()`
- `bool Enable { get; set; }`: Should use this service (default: false). Prefer robot.Cgtp.Kcl, enabled by default, for new developments.
- Inherited from [TelnetConnectParametersBase](../api/UnderAutomation.Fanuc.Telnet.Internal.md#telnetconnectparametersbase): `TelnetKclPassword`

**FtpConnectParameters** ([reference](../api/UnderAutomation.Fanuc.Common.md#ftpconnectparameters))

- `FtpConnectParameters()`
- `bool Enable { get; set; }`: Should enable memory access for this connection (default: true)
- Inherited from [FtpConnectParametersBase](../api/UnderAutomation.Fanuc.Ftp.Internal.md#ftpconnectparametersbase): `FtpUser`, `FtpPassword`, `FtpTimeoutMs`

**SnpxConnectParameters** ([reference](../api/UnderAutomation.Fanuc.Common.md#snpxconnectparameters))

- `SnpxConnectParameters()`
- `bool Enable { get; set; }`: Should enable SNPX for this connection (default: false)
- Inherited from [SnpxConnectParametersBase](../api/UnderAutomation.Fanuc.Snpx.Internal.md#snpxconnectparametersbase): `DEFAULT_PORT`, `Port`

**CgtpConnectParameters** ([reference](../api/UnderAutomation.Fanuc.Common.md#cgtpconnectparameters))

- `CgtpConnectParameters()`
- `bool Enable { get; set; }`: Should enable CGTP Web Server for this connection (default: true)
- Inherited from [CgtpConnectParametersBase](../api/UnderAutomation.Fanuc.Cgtp.Internal.md#cgtpconnectparametersbase): `DEFAULT_PORT`, `DEFAULT_REQUEST_TIMEOUT_MS`, `Port`, `RequestTimeoutMs`, `Login`, `Password`

**RmiConnectParameters** ([reference](../api/UnderAutomation.Fanuc.Common.md#rmiconnectparameters))

- `RmiConnectParameters()`
- `bool Enable { get; set; }`: Should enable RMI for this connection (default: false)
- Inherited from [RmiConnectParametersBase](../api/UnderAutomation.Fanuc.Rmi.Internal.md#rmiconnectparametersbase): `DEFAULT_PORT`, `DEFAULT_READ_TIMEOUT_MS`, `Port`, `ReadTimeoutMs`

**StreamMotionConnectParameters** ([reference](../api/UnderAutomation.Fanuc.Common.md#streammotionconnectparameters))

- `StreamMotionConnectParameters()`
- `bool Enable { get; set; }`: Should enable Stream Motion for this connection (default: false)
- `string Ip { get; set; }`: IP address of the robot for standalone Stream Motion connections
- Inherited from [StreamMotionConnectParametersBase](../api/UnderAutomation.Fanuc.StreamMotion.Internal.md#streammotionconnectparametersbase): `DEFAULT_PORT`, `DEFAULT_PROTOCOL_VERSION`, `DEFAULT_BUFFER_LEAD_TIME`, `DEFAULT_PACKET_STACK_SIZE`, `DEFAULT_STATUS_TIMEOUT_MS`, `Port`, `ProtocolVersion`, `BufferLeadTime`, `PacketStackSize`, `StatusTimeoutMs`, `HighPriority`

## What to read next

- [Test with ROBOGUIDE](simulator.md): work without a real robot.
- [Demo application](demo-app.md): try the connection without writing code.
- The protocol pages: [CGTP](cgtp.md), [SNPX](snpx.md), [Telnet](telnet.md), [FTP](ftp.md), [RMI](rmi.md), [Stream Motion](stream-motion.md).
