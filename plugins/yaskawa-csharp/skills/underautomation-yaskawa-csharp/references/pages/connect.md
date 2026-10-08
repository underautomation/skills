# Connect to your robot

Prepare the controller (remote mode, job selection, file overwrite), then connect the SDK: High Speed Ethernet Server by default, Ethernet Server, HTTP and FTP on demand. Ports, timeouts, errors.

Web page: https://underautomation.com/yaskawa/documentation/connect

This page explains how to connect the SDK to a Yaskawa Motoman controller: the settings of the controller, the connection parameters, the errors and the disconnection. By default the SDK uses the High Speed Ethernet Server of the controller, over UDP. The Ethernet Server, HTTP and FTP are enabled with one flag each, see [Choose a protocol](protocols.md). Nothing is installed on the controller.

## Prerequisites

- The PC reaches the controller on the network. Its address is set in `LAN INTERFACE SETTING`, see [Enable the Ethernet function](#enable_the_ethernet_function).
- The Ethernet function is enabled on the controller. The High Speed Ethernet Server answers on the UDP ports 10040 (data) and 10041 (files). A firewall between the PC and the controller must let these ports through.
- The controller is one of: YRC1000 (micro), MOTOMAN NEXT, DX100 / DX200, FS100.

The read methods work in any mode. The commands (servo, motion, job start, file write) need the settings below.

## Prepare the controller

Each setting is made once, on the programming pendant, with the security mode set to `MANAGEMENT`. Do the steps in this order: first the Ethernet function, then the parameters, then the remote commands.

### Enable the Ethernet function

The Ethernet function is set in the maintenance mode of the controller.

1. Start the controller in maintenance mode. Two ways:
   - Switch on the controller while you hold the `MAIN MENU` key of the pendant.
   - On a running controller, select `CPU RESET` > `MAINTENANCE` > `REBOOT`.
2. Select `SYSTEM INFO` and press the `SECURITY` button.
3. Select the mode and change it to `MANAGEMENT`. The default password is sixteen 9: `9999999999999999`.
4. In the main menu, select `SYSTEM` > `SETUP` > `OPTION FUNCTION`.

![Option function](https://underautomation.com/yaskawa/documentation/pendant-option-function.png)

5. In `LAN INTERFACE SETTING`, set the IP address, the subnet mask and the gateway of the controller.
6. In `NETWORK FUNCTION SETTING`:
   - Set `ETHERNET` to `USED`.
   - Set `FTP` to `EXPANDED`. The [FTP](ftp.md) client needs it.
   - Set `ETHERNET SERVER` to `EXPANDED`. The [Ethernet Server](ethernet-server.md) client needs it.

![Network function setting](https://underautomation.com/yaskawa/documentation/pendant-network-function-setting.png)

7. Restart the controller in normal mode.

If `ETHERNET` stays at `NOT USED` and cannot be changed, the Ethernet function is not enabled on your controller. Ask the Yaskawa support to enable it. It is a parameter of the FD type: only the Yaskawa mode can change it, with a checksum signature in the file `ALL.PRM`.

### Set the parameters

Select `PARAMETER` > `RS` and set these values:

| Parameter | Value | Meaning                                                               |
| --------- | ----- | --------------------------------------------------------------------- |
| `RS000`   | `2`   | Transmission protocol of the host control function                    |
| `RS005`   | `1`   | The port is used by the host control function                         |
| `RS007`   | `2`   | Read and write are accepted when the controller is not in remote mode |
| `RS022`   | `1`   | The variable number `0` is accepted                                   |
| `RS029`   | `1`   | Upload files and write data during the playback                       |
| `RS034`   | `200` | Response wait timer A, in ms. Factory value                           |
| `RS035`   | `200` | Monitoring timer B, in ms. Factory value                              |

To write the I/O and the variables in play mode, select `PARAMETER` > `S2C` and set:

| Controller                   | Parameter          | Value |
| ---------------------------- | ------------------ | ----- |
| DX100, FS100                 | `S2C409`           | `1`   |
| DX200, YRC1000, YRC1000micro | `S2C541`, `S2C542` | `0`   |

`GetSystemParameter` reads these values back from your application, see [System parameters](hses-system.md#system_parameters).

### Enable the remote commands

- Select `IN/OUT` > `PSEUDO INPUT SIGNAL`.
- Move the cursor to `#82015 CMD REMOTE SEL` and press `INTER LOCK` + `SELECT`.

![Enable remote command](https://raw.githubusercontent.com/underautomation/Yaskawa.NET/refs/heads/main/.github/assets/cmd-remote-sel.png)

### Put the key in the remote position

The commands need the key of the pendant in the remote position.

![Pendant remote key](https://raw.githubusercontent.com/underautomation/Yaskawa.NET/refs/heads/main/.github/assets/pendant-remote.png)

To use the key for the remote control, copy `#80011` (key in the remote position) to `#40042` (remote control enabled) with the ladder editor:

- Select `IN/OUT` > `LADDER EDITOR`.
- Check that no other rung writes `#40042`, then add this rung:

![Ladder remote key](https://raw.githubusercontent.com/underautomation/Yaskawa.NET/refs/heads/main/.github/assets/ladder-remote.png)

`GetStatusInformation().CommandRemote` is `true` when the controller accepts the remote commands.

### Allow the job selection

- Select `SETUP` > `FUNCTION ENABLE`.
- Set `JOB SELECT WHEN REMOTE AND PLAY` to `PERMIT`. On the Smart Pendant, set the parameter `SC2 224` to `0`.

![Job select when remote and play](https://raw.githubusercontent.com/underautomation/Yaskawa.NET/refs/heads/main/.github/assets/job-select-when-remote-and-play.png)

### Allow the file overwrite

To send a file that already exists on the controller:

- Select `PARAMETER` > `RS`.
- Set `RS029` to `1` and `RS214` to `1`.

## Quick connection

Pass the address of the controller. The other parameters keep their default values.

```csharp
using UnderAutomation.Yaskawa;

public class ConnectQuick
{
    static void Main()
    {
        var robot = new YaskawaRobot();

        // IP address of the controller, default ports and timeouts
        robot.Connect("192.168.0.1");

        // Every function of the SDK is a method of robot.HighSpeedEServer
        var status = robot.HighSpeedEServer.GetStatusInformation();
        Console.WriteLine($"Servo on: {status.ServoOn}, play mode: {status.Play}");

        robot.Disconnect();
    }
}
```

`YaskawaRobot` gives access to every function of the SDK, through its `HighSpeedEServer` property.

## Connection parameters

`ConnectParameters` holds every option. Use it when the controller has other ports, or when the network needs longer timeouts.

```csharp
using UnderAutomation.Yaskawa;

public class Connect
{
    static void Main()
    {
        var parameters = new ConnectParameters("192.168.0.1");

        // Ping the controller first (default: true)
        parameters.PingBeforeConnect = true;

        // UDP ports of the High Speed Ethernet Server (defaults: 10040 and 10041)
        parameters.HighSpeedEServer.DataPort = 10040;
        parameters.HighSpeedEServer.FilePort = 10041;

        // Time to wait for an answer, in milliseconds
        parameters.HighSpeedEServer.DataTimeoutMilliseconds = 1500;
        parameters.HighSpeedEServer.PowerOnTimeoutMilliseconds = 8000;
        parameters.HighSpeedEServer.FileTimeoutMilliseconds = 4000;

        var robot = new YaskawaRobot();
        robot.Connect(parameters);

        robot.Disconnect();
    }
}
```

| Parameter                                     | Default | Meaning                                                                 |
| --------------------------------------------- | ------- | ----------------------------------------------------------------------- |
| `IP`                                          | none    | IP address or host name of the controller                               |
| `PingBeforeConnect`                           | `true`  | Send a ping first. The connection fails if there is no answer in 200 ms |
| `HighSpeedEServer.Enable`                     | `true`  | Open the High Speed Ethernet Server client                              |
| `HighSpeedEServer.DataPort`                   | `10040` | UDP port of the data commands                                           |
| `HighSpeedEServer.FilePort`                   | `10041` | UDP port of the file transfers                                          |
| `HighSpeedEServer.DataTimeoutMilliseconds`    | `1500`  | Time to wait for the answer of a data command                           |
| `HighSpeedEServer.PowerOnTimeoutMilliseconds` | `8000`  | Time to wait for the answer of `SetServo(true)`                         |
| `HighSpeedEServer.FileTimeoutMilliseconds`    | `4000`  | Time to wait for the answer of a file transfer                          |
| `EServer.Enable`                              | `false` | Open the [Ethernet Server](ethernet-server.md) client (TCP 80) |
| `Http.Enable`                                 | `false` | Open the [HTTP](http.md) client (TCP 80)            |
| `Ftp.Enable`                                  | `false` | Open the [FTP](ftp.md) client (TCP 21)              |

The other parameters of `EServer`, `Http` and `Ftp` (ports, timeouts, FTP account) are described on the page of each protocol.

```csharp
using UnderAutomation.Yaskawa;
using UnderAutomation.Yaskawa.Common;

public class ConnectAllProtocols
{
    static void Main()
    {
        var parameters = new ConnectParameters("192.168.0.1");

        // High Speed Ethernet Server (UDP 10040 and 10041): enabled by default
        parameters.HighSpeedEServer.Enable = true;

        // Ethernet Server (TCP 80): status, jobs, variables, I/O and moves
        parameters.EServer.Enable = true;

        // Web server of the controller (TCP 80): file lists and text files
        parameters.Http.Enable = true;

        // FTP server of the controller (TCP 21): file transfers
        parameters.Ftp.Enable = true;
        parameters.Ftp.FtpUser = "ftp"; // "anonymous" can only download

        var robot = new YaskawaRobot();
        robot.Connect(parameters);

        // One property per protocol
        var status = robot.HighSpeedEServer.GetStatusInformation();
        var jobs = robot.EServer.GetJobDirectory();
        var files = robot.Http.GetFileList(FileExtension.JOB);
        var listing = robot.Ftp.GetListing("/JOB");

        // Closes every protocol
        robot.Disconnect();
    }
}
```

The ping also protects the controller: a request sent while the controller starts can raise an error on it. Set `PingBeforeConnect` to `false` only when a firewall blocks ICMP between the PC and the controller.

## UDP: what "connected" means

UDP has no connection. `Connect` checks the license, sends the ping and opens the socket: it does not exchange a message with the controller. The first method call is the first exchange. If the controller does not answer, this call fails after `DataTimeoutMilliseconds`.

To check the link at startup, call a read method, for example `GetStatusInformation()`, right after `Connect`.

`Connected` is `true` while the socket is open.

## Standalone client

`HighSpeedEServerClient` opens a High Speed Ethernet Server client without `YaskawaRobot`. The methods are then directly on the client: `client.GetStatusInformation()` instead of `robot.HighSpeedEServer.GetStatusInformation()`.

```csharp
using UnderAutomation.Yaskawa.HighSpeedEServer;

public class ConnectStandalone
{
    static void Main()
    {
        // A High Speed Ethernet Server client without YaskawaRobot
        var client = new HighSpeedEServerClient();
        client.Connect("192.168.0.1", new HighSpeedEServerConnectParameters());

        // The methods are directly on the client
        RobotStatusData status = client.GetStatusInformation();
        Console.WriteLine($"Running: {status.Running}");

        client.Close();
    }
}
```

## Errors

```csharp
using System.Net.Sockets;
using UnderAutomation.Yaskawa;
using UnderAutomation.Yaskawa.Common;
using UnderAutomation.Yaskawa.HighSpeedEServer;
using UnderAutomation.Yaskawa.License;

public class ConnectErrors
{
    static void Main()
    {
        var robot = new YaskawaRobot();

        try
        {
            robot.Connect("192.168.0.1");
            robot.HighSpeedEServer.StartJob();
        }
        catch (InvalidLicenseException ex)
        {
            // No valid license: the trial is over, or the key is wrong
            Console.WriteLine(ex.LicenseInfo);
        }
        catch (ConnectException ex)
        {
            // The UDP socket could not be opened
            Console.WriteLine($"{ex.Address}: {ex.Message}");
        }
        catch (InvalidDataAnswerException ex)
        {
            // The controller refused the command, for example "Servo OFF" or "Command remote not set"
            Console.WriteLine($"{ex.Message} ({ex.Status}, {ex.AddedStatus})");
        }
        catch (SocketException ex)
        {
            // No answer before the timeout
            Console.WriteLine(ex.Message);
        }
        catch (Exception ex)
        {
            // For example, no answer to the ping
            Console.WriteLine(ex.Message);
        }
    }
}
```

| Exception                    | When                                                                                                 |
| ---------------------------- | ---------------------------------------------------------------------------------------------------- |
| `InvalidLicenseException`    | `Connect` is called without a valid license. See [Licensing](license.md)         |
| `Exception`                  | No answer to the ping, or a method is called before `Connect`                                        |
| `ConnectException`           | The UDP socket could not be opened. `Address` gives the address and the port                         |
| `SocketException`            | No answer before the timeout, or the port is closed                                                  |
| `InvalidDataAnswerException` | The controller refused the command. `Message` gives the reason, `Status` and `AddedStatus` the codes |
| `HostControlException`       | The controller refused a command of the [Ethernet Server](ethernet-server.md#errors) |
| `FtpException`               | An FTP operation failed. `Reason` gives the cause, see [FTP](ftp.md#errors)      |

Frequent messages of `InvalidDataAnswerException`, and what to check:

| Message                                        | Check                                                                          |
| ---------------------------------------------- | ------------------------------------------------------------------------------ |
| `Command remote not set`                       | The remote mode, see [Prepare the controller](#prepare_the_controller)         |
| `Incorrect mode`                               | The mode of the controller: play mode to start a job                           |
| `Servo OFF`                                    | Switch the servo on first                                                      |
| `Error/alarm occurring`                        | Reset the alarm, see [Alarms](hses-alarms.md)              |
| `Hold by programming pendant`, `External hold` | Release the hold on the pendant or on the external signal                      |
| `Cannot over write the target file`            | `RS029` and `RS214`, see [Allow the file overwrite](#allow_the_file_overwrite) |

## Disconnect

`Disconnect` closes the sockets. Call it when your application ends, or when it no longer needs the controller.

```csharp
using UnderAutomation.Yaskawa;

public class ConnectDisconnect
{
    static void Main()
    {
        var robot = new YaskawaRobot();
        robot.Connect("192.168.0.1");

        // True while the UDP socket is open
        Console.WriteLine(robot.Connected);

        // Close the sockets when the application no longer needs the controller
        robot.Disconnect();
    }
}
```

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**ConnectParameters** ([reference](../api/UnderAutomation.Yaskawa.md#connectparameters))

- `ConnectParameters()`: Creates a new set of connect parameters
- `ConnectParameters(string ip)`: Creates a new set of connect parameters and defines IP property
- `EServerConnectParametersInternal EServer { get; set; }`: Ethernet Server connect parameters. Used for TCP-based Host Control communication via Ethernet Server.
- `FtpConnectParametersInternal Ftp { get; set; }`: FTP connect parameters. Used for file upload, download, listing and management via the robot's built-in FTP server.
- `HighSpeedEServerConnectParametersInternal HighSpeedEServer { get; set; }`: High Speed Ethernet Server connect parameters
- `HttpConnectParametersInternal Http { get; set; }`: HTTP connect parameters. Used for file listing and file content retrieval via the robot's built-in web server.
- `string IP { get; set; }`: IP Adress or robot host name
- `bool PingBeforeConnect { get; set; }`: Send a ping command before connecting

**HighSpeedEServerConnectParametersInternal** ([reference](../api/UnderAutomation.Yaskawa.HighSpeedEServer.Internal.md#highspeedeserverconnectparametersinternal))

- `HighSpeedEServerConnectParametersInternal()`
- `bool Enable { get; set; }`: Gets or sets a value indicating whether to enable the High Speed Ethernet Server connection (default: true).
- Inherited from [HighSpeedEServerConnectParameters](../api/UnderAutomation.Yaskawa.HighSpeedEServer.md#highspeedeserverconnectparameters): `DEFAULT_DATA_TIMEOUT_MILLISECONDS`, `DEFAULT_POWER_ON_TIMEOUT_MILLISECONDS`, `DEFAULT_FILE_TIMEOUT_MILLISECONDS`, `DEFAULT_DATA_PORT`, `DEFAULT_FILE_PORT`, `DataTimeoutMilliseconds`, `PowerOnTimeoutMilliseconds`, `FileTimeoutMilliseconds`, `DataPort`, `FilePort`

**HighSpeedEServerConnectParameters** ([reference](../api/UnderAutomation.Yaskawa.HighSpeedEServer.md#highspeedeserverconnectparameters))

- `HighSpeedEServerConnectParameters()`: Initializes a new instance of the connection parameters class.
- `const int DEFAULT_DATA_PORT = 10040`: Default UDP port for data communication (10040).
- `const int DEFAULT_DATA_TIMEOUT_MILLISECONDS = 1500`: Default timeout in milliseconds for data commands (1500ms).
- `const int DEFAULT_FILE_PORT = 10041`: Default UDP port for file transfer operations (10041).
- `const int DEFAULT_FILE_TIMEOUT_MILLISECONDS = 4000`: Default timeout in milliseconds for file operations (4000ms).
- `const int DEFAULT_POWER_ON_TIMEOUT_MILLISECONDS = 8000`: Default timeout in milliseconds for servo power on operations (8000ms).
- `int DataPort { get; set; }`: Gets or sets the UDP port number for data communication. Must match the robot controller's High Speed Ethernet Server data port configuration. Default: 10040.
- `int DataTimeoutMilliseconds { get; set; }`: Gets or sets the maximum time in milliseconds to wait for a response to data commands. Applies to most read/write operations like position reading, variable access, etc. Default: 1500ms.
- `int FilePort { get; set; }`: Gets or sets the UDP port number for file transfer operations. Must match the robot controller's High Speed Ethernet Server file port configuration. Default: 10041.
- `int FileTimeoutMilliseconds { get; set; }`: Gets or sets the maximum time in milliseconds to wait for file operation responses. File operations may be slower due to larger data transfers and disk I/O on the controller. Default: 4000ms.
- `int PowerOnTimeoutMilliseconds { get; set; }`: Gets or sets the maximum time in milliseconds to wait for servo power on to complete. Servo power on may take longer due to brake release and motor initialization. Default: 8000ms.

**ConnectException** ([reference](../api/UnderAutomation.Yaskawa.Common.md#connectexception))

- `string Address { get; }`: Address of the robot (IP:port)
- `string Service { get; }`: Name of the protocol that failed to connect

**InvalidDataAnswerException** ([reference](../api/UnderAutomation.Yaskawa.HighSpeedEServer.md#invaliddataanswerexception))

- `int AddedStatus { get; }`: Gets the additional status code providing more detailed error information. The interpretation of this value depends on the primary Status code.
- `int Status { get; }`: Gets the primary status code returned by the robot controller. A value of 0 indicates success; any other value indicates an error condition.

## What to read next

- [Choose a protocol](protocols.md): High Speed Ethernet Server, Ethernet Server, HTTP and FTP side by side.
- [High Speed Ethernet Server](high-speed-ethernet-server.md): the topics of the default protocol.
