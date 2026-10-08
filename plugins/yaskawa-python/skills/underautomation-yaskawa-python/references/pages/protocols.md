# Choose a protocol

The four protocols of the Yaskawa SDK side by side: High Speed Ethernet Server, Ethernet Server, HTTP and FTP. Ports, tasks, speed, and code that works with two protocols.

Web page: https://underautomation.com/yaskawa/documentation/protocols

This page compares the four protocols that the Yaskawa SDK uses to talk to a Motoman controller: High Speed Ethernet Server, Ethernet Server, HTTP and FTP. It says what each one does, which ports it needs, and how to use several of them in one application.

## The four protocols

| Protocol                                                                  | Transport           | Property of `YaskawaRobot` | Enabled by default | Main use                                                      |
| ------------------------------------------------------------------------- | ------------------- | -------------------------- | ------------------ | ------------------------------------------------------------- |
| [High Speed Ethernet Server](high-speed-ethernet-server.md) | UDP 10040 and 10041 | `HighSpeedEServer`         | Yes                | Status, positions, motion, jobs, variables, I/O, files        |
| [Ethernet Server](ethernet-server.md)                 | TCP 80              | `EServer`                  | No                 | Status, positions, motion, jobs, variables, I/O, over TCP     |
| [HTTP](http.md)                                       | TCP 80              | `Http`                     | No                 | Read the file lists and the text files                        |
| [FTP](ftp.md)                                         | TCP 21              | `Ftp`                      | No                 | Download, upload and delete files, large files                |

Nothing is installed on the controller for any of them. The [offline kinematics](kinematics.md) need no protocol at all.

## Which protocol for which task

| Task                                             | First choice                | Also possible                       |
| ------------------------------------------------ | --------------------------- | ----------------------------------- |
| Read the status, the position, the alarms        | High Speed Ethernet Server  | Ethernet Server                     |
| Read and write B, I, D, R, S variables           | High Speed Ethernet Server  | Ethernet Server                     |
| Read and write P, BP, EX variables and registers | High Speed Ethernet Server  |                                     |
| Read the I/O, write the network inputs           | High Speed Ethernet Server  | Ethernet Server                     |
| Start a job and wait for its end                 | Ethernet Server (one call)  | High Speed Ethernet Server (polling) |
| Move the robot without a job                     | High Speed Ethernet Server  | Ethernet Server                     |
| Encoder temperatures, maximum torque             | Ethernet Server             |                                     |
| Download a job or a data file                    | FTP or HTTP                 | High Speed Ethernet Server          |
| Upload a job                                     | FTP                         | High Speed Ethernet Server          |
| Download a large file (`ALL.PRM`, 1.4 MB)        | FTP or HTTP (about 13 s)    | High Speed Ethernet Server (about 45 s) |
| CMOS backup                                      | High Speed Ethernet Server  |                                     |
| Only TCP passes the firewall                     | Ethernet Server, HTTP, FTP  |                                     |

The times are measured on a YRC1000micro. On the same controller, a status read takes about 10 ms with the High Speed Ethernet Server and about 20 ms with the Ethernet Server.

## Enable several protocols

Each protocol has an `Enable` flag in `ConnectParameters`. `Connect` opens every enabled protocol, `Disconnect` closes them all, and `Connected` is `true` when at least one is open.

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

### Ports to open in the firewall

| Protocol                   | Port         | Direction           |
| -------------------------- | ------------ | ------------------- |
| High Speed Ethernet Server | UDP 10040, UDP 10041 | PC to controller, and the answers |
| Ethernet Server            | TCP 80       | PC to controller    |
| HTTP                       | TCP 80       | PC to controller    |
| FTP                        | TCP 21, and the data connections of FTP | PC to controller |

The ping before the connection (`PingBeforeConnect`) also needs ICMP.

### Settings of the controller

