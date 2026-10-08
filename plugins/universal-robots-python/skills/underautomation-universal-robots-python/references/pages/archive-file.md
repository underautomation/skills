# Program and installation files

Open the .urp program and .installation files of a UR cobot on the PC, read and change their XML, and save them again.

Web page: https://underautomation.com/universal-robots/documentation/archive-file

A program (`.urp`) and an installation (`.installation`) of a Universal Robots cobot are compressed XML files. The SDK opens them on the PC, gives their XML, and writes them again. This page shows how, without a robot.

## How it works

`URProgram.Load` and `URInstallation.Load` read a file and decompress it. `XML` is the content of the file, as an `XElement`: read it, change it, add elements. `Save` writes the file again: to a `Stream`, or to a folder, with the name of the program as file name.

To get a file from the robot, or to send it back, use [SFTP](sftp-file-handling.md). The XML format is the format of PolyScope: open a file saved by PolyScope to see the elements of an instruction.

## Program files

```python
from underautomation.universal_robots.files.ur_program import URProgram

# Open a program file downloaded from the robot
program = URProgram.load("C:\\temp\\my_program.urp")

# Content of the program, as a .NET XElement
xml = program.xml

# For example, the installation used by the program
xml.Attribute("installationRelativePath").Value = "default"

# Save in a folder: the file name is the name of the program.
# Then send the file to the robot with SFTP
path = program.save("C:\\temp\\modified")
```

## Installation files

```python
from underautomation.universal_robots.files.ur_installation import URInstallation

installation = URInstallation.load("C:\\temp\\default.installation")

# Content of the installation, as a .NET XElement
xml = installation.xml

# For example, show the speed slider on the Run tab
xml.Attribute("showSpeedSliderOnRunTab").Value = "true"

# Save in a folder: the file name is the name of the installation
path = installation.save("C:\\temp\\modified")
```

A program or an installation changed by the SDK is loaded by PolyScope like any other file. Keep a copy of the original, and check the result in PolyScope or URSim before you use it on a robot.

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**URArchive** ([reference](../api/underautomation.universal_robots.files.md#urarchive))

- `save(directory: str) -> str`: Save encoded file to a directory, overwrite it if it exists
- `xml: typing.Any (read only)`: XML description of the object
- `name: str`: Gets or sets the name of this archive, stored as an XML attribute.
- `file_name: str (read only)`: File name that should be used on a UR robot

**URProgram** ([reference](../api/underautomation.universal_robots.files.md#urprogram))

- `URProgram(xml: typing.Any)`: Creates a URProgram from its XML definition.
- `static load(urpFile: str) -> 'URProgram'`: Load a *.urp program from file path
- `static EXTENSION: str`: File extension for UR program files.
- Inherited from [URArchive](../api/underautomation.universal_robots.files.md#urarchive): `save`, `xml`, `name`, `file_name`

**URInstallation** ([reference](../api/underautomation.universal_robots.files.md#urinstallation))

- `URInstallation(xml: typing.Any)`: Creates a URInstallation from its XML definition.
- `static load(urpFile: str) -> 'URInstallation'`: Load a *.installation file from path
- `static EXTENSION: str`: File extension for UR installation files.
- Inherited from [URArchive](../api/underautomation.universal_robots.files.md#urarchive): `save`, `xml`, `name`, `file_name`
