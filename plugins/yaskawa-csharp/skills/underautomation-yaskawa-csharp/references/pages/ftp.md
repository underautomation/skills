# FTP: connection and file management

Connect to the FTP server of a Yaskawa controller, choose the account, list the folders and files, test and delete files, and handle the FTP errors.

Web page: https://underautomation.com/yaskawa/documentation/ftp

This page explains how to connect to the FTP server of a Yaskawa Motoman controller with the SDK, which account to use, and how to list, test and delete files. It covers the YRC1000 and YRC1000micro controllers. File transfers are on the next page, [FTP file transfers](ftp-transfer.md).

## What the FTP client does

The controller has an FTP server on TCP port 21. The SDK connects to it, logs in, and gives you methods to list, download, upload and delete the files of the controller. Every FTP method has an async version in .NET (`GetListingAsync`, `DownloadFileAsync`...).

FTP is the fastest way to transfer large files: `ALL.PRM` (1.4 MB) is downloaded in about 13 s on a YRC1000micro, against about 45 s with the High Speed Ethernet Server.

## Prerequisites

- The PC reaches the controller on TCP port 21. A firewall between them must let the FTP connections through.
- The FTP server function is enabled on the controller. Depending on the controller and its settings, it can also need the command remote: see [Prepare the controller](connect.md#prepare_the_controller). On the YRC1000micro used to test this page, FTP works in teach mode, without the command remote.

## Accounts

The account gives the rights. "Download" means from the controller to the PC, "upload" from the PC to the controller.

| User name               | Password                       | Rights                                                                                       |
| ----------------------- | ------------------------------ | -------------------------------------------------------------------------------------------- |
| `anonymous` (default)   | Any                            | Download of jobs, condition files and general data. No upload, no deletion                   |
| `ftp`                   | Any                            | Download and upload of jobs, condition files and general data. Download of system data and backups |
| `rcmaster`              | Password of the management mode | Same as `ftp`, plus the download of the parameters                                          |

The rights depend on the controller and on its software version: on the YRC1000micro used to test this page, `anonymous` also downloads the parameter files. `ftp` and `anonymous` work in the standard security mode only. When the password protection option is enabled on the controller, only the user and the password defined in this option are accepted.

## Connect

### Enable FTP

Set `Ftp.Enable` to `true` in `ConnectParameters`, and choose the account. Unlike the other protocols, `Connect` opens the FTP session and logs in at once: a wrong address or a wrong password fails in `Connect`.

```csharp
using UnderAutomation.Yaskawa;

public class FtpConnect
{
    static void Main()
    {
        var parameters = new ConnectParameters("192.168.0.1");
        parameters.Ftp.Enable = true;

        // "anonymous" (default): download only. "ftp": download and upload.
        // "rcmaster" with the password of the management mode: every right.
        parameters.Ftp.FtpUser = "ftp";
        parameters.Ftp.FtpPassword = null;

        parameters.Ftp.Port = 21;                    // default
        parameters.Ftp.TimeoutMilliseconds = 30000;  // default

        var robot = new YaskawaRobot();
        robot.Connect(parameters); // opens the FTP session and logs in

        Console.WriteLine($"Logged as {robot.Ftp.User}");

        robot.Disconnect();
    }
}
```

| Parameter                 | Default       | Meaning                                         |
| ------------------------- | ------------- | ----------------------------------------------- |
| `Ftp.Enable`              | `false`       | Open the FTP client                             |
| `Ftp.FtpUser`             | `"anonymous"` | User name                                       |
| `Ftp.FtpPassword`         | `null`        | Password                                        |
| `Ftp.Port`                | `21`          | TCP port of the FTP server                      |
| `Ftp.TimeoutMilliseconds` | `30000`       | Time to wait for a connection, a reply or data  |

### Standalone client

`FtpClient` opens an FTP client without `YaskawaRobot`. `Connect` takes the address, the user, the password, the port and the timeout.

```csharp
using UnderAutomation.Yaskawa.Ftp;

public class FtpStandalone
{
    static void Main()
    {
        // An FTP client without YaskawaRobot
        var client = new FtpClient();
        client.Connect("192.168.0.1", "ftp");

        foreach (FtpListItem item in client.GetListing("/"))
            Console.WriteLine(item.FullName); // /JOB, /DAT, /CND, /SYS, /PRM...

        client.Close();
    }
}
```

## List and test the files

```csharp
using UnderAutomation.Yaskawa;
using UnderAutomation.Yaskawa.Common;
using UnderAutomation.Yaskawa.Ftp;

public class FtpListing
{
    static void Main()
    {
        var parameters = new ConnectParameters("192.168.0.1");
        parameters.Ftp.Enable = true;
        parameters.Ftp.FtpUser = "ftp";
        var robot = new YaskawaRobot();
        robot.Connect(parameters);

        // Folders of the controller: /JOB, /DAT, /CND, /SYS, /PRM, /LST, /CSV, /LOG, /TXT
        foreach (FtpListItem item in robot.Ftp.GetListing("/JOB"))
            Console.WriteLine($"{item.Name} {item.Modified:yyyy-MM-dd HH:mm} {item.Type}");

        // File names by type, or by pattern
        string[] jobs = robot.Ftp.GetFileList(FileExtension.JOB);
        string[] parameterFiles = robot.Ftp.GetFileListByPattern("*.PRM");

        // Test a file or a folder
        bool exists = robot.Ftp.FileExists("/JOB/TEST.JBI");
        bool folder = robot.Ftp.DirectoryExists("/JOB");

        robot.Disconnect();
    }
}
```

The root of the controller has one folder per type of file: `/JOB`, `/DAT`, `/CND`, `/SYS`, `/PRM`, `/LST`, `/CSV`, `/LOG`, `/TXT`.

| Method                        | Returns                                                             |
| ----------------------------- | ------------------------------------------------------------------- |
| `GetListing(path)`            | The files and folders of a folder: `Name`, `FullName`, `Modified`, `Type` |
| `GetFileList(fileExtension)`  | The names of the files of one type                                  |
| `GetFileListByPattern("*.PRM")` | The names of the files that match a pattern                       |
| `FileExists(path)`            | `true` if the file exists                                           |
| `DirectoryExists(path)`       | `true` if the folder exists                                         |

The controller does not give the size of the files in the listing. Download a file to know its size.

## Delete a file

`DeleteFile(name)` deletes a file. The folder is found from the extension. It needs the `ftp` or `rcmaster` account. There is no undo: download the file first if you may need it.

The controller does not overwrite a job by FTP. To replace a job, delete it, then send the new one:

```csharp
using UnderAutomation.Yaskawa;

public class FtpDelete
{
    static void Main()
    {
        var parameters = new ConnectParameters("192.168.0.1");
        parameters.Ftp.Enable = true;
        parameters.Ftp.FtpUser = "ftp";
        var robot = new YaskawaRobot();
        robot.Connect(parameters);

        // A job must be deleted before it is sent again: the controller does not overwrite a job by FTP
        if (robot.Ftp.FileExists("/JOB/NEWJOB.JBI"))
            robot.Ftp.DeleteFile("NEWJOB.JBI");

        robot.Ftp.LoadFile("NEWJOB.JBI", File.ReadAllText("NEWJOB.JBI"));

        robot.Disconnect();
    }
}
```

## Errors

Each failure throws an `FtpException`, with the operation, the file and the reason.

```csharp
using UnderAutomation.Yaskawa;
using UnderAutomation.Yaskawa.Ftp;

public class FtpErrors
{
    static void Main()
    {
        var parameters = new ConnectParameters("192.168.0.1");
        parameters.Ftp.Enable = true;
        parameters.Ftp.FtpUser = "ftp";
        var robot = new YaskawaRobot();
        robot.Connect(parameters);

        try
        {
            robot.Ftp.LoadFile("NEWJOB.JBI", File.ReadAllText("NEWJOB.JBI"));
        }
        catch (FtpException ex)
        {
            // Reason: LoginIncorrect, AccessDenied, FileNotFound, JobAlreadyExists, DeleteRefused, ConnectionError
            Console.WriteLine($"{ex.Operation} of {ex.RemotePath} failed: {ex.Reason}");
            Console.WriteLine($"Controller reply {ex.ReplyCode}: {ex.ReplyMessage}");
        }

        robot.Disconnect();
    }
}
```

| `Reason`           | Meaning                                                                   |
| ------------------ | ------------------------------------------------------------------------- |
| `LoginIncorrect`   | The user name or the password is refused                                  |
| `AccessDenied`     | The account has no right for this operation, for example an upload with `anonymous` |
| `FileNotFound`     | The file does not exist on the controller                                 |
| `JobAlreadyExists` | The job exists: delete it first                                           |
| `DeleteRefused`    | The controller refused to delete the file                                 |
| `ConnectionError`  | The connection was lost, or no answer before the timeout                  |
| `Unknown`          | Another refusal: `ReplyCode` and `ReplyMessage` give the answer of the controller |

## Reference

**Methods of FtpClientBase** ([reference](../api/UnderAutomation.Yaskawa.Ftp.Internal.md#ftpclientbase-robotftp))

- `void DeleteFile(string fileName)`: Deletes a file from the robot controller. The "anonymous" user cannot delete files.
  - async: `Task DeleteFileAsync(string fileName, CancellationToken cancellationToken = default)`
- `bool DirectoryExists(string path)`: Checks whether a folder exists on the controller.
  - async: `Task<bool> DirectoryExistsAsync(string path, CancellationToken cancellationToken = default)`
- `bool FileExists(string remotePath)`: Checks whether a file exists on the controller.
  - async: `Task<bool> FileExistsAsync(string remotePath, CancellationToken cancellationToken = default)`
- `string[] GetFileList(FileExtension fileExtension)`: Lists the files of the specified type on the controller.
  - async: `Task<string[]> GetFileListAsync(FileExtension fileExtension, CancellationToken cancellationToken = default)`
- `string[] GetFileListByPattern(string pattern)`: Lists the files whose names match the specified pattern. When the pattern has a known extension (e.g. "*.JBI"), only the matching folder is listed. Otherwise, all folders of the controller are listed.
  - async: `Task<string[]> GetFileListByPatternAsync(string pattern, CancellationToken cancellationToken = default)`
- `FtpListItem[] GetListing(string path)`: Returns the files and folders at the specified path on the controller. The root contains one folder per file type (JOB, DAT, CND, SYS, PRM, LST, CSV, LOG, TXT).
  - async: `Task<FtpListItem[]> GetListingAsync(string path, CancellationToken cancellationToken = default)`

**FtpConnectParameters** ([reference](../api/UnderAutomation.Yaskawa.Ftp.md#ftpconnectparameters))

- `FtpConnectParameters()`: Initializes a new instance of the FTP connection parameters with default values.
- `const int DEFAULT_PORT = 21`: Default FTP port (21).
- `const int DEFAULT_TIMEOUT_MILLISECONDS = 30000`: Default timeout in milliseconds for FTP operations (30000ms).
- `string FtpPassword { get; set; }`: Gets or sets the FTP password associated with FtpConnectParameters.FtpUser. For rcmaster: must be the controller management mode password.For ftp or anonymous: any value is accepted (including null or empty).If the password protection option is enabled: use the password defined in that option. De...
- `string FtpUser { get; set; }`: Gets or sets the FTP user name used to authenticate with the robot controller. Standard accounts: rcmaster: widest rights, requires the management mode password.ftp: standard mode only, accepts any password.anonymous: standard mode only, accepts any password, download only. If the password protec...
- `int Port { get; set; }`: Gets or sets the FTP port number. Default: 21.
- `int TimeoutMilliseconds { get; set; }`: Gets or sets the timeout in milliseconds applied to FTP read, connect, and data transfer operations. Default: 30000ms.

**FtpListItem** ([reference](../api/UnderAutomation.Yaskawa.Ftp.md#ftplistitem))

- `string FullName { get; }`: Full path on the controller (e.g. "/JOB/TEST.JBI").
- `DateTime Modified { get; }`: Date and time of the last modification, as given by the controller.
- `string Name { get; }`: File or folder name without its path (e.g. "TEST.JBI").
- `FtpFileSystemObjectType Type { get; }`: Indicates whether this item is a file or a folder.

**FtpException** ([reference](../api/UnderAutomation.Yaskawa.Ftp.md#ftpexception))

- `FtpOperation Operation { get; }`: Operation that failed.
- `FtpErrorReason Reason { get; }`: Reason of the failure.
- `string RemotePath { get; }`: Path of the file on the controller concerned by the operation. Null for connection and listing errors.
- `int ReplyCode { get; }`: FTP reply code returned by the controller (e.g. 550). 0 if the controller did not reply.
- `string ReplyMessage { get; }`: Raw reply text returned by the controller. Null if the controller did not reply.
- `string User { get; }`: FTP user name that was logged when the error occurred.

**FtpErrorReason** ([reference](../api/UnderAutomation.Yaskawa.Ftp.md#ftperrorreason))

- AccessDenied: The logged user does not have the right to do this operation on this file.
- ConnectionError: The connection with the controller was lost or timed out.
- DeleteRefused: The controller refused to delete the file.
- FileNotFound: The file does not exist on the controller.
- JobAlreadyExists: The job already exists on the controller. The controller does not overwrite a job by FTP.
- LoginIncorrect: The user name or the password is not accepted by the controller.
- Unknown: The controller refused the operation for another reason. See FtpException.ReplyMessage.

## What to read next

- [FTP file transfers](ftp-transfer.md): download and upload text, bytes and local files.
- [Transfer files and backups](how-to-transfer-files.md): FTP, HTTP or High Speed Ethernet Server.
