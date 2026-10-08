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

```python
from underautomation.fanuc.fanuc_robot import FanucRobot

robot = FanucRobot()
robot.connect("192.168.0.1")
```

### Several protocols

To use several protocols, create a `ConnectionParameters` object and enable each protocol you need.

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters
from underautomation.fanuc.common.languages import Languages

# Create a robot instance
robot = FanucRobot()

# Configure connection parameters
parameters = ConnectionParameters("192.168.0.1")

# Enable Telnet KCL for remote commands
parameters.telnet.enable = True
parameters.telnet.telnet_kcl_password = "your_password"

# Enable FTP for file and variable access
parameters.ftp.enable = True
parameters.ftp.ftp_user = ""
parameters.ftp.ftp_password = ""

# Enable SNPX for high-speed register and I/O access
parameters.snpx.enable = True

# Enable CGTP Web Server (enabled by default)
parameters.cgtp.enable = True

# Enable RMI for remote motion commands
parameters.rmi.enable = True

# Connect to the robot
robot.connect(parameters)

# Check connection status
is_connected = robot.enabled

# Disconnect when done
robot.disconnect()
```

### ROBOGUIDE

Instead of an IP address, pass the folder of a robot of a ROBOGUIDE workcell. The SDK reads the file `services.txt` of that folder to find the TCP ports of the virtual robot. See [Test with ROBOGUIDE](simulator.md).

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters

robot = FanucRobot()

parameters = ConnectionParameters(r"C:\Users\you\Documents\My Workcells\CRX 10iA L\Robot_1")
parameters.telnet.enable = True
parameters.telnet.telnet_kcl_password = ""
parameters.ftp.enable = True
parameters.ftp.ftp_user = ""
parameters.ftp.ftp_password = ""
robot.connect(parameters)
```

## Connection options

### Ping

When `PingBeforeConnect` is `true` (default), the SDK pings the controller before it opens any connection. If the controller does not answer within 100 ms, `Connect` throws an exception at once. Set it to `false` when ICMP is blocked on your network.

### Language of the controller

Set the `Language` property to the language of the controller, so that the strings read with SNPX, FTP and Telnet are decoded correctly: English (ASCII, default), Japanese (Shift-JIS) or Chinese (GB2312).

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters
from underautomation.fanuc.common.languages import Languages

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")

# Ping before connecting (default: True)
parameters.ping_before_connect = True
# Set to False for ROBOGUIDE or when ICMP is blocked

# Controller language for correct string decoding
parameters.language = Languages.English   # default (ASCII)
# parameters.language = Languages.Japanese  # Shift-JIS
# parameters.language = Languages.Chinese   # GB2312

robot.connect(parameters)
```

## Standalone protocol clients

Each protocol can also be used without `FanucRobot`, when you only need one protocol:

```python
from underautomation.fanuc.snpx.snpx_client import SnpxClient
from underautomation.fanuc.telnet.telnet_client import TelnetClient
from underautomation.fanuc.cgtp.cgtp_client import CgtpClient

# Standalone SNPX client
snpx = SnpxClient()
snpx.connect("192.168.0.1")

# Standalone Telnet client
telnet = TelnetClient()
telnet.connect("192.168.0.1", "telnet_password")

# Standalone CGTP client
cgtp = CgtpClient()
cgtp.connect("192.168.0.1")
```

## Disconnect

Always disconnect when you are done, to close the connections of every protocol.

```python
from underautomation.fanuc.fanuc_robot import FanucRobot

robot = FanucRobot()
robot.connect("192.168.0.1")

