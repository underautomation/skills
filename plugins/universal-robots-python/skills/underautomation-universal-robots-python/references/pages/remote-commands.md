# Dashboard Server: remote commands

Power, brakes, programs, popups, robot mode and safety status of a UR cobot with the Dashboard Server of PolyScope 5. All the commands of the SDK.

Web page: https://underautomation.com/universal-robots/documentation/remote-commands

The Dashboard Server of a Universal Robots cobot accepts remote commands on TCP port 29999: power on and off, release the brakes, load and play programs, show popups, read the robot mode and the safety status. This page lists the commands of the SDK for CB-Series and e-Series robots with PolyScope.

PolyScope X has no Dashboard Server: use the [REST API](rest-api.md).

## Prerequisites

- The service `Dashboard Server` is enabled on the robot: see [Prepare the robot](connect.md#prepare_the_robot).
- On e-Series, the commands that change the state of the robot (power, brakes, load, play) need the remote control: see [Remote control](connect.md#remote_control). The commands that read a value work in local control.

## Example

The Dashboard Server is enabled by default: `Connect("192.168.0.1")` opens it.

```python
from underautomation.universal_robots.ur import UR
from underautomation.universal_robots.connect_parameters import ConnectParameters

robot = UR()

parameters = ConnectParameters("192.168.0.1")

# The Dashboard Server is enabled by default
parameters.dashboard.enable = True

robot.connect(parameters)

# Every command returns a CommandResponse
power_on = robot.dashboard.power_on()
if not power_on.succeed:
    print(power_on.message)

robot.dashboard.release_brake()
robot.dashboard.load_program("pick_and_place.urp")
robot.dashboard.play()

# Commands that read a value return a CommandResponse with a value
running = robot.dashboard.is_program_running()
print(f"Running: {running.value}")

# Close the Dashboard Server only
robot.dashboard.disable()
```

The same client works without `UR`:

```python
from underautomation.universal_robots.dashboard.dashboard_client import DashboardClient

# A Dashboard Server client, without a UR instance
client = DashboardClient()

# Address of the robot. Optional: port, receive and send timeouts
client.enable("192.168.0.1")

client.power_on()
client.release_brake()
client.play()

client.disable()
```

## Responses

Every command returns a `CommandResponse`: `Succeed` says if the robot accepted the command, `Message` gives its answer. The commands that read a value return a `CommandResponse<T>`, with the value in `Value`.

**CommandResponse** ([reference](../api/underautomation.universal_robots.dashboard.md#commandresponse))

- `CommandResponse()`
- `succeed: bool`: The command as succeeded
- `message: str`: A message that described the error or the action done

## Power and brakes

### GetRobotMode

Get the current robot mode.

```python
# Returns the current robot state. (From FW 1.6)
get_robot_mode() -> CommandResponse1[RobotModes]

response = robot.dashboard.get_robot_mode()
print("Succeed" if response.succeed else "Command failed")
print(response.message)
robot_mode = response.value
```

**RobotModes** ([reference](../api/underautomation.universal_robots.common.md#robotmodes-robotprimary_interfacerobot_mode_datarobot_mode))

- Other: Robot is in an obsolete CB2 mode
- Disconnected: Robot is not connected to its controller
- ConfirmSafety: Robot has stopped due to a Safety Stop
- Booting: The robot controller is booting
- PowerOff: The robot is powered off
- PowerOn: The robot is powered on
- Idle: Power is on but breaks are not released
- BackDrive: The robot is hand guided by pushing teached button
- Running: Robot is in normal mode
- UpdatingFirmware: Firmware is upgrading

### PowerOn

Power on the robot.

```python
# Powers on the robot arm. (From FW 3.0)
power_on() -> CommandResponse

response = robot.dashboard.power_on()
print("Succeed" if response.succeed else "Command failed")
print(response.message)
```

### PowerOff

Power off the robot.

```python
# Powers off the robot arm. (From FW 3.0)
power_off() -> CommandResponse

response = robot.dashboard.power_off()
print("Succeed" if response.succeed else "Command failed")
print(response.message)
```

### ReleaseBrake

Release the brakes after powering on.

```python
# Releases the brakes. (From FW 3.0)
release_brake() -> CommandResponse

response = robot.dashboard.release_brake()
print("Succeed" if response.succeed else "Command failed")
print(response.message)
```

### UnlockProtectiveStop

Unlock the robot from protective stop state.

```python
# Closes the current popup and unlocks protective stop. (From FW 3.1)
unlock_protective_stop() -> CommandResponse

response = robot.dashboard.unlock_protective_stop()
print("Succeed" if response.succeed else "Command failed")
print(response.message)
```

### Shutdown

Completely shut down the robot.

```python
# Shuts down and turns off robot and controller. Closes the connection. (From FW 1.4)
shutdown() -> CommandResponse

response = robot.dashboard.shutdown()
print("Succeed" if response.succeed else "Command failed")
print(response.message)
```

## Programs

### LoadProgram

Load a program from the robot's file system.

```python
# Start loading the specified program. (From FW 1.4) Returns when both program and associated installation has loaded (or failed). The load command fails if the associated installation requires confirmation of safety.The return value in this case will be 'Error while loading program'.
load_program(programName: str) -> CommandResponse

response = robot.dashboard.load_program("prg1.urp")
print("Succeed" if response.succeed else "Command failed")
print(response.message)
```

### GetLoadedProgram

Get the name of the currently loaded program.

```python
# Returns the path of the loaded program. If not program is loaded, Value member is null. (From FW 1.6)
get_loaded_program() -> CommandResponse1[str]

response = robot.dashboard.get_loaded_program()
print("Succeed" if response.succeed else "Command failed")
print(response.message)
loaded_program = response.value
```

### Play

Start executing the loaded program.

```python
# Starts program, if any program is loaded and robot is ready. (From FW 1.4) Returns failure if the program fails to start.
play() -> CommandResponse

response = robot.dashboard.play()
print("Succeed" if response.succeed else "Command failed")
print(response.message)
```

### Stop

Stop program execution.

```python
# Stops running program. (From FW 1.4) Returns failure if the program fails to stop
stop() -> CommandResponse

response = robot.dashboard.stop()
print("Succeed" if response.succeed else "Command failed")
print(response.message)
```

### Pause

Pause the running program.

```python
# Pauses the running program . (From FW 1.4) Returns failure if the program fails to pause
pause() -> CommandResponse

response = robot.dashboard.pause()
print("Succeed" if response.succeed else "Command failed")
print(response.message)
```

### IsProgramRunning

Check if a program is currently running.

```python
# Returns a True value is a program is running. (From FW 1.6)
is_program_running() -> CommandResponse1[bool]

response = robot.dashboard.is_program_running()
print("Succeed" if response.succeed else "Command failed")
print(response.message)
is_program_running = response.value
```

### GetProgramState

Get the current program state.

```python
# Returns the state of the active program and path to loaded program file, or STOPPED if no program is loaded
get_program_state() -> CommandResponse1[ProgramState]

response = robot.dashboard.get_program_state()
print("Succeed" if response.succeed else "Command failed")
print(response.message)
state = response.value
```

**ProgramState** ([reference](../api/underautomation.universal_robots.dashboard.md#programstate))

- `ProgramState()`
- `state: ProgramStates`: Running state of the loaded program
- `name: str`: Name of the loaded program

### IsProgramSaved

Check if the current program has unsaved changes.

```python
# Returns the save state of the active program and path to loaded program file. (From FW 1.8.11997)
is_program_saved() -> CommandResponse1[ProgramSaveState]

response = robot.dashboard.is_program_saved()
print("Succeed" if response.succeed else "Command failed")
print(response.message)
state = response.value
```

**ProgramSaveState** ([reference](../api/underautomation.universal_robots.dashboard.md#programsavestate))

- `ProgramSaveState()`
- `is_saved: bool`: Is the program saved
- `name: str`: Name of the loaded program

## Teach pendant

### ShowPopup

Display a popup message on the teach pendant.

```python
# Shows a popup on Polyscope with the specified message. The popup-text will be translated to the selected language, if the text exists in the language file. (From FW 1.6)
show_popup(message: str) -> CommandResponse

response = robot.dashboard.show_popup("This is a popup message !")
print("Succeed" if response.succeed else "Command failed")
print(response.message)
```

### ClosePopup

Close any open popup message.

```python
# Closes the popup (From FW 1.6)
close_popup() -> CommandResponse

response = robot.dashboard.close_popup()
print("Succeed" if response.succeed else "Command failed")
print(response.message)
```

### AddToLog

Add a message to the robot's log.

```python
# Adds log-message to the Log history. (From FW 1.8.11657)
add_to_log(message: str) -> CommandResponse

response = robot.dashboard.add_to_log("This is a log message !")
print("Succeed" if response.succeed else "Command failed")
print(response.message)
```

## Robot information

### GetPolyscopeVersion

Get the Polyscope software version.

```python
# Returns the version of the Polyscope software (From FW 1.8.14035)
get_polyscope_version() -> CommandResponse1[PolyscopeVersion]

response = robot.dashboard.get_polyscope_version()
print("Succeed" if response.succeed else "Command failed")
print(response.message)
```

### GetSerialNumber

Get the robot's serial number.

```python
# Returns serial number of the robot (FW 3.12 and from FW 5.6)
get_serial_number() -> CommandResponse

response = robot.dashboard.get_serial_number()
print("Succeed" if response.succeed else "Command failed")
print(response.message)
```

### GetRobotModel

Get the robot model (UR3, UR5, UR10, etc.).

```python
# Returns the robot model (UR3, UR5, UR10, UR16, ...). (FW 3.12 and from FW 5.6)
get_robot_model() -> CommandResponse1[RobotModels]

response = robot.dashboard.get_robot_model()
print("Succeed" if response.succeed else "Command failed")
print(response.message)
model = response.value
```

**RobotModels** ([reference](../api/underautomation.universal_robots.common.md#robotmodels-robotprimary_interfaceconfiguration_datarobot_type))

- UR5: UR5 robot model.
- UR10: UR10 robot model.
- UR3: UR3 robot model.
- UR16: UR16 robot model.
- UR20: UR20 robot model.
- UR30: UR30 robot model.
- UR8L: UR8 Long robot model.
- UR18: UR18 robot model.

### LoadInstallation

Load an installation file.

```python
# Loads the specified installation file (From FW 3.2.18654)
load_installation(installation: str) -> CommandResponse

response = robot.dashboard.load_installation("default.installation")
print("Succeed" if response.succeed else "Command failed")
print(response.message)
```

## Operational mode

### GetOperationalMode

Get the current operational mode.

```python
# Returns the operational mode. (From FW 5.6)
get_operational_mode() -> CommandResponse1[OperationalModes]

response = robot.dashboard.get_operational_mode()
print("Succeed" if response.succeed else "Command failed")
print(response.message)
mode = response.value
```

**OperationalModes** ([reference](../api/underautomation.universal_robots.dashboard.md#operationalmodes))

- Manual: Loading and editing programs is allowed
- Automatic: Loading and editing programs and installations is not allowed, only playing programs
- None_: The password has not been set.

### SetOperationalMode

Set the operational mode.

```python
# Controls the operational mode. See User manual for details. If this function is called the operational mode cannot be changed from PolyScope, and the user password is disabled. OperationalModes.None is not a valid operational mode. (From FW 5.0.0)
set_operational_mode(mode: OperationalModes) -> CommandResponse

response = robot.dashboard.set_operational_mode(OperationalModes.Manual)
print("Succeed" if response.succeed else "Command failed")
print(response.message)
```

### ClearOperationalMode

Clear the current operational mode.

```python
# The operational mode can again be changed from PolyScope, and the user password is enabled. (From FW 5.0.0)
clear_operational_mode() -> CommandResponse

response = robot.dashboard.clear_operational_mode()
print("Succeed" if response.succeed else "Command failed")
print(response.message)
```

### IsInRemoteControl

Check if the robot is in remote control mode.

```python
# Returns the remote control status of the robot. If the robot Is In remote control it returns False And If remote control Is disabled Or robot Is in local control it returns false. (From FW 5.6)
is_in_remote_control() -> CommandResponse1[bool]

response = robot.dashboard.is_in_remote_control()
print("Succeed" if response.succeed else "Command failed")
print(response.message)
is_remote_control = response.value
```

## Safety

### GetSafetyStatus

Get the current safety status.

```python
# Returns the current safety status. (From FW 3.11 to 3.12 and from FW 5.5)
get_safety_status() -> CommandResponse1[SafetyStatus]

response = robot.dashboard.get_safety_status()
print("Succeed" if response.succeed else "Command failed")
print(response.message)
status = response.value
```

**SafetyStatus** ([reference](../api/underautomation.universal_robots.common.md#safetystatus-robotprimary_interfacemasterboard_datasafetymode))

- Normal: Safety is in normal operating conditions
- Reduced: Speed is reduced
- ProtectiveStop: Protective safeguard Stop. This safety function is triggeredby an external protective device using safety inputs which will trigger a Cat 2 stop3per IEC 60204-1.
- Recovery: When a safety limit is violated, the safety system must be restarted.
- SafeguardStop: (SI0 + SI1 + SBUS) Physical s-stop interface input
- SystemEmergencyStop: (EA + EB + SBUS->Euromap67) Physical e-stop interface input activated
- RobotEmergencyStop: (EA + EB + SBUS->Screen) Physical e-stop interface input activated
- Violation: Safety is in violation mode (for example, violation of the allowed delay between redundant signals)
- Fault: Safety is in fault mode
- AutomaticModeSafeguardStop: Automatic mode safeguard stop is active.
- SystemThreePositionEnablingStop: System three-position enabling device stop is active.

### CloseSafetyPopup

Close any safety-related popup.

```python
# Closes a safety popup. (From FW 3.1)
close_safety_popup() -> CommandResponse

response = robot.dashboard.close_safety_popup()
print("Succeed" if response.succeed else "Command failed")
print(response.message)
```

### RestartSafety

Restart the safety system after a safety fault.

```python
# Restarts the safety. Used when robot gets a safety fault or violation to restart the safety. After safety has been rebooted the robot will be in Power Off. (From FW 3.7 to 3.12.0 and from 5.1.0)
restart_safety() -> CommandResponse

response = robot.dashboard.restart_safety()
print("Succeed" if response.succeed else "Command failed")
print(response.message)
```

## Variables and other commands

### GetVariable

Read a global variable of the running program. See [Read and write variables](variables.md).

```python
# Get variable value and estimate its type
get_variable(name: str) -> CommandResponse1[GlobalVariable]

response = robot.dashboard.get_variable("myVar")
print("Succeed" if response.succeed else "Command failed")
print(response.message)
variable = response.value
```

### SendCustomDashboardCommand

Send a command of the Dashboard Server that has no method in the SDK. The answer of the robot is in `Message`.

```python
# Send a custom command to the Dashboard Server port
send_custom_dashboard_command(command: str) -> CommandResponse

response = robot.dashboard.send_custom_dashboard_command("robotmode")
print("Succeed" if response.succeed else "Command failed")
print(response.message)
```

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## What to read next

- [Run a program](how-to-run-program.md): a complete program, from power on to the end of the program.
- [Read and reset alarms](how-to-read-reset-alarms.md): protective stops and safety faults.
- [Dashboard Server](https://www.universal-robots.com/articles/ur/dashboard-server-e-series-port-29999/) by Universal Robots: the list of the commands of the robot.
