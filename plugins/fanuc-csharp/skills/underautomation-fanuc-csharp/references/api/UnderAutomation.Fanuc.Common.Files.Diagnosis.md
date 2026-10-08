# UnderAutomation.Fanuc.Common.Files.Diagnosis

## CurrentPosition

`class CurrentPosition : IFanucContent`

Contains the position for each robots

- `CurrentPosition()`
- `GroupPosition[] GroupsPosition { get; }`: Position of each robots handled by this controller
- `string Name { get; }`: File name : curpos.dg

## CurrentPositionReader

`class CurrentPositionReader : SectionParser<CurrentPosition>`

Parser for reading and interpreting current robot position data from diagnostic files.

- `CurrentPositionReader()`
- `void AfterParse()`: Called after all lines have been parsed. Override to perform final processing.
- `void ParseLine(string line)`: Parses a single line from the section content.
- `string[] SectionStart { get; }`: Gets the possible section header strings that indicate the start of this section.
- `readonly CurrentPosition Section`: The parsed section instance.
- Inherited from [SectionParser](UnderAutomation.Fanuc.Common.Files.md#sectionparser): `CanHandleSection`, `EndOfFile`

## DiagnosisReader<T, U>

`class DiagnosisReader<T, U> : FileReader<T>, IFileReader<T>, IFileReader where T : IFanucContent, new() where U : SectionParser<T>, new()`

Generic diagnosis file reader that parses a specific section from a diagnostic stream.

- `T ReadFile(Stream fileStream, Languages language, string fileName = null)`: Read and decode the file stream
- Inherited from [FileReader](UnderAutomation.Fanuc.Common.Files.md#filereader): `FileName`

## Feature

`class Feature`

Represents a single software feature installed on the controller.

- `Feature()`
- `string Name { get; set; }`: Name of the feature
- `string OrderNo { get; set; }`: Order number of the feature (set of 4 alphanumeric characters)

## Features

`class Features`

Represents the collection of features available on the controller.

- `Features()`
- `Feature[] FeaturesList { get; }`: List of features
- `bool HasAsciiUpload { get; }`: Indicates if the robot has the ASCII upload feature enabled : R507 ("ASCII Upload" on older controllers) or R796 ("ASCII Program Loader" on most recent controllers).
- `bool HasSnpx { get; }`: Indicates if the robot has the SNPX feature enabled (R553 or R651).
- `bool HasStreamMotion { get; }`: Indicates if the robot has the Stream Motion feature enabled (J519).
- `bool HasTelnet { get; }`: Indicates if the robot has the TELNET feature enabled (TELN).

## FeaturesParser

`class FeaturesParser : SectionParser<Features>`

Parser for reading and interpreting controller feature data from diagnostic files.

- `FeaturesParser()`
- `void AfterParse()`: Called after all lines have been parsed. Override to perform final processing.
- `void ParseLine(string line)`: Parses a single line from the section content.
- `string[] SectionStart { get; }`: Gets the possible section header strings that indicate the start of this section.
- `readonly Features Section`: The parsed section instance.
- Inherited from [SectionParser](UnderAutomation.Fanuc.Common.Files.md#sectionparser): `CanHandleSection`, `EndOfFile`

## GroupPosition

`class GroupPosition`

Complete position information of a group

- `GroupPosition()`
- `int Id { get; }`: Group ID
- `JointsPosition JointsPosition { get; }`: Joint positions : the position of each robot angles
- `CartesianPositionWithUserFrame[] UserFramePositions { get; }`: Position of each tools in each user frames
- `CartesianPositionWithTool[] WorldPositions { get; }`: Position of each tools in world coordinates

## HeaderSection

`class HeaderSection`

Header information of a diagnostic file

- `HeaderSection()`
- `DateTime Date { get; }`: Current controller time
- `string FNumber { get; }`: Failsafe number
- `string Version { get; }`: Controller version
- `DateTime VersionDate { get; }`: Firmware release date
- `string VersionFirmware { get; }`: Firmware version

## IOState

`class IOState : IFanucContent`

Status of all controller inputs and outputs

- `IOState()`
- `string Name { get; }`: File name : iostate.dg
- `IOStatus[] States { get; }`: Status of all controller inputs and outputs

## IOStateParser

`class IOStateParser : SectionParser<IOState>`

Parser for reading and interpreting IO state data from diagnostic files.

- `IOStateParser()`
- `void AfterParse()`: Called after all lines have been parsed. Override to perform final processing.
- `void ParseLine(string line)`: Parses a single line from the section content.
- `string[] SectionStart { get; }`: Gets the possible section header strings that indicate the start of this section.
- `readonly IOState Section`: The parsed section instance.
- Inherited from [SectionParser](UnderAutomation.Fanuc.Common.Files.md#sectionparser): `CanHandleSection`, `EndOfFile`

## ProgramStates

`class ProgramStates : IFanucContent`

Implements IFanucContent to hold a collection of task states.

- `ProgramStates()`
- `string Name { get; }`: File name: prgstate.dg
- `TaskState[] TaskStates { get; set; }`: Array of task states currently on the controller.

## ProgramStatesParser

`class ProgramStatesParser : SectionParser<ProgramStates>`

Parser for the "TASK STATES" section, renamed from ProgramStatesReader to ProgramStatesParser. Uses compiled Regex for efficiency.

- `ProgramStatesParser()`
- `void AfterParse()`: Called after all lines have been parsed. Override to perform final processing.
- `void ParseLine(string line)`: Parses a single line from the section content.
- `string[] SectionStart { get; }`: Gets the possible section header strings that indicate the start of this section.
- `readonly ProgramStates Section`: The parsed section instance.
- Inherited from [SectionParser](UnderAutomation.Fanuc.Common.Files.md#sectionparser): `CanHandleSection`, `EndOfFile`

## SafetyStatus

`class SafetyStatus : IFanucContent`

Safety status informations

- `SafetyStatus()`
- `bool BeltBroken { get; }`: Belt broken signal is active
- `bool ExternalEStop { get; }`: External emergency stop active
- `bool FenceOpen { get; }`: Safety fence is open
- `bool HandBroken { get; }`: Hand broken signal is active
- `bool LowAirAlarm { get; }`: Low air pressure alarm is active
- `string Name { get; }`: File name : sftysig.dg
- `bool NonTeacherEnb { get; }`: Non-teacher enable signal is active
- `bool OverTravel { get; }`: Over travel limit is active
- `bool SOPEStop { get; }`: Emergency stop active by SOP signal
- `bool SVOFFDetect { get; }`: Servo off detection is active
- `bool TPDeadman { get; }`: The deadman switch of the teach pendant is active
- `bool TPEStop { get; }`: Emergency stop active on teach peandant
- `bool TPEnable { get; }`: Teach pendant is enabled

## SafetyStatusParser

`class SafetyStatusParser : SectionParser<SafetyStatus>`

Parser for reading and interpreting safety status signals from diagnostic files.

- `SafetyStatusParser()`
- `void ParseLine(string line)`: Parses a single line from the section content.
- `void ParseLine(string line, string start, Action<bool> setValue)`: Parses a single line, checking if it starts with the specified prefix and extracting a boolean value.
- `string[] SectionStart { get; }`: Gets the possible section header strings that indicate the start of this section.
- `readonly SafetyStatus Section`: The parsed section instance.
- Inherited from [SectionParser](UnderAutomation.Fanuc.Common.Files.md#sectionparser): `CanHandleSection`, `AfterParse`, `EndOfFile`

## SummaryDiagnosis

`class SummaryDiagnosis : IFanucContent`

All diagnosis information

- `SummaryDiagnosis()`
- `CurrentPosition CurrentPosition { get; }`: Current position of each robots and groups handled by this controller
- `Features Features { get; }`: Controller features status
- `IOState IOs { get; }`: Controller IO status
- `string Name { get; }`: File name : summary.dg
- `ProgramStates ProgramStates { get; }`: Controller program states
- `SafetyStatus Safety { get; }`: Controller safety information

## SummaryDiagnosisReader

`class SummaryDiagnosisReader : FileReader<SummaryDiagnosis>, IFileReader<SummaryDiagnosis>, IFileReader`

Read and parse the file summary.dg

- `SummaryDiagnosis ReadFile(Stream fileStream, Languages language, string fileName)`: Read and parse the file
- Inherited from [FileReader](UnderAutomation.Fanuc.Common.Files.md#filereader): `FileName`

## TaskHistoryData

`class TaskHistoryData`

Represents one frame in the task's call stack.

- `TaskHistoryData()`
- `int LineNumber { get; set; }`: Line number currently being executed.
- `string ProgramName { get; set; }`: Name of the program containing the routine.
- `ProgramType ProgramType { get; set; }`: Type of the program (TP, Karel, etc.).
- `int RoutineDepth { get; set; }`: Depth of the routine in the call stack.
- `string RoutineName { get; set; }`: Name of the routine.

## TaskState

`class TaskState`

Represents a single task's state.

- `TaskState()`
- `TaskHistoryData[] History { get; set; }`: Call stack history frames for the task.
- `string Name { get; set; }`: Task name.
- `int Number { get; set; }`: Task number.
- `TaskStatus Status { get; set; }`: Current execution status of the task.
