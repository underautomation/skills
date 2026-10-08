# underautomation.fanuc.common.files

## FanucFileReaders

`from underautomation.fanuc.common.files.fanuc_file_readers import FanucFileReaders`

Contains static functions to decode Fanuc files (variables, diagnosis, listing, ...)

- `static read_file(fileName: str, language: Languages) -> IFanucContent`: Read any file by path on disc, recognize it by name and decode it
- `static readers: typing.List[IFileReader1] (read only)`: Get the collection of all parsers
- `static VariableReader: VariableReader`: Helper to read variable files *.va
- `static ErrorListReader: ErrorListReader`: Helper to read error files like errall.ls
- `static SummaryDiagnosticReader: SummaryDiagnosisReader`: Helper to read summary diagnosis file summary.dg
- `static CurrentPositionReader: DiagnosisReader2[CurrentPosition, CurrentPositionReader]`: Decode current position file curpos.dg
- `static IOStateReader: DiagnosisReader2[IOState, IOStateParser]`: Decode IO Status file iostate.dg
- `static SafetyStatusReader: DiagnosisReader2[SafetyStatus, SafetyStatusParser]`: Decode IO Status file iostate.dg
- `static ProgramStates: DiagnosisReader2[ProgramStates, ProgramStatesParser]`: Decode task and program states prgstate.dg

## FileClientBase (robot.ftp)

`from underautomation.fanuc.common.files.file_client_base import FileClientBase`

Base class for Fanuc file client. It provides methods to read and parse known files such as summary diagnostic, error list, current position, ...

- `get_summary_diagnostic() -> SummaryDiagnosis`: Get controller status (position, safety, ios, ...)
- `get_all_errors_list() -> ErrorList`: Get a list of all errors logged by the controller
- `get_current_position() -> CurrentPosition`: Get current robot position of each robot handled by this controller
- `get_io_state() -> IOState`: Get controller IO State
- `get_safety_status() -> SafetyStatus`: Get controller safety status
- `get_program_states() -> ProgramStates`: Get controller program states
- `get_variables_from_file(variableFileName: str) -> GenericVariableFile`: Get and parse a variable file from its name
- `enumerate_variable_file_names() -> typing.List[str]`: Get the list of all variable file names available on the controller
- `get_all_variables(progress: typing.Callable[[float], None] | OnProgressDelegate=None) -> VariableFileList`: Get the list of all variables on the controller. All variables files are read and decoded
- `known_variable_files: KnownVariableFiles (read only)`: A list of method to read specific files
- `ip: str (read only)`: IP address of the controller

## FileReader1

`from underautomation.fanuc.common.files.file_reader_1 import FileReader1`

File reader for specific files

