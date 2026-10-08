# UnderAutomation.Fanuc.Cgtp.Internal

## CgtpClientBase (robot.Cgtp)

`abstract class CgtpClientBase`

Base implementation for the CGTP Web Server client.

- `void AbortTask(string progName = null)`: Abort the task specified by progName. Set to null to abort all user tasks. From firmware 9.10
- `void ChangeActiveProgram(string progName)`: Change the active TP program to progName. From firmware 9.10
- `void CreateProgram(string progName, string owner = null, string comment = null, int defaultGroup = 0, CgtpProgramSubType subType = CgtpProgramSubType.None)`: Create a new TP program on the controller. From firmware 9.10
- `void DeleteProgram(string progName)`: Delete the program progName from the controller. From firmware 9.10
- `void DeleteSourceLines(string progName, int lineNum, int count = 1)`: Delete count lines starting at lineNum in program progName. From firmware 9.10
- `void Disconnect()`: Disconnect from the CGTP Web Server. After calling this method, the client must be reconnected before it can be used again.
- `bool Enabled { get; }`: Indicates whether the client is currently connected to the CGTP Web Server.
- `CartesianPosition ForwardKinematics(int group, JointsPosition jointPosition, int userTool = -1, int userFrame = -1)`: Compute the forward kinematics on the controller: convert joint angles to a Cartesian position.
- `string[] GetComments(CgtpCommentType type)`: Read all comments for the specified element type. For I/O types (RI, RO, DI, DO, GI, GO, AI, AO), returns the input or output comments accordingly.
- `string GetFileAsString(string pathName)`: Download the content of a file from the controller as a string. From firmware 9.10
- `IOComments GetIoComments(CgtpCommentIoType type)`: Read all I/O comments for the specified I/O type.
- `bool GetIoSimulationStatus(CgtpIoPortType portType, int index)`: Check whether I/O port at index of type portType is simulated. From firmware 8.30
- `string GetProgramComment(string progName)`: Get the comment of program progName. From firmware 9.10
- `bool GetProgramIgnorePause(string progName)`: Get whether program progName ignores pause requests. From firmware 9.10
- `string GetProgramOwner(string progName)`: Get the owner of program progName. From firmware 9.10
- `int GetProgramStackSize(string progName)`: Get the stack size of program progName. From firmware 9.10
- `CgtpProgramSubType GetProgramSubType(string progName)`: Get the sub-type of program progName. From firmware 9.10
- `bool GetProgramWriteProtect(string progName)`: Get whether program progName is write-protected. From firmware 9.10
- `CgtpHttpClient Http { get; }`: Provides methods to download and decode files from the controller via HTTP.
- `void InsertSourceLine(string progName, string lineContent, int lineNum)`: Insert a source line before lineNum in program progName. From firmware 9.10
- `JointsPosition InvertKinematics(int group, CartesianPosition cartesianPosition, int userTool = -1, int userFrame = -1)`: Compute the inverse kinematics on the controller: convert a Cartesian position to joint angles.
- `CgtpKclClient Kcl { get; }`: KCL client for executing KCL commands over CGTP. Use it instead of the Telnet KCL client, which is a legacy protocol. Some commands are sent in Unsafe mode: the controller returns no status, so the result cannot tell if the command was executed. To start a program, prefer RunProgram().
- `Languages Language { get; set; }`: Controller language (default is English)
- `string[] ListFiles(string pathName = "MD:")`: List files at the specified path on the controller. From firmware 9.40
- `string[] ListPrograms(CgtpProgramType type, CgtpProgramSubType subType)`: List all TP or Karel programs on the controller
- `string[] ListTpPrograms()`: List all TP programs on the controller, regardless of their sub-type.
- `void PauseAllPrograms()`: Pause program execution on the controller. From firmware 9.10
- `CgtpBatchReadResult ReadBatchVariables(CgtpBatchVariables variables)`: Read multiple variables from the controller in a single batch operation. Each variable in variables will be updated with the value read from the controller.
- `CartesianPosition ReadCartesianPosition(int groupNum = 1)`: Read the current Cartesian position of motion group groupNum. From firmware 9.10
- `int ReadIo(CgtpIoPortType portType, int index)`: Read the value of I/O port at index of type portType. From firmware 8.30
- `JointsPosition ReadJointPosition(int groupNum = 1)`: Read the current joint angles of motion group groupNum. From firmware 9.10
- `NumericRegisterWithComment ReadNumericRegisterWithComment(int index)`: Read the numeric register (R[]) at index. From firmware 9.10
- `NumericRegisterWithComment[] ReadNumericRegistersWithComment()`: Read all numeric registers (R[]) with their comments and values.
- `PositionRegisterWithComment ReadPositionRegisterWithComment(int index, int groupNum = 1)`: Read the position register (PR[]) at index for motion group groupNum. From firmware 9.10
- `StringRegisterWithComment[] ReadStringRegistersWithComment()`: Read all string registers (SR[]) with their comments and values.
- `UserAlarmDefinition[] ReadUserAlarms()`: Read all user alarm definitions with their comments and severity.
- `CgtpVariableValue ReadVariable(string varName, string progName = null)`: Read the typed value of variable varName in program progName. From firmware 9.10
- `string ReadVariableAsString(string varName, string progName = null)`: Read the value of variable varName in program progName. From firmware 9.10
- `void RenameProgram(string sourceName, string newName)`: Rename program sourceName to newName. From firmware 9.10
- `void ReplaceSourceLine(string progName, string lineContent, int lineNum)`: Replace the source line at lineNum in program progName. From firmware 9.10
- `void RunProgram(string progName, int lineNum = 1)`: Run the specified program starting at lineNum. From firmware 9.30
- `void SelectProgram(string progName, int lineNum = 1)`: Open the TP program progName and move cursor to lineNum. From firmware 9.10
- `void SetComment(CgtpCommentType type, int index, string comment)`: Set the comment of a register or I/O port identified by type and index.
- `void SetProgramComment(string progName, string comment)`: Set the comment of program progName. From firmware 9.10
- `void SetProgramIgnorePause(string progName, bool ignorePause)`: Set whether program progName ignores pause requests. From firmware 9.10
- `void SetProgramOwner(string progName, string owner)`: Set the owner of program progName. From firmware 9.10
- `void SetProgramPosition(string progName, int positionIndex, Position position)`: Set position at index positionIndex in program progName to the given position. Supports both joint and Cartesian representations. Only the first motion group is supported via CGTP. From firmware 9.10
- `CartesianPosition SetProgramPositionToCurrentCartesianPosition(string progName, int positionIndex, int groupNumber = 1)`: Set position at index positionIndex to the current Cartesian position in program progName and return the updated position.
- `void SetProgramStackSize(string progName, int stackSize)`: Set the stack size of program progName. From firmware 9.10
- `void SetProgramSubType(string progName, CgtpProgramSubType subType)`: Set the sub-type of program progName. From firmware 9.10
- `void SetProgramWriteProtect(string progName, bool writeProtect)`: Set whether program progName is write-protected. From firmware 9.10
- `void SetUserAlarmSeverity(int index, int severity)`: Set the severity of a user alarm.
- `void SimulateIo(CgtpIoPortType portType, int index)`: Set I/O port at index of type portType to simulated. From firmware 8.30
- `void UnsimulateIo(CgtpIoPortType portType, int index)`: Remove simulation from I/O port at index of type portType. From firmware 8.30
- `CgtpBatchWriteResult WriteBatchVariables(CgtpBatchVariables variables)`: Write multiple variables to the controller in a single batch operation.
- `void WriteIo(CgtpIoPortType portType, int index, int value)`: Set the value of I/O port at index of type portType. From firmware 8.30
- `void WriteNumericRegisterAsDouble(int index, double value)`: Write a real (double) value to numeric register R[index].
- `void WriteNumericRegisterAsInteger(int index, int value)`: Write an integer value to numeric register R[index].
- `void WritePositionRegisterAsCartesian(int index, CartesianPosition value, int groupNum = 1)`: Write a cartesian position value to a position register (PR[])
- `void WritePositionRegisterAsJoint(int index, JointsPosition value, int groupNum = 1)`: Write a joint position value to a position register (PR[])
- `void WriteStringRegister(int index, string value)`: Write a string value to string register SR[index].
- `void WriteVariable(string varName, double value, string progName = null)`: Write a real (double) value to variable varName in program progName. From firmware 8.30
- `void WriteVariable(string varName, int value, string progName = null)`: Write an integer value to variable varName in program progName. From firmware 8.30
- `void WriteVariable(string varName, string value, string progName = null)`: Write value to variable varName in program progName. From firmware 8.30

