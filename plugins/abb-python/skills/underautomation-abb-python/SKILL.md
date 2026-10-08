---
name: underautomation-abb-python
description: "UnderAutomation ABB SDK for Python (pip UnderAutomation.ABB, import underautomation.abb). Use it when Python code talks to an ABB robot controller (IRC5 with RobotWare 6, OmniCore with RobotWare 7) or a RobotStudio virtual controller, or when the user asks about the ABB SDK, Robot Web Services or its exceptions. Protocol of the SDK: Robot Web Services (RWS 1.0 on IRC5, RWS 2.0 on OmniCore), plus the discovery of the controllers of the network. It answers questions such as which RWS version and which mastership domain to use, how to read and write RAPID variables and I/O signals, how to start and stop a RAPID program, read the robot position, jog the robot, compute the kinematics, manage files, backups and the event log, and why an RwsException is raised. It holds the documentation pages, the Python code samples and the list of every public class and member of the package, with the Python names."
metadata:
  sdk-version: 1.1.0
---

# UnderAutomation ABB SDK for Python

The UnderAutomation ABB SDK connects a PC to an ABB robot controller (IRC5 with RobotWare 6, OmniCore with RobotWare 7) or to a RobotStudio virtual controller over Robot Web Services (RWS), the HTTP interface of the controller. Nothing is installed on the robot. The main class is `AbbController` (`from underautomation.abb.abb_controller import AbbController`): the nine services of RWS are properties of `robot.rws`.

## Before writing code

1. Run `pip show UnderAutomation.ABB` in the environment of the project. If the package is missing, ask the user before you install it with `pip install UnderAutomation.ABB`.
2. Compare its version with `sdk-version` above (1.1.0). A 4th version digit is the same release: for example pip 1.1.0.1 and `sdk-version` 1.1.0. If they differ, tell the user: an older package can miss members listed here, a newer one can have members that this skill does not list.
3. On Linux and macOS, the package needs a .NET runtime: see [Get started with Python](references/pages/get-started-python.md).
4. When you cannot run commands (claude.ai, ChatGPT), skip the check and tell the user that this skill documents version 1.1.0 of the SDK.

## Choose the service and the controller state

The SDK has one protocol, RWS. A generic agent does not know which RWS version a controller speaks, nor which mastership, operation mode and option a write needs. Use this table, then open the page of the service.

| What the user wants to do | Service | What the controller needs |
| --- | --- | --- |
| Read anything: position, I/O, RAPID variables, states, event log, files | Any service | A valid user account. No mastership, any operation mode |
| Write a RAPID variable, load or unload a module, move the program pointer | `rws.rapid` | Mastership of the `Rapid` domain. Many RAPID writes are refused in manual mode |
| Start a RAPID program | `rws.rapid.start` | Automatic mode, motors on, `Rapid` mastership, a program loaded and built, a program pointer. A start refused with HTTP 500 means one of them is missing |
| Stop a RAPID program | `rws.rapid.stop` | No mastership. A stop is not an emergency stop |
| Read and write I/O signals | `rws.io` | A signal with write access for the user. On a bare virtual controller, every signal write answers 403 |
| Motors on and off, speed ratio, operation mode | `rws.panel` | The operation mode is set with the key of the controller, an application cannot change it. The speed ratio is accepted in automatic mode only |
| Jog the robot, or move it to a Cartesian target | `rws.motion_system` | Manual mode, motors on, this client as the local client of the controller, `Motion` mastership. In automatic mode the request is refused with 403 |
| Read the position, compute forward and inverse kinematics | `rws.motion_system` | Nothing. The kinematics calculations work in metres and radians, the positions in millimetres and degrees |
| System parameters, network, time zone | `rws.controller` | Mastership of the `Configuration` domain. Several of them need a real controller |
| Files, backup and restore | `rws.file`, `rws.controller` | A user account with the matching grant |
| Find the controllers of the network | `AbbController.discover` | Nothing: no connection and no license. Same local network only |

