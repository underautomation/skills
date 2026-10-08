# Connect to the robot

Enable the interfaces of the UR cobot, set the network and the remote control, then connect with ConnectParameters. Ports, settings and errors.

Web page: https://underautomation.com/universal-robots/documentation/connect

This page explains how to prepare a Universal Robots cobot for the SDK, and how to connect to it from C# or Python. It applies to CB-Series and e-Series robots with PolyScope, to the robots with PolyScope X, and to URSim.

## Interfaces and ports

The SDK uses the standard interfaces of the robot. Each one is enabled in `ConnectParameters`, and some must also be enabled on the robot.

| Interface            | Port         | `ConnectParameters`                  | Default  | Setting on the robot                               |
| -------------------- | ------------ | ------------------------------------ | -------- | -------------------------------------------------- |
| Primary Interface    | 30001        | `PrimaryInterface`                   | enabled  | Service `Primary Client Interface`                 |
| Dashboard Server     | 29999        | `Dashboard`                          | enabled  | Service `Dashboard Server`. Not on PolyScope X     |
| RTDE                 | 30004        | `Rtde`                               | disabled | Service `RTDE`                                     |
| Interpreter Mode     | 30020        | `InterpreterMode`                    | disabled | Service `Interpreter Mode Socket`                  |
| REST API             | 80           | `Rest`                               | disabled | PolyScope X only                                   |
| SSH and SFTP         | 22           | `Ssh.EnableSsh`, `Ssh.EnableSftp`    | disabled | `Secure Shell` enabled                             |
| XML-RPC server       | 50000 (PC)   | `XmlRpc`                             | disabled | None. The robot program connects to the PC         |
| Socket server        | 50001 (PC)   | `SocketCommunication`                | disabled | None. The robot program connects to the PC         |

The Primary Interface can also use the Secondary Interface (30002) and the read only ports (30011, 30012), with `PrimaryInterface.Port`. The read only ports do not accept URScript.

## Prepare the robot

### Network

The robot and the PC must be on the same network, with addresses in the same subnet. On PolyScope, the address is set in the menu at the top right, `Settings`, `System`, `Network`.

Before it connects, `Connect` sends a ping to the robot and stops if the robot does not answer within 500 ms. When a firewall blocks the ping, set `PingBeforeConnecting` to `false`.

### Services

For security, each interface must be enabled on the robot. On PolyScope, open the menu at the top right, `Settings`, `Security`, `Services`, and enable the interfaces of the table above.

