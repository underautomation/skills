# Ethernet Server overview

The Ethernet Server of YRC1000 controllers over TCP: what the SDK does with it, how it compares with the High Speed Ethernet Server, connection, errors and units.

Web page: https://underautomation.com/yaskawa/documentation/ethernet-server

This page gives an overview of the Ethernet Server function of Yaskawa Motoman controllers (YRC1000, YRC1000micro), and of what the SDK does with it. The Ethernet Server is a second way to read and command the controller, over TCP, next to the [High Speed Ethernet Server](high-speed-ethernet-server.md).

## What is the Ethernet Server

The Ethernet Server is a function of the controller that answers commands of a PC over TCP. Its default port is 80, the port of the web server of the controller. The SDK opens one TCP connection for each command, sends it, reads the answer and closes the connection. There is no session to keep alive: a call made after a network cut works again as soon as the network is back.

The SDK gives you .NET objects. You do not build the messages. Nothing is installed on the controller and no job has to run.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters

parameters = ConnectParameters("192.168.0.1")
parameters.e_server.enable = True

robot = YaskawaRobot()
robot.connect(parameters)

# State of the controller
status = robot.e_server.get_status_information()
print(f"Play: {status.play}, remote: {status.command_remote}, servo: {status.servo_on}")

# Position of the robot, in mm and degrees
tcp = robot.e_server.get_robot_cartesian_position()
print(f"X={tcp.x} Y={tcp.y} Z={tcp.z}")

# Executing job
job = robot.e_server.get_executing_job_information()
print(f"Job {job.name}, line {job.line}")

# Variables D000 to D003
d = robot.e_server.read_double_integer(0, 4)

robot.disconnect()
```

## Ethernet Server or High Speed Ethernet Server

Both protocols read the state of the controller and command it. Most applications use the High Speed Ethernet Server. The Ethernet Server is useful in these cases:

| Need                                                        | Ethernet Server                                                                  | High Speed Ethernet Server                                      |
| ----------------------------------------------------------- | -------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| Transport                                                   | TCP, port 80                                                                     | UDP, ports 10040 and 10041                                      |
| A firewall lets only TCP through                            | Yes                                                                              | No                                                              |
| Read a status (measured on a YRC1000micro)                  | About 20 ms per call                                                             | About 10 ms per call                                            |
| Alarm texts                                                 | Error and 4 alarms, with code, sub code and text                                 | Up to 4 alarms with code, sub code, text and time               |
| Position in a user frame or in the tool frame               | Yes, `HostControlCoordinateSystem`                                               | Base frame. P variables in any frame                            |
| Wait for the end of a job                                   | `WaitForJobCompletion(seconds)`, one blocking call                               | Poll `GetStatusInformation().Running`                           |
| Job list, master job, job deletion                          | Yes                                                                              | Job list and deletion with the file functions                   |
| Encoder temperatures, maximum torque                        | Yes                                                                              | No                                                              |
| Position variables (P, BP, EX), registers, system variables | No                                                                               | Yes                                                             |
| File transfers                                              | No, use [FTP](ftp.md) or [HTTP](http.md) | Yes                                                             |

The two protocols can be used together: enable both in `ConnectParameters`, then call `robot.HighSpeedEServer` or `robot.EServer`. Code that must work with both can use the common interfaces, see [Choose a protocol](protocols.md#write_code_for_both_protocols).

## Topics

| Page                                                                    | What you can do                                                             |
| ----------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| [Status, alarms and servo](eserver-status.md)       | Read the state, read and reset alarms, servo, hold, cycle, mode, pendant    |
| [Positions and torque](eserver-positions.md)        | Joint pulses, Cartesian position in a frame, torque, encoder temperatures   |
| [Jobs](eserver-jobs.md)                             | List, select, start and wait for a job, master job, delete a job            |
| [Motion](eserver-motion.md)                         | Joint, linear and incremental moves, moves to a target in pulses            |
| [Variables and I/O](eserver-variables-io.md)        | B, I, D, R and S variables, read the I/O, write the network inputs          |

All these functions are methods of `robot.EServer` (`robot.e_server` in Python).

## Connect

### Prerequisites

- The PC reaches the controller on TCP port 80. A firewall between them must let this port through.
- The read methods work in any mode. The commands (servo, hold, jobs, moves, writes) need the remote mode, set as for the High Speed Ethernet Server: see [Prepare the controller](connect.md#prepare_the_controller).

### Enable the Ethernet Server

The Ethernet Server is disabled by default in `ConnectParameters`. Set `EServer.Enable` to `true`. The other protocols keep their own setting.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters

parameters = ConnectParameters("192.168.0.1")

# Only the Ethernet Server
parameters.high_speed_e_server.enable = False
parameters.e_server.enable = True

# TCP port of the Ethernet Server (default: 80)
parameters.e_server.port = 80

# Time to wait for an answer, in milliseconds
parameters.e_server.timeout_milliseconds = 5000            # most commands
parameters.e_server.power_on_timeout_milliseconds = 10000  # set_servo(True)
parameters.e_server.motion_timeout_milliseconds = 30000    # moves

robot = YaskawaRobot()
robot.connect(parameters)

robot.disconnect()
```

