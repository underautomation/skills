---
name: underautomation-yaskawa-python
description: "UnderAutomation Yaskawa SDK for Python (pip UnderAutomation.Yaskawa, import underautomation.yaskawa). Use it when Python code talks to a Yaskawa Motoman robot controller (YRC1000, YRC1000micro, MOTOMAN NEXT, DX100, DX200, FS100), or when the user asks about the Yaskawa SDK, its protocols or its exceptions. Protocols of the SDK: High Speed Ethernet Server (UDP 10040 and 10041, the default), Ethernet Server (TCP 80), HTTP (web server) and FTP, plus offline kinematics for 169 robot models. It answers questions such as which protocol and which controller setting to use (remote mode, RS parameters, job selection), how to read the status, the position, the alarms, the variables and the I/O, how to switch the servo on, select and start a job, move the robot without a job, transfer files and back up the controller, compute the kinematics, and why an exception is raised. It holds the documentation pages, the Python code samples and the list of every public class and member of the package, with the Python names."
metadata:
  sdk-version: 3.0.1
---

# UnderAutomation Yaskawa SDK for Python

The UnderAutomation Yaskawa SDK connects a PC to a Yaskawa Motoman robot controller (YRC1000, YRC1000micro, MOTOMAN NEXT, DX100, DX200, FS100) over Ethernet, with nothing to install on the controller and no job to run. The main class is `YaskawaRobot` (`from underautomation.yaskawa.yaskawa_robot import YaskawaRobot`): each protocol of the controller is a property of it, enabled on its own in `ConnectParameters`.

## Before writing code

1. Run `pip show UnderAutomation.Yaskawa` in the environment of the project. If the package is missing, ask the user before you install it with `pip install UnderAutomation.Yaskawa`.
2. Compare its version with `sdk-version` above (3.0.1). A 4th version digit is the same release: for example pip 3.0.1.1 and `sdk-version` 3.0.1. If they differ, tell the user: an older package can miss members listed here, a newer one can have members that this skill does not list.
3. On Linux and macOS, the package needs a .NET runtime: see [Get started with Python](references/pages/get-started-python.md).
4. When you cannot run commands (claude.ai, ChatGPT), skip the check and tell the user that this skill documents version 3.0.1 of the SDK.

## Choose the protocol

A generic agent does not know which protocol of the controller gives which data, nor which setting of the controller it needs. Use this table, then open the page of the protocol.

| What the user wants to do | Protocol | Controller setting |
| --- | --- | --- |
| Read the status, the alarms, the position (Cartesian in mm and degrees, joints in pulses), the torque, the system information. About 10 ms per call | High Speed Ethernet Server, `robot.high_speed_e_server`. Enabled by default | `ETHERNET` set to `USED` (maintenance mode, `NETWORK FUNCTION SETTING`). UDP ports 10040 (data) and 10041 (files). Reads work in any mode |
| Switch the servo, hold, select and start a job, move the robot without a job, write variables and I/O | High Speed Ethernet Server, or Ethernet Server | Remote mode: `RS000` = 2, `RS005` = 1, `RS007` = 2, pseudo input `#82015 CMD REMOTE SEL`, key of the pendant in the remote position. A job start also needs the play mode and `JOB SELECT WHEN REMOTE AND PLAY` set to `PERMIT` |
| Read and write the B, I, D, R and S variables | High Speed Ethernet Server, or Ethernet Server | `RS022` = 1 to accept the variable number 0. Writes in play mode: `S2C541` and `S2C542` = 0 (DX200, YRC1000), `S2C409` = 1 (DX100, FS100) |
| Read and write the P, BP and EX position variables and the M registers, read the system parameters, download the CMOS backup | High Speed Ethernet Server only | As above |
| Start a job and wait for its end in one call, set the master job, read the position in a user or tool frame, the encoder temperatures, the maximum torque. Only TCP passes the firewall | Ethernet Server, `robot.e_server` | YRC1000 and YRC1000micro. `ETHERNET SERVER` set to `EXPANDED`. TCP port 80. `e_server.enable = True` in the parameters. About 20 ms per call |
| List the files with their description and read text files (jobs, data, parameters), without account and in any mode | HTTP, `robot.http` | YRC1000 and YRC1000micro. TCP port 80. Read only |
| Download, upload and delete files, large files | FTP, `robot.ftp` | `FTP` set to `EXPANDED`. TCP port 21. Account `ftp` to upload or delete (`anonymous`, the default, only downloads). FTP never overwrites a job: delete it first, otherwise the upload fails with the reason `JobAlreadyExists` |
| Forward and inverse kinematics of 169 robot models | Offline kinematics | No connection to a controller |

