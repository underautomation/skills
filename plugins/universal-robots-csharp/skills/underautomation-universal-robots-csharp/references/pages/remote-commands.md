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

```csharp
using UnderAutomation.UniversalRobots;

class Dashboard
{
  static void Main(string[] args)
  {
    var robot = new UR();

    var parameters = new ConnectParameters("192.168.0.1");

    // The Dashboard Server is enabled by default
    parameters.Dashboard.Enable = true;

    robot.Connect(parameters);

    // Every command returns a CommandResponse
    var powerOn = robot.Dashboard.PowerOn();
    if (!powerOn.Succeed) Console.WriteLine(powerOn.Message);

    robot.Dashboard.ReleaseBrake();
    robot.Dashboard.LoadProgram("pick_and_place.urp");
    robot.Dashboard.Play();

    // Commands that read a value return a CommandResponse<T>
    var running = robot.Dashboard.IsProgramRunning();
    Console.WriteLine($"Running: {running.Value}");

    // Close the Dashboard Server only
    robot.Dashboard.Disable();
  }
}
```

The same client works without `UR`:

```csharp
using UnderAutomation.UniversalRobots.Dashboard;

class DashboardDirect
{
  static void Main(string[] args)
  {
    // A Dashboard Server client, without a UR instance
    var client = new DashboardClient();

    // Address of the robot. Optional: port, receive and send timeouts
    client.Enable("192.168.0.1");

    client.PowerOn();
    client.ReleaseBrake();
    client.Play();

    client.Disable();
  }
}
```

## Responses

Every command returns a `CommandResponse`: `Succeed` says if the robot accepted the command, `Message` gives its answer. The commands that read a value return a `CommandResponse<T>`, with the value in `Value`.

