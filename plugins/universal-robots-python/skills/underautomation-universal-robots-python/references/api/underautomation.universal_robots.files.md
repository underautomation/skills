# underautomation.universal_robots.files

## URArchive

`from underautomation.universal_robots.files.ur_archive import URArchive`

Contains basic methods to encode and decode a UR archive

- `save(directory: str) -> str`: Save encoded file to a directory, overwrite it if it exists
- `xml: typing.Any (read only)`: XML description of the object
- `name: str`: Gets or sets the name of this archive, stored as an XML attribute.
- `file_name: str (read only)`: File name that should be used on a UR robot

## URInstallation

`from underautomation.universal_robots.files.ur_installation import URInstallation`

Functions to encode and decode a *.installation file

- `URInstallation(xml: typing.Any)`: Creates a URInstallation from its XML definition.
- `static load(urpFile: str) -> 'URInstallation'`: Load a *.installation file from path
- `static EXTENSION: str`: File extension for UR installation files.
- Inherited from [URArchive](underautomation.universal_robots.files.md#urarchive): `save`, `xml`, `name`, `file_name`

## URProgram

`from underautomation.universal_robots.files.ur_program import URProgram`

Functions to compile and decompile a *.urp program file

- `URProgram(xml: typing.Any)`: Creates a URProgram from its XML definition.
- `static load(urpFile: str) -> 'URProgram'`: Load a *.urp program from file path
- `static EXTENSION: str`: File extension for UR program files.
- Inherited from [URArchive](underautomation.universal_robots.files.md#urarchive): `save`, `xml`, `name`, `file_name`