- RWS version: `RwsVersion.Irc5_V1_0` for an IRC5 (RobotWare 6), `RwsVersion.OmniCore_V2_0` for an OmniCore (RobotWare 7, the default). A wrong version gives an `RwsException` with HTTP 404 on the first request. Ask the user which controller they have when the code does not say it. See [IRC5 or OmniCore](references/pages/irc5-vs-omnicore.md).
- HTTP or HTTPS (`use_https`) does not depend on the RWS version: it depends on the setup of the controller. Port 0 means 80 for HTTP and 443 for HTTPS. A self-signed certificate is accepted.
- Default user account: `Default User`, password `robotics`. A write also needs the matching grant of the User Authorization System (UAS) on the account.
- Mastership is the write lock of the controller. Take it just before the write, release it in a `finally` block. IRC5 has the domains `Configuration`, `Rapid` and `Motion`. OmniCore has `Edit` (system parameters and RAPID together) and `Motion`. Any of the 4 values of `MastershipDomain` works on both controllers. `panel.set_speed_ratio` and `controller.restart` take the mastership themselves on OmniCore. See [Mastership](references/pages/rws-mastership.md).
- HTTP 403 means: mastership held by another client (often the FlexPendant), missing UAS grant, or an operation mode that does not allow the action. Read `mastership.get_info()` and `held_by_me` to tell them apart.
- RAPID symbols are addressed as `RAPID/<task>/<module>/<name>`, for example `RAPID/T_ROB1/MainModule/myFlag`. Values are RAPID text: a dot as decimal separator, `TRUE` or `FALSE`, quotes around a string. See [Read & write RAPID variables](references/pages/read-write-rapid-variables.md).
- Options of the controller: Collision Detection, the Safety Module and the key-less mode selector are RobotWare options. Without them, the matching requests are refused with an error that names the option.
- The SDK has no event subscription: poll the state. The configuration database (CFG), the UAS management, the manual mode privileges (RMMP) and the RAPID message queues are not wrapped yet, see [Roadmap](references/pages/rws-roadmap.md). Do not invent methods for them.
- A controller accepts about 70 sessions (OmniCore). Connect once and disconnect at the end: a loop that connects without disconnecting gets HTTP 503.
- RobotStudio: connect to `127.0.0.1`, with the RWS version of the RobotWare of the virtual controller. `robot.rws.system.get_license()` returns `VIRTUAL_USE` on a virtual controller. See [Test with a RobotStudio virtual controller](references/pages/virtual-controller.md).
- The Python package has no asynchronous methods. An `RwsException` comes from the .NET runtime: catch it with `from UnderAutomation.ABB.Rws import RwsException`, and read its .NET members (`ex.StatusCode`, `ex.RwsErrorMessage`).

The how-to pages give the details per task: [Start & stop a RAPID program](references/pages/start-stop-rapid-program.md), [Get the robot position](references/pages/get-robot-position.md), [Read & write I/O signals](references/pages/read-write-io-signals.md) and [Backup & restore a controller](references/pages/backup-restore-controller.md).

## Connect and license

Create an `AbbController` and connect. `connect(ip)` uses the default parameters: OmniCore, HTTP, `Default User`. For an IRC5, HTTPS or another account, use `ConnectionParameters`. Always disconnect at the end. See [Connect to your robot](references/pages/connect.md).

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.connection_parameters import ConnectionParameters
from underautomation.abb.rws.rws_version import RwsVersion

parameters = ConnectionParameters("192.168.0.1")

# Ping the controller first, so an unreachable robot fails immediately
parameters.ping_before_connect = True

parameters.rws.enable = True
parameters.rws.username = "Default User"
parameters.rws.password = "robotics"
parameters.rws.use_https = False
parameters.rws.port = 0  # 0 means 80 for HTTP and 443 for HTTPS
parameters.rws.timeout = 10000
parameters.rws.version = RwsVersion.OmniCore_V2_0

robot = AbbController()
robot.connect(parameters)