| Parameter                            | Default | Meaning                                         |
| ------------------------------------ | ------- | ----------------------------------------------- |
| `EServer.Enable`                     | `false` | Open the Ethernet Server client                 |
| `EServer.Port`                       | `80`    | TCP port of the Ethernet Server                 |
| `EServer.TimeoutMilliseconds`        | `5000`  | Time to wait for the answer of a command        |
| `EServer.PowerOnTimeoutMilliseconds` | `10000` | Time to wait for the answer of `SetServo(true)` |
| `EServer.MotionTimeoutMilliseconds`  | `30000` | Time to wait for the answer of a move           |

### What "connected" means

Each command opens its own TCP connection. So `Connect` checks the license and the address, but does not exchange a message with the controller. The first method call is the first exchange. To check the link at startup, call a read method, for example `GetStatusInformation()`, right after `Connect`.

### Standalone client

`EServerClient` opens an Ethernet Server client without `YaskawaRobot`. The methods are then directly on the client.

```python
from underautomation.yaskawa.host_control.e_server_client import EServerClient

# An Ethernet Server client without YaskawaRobot
client = EServerClient()
client.connect("192.168.0.1")

status = client.get_status_information()
print(f"Running: {status.running}")

client.close()
```

## Errors

When the controller refuses a command, the SDK throws a `HostControlException`. `Message` gives the reason in clear text, `ErrorCode` the code returned by the controller. A call made before `Connect` throws an `InvalidOperationException`.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters
from UnderAutomation.Yaskawa.HostControl import HostControlException

parameters = ConnectParameters("192.168.0.1")
parameters.e_server.enable = True
robot = YaskawaRobot()
robot.connect(parameters)

# The exceptions come from the .NET runtime: their members keep their .NET names
try:
    robot.e_server.start_job("PICK")
except HostControlException as ex:
    # Message gives the reason, ErrorCode the code of the controller
    print(f"Refused: {ex.Message} (code {ex.ErrorCode})")

