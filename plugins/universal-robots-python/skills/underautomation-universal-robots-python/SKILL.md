---
name: underautomation-universal-robots-python
description: "UnderAutomation Universal Robots SDK for Python (pip UnderAutomation.UniversalRobots, import underautomation.universal_robots). Use it when Python code talks to a Universal Robots cobot (CB-Series, e-Series, UR20 and UR30, PolyScope 5 or PolyScope X) or to URSim, or when the user asks about the Universal Robots SDK, its interfaces or its exceptions. Interfaces of the SDK: Primary and Secondary Interface (data at 10 Hz, URScript), RTDE (up to 500 Hz), Dashboard Server, REST API of PolyScope X, Interpreter Mode, XML-RPC server, socket server, SSH and SFTP. It answers questions such as which interface and which robot setting to use, how to read the position, the I/O, the variables and the registers, how to power on the robot and run a program, send URScript, move the robot, transfer files, read the alarms, compute the kinematics offline, and why an exception is thrown. It holds the documentation pages, the Python code samples and the list of every public class and member of the package, with the Python names."
metadata:
  sdk-version: 9.4.0
---

# UnderAutomation Universal Robots SDK for Python

The UnderAutomation Universal Robots SDK connects a PC to a Universal Robots cobot (CB-Series and e-Series with PolyScope 5, robots with PolyScope X) or to URSim over Ethernet, with nothing to install on the robot. The main class is `UR` (`from underautomation.universal_robots.ur import UR`): each interface of the robot is a property of it, enabled on its own in `ConnectParameters`. Each interface is also a class that works without `UR` (`RtdeClient`, `DashboardClient`, `PrimaryInterfaceClient`...).

## Before writing code

1. Run `pip show UnderAutomation.UniversalRobots` in the environment of the project. If the package is missing, ask the user before you install it with `pip install UnderAutomation.UniversalRobots`.
2. Compare its version with `sdk-version` above (9.4.0). A 4th version digit is the same release: for example pip 9.4.0.1 and `sdk-version` 9.4.0. If they differ, tell the user: an older package can miss members listed here, a newer one can have members that this skill does not list.
3. On Linux and macOS, the package needs a .NET runtime: see [Get started with Python](references/pages/get-started-python.md).
4. When you cannot run commands (claude.ai, ChatGPT), skip the check and tell the user that this skill documents version 9.4.0 of the SDK.

## Choose the interface

A generic agent does not know which interface of the robot gives which data, nor which setting it needs. Use this table, then open the page of the interface.

| What the user wants to do | Interface | Setting on the robot, port |
| --- | --- | --- |
| Read the state at 10 Hz: robot mode, joints, TCP, I/O, global variables, error messages, configuration. Enabled by default | Primary Interface | Service `Primary Client Interface`. Port 30001 (30002 Secondary, 30011 and 30012 read only) |
| Send URScript: a line, a program, a secondary program. The running program stops, except for a secondary program | Primary Interface | Same service. e-Series and PolyScope X: remote control. Not on the read only ports |
| Read data fast (up to 500 Hz on e-Series, 125 Hz on CB-Series), write I/O, registers, speed slider | RTDE | Service `RTDE`. Port 30004. Writing inputs needs remote control |
| Power on, release the brakes, load, play, pause, stop a `.urp` program, popups, safety status, robot mode | Dashboard Server | PolyScope 5 only (CB-Series, e-Series). Service `Dashboard Server`. Port 29999. Commands that change the state need remote control |
| The same on PolyScope X: power, brakes, load, play and stop programs, program state | REST API | PolyScope X only. Remote control (default password `operator`). Port 80 |
| Send URScript statements to a running program without stopping it | Interpreter Mode | Service `Interpreter Mode Socket`. Port 30020. The program calls `interpreter_mode()` |
| Answer function calls of a robot program (position from a vision system, numbers, text) | XML-RPC server (the SDK listens) | Nothing on the robot. Port 50000 on the PC, open in the PC firewall. The program uses `rpc_factory` |
| Exchange your own messages with a robot program | Socket server (the SDK listens) | Nothing on the robot. Port 50001 on the PC. The program uses `socket_open` |
| Download, upload, list, delete files: programs, installations, backups | SFTP | `Secure Shell` enabled. Port 22. User `root` on a robot, `ur` on URSim, password `easybot` by default |
| Run Linux commands on the controller | SSH | Same as SFTP |
| Forward and inverse kinematics, pose conversions, read and change `.urp` and `.installation` files | Offline toolbox | No connection to a robot |