## CgtpClientInternal (robot.Cgtp)

`class CgtpClientInternal : CgtpClientBase`

Internal CGTP Web Server client used by the library infrastructure.

- Inherited from [CgtpClientBase](UnderAutomation.Fanuc.Cgtp.Internal.md#cgtpclientbase-robotcgtp): `Disconnect`, `AbortTask`, `SelectProgram`, `DeleteProgram`, `GetProgramComment`, `SetProgramComment`, `GetProgramOwner`, `SetProgramOwner`, `GetProgramStackSize`, `SetProgramStackSize`, `GetProgramIgnorePause`, `SetProgramIgnorePause`, `GetProgramWriteProtect`, `SetProgramWriteProtect`, `GetProgramSubType`, `SetProgramSubType`, `CreateProgram`, `RenameProgram`, `ListPrograms`, `ListTpPrograms`, `DeleteSourceLines`, `InsertSourceLine`, `ReplaceSourceLine`, `SetProgramPositionToCurrentCartesianPosition`, `SetProgramPosition`, `RunProgram`, `ChangeActiveProgram`, `PauseAllPrograms`, `ReadVariableAsString`, `ReadVariable`, `WriteVariable`, `SetComment`, `WriteNumericRegisterAsDouble`, `WriteNumericRegisterAsInteger`, `WriteStringRegister`, `SetUserAlarmSeverity`, `ReadNumericRegistersWithComment`, `ReadStringRegistersWithComment`, `ReadUserAlarms`, `GetIoComments`, `GetComments`, `ReadNumericRegisterWithComment`, `ReadPositionRegisterWithComment`, `ReadBatchVariables`, `WritePositionRegisterAsCartesian`, `WritePositionRegisterAsJoint`, `WriteBatchVariables`, `ReadIo`, `WriteIo`, `GetIoSimulationStatus`, `SimulateIo`, `UnsimulateIo`, `ReadCartesianPosition`, `ReadJointPosition`, `InvertKinematics`, `ForwardKinematics`, `ListFiles`, `GetFileAsString`, `Kcl`, `Http`, `Language`, `Enabled`

## CgtpConnectParametersBase

`class CgtpConnectParametersBase`

Base class for CGTP Web Server connection parameters.

- `CgtpConnectParametersBase()`
- `const int DEFAULT_PORT = 3080`: Default HTTP port for CGTP Web Server.
- `const int DEFAULT_REQUEST_TIMEOUT_MS = 3000`: Default request timeout in milliseconds.
- `string Login { get; set; }`: Login for HTTP Basic authentication (optional).
- `string Password { get; set; }`: Password for HTTP Basic authentication (optional).
- `int Port { get; set; }`: HTTP port number of the CGTP Web Server.
- `int RequestTimeoutMs { get; set; }`: HTTP request timeout in milliseconds.

## CgtpHttpClient (robot.Cgtp.Http)

`class CgtpHttpClient : FileClientBase`

Provides methods to download and list files from the controller via HTTP.

- `string BasePath { get; set; }`: Base path used to build the download URL. Default is "MD".
- `byte[] DownloadAsBytes(string fileName)`: Download a file from the controller and return its raw bytes.
- `Stream DownloadAsStream(string fileName)`: Download a file from the controller and return a readable stream. Otherwise the raw binary response is returned.
- `string DownloadAsString(string fileName)`: Download a file from the controller and return its content as a string.
- `string[] EnumerateVariableFileNames()`: Get the list of all variable file names available on the controller
- `string IP { get; }`: IP address of the controller
- `CgtpFileItem[] ListDiagnosticFiles()`: List diagnostic and error files available on the controller.
- `CgtpFileItem[] ListOtherFiles()`: List other files available on the controller.
- `CgtpAsciiFileItem[] ListTpPrograms()`: List TP program files available on the controller.
- `CgtpAsciiFileItem[] ListVariableFiles()`: List variable files available on the controller.
- Inherited from [FileClientBase](UnderAutomation.Fanuc.Common.Files.md#fileclientbase-robotftp): `GetSummaryDiagnostic`, `GetAllErrorsList`, `GetCurrentPosition`, `GetIOState`, `GetSafetyStatus`, `GetProgramStates`, `GetVariablesFromFile`, `GetAllVariables`, `KnownVariableFiles`

## CgtpKclClient (robot.Cgtp.Kcl)

`class CgtpKclClient : KclClientBase`

KCL client that uses the web server of the controller (CGTP) instead of Telnet. It has the same commands as the Telnet KCL client and does not need a Telnet password. Some commands (Abort, AbortAll, ClearProgram, ClearVars, Continue, Hold, Pause, Run, StepOn, StepOff, SendCustomCommandUnsafe) are...

- `bool Enabled { get; }`: Indicates whether the KCL client is currently connected.
- `CustomCommandResult SendCustomCommandUnsafe(string command)`: Sends a custom KCL command in Unsafe mode. Success or failure cannot be determined from the result.
- Inherited from [KclClientBase](UnderAutomation.Fanuc.Common.Kcl.md#kclclientbase-robottelnet): `Abort`, `AbortAll`, `ClearAll`, `ClearProgram`, `ClearVars`, `Continue`, `Hold`, `Pause`, `Reset`, `Run`, `SetPort`, `SetVariable`, `GetCurrentPose`, `GetVariable`, `Simulate`, `UnsimulateAll`, `Unsimulate`, `SendCustomCommand`, `SendCustomCommand``1`, `GetTaskInformation`, `AddBreakpoint`, `RemoveBreakpoint`, `RemoveAllBreakpoints`, `GetBreakpoints`, `StepOn`, `StepOff`