robot.disconnect()
```

The SDK runs 30 days without a license key. With a key, register it once at startup, before the first connection. Without a valid license, the connection raises an `InvalidLicenseException`. The discovery of the controllers does not need a license. See [Licensing](references/pages/license.md).

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.license.license_state import LicenseState
from UnderAutomation.ABB.License import InvalidLicenseException

# Register the license once, before the first connection
AbbController.register_license("YourCompanyName", "YOUR_LICENSE_KEY")

robot = AbbController()
info = robot.license_info

# Number of trial days remaining, None when the product is licensed
evaluation_days_left = info.evaluation_days_left

license_valid = info.state == LicenseState.Licensed

# A readable description of the current state
print(info)

# Check the license once at startup, rather than catching the exception
# on every connection
if not info.is_licensed:
    print(info)
    raise SystemExit(0)

# Without a key the library runs in its 30 day trial period.
# connect raises an InvalidLicenseException once the trial has expired.
try:
    robot = AbbController()
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
- Propose a first test on a virtual robot: [Test with a RobotStudio virtual controller](references/pages/virtual-controller.md).
- The SDK does not replace the safety functions of the controller (emergency stop, safety fences, collision detection).

## Rules for the agent

- Use only the types and members listed in `references/api`. Search `references/api/index.md` for a type, then open the file of its namespace.
- If a member seems missing, do not guess it: read the installed package: `pip show -f UnderAutomation.ABB` gives its folder in `site-packages`, the classes are in `underautomation/abb/`.
- Start from the code samples of `references/pages`: their names are checked against this version of the package.
- Use the Python names (snake_case) of this skill. The .NET names (PascalCase) of the C# documentation do not exist in the Python package, except on a caught exception (next rule).
- Exceptions: the SDK raises the .NET exception. Catch it with its .NET type, imported from its .NET namespace, for example `from UnderAutomation.ABB.Rws import RwsException`, then `except RwsException as e`. Its members keep their .NET names: `e.Message`, `e.InnerException`. The classes of the same name in the `underautomation.abb` modules are not Python exceptions: `except` on one of them raises a `TypeError`. For the list and what to check, read `references/errors.md`.
- When the answer depends on the controller (model, software version, options, settings), ask the user.

## Index of the references

- [API index](references/api/index.md): every public type, with the file of its namespace.
- [Errors](references/errors.md): exceptions of the SDK, when they are raised, what to check.
- [Get started: Get started with Python](references/pages/get-started-python.md): Install the ABB SDK from PyPI and talk to an IRC5 or an OmniCore controller from Python 3.7 to 3.13, on Windows, Linux and macOS. Same features as the .NET library, with Python names.
- [Get started: Try the SDK with the demo application](references/pages/demo-app.md): A ready made Windows application, single executable and open source, that exposes every function of the SDK. Test what your controller answers before writing any code.
- [Get started: Connect to your robot](references/pages/connect.md): Configure the connection to an IRC5 or OmniCore controller, choose the Robot Web Services version, and use the synchronous or asynchronous API.
- [Get started: Discover controllers on the network](references/pages/discover-controllers.md): Find the ABB controllers of the local network and the virtual controllers of this machine, without a license and without an existing connection.
- [Get started: Test with a RobotStudio virtual controller](references/pages/virtual-controller.md): Run the SDK without a real robot. Create a virtual controller in ABB RobotStudio and enable Robot Web Services on it.
- [Get started: Licensing](references/pages/license.md): To be used, this SDK is subject to licensing. You have 30 days to test it for free.
- [Robot Web Services: Robot Web Services overview](references/pages/rws.md): Robot Web Services (RWS) is the REST interface of ABB robot controllers. One API covers RWS 1.0 on IRC5 and RWS 2.0 on OmniCore.
- [Robot Web Services: Controller: identity, clock & backup](references/pages/rws-controller.md): Read controller identity and options, set the clock, the time zone and the network configuration, restart the controller, create and restore backups, read the safety state.
- [Robot Web Services: Control panel & operation mode](references/pages/rws-panel.md): Read and change the operation mode, the controller state (motors on/off), the speed ratio, and the collision detection state.
- [Robot Web Services: RAPID tasks & program execution](references/pages/rws-rapid-tasks.md): List RAPID tasks, start and stop program execution, follow the execution state, move the program pointer, load and unload modules.
- [Robot Web Services: RAPID variables & symbols](references/pages/rws-rapid-symbols.md): Read and write RAPID variables, persistents and constants, search symbols in the loaded program, and validate a value before writing it.
- [Robot Web Services: RAPID modules & program files](references/pages/rws-rapid-modules.md): Load, save and unload RAPID programs, read and edit module source text, manage breakpoints, read build errors and modify taught positions.
- [Robot Web Services: I/O signals, devices & networks](references/pages/rws-io.md): Read and write digital, analog and group signals, pulse or invert a signal, and browse the I/O devices and networks of the controller.
- [Robot Web Services: Motion system, position & kinematics](references/pages/rws-motion.md): Read the robot position as a robtarget or a jointtarget, jog the robot, compute forward and inverse kinematics, and manage mechanical units and calibration.
- [Robot Web Services: File system](references/pages/rws-files.md): Browse the controller file system, download and upload files, create, copy, rename and delete files and directories.
- [Robot Web Services: Event log](references/pages/rws-elog.md): Read the controller event log, filter by domain and language, get the arguments of a message, and clear the log.
- [Robot Web Services: Mastership](references/pages/rws-mastership.md): Mastership is the write lock of the controller. Request and release it explicitly, or let the SDK take it implicitly for a single call.
- [Robot Web Services: System information & energy](references/pages/rws-system.md): Read the RobotWare version, the installed options and products, the robot types of the system, and the energy consumption counters.
- [Robot Web Services: Roadmap: operations not wrapped yet](references/pages/rws-roadmap.md): Robot Web Services offers more operations than the SDK wraps today. This page lists what is on the roadmap, and how to have an operation prioritized for your project.
- [How-To Articles: IRC5 or OmniCore: which RWS version](references/pages/irc5-vs-omnicore.md): RWS 1.0 runs on IRC5 with RobotWare 6, RWS 2.0 on OmniCore with RobotWare 7. Compare both, and see what changes in your code.
- [How-To Articles: Read & write RAPID variables](references/pages/read-write-rapid-variables.md): Read and write a RAPID num, bool, string, robtarget or a custom record from C#, on IRC5 and on OmniCore.
- [How-To Articles: Get the robot position](references/pages/get-robot-position.md): Read the current Cartesian position (robtarget) and the joint position (jointtarget) of an ABB robot, and convert between them.
- [How-To Articles: Start & stop a RAPID program](references/pages/start-stop-rapid-program.md): Start, stop and reset a RAPID program remotely: motors on, program pointer, execution cycle, and how to check that it really started.
- [How-To Articles: Read & write I/O signals](references/pages/read-write-io-signals.md): Read and write digital, analog and group I/O signals of an ABB controller, pulse a signal and simulate one during tests.
- [How-To Articles: Backup & restore a controller](references/pages/backup-restore-controller.md): Create a full controller backup, download it to your PC, check it and restore it, entirely from your application.