- `connect(ip)` without parameters opens the Primary Interface and the Dashboard Server only. RTDE, Interpreter Mode, REST, SSH, SFTP, XML-RPC and socket server are disabled by default: enable them in `ConnectParameters`.
- Every interface is also a service to enable on the robot: PolyScope, `Settings`, `Security`, `Services`. In `Settings`, `Security`, `General`, the inbound connections must not be restricted for these ports. See [Connect to the robot](references/pages/connect.md).
- Remote control (e-Series and PolyScope X): enable it in `Settings`, `System`, `Remote Control`, then switch the robot from `Local` to `Remote` at the top right of PolyScope. Reading data does not need it. Commands that change the state of the robot and URScript do.
- PolyScope X has no Dashboard Server: use the REST API. An application for both PolyScope 5 and PolyScope X enables the client of the robot, see [REST API](references/pages/rest-api.md).
- Position: RTDE `ActualQ` and `ActualTcpPose` for fast reads, or the Primary Interface (`JointData`, `CartesianInfo`) with no setup. The TCP pose is in m and a rotation vector in rad, in the base frame. See [Get the robot position](references/pages/how-to-get-position.md).
- Exchange values with a running program: registers with RTDE. Use the RTDE half of the registers (integer and float 24 to 47, boolean 64 to 127) when a fieldbus uses the others. See [Read and write registers](references/pages/registers.md).
- Global variables are read only, with the Primary Interface or the Dashboard Server. To change a value while a program runs, use registers. See [Read and write variables](references/pages/variables.md).
- URScript sent with `robot.primary_interface.script.send` gets no answer: the call returns when the text is sent. Follow the end with `robot_mode_data.program_running` and the errors with the event `runtime_exception_message_received`. Write the numbers of the script with a dot.
- The Dashboard and REST commands return a response object with a success flag and the message of the robot. Check it: a failed `play()` does not raise.
- `connect` first pings the robot and stops after 500 ms without answer. When a firewall blocks the ping, set `ping_before_connecting` to `False`.
- URSim: the PolyScope 5 version (VirtualBox) has every interface, the PolyScope X version (Docker) has REST, Primary Interface and RTDE. See [Develop without a robot (URSim)](references/pages/configure-offline-simulator.md).

The comparison tables of the how-to pages give the details per task, for example [Move the robot from a PC](references/pages/how-to-move-robot.md), [Run a program](references/pages/how-to-run-program.md) and [Read and write I/O](references/pages/how-to-read-write-io.md).

## Moves from the PC

Every way to move a UR cobot from the PC is a motion command: "Motion safety" below applies.

- URScript with the Primary Interface (`movel`, `movej`): stops the running program. In the generated code, give low values to `a` and `v` (for example `v=0.05` m/s for `movel`, `v=0.2` rad/s for `movej`), and show where to change them.
- Interpreter Mode: the moves run inside a program of the operator, which continues after them.
- Registers and a program on the robot: the program reads its targets in the registers written by RTDE. The control stays on the robot side.
- The speed slider of the robot can also be set from the PC with RTDE: inputs `SpeedSliderMask` (value 1) and `SpeedSliderFraction` (0.0 to 1.0) of `RtdeInputData`, set in `RtdeInputValues` (`speed_slider_mask`, `speed_slider_fraction`), in remote control.
- Before a move: the robot is powered on, the brakes are released, and it is in remote control (e-Series, PolyScope X). Check the target with the [inverse kinematics](references/pages/kinematics.md) when it comes from a computation.

## Connect and license

Create a `UR`, enable the interfaces you need in `ConnectParameters`, then connect. Always disconnect at the end. See [Connect to the robot](references/pages/connect.md).

```python
from underautomation.universal_robots.ur import UR
from underautomation.universal_robots.connect_parameters import ConnectParameters
from underautomation.universal_robots.rtde.rtde_input_data import RtdeInputData
from underautomation.universal_robots.rtde.rtde_output_data import RtdeOutputData

robot = UR()

parameters = ConnectParameters("192.168.0.1")

# Enabled by default
parameters.primary_interface.enable = True
parameters.dashboard.enable = True

# RTDE: select the data to exchange and the frequency
parameters.rtde.enable = True
parameters.rtde.frequency = 500  # Hz
parameters.rtde.output_setup.add(RtdeOutputData.ActualTcpPose)
parameters.rtde.output_setup.add(RtdeOutputData.ActualQ)
parameters.rtde.input_setup.add(RtdeInputData.InputIntRegisters, 24)

# Local XML-RPC server, called by the robot program
parameters.xml_rpc.enable = True
parameters.xml_rpc.port = 50000

# Local socket server, the robot program connects to it
parameters.socket_communication.enable = True
parameters.socket_communication.port = 50001

# SSH and SFTP, with the Linux user of the controller
parameters.ssh.enable_ssh = True
parameters.ssh.enable_sftp = True
parameters.ssh.username = "ur"
parameters.ssh.password = "easybot"

# Interpreter Mode and REST API (PolyScope X) are disabled by default
parameters.interpreter_mode.enable = False
parameters.rest.enable = False

robot.connect(parameters)

# ...

# Close every service
robot.disconnect()
```

