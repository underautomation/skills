# UnderAutomation.UniversalRobots.Dashboard

## CommandResponse<T>

`class CommandResponse<T> : CommandResponse`

Answer returned by a command which contains a typed value.

- `CommandResponse(CommandResponse command)`: Initializes a new instance of Dashboard.CommandResponse%601 by copying the base response data.
- `T Value`: Value return by the command
- Inherited from [CommandResponse](UnderAutomation.UniversalRobots.Dashboard.md#commandresponse): `Succeed`, `Message`

## CommandResponse

`class CommandResponse`

Generic answer returned by a command

- `CommandResponse()`
- `string Message`: A message that described the error or the action done
- `bool Succeed`: The command as succeeded

## DashboardClient

`class DashboardClient : DashboardClientBase`

Client for the Universal Robots Dashboard Server protocol. Enables remote control of the robot (load/play/stop programs, power on/off, etc.) via TCP commands on port 29999.

- `DashboardClient()`
- `void Enable(string ip, int port = 29999, int receiveTimeoutMs = 2000, int sendTimeoutMs = 500)`: Specifies the IP address of the robot. No TCP connection is maintained. A new connection is created when sending each command.
- Inherited from [DashboardClientBase](UnderAutomation.UniversalRobots.Dashboard.Internal.md#dashboardclientbase-robotdashboard): `BeforeShutdown`, `Disable`, `LoadProgram`, `Play`, `Stop`, `Pause`, `SendCustomDashboardCommand`, `GetVariable`, `Shutdown`, `IsProgramRunning`, `GetRobotMode`, `GetLoadedProgram`, `ShowPopup`, `ClosePopup`, `AddToLog`, `IsProgramSaved`, `GetProgramState`, `GetPolyscopeVersion`, `SetUserRole`, `SetOperationalMode`, `ClearOperationalMode`, `GetOperationalMode`, `IsInRemoteControl`, `PowerOn`, `PowerOff`, `ReleaseBrake`, `UnlockProtectiveStop`, `CloseSafetyPopup`, `LoadInstallation`, `RestartSafety`, `GetSafetyStatus`, `GetSerialNumber`, `GetRobotModel`, `IP`, `Port`, `ReceiveTimeoutMs`, `SendTimeoutMs`, `Initialized`
- Inherited from [URServiceBase](UnderAutomation.UniversalRobots.Internal.md#urservicebase-robot): `InternalErrorOccured`

## OperationalModes

`enum OperationalModes`

Enumerates all robot operational modes

- Automatic: Loading and editing programs and installations is not allowed, only playing programs
- Manual: Loading and editing programs is allowed
- None: The password has not been set.

## PolyscopeVersion

`class PolyscopeVersion`

Describes a Polyscope version (robot controller firmware).

- `PolyscopeVersion()`
- `string Date`: Release date (example : "Nov 2020")
- `string Description`: String description of the firmware version (exemple : "5.0.16.8524 (Nov 2020)")
- `Version Version`: Firmware version

## ProgramSaveState

`class ProgramSaveState`

Represents the save state of the currently loaded program on the Universal Robots controller.

- `ProgramSaveState()`
- `bool IsSaved`: Is the program saved
- `string Name`: Name of the loaded program

## ProgramState

`class ProgramState`

Describes a program state (its running state and its name)

- `ProgramState()`
- `string Name`: Name of the loaded program
- `ProgramStates State`: Running state of the loaded program

## ProgramStates

`enum ProgramStates`

Enumerate possible states of a program.

- Paused: Program is paused.
- Playing: Program is running.
- Stopped: No program is running.

## UserRoles

`enum UserRoles`

Enumerates all user roles

- Locked: All buttons disabled and "Expert Mode" cannot be activated
- None: All buttons enabled, "Expert Mode" is available (if correct password is supplied)
- Operator: Only "RUN Program" And "SHUTDOWN Robot" buttons are enabled, "Expert Mode" cannot be activated
- Programmer: In Setup Robot, buttons "Update", "Set Password", "Network", "Time" and "URCaps" are disabled, "Expert Mode" is available (if correct password is supplied)
- restricted: Works like "operator" but does not give access to the move tab. (From FW 3.1.17136)
