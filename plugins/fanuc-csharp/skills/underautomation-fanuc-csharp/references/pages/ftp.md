# FTP overview

FTP provides access to internal controller files including variables, programs, diagnostics, safety status, and current position.

Web page: https://underautomation.com/fanuc/documentation/ftp

FTP (File Transfer Protocol) provides direct access to the Fanuc controller's internal file system. The SDK uses FTP to transfer files (programs, backups) and to read and decode diagnostic data, variables, registers, and safety status.

## Key features

- **File management**: Upload, download, delete, rename files and directories
- **Variable reading**: Read all system variables in bulk from .va files
- **Registers**: Read numeric, position, and string registers
- **Diagnostics**: Safety status, I/O state, current position, error history
- **Installed features**: Detect available options on the controller
- **Asynchronous methods**: every blocking method has an `...Async` version with a `CancellationToken`

## Quick example

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common.Files.Diagnosis;

  public class Ftp
  {
    static void Main()
    {
      // Create a new Fanuc robot instance
      FanucRobot robot = new FanucRobot();

      // Set connection parameters
      ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");
      parameters.Ftp.Enable = true;
      parameters.Ftp.FtpUser = "user";
      parameters.Ftp.FtpPassword = "ftp password";

      // Connect to the robot
      robot.Connect(parameters);

      IOState ioState = robot.Ftp.GetIOState();

      // Read a variable
      var variableFiles = robot.Ftp.GetAllVariables();
      foreach (var variableFile in variableFiles)
        foreach (var variable in variableFile.Variables)
          Console.WriteLine($"{variable.Name} = {variable.Value}");

      // Read system variable $RMT_MASTER
      int remoteMode = robot.Ftp.KnownVariableFiles.GetSystemFile().RmtMaster;

      // Read safety status
      SafetyStatus safetyStatus = robot.Ftp.GetSafetyStatus();
      Console.WriteLine($"Emergency Stop: {safetyStatus.ExternalEStop}");
      Console.WriteLine($"Teach Pendant Enabled: {safetyStatus.TPEnable}");

      // Get current position for each arm (Joints, World position of each tool, user frame positions)
      CurrentPosition currentPosition = robot.Ftp.GetCurrentPosition();

      // Upload a TP program to the controller
      robot.Ftp.DirectFileHandling.UploadFileToController(@"C:\Programs\MyPrg.tp", "md:/MyPrg.tp");

      // Download a file from the robot
      robot.Ftp.DirectFileHandling.DownloadFileFromController("md:/Backup.va", @"C:\Backup\Backup.va");

      // Delete a file on the robot
      robot.Ftp.DirectFileHandling.DeleteFile("md:/OldProgram.tp");
    }

  }
```

## Connection

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Ftp;

public class FtpConnection
{
    static void Main()
    {
        // Via FanucRobot
        var robot = new FanucRobot();
        var parameters = new ConnectionParameters("192.168.0.1");
        parameters.Ftp.Enable = true;
        parameters.Ftp.FtpUser = "";          // usually empty
        parameters.Ftp.FtpPassword = "";      // usually empty
        parameters.Ftp.FtpTimeoutMs = 30000;  // optional, default is 30 seconds
        robot.Connect(parameters);

        // Or standalone
        var ftp = new FtpClient();
        ftp.Connect("192.168.0.1", "", "");
    }
}
```

The `FtpTimeoutMs` property controls the connection, read, and data transfer timeouts. The default is 30,000 ms (30 seconds). Lower it for faster failure detection on unreachable controllers, or raise it for slow networks.

### User and rights

The rights of the FTP session depend on the user and on the password settings of the controller. Without a user (`FtpUser = ""`), the controller logs in at the OPERATOR level: it can refuse some operations, for example the upload of a program, with the reply "Operation password protected". Connect with a user of a higher level (for example INSTALL), defined in the password settings of the controller. The refusal is an `FtpException`, see [File management](ftp-file-management.md).

### Standalone client

`FtpClient` connects to the FTP server only, without `FanucRobot`: `Connect(ip, user, password, port, timeoutMs)` or `ConnectAsync(...)`.

## Synchronous and asynchronous

