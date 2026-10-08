# UnderAutomation.UniversalRobots.Dashboard.Internal

## DashboardClientBase (robot.Dashboard)

`abstract class DashboardClientBase : URServiceBase`

Abstract base class providing Dashboard Server command implementations for the Universal Robots controller. Sends text-based commands over TCP and parses responses. A new TCP connection is created for each command.

- `CommandResponse AddToLog(string message)`: Adds log-message to the Log history. (From FW 1.8.11657)
- `EventHandler BeforeShutdown`: Event raised when function DashboardClientBase.Shutdown is called.
- `CommandResponse ClearOperationalMode()`: The operational mode can again be changed from PolyScope, and the user password is enabled. (From FW 5.0.0)
- `CommandResponse ClosePopup()`: Closes the popup (From FW 1.6)
- `CommandResponse CloseSafetyPopup()`: Closes a safety popup. (From FW 3.1)
- `void Disable()`: Disable dashboard client
- `CommandResponse<string> GetLoadedProgram()`: Returns the path of the loaded program. If not program is loaded, Value member is null. (From FW 1.6)
- `CommandResponse<OperationalModes> GetOperationalMode()`: Returns the operational mode. (From FW 5.6)
- `CommandResponse<PolyscopeVersion> GetPolyscopeVersion()`: Returns the version of the Polyscope software (From FW 1.8.14035)
- `CommandResponse<ProgramState> GetProgramState()`: Returns the state of the active program and path to loaded program file, or STOPPED if no program is loaded
- `CommandResponse<RobotModes> GetRobotMode()`: Returns the current robot state. (From FW 1.6)
- `CommandResponse<RobotModels> GetRobotModel()`: Returns the robot model (UR3, UR5, UR10, UR16, ...). (FW 3.12 and from FW 5.6)
- `CommandResponse<SafetyStatus> GetSafetyStatus()`: Returns the current safety status. (From FW 3.11 to 3.12 and from FW 5.5)
- `CommandResponse GetSerialNumber()`: Returns serial number of the robot (FW 3.12 and from FW 5.6)
- `CommandResponse<GlobalVariable> GetVariable(string name)`: Get variable value and estimate its type
- `string IP { get; }`: IP of the robot to connect to for sending commands
- `bool Initialized { get; }`: Indicates that the dashboard client has been initialized and is ready to send commands
- `CommandResponse<bool> IsInRemoteControl()`: Returns the remote control status of the robot. If the robot Is In remote control it returns False And If remote control Is disabled Or robot Is in local control it returns false. (From FW 5.6)
- `CommandResponse<bool> IsProgramRunning()`: Returns a True value is a program is running. (From FW 1.6)
- `CommandResponse<ProgramSaveState> IsProgramSaved()`: Returns the save state of the active program and path to loaded program file. (From FW 1.8.11997)
- `CommandResponse LoadInstallation(string installation)`: Loads the specified installation file (From FW 3.2.18654)
- `CommandResponse LoadProgram(string programName)`: Start loading the specified program. (From FW 1.4) Returns when both program and associated installation has loaded (or failed). The load command fails if the associated installation requires confirmation of safety.The return value in this case will be 'Error while loading program'.
- `CommandResponse Pause()`: Pauses the running program . (From FW 1.4) Returns failure if the program fails to pause
- `CommandResponse Play()`: Starts program, if any program is loaded and robot is ready. (From FW 1.4) Returns failure if the program fails to start.
- `int Port { get; }`: Dashboard server port
- `CommandResponse PowerOff()`: Powers off the robot arm. (From FW 3.0)
- `CommandResponse PowerOn()`: Powers on the robot arm. (From FW 3.0)
- `int ReceiveTimeoutMs { get; }`: Receive timeout in milliseconds
- `CommandResponse ReleaseBrake()`: Releases the brakes. (From FW 3.0)
- `CommandResponse RestartSafety()`: Restarts the safety. Used when robot gets a safety fault or violation to restart the safety. After safety has been rebooted the robot will be in Power Off. (From FW 3.7 to 3.12.0 and from 5.1.0)
- `CommandResponse SendCustomDashboardCommand(string command)`: Send a custom command to the Dashboard Server port
- `int SendTimeoutMs { get; }`: Send timeout in milliseconds
- `CommandResponse SetOperationalMode(OperationalModes mode)`: Controls the operational mode. See User manual for details. If this function is called the operational mode cannot be changed from PolyScope, and the user password is disabled. OperationalModes.None is not a valid operational mode. (From FW 5.0.0)
- `CommandResponse SetUserRole(UserRoles role)`: Controls the available options on the Welcome screen (From FW 1.8.14035 to 3.12.0)
- `CommandResponse ShowPopup(string message)`: Shows a popup on Polyscope with the specified message. The popup-text will be translated to the selected language, if the text exists in the language file. (From FW 1.6)
- `CommandResponse Shutdown()`: Shuts down and turns off robot and controller. Closes the connection. (From FW 1.4)
- `CommandResponse Stop()`: Stops running program. (From FW 1.4) Returns failure if the program fails to stop
- `CommandResponse UnlockProtectiveStop()`: Closes the current popup and unlocks protective stop. (From FW 3.1)
- Inherited from [URServiceBase](UnderAutomation.UniversalRobots.Internal.md#urservicebase-robot): `InternalErrorOccured`

## DashboardClientParametersBase

`abstract class DashboardClientParametersBase`

Abstract base class for Dashboard Server connection parameters, providing default port and timeout values.

- `const int DEFAULT_PORT = 29999`: Default Dashboard server TCP port
- `const int DEFAULT_RECEIVE_TIMEOUT_MS = 2000`: Default receive timeout in milliseconds
- `const int DEFAULT_SEND_TIMEOUT_MS = 500`: Default send timeout in milliseconds
- `int Port { get; set; }`: Dashboard client TCP port. Default : 29999
- `int ReceiveTimeoutMs { get; set; }`: Receive timeout in milliseconds. Default : 2000 ms
- `int SendTimeoutMs { get; set; }`: Send timeout in milliseconds. Default : 500 ms