- The settings are made once on the pendant, in the `MANAGEMENT` security mode: see [Connect to your robot](references/pages/connect.md). If `ETHERNET` stays at `NOT USED`, the Ethernet function is not enabled on the controller: only the Yaskawa support can enable it.
- Several protocols can be enabled together. `connect` opens every enabled protocol. Firewalls must let their ports through, and ICMP for the ping before the connection (`ping_before_connect`).
- The High Speed Ethernet Server is UDP: `connect` does not exchange a message with the controller. A wrong address or a closed port shows at the first call, after `high_speed_e_server.data_timeout_milliseconds` (1500 ms), as a `SocketException`. In the generated code, call `get_status_information()` right after the connection to check the link.
- `get_status_information().command_remote` is true when the controller accepts the remote commands. Check it before a command, and give the user the settings above when it is false.
- When the controller refuses a command of the High Speed Ethernet Server, the SDK raises an `InvalidDataAnswerException` whose message is the reason: `Command remote not set` (remote mode), `Incorrect mode` (play mode to start a job), `Servo OFF`, `Error/alarm occurring` (reset the alarm), `Hold by programming pendant` or `External hold`, `Cannot over write the target file` (the file exists: set `RS029` = 1 and `RS214` = 1, or delete it first). The Ethernet Server raises a `HostControlException` with the same kind of reasons. See [Connect to your robot](references/pages/connect.md).
- `move_cartesian` and `move_joints` use `StraightIncrement` when the command type is not given: the values are then an offset from the current position, not a target. Always pass `PositionCommandType.StraightAbsolute` or `LinkAbsolute` for an absolute target. Use `LinkPercent` with `LinkAbsolute`, and `Cartesian_MM_S` with the straight moves. Pass the posture of the current position (`form` of the Cartesian position) to keep the configuration of the arm. See [Motion](references/pages/hses-motion.md).
- The moves return when the controller accepts them, not at the end of the move. To chain moves, read the position until it reaches the target, with a timeout. To stop a move, hold the robot: `set_hold(True)`. See [Move the robot from a PC](references/pages/how-to-move-robot.md).
- Units: joints in encoder pulses, sent back to `move_joints` as they are read. The SDK does not convert pulses to degrees: the offline kinematics use degrees. The Cartesian P variables are in micrometers and 1/10000 degree, the current position in mm and degrees.
- Starting a job from the PC (`start_job`, Ethernet Server `start_job`) is a motion command: "Motion safety" applies. No method of the SDK writes the speed override: the job runs at its taught speeds. In the generated code, select the cycle `OneCycle` or `Step` with `set_cycle` before the start, ask for a confirmation, and tell the user to check the job on the pendant in teach mode first.
- The High Speed Ethernet Server and the Ethernet Server clients have the same methods for status, positions, alarms, I/O, variables and moves (same method names). See [Choose a protocol](references/pages/protocols.md).
- There is no simulator: the virtual controller of MotoSim EG-VRC does not answer the SDK. Test on a real controller, or on a controller on a test bench for everything except motion. See [Develop without a robot](references/pages/simulator.md).
- The exceptions come from the .NET runtime. Import them from the .NET namespace, for example `from UnderAutomation.Yaskawa.HighSpeedEServer import InvalidDataAnswerException` or `from UnderAutomation.Yaskawa.License import InvalidLicenseException`, after the first import of `underautomation.yaskawa`. Their members keep the .NET names: `ex.Message`, `ex.LicenseInfo`.

