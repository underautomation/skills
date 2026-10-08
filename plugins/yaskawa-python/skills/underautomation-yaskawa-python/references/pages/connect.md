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

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters

robot = YaskawaRobot()

# IP address of the controller, default ports and timeouts
robot.connect(ConnectParameters("192.168.0.1"))

# Every function of the SDK is a method of robot.high_speed_e_server
status = robot.high_speed_e_server.get_status_information()
print(f"Servo on: {status.servo_on}, play mode: {status.play}")

robot.disconnect()
```

`YaskawaRobot` gives access to every function of the SDK, through its `HighSpeedEServer` property.

## Connection parameters

`ConnectParameters` holds every option. Use it when the controller has other ports, or when the network needs longer timeouts.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters

parameters = ConnectParameters("192.168.0.1")

# Ping the controller first (default: True)
parameters.ping_before_connect = True

# UDP ports of the High Speed Ethernet Server (defaults: 10040 and 10041)
parameters.high_speed_e_server.data_port = 10040
parameters.high_speed_e_server.file_port = 10041

# Time to wait for an answer, in milliseconds
parameters.high_speed_e_server.data_timeout_milliseconds = 1500
parameters.high_speed_e_server.power_on_timeout_milliseconds = 8000
parameters.high_speed_e_server.file_timeout_milliseconds = 4000

robot = YaskawaRobot()
robot.connect(parameters)

robot.disconnect()
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

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters
from underautomation.yaskawa.common.file_extension import FileExtension

parameters = ConnectParameters("192.168.0.1")

# High Speed Ethernet Server (UDP 10040 and 10041): enabled by default
parameters.high_speed_e_server.enable = True

# Ethernet Server (TCP 80): status, jobs, variables, I/O and moves
parameters.e_server.enable = True

# Web server of the controller (TCP 80): file lists and text files
parameters.http.enable = True

# FTP server of the controller (TCP 21): file transfers
parameters.ftp.enable = True
parameters.ftp.ftp_user = "ftp"  # "anonymous" can only download

robot = YaskawaRobot()
robot.connect(parameters)

# One property per protocol
status = robot.high_speed_e_server.get_status_information()
jobs = robot.e_server.get_job_directory()
files = robot.http.get_file_list(FileExtension.JOB)
listing = robot.ftp.get_listing("/JOB")

# Closes every protocol
robot.disconnect()
```

The ping also protects the controller: a request sent while the controller starts can raise an error on it. Set `PingBeforeConnect` to `false` only when a firewall blocks ICMP between the PC and the controller.

## UDP: what "connected" means

UDP has no connection. `Connect` checks the license, sends the ping and opens the socket: it does not exchange a message with the controller. The first method call is the first exchange. If the controller does not answer, this call fails after `DataTimeoutMilliseconds`.

To check the link at startup, call a read method, for example `GetStatusInformation()`, right after `Connect`.

`Connected` is `true` while the socket is open.

## Standalone client

`HighSpeedEServerClient` opens a High Speed Ethernet Server client without `YaskawaRobot`. The methods are then directly on the client: `client.GetStatusInformation()` instead of `robot.HighSpeedEServer.GetStatusInformation()`.

```python
from underautomation.yaskawa.high_speed_e_server.high_speed_e_server_client import HighSpeedEServerClient
from underautomation.yaskawa.high_speed_e_server.high_speed_e_server_connect_parameters import HighSpeedEServerConnectParameters

# A High Speed Ethernet Server client without YaskawaRobot
client = HighSpeedEServerClient()
client.connect("192.168.0.1", HighSpeedEServerConnectParameters())

# The methods are directly on the client
status = client.get_status_information()
print(f"Running: {status.running}")

client.close()
```

## Errors

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters
from UnderAutomation.Yaskawa.License import InvalidLicenseException
from UnderAutomation.Yaskawa.Common import ConnectException
from UnderAutomation.Yaskawa.HighSpeedEServer import InvalidDataAnswerException
from System.Net.Sockets import SocketException

robot = YaskawaRobot()

# The exceptions come from the .NET runtime, so their members keep their original names
try:
    robot.connect(ConnectParameters("192.168.0.1"))
    robot.high_speed_e_server.start_job()
except InvalidLicenseException as ex:
    # No valid license: the trial is over, or the key is wrong
    print(ex.LicenseInfo)
except ConnectException as ex:
    # The UDP socket could not be opened
    print(f"{ex.Address}: {ex.Message}")
except InvalidDataAnswerException as ex:
    # The controller refused the command, for example "Servo OFF" or "Command remote not set"
    print(f"{ex.Message} ({ex.Status}, {ex.AddedStatus})")
except SocketException as ex:
    # No answer before the timeout
    print(ex.Message)
except Exception as ex:
    # For example, no answer to the ping
    print(ex)
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

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters

robot = YaskawaRobot()
robot.connect(ConnectParameters("192.168.0.1"))

# True while the UDP socket is open
print(robot.connected)

# Close the sockets when the application no longer needs the controller
robot.disconnect()
```

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**ConnectParameters** ([reference](../api/underautomation.yaskawa.md#connectparameters))

- `ConnectParameters(ip: str)`: Creates a new set of connect parameters and defines IP property
- `ping_before_connect: bool`: Send a ping command before connecting
- `ip: str`: IP Adress or robot host name
- `high_speed_e_server: HighSpeedEServerConnectParametersInternal`: High Speed Ethernet Server connect parameters
- `e_server: EServerConnectParametersInternal`: Ethernet Server connect parameters. Used for TCP-based Host Control communication via Ethernet Server.
- `http: HttpConnectParametersInternal`: HTTP connect parameters. Used for file listing and file content retrieval via the robot's built-in web server.
- `ftp: FtpConnectParametersInternal`: FTP connect parameters. Used for file upload, download, listing and management via the robot's built-in FTP server.

**HighSpeedEServerConnectParametersInternal** ([reference](../api/underautomation.yaskawa.high_speed_e_server.internal.md#highspeedeserverconnectparametersinternal))

- `HighSpeedEServerConnectParametersInternal()`
- `enable: bool`: Gets or sets a value indicating whether to enable the High Speed Ethernet Server connection (default: true).
- Inherited from [HighSpeedEServerConnectParameters](../api/underautomation.yaskawa.high_speed_e_server.md#highspeedeserverconnectparameters): `DEFAULT_DATA_TIMEOUT_MILLISECONDS`, `DEFAULT_POWER_ON_TIMEOUT_MILLISECONDS`, `DEFAULT_FILE_TIMEOUT_MILLISECONDS`, `DEFAULT_DATA_PORT`, `DEFAULT_FILE_PORT`, `data_timeout_milliseconds`, `power_on_timeout_milliseconds`, `file_timeout_milliseconds`, `data_port`, `file_port`

**HighSpeedEServerConnectParameters** ([reference](../api/underautomation.yaskawa.high_speed_e_server.md#highspeedeserverconnectparameters))

- `HighSpeedEServerConnectParameters()`: Initializes a new instance of the connection parameters class.
- `data_timeout_milliseconds: int`: Gets or sets the maximum time in milliseconds to wait for a response to data commands. Applies to most read/write operations like position reading, variable access, etc. Default: 1500ms.
- `power_on_timeout_milliseconds: int`: Gets or sets the maximum time in milliseconds to wait for servo power on to complete. Servo power on may take longer due to brake release and motor initialization. Default: 8000ms.
- `file_timeout_milliseconds: int`: Gets or sets the maximum time in milliseconds to wait for file operation responses. File operations may be slower due to larger data transfers and disk I/O on the controller. Default: 4000ms.
- `data_port: int`: Gets or sets the UDP port number for data communication. Must match the robot controller's High Speed Ethernet Server data port configuration. Default: 10040.
- `file_port: int`: Gets or sets the UDP port number for file transfer operations. Must match the robot controller's High Speed Ethernet Server file port configuration. Default: 10041.
- `static DEFAULT_DATA_TIMEOUT_MILLISECONDS: int`: Default timeout in milliseconds for data commands (1500ms).
- `static DEFAULT_POWER_ON_TIMEOUT_MILLISECONDS: int`: Default timeout in milliseconds for servo power on operations (8000ms).
- `static DEFAULT_FILE_TIMEOUT_MILLISECONDS: int`: Default timeout in milliseconds for file operations (4000ms).
- `static DEFAULT_DATA_PORT: int`: Default UDP port for data communication (10040).
- `static DEFAULT_FILE_PORT: int`: Default UDP port for file transfer operations (10041).

**ConnectException** ([reference](../api/underautomation.yaskawa.common.md#connectexception))

- `Service: str (read only)`: Name of the protocol that failed to connect
- `Address: str (read only)`: Address of the robot (IP:port)
- Inherited from System.Exception: `Message`, `InnerException`

**InvalidDataAnswerException** ([reference](../api/underautomation.yaskawa.high_speed_e_server.md#invaliddataanswerexception))

- `Status: int (read only)`: Gets the primary status code returned by the robot controller. A value of 0 indicates success; any other value indicates an error condition.
- `AddedStatus: int (read only)`: Gets the additional status code providing more detailed error information. The interpretation of this value depends on the primary Status code.
- Inherited from System.Exception: `Message`, `InnerException`

## What to read next

- [Choose a protocol](protocols.md): High Speed Ethernet Server, Ethernet Server, HTTP and FTP side by side.
- [High Speed Ethernet Server](high-speed-ethernet-server.md): the topics of the default protocol.