robot.disconnect()
```

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**ConnectionParameters** ([reference](../api/underautomation.fanuc.md#connectionparameters))

- `ConnectionParameters(address: str)`: Instanciate a new connection parameters with a specified address
- `address: str`: Address of the robot (IP, host name, or path to ROBOGUIDE project folder)
- `ping_before_connect: bool`: Send a ping command before initializing any connections
- `language: Languages`: Controller language (default: English)
- `telnet: TelnetConnectParameters`: Sends commands to the robot for remote control
- `ftp: FtpConnectParameters`: Access controller internal memory to read variables, IO, positions, diagnosis, ...
- `snpx: SnpxConnectParameters`: Read and write IOs, read and clear alarms, read current program tasks
- `rmi: RmiConnectParameters`: Parameters for RMI (Remote Motion Interface)
- `stream_motion: StreamMotionConnectParameters`: Parameters for Stream Motion (J519 option) - real-time streaming motion control over UDP
- `cgtp: CgtpConnectParameters`: Parameters for CGTP Web Server (HTTP-based COMET RPC interface)

**TelnetConnectParameters** ([reference](../api/underautomation.fanuc.common.md#telnetconnectparameters))

- `TelnetConnectParameters()`
- `enable: bool`: Should use this service (default: false)
- Inherited from [TelnetConnectParametersBase](../api/underautomation.fanuc.telnet.internal.md#telnetconnectparametersbase): `telnet_kcl_password`

**FtpConnectParameters** ([reference](../api/underautomation.fanuc.common.md#ftpconnectparameters))

- `FtpConnectParameters()`
- `enable: bool`: Should enable memory access for this connection (default: true)
- Inherited from [FtpConnectParametersBase](../api/underautomation.fanuc.ftp.internal.md#ftpconnectparametersbase): `ftp_user`, `ftp_password`, `ftp_timeout_ms`

**SnpxConnectParameters** ([reference](../api/underautomation.fanuc.common.md#snpxconnectparameters))

- `SnpxConnectParameters()`
- `enable: bool`: Should enable SNPX for this connection (default: false)
- Inherited from [SnpxConnectParametersBase](../api/underautomation.fanuc.snpx.internal.md#snpxconnectparametersbase): `DEFAULT_PORT`, `port`

**CgtpConnectParameters** ([reference](../api/underautomation.fanuc.common.md#cgtpconnectparameters))

- `CgtpConnectParameters()`
- `enable: bool`: Should enable CGTP Web Server for this connection (default: true)
- Inherited from [CgtpConnectParametersBase](../api/underautomation.fanuc.cgtp.internal.md#cgtpconnectparametersbase): `DEFAULT_PORT`, `DEFAULT_REQUEST_TIMEOUT_MS`, `port`, `request_timeout_ms`, `login`, `password`

**RmiConnectParameters** ([reference](../api/underautomation.fanuc.common.md#rmiconnectparameters))

- `RmiConnectParameters()`
- `enable: bool`: Should enable RMI for this connection (default: false)
- Inherited from [RmiConnectParametersBase](../api/underautomation.fanuc.rmi.internal.md#rmiconnectparametersbase): `DEFAULT_PORT`, `DEFAULT_READ_TIMEOUT_MS`, `port`, `read_timeout_ms`

**StreamMotionConnectParameters** ([reference](../api/underautomation.fanuc.common.md#streammotionconnectparameters))

- `StreamMotionConnectParameters()`
- `enable: bool`: Should enable Stream Motion for this connection (default: false)
- `ip: str`: IP address of the robot for standalone Stream Motion connections
- Inherited from [StreamMotionConnectParametersBase](../api/underautomation.fanuc.stream_motion.internal.md#streammotionconnectparametersbase): `DEFAULT_PORT`, `DEFAULT_PROTOCOL_VERSION`, `DEFAULT_BUFFER_LEAD_TIME`, `DEFAULT_PACKET_STACK_SIZE`, `DEFAULT_STATUS_TIMEOUT_MS`, `port`, `protocol_version`, `buffer_lead_time`, `packet_stack_size`, `status_timeout_ms`, `high_priority`

## What to read next

- [Test with ROBOGUIDE](simulator.md): work without a real robot.
- [Demo application](demo-app.md): try the connection without writing code.
- The protocol pages: [CGTP](cgtp.md), [SNPX](snpx.md), [Telnet](telnet.md), [FTP](ftp.md), [RMI](rmi.md), [Stream Motion](stream-motion.md).