The comparison tables of the pages give the details per task, for example [Choose a protocol](references/pages/protocols.md), [Ethernet Server overview](references/pages/ethernet-server.md) and [Run a job](references/pages/how-to-run-program.md).

## Connect and license

Create a `YaskawaRobot`, enable the protocols you need in `ConnectParameters`, then connect. Without parameters, `connect(ip)` enables the High Speed Ethernet Server only. Always disconnect at the end. See [Connect to your robot](references/pages/connect.md).

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

The SDK runs 30 days without a license key. With a key, register it once at startup, before the first connection. Without a valid license, the connection raises an `InvalidLicenseException`. The offline kinematics do not need a connection. See [Licensing](references/pages/license.md).

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters
from underautomation.yaskawa.license.license_state import LicenseState
from UnderAutomation.Yaskawa.License import InvalidLicenseException

# Register the license once, before the first connection.
# The returned object describes the state of the license
info = YaskawaRobot.register_license("YourCompanyName", "YOUR_LICENSE_KEY")

# Number of trial days remaining
evaluation_days_left = info.evaluation_days_left

license_valid = info.state == LicenseState.Licensed

# A readable description of the current state
print(info)

# Check the license once at startup, rather than catching
# the exception on every connection
if not info.is_licensed:
    print(info)
    raise SystemExit(0)

try:
    robot = YaskawaRobot()
    robot.connect(ConnectParameters("192.168.0.1"))
except InvalidLicenseException as ex:
    # The exception comes from the .NET runtime, so its members keep their original names
    print(ex.Message)
    print(ex.LicenseInfo.State)
