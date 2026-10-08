# HTTP: read files from the web server

List the files of a Yaskawa controller with their description and read their text through its web server, without account and in any mode.

Web page: https://underautomation.com/yaskawa/documentation/http

This page shows how to list the files of a Yaskawa Motoman controller and read their content through its web server, with the HTTP client of the SDK. It covers the YRC1000 and YRC1000micro controllers, and gives read only access: jobs, data files, parameters, logs.

## What the HTTP client does

The controller has a web server on TCP port 80. The SDK reads the file lists and the files of this server, and gives you the names, the descriptions and the text of the files. It is the simplest way to read a file: no account, no remote mode, any mode of the controller.

| Need                                    | HTTP | Other protocol                                              |
| --------------------------------------- | ---- | ----------------------------------------------------------- |
| List the files of one type              | Yes  | FTP, High Speed Ethernet Server                             |
| Name and description of the data files  | Yes  | No                                                          |
| Read a text file (job, data, parameter) | Yes  | FTP, High Speed Ethernet Server                             |
| Upload or delete a file                 | No   | [FTP](ftp-transfer.md), [High Speed Ethernet Server](hses-files.md) |
| Binary files, CMOS backup               | No   | FTP, High Speed Ethernet Server                             |

## Connect

### Prerequisites

- The PC reaches the controller on TCP port 80.
- Nothing else: HTTP works in teach and in play mode, without the remote mode.

### Enable HTTP

Set `Http.Enable` to `true` in `ConnectParameters`. `Connect` checks the address but does not send a request: the first method call is the first exchange.

| Parameter                  | Default | Meaning                               |
| -------------------------- | ------- | ------------------------------------- |
| `Http.Enable`              | `false` | Open the HTTP client                  |
| `Http.Port`                | `80`    | TCP port of the web server            |
| `Http.TimeoutMilliseconds` | `5000`  | Time to wait for the answer of a request |

## List the files

`GetFileList(fileExtension)` lists the files of one type. Each `FileDescription` has the `Name` of the file and, for the data and parameter files, the `Description` given by the controller.

```csharp
using UnderAutomation.Yaskawa;
using UnderAutomation.Yaskawa.Common;
using UnderAutomation.Yaskawa.Http;

public class HttpFileList
{
    static void Main()
    {
        var parameters = new ConnectParameters("192.168.0.1");
        parameters.Http.Enable = true;
        var robot = new YaskawaRobot();
        robot.Connect(parameters);

        // Jobs: the name only
        FileDescription[] jobs = robot.Http.GetFileList(FileExtension.JOB);

        // Data files: the name and the description given by the controller
        foreach (FileDescription file in robot.Http.GetFileList(FileExtension.DAT))
            Console.WriteLine($"{file.Name}: {file.Description}"); // VAR.DAT: VARIABLE DATA

        robot.Disconnect();
    }
}
```

| `FileExtension` | Files                                                       |
| --------------- | ----------------------------------------------------------- |
| `JOB`           | Jobs (`.JBI`)                                               |
| `DAT`           | Data files: variables, alarm history, I/O names... (`.DAT`) |
| `CND`           | Condition files (`.CND`)                                    |
| `PRM`           | Parameter files (`.PRM`), for example `ALL.PRM`             |
| `SYS`           | System files (`.SYS`)                                       |
| `LST`           | List files (`.LST`)                                         |
| `CSV`, `LOG`, `TXT` | Other text files                                        |

On a YRC1000micro, `GetFileList(FileExtension.DAT)` returns `VAR.DAT - VARIABLE DATA`, `ALMHIST.DAT - ALARM HISTORY DATA`, `IONAME.DAT - IO NAME DATA` and more.

## Read a file

`GetFile(name)` returns the text of a file. The SDK finds the folder of the file from its extension: `TEST.JBI` is a job, `VAR.DAT` a data file.

