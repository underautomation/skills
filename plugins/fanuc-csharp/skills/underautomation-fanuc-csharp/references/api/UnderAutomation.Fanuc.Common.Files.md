# UnderAutomation.Fanuc.Common.Files

## FanucFileReaders

`static class FanucFileReaders`

Contains static functions to decode Fanuc files (variables, diagnosis, listing, ...)

- `static readonly DiagnosisReader<CurrentPosition, CurrentPositionReader> CurrentPositionReader`: Decode current position file curpos.dg
- `static readonly ErrorListReader ErrorListReader`: Helper to read error files like errall.ls
- `static readonly DiagnosisReader<IOState, IOStateParser> IOStateReader`: Decode IO Status file iostate.dg
- `static readonly DiagnosisReader<ProgramStates, ProgramStatesParser> ProgramStates`: Decode task and program states prgstate.dg
- `static IFanucContent ReadFile(Stream fileStream, string fileName, Languages language)`: Read any file by path on disc, recognize it by name and decode it
- `static IFanucContent ReadFile(string fileName, Languages language)`: Read any file by path on disc, recognize it by name and decode it
- `static IFileReader<IFanucContent>[] Readers { get; }`: Get the collection of all parsers
- `static readonly DiagnosisReader<SafetyStatus, SafetyStatusParser> SafetyStatusReader`: Decode IO Status file iostate.dg
- `static readonly SummaryDiagnosisReader SummaryDiagnosticReader`: Helper to read summary diagnosis file summary.dg
- `static readonly VariableReader VariableReader`: Helper to read variable files *.va

## FileClientBase (robot.Ftp)

`abstract class FileClientBase`

Base class for Fanuc file client. It provides methods to read and parse known files such as summary diagnostic, error list, current position, ...

- `abstract string[] EnumerateVariableFileNames()`: Get the list of all variable file names available on the controller
- `ErrorList GetAllErrorsList()`: Get a list of all errors logged by the controller
- `VariableFileList GetAllVariables(OnProgressDelegate progress = null)`: Get the list of all variables on the controller. All variables files are read and decoded
- `CurrentPosition GetCurrentPosition()`: Get current robot position of each robot handled by this controller
- `IOState GetIOState()`: Get controller IO State
- `ProgramStates GetProgramStates()`: Get controller program states
- `SafetyStatus GetSafetyStatus()`: Get controller safety status
- `SummaryDiagnosis GetSummaryDiagnostic()`: Get controller status (position, safety, ios, ...)
- `GenericVariableFile GetVariablesFromFile(string variableFileName)`: Get and parse a variable file from its name
- `abstract string IP { get; }`: IP address of the controller
- `KnownVariableFiles KnownVariableFiles { get; }`: A list of method to read specific files

## FileReader<T>

`abstract class FileReader<T> : FileReader, IFileReader<T>, IFileReader where T : IFanucContent`

File reader for specific files