robot.disconnect()
```

Frequent reasons, and what to check:

| Reason                                    | Check                                                                               |
| ----------------------------------------- | ----------------------------------------------------------------------------------- |
| Command remote not set                    | The remote mode, see [Prepare the controller](connect.md#prepare_the_controller) |
| Servo off                                 | Call `SetServo(true)` first                                                         |
| Alarm or error                            | Read and reset the alarm, see [Alarms](eserver-status.md#alarms) |
| Hold by the pendant, by a signal, by a command | Release the hold                                                               |
| Incorrect mode                            | Play mode to start a job, teach mode for some commands                              |
| Argument out of range                     | The number of a variable, a signal or a frame does not exist on this controller     |

## Units

| Value                                  | Unit                                       |
| -------------------------------------- | ------------------------------------------ |
| Cartesian X, Y, Z                      | mm                                         |
| Cartesian Rx, Ry, Rz                   | degrees                                    |
| Joint positions and moves in pulses    | encoder pulses                             |
| Torque                                 | percent of the rated torque                |
| Encoder temperature                    | degrees Celsius                            |
| Speed of a joint move                  | percent of the maximum speed               |
| Speed of a linear move                 | percent, or mm/s, set by `HostControlSpeedType` |

## Reference

**EServerClient** ([reference](../api/underautomation.yaskawa.host_control.md#eserverclient))

- `EServerClient()`: Creates a new instance of EServerClient for robot communication via TCP. Call Connect() to configure communication with a robot controller.
- `connect(ip: str, parameters: EServerConnectParameters) -> None`: Configures connection to the robot controller via TCP.
- `connect(ip: str) -> None`: Configures connection to the robot controller via TCP using default parameters.
- Inherited from [EServerClientInternal](../api/underautomation.yaskawa.host_control.internal.md#eserverclientinternal-robote_server): `close`, `connected`, `address`, `port`
- Inherited from [HostControlClientBase](../api/underautomation.yaskawa.host_control.internal.md#hostcontrolclientbase-robote_server): `get_alarm`, `get_status_information`, `get_executing_job_information`, `get_control_group`, `get_robot_joint_position`, `get_robot_cartesian_position`, `set_hold`, `alarm_reset`, `error_cancel`, `set_mode`, `set_cycle`, `set_servo`, `set_teach_pendant_lock_state`, `display`, `start_job`, `set_control_group`, `set_task`, `move_joint`, `move_linear`, `move_incremental`, `move_pulse_joint`, `move_pulse_linear`, `read_io`, `write_io`, `read_byte`, `write_byte`, `read_integer`, `write_integer`, `read_double_integer`, `write_double_integer`, `read_real`, `write_real`, `read16_bytes_char`, `write16_bytes_char`, `get_job_directory`, `get_user_frame`, `set_user_frame`, `delete_job`, `set_master_job`, `select_job`, `wait_for_job_completion`, `convert_to_relative_job`, `convert_to_standard_job`, `get_torque`, `get_max_torque`, `get_encoder_temperature`, `get_system_time`, `get_absolute_encoder_position`, `set_absolute_encoder_position`, `set_frame_type`, `get_alarm_with_messages`

**EServerConnectParametersInternal** ([reference](../api/underautomation.yaskawa.host_control.internal.md#eserverconnectparametersinternal))

- `EServerConnectParametersInternal()`
- `enable: bool`: Gets or sets a value indicating whether to enable the Ethernet Server connection (default: false).
- Inherited from [EServerConnectParameters](../api/underautomation.yaskawa.host_control.md#eserverconnectparameters): `DEFAULT_PORT`, `port`
- Inherited from [HostControlConnectParametersBase](../api/underautomation.yaskawa.host_control.internal.md#hostcontrolconnectparametersbase): `DEFAULT_TIMEOUT_MILLISECONDS`, `DEFAULT_POWER_ON_TIMEOUT_MILLISECONDS`, `DEFAULT_MOTION_TIMEOUT_MILLISECONDS`, `timeout_milliseconds`, `power_on_timeout_milliseconds`, `motion_timeout_milliseconds`

**EServerConnectParameters** ([reference](../api/underautomation.yaskawa.host_control.md#eserverconnectparameters))

- `EServerConnectParameters()`: Initializes a new instance of the Ethernet Server connection parameters.
- `port: int`: Gets or sets the TCP port number for Ethernet Server communication. Must match the robot controller's Ethernet Server port configuration. Default: 80.
- `static DEFAULT_PORT: int`: Default TCP port for Ethernet Server communication (80).
- Inherited from [HostControlConnectParametersBase](../api/underautomation.yaskawa.host_control.internal.md#hostcontrolconnectparametersbase): `DEFAULT_TIMEOUT_MILLISECONDS`, `DEFAULT_POWER_ON_TIMEOUT_MILLISECONDS`, `DEFAULT_MOTION_TIMEOUT_MILLISECONDS`, `timeout_milliseconds`, `power_on_timeout_milliseconds`, `motion_timeout_milliseconds`

**HostControlException** ([reference](../api/underautomation.yaskawa.host_control.md#hostcontrolexception))

- `ErrorCode: str (read only)`: Gets the error code returned by the robot controller.
- `Command: str (read only)`: Gets the command that caused the exception.
- Inherited from System.Exception: `Message`, `InnerException`

## What to read next

- [Status, alarms and servo](eserver-status.md): the first commands to try.
- [Choose a protocol](protocols.md): HSES, Ethernet Server, HTTP and FTP side by side.
