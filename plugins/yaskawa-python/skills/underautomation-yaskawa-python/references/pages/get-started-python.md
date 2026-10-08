# Get started with Python

Install the Yaskawa SDK from PyPI and control a Motoman controller from Python 3.7 to 3.13, on Windows, Linux and macOS. Same functions as the .NET library, with Python names.

Web page: https://underautomation.com/yaskawa/documentation/get-started-python

This page shows how to install the Yaskawa SDK for Python and write a first program for a Yaskawa Motoman controller. The Python package has the same functions as the .NET library, with Python names.

## How it works

The package `UnderAutomation.Yaskawa` contains the .NET library `UnderAutomation.Yaskawa.dll` and a Python layer that calls it through [pythonnet](https://github.com/pythonnet/pythonnet). pythonnet runs .NET code in the Python process. Nothing is installed on the controller.

| Item             | Supported                                                            |
| ---------------- | -------------------------------------------------------------------- |
| Python           | 3.7 to 3.13                                                          |
| pythonnet        | 3.0.5, installed with the package                                    |
| Operating system | Windows, Linux, macOS                                                |
| Controllers      | YRC1000 (micro), MOTOMAN NEXT, DX100 / DX200, FS100, ERC / XRC / MRC |

- **Windows:** the DLL runs on the .NET Framework 4.x of Windows. Nothing else to install.
- **Linux and macOS:** install the .NET runtime (for example .NET 8), then select it for pythonnet before you start Python. Without this, pythonnet uses Mono, its default runtime on Linux and macOS.

```bash
sudo apt-get install -y dotnet-runtime-8.0
```

Always write the `export`: a variable set without it does not reach the Python process. The same choice can be made in code, before the first import of the package:

```python
# Linux and macOS: use the .NET runtime instead of Mono.
# Same effect as "export PYTHONNET_RUNTIME=coreclr", before the first import of the SDK.
from pythonnet import load

load("coreclr")

from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
```

## Install from PyPI

Install the package in a virtual environment:

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux and macOS
source .venv/bin/activate

pip install UnderAutomation.Yaskawa
```

Package page: [pypi.org/project/UnderAutomation.Yaskawa](https://pypi.org/project/UnderAutomation.Yaskawa)

## Install from the sources

```bash
git clone https://github.com/underautomation/Yaskawa.py.git
cd Yaskawa.py
pip install -e .
```

The repository also holds runnable examples, one file per function, in `examples/high_speed_e_server` (for example `hses_get_status.py`, `hses_read_write_io.py`). Run `python examples/launcher.py` to choose one from a menu. The first run asks the address of the controller and saves it in `examples/robot_config.json`.

## Use the SDK with an AI agent

An AI agent such as Claude Code, Codex, GitHub Copilot or Cursor can write your Python code with the SDK. Without help, it does not know which protocol to use, which controller option is needed, or the exact names of the API, so it can invent members that do not exist. The UnderAutomation skill gives it the documentation of this version of the SDK: protocols, controller settings, API in Python, errors and safety rules for robot motion.

With the skill installed, you can ask for example:

> Should I use the High Speed Ethernet Server or the Ethernet Server for my YRC1000?

> Write a program that reads the I variables 0 to 9 and the robot position.

Install the skill in your project:

```bash
npx skills add underautomation/skills --skill underautomation-yaskawa-python
```

With Claude Code, you can also install it as a plugin:

```bash
claude plugin marketplace add underautomation/skills
claude plugin install yaskawa-python@underautomation
```

Or paste this prompt to your agent: "Install the UnderAutomation Yaskawa skill: follow https://underautomation.com/yaskawa/documentation/ai-skills.md". The other installation modes are in [AI agent skills](https://underautomation.com/yaskawa/documentation/ai-skills).

## First program

Import `YaskawaRobot` and `ConnectParameters`, connect and read a value.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters

# Without a key, the SDK runs in its 30 day trial period.
# With a license, register it once, before the first connection.
YaskawaRobot.register_license("YourCompanyName", "YOUR_LICENSE_KEY")

# The whole SDK is reachable from a single object
robot = YaskawaRobot()
robot.connect(ConnectParameters("192.168.0.1"))

# Read the position of the tool center point, in mm and degrees
p = robot.high_speed_e_server.get_robot_cartesian_position()
print(f"X={p.x} Y={p.y} Z={p.z} Rx={p.rx} Ry={p.ry} Rz={p.rz}")

robot.disconnect()
```

The SDK runs for 30 days without a key. After that, `register_license` is needed: see [Licensing](license.md).

## How the names are written

The Python package follows the .NET API, with Python names:

| .NET                                            | Python                                                          |
| ----------------------------------------------- | --------------------------------------------------------------- |
| `robot.HighSpeedEServer.GetStatusInformation()` | `robot.high_speed_e_server.get_status_information()`            |
| `parameters.HighSpeedEServer.DataPort`          | `parameters.high_speed_e_server.data_port`                      |
| `YaskawaRobot.RegisterLicense(...)`             | `YaskawaRobot.register_license(...)`                            |
| `position.X`, `status.ServoOn`                  | `position.x`, `status.servo_on`                                 |
| `Read16BytesChar(0, 2)`                         | `read16_bytes_char(0, 2)`                                       |
| `RobotCycleType.OneCycle`                       | `RobotCycleType.OneCycle`                                       |
| `SwitchingCommands.Continue`                    | `SwitchingCommands.Continue_`                                   |
| `short[]`, `int[]` returned                     | a .NET array: index it, iterate it, or copy it with `list(...)` |

Methods and properties become snake_case. Enumerations are Python `IntEnum` classes that keep the .NET value names: use `.name` to print the name. Each type is in a module named after it, and a method that takes a .NET array accepts a Python list:

```python
# One module per type, named after the type in snake case
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters
from underautomation.yaskawa.common.io_type import IOType
from underautomation.yaskawa.common.robot_cycle_type import RobotCycleType
from underautomation.yaskawa.high_speed_e_server.robot_control_group import RobotControlGroup

robot = YaskawaRobot()
robot.connect(ConnectParameters("192.168.0.1"))

# A .NET array parameter accepts a Python list
robot.high_speed_e_server.write_integer(0, [10, 20])

# Pass the arguments by position: their names keep the .NET spelling
values = robot.high_speed_e_server.read_integer(0, 2).value
print(list(values))
```

The arguments keep their .NET names (`firstIndex`, `RobotControlGroup`): pass them by position, or with these names.

## Errors

An error raised by the SDK comes from the .NET runtime. Import the exception class from its .NET namespace, after the import of the package. Its members keep their .NET names: `Message`, `Status`, `AddedStatus`.

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

## Differences with the .NET API

- The static fields of the .NET types have the same name in Python: `RobotControlGroup.DefaultRobotPulse`, `RobotSystemTypeData.Default`, `RobotPosture.Default`.
- The exceptions are the .NET exceptions (see above), not Python classes.

Version 2.2.0 of the package has these limits:

- `connect` takes a `ConnectParameters`: `robot.connect(ConnectParameters("192.168.0.1"))`.
- When a .NET method has several overloads, Python has the one with the most parameters. `read_io` and `write_io` take an I/O type and a group (`read_io(IOType.GeneralOutput, 1, 2)`). `get_position_error`, `get_torque`, `get_robot_position` and `get_configuration_information` take a `RobotControlGroup`, for example `RobotControlGroup.DefaultRobotPulse`. `get_system_information` takes `RobotSystemTypeData.Default`.
- To create a `RobotControlGroup`, use the `ControlGroup` enumeration of the .NET namespace: `from UnderAutomation.Yaskawa.HighSpeedEServer import ControlGroup`, after the import of the package.
- `load_file` and `get_file` take no progress callback.
- The SDK has no asynchronous methods and no events.

## What to read next

- [Connect to your robot](connect.md): the settings of the controller, the connection parameters, the errors.
- [High Speed Ethernet Server overview](high-speed-ethernet-server.md): the functions of the SDK, one page per topic. Every code sample has a Python tab.
- [Choose a protocol](protocols.md): the Ethernet Server (`robot.e_server`), HTTP (`robot.http`) and FTP (`robot.ftp`).
- [Offline kinematics](kinematics.md): `KinematicsUtils.forward_kinematics` and `inverse_kinematics`, without a controller.
- [Licensing](license.md): the 30 day trial and the license key.
- [AI agent skills](https://underautomation.com/yaskawa/documentation/ai-skills): install the Python skill of the SDK in Claude Code, Codex, GitHub Copilot or Cursor.