Every blocking FTP method exists twice: a synchronous version, and an asynchronous one with the same name followed by `Async` and an optional `CancellationToken`. The file reading methods (`GetSummaryDiagnosticAsync`, `KnownVariableFiles.GetNumregFileAsync`...) are also available on the web server client, `robot.Cgtp.Http`.

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Ftp;

public class FtpAsync
{
    static async Task Main()
    {
        FanucRobot robot = new FanucRobot();
        var parameters = new ConnectionParameters("192.168.0.1");
        parameters.Ftp.Enable = true;
        parameters.Ftp.FtpUser = "";
        parameters.Ftp.FtpPassword = "";
        robot.Connect(parameters);

        // Every blocking FTP method has an asynchronous twin, with a cancellation token
        FtpListItem[] files = await robot.Ftp.DirectFileHandling.GetListingAsync("md:");
        var diagnosis = await robot.Ftp.GetSummaryDiagnosticAsync();

        using (var cts = new CancellationTokenSource(TimeSpan.FromSeconds(10)))
        {
            var numreg = await robot.Ftp.KnownVariableFiles.GetNumregFileAsync(cts.Token);
            Console.WriteLine($"R[1] = {numreg.Numreg[0]}");
        }

        // The standalone FTP client also connects asynchronously
        var ftp = new FtpClient();
        await ftp.ConnectAsync("192.168.0.1", "", "");

        Console.WriteLine($"{files.Length} files on md:");
        ftp.Disconnect();
        robot.Disconnect();
    }
}
```

The asynchronous methods are not available on .NET Framework 3.5 and 4.0, which have no `async` / `await`. The synchronous and asynchronous methods of one client can be called from several threads: they run one at a time on the FTP connection.

## Limitations

- **Read-only for most data**: Variables and diagnostics are read-only via FTP. Use Telnet, SNPX, or CGTP to write values
- **Slower than SNPX**: FTP transfers entire files rather than individual values
- **No real-time data**: Data represents a snapshot at the time of the FTP request

## Next steps

- [File management](ftp-file-management.md) : Upload, download, delete files
- [Diagnostics & variables](ftp-diagnostics.md) : Safety status, registers, variables

## API reference

**FtpClient** ([reference](../api/UnderAutomation.Fanuc.Ftp.md#ftpclient))

- `FtpClient()`: Instanciate a new FTP client connection
- `void Connect(string ip, string user, string password, int port = 21, int timeoutMs = 30000)`: Connect to a robot
- Inherited from [FtpClientBase](../api/UnderAutomation.Fanuc.Ftp.Internal.md#ftpclientbase-robotftp): `Disconnect`, `EnumerateVariableFiles`, `EnumerateVariableFileNames`, `IP`, `Language`, `Connected`, `DirectFileHandling`
- Inherited from [FileClientBase](../api/UnderAutomation.Fanuc.Common.Files.md#fileclientbase-robotftp): `GetSummaryDiagnostic`, `GetAllErrorsList`, `GetCurrentPosition`, `GetIOState`, `GetSafetyStatus`, `GetProgramStates`, `GetVariablesFromFile`, `GetAllVariables`, `KnownVariableFiles`

**FtpClientBase** ([reference](../api/UnderAutomation.Fanuc.Ftp.Internal.md#ftpclientbase-robotftp))

- `bool Connected { get; }`: Indicates that FTP connection is active
- `FtpDirectFileHandling DirectFileHandling { get; }`: Contains methods to manipulate files and folders on the controller (upload, download, delete, ...)
- `void Disconnect()`: Disconnects from FTP server
- `string[] EnumerateVariableFileNames()`: Get the list of all variable file names available on the controller
- `FtpListItem[] EnumerateVariableFiles()`: Get a list of all variable files on controller
- `string IP { get; }`: Connect robot IP address or host name
- `Languages Language { get; set; }`: Controller language (default is English)
- Inherited from [FileClientBase](../api/UnderAutomation.Fanuc.Common.Files.md#fileclientbase-robotftp): `GetSummaryDiagnostic`, `GetAllErrorsList`, `GetCurrentPosition`, `GetIOState`, `GetSafetyStatus`, `GetProgramStates`, `GetVariablesFromFile`, `GetAllVariables`, `KnownVariableFiles`