```

## Motion safety

- Never start a motion, a program or an output that can move the robot unless the user asked for it.
- A generated program that moves the robot does not move by default. It first prints what it will do (program, targets, speed), then asks for a typed confirmation, or it needs an explicit option such as `--run`.
- In the generated code, use the lowest speed the API allows: a low override, or low speed limits in the motion parameters (see the notes of the brand in this file). Show where to change it.
- No method of the SDK writes the speed override, and a job runs at its taught speeds. Before a job start, select the cycle `OneCycle` or `Step`. In the move commands, pass low speed values, for example `LinkPercent` 10 or `Cartesian_MM_S` 20, as in [Move the robot from a PC](references/pages/how-to-move-robot.md).
- When the controller allows it, tell the user to run the first test in manual mode at reduced speed, with the enabling device in hand.
- Tell the user to check the work area before the first run: nobody in the cell, no obstacle on the path, every target reachable.
- There is no simulator for the SDK: propose a first test on a controller on a test bench, with the arm clear. See [Develop without a robot](references/pages/simulator.md).
- The SDK does not replace the safety functions of the controller (emergency stop, safety fences, collision detection).

## Rules for the agent

- Use only the types and members listed in `references/api`. Search `references/api/index.md` for a type, then open the file of its namespace.
- If a member seems missing, do not guess it: read the installed package: `pip show -f UnderAutomation.Yaskawa` gives its folder in `site-packages`, the classes are in `underautomation/yaskawa/`.
- Start from the code samples of `references/pages`: their names are checked against this version of the package.
- Use the Python names (snake_case) of this skill. The .NET names (PascalCase) of the C# documentation do not exist in the Python package, except on a caught exception (next rule).
- Exceptions: the SDK raises the .NET exception. Catch it with its .NET type, imported from its .NET namespace, for example `from UnderAutomation.Yaskawa.Common import ConnectException`, then `except ConnectException as e`. Its members keep their .NET names: `e.Message`, `e.InnerException`. The classes of the same name in the `underautomation.yaskawa` modules are not Python exceptions: `except` on one of them raises a `TypeError`. For the list and what to check, read `references/errors.md`.
- When the answer depends on the controller (model, software version, options, settings), ask the user.

## Index of the references

- [API index](references/api/index.md): every public type, with the file of its namespace.
- [Errors](references/errors.md): exceptions of the SDK, when they are raised, what to check.
- [Get started: Get started with Python](references/pages/get-started-python.md): Install the Yaskawa SDK from PyPI and control a Motoman controller from Python 3.7 to 3.13, on Windows, Linux and macOS. Same functions as the .NET library, with Python names.
- [Get started: Try the SDK with the demo application](references/pages/demo-app.md): A Windows application, one executable and open source, that calls every function of the SDK. Test what your Yaskawa controller answers before you write any code.
- [Get started: Connect to your robot](references/pages/connect.md): Prepare the controller (remote mode, job selection, file overwrite), then connect the SDK: High Speed Ethernet Server by default, Ethernet Server, HTTP and FTP on demand. Ports, timeouts, errors.
- [Get started: Choose a protocol](references/pages/protocols.md): The four protocols of the Yaskawa SDK side by side: High Speed Ethernet Server, Ethernet Server, HTTP and FTP. Ports, tasks, speed, and code that works with two protocols.
- [Get started: Develop without a robot](references/pages/simulator.md): MotoSim EG-VRC does not simulate the network of the controller. What you need to test the SDK, and how to organize your code when the robot is not available.
- [Get started: Licensing](references/pages/license.md): The 30 day trial, the license key and RegisterLicense, the license states, the maintenance and the source license of the Yaskawa SDK.
- [High Speed Ethernet Server: High Speed Ethernet Server overview](references/pages/high-speed-ethernet-server.md): The High Speed Ethernet Server of Motoman controllers, what the SDK does with it, the units, the controllers and the list of topics.
- [High Speed Ethernet Server: Status and servo](references/pages/hses-status.md): Read the mode and the state of a Yaskawa controller, switch the servo power, hold the robot, select the cycle mode, lock the pendant and show a message on it.
- [High Speed Ethernet Server: Alarms](references/pages/hses-alarms.md): Read up to 4 alarms of a Yaskawa controller with their code, text and time, read the sub codes, then reset the alarms or cancel an error.
- [High Speed Ethernet Server: System information and parameters](references/pages/hses-system.md): Read the software version, the axis names, the operating times and the system parameters (S1CG, RS...) of a Yaskawa controller.
- [High Speed Ethernet Server: Positions](references/pages/hses-positions.md): Read the Cartesian position in mm and degrees, the joint pulses, the position error and the torque of a Yaskawa robot, a station or a base axis.
- [High Speed Ethernet Server: Motion](references/pages/hses-motion.md): Move a Yaskawa robot from a PC: linear and joint moves to a Cartesian target, relative moves, moves in pulses, speed units, frames and posture.
- [High Speed Ethernet Server: Jobs](references/pages/hses-jobs.md): List the jobs of a Yaskawa controller, select a job and start it, hold it, and read the executing job, its line and the call stack of each task.
- [High Speed Ethernet Server: Variables and registers](references/pages/hses-variables.md): Read and write the B, I, D, R and S variables, the P, BP and EX position variables and the M registers of a Yaskawa controller.
- [High Speed Ethernet Server: Inputs and outputs](references/pages/hses-io.md): Read the I/O groups of a Yaskawa controller (general, external, specific, network...), test one signal and write the network inputs.
- [High Speed Ethernet Server: Files and backup](references/pages/hses-files.md): List, download, upload and delete the job and data files of a Yaskawa controller, and download its CMOS backup.
- [Ethernet Server: Ethernet Server overview](references/pages/ethernet-server.md): The Ethernet Server of YRC1000 controllers over TCP: what the SDK does with it, how it compares with the High Speed Ethernet Server, connection, errors and units.
- [Ethernet Server: Status, alarms and servo](references/pages/eserver-status.md): Read the state and the alarms with their text through the Ethernet Server, reset them, switch the servo, hold the robot, set the cycle, the mode and the pendant lock.
- [Ethernet Server: Positions and torque](references/pages/eserver-positions.md): Read the joint pulses and the Cartesian position in the base, robot, user or tool frame, the posture, the torque and the encoder temperatures through the Ethernet Server.
- [Ethernet Server: Jobs](references/pages/eserver-jobs.md): List the jobs of a Yaskawa controller through the Ethernet Server, select and start a job, wait for its end in one call, set the master job and delete jobs.
- [Ethernet Server: Motion](references/pages/eserver-motion.md): Move a Yaskawa robot through the Ethernet Server: linear and joint moves to a Cartesian target in a frame, relative moves and moves to a target in pulses.
- [Ethernet Server: Variables and I/O](references/pages/eserver-variables-io.md): Read and write the B, I, D, R and S variables, read the I/O signals and write the network inputs of a Yaskawa controller through the Ethernet Server.
- [FTP and HTTP: FTP: connection and file management](references/pages/ftp.md): Connect to the FTP server of a Yaskawa controller, choose the account, list the folders and files, test and delete files, and handle the FTP errors.
- [FTP and HTTP: FTP file transfers](references/pages/ftp-transfer.md): Download and upload the jobs and data files of a Yaskawa controller over FTP: text, bytes, local files, several files at once, progress and async methods.
- [FTP and HTTP: HTTP: read files from the web server](references/pages/http.md): List the files of a Yaskawa controller with their description and read their text through its web server, without account and in any mode.
- [Offline kinematics: Forward and inverse kinematics](references/pages/kinematics.md): Compute the flange position from joint angles, and every set of joint angles for a position, for 169 Yaskawa arms and cobots, offline on the PC.
- [Offline kinematics: Inverse kinematics solutions](references/pages/kinematics-inverse.md): Why a position has up to 8 or 16 joint solutions on a Yaskawa robot, what they look like, which positions are reachable, and how to choose a solution.
- [Offline kinematics: Kinematics models and DH parameters](references/pages/kinematics-models.md): Get the DH parameters of a Yaskawa robot from the catalog of 169 models, from the ALL.PRM file of the controller, or from your own values.
- [How-To Articles: Get the robot position](references/pages/how-to-get-position.md): Read the position of a Yaskawa robot from C# or Python: Cartesian position or joint pulses, which method to choose, and a polling loop. Complete program included.
- [How-To Articles: Read and write I/O](references/pages/how-to-read-write-io.md): Switch a network input and wait for an output of a Yaskawa controller from C# or Python, with the signal numbers, groups and bits explained.
- [How-To Articles: Read and write variables](references/pages/how-to-read-write-variables.md): Exchange data with a Yaskawa job from C# or Python: integer, real, byte and string variables, which type to choose, and the frequent errors.
- [How-To Articles: Run a job](references/pages/how-to-run-program.md): Select a job of a Yaskawa controller, switch the servo on, start it and wait for its end from C# or Python. Settings of the controller and frequent errors.
- [How-To Articles: Read and reset alarms](references/pages/how-to-read-reset-alarms.md): Detect an alarm of a Yaskawa controller, read its code and text, reset it and check the result, from C# or Python.
- [How-To Articles: Transfer files and backups](references/pages/how-to-transfer-files.md): Back up every job of a Yaskawa controller, send a job written on the PC and download the CMOS backup, from C# or Python.
- [How-To Articles: Monitor the state of the robot](references/pages/how-to-monitor-state.md): Poll the mode, the servo, the hold, the alarms and the job of a Yaskawa controller, and print each change of state.
- [How-To Articles: Move the robot from a PC](references/pages/how-to-move-robot.md): Switch the servo on and move a Yaskawa robot in a straight line from C# or Python, without a job. Which move to choose, how to wait for the end, and the frequent errors.