`connect` opens the interfaces one after the other. When one fails, it closes the others and raises a `ConnectException`: its message names the interface, the address and the port, and the inner exception gives the cause. After the connection, the errors of the background threads raise the event `internal_error_occured`.

The SDK runs 30 days without a license key. With a key, register it once at startup, before the first connection: the registration is static and also applies to the clients used without `UR`. Without a valid license, the connection raises an `InvalidLicenseException`. See [Licensing](references/pages/license.md).

```python
from underautomation.universal_robots.ur import UR
from underautomation.universal_robots.license.license_state import LicenseState
from UnderAutomation.UniversalRobots.License import InvalidLicenseException

# Register the license once, before the first connection.
# The returned object describes the state of the license
info = UR.register_license("YourCompanyName", "YOUR_LICENSE_KEY")

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
    robot = UR()
    robot.connect("192.168.0.1")
except InvalidLicenseException as ex:
    # The exception comes from the .NET runtime, so its members keep their original names
    print(ex.Message)
    print(ex.LicenseInfo.State)
```

## Motion safety

- Never start a motion, a program or an output that can move the robot unless the user asked for it.
- A generated program that moves the robot does not move by default. It first prints what it will do (program, targets, speed), then asks for a typed confirmation, or it needs an explicit option such as `--run`.
- In the generated code, use the lowest speed the API allows: a low override, or low speed limits in the motion parameters (see the notes of the brand in this file). Show where to change it.
- When the controller allows it, tell the user to run the first test in manual mode at reduced speed, with the enabling device in hand.
- Tell the user to check the work area before the first run: nobody in the cell, no obstacle on the path, every target reachable.
- Propose a first test on a virtual robot: [Develop without a robot (URSim)](references/pages/configure-offline-simulator.md).
- The SDK does not replace the safety functions of the controller (emergency stop, safety fences, collision detection).

## Rules for the agent

- Use only the types and members listed in `references/api`. Search `references/api/index.md` for a type, then open the file of its namespace.
- If a member seems missing, do not guess it: read the installed package: `pip show -f UnderAutomation.UniversalRobots` gives its folder in `site-packages`, the classes are in `underautomation/universal_robots/`.
- Start from the code samples of `references/pages`: their names are checked against this version of the package.
- Use the Python names (snake_case) of this skill. The .NET names (PascalCase) of the C# documentation do not exist in the Python package, except on a caught exception (next rule).
- Exceptions: the SDK raises the .NET exception. Catch it with its .NET type, imported from its .NET namespace, for example `from UnderAutomation.UniversalRobots.Common import ConnectException`, then `except ConnectException as e`. Its members keep their .NET names: `e.Message`, `e.InnerException`. The classes of the same name in the `underautomation.universal_robots` modules are not Python exceptions: `except` on one of them raises a `TypeError`. For the list and what to check, read `references/errors.md`.
- When the answer depends on the controller (model, software version, options, settings), ask the user.

## Index of the references

