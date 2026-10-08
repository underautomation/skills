# underautomation.fanuc.common.files.diagnosis

## CurrentPosition

`from underautomation.fanuc.common.files.diagnosis.current_position import CurrentPosition`

Contains the position for each robots

- `CurrentPosition()`
- `groups_position: typing.List[GroupPosition] (read only)`: Position of each robots handled by this controller
- `name: str (read only)`: File name : curpos.dg

## CurrentPositionReader

`from underautomation.fanuc.common.files.diagnosis.current_position_reader import CurrentPositionReader`

Parser for reading and interpreting current robot position data from diagnostic files.

- `CurrentPositionReader()`
- `after_parse() -> None`
- `parse_line(line: str) -> None`
- `section_start: typing.List[str] (read only)`
- `section: CurrentPosition`: The parsed section instance.
- Inherited from [SectionParser](underautomation.fanuc.common.files.md#sectionparser): `can_handle_section`, `end_of_file`

## DiagnosisReader2

`from underautomation.fanuc.common.files.diagnosis.diagnosis_reader_2 import DiagnosisReader2`

Generic diagnosis file reader that parses a specific section from a diagnostic stream.

- `read_file(filePath: str, language: Languages) -> T`: Read and decode the file on disc
- Inherited from [FileReader](underautomation.fanuc.common.files.md#filereader): `file_name`

## Feature

`from underautomation.fanuc.common.files.diagnosis.feature import Feature`

Represents a single software feature installed on the controller.

- `Feature()`
- `name: str`: Name of the feature
- `order_no: str`: Order number of the feature (set of 4 alphanumeric characters)

## Features

`from underautomation.fanuc.common.files.diagnosis.features import Features`

Represents the collection of features available on the controller.

- `Features()`
- `features_list: typing.List[Feature] (read only)`: List of features
- `has_telnet: bool (read only)`: Indicates if the robot has the TELNET feature enabled (TELN).
- `has_snpx: bool (read only)`: Indicates if the robot has the SNPX feature enabled (R553 or R651).
- `has_ascii_upload: bool (read only)`: Indicates if the robot has the ASCII upload feature enabled : R507 ("ASCII Upload" on older controllers) or R796 ("ASCII Program Loader" on most recent controllers).
- `has_stream_motion: bool (read only)`: Indicates if the robot has the Stream Motion feature enabled (J519).

## FeaturesParser

`from underautomation.fanuc.common.files.diagnosis.features_parser import FeaturesParser`

Parser for reading and interpreting controller feature data from diagnostic files.

- `FeaturesParser()`
- `parse_line(line: str) -> None`
- `after_parse() -> None`
- `section_start: typing.List[str] (read only)`
- `section: Features`: The parsed section instance.
- Inherited from [SectionParser](underautomation.fanuc.common.files.md#sectionparser): `can_handle_section`, `end_of_file`

## GroupPosition

`from underautomation.fanuc.common.files.diagnosis.group_position import GroupPosition`

Complete position information of a group

- `GroupPosition()`
- `id: int (read only)`: Group ID
- `joints_position: JointsPosition (read only)`: Joint positions : the position of each robot angles
- `user_frame_positions: typing.List[CartesianPositionWithUserFrame] (read only)`: Position of each tools in each user frames
- `world_positions: typing.List[CartesianPositionWithTool] (read only)`: Position of each tools in world coordinates

## HeaderSection

`from underautomation.fanuc.common.files.diagnosis.header_section import HeaderSection`

Header information of a diagnostic file

- `HeaderSection()`
- `f_number: str (read only)`: Failsafe number
- `version: str (read only)`: Controller version
- `version_firmware: str (read only)`: Firmware version
- `version_date: datetime (read only)`: Firmware release date
- `date: datetime (read only)`: Current controller time

## IOState

`from underautomation.fanuc.common.files.diagnosis.io_state import IOState`

Status of all controller inputs and outputs

- `IOState()`
- `states: typing.List[IOStatus] (read only)`: Status of all controller inputs and outputs
- `name: str (read only)`: File name : iostate.dg

## IOStateParser

`from underautomation.fanuc.common.files.diagnosis.io_state_parser import IOStateParser`

Parser for reading and interpreting IO state data from diagnostic files.

- `IOStateParser()`
- `parse_line(line: str) -> None`
- `after_parse() -> None`
- `section_start: typing.List[str] (read only)`
- `section: IOState`: The parsed section instance.
- Inherited from [SectionParser](underautomation.fanuc.common.files.md#sectionparser): `can_handle_section`, `end_of_file`

## ProgramStates

`from underautomation.fanuc.common.files.diagnosis.program_states import ProgramStates`

Implements IFanucContent to hold a collection of task states.

- `ProgramStates()`
- `task_states: typing.List[TaskState]`: Array of task states currently on the controller.
- `name: str (read only)`: File name: prgstate.dg

## ProgramStatesParser

`from underautomation.fanuc.common.files.diagnosis.program_states_parser import ProgramStatesParser`

Parser for the "TASK STATES" section, renamed from ProgramStatesReader to ProgramStatesParser. Uses compiled Regex for efficiency.

- `ProgramStatesParser()`
- `parse_line(line: str) -> None`
- `after_parse() -> None`
- `section_start: typing.List[str] (read only)`
- `section: ProgramStates`: The parsed section instance.
- Inherited from [SectionParser](underautomation.fanuc.common.files.md#sectionparser): `can_handle_section`, `end_of_file`

## SafetyStatus

`from underautomation.fanuc.common.files.diagnosis.safety_status import SafetyStatus`

Safety status informations

- `SafetyStatus()`
- `external_e_stop: bool (read only)`: External emergency stop active
- `sope_stop: bool (read only)`: Emergency stop active by SOP signal
- `tpe_stop: bool (read only)`: Emergency stop active on teach peandant
- `hand_broken: bool (read only)`: Hand broken signal is active
- `over_travel: bool (read only)`: Over travel limit is active
- `low_air_alarm: bool (read only)`: Low air pressure alarm is active
- `fence_open: bool (read only)`: Safety fence is open
- `belt_broken: bool (read only)`: Belt broken signal is active
- `tp_enable: bool (read only)`: Teach pendant is enabled
- `tp_deadman: bool (read only)`: The deadman switch of the teach pendant is active
- `svoff_detect: bool (read only)`: Servo off detection is active
- `non_teacher_enb: bool (read only)`: Non-teacher enable signal is active
- `name: str (read only)`: File name : sftysig.dg

## SafetyStatusParser

`from underautomation.fanuc.common.files.diagnosis.safety_status_parser import SafetyStatusParser`

Parser for reading and interpreting safety status signals from diagnostic files.

- `SafetyStatusParser()`
- `parse_line(line: str, start: str, setValue: typing.Callable[[bool], None]) -> None`: Parses a single line, checking if it starts with the specified prefix and extracting a boolean value.
- `parse_line(line: str) -> None`
- `section_start: typing.List[str] (read only)`
- `section: SafetyStatus`: The parsed section instance.
- Inherited from [SectionParser](underautomation.fanuc.common.files.md#sectionparser): `can_handle_section`, `after_parse`, `end_of_file`

## SummaryDiagnosis

`from underautomation.fanuc.common.files.diagnosis.summary_diagnosis import SummaryDiagnosis`

All diagnosis information

- `SummaryDiagnosis()`
- `name: str (read only)`: File name : summary.dg
- `current_position: CurrentPosition (read only)`: Current position of each robots and groups handled by this controller
- `safety: SafetyStatus (read only)`: Controller safety information
- `i_os: IOState (read only)`: Controller IO status
- `features: Features (read only)`: Controller features status
- `program_states: ProgramStates (read only)`: Controller program states

## SummaryDiagnosisReader

`from underautomation.fanuc.common.files.diagnosis.summary_diagnosis_reader import SummaryDiagnosisReader`

Read and parse the file summary.dg

- `read_file(filePath: str, language: Languages) -> SummaryDiagnosis`: Read and decode the file on disc
- Inherited from [FileReader](underautomation.fanuc.common.files.md#filereader): `file_name`

## TaskHistoryData

`from underautomation.fanuc.common.files.diagnosis.task_history_data import TaskHistoryData`

Represents one frame in the task's call stack.

- `TaskHistoryData()`
- `routine_depth: int`: Depth of the routine in the call stack.
- `routine_name: str`: Name of the routine.
- `line_number: int`: Line number currently being executed.
- `program_name: str`: Name of the program containing the routine.
- `program_type: ProgramType`: Type of the program (TP, Karel, etc.).

## TaskState

`from underautomation.fanuc.common.files.diagnosis.task_state import TaskState`

Represents a single task's state.

- `TaskState()`
- `number: int`: Task number.
- `name: str`: Task name.
- `status: TaskStatus`: Current execution status of the task.
- `history: typing.List[TaskHistoryData]`: Call stack history frames for the task.
