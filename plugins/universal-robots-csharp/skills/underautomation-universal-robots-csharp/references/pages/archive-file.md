# Program and installation files

Open the .urp program and .installation files of a UR cobot on the PC, read and change their XML, and save them again.

Web page: https://underautomation.com/universal-robots/documentation/archive-file

A program (`.urp`) and an installation (`.installation`) of a Universal Robots cobot are compressed XML files. The SDK opens them on the PC, gives their XML, and writes them again. This page shows how, without a robot.

## How it works

`URProgram.Load` and `URInstallation.Load` read a file and decompress it. `XML` is the content of the file, as an `XElement`: read it, change it, add elements. `Save` writes the file again: to a `Stream`, or to a folder, with the name of the program as file name.

To get a file from the robot, or to send it back, use [SFTP](sftp-file-handling.md). The XML format is the format of PolyScope: open a file saved by PolyScope to see the elements of an instruction.

## Program files

```csharp
using System.Xml.Linq;
using UnderAutomation.UniversalRobots.Files;

class FileProgram
{
  static void Main(string[] args)
  {
    // Open a program file downloaded from the robot
    URProgram program = URProgram.Load(@"C:\temp\my_program.urp");

    // Content of the program, as XML
    XElement xml = program.XML;

    // For example, the installation used by the program
    xml.Attribute("installationRelativePath").Value = "default";

    // Save in a folder: the file name is the name of the program.
    // Then send the file to the robot with SFTP
    string path = program.Save(@"C:\temp\modified");
  }
}
```

## Installation files

```csharp
using System.Xml.Linq;
using UnderAutomation.UniversalRobots.Files;

class FileInstallation
{
  static void Main(string[] args)
  {
    URInstallation installation = URInstallation.Load(@"C:\temp\default.installation");

    XElement xml = installation.XML;

    // For example, show the speed slider on the Run tab
    xml.Attribute("showSpeedSliderOnRunTab").Value = "true";

    // Save in a folder: the file name is the name of the installation
    string path = installation.Save(@"C:\temp\modified");
  }
}
```

A program or an installation changed by the SDK is loaded by PolyScope like any other file. Keep a copy of the original, and check the result in PolyScope or URSim before you use it on a robot.

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**URArchive** ([reference](../api/UnderAutomation.UniversalRobots.Files.md#urarchive))

- `string FileName { get; }`: File name that should be used on a UR robot
- `static XElement Load(Stream fileStream)`: Load a UR archive from stream and decode it as XML
- `static XElement Load(string filePath)`: Load a UR archive from file path and decode it as XML
- `string Name { get; set; }`: Gets or sets the name of this archive, stored as an XML attribute.
- `void Save(Stream stream)`: Save encoded file to a stream
- `string Save(string directory)`: Save encoded file to a directory, overwrite it if it exists
- `XElement XML { get; }`: XML description of the object

**URProgram** ([reference](../api/UnderAutomation.UniversalRobots.Files.md#urprogram))

- `URProgram(XElement xml)`: Creates a URProgram from its XML definition.
- `const string EXTENSION = ".urp"`: File extension for UR program files.
- `static URProgram Load(Stream urpStream)`: Load a program from stream
- `static URProgram Load(string urpFile)`: Load a *.urp program from file path
- Inherited from [URArchive](../api/UnderAutomation.UniversalRobots.Files.md#urarchive): `Save`, `XML`, `Name`, `FileName`

**URInstallation** ([reference](../api/UnderAutomation.UniversalRobots.Files.md#urinstallation))

- `URInstallation(XElement xml)`: Creates a URInstallation from its XML definition.
- `const string EXTENSION = ".installation"`: File extension for UR installation files.
- `static URInstallation Load(Stream urpStream)`: Load an installation file from stream
- `static URInstallation Load(string urpFile)`: Load a *.installation file from path
- Inherited from [URArchive](../api/UnderAutomation.UniversalRobots.Files.md#urarchive): `Save`, `XML`, `Name`, `FileName`
