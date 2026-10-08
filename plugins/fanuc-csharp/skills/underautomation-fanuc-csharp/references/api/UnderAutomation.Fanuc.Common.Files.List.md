# UnderAutomation.Fanuc.Common.Files.List

## ErrallSectionItem

`class ErrallSectionItem`

Represents a single error item from the ERRALL error log

- `ErrallSectionItem()`
- `string ErrorCode { get; }`: Parsed error code (e.g. "SRVO-001")
- `int Id { get; }`: Error entry identifier
- `bool IsReset { get; }`: Indicates whether this entry is a RESET marker
- `string Message { get; }`: Error message description
- `DateTime OccurringTime { get; }`: Date and time when the error occurred
- `string Text { get; }`: Raw text of the error entry

## ErrorList

`class ErrorList : IFanucContent`

Represents the parsed content of the ERRALL.LS error log file

- `ErrorList()`
- `ErrallSectionItem[] FilterActiveAlarms()`: Return active alarms among the list of all error items
- `ErrallSectionItem[] Items { get; }`: List of all error items (active and history)
- `string Name { get; }`: File name (ERRALL.LS)

## ErrorListReader

`class ErrorListReader : FileReader<ErrorList>, IFileReader<ErrorList>, IFileReader`

Reader for the ERRALL.LS error log file

- `ErrorListReader()`: Creates a new instance of the error list reader
- `ErrorList ReadFile(Stream fileStream, Languages language, string fileName = null)`: Read and decode the file stream
- Inherited from [FileReader](UnderAutomation.Fanuc.Common.Files.md#filereader): `FileName`
