# UnderAutomation.UniversalRobots.Files

## URArchive

`abstract class URArchive`

Contains basic methods to encode and decode a UR archive

- `string FileName { get; }`: File name that should be used on a UR robot
- `static XElement Load(Stream fileStream)`: Load a UR archive from stream and decode it as XML
- `static XElement Load(string filePath)`: Load a UR archive from file path and decode it as XML
- `string Name { get; set; }`: Gets or sets the name of this archive, stored as an XML attribute.
- `void Save(Stream stream)`: Save encoded file to a stream
- `string Save(string directory)`: Save encoded file to a directory, overwrite it if it exists
- `XElement XML { get; }`: XML description of the object

## URInstallation

`class URInstallation : URArchive`

Functions to encode and decode a *.installation file

- `URInstallation(XElement xml)`: Creates a URInstallation from its XML definition.
- `const string EXTENSION = ".installation"`: File extension for UR installation files.
- `static URInstallation Load(Stream urpStream)`: Load an installation file from stream
- `static URInstallation Load(string urpFile)`: Load a *.installation file from path
- Inherited from [URArchive](UnderAutomation.UniversalRobots.Files.md#urarchive): `Save`, `XML`, `Name`, `FileName`

## URProgram

`class URProgram : URArchive`

Functions to compile and decompile a *.urp program file

- `URProgram(XElement xml)`: Creates a URProgram from its XML definition.
- `const string EXTENSION = ".urp"`: File extension for UR program files.
- `static URProgram Load(Stream urpStream)`: Load a program from stream
- `static URProgram Load(string urpFile)`: Load a *.urp program from file path
- Inherited from [URArchive](UnderAutomation.UniversalRobots.Files.md#urarchive): `Save`, `XML`, `Name`, `FileName`
