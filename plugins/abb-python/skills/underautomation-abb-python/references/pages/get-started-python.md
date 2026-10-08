# Get started with Python

Install the ABB SDK from PyPI and talk to an IRC5 or an OmniCore controller from Python 3.7 to 3.13, on Windows, Linux and macOS. Same features as the .NET library, with Python names.

Web page: https://underautomation.com/abb/documentation/get-started-python

This page shows how to install the ABB SDK for Python and write a first program for an IRC5 or OmniCore controller. The Python package has the same features as the .NET library, with Python names.

## How it works

The package `UnderAutomation.ABB` contains the .NET library `UnderAutomation.ABB.dll` and a Python layer that calls it through [pythonnet](https://github.com/pythonnet/pythonnet). pythonnet runs .NET code in the Python process. Nothing is installed on the controller.

| Item             | Supported                                                                           |
| ---------------- | ----------------------------------------------------------------------------------- |
| Python           | 3.7 to 3.13                                                                         |
| pythonnet        | 3.0.5, installed with the package                                                   |
| Operating system | Windows, Linux, macOS                                                               |
| Controllers      | IRC5 with RobotWare 6 and OmniCore with RobotWare 7, real or virtual in RobotStudio |

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

from underautomation.abb.abb_controller import AbbController
```

## Install from PyPI

Install the package in a virtual environment:

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux and macOS
source .venv/bin/activate

pip install UnderAutomation.ABB
```

Package page: [pypi.org/project/UnderAutomation.ABB](https://pypi.org/project/UnderAutomation.ABB)

## Install from the sources

```bash
git clone https://github.com/underautomation/ABB.py.git
cd ABB.py
pip install -e .
```

The repository also holds runnable examples, one folder per feature: `examples/controller`, `examples/io`, `examples/rapid`, `examples/motion`, and others.

## Use the SDK with an AI agent

An AI agent such as Claude Code, Codex, GitHub Copilot or Cursor can write your Python code with the SDK. Without help, it does not know which protocol to use, which controller option is needed, or the exact names of the API, so it can invent members that do not exist. The UnderAutomation skill gives it the documentation of this version of the SDK: protocols, controller settings, API in Python, errors and safety rules for robot motion.

With the skill installed, you can ask for example:

> What do I need on my OmniCore controller to write a RAPID variable from my application?

> Write a program that reads the robot position and the digital inputs of my ABB robot.

Install the skill in your project:

```bash
npx skills add underautomation/skills --skill underautomation-abb-python
```

With Claude Code, you can also install it as a plugin:

```bash
claude plugin marketplace add underautomation/skills
claude plugin install abb-python@underautomation
```

Or paste this prompt to your agent: "Install the UnderAutomation ABB skill: follow https://underautomation.com/abb/documentation/ai-skills.md". The other installation modes are in [AI agent skills](https://underautomation.com/abb/documentation/ai-skills).

## First program

Import `AbbController`, connect and call a service.

```python
from underautomation.abb.abb_controller import AbbController

# Without a key, the SDK runs in its 30 day trial period.
# With a license, register it once, before the first connection.
AbbController.register_license("YourCompanyName", "YOUR_LICENSE_KEY")

# The whole SDK is reachable from a single object
robot = AbbController()
robot.connect("192.168.0.1")

# Controller identity
identity = robot.rws.controller.get_identity()
print(f"Connected to {identity.name}")

# RAPID tasks
for task in robot.rws.rapid.get_tasks():
    print(f"{task.name} : {task.execution_state}")

robot.disconnect()
```

The SDK runs for 30 days without a key. After that, `register_license` is needed: see [Licensing](license.md).

The default parameters target an OmniCore controller. For an IRC5 with RobotWare 6, set the RWS version. See [Connect to your robot](connect.md) for the connection parameters. When the controller answers on HTTPS with a certificate it signed itself, the SDK accepts it and enables TLS 1.2: nothing has to be set in Python.

## How the names are written

The Python package follows the .NET API, with Python names:

| .NET                                           | Python                                            |
| ---------------------------------------------- | ------------------------------------------------- |
| `robot.Rws.Controller.GetIdentity()`           | `robot.rws.controller.get_identity()`             |
| `robot.Rws.MotionSystem.GetRobTarget("ROB_1")` | `robot.rws.motion_system.get_rob_target("ROB_1")` |
| `identity.MacAddress`                          | `identity.mac_address`                            |
| `AbbController.RegisterLicense(...)`           | `AbbController.register_license(...)`             |
| `ControllerState.MotorsOn`                     | `ControllerState.MotorsOn`                        |

Methods and properties become snake*case. Enumeration values keep the name they have in .NET. A value whose name is a Python keyword gets a trailing underscore: `RapidRegainMode.Continue*`, `RapidStartCondition.None*`, `RapidTextQueryMode.Try*`.

Each type is in its own module, named after it:

```python
# One module per type, named after the type in snake case
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.connection_parameters import ConnectionParameters
from underautomation.abb.rws.rws_version import RwsVersion
from underautomation.abb.rws.data.controller_state import ControllerState
from underautomation.abb.common.pose import Pose
```

## Errors

Every failure reported by the controller raises an `RwsException`. It comes from the .NET runtime: import it from its .NET namespace, after the import of the package. Its members keep their .NET names: `StatusCode`, `RwsErrorCode`, `RwsErrorMessage`, `ResponseBody`.

```python
from underautomation.abb.abb_controller import AbbController
from UnderAutomation.ABB.Rws import RwsException

robot = AbbController()
robot.connect("192.168.0.1")

try:
    robot.rws.io.set_signal_value("Local", "PANEL", "DO_Gripper", 1)
except RwsException as ex:
    # The exception comes from the .NET runtime, so its members keep their original names.
    # StatusCode is the HTTP status code the controller answered
    if ex.StatusCode == 403:
        print("Mastership is held elsewhere, or the user account lacks the grant")
    elif ex.StatusCode == 404:
        print("This signal does not exist on this controller")
    else:
        print(f"RWS error {ex.StatusCode} : {ex.RwsErrorMessage}")

robot.disconnect()
```

## Differences with the .NET API

- The asynchronous methods are not wrapped. Every service method is available in its synchronous form.
- The file service reads and writes bytes, not text or streams. Decode and encode in your own code: `bytes(robot.rws.file.get_file_as_bytes(path)).decode("utf-8")`.
- Python has no method overloading, so a .NET method that exists in several forms is wrapped once. The mastership is an example: it is always taken with the domain it applies to, `robot.rws.mastership.request(MastershipDomain.Rapid)`. To hold every domain, as the parameterless .NET call does, take them one by one:

```python
from underautomation.abb.abb_controller import AbbController

robot = AbbController()
robot.connect("192.168.0.1")

# The parameterless .NET Request() is not wrapped: take the domains one by one
domains = robot.rws.mastership.get_domains()
for domain in domains:
    robot.rws.mastership.request(domain)

try:
    pass  # changes that need every domain
finally:
    for domain in domains:
        robot.rws.mastership.release(domain)

robot.disconnect()
```

## What to read next

- [Connect to your robot](connect.md): connection parameters, IRC5 and OmniCore, errors.
- [Test with a RobotStudio virtual controller](virtual-controller.md): work without a real robot.
- [AI agent skills](https://underautomation.com/abb/documentation/ai-skills): install the Python skill of the SDK in Claude Code, Codex, GitHub Copilot or Cursor.
- [Robot Web Services overview](rws.md): the services of the SDK, one page per topic. Every code sample has a Python tab.
- [Licensing](license.md): the 30 day trial and the license key.