- `read_file(filePath: str, language: Languages) -> T`: Read and decode the file on disc
- Inherited from [FileReader](underautomation.fanuc.common.files.md#filereader): `file_name`

## FileReader

`from underautomation.fanuc.common.files.file_reader import FileReader`

Read and decode fanuc files

- `file_name: str (read only)`: File name

## IFanucContent

`from underautomation.fanuc.common.files.i_fanuc_content import IFanucContent`

Interface of a file that comes from a Fanuc controller

- `name: str (read only)`: File name

## IFileReader1

`from underautomation.fanuc.common.files.i_file_reader_1 import IFileReader1`

Interface for Fanuc file readers

- `read_file(filePath: str, language: Languages) -> T`: Reads file by path and decodes it
- Inherited from [IFileReader](underautomation.fanuc.common.files.md#ifilereader): `file_name`

## IFileReader

`from underautomation.fanuc.common.files.i_file_reader import IFileReader`

Interface for Fanuc file readers

- `file_name: str (read only)`: File name

## KnownVariableFiles (robot.ftp.known_variable_files)

`from underautomation.fanuc.common.files.known_variable_files import KnownVariableFiles`

Wrapper class of methods to download and decode variable files

- `get_aavmmain_file() -> AavmmainFile`: Reads and parse aavmmain.va variable file
- `get_bicsetup_file() -> BicsetupFile`: Reads and parse bicsetup.va variable file
- `get_cbparam_file() -> CbparamFile`: Reads and parse cbparam.va variable file
- `get_cellio_file() -> CellioFile`: Reads and parse cellio.va variable file
- `get_comset_file() -> ComsetFile`: Reads and parse comset.va variable file
- `get_diocfgsv_file() -> DiocfgsvFile`: Reads and parse diocfgsv.va variable file
- `get_gemdata_file() -> GemdataFile`: Reads and parse gemdata.va variable file
- `get_htcolrec_file() -> HtcolrecFile`: Reads and parse htcolrec.va variable file
- `get_httpkcl_file() -> HttpkclFile`: Reads and parse httpkcl.va variable file
- `get_irc_counter_file() -> IrcCounterFile`: Reads and parse irc_counter.va variable file
- `get_irc_msg_file() -> IrcMsgFile`: Reads and parse irc_msg.va variable file
- `get_irc_status_file() -> IrcStatusFile`: Reads and parse irc_status.va variable file
- `get_irc_stlabel_file() -> IrcStlabelFile`: Reads and parse irc_stlabel.va variable file
- `get_klaction_file() -> KlactionFile`: Reads and parse klaction.va variable file
- `get_mixlogic_file() -> MixlogicFile`: Reads and parse mixlogic.va variable file
- `get_mtparam_file() -> MtparamFile`: Reads and parse mtparam.va variable file
- `get_numreg_file() -> NumregFile`: Reads and parse numreg.va variable file
- `get_palreg_file() -> PalregFile`: Reads and parse palreg.va variable file
- `get_posreg_file() -> PosregFile`: Reads and parse posreg.va variable file
- `get_strreg_file() -> StrregFile`: Reads and parse strreg.va variable file
- `get_swiupdt_file() -> SwiupdtFile`: Reads and parse swiupdt.va variable file
- `get_sycldint_file() -> SycldintFile`: Reads and parse sycldint.va variable file
- `get_symotn_file() -> SymotnFile`: Reads and parse symotn.va variable file
- `get_synosave_file() -> SynosaveFile`: Reads and parse synosave.va variable file
- `get_sysframe_file() -> SysframeFile`: Reads and parse sysframe.va variable file
- `get_sysfsac_file() -> SysfsacFile`: Reads and parse sysfsac.va variable file
- `get_syshost_file() -> SyshostFile`: Reads and parse syshost.va variable file
- `get_sysmacro_file() -> SysmacroFile`: Reads and parse sysmacro.va variable file
- `get_sysmast_file() -> SysmastFile`: Reads and parse sysmast.va variable file
- `get_syspass_file() -> SyspassFile`: Reads and parse syspass.va variable file
- `get_sysservo_file() -> SysservoFile`: Reads and parse sysservo.va variable file
- `get_system_file() -> SystemFile`: Reads and parse system.va variable file
- `get_sysuif_file() -> SysuifFile`: Reads and parse sysuif.va variable file
- `get_tpsnap_file() -> TpsnapFile`: Reads and parse tpsnap.va variable file
- `get_vcmrinit_file() -> VcmrinitFile`: Reads and parse vcmrinit.va variable file

## OnProgressDelegate

`from underautomation.fanuc.common.files.on_progress_delegate import OnProgressDelegate`

Delegate to track File transfer progress. The value provided is in the range 0 to 100

## SectionParser1

`from underautomation.fanuc.common.files.section_parser_1 import SectionParser1`

Abstract generic section parser that creates and populates a section of type T.

- `SectionParser1()`: Initializes a new instance of the SectionParser class.
- `section: T`: The parsed section instance.
- Inherited from [SectionParser](underautomation.fanuc.common.files.md#sectionparser): `can_handle_section`, `parse_line`, `after_parse`, `section_start`, `end_of_file`

## SectionParser

`from underautomation.fanuc.common.files.section_parser import SectionParser`

Abstract base class for parsing sections of diagnostic files.

- `can_handle_section(line: str) -> bool`: Determines whether this parser can handle the given section header line.
- `parse_line(line: str) -> None`: Parses a single line from the section content.
- `after_parse() -> None`: Called after all lines have been parsed. Override to perform final processing.
- `section_start: typing.List[str] (read only)`: Gets the possible section header strings that indicate the start of this section.
- `end_of_file: bool`: Gets or sets a value indicating whether the end of the file or section has been reached.