```csharp
using UnderAutomation.Yaskawa;

public class HttpFileGet
{
    static void Main()
    {
        var parameters = new ConnectParameters("192.168.0.1");
        parameters.Http.Enable = true;
        var robot = new YaskawaRobot();
        robot.Connect(parameters);

        // Text of a job: the folder is deduced from the extension
        string job = robot.Http.GetFile("TEST.JBI");

        // Variables, alarm history, parameters...
        string variables = robot.Http.GetFile("VAR.DAT");
        string alarmHistory = robot.Http.GetFile("ALMHIST.DAT");

        File.WriteAllText("TEST.JBI", job);

        robot.Disconnect();
    }
}
```

The text is the same as the file downloaded with FTP or with the High Speed Ethernet Server. A large file takes time: `ALL.PRM` (1.4 MB) takes about 13 s on a YRC1000micro, the same as with FTP. Increase `TimeoutMilliseconds` for large files.

## Standalone client

`HttpClient` of the namespace `UnderAutomation.Yaskawa.Http` opens an HTTP client without `YaskawaRobot`. In a .NET project with implicit usings, `System.Net.Http.HttpClient` has the same name: write the full name, or add a `using` alias.

```csharp
using UnderAutomation.Yaskawa.Common;
using UnderAutomation.Yaskawa.Http;

public class HttpStandalone
{
    static void Main()
    {
        // An HTTP client without YaskawaRobot
        // Full name: System.Net.Http also has an HttpClient class
        var client = new UnderAutomation.Yaskawa.Http.HttpClient();
        client.Connect("192.168.0.1", new HttpConnectParameters
        {
            Port = 80,                   // default
            TimeoutMilliseconds = 5000,  // default
        });

        foreach (FileDescription file in client.GetFileList(FileExtension.PRM))
            Console.WriteLine(file);

        client.Close();
    }
}
```

## Reference

**Methods of HttpClientBase** ([reference](../api/UnderAutomation.Yaskawa.Http.Internal.md#httpclientbase-robothttp))

- `void Close()`: Marks the client as disconnected.
- `string GetFile(string fileName)`: Gets the content of a file from the robot controller. The file type is deduced from the file name extension (e.g. "PICK_JOB.JBI" queries /FGET_REQUEST/ROBOT/JOB/PICK_JOB.JBI).
- `FileDescription[] GetFileList(FileExtension fileExtension)`: Gets the list of files of the specified type available on the robot controller.

**FileDescription** ([reference](../api/UnderAutomation.Yaskawa.Http.md#filedescription))

- `FileDescription()`
- `string Description { get; }`: Description of the file, if available.
- `string Name { get; }`: File name including extension.

**FileExtension** ([reference](../api/UnderAutomation.Yaskawa.Common.md#fileextension))

- CND: Condition files (.CND)
- CSV: CSV files (.CSV)
- DAT: Data files (.DAT)
- JOB: Job files (.JBI)
- LOG: Log files (.LOG)
- LST: List files (.LST)
- PRM: Parameter files (.PRM)
- SYS: System files (.SYS)
- TXT: Text files (.TXT)

**HttpConnectParameters** ([reference](../api/UnderAutomation.Yaskawa.Http.md#httpconnectparameters))

- `HttpConnectParameters()`: Initializes a new instance of the HTTP connection parameters.
- `const int DEFAULT_PORT = 80`: Default HTTP port (80).
- `const int DEFAULT_TIMEOUT_MILLISECONDS = 5000`: Default timeout in milliseconds for HTTP requests (5000ms).
- `int Port { get; set; }`: Gets or sets the HTTP port number. Default: 80.
- `int TimeoutMilliseconds { get; set; }`: Gets or sets the maximum time in milliseconds to wait for a response. Default: 5000ms.

## What to read next

- [FTP](ftp.md): upload, download and delete files.
- [Transfer files and backups](how-to-transfer-files.md): which protocol to choose for each file task.