![Enable the services](https://underautomation.com/universal-robots/enable-remote.png)

In `Settings`, `Security`, `General`, the inbound connections must not be restricted for the ports that the SDK uses.

![Inbound connections](https://underautomation.com/universal-robots/inbound-connection.png)

### Remote control

On e-Series and PolyScope X, the robot accepts commands from the network only in remote control: Dashboard commands that change its state (power, brakes, load, play), URScript sent with the Primary Interface, and REST commands. Reading data does not need it.

Enable the remote control in `Settings`, `System`, `Remote Control`, then switch the robot from `Local` to `Remote` with the icon at the top right of PolyScope.

![Enable remote control](https://underautomation.com/universal-robots/enable-remote-control.png)

![Switch to remote control](https://underautomation.com/universal-robots/switch-remote.png)

### Firewall of the PC

The antivirus or the firewall of the PC can block these ports. If the connection fails, check them first. The XML-RPC and socket servers listen on the PC: allow their ports in the firewall of the PC.

## Connect

`Connect("192.168.0.1")` opens the Primary Interface and the Dashboard Server. To choose the interfaces and their settings, pass a `ConnectParameters`:

```csharp
using UnderAutomation.UniversalRobots;
using UnderAutomation.UniversalRobots.Rtde;

class Connect
{
  static void Main(string[] args)
  {
    var robot = new UR();

    var parameters = new ConnectParameters("192.168.0.1");

    // Enabled by default
    parameters.PrimaryInterface.Enable = true;
    parameters.Dashboard.Enable = true;

    // RTDE: select the data to exchange and the frequency
    parameters.Rtde.Enable = true;
    parameters.Rtde.Frequency = 500; // Hz
    parameters.Rtde.OutputSetup.Add(RtdeOutputData.ActualTcpPose);
    parameters.Rtde.OutputSetup.Add(RtdeOutputData.ActualQ);
    parameters.Rtde.InputSetup.Add(RtdeInputData.InputIntRegisters, 24);

    // Local XML-RPC server, called by the robot program
    parameters.XmlRpc.Enable = true;
    parameters.XmlRpc.Port = 50000;

    // Local socket server, the robot program connects to it
    parameters.SocketCommunication.Enable = true;
    parameters.SocketCommunication.Port = 50001;

    // SSH and SFTP, with the Linux user of the controller
    parameters.Ssh.EnableSsh = true;
    parameters.Ssh.EnableSftp = true;
    parameters.Ssh.Username = "ur";
    parameters.Ssh.Password = "easybot";

    // Interpreter Mode and REST API (PolyScope X) are disabled by default
    parameters.InterpreterMode.Enable = false;
    parameters.Rest.Enable = false;

    robot.Connect(parameters);

    // ...

    // Close every service
    robot.Disconnect();
  }
}
```

**ConnectParameters** ([reference](../api/UnderAutomation.UniversalRobots.md#connectparameters))

- `ConnectParameters()`: Initializes a new instance of UniversalRobots.ConnectParameters with default values.
- `ConnectParameters(string ip)`: Initializes a new instance of UniversalRobots.ConnectParameters with the specified robot IP address.
- `DashboardConnectParameters Dashboard { get; set; }`: Dashboard Server connection parameters (port 29999).
- `string IP { get; set; }`: IP address of the Universal Robots controller.
- `InterpreterModeConnectParameters InterpreterMode { get; set; }`: Interpreter Mode connection parameters for sending URScript lines interactively.
- `bool PingBeforeConnecting { get; set; }`: If true, a ping is sent to the robot before attempting connection. Default is true.
- `PrimaryInterfaceConnectParameters PrimaryInterface { get; set; }`: Primary Interface connection parameters (port 30001/30002).
- `RestConnectParameters Rest { get; set; }`: REST API connection parameters (PolyscopeX only)
- `RtdeConnectParameters Rtde { get; set; }`: Real-Time Data Exchange (RTDE) connection parameters (port 30004).
- `SocketCommunicationConnectParameters SocketCommunication { get; set; }`: Socket communication connection parameters for exchanging data with URScript programs.
- `SshConnectParameters Ssh { get; set; }`: SSH and SFTP connection parameters for file transfer and remote shell access.
- `XmlRpcConnectParameters XmlRpc { get; set; }`: XML-RPC connection parameters for remote procedure calls.

Each interface is also a class that works without `UR`: `PrimaryInterfaceClient`, `DashboardClient`, `RtdeClient`, `RestClient`, `SftpClient`, `SshClient`, `InterpreterModeClient`, `XmlRpcServer`, `SocketCommunicationServer`. The page of each interface shows it.

## Errors

`Connect` opens the interfaces one after the other. When one fails, it closes the others and throws:

| Exception                 | Cause                                                                          |
| ------------------------- | ------------------------------------------------------------------------------ |
| `InvalidLicenseException` | The trial is over, or the license key is not valid                             |
| `ConnectException`        | One interface did not connect. `Service` names it, `RobotIp` gives the address |
| `Exception`               | The robot does not answer the ping, or the address is empty                    |

After the connection, the errors of the background threads raise the event `InternalErrorOccured`, on `UR` and on each client.

```csharp
using UnderAutomation.UniversalRobots;
using UnderAutomation.UniversalRobots.Common;
using UnderAutomation.UniversalRobots.License;

class ConnectErrors
{
  static void Main(string[] args)
  {
    var robot = new UR();

    try
    {
      robot.Connect("192.168.0.1");
    }
    catch (InvalidLicenseException ex)
    {
      // The trial is over or the license key is not valid
      Console.WriteLine(ex.LicenseInfo);
    }
    catch (ConnectException ex)
    {
      // One service did not connect: the other services are closed
      Console.WriteLine($"{ex.Service} of {ex.RobotIp}: {ex.Message}");
    }
    catch (Exception ex)
    {
      // For example, the robot does not answer the ping
      Console.WriteLine(ex.Message);
    }

    // Errors that happen after the connection, in a background thread
    robot.InternalErrorOccured += (sender, e) =>
    {
      Console.WriteLine($"{e.Status}: {e.Message}");
    };
  }
}
```

## Disconnect

`Disconnect()` closes every interface. Each client also has its own method: `robot.Rtde.Disconnect()`, `robot.Dashboard.Disable()`...

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## What to read next

- [Develop without a robot](configure-offline-simulator.md): install URSim.
- [RTDE](rtde.md) and [Primary Interface](data-streaming.md): read the state of the robot.
- [Licensing](license.md): the 30 day trial and the license key.
