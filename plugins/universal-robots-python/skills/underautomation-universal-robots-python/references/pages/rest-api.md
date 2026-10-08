# REST API (PolyScope X)

Control a UR cobot with PolyScope X over HTTP: power, brakes, load, play and stop programs, read the program state. Replaces the Dashboard Server.

Web page: https://underautomation.com/universal-robots/documentation/rest-api

The REST API of PolyScope X controls a Universal Robots cobot over HTTP: power, brakes, load and play programs, read the state of the program. This page shows how to use it with the SDK. It replaces the Dashboard Server, which PolyScope X does not have.

For CB-Series and e-Series robots with PolyScope 5, use the [Dashboard Server](remote-commands.md).

## Prerequisites

- The robot runs PolyScope X, or URSim PolyScope X: see [Develop without a robot](configure-offline-simulator.md).
- The robot is in remote control. Switch it with the icon at the top right of PolyScope X. The default password is `operator`.

![Remote control on PolyScope X](https://underautomation.com/universal-robots/switch-remote-polyscopex.png)

## Example

The REST API is disabled by default: set `Rest.Enable` in `ConnectParameters`.

```python
from underautomation.universal_robots.ur import UR
from underautomation.universal_robots.connect_parameters import ConnectParameters

robot = UR()

parameters = ConnectParameters("192.168.0.1")

# The REST API is disabled by default
parameters.rest.enable = True

# The Dashboard Server does not exist on PolyScope X
parameters.dashboard.enable = False

robot.connect(parameters)

robot.rest.power_on()
robot.rest.brake_release()
robot.rest.load_program("my_program")
robot.rest.play()

# Playing, Paused, Stopped or Unknown
state = robot.rest.get_program_state()
print(state.value.state)

robot.disconnect()
```

The same client works without `UR`:

```python
from underautomation.universal_robots.rest.rest_client import RestClient

# A REST client, without a UR instance
client = RestClient()

# Address of the robot. Optional: port, API version, timeout
client.enable("192.168.0.1")

client.power_on()
client.load_program("my_program")
client.play()

client.disable()
```

## Connection parameters

| Property    | Default  | Role                                 |
| ----------- | -------- | ------------------------------------ |
| `Enable`    | `false`  | Enable the REST client               |
| `Port`      | `80`     | HTTP port of the robot               |
| `Version`   | `Latest` | Version of the API (`V1`, `Latest`)  |
| `TimeoutMs` | `5000`   | Timeout of a request, in ms          |

```python
from underautomation.universal_robots.ur import UR
from underautomation.universal_robots.connect_parameters import ConnectParameters
from underautomation.universal_robots.rest.rest_api_version import RestApiVersion

robot = UR()

parameters = ConnectParameters("192.168.0.1")

parameters.rest.enable = True
parameters.rest.port = 80                       # HTTP port, 80 by default
parameters.rest.version = RestApiVersion.V1     # Latest by default
parameters.rest.timeout_ms = 10000              # 5000 ms by default

robot.connect(parameters)

# The client is ready
if robot.rest.initialized:
    print(f"{robot.rest.ip}:{robot.rest.port}")
```

## Commands

### State of the robot

`PowerOn`, `BrakeRelease`, `PowerOff`, `UnlockProtectiveStop` and `RestartSafety` change the state of the robot. `ChangeRobotState` does the same with a `RobotStateAction`.

```python
from underautomation.universal_robots.ur import UR
from underautomation.universal_robots.connect_parameters import ConnectParameters
from underautomation.universal_robots.rest.robot_state_action import RobotStateAction

robot = UR()
parameters = ConnectParameters("192.168.0.1")
parameters.rest.enable = True
robot.connect(parameters)

# Power on, then release the brakes
robot.rest.power_on()
robot.rest.brake_release()

# After a protective stop or a safety fault
robot.rest.unlock_protective_stop()
robot.rest.restart_safety()

robot.rest.power_off()

# The same actions, with one generic method
robot.rest.change_robot_state(RobotStateAction.POWER_ON)
robot.rest.change_robot_state(RobotStateAction.BRAKE_RELEASE)
```

### Programs

`LoadProgram` loads a program by its name, with or without the `.urp` extension. `Play`, `Pause`, `Resume` and `Stop` control it, and `GetProgramState` returns its state: `Playing`, `Paused`, `Stopped` or `Unknown`. `ChangeProgramState` does the same with a `ProgramStateAction`.

```python
from underautomation.universal_robots.ur import UR
from underautomation.universal_robots.connect_parameters import ConnectParameters
from underautomation.universal_robots.rest.program_state_action import ProgramStateAction

robot = UR()
parameters = ConnectParameters("192.168.0.1")
parameters.rest.enable = True
robot.connect(parameters)

# The name of the program, with or without .urp
robot.rest.load_program("my_program")

robot.rest.play()
robot.rest.pause()
robot.rest.resume()
robot.rest.stop()

# The same actions, with one generic method
robot.rest.change_program_state(ProgramStateAction.play)

response = robot.rest.get_program_state()
if response.succeed:
    state = response.value.state  # Playing, Paused, Stopped, Unknown
```

## Responses and errors

Every method returns a `RestApiResponse`. `GetProgramState` returns a `RestApiResponse<ProgramStateResponse>`, with the state in `Value`.

| Property      | Role                                       |
| ------------- | ------------------------------------------ |
| `Succeed`     | `true` when the robot answered HTTP 200    |
| `StatusCode`  | HTTP status of the answer                  |
| `Message`     | Message of success, or description of the error |
| `RawResponse` | Body of the answer, in JSON                |
| `Value`       | Typed value (`RestApiResponse<T>` only)    |

The errors of the SDK, a timeout for example, raise `InternalErrorOccured`.

```python
from underautomation.universal_robots.ur import UR
from underautomation.universal_robots.connect_parameters import ConnectParameters
from underautomation.universal_robots.common.internal_error_event_args import InternalErrorEventArgs

robot = UR()
parameters = ConnectParameters("192.168.0.1")
parameters.rest.enable = True
robot.connect(parameters)

response = robot.rest.power_on()

if not response.succeed:
    # HTTP status, message and body of the answer of the robot
    print(response.status_code)
    print(response.message)
    print(response.raw_response)

# Errors of the SDK, for example a timeout
def on_error(sender, e):
    error = InternalErrorEventArgs(e._instance)
    print(error.message)
    print(error.exception)

robot.rest.internal_error_occured(on_error)
```

## From the Dashboard Server to the REST API

An application that supports both PolyScope 5 and PolyScope X enables the client of the robot:

```python
from underautomation.universal_robots.ur import UR
from underautomation.universal_robots.connect_parameters import ConnectParameters

robot = UR()

# PolyScope 5 and CB-Series: Dashboard Server
parameters = ConnectParameters("192.168.0.1")
parameters.dashboard.enable = True
robot.connect(parameters)
robot.dashboard.power_on()
robot.dashboard.load_program("/programs/my_program.urp")
robot.dashboard.play()

# PolyScope X: REST API
parameters = ConnectParameters("192.168.0.1")
parameters.rest.enable = True
robot.connect(parameters)
robot.rest.power_on()
robot.rest.load_program("my_program")
robot.rest.play()
```

- The REST API uses HTTP (port 80), the Dashboard Server TCP (port 29999).
- `LoadProgram` takes the name of the program, without its folder.
- `ReleaseBrake` of the Dashboard Server is `BrakeRelease` in the REST API.

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**RestClientBase** ([reference](../api/underautomation.universal_robots.rest.internal.md#restclientbase-robotrest))

- `disable() -> None`: Disable the REST client
- `change_robot_state(action: RobotStateAction) -> RestApiResponse`: Change the robot's operational state.
- `unlock_protective_stop() -> RestApiResponse`: Unlock the robot from protective stop state.
- `restart_safety() -> RestApiResponse`: Restart the safety system.
- `power_off() -> RestApiResponse`: Power off the robot.
- `power_on() -> RestApiResponse`: Power on the robot.
- `brake_release() -> RestApiResponse`: Release the robot brakes.
- `load_program(programName: str) -> RestApiResponse`: Load a program by name.
- `change_program_state(action: ProgramStateAction) -> RestApiResponse`: Change the program state.
- `play() -> RestApiResponse`: Start playing the loaded program.
- `pause() -> RestApiResponse`: Pause the running program.
- `stop() -> RestApiResponse`: Stop the running program.
- `resume() -> RestApiResponse`: Resume a paused program.
- `get_program_state() -> RestApiResponse1[ProgramStateResponse]`: Get the current program state.
- `ip: str (read only)`: IP address of the robot
- `port: int (read only)`: HTTP port for REST API
- `version: RestApiVersion (read only)`: REST API version being used
- `timeout_ms: int (read only)`: Request timeout in milliseconds
- `initialized: bool (read only)`: Indicates whether the REST client has been initialized
- Inherited from [URServiceBase](../api/underautomation.universal_robots.internal.md#urservicebase-robot): `internal_error_occured`

**RestApiResponse** ([reference](../api/underautomation.universal_robots.rest.md#restapiresponse))

- `RestApiResponse()`
- `succeed: bool`: Indicates whether the API call succeeded (HTTP 200)
- `status_code: typing.Any`: HTTP status code returned by the API
- `message: str`: Response message or error description
- `raw_response: str`: Raw JSON response body

**RobotStateAction** ([reference](../api/underautomation.universal_robots.rest.md#robotstateaction))

- UNLOCK_PROTECTIVE_STOP: Unlocks the robot from a protective stop state
- RESTART_SAFETY: Restarts the safety system
- POWER_OFF: Powers off the robot
- POWER_ON: Powers on the robot
- BRAKE_RELEASE: Releases the robot brakes

**ProgramStateAction** ([reference](../api/underautomation.universal_robots.rest.md#programstateaction))

- play: Start or resume playing the program
- pause: Pause the running program
- stop: Stop the running program
- resume: Resume a paused program

**RestProgramState** ([reference](../api/underautomation.universal_robots.rest.md#restprogramstate))

- Unknown: Unknown state
- Stopped: Program is stopped
- Playing: Program is playing
- Paused: Program is paused

## What to read next

- [Run a program](how-to-run-program.md): the steps from power on to the end of the program.
- [RTDE](rtde.md): the data of the robot, also on PolyScope X.