- `abstract T ReadFile(Stream fileStream, Languages language, string fileName = null)`: Read and decode the file stream
- `T ReadFile(string filePath, Languages language)`: Read and decode the file on disc
- Inherited from [FileReader](UnderAutomation.Fanuc.Common.Files.md#filereader): `FileName`

## FileReader

`abstract class FileReader : IFileReader`

Read and decode fanuc files

- `string FileName { get; }`: File name

## IFanucContent

`interface IFanucContent`

Interface of a file that comes from a Fanuc controller

- `string Name { get; }`: File name

## IFileReader<T>

`interface IFileReader<out T> : IFileReader where T : IFanucContent`

Interface for Fanuc file readers

- `T ReadFile(Stream fileStream, Languages language, string fileName)`: Reads file stream and decodes it
- `T ReadFile(string filePath, Languages language)`: Reads file by path and decodes it
- Inherited from [IFileReader](UnderAutomation.Fanuc.Common.Files.md#ifilereader): `FileName`

## IFileReader

`interface IFileReader`

Interface for Fanuc file readers

- `string FileName { get; }`: File name

## KnownVariableFiles (robot.Ftp.KnownVariableFiles)

`class KnownVariableFiles`

Wrapper class of methods to download and decode variable files

- `AavmmainFile GetAavmmainFile()`: Reads and parse aavmmain.va variable file
- `BicsetupFile GetBicsetupFile()`: Reads and parse bicsetup.va variable file
- `CbparamFile GetCbparamFile()`: Reads and parse cbparam.va variable file
- `CellioFile GetCellioFile()`: Reads and parse cellio.va variable file
- `ComsetFile GetComsetFile()`: Reads and parse comset.va variable file
- `DiocfgsvFile GetDiocfgsvFile()`: Reads and parse diocfgsv.va variable file
- `GemdataFile GetGemdataFile()`: Reads and parse gemdata.va variable file
- `HtcolrecFile GetHtcolrecFile()`: Reads and parse htcolrec.va variable file
- `HttpkclFile GetHttpkclFile()`: Reads and parse httpkcl.va variable file
- `IrcCounterFile GetIrcCounterFile()`: Reads and parse irc_counter.va variable file
- `IrcMsgFile GetIrcMsgFile()`: Reads and parse irc_msg.va variable file
- `IrcStatusFile GetIrcStatusFile()`: Reads and parse irc_status.va variable file
- `IrcStlabelFile GetIrcStlabelFile()`: Reads and parse irc_stlabel.va variable file
- `KlactionFile GetKlactionFile()`: Reads and parse klaction.va variable file
- `MixlogicFile GetMixlogicFile()`: Reads and parse mixlogic.va variable file
- `MtparamFile GetMtparamFile()`: Reads and parse mtparam.va variable file
- `NumregFile GetNumregFile()`: Reads and parse numreg.va variable file
- `PalregFile GetPalregFile()`: Reads and parse palreg.va variable file
- `PosregFile GetPosregFile()`: Reads and parse posreg.va variable file
- `StrregFile GetStrregFile()`: Reads and parse strreg.va variable file
- `SwiupdtFile GetSwiupdtFile()`: Reads and parse swiupdt.va variable file
- `SycldintFile GetSycldintFile()`: Reads and parse sycldint.va variable file
- `SymotnFile GetSymotnFile()`: Reads and parse symotn.va variable file
- `SynosaveFile GetSynosaveFile()`: Reads and parse synosave.va variable file
- `SysframeFile GetSysframeFile()`: Reads and parse sysframe.va variable file
- `SysfsacFile GetSysfsacFile()`: Reads and parse sysfsac.va variable file
- `SyshostFile GetSyshostFile()`: Reads and parse syshost.va variable file
- `SysmacroFile GetSysmacroFile()`: Reads and parse sysmacro.va variable file
- `SysmastFile GetSysmastFile()`: Reads and parse sysmast.va variable file
- `SyspassFile GetSyspassFile()`: Reads and parse syspass.va variable file
- `SysservoFile GetSysservoFile()`: Reads and parse sysservo.va variable file
- `SystemFile GetSystemFile()`: Reads and parse system.va variable file
- `SysuifFile GetSysuifFile()`: Reads and parse sysuif.va variable file
- `TpsnapFile GetTpsnapFile()`: Reads and parse tpsnap.va variable file
- `VcmrinitFile GetVcmrinitFile()`: Reads and parse vcmrinit.va variable file

## OnProgressDelegate

`delegate void OnProgressDelegate(double progress)`

Delegate to track File transfer progress. The value provided is in the range 0 to 100

- `OnProgressDelegate(object @object, IntPtr method)`
- `IAsyncResult BeginInvoke(double progress, AsyncCallback callback, object @object)`
- `void EndInvoke(IAsyncResult result)`
- `void Invoke(double progress)`

## SectionParser<T>

`abstract class SectionParser<T> : SectionParser where T : new()`

Abstract generic section parser that creates and populates a section of type T.

- `SectionParser()`: Initializes a new instance of the Files.SectionParser%601 class.
- `readonly T Section`: The parsed section instance.
- Inherited from [SectionParser](UnderAutomation.Fanuc.Common.Files.md#sectionparser): `CanHandleSection`, `ParseLine`, `AfterParse`, `SectionStart`, `EndOfFile`

## SectionParser

`abstract class SectionParser`

Abstract base class for parsing sections of diagnostic files.

- `void AfterParse()`: Called after all lines have been parsed. Override to perform final processing.
- `bool CanHandleSection(string line)`: Determines whether this parser can handle the given section header line.
- `bool EndOfFile { get; set; }`: Gets or sets a value indicating whether the end of the file or section has been reached.
- `abstract void ParseLine(string line)`: Parses a single line from the section content.
- `string[] SectionStart { get; }`: Gets the possible section header strings that indicate the start of this section.
