# High Speed Ethernet Server overview

The High Speed Ethernet Server of Motoman controllers, what the SDK does with it, the units, the controllers and the list of topics.

Web page: https://underautomation.com/yaskawa/documentation/high-speed-ethernet-server

This page gives an overview of the High Speed Ethernet Server of Yaskawa Motoman controllers, and of what the SDK does with it. Each topic has its own page, listed below.

## What is the High Speed Ethernet Server

The High Speed Ethernet Server is a function of the Motoman controllers that answers requests of a PC over UDP. MotoSim EG-VRC uses it for its online functions. The SDK uses the same function, so nothing is installed on the controller and no job has to run for the SDK to work.

The SDK sends the requests, reads the answers and gives you .NET objects. You do not have to build UDP messages. One API covers these controllers: YRC1000 (micro), MOTOMAN NEXT, DX100 / DX200, FS100, ERC / XRC / MRC.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters

robot = YaskawaRobot()
robot.connect(ConnectParameters("192.168.0.1"))

# Status of the controller
status = robot.high_speed_e_server.get_status_information()
print(f"Play: {status.play}, running: {status.running}, alarm: {status.alarming}")

# Position of the tool, in mm and degrees
p = robot.high_speed_e_server.get_robot_cartesian_position()
print(f"X={p.x} Y={p.y} Z={p.z}")

# Job that the controller executes
job = robot.high_speed_e_server.get_executing_job_information()
print(f"{job.name}, line {job.line}")

# Integer variables I000 to I004
values = robot.high_speed_e_server.read_integer(0, 5).value
print(list(values))

robot.disconnect()
```

## Topics

| Page                                                                    | What you can do                                                                     |
| ----------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| [Status and servo](hses-status.md)                  | Read the mode and the state, switch the servo, hold, cycle mode, pendant message    |
| [Alarms](hses-alarms.md)                            | Read up to 4 alarms and their sub codes, reset them                                 |
| [System information and parameters](hses-system.md) | Software version, axis names, operating times, system parameters                    |
| [Positions](hses-positions.md)                      | Cartesian position, joint pulses, position error and torque, stations and base axes |
| [Motion](hses-motion.md)                            | Linear and joint moves, absolute and relative, in mm or in pulses                   |
| [Jobs](hses-jobs.md)                                | List, select and start jobs, read the executing job and the call stack              |
| [Variables and registers](hses-variables.md)        | B, I, D, R and S variables, P, BP and EX position variables, M registers            |
| [Inputs and outputs](hses-io.md)                    | Read the I/O groups, write the network inputs                                       |
| [Files and backup](hses-files.md)                   | List, download, upload and delete files, CMOS backup                                |

All these functions are methods of `robot.HighSpeedEServer` (`robot.high_speed_e_server` in Python), after [the connection](connect.md).

The SDK also uses three other protocols of the controller: the [Ethernet Server](ethernet-server.md) (TCP), [HTTP](http.md) and [FTP](ftp.md). [Choose a protocol](protocols.md) compares them.

## Units

| Value                                           | Unit                                                               |
| ----------------------------------------------- | ------------------------------------------------------------------ |
| Cartesian X, Y, Z (current position, motion)    | mm                                                                 |
| Cartesian Rx, Ry, Rz (current position, motion) | degrees                                                            |
| Joint positions and joint moves                 | encoder pulses                                                     |
| Position error                                  | encoder pulses                                                     |
| Torque                                          | percent of the rated torque                                        |
| Cartesian P variables                           | micrometers and 1/10000 degree                                     |
| Motion speed                                    | percent, mm/s or degrees/s, set by `PositionCommandClassification` |

The number of pulses per degree depends on the axis and on the robot model. It is a parameter of the controller.

## Read in any mode, command in remote mode

The read methods work in teach mode and in play mode. The methods that change the state of the controller (servo, hold, job select and start, motion, file writes) need the remote mode and the settings described in [Connect to your robot](connect.md). When a setting is missing, the controller refuses the command and the SDK throws an `InvalidDataAnswerException` with the reason.

## Requests and timing

Each method call is one request to the controller, and waits for its answer. The time of a call depends on the network and on the load of the controller: measure it on your cell before you choose a polling period. Variables and I/O are read in blocks: one call reads several values (`ReadInteger(0, 10)`) faster than ten calls.

The SDK sends one request at a time on each socket. File transfers use their own socket and their own port, so a file transfer does not block the data requests of another thread.

## What to read next

- [Connect to your robot](connect.md): the settings of the controller, the parameters and the errors.
- [How-to articles](how-to-get-position.md): complete programs for the frequent tasks.
- [Choose a protocol](protocols.md): when to use the Ethernet Server, HTTP or FTP instead.
