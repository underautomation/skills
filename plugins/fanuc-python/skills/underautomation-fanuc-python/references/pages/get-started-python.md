# Get started with Python

Install the Fanuc SDK from PyPI and control a Fanuc controller or ROBOGUIDE from Python 3.7 to 3.13, on Windows, Linux and macOS. Same features as the .NET library, with Python names.

Web page: https://underautomation.com/fanuc/documentation/get-started-python

This page shows how to install the Fanuc SDK for Python and write a first program for a Fanuc controller or a ROBOGUIDE virtual robot. The Python package has the same features as the .NET library, with Python names.

## How it works

### The package

The package `UnderAutomation.Fanuc` contains the .NET library `UnderAutomation.Fanuc.dll` and a Python layer that calls it through [pythonnet](https://github.com/pythonnet/pythonnet). pythonnet runs .NET code in the Python process. Nothing is installed on the controller, and no PCDK or Robot Interface is needed on the PC.

| Item             | Supported                                                         |
| ---------------- | ----------------------------------------------------------------- |
| Python           | 3.7 to 3.13                                                       |
| pythonnet        | 3.0.5, installed with the package                                 |
| Operating system | Windows, Linux, macOS                                             |
| Controllers      | R-J3iB, R-30iA, R-30iB, R-30iB Plus, R-50iA, and ROBOGUIDE robots |

### Windows

The DLL runs on the .NET Framework 4.x of Windows. Nothing else to install.

### Linux and macOS

Install the .NET runtime (for example .NET 8), then select it for pythonnet before you start Python. Without this, pythonnet uses Mono, its default runtime on Linux and macOS.

```bash
sudo apt-get install -y dotnet-runtime-8.0
```

Always write the `export`: a variable set without it does not reach the Python process. The same choice can be made in code, before the first import of the package:

```python
# Linux and macOS: use the .NET runtime instead of Mono.
# Same effect as "export PYTHONNET_RUNTIME=coreclr", before the first import of the SDK.
from pythonnet import load

load("coreclr")

from underautomation.fanuc.fanuc_robot import FanucRobot
```

## Install

### From PyPI

Install the package in a virtual environment:

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux and macOS
source .venv/bin/activate

pip install UnderAutomation.Fanuc
```

Package page: [pypi.org/project/UnderAutomation.Fanuc](https://pypi.org/project/UnderAutomation.Fanuc)

### From the sources

```bash
git clone https://github.com/underautomation/Fanuc.py.git
cd Fanuc.py
pip install -e .
```

## Use the SDK with an AI agent

An AI agent such as Claude Code, Codex, GitHub Copilot or Cursor can write your Python code with the SDK. Without help, it does not know which protocol to use, which controller option is needed, or the exact names of the API, so it can invent members that do not exist. The UnderAutomation skill gives it the documentation of this version of the SDK: protocols, controller settings, API in Python, errors and safety rules for robot motion.

With the skill installed, you can ask for example:

> Which protocol should I use to read the position registers of my Fanuc robot?

> Write a program that reads R[1] to R[10] and prints them.

Install the skill in your project:

```bash
npx skills add underautomation/skills --skill underautomation-fanuc-python
```

With Claude Code, you can also install it as a plugin:

```bash
claude plugin marketplace add underautomation/skills
claude plugin install fanuc-python@underautomation
```

Or paste this prompt to your agent: "Install the UnderAutomation Fanuc skill: follow https://underautomation.com/fanuc/documentation/ai-skills.md". The other installation modes are in [AI agent skills](https://underautomation.com/fanuc/documentation/ai-skills).

## First program

### Connect and read a register

Import `FanucRobot`, connect and read a value.

```python
from underautomation.fanuc.fanuc_robot import FanucRobot

# Without a key, the SDK runs in its 30 day trial period.
# With a license, register it once, before the first connection.
FanucRobot.register_license("YourCompanyName", "YOUR_LICENSE_KEY")

# With an IP address only, the SDK connects to the web server of the controller (CGTP)
robot = FanucRobot()
robot.connect("192.168.0.1")

# Numeric register R[1]
r1 = robot.cgtp.read_numeric_register_with_comment(1)
print(f"R[1] = {r1}")

# Current position of motion group 1
position = robot.cgtp.read_cartesian_position()
print(f"X={position.x}, Y={position.y}, Z={position.z}")

robot.disconnect()
```

With an IP address only, `connect` uses the web server of the controller (CGTP). It needs no option on the controller, and firmware V8.30 or later (V9.10 for the position). To use Telnet KCL, FTP, SNPX, RMI or Stream Motion, enable them in a `ConnectionParameters` object: see [Connect to your robot](connect.md). For a ROBOGUIDE robot, pass the folder of the robot instead of the IP address: see [Test with ROBOGUIDE](simulator.md).

### License

The SDK runs for 30 days without a key. After that, `register_license` is needed: see [Licensing](license.md).

## How the names are written

### Methods, properties and enumerations

The Python package follows the .NET API, with Python names. Every page of this documentation has a Python tab next to the C# code.

| .NET                                               | Python                                                 |
| -------------------------------------------------- | ------------------------------------------------------ |
| `robot.Snpx.NumericRegisters.Read(1)`              | `robot.snpx.numeric_registers.read(1)`                 |
| `parameters.Telnet.TelnetKclPassword`              | `parameters.telnet.telnet_kcl_password`                |
| `FanucRobot.RegisterLicense(...)`                  | `FanucRobot.register_license(...)`                     |
| `CgtpIoPortType.DO`                                | `CgtpIoPortType.DO`, an `IntEnum`                      |
| `RmiLinearSpeedType.MmSec`                         | `RmiLinearSpeedType.MmSec`                             |
| An array, like `JointsPosition[]`                  | A list-like object. `list(...)` copies it              |
| A nullable value, like `int?`                      | `int \| None`                                          |

Methods and properties become snake_case. Enumeration values keep the name they have in .NET. A name that is a Python keyword gets a trailing underscore: `robot.telnet.continue_(...)`, `robot.rmi.continue_()`, `CgtpProgramSubType.None_`.

### Modules

Each type is in its own module, named after it in snake_case. The modules follow the .NET namespaces:

```python
# UnderAutomation.Fanuc.FanucRobot
from underautomation.fanuc.fanuc_robot import FanucRobot

# UnderAutomation.Fanuc.ConnectionParameters
from underautomation.fanuc.connection_parameters import ConnectionParameters

# UnderAutomation.Fanuc.Common.Languages
from underautomation.fanuc.common.languages import Languages

# UnderAutomation.Fanuc.Cgtp.CgtpIoPortType
from underautomation.fanuc.cgtp.cgtp_io_port_type import CgtpIoPortType
```

The motion planner, common to the UnderAutomation robot SDKs, is in the `underautomation.robotics` modules.

## Differences with the .NET API

- The offline file readers (`FanucFileReaders`) are not wrapped yet. To read a variable or diagnostic file of the controller, use the FTP client: `robot.ftp.known_variable_files`, `robot.ftp.get_safety_status()`...
- A .NET event becomes a method that registers a Python function: `robot.telnet.command_sent(on_command_sent)`. The function is called from a thread of the SDK.
- A .NET method that exists in several forms is wrapped once, with optional arguments.
- With Stream Motion, prefer the target tracking to a callback that computes each position: the timing of a Python callback depends on the interpreter. See [Real-time control](stream-motion-real-time.md).

## Errors

A failure of the SDK raises the .NET exception, for example `InvalidLicenseException` when the license is not valid, or an `Exception` when the controller does not answer the ping that precedes the connection. It is a Python exception: catch it with `except Exception as e` and read `str(e)`.

## Examples

The repository [Fanuc.py](https://github.com/underautomation/Fanuc.py) holds runnable scripts in the folder `examples`, one folder per feature: `cgtp`, `snpx`, `telnet`, `ftp`, `stream_motion`, `motion`, `kinematics`, `license`.

```bash
python examples/snpx/snpx_read_numeric_register.py
python examples/launcher.py
```

The first run asks the address of the robot (or the folder of the ROBOGUIDE robot) and the credentials, and saves them in `examples/robot_config.json`. `launcher.py` lists the scripts by category and runs the one you choose. The scripts that move the robot (RMI, Stream Motion) need the surroundings of the robot to be checked first.

## What to read next

- [Connect to your robot](connect.md): the protocols, their setup on the controller, the connection parameters.
- [Test with ROBOGUIDE](simulator.md): work without a real robot.
- [AI agent skills](https://underautomation.com/fanuc/documentation/ai-skills): install the Python skill of the SDK in Claude Code, Codex, GitHub Copilot or Cursor.
- The protocol pages: [CGTP](cgtp.md), [SNPX](snpx.md), [Telnet](telnet.md), [FTP](ftp.md), [RMI](rmi.md), [Stream Motion](stream-motion.md).
- [Licensing](license.md): the 30 day trial and the license key.
