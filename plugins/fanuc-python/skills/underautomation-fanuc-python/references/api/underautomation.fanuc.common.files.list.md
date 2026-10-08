# underautomation.fanuc.common.files.list

## ErrallSectionItem

`from underautomation.fanuc.common.files.list.errall_section_item import ErrallSectionItem`

Represents a single error item from the ERRALL error log

- `ErrallSectionItem()`
- `id: int (read only)`: Error entry identifier
- `text: str (read only)`: Raw text of the error entry
- `error_code: str (read only)`: Parsed error code (e.g. "SRVO-001")
- `message: str (read only)`: Error message description
- `occurring_time: datetime (read only)`: Date and time when the error occurred
- `is_reset: bool (read only)`: Indicates whether this entry is a RESET marker

## ErrorList

`from underautomation.fanuc.common.files.list.error_list import ErrorList`

Represents the parsed content of the ERRALL.LS error log file

- `ErrorList()`
- `filter_active_alarms() -> typing.List[ErrallSectionItem]`: Return active alarms among the list of all error items
- `name: str (read only)`: File name (ERRALL.LS)
- `items: typing.List[ErrallSectionItem] (read only)`: List of all error items (active and history)

## ErrorListReader

`from underautomation.fanuc.common.files.list.error_list_reader import ErrorListReader`

Reader for the ERRALL.LS error log file

- `ErrorListReader()`: Creates a new instance of the error list reader
- `read_file(filePath: str, language: Languages) -> ErrorList`: Read and decode the file on disc
- Inherited from [FileReader](underautomation.fanuc.common.files.md#filereader): `file_name`
