# Get started with Python

Install the Universal Robots SDK from PyPI and write a first Python program. Python 3.7 to 3.13 on Windows, Linux and macOS, with pythonnet.

Web page: https://underautomation.com/universal-robots/documentation/get-started-python

This page shows how to install the Universal Robots SDK for Python and write a first program for a UR cobot. The Python package has the same functions as the .NET library, with Python names.

## How it works

The package `UnderAutomation.UniversalRobots` contains the .NET library `UnderAutomation.UniversalRobots.dll` and a Python layer that calls it through [pythonnet](https://github.com/pythonnet/pythonnet). pythonnet runs .NET code in the Python process. Nothing is installed on the robot.

| Item             | Supported                                                                                         |
| ---------------- | ------------------------------------------------------------------------------------------------- |
| Python           | 3.7 to 3.13                                                                                       |
| pythonnet        | 3.0.5, installed with the package                                                                 |
| Operating system | Windows, Linux, macOS                                                                             |
| Robots           | CB-Series, e-Series, UR8 Long, UR15, UR18, UR20, UR30, with PolyScope or PolyScope X, and URSim |

- **Windows:** the DLL runs on the .NET Framework 4.x of Windows. Nothing else to install.
- **Linux and macOS:** install the .NET runtime (for example .NET 8), then select it for pythonnet before you start Python. Without this, pythonnet uses Mono, its default runtime on Linux and macOS.

```bash
sudo apt-get install -y dotnet-runtime-8.0
```

Always write the `export`: a variable set without it does not reach the Python process. The same choice can be made in code, before the first import of the package:

```python
# Linux and macOS: use the .NET runtime instead of Mono.
# Same effect as "export PYTHONNET_RUNTIME=coreclr", before the first import of the SDK
from pythonnet import load
load("coreclr")

from underautomation.universal_robots.ur import UR
```

## Install the package

### From PyPI

Install the package in a virtual environment:

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux and macOS
source .venv/bin/activate

pip install UnderAutomation.UniversalRobots
```

Package page: [pypi.org/project/UnderAutomation.UniversalRobots](https://pypi.org/project/UnderAutomation.UniversalRobots)

### From the sources

```bash
git clone https://github.com/underautomation/UniversalRobots.py.git
cd UniversalRobots.py
pip install -e .
```

The repository also holds runnable examples, one folder per interface: `examples/dashboard`, `examples/primary_interface`, `examples/rtde`, `examples/rest`, `examples/sftp`, `examples/kinematics` and `examples/license`. Run `python examples/launcher.py` to choose one from a menu. The first run asks the address of the robot and saves it in `examples/robot_config.json`.

## Use the SDK with an AI agent

An AI agent such as Claude Code, Codex, GitHub Copilot or Cursor can write your Python code with the SDK. Without help, it does not know which protocol to use, which controller option is needed, or the exact names of the API, so it can invent members that do not exist. The UnderAutomation skill gives it the documentation of this version of the SDK: protocols, controller settings, API in Python, errors and safety rules for robot motion.

With the skill installed, you can ask for example:

> Should I use RTDE or the Primary Interface to read the TCP position of my UR cobot?

> Write a program that powers on my UR robot, releases the brakes and plays a program.

Install the skill in your project:

```bash
npx skills add underautomation/skills --skill underautomation-universal-robots-python
```

With Claude Code, you can also install it as a plugin:

```bash
claude plugin marketplace add underautomation/skills
claude plugin install universal-robots-python@underautomation
```

Or paste this prompt to your agent: "Install the UnderAutomation Universal Robots skill: follow https://underautomation.com/universal-robots/documentation/ai-skills.md". The other installation modes are in [AI agent skills](https://underautomation.com/universal-robots/documentation/ai-skills).

## First program

Import `UR`, connect and read a value.

```python
import time
from underautomation.universal_robots.ur import UR

# Only after the 30 day trial: register your license key
# UR.register_license("YourCompanyName", "YOUR_LICENSE_KEY")

robot = UR()

# Connect with the default services: Primary Interface and Dashboard Server
robot.connect("192.168.0.1")

# The Primary Interface receives the state of the robot at 10 Hz
time.sleep(0.5)

# Cartesian position of the tool, in meters and radians
pose = robot.primary_interface.cartesian_info.as_pose()
print(f"X={pose.x} Y={pose.y} Z={pose.z}")

# Mode of the robot, read with the Dashboard Server
mode = robot.dashboard.get_robot_mode()
print(f"Robot mode: {mode.value}")

robot.disconnect()
```

The SDK runs for 30 days without a key. After that, `register_license` is needed: see [Licensing](license.md).

## How the names are written

The Python package follows the .NET API, with Python names:

| .NET                                          | Python                                                     |
| --------------------------------------------- | ---------------------------------------------------------- |
| `robot.PrimaryInterface.JointData`            | `robot.primary_interface.joint_data`                       |
| `robot.Dashboard.GetProgramState()`           | `robot.dashboard.get_program_state()`                      |
| `parameters.Rtde.OutputSetup.Add(...)`        | `parameters.rtde.output_setup.add(...)`                    |
| `UR.RegisterLicense(...)`                     | `UR.register_license(...)`                                 |
| `pose.X`, `pose.Rx`                           | `pose.x`, `pose.rx`                                        |
| `values.InputIntRegisters.X24`                | `values.input_int_registers.x24`                           |
| `RtdeOutputData.ActualTcpPose`                | `RtdeOutputData.ActualTcpPose`                             |
| `SingularityType.None`                        | `SingularityType.None_`                                    |
| `robot.Rtde.OutputDataReceived += handler`    | `robot.rtde.output_data_received(handler)`                 |
| A callback, like `Action<ulong>` of `UploadFile` | A Python function: `upload_file(local, remote, lambda sent: print(sent))` |
| `double[]`, `double[][]` returned             | a .NET array: index it, iterate it, or copy it with `list(...)` |

Methods and properties become snake_case. Enumerations are Python `IntEnum` classes that keep the .NET value names, except the Python keywords (`None_`). Each type is in a module named after it, in the folder of its .NET namespace. A method that takes a .NET array accepts a Python list:

```python
# Main class and connection settings
from underautomation.universal_robots.ur import UR
from underautomation.universal_robots.connect_parameters import ConnectParameters

# One module per type, in the folder of its .NET namespace
from underautomation.universal_robots.common.pose import Pose
from underautomation.universal_robots.rtde.rtde_input_data import RtdeInputData
from underautomation.universal_robots.rtde.rtde_output_data import RtdeOutputData
from underautomation.universal_robots.rtde.rtde_input_values import RtdeInputValues
from underautomation.universal_robots.kinematics.kinematics_utils import KinematicsUtils
from underautomation.universal_robots.files.ur_program import URProgram
```

## Events

An event of the .NET API is a method in Python: call it with your function. The function receives two arguments, the sender and the event arguments. Read the new values in the properties of the client, or wrap the arguments in their Python class:

```python
from underautomation.universal_robots.ur import UR
from underautomation.universal_robots.connect_parameters import ConnectParameters
from underautomation.universal_robots.socket_communication.socket_client_connection_event_args import SocketClientConnectionEventArgs
from underautomation.universal_robots.socket_communication.socket_request_event_args import SocketRequestEventArgs
from underautomation.universal_robots.socket_communication.socket_get_var_event_args import SocketGetVarEventArgs
from underautomation.universal_robots.socket_communication.socket_client_disconnection_event_args import SocketClientDisconnectionEventArgs

robot = UR()

parameters = ConnectParameters("192.168.0.1")

# The socket server is disabled by default
parameters.socket_communication.enable = True
parameters.socket_communication.port = 50001

robot.connect(parameters)

# URScript: socket_open("192.168.0.10", 50001)
def on_connection(sender, e):
    SocketClientConnectionEventArgs(e._instance).client.socket_write("Welcome")

# URScript: socket_send_string("Hello")
def on_request(sender, e):
    request = SocketRequestEventArgs(e._instance)
    print(request.client.end_point, "says", request.message)

# URScript: value := socket_get_var("COUNTER")
def on_get_var(sender, e):
    request = SocketGetVarEventArgs(e._instance)
    if request.name == "COUNTER":
        request.value = 12  # integer only

# URScript: socket_close()
def on_disconnection(sender, e):
    print(SocketClientDisconnectionEventArgs(e._instance).client.end_point, "disconnected")

robot.socket_communication.socket_client_connection(on_connection)
robot.socket_communication.socket_request(on_request)
robot.socket_communication.socket_get_var(on_get_var)
robot.socket_communication.socket_client_disconnection(on_disconnection)

# Send a message to every connected robot
robot.socket_communication.socket_write("Start")

# Or to one robot
for client in robot.socket_communication.connected_clients:
    client.socket_write(f"Hello {client.end_point}")
```

The function runs in a thread of the SDK, not in the main thread of Python.

## Errors

An error raised by the SDK comes from the .NET runtime. Import the exception class from its .NET namespace, after the import of the package. Its members keep their .NET names: `Message`, `Service`, `LicenseInfo`.

```python
from underautomation.universal_robots.ur import UR
from underautomation.universal_robots.common.internal_error_event_args import InternalErrorEventArgs
from UnderAutomation.UniversalRobots.License import InvalidLicenseException
from UnderAutomation.UniversalRobots.Common import ConnectException

robot = UR()

# The exceptions come from the .NET runtime: their members keep their .NET names
try:
    robot.connect("192.168.0.1")
except InvalidLicenseException as ex:
    # The trial is over or the license key is not valid
    print(ex.LicenseInfo)
except ConnectException as ex:
    # One service did not connect: the other services are closed
    print(f"{ex.Service} of {ex.RobotIp}: {ex.Message}")
except Exception as ex:
    # For example, the robot does not answer the ping
    print(ex)

# Errors that happen after the connection, in a background thread
def on_error(sender, e):
    error = InternalErrorEventArgs(e._instance)
    print(f"{error.status}: {error.message}")

robot.internal_error_occured(on_error)
```

## Limits of the Python package

- A .NET method with an `out` parameter, like `Pose.TryParse` and `Pose.FromRotationVectorToQuaternion`, is not usable from Python.
- `GlobalVariable.ToMatrix` has no Python twin.
- The SDK has no asynchronous methods.

## What to read next

- [Connect to the robot](connect.md): the settings of the robot, the connection parameters, the errors.
- [RTDE](rtde.md) and [Primary Interface](data-streaming.md): every code sample has a Python tab.
- [Licensing](license.md): the 30 day trial and the license key.
- [AI agent skills](https://underautomation.com/universal-robots/documentation/ai-skills): install the Python skill of the SDK in Claude Code, Codex, GitHub Copilot or Cursor.