The commands (servo, jobs, moves, writes) of the High Speed Ethernet Server and of the Ethernet Server need the remote mode: see [Prepare the controller](connect.md#prepare_the_controller). HTTP reads in any mode. FTP needs the right account to upload or delete: see [Accounts](ftp.md#accounts).

## Write code for both protocols

The High Speed Ethernet Server and the Ethernet Server clients implement the same interfaces of the namespace `UnderAutomation.Yaskawa.Common`. A function that takes an `IRobotClient` works with `robot.HighSpeedEServer` and with `robot.EServer`.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters

# Works with robot.high_speed_e_server and with robot.e_server: same method names
def print_state(client):
    status = client.get_status_information()
    tcp = client.get_robot_cartesian_position()

    print(f"{client.address}: servo {status.servo_on}, running {status.running}")
    print(f"X={tcp.x} Y={tcp.y} Z={tcp.z}")

parameters = ConnectParameters("192.168.0.1")
parameters.e_server.enable = True

robot = YaskawaRobot()
robot.connect(parameters)

# The same code reads the robot through two protocols
print_state(robot.high_speed_e_server)
print_state(robot.e_server)

robot.disconnect()
```

| Interface         | Methods                                                                            |
| ----------------- | ---------------------------------------------------------------------------------- |
| `IStatusReader`   | `GetStatusInformation`, `GetExecutingJobInformation`                               |
| `IPositionReader` | `GetRobotJointPosition` (pulses), `GetRobotCartesianPosition` (mm and degrees)     |
| `IAlarmReader`    | `GetActiveAlarms`                                                                  |
| `IRobotControl`   | `AlarmReset`, `SetServo`, `SetHold`, `SetTeachPendantLockState`, `SetCycle`, `StartJob`, `SelectJob`, `Display` |
| `IIOAccess`       | `ReadIO`, `WriteIO`                                                                |
| `IVariableAccess` | Read and write the B, I, D, R and S variables                                      |
| `ITorqueReader`   | `GetTorque`                                                                        |
| `IMotionControl`  | `MoveCartesian`, `MoveJoints`                                                      |
| `IRobotClient`    | All the interfaces above                                                           |
| `IFileReader`, `IFileWriter`, `IFileManager` | `GetFile`, `GetFileList`, `LoadFile`, `DeleteFile`: High Speed Ethernet Server, HTTP (read only) and FTP |

In Python, the clients have the same method names: a function that calls `get_status_information()` works with both, without the interfaces.

## Reference

**ConnectParameters** ([reference](../api/underautomation.yaskawa.md#connectparameters))

- `ConnectParameters(ip: str)`: Creates a new set of connect parameters and defines IP property
- `ping_before_connect: bool`: Send a ping command before connecting
- `ip: str`: IP Adress or robot host name
- `high_speed_e_server: HighSpeedEServerConnectParametersInternal`: High Speed Ethernet Server connect parameters
- `e_server: EServerConnectParametersInternal`: Ethernet Server connect parameters. Used for TCP-based Host Control communication via Ethernet Server.
- `http: HttpConnectParametersInternal`: HTTP connect parameters. Used for file listing and file content retrieval via the robot's built-in web server.
- `ftp: FtpConnectParametersInternal`: FTP connect parameters. Used for file upload, download, listing and management via the robot's built-in FTP server.

**IRobotClient** ([reference](../api/underautomation.yaskawa.common.md#irobotclient))

- Inherited from [IStatusReader](../api/underautomation.yaskawa.common.md#istatusreader): `get_status_information`, `get_executing_job_information`
- Inherited from [IPositionReader](../api/underautomation.yaskawa.common.md#ipositionreader): `get_robot_joint_position`, `get_robot_cartesian_position`
- Inherited from [IAlarmReader](../api/underautomation.yaskawa.common.md#ialarmreader): `get_active_alarms`
- Inherited from [IRobotControl](../api/underautomation.yaskawa.common.md#irobotcontrol): `alarm_reset`, `set_servo`, `set_hold`, `set_teach_pendant_lock_state`, `set_cycle`, `start_job`, `select_job`, `display`
- Inherited from [IIOAccess](../api/underautomation.yaskawa.common.md#iioaccess): `read_io`, `write_io`
- Inherited from [IVariableAccess](../api/underautomation.yaskawa.common.md#ivariableaccess): `read_byte`, `write_byte`, `read_integer`, `write_integer`, `read_double_integer`, `write_double_integer`, `read_real`, `write_real`, `read16_bytes_char`, `write16_bytes_char`
- Inherited from [ITorqueReader](../api/underautomation.yaskawa.common.md#itorquereader): `get_torque`
- Inherited from [IMotionControl](../api/underautomation.yaskawa.common.md#imotioncontrol): `move_cartesian`, `move_joints`
- Inherited from [IYaskawaClient](../api/underautomation.yaskawa.common.md#iyaskawaclient): `close`, `address`, `connected`

**IFileManager** ([reference](../api/underautomation.yaskawa.common.md#ifilemanager))

- Inherited from [IFileReader](../api/underautomation.yaskawa.common.md#ifilereader): `get_file`, `get_file_list`
- Inherited from [IFileWriter](../api/underautomation.yaskawa.common.md#ifilewriter): `load_file`, `delete_file`
- Inherited from [IYaskawaClient](../api/underautomation.yaskawa.common.md#iyaskawaclient): `close`, `address`, `connected`

## What to read next

- [Connect to your robot](connect.md): the settings of the controller and the connection errors.
- [Ethernet Server](ethernet-server.md), [HTTP](http.md), [FTP](ftp.md): the pages of each protocol.