**CommandResponse** ([reference](../api/UnderAutomation.UniversalRobots.Dashboard.md#commandresponse))

- `CommandResponse()`
- `string Message`: A message that described the error or the action done
- `bool Succeed`: The command as succeeded

## Power and brakes

### GetRobotMode

Get the current robot mode.

```csharp
// Returns the current robot state. (From FW 1.6)
CommandResponse<RobotModes> GetRobotMode();

var response = robot.Dashboard.GetRobotMode();
if (response.Succeed) Console.WriteLine("Succeed");
else Console.WriteLine("Command failed");
Console.WriteLine(response.Message);
RobotModes robotMode = response.Value;
```

**RobotModes** ([reference](../api/UnderAutomation.UniversalRobots.Common.md#robotmodes-robotprimaryinterfacerobotmodedatarobotmode))

- BackDrive: The robot is hand guided by pushing teached button
- Booting: The robot controller is booting
- ConfirmSafety: Robot has stopped due to a Safety Stop
- Disconnected: Robot is not connected to its controller
- Idle: Power is on but breaks are not released
- Other: Robot is in an obsolete CB2 mode
- PowerOff: The robot is powered off
- PowerOn: The robot is powered on
- Running: Robot is in normal mode
- UpdatingFirmware: Firmware is upgrading

### PowerOn

Power on the robot.

```csharp
// Powers on the robot arm. (From FW 3.0)
CommandResponse PowerOn();

var response = robot.Dashboard.PowerOn();
if (response.Succeed) Console.WriteLine("Succeed");
else Console.WriteLine("Command failed");
Console.WriteLine(response.Message);
```

### PowerOff

Power off the robot.

```csharp
// Powers off the robot arm. (From FW 3.0)
CommandResponse PowerOff();

var response = robot.Dashboard.PowerOff();
if (response.Succeed) Console.WriteLine("Succeed");
else Console.WriteLine("Command failed");
Console.WriteLine(response.Message);
```

### ReleaseBrake

Release the brakes after powering on.

```csharp
// Releases the brakes. (From FW 3.0)
CommandResponse ReleaseBrake();

var response = robot.Dashboard.ReleaseBrake();
if (response.Succeed) Console.WriteLine("Succeed");
else Console.WriteLine("Command failed");
Console.WriteLine(response.Message);
```

### UnlockProtectiveStop

Unlock the robot from protective stop state.

```csharp
// Closes the current popup and unlocks protective stop. (From FW 3.1)
CommandResponse UnlockProtectiveStop();

var response = robot.Dashboard.UnlockProtectiveStop();
if (response.Succeed) Console.WriteLine("Succeed");
else Console.WriteLine("Command failed");
Console.WriteLine(response.Message);
```

### Shutdown

Completely shut down the robot.

```csharp
// Shuts down and turns off robot and controller. Closes the connection. (From FW 1.4)
CommandResponse Shutdown();

var response = robot.Dashboard.Shutdown();
if (response.Succeed) Console.WriteLine("Succeed");
else Console.WriteLine("Command failed");
Console.WriteLine(response.Message);
```

## Programs

### LoadProgram

Load a program from the robot's file system.

```csharp
// Start loading the specified program. (From FW 1.4) Returns when both program and associated installation has loaded (or failed). The load command fails if the associated installation requires confirmation of safety.The return value in this case will be 'Error while loading program'.
CommandResponse LoadProgram(string programName);

var response = robot.Dashboard.LoadProgram("prg1.urp");
if (response.Succeed) Console.WriteLine("Succeed");
else Console.WriteLine("Command failed");
Console.WriteLine(response.Message);
```

### GetLoadedProgram

Get the name of the currently loaded program.

```csharp
// Returns the path of the loaded program. If not program is loaded, Value member is null. (From FW 1.6)
CommandResponse<string> GetLoadedProgram();

var response = robot.Dashboard.GetLoadedProgram();
if (response.Succeed) Console.WriteLine("Succeed");
else Console.WriteLine("Command failed");
Console.WriteLine(response.Message);
string loadedProgram = response.Value;
```

### Play

Start executing the loaded program.

```csharp
// Starts program, if any program is loaded and robot is ready. (From FW 1.4) Returns failure if the program fails to start.
CommandResponse Play();

var response = robot.Dashboard.Play();
if (response.Succeed) Console.WriteLine("Succeed");
else Console.WriteLine("Command failed");
Console.WriteLine(response.Message);
```

### Stop

Stop program execution.

```csharp
// Stops running program. (From FW 1.4) Returns failure if the program fails to stop
CommandResponse Stop();

var response = robot.Dashboard.Stop();
if (response.Succeed) Console.WriteLine("Succeed");
else Console.WriteLine("Command failed");
Console.WriteLine(response.Message);
```

### Pause

Pause the running program.

```csharp
// Pauses the running program . (From FW 1.4) Returns failure if the program fails to pause
CommandResponse Pause();

var response = robot.Dashboard.Pause();
if (response.Succeed) Console.WriteLine("Succeed");
else Console.WriteLine("Command failed");
Console.WriteLine(response.Message);
```

### IsProgramRunning

Check if a program is currently running.

```csharp
// Returns a True value is a program is running. (From FW 1.6)
CommandResponse<bool> IsProgramRunning();

var response = robot.Dashboard.IsProgramRunning();
if (response.Succeed) Console.WriteLine("Succeed");
else Console.WriteLine("Command failed");
Console.WriteLine(response.Message);
bool isProgramRunning = response.Value;
```

### GetProgramState

Get the current program state.

```csharp
// Returns the state of the active program and path to loaded program file, or STOPPED if no program is loaded
CommandResponse<ProgramState> GetProgramState();

var response = robot.Dashboard.GetProgramState();
if (response.Succeed) Console.WriteLine("Succeed");
else Console.WriteLine("Command failed");
Console.WriteLine(response.Message);
ProgramState state = response.Value;
```

**ProgramState** ([reference](../api/UnderAutomation.UniversalRobots.Dashboard.md#programstate))

- `ProgramState()`
- `string Name`: Name of the loaded program
- `ProgramStates State`: Running state of the loaded program

### IsProgramSaved

Check if the current program has unsaved changes.

```csharp
// Returns the save state of the active program and path to loaded program file. (From FW 1.8.11997)
CommandResponse<ProgramSaveState> IsProgramSaved();

var response = robot.Dashboard.IsProgramSaved();
if (response.Succeed) Console.WriteLine("Succeed");
else Console.WriteLine("Command failed");
Console.WriteLine(response.Message);
ProgramSaveState state = response.Value;
```

**ProgramSaveState** ([reference](../api/UnderAutomation.UniversalRobots.Dashboard.md#programsavestate))

- `ProgramSaveState()`
- `bool IsSaved`: Is the program saved
- `string Name`: Name of the loaded program

## Teach pendant

### ShowPopup

Display a popup message on the teach pendant.

```csharp
// Shows a popup on Polyscope with the specified message. The popup-text will be translated to the selected language, if the text exists in the language file. (From FW 1.6)
CommandResponse ShowPopup(string message);

var response = robot.Dashboard.ShowPopup("This is a popup message !");
if (response.Succeed) Console.WriteLine("Succeed");
else Console.WriteLine("Command failed");
Console.WriteLine(response.Message);
```

### ClosePopup

Close any open popup message.

```csharp
// Closes the popup (From FW 1.6)
CommandResponse ClosePopup();

var response = robot.Dashboard.ClosePopup();
if (response.Succeed) Console.WriteLine("Succeed");
else Console.WriteLine("Command failed");
Console.WriteLine(response.Message);
```

### AddToLog

Add a message to the robot's log.

```csharp
// Adds log-message to the Log history. (From FW 1.8.11657)
CommandResponse AddToLog(string message);

var response = robot.Dashboard.AddToLog("This is a log message !");
if (response.Succeed) Console.WriteLine("Succeed");
else Console.WriteLine("Command failed");
Console.WriteLine(response.Message);
```

## Robot information

### GetPolyscopeVersion

Get the Polyscope software version.

```csharp
// Returns the version of the Polyscope software (From FW 1.8.14035)
CommandResponse<PolyscopeVersion> GetPolyscopeVersion();

var response = robot.Dashboard.GetPolyscopeVersion();
if (response.Succeed) Console.WriteLine("Succeed");
else Console.WriteLine("Command failed");
Console.WriteLine(response.Message);
```

### GetSerialNumber

Get the robot's serial number.

```csharp
// Returns serial number of the robot (FW 3.12 and from FW 5.6)
CommandResponse GetSerialNumber();

var response = robot.Dashboard.GetSerialNumber();
if (response.Succeed) Console.WriteLine("Succeed");
else Console.WriteLine("Command failed");
Console.WriteLine(response.Message);
```

### GetRobotModel

Get the robot model (UR3, UR5, UR10, etc.).

```csharp
// Returns the robot model (UR3, UR5, UR10, UR16, ...). (FW 3.12 and from FW 5.6)
CommandResponse<RobotModels> GetRobotModel();

var response = robot.Dashboard.GetRobotModel();
if (response.Succeed) Console.WriteLine("Succeed");
else Console.WriteLine("Command failed");
Console.WriteLine(response.Message);
RobotModels model = response.Value;
```

**RobotModels** ([reference](../api/UnderAutomation.UniversalRobots.Common.md#robotmodels-robotprimaryinterfaceconfigurationdatarobottype))

- UR10: UR10 robot model.
- UR16: UR16 robot model.
- UR18: UR18 robot model.
- UR20: UR20 robot model.
- UR3: UR3 robot model.
- UR30: UR30 robot model.
- UR5: UR5 robot model.
- UR8L: UR8 Long robot model.

### LoadInstallation

Load an installation file.

```csharp
// Loads the specified installation file (From FW 3.2.18654)
CommandResponse LoadInstallation(string installation);

var response = robot.Dashboard.LoadInstallation("default.installation");
if (response.Succeed) Console.WriteLine("Succeed");
else Console.WriteLine("Command failed");
Console.WriteLine(response.Message);
```

## Operational mode

### GetOperationalMode

Get the current operational mode.

```csharp
// Returns the operational mode. (From FW 5.6)
CommandResponse<OperationalModes> GetOperationalMode();

var response = robot.Dashboard.GetOperationalMode();
if (response.Succeed) Console.WriteLine("Succeed");
else Console.WriteLine("Command failed");
Console.WriteLine(response.Message);
OperationalModes mode = response.Value;
```

**OperationalModes** ([reference](../api/UnderAutomation.UniversalRobots.Dashboard.md#operationalmodes))

- Automatic: Loading and editing programs and installations is not allowed, only playing programs
- Manual: Loading and editing programs is allowed
- None: The password has not been set.

### SetOperationalMode

Set the operational mode.

```csharp
// Controls the operational mode. See User manual for details. If this function is called the operational mode cannot be changed from PolyScope, and the user password is disabled. OperationalModes.None is not a valid operational mode. (From FW 5.0.0)
CommandResponse SetOperationalMode(OperationalModes mode);

var response = robot.Dashboard.SetOperationalMode(OperationalModes.Manual);
if (response.Succeed) Console.WriteLine("Succeed");
else Console.WriteLine("Command failed");
Console.WriteLine(response.Message);
```

### ClearOperationalMode

Clear the current operational mode.

```csharp
// The operational mode can again be changed from PolyScope, and the user password is enabled. (From FW 5.0.0)
CommandResponse ClearOperationalMode();

var response = robot.Dashboard.ClearOperationalMode();
if (response.Succeed) Console.WriteLine("Succeed");
else Console.WriteLine("Command failed");
Console.WriteLine(response.Message);
```

### IsInRemoteControl

Check if the robot is in remote control mode.

```csharp
// Returns the remote control status of the robot. If the robot Is In remote control it returns False And If remote control Is disabled Or robot Is in local control it returns false. (From FW 5.6)
CommandResponse<bool> IsInRemoteControl();

var response = robot.Dashboard.IsInRemoteControl();
if (response.Succeed) Console.WriteLine("Succeed");
else Console.WriteLine("Command failed");
Console.WriteLine(response.Message);
bool isRemoteControl = response.Value;
```

## Safety

### GetSafetyStatus

Get the current safety status.

```csharp
// Returns the current safety status. (From FW 3.11 to 3.12 and from FW 5.5)
CommandResponse<SafetyStatus> GetSafetyStatus();

var response = robot.Dashboard.GetSafetyStatus();
if (response.Succeed) Console.WriteLine("Succeed");
else Console.WriteLine("Command failed");
Console.WriteLine(response.Message);
SafetyStatus status = response.Value;
```

**SafetyStatus** ([reference](../api/UnderAutomation.UniversalRobots.Common.md#safetystatus-robotprimaryinterfacemasterboarddatasafetymode))

- AutomaticModeSafeguardStop: Automatic mode safeguard stop is active.
- Fault: Safety is in fault mode
- Normal: Safety is in normal operating conditions
- ProtectiveStop: Protective safeguard Stop. This safety function is triggeredby an external protective device using safety inputs which will trigger a Cat 2 stop3per IEC 60204-1.
- Recovery: When a safety limit is violated, the safety system must be restarted.
- Reduced: Speed is reduced
- RobotEmergencyStop: (EA + EB + SBUS-&gt;Screen) Physical e-stop interface input activated
- SafeguardStop: (SI0 + SI1 + SBUS) Physical s-stop interface input
- SystemEmergencyStop: (EA + EB + SBUS-&gt;Euromap67) Physical e-stop interface input activated
- SystemThreePositionEnablingStop: System three-position enabling device stop is active.
- Violation: Safety is in violation mode (for example, violation of the allowed delay between redundant signals)

### CloseSafetyPopup

Close any safety-related popup.

```csharp
// Closes a safety popup. (From FW 3.1)
CommandResponse CloseSafetyPopup();

var response = robot.Dashboard.CloseSafetyPopup();
if (response.Succeed) Console.WriteLine("Succeed");
else Console.WriteLine("Command failed");
Console.WriteLine(response.Message);
```

### RestartSafety

Restart the safety system after a safety fault.

```csharp
// Restarts the safety. Used when robot gets a safety fault or violation to restart the safety. After safety has been rebooted the robot will be in Power Off. (From FW 3.7 to 3.12.0 and from 5.1.0)
CommandResponse RestartSafety();

var response = robot.Dashboard.RestartSafety();
if (response.Succeed) Console.WriteLine("Succeed");
else Console.WriteLine("Command failed");
Console.WriteLine(response.Message);
```

## Variables and other commands

### GetVariable

Read a global variable of the running program. See [Read and write variables](variables.md).

```csharp
// Get variable value and estimate its type
CommandResponse<GlobalVariable> GetVariable(string name);

var response = robot.Dashboard.GetVariable("myVar");
if (response.Succeed) Console.WriteLine("Succeed");
else Console.WriteLine("Command failed");
Console.WriteLine(response.Message);
GlobalVariable variable = response.Value;
```

### SendCustomDashboardCommand

Send a command of the Dashboard Server that has no method in the SDK. The answer of the robot is in `Message`.

```csharp
// Send a custom command to the Dashboard Server port
CommandResponse SendCustomDashboardCommand(string command);

var response = robot.Dashboard.SendCustomDashboardCommand("robotmode");
if (response.Succeed) Console.WriteLine("Succeed");
else Console.WriteLine("Command failed");
Console.WriteLine(response.Message);
```

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## What to read next

- [Run a program](how-to-run-program.md): a complete program, from power on to the end of the program.
- [Read and reset alarms](how-to-read-reset-alarms.md): protective stops and safety faults.
- [Dashboard Server](https://www.universal-robots.com/articles/ur/dashboard-server-e-series-port-29999/) by Universal Robots: the list of the commands of the robot.
