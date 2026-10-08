# Offline file parsing

Parse and decode Fanuc variable files (.va), error lists (.ls), I/O state, safety status, and current position files without a robot connection.

Web page: https://underautomation.com/fanuc/documentation/offline-file-parsing

The SDK includes offline file parsers for reading and editing Fanuc controller files without a network connection. Download files from the robot via FTP, then parse them locally.

The offline parsers are available in .NET. The Python package does not wrap them yet: in Python, read these files from the controller with the FTP client (`robot.ftp.known_variable_files`, `robot.ftp.get_safety_status()`...), see [Diagnostics & variables](ftp-diagnostics.md).

## Variable files (.va)

Parse any variable file (.va) into a hierarchical list of typed variables:



This works with all .va files: `numreg.va`, `posreg.va`, `strreg.va`, `sysvars.va`, `sysmotn.va`, etc.

## Error log (errall.ls)




## Workflow: FTP download + offline parse

A common pattern is to download files via FTP and parse them locally:



## Complete example



## API reference

**GenericVariableFile** ([reference](../api/underautomation.fanuc.common.files.variables.md#genericvariablefile))

- `GenericVariableFile()`
- `get_field(name: str) -> GenericVariable`: Gets a variable by name (case-insensitive)
- `generate_va(pathToVa: str) -> None`: Generates a .va file and writes it to the specified path
- `generated_va() -> str`: Generates the content of a .va variable file as a string.
- `variables: typing.List[GenericVariable] (read only)`: Variables declared in this file
- `name: str (read only)`: File name
- `parent: IGenericVariableType`: Parent container

**FanucFileReaders** ([reference](../api/underautomation.fanuc.common.files.md#fanucfilereaders))

- `static read_file(fileName: str, language: Languages) -> IFanucContent`: Read any file by path on disc, recognize it by name and decode it
- `static readers: typing.List[IFileReader1] (read only)`: Get the collection of all parsers
- `static VariableReader: VariableReader`: Helper to read variable files *.va
- `static ErrorListReader: ErrorListReader`: Helper to read error files like errall.ls
- `static SummaryDiagnosticReader: SummaryDiagnosisReader`: Helper to read summary diagnosis file summary.dg
- `static CurrentPositionReader: DiagnosisReader2[CurrentPosition, CurrentPositionReader]`: Decode current position file curpos.dg
- `static IOStateReader: DiagnosisReader2[IOState, IOStateParser]`: Decode IO Status file iostate.dg
- `static SafetyStatusReader: DiagnosisReader2[SafetyStatus, SafetyStatusParser]`: Decode IO Status file iostate.dg
- `static ProgramStates: DiagnosisReader2[ProgramStates, ProgramStatesParser]`: Decode task and program states prgstate.dg