- [API index](references/api/index.md): every public type, with the file of its namespace.
- [Errors](references/errors.md): exceptions of the SDK, when they are raised, what to check.
- [Get started: Get started with Python](references/pages/get-started-python.md): Install the Universal Robots SDK from PyPI and write a first Python program. Python 3.7 to 3.13 on Windows, Linux and macOS, with pythonnet.
- [Get started: Try the SDK with the demo application](references/pages/demo-app.md): Download the Windows demo application of the Universal Robots SDK and try every interface on your robot or on URSim, without writing code. Its C# sources are on GitHub.
- [Get started: Connect to the robot](references/pages/connect.md): Enable the interfaces of the UR cobot, set the network and the remote control, then connect with ConnectParameters. Ports, settings and errors.
- [Get started: Develop without a robot (URSim)](references/pages/configure-offline-simulator.md): Install URSim, the simulator of Universal Robots, in VirtualBox for PolyScope 5 or in Docker for PolyScope X, and connect the SDK to it.
- [Get started: Licensing](references/pages/license.md): The 30 day trial of the Universal Robots SDK, the license key, the license states, the maintenance and the source license.
- [Communication protocols: RTDE: Real-Time Data Exchange](references/pages/rtde.md): Exchange data with a UR cobot up to 500 Hz with RTDE: choose the outputs and the inputs, receive the data, write the inputs, pause and resume.
- [Communication protocols: Primary Interface: data streaming](references/pages/data-streaming.md): Receive the state of a UR cobot at 10 Hz with the Primary Interface: robot mode, joints, tool, I/O, Cartesian position, kinematics and configuration.
- [Communication protocols: Send URScript](references/pages/remote-send-script.md): Send URScript to a UR cobot with the Primary Interface: a line, a program or a secondary program, and their effect on the running program.
- [Communication protocols: Dashboard Server: remote commands](references/pages/remote-commands.md): Power, brakes, programs, popups, robot mode and safety status of a UR cobot with the Dashboard Server of PolyScope 5. All the commands of the SDK.
- [Communication protocols: REST API (PolyScope X)](references/pages/rest-api.md): Control a UR cobot with PolyScope X over HTTP: power, brakes, load, play and stop programs, read the program state. Replaces the Dashboard Server.
- [Communication protocols: SFTP file handling](references/pages/sftp-file-handling.md): Download, upload, list, rename and delete the files of a UR controller with SFTP: programs, installations and any other file.
- [Communication protocols: SSH Linux commands](references/pages/ssh-commands.md): Run Linux commands on the controller of a UR cobot with SSH, one by one or in a shell that keeps its session.
- [Communication protocols: XML-RPC](references/pages/xml-rpc.md): Answer the XML-RPC calls of a UR robot program from your application: positions, numbers, text. The SDK is the server.
- [Communication protocols: Interpreter Mode](references/pages/interpreter-mode.md): Send URScript statements to a running UR program in interpreter_mode(), follow their execution, skip or clear the buffer, end the mode.
- [Communication protocols: Socket communication](references/pages/socket-communication.md): Exchange your own messages with a UR robot program through the socket functions of URScript. The SDK is the socket server.
- [Offline Toolbox: Forward and inverse kinematics](references/pages/kinematics.md): Compute the forward and inverse kinematics of UR cobots without a robot: DH parameters of each model, flange pose, up to 8 solutions, singularities.
- [Offline Toolbox: Convert position types](references/pages/tools.md): Convert the orientation of a UR pose between rotation vector, roll pitch yaw, 4x4 transform and quaternion with the Pose class.
- [Offline Toolbox: Program and installation files](references/pages/archive-file.md): Open the .urp program and .installation files of a UR cobot on the PC, read and change their XML, and save them again.
- [How-To Articles: Get the robot position](references/pages/how-to-get-position.md): Read the joint positions and the TCP position of a UR cobot in C# or Python, with RTDE up to 500 Hz or with the Primary Interface.
- [How-To Articles: Read and write I/O](references/pages/how-to-read-write-io.md): Read and write the digital and analog I/O of a UR cobot in C# or Python, with RTDE and its masks, or with the Primary Interface.
- [How-To Articles: Read and write variables](references/pages/variables.md): Read the program and installation variables of a UR cobot in C# or Python with the Primary Interface or the Dashboard Server, and how to change them.
- [How-To Articles: Read and write registers](references/pages/registers.md): Exchange values between a UR robot program and a PC with the boolean, integer and float registers, with RTDE up to 500 Hz.
- [How-To Articles: Run a program](references/pages/how-to-run-program.md): Power on a UR cobot, release the brakes, load a program and play it from a PC in C# or Python, then follow it until its end.
- [How-To Articles: Read and reset alarms](references/pages/how-to-read-reset-alarms.md): Read the error messages, the program errors and the safety status of a UR cobot in C# or Python, and reset a protective stop or a safety fault.
- [How-To Articles: Transfer files and backups](references/pages/how-to-transfer-files.md): Copy the programs of a UR cobot to a PC for a backup, send a program to the robot and load it, in C# or Python with SFTP.
- [How-To Articles: Monitor the state of the robot](references/pages/how-to-monitor-state.md): Follow the robot mode, the program, the stops, the safety status and the connection of a UR cobot in C# or Python.
- [How-To Articles: Move the robot from a PC](references/pages/how-to-move-robot.md): Move a UR cobot from a PC in C# or Python with URScript, the Interpreter Mode, registers or a program, and check the position reached.
