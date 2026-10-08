# Get started with Python

Install the Staubli SDK from PyPI and control a CS8 or CS9 controller from Python 3.7 to 3.13, on Windows, Linux and macOS. Same functions as the .NET library, with Python names.

Web page: https://underautomation.com/staubli/documentation/get-started-python

This page shows how to install the Staubli SDK for Python and write a first program for a Staubli CS8 or CS9 controller. The Python package has the same functions as the .NET library, with Python names.

## How it works

The package `UnderAutomation.Staubli` contains the .NET library `UnderAutomation.Staubli.dll` and a Python layer that calls it through [pythonnet](https://github.com/pythonnet/pythonnet). pythonnet runs .NET code in the Python process. Nothing is installed on the controller.

| Item             | Supported                                               |
| ---------------- | ------------------------------------------------------- |
| Python           | 3.7 to 3.13                                             |
| pythonnet        | 3.0.5, installed with the package                       |
| Operating system | Windows, Linux, macOS                                   |
| Controllers      | CS8 and CS9, and the emulator of Staubli Robotics Suite |

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

from underautomation.staubli.staubli_controller import StaubliController
```

## Install from PyPI

Install the package in a virtual environment:

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux and macOS
source .venv/bin/activate

pip install UnderAutomation.Staubli
```

Package page: [pypi.org/project/UnderAutomation.Staubli](https://pypi.org/project/UnderAutomation.Staubli)

## Install from the sources

```bash
git clone https://github.com/underautomation/Staubli.py.git
cd Staubli.py
pip install -e .
```

The repository also holds runnable examples, one folder per topic: `examples/controller`, `examples/motion`, `examples/io` and `examples/applications`. The first run asks the address, the user and the password of the controller, and saves them in `examples/robot_config.json`.

## Use the SDK with an AI agent

An AI agent such as Claude Code, Codex, GitHub Copilot or Cursor can write your Python code with the SDK. Without help, it does not know which protocol to use, which controller option is needed, or the exact names of the API, so it can invent members that do not exist. The UnderAutomation skill gives it the documentation of this version of the SDK: protocols, controller settings, API in Python, errors and safety rules for robot motion.

With the skill installed, you can ask for example:

> What do I need on my Staubli CS9 controller to read the robot position from my application?

> Write a program that reads the joints and the Cartesian position of my Staubli robot.

Install the skill in your project:

```bash
npx skills add underautomation/skills --skill underautomation-staubli-python
```

With Claude Code, you can also install it as a plugin:

```bash
claude plugin marketplace add underautomation/skills
claude plugin install staubli-python@underautomation
```

Or paste this prompt to your agent: "Install the UnderAutomation Staubli skill: follow https://underautomation.com/staubli/documentation/ai-skills.md". The other installation modes are in [AI agent skills](https://underautomation.com/staubli/documentation/ai-skills).

## First program

Import `StaubliController`, connect and read a value.

```python
from underautomation.staubli.staubli_controller import StaubliController

# Without a key, the SDK runs in its 30 day trial period.
# With a license, register it once, before the first connection.
StaubliController.register_license("YourCompanyName", "YOUR_LICENSE_KEY")

# The whole SDK is reachable from a single object
controller = StaubliController()
controller.connect("192.168.0.254")

# Read the position of each joint of the first robot, in radians
joints = controller.soap.get_current_joint_position(0)
print(list(joints))

controller.disconnect()
```

The SDK runs for 30 days without a key. After that, `register_license` is needed: see [Licensing](license.md).

## How the names are written

The Python package follows the .NET API, with Python names:

| .NET                                         | Python                                                |
| -------------------------------------------- | ----------------------------------------------------- |
| `controller.Soap.GetCurrentJointPosition(0)` | `controller.soap.get_current_joint_position(0)`       |
| `parameters.Soap.User`                       | `parameters.soap.user`                                |
| `StaubliController.RegisterLicense(...)`     | `StaubliController.register_license(...)`             |
| `position.CartesianPosition.X`               | `position.cartesian_position.x`                       |
| `ReversingResult.Success`                    | `ReversingResult.Success`                             |
| `double[]`                                   | a .NET array: iterate it, or copy it with `list(...)` |

Methods and properties become snake_case. Enumerations are Python `IntEnum` classes that keep the .NET value names: use `.name` to print the name. Each type is in a module named after it, and a method that takes a .NET array accepts a Python list:

```python
# One module per type, named after the type in snake case
from underautomation.staubli.staubli_controller import StaubliController
from underautomation.staubli.connection_parameters import ConnectionParameters
from underautomation.staubli.soap.data.motion_desc import MotionDesc
from underautomation.staubli.soap.data.frame import Frame
from underautomation.staubli.soap.data.reversing_result import ReversingResult

# A .NET array parameter accepts a Python list
controller = StaubliController()
controller.connect("192.168.0.254")
states = controller.soap.read_ios([r"BasicIO-1\%I0"])
```

## Errors

An error raised by the SDK comes from the .NET runtime. Import the exception class from its .NET namespace, after the import of the package. Its members keep their .NET names: `ErrorCode`, `Description`, `Message`.

```python
from underautomation.staubli.staubli_controller import StaubliController
from UnderAutomation.Staubli.License import InvalidLicenseException
from UnderAutomation.Staubli.Soap.Errors import CustomSoapException, SoapErrorCode
from System.Net import WebException

controller = StaubliController()

# The exceptions come from the .NET runtime, so their members keep their original names
try:
    controller.connect("192.168.0.254")
    controller.soap.task_kill("myTask", "Disk://myProject/myProject.pjx")
except InvalidLicenseException as ex:
    # No valid license: the trial is over, or the key is wrong
    print(ex.LicenseInfo)
except CustomSoapException as ex:
    if ex.ErrorCode == SoapErrorCode.InvalidCredentials:
        print("Wrong user or password")
    else:
        # The controller refused the request
        print(f"{ex.ErrorCode} : {ex.Description}")
except WebException as ex:
    # No answer on the SOAP port
    print(ex.Message)
except Exception as ex:
    # For example, no answer to the ping
    print(ex)
```

## Differences with the .NET API

- Named arguments use the Python syntax: `GetCurrentJointPosition(robot: 0)` is `get_current_joint_position(robot=0)`, or `get_current_joint_position(0)`.
- The exceptions are the .NET exceptions (see above), not Python classes.
- The SDK has no asynchronous methods and no events: the Python API is the full API.

## What to read next

- [Connect to your robot](connect.md): connection parameters, errors, disconnection.
- [Test with the Staubli Robotics Suite emulator](simulator.md): work without a real robot.
- [SOAP overview](soap-overview.md): the functions of the SDK, one page per topic. Every code sample has a Python tab.
- [Licensing](license.md): the 30 day trial and the license key.
- [AI agent skills](https://underautomation.com/staubli/documentation/ai-skills): install the Python skill of the SDK in Claude Code, Codex, GitHub Copilot or Cursor.
