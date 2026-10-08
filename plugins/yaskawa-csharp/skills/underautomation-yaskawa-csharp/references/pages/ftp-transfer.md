# FTP file transfers

Download and upload the jobs and data files of a Yaskawa controller over FTP: text, bytes, local files, several files at once, progress and async methods.

Web page: https://underautomation.com/yaskawa/documentation/ftp-transfer

This page shows how to download and upload the files of a Yaskawa Motoman controller over FTP with the SDK: text, bytes, local files and several files at once, with the progress of each transfer. It covers the YRC1000 and YRC1000micro controllers. The connection and the accounts are explained in [FTP](ftp.md).

## File names and paths

Each method takes a file name or a full path on the controller:

- A name, for example `TEST.JBI`: the SDK finds the folder from the extension. `.JBI` and `.JBR` go to `/JOB`, `.DAT` to `/DAT`, `.PRM` to `/PRM`, and so on for `.CND`, `.SYS`, `.LST`, `.CSV`, `.LOG` and `.TXT`.
- A full path, for example `/JOB/TEST.JBI`.

## Download

```csharp
using UnderAutomation.Yaskawa;

public class FtpDownload
{
    static void Main()
    {
        var parameters = new ConnectParameters("192.168.0.1");
        parameters.Ftp.Enable = true;
        parameters.Ftp.FtpUser = "ftp";
        var robot = new YaskawaRobot();
        robot.Connect(parameters);

        // Text of a file: the folder is deduced from the extension
        string job = robot.Ftp.GetFile("TEST.JBI");

        // Bytes of a file, with its full path
        byte[] variables = robot.Ftp.DownloadFile("/DAT/VAR.DAT");

        // To a file of the PC
        robot.Ftp.DownloadFileToLocal("/PRM/ALL.PRM", @"C:\Backup\ALL.PRM");

        // Several files into a folder of the PC: returns the local paths
        string[] saved = robot.Ftp.DownloadFilesToLocal(new[] { "/JOB/TEST.JBI", "/DAT/VAR.DAT" }, @"C:\Backup");

        robot.Disconnect();
    }
}
```

| Method                                    | Result                                                                  |
| ----------------------------------------- | ----------------------------------------------------------------------- |
| `GetFile(name)`                           | Text of the file                                                        |
| `DownloadFile(path)`                      | Bytes of the file                                                       |
| `DownloadFileToLocal(path, localPath)`    | File saved on the PC. An existing local file is replaced. Nothing is written if the download fails |
| `DownloadFilesToLocal(paths, localFolder)` | Files saved in a folder of the PC, created if needed. Returns the local paths |
| `DownloadFileToStream(path, stream)`      | Bytes written to a .NET stream (.NET only)                              |

## Upload

### Rules of the controller

- Only jobs (`.JBI`, `.JBR`), condition files (`.CND`) and general data (`.DAT`) can be uploaded.
- The account must be `ftp` or `rcmaster`. `anonymous` cannot upload.
- The controller does not overwrite a job: delete it first, see [Delete a file](ftp.md#delete_a_file). Otherwise the upload fails with the reason `JobAlreadyExists`.
- An empty file is refused: the SDK throws an `ArgumentException` before the transfer.
- The controller checks the syntax of a job when it receives it.

### Methods

```csharp
using UnderAutomation.Yaskawa;
using System.Text;

public class FtpUpload
{
    static void Main()
    {
        var parameters = new ConnectParameters("192.168.0.1");
        parameters.Ftp.Enable = true;
        parameters.Ftp.FtpUser = "ftp";
        var robot = new YaskawaRobot();
        robot.Connect(parameters);

        // A job written on the PC: the folder is deduced from the extension
        string job = File.ReadAllText("NEWJOB.JBI");
        robot.Ftp.LoadFile("NEWJOB.JBI", job);

        // Bytes, with the full path on the controller
        robot.Ftp.UploadFile("/JOB/OTHER.JBI", Encoding.ASCII.GetBytes(job));

        // A file of the PC: the remote path is deduced from its name and extension
        robot.Ftp.UploadFileFromLocal(@"C:\Jobs\PICK.JBI");

        // Several files of the PC: returns the remote paths
        string[] sent = robot.Ftp.UploadFilesFromLocal(new[] { @"C:\Jobs\A.JBI", @"C:\Jobs\B.JBI" });

        robot.Disconnect();
    }
}
```

| Method                                   | Source                                                                  |
| ---------------------------------------- | ----------------------------------------------------------------------- |
| `LoadFile(name, text)`                   | Text                                                                    |
| `UploadFile(path, bytes)`                | Bytes                                                                   |
| `UploadFileFromLocal(localPath, path)`   | File of the PC. Without `path`, the name of the local file is used      |
| `UploadFilesFromLocal(localPaths)`       | Several files of the PC, each with its own name. Stops at the first error. Returns the remote names |
| `UploadFileFromStream(path, stream)`     | A .NET stream, read from its current position (.NET only)               |

## Progress

The transfer methods take an optional callback. It receives the progress in percent, from 0 to 100, or -1 when the size is not known. For several files, the progress is the global progress.

```csharp
using UnderAutomation.Yaskawa;

public class FtpProgress
{
    static void Main()
    {
        var parameters = new ConnectParameters("192.168.0.1");
        parameters.Ftp.Enable = true;
        parameters.Ftp.FtpUser = "ftp";
        var robot = new YaskawaRobot();
        robot.Connect(parameters);

        // Percentage from 0 to 100, -1 when the size is not known
        byte[] backup = robot.Ftp.DownloadFile("/PRM/ALL.PRM",
            progress => Console.WriteLine($"{progress:F0} %"));

        robot.Disconnect();
    }
}
```

In Python, pass a function or a lambda.

## Async methods

In .NET, every FTP method has an async version that takes a `CancellationToken`: `ConnectAsync`, `GetFileAsync`, `DownloadFilesToLocalAsync`, `UploadFileFromLocalAsync`... Use them in a user interface, so that a long transfer does not block it. They are not available on .NET Framework 3.5 and 4.0, and not in Python.

```csharp
using UnderAutomation.Yaskawa.Ftp;

public class FtpAsync
{
    static async Task Main()
    {
        var client = new FtpClient();
        await client.ConnectAsync("192.168.0.1", "ftp");

        // Every FTP method has an async version with a CancellationToken
        using var cts = new CancellationTokenSource(TimeSpan.FromMinutes(1));
        string[] jobs = await client.GetFileListByPatternAsync("*.JBI", cts.Token);
        string[] saved = await client.DownloadFilesToLocalAsync(
            jobs.Select(j => "/JOB/" + j).ToArray(), @"C:\Backup", null, cts.Token);

        client.Close();
    }
}
```

## Reference

**Methods of FtpClientBase** ([reference](../api/UnderAutomation.Yaskawa.Ftp.Internal.md#ftpclientbase-robotftp))

- `byte[] DownloadFile(string remotePath, OnProgressDelegate progress = null)`: Downloads a file from the controller and returns its content.
  - async: `Task<byte[]> DownloadFileAsync(string remotePath, OnProgressDelegate progress = null, CancellationToken cancellationToken = default)`
- `void DownloadFileToLocal(string remotePath, string localPath, OnProgressDelegate progress = null)`: Downloads a file from the controller and saves it on the local file system. Overwrites the local file if it already exists. The local file is not created if the download fails.
  - async: `Task DownloadFileToLocalAsync(string remotePath, string localPath, OnProgressDelegate progress = null, CancellationToken cancellationToken = default)`
- `void DownloadFileToStream(string remotePath, Stream destination, OnProgressDelegate progress = null)`: Downloads a file from the controller and writes its content into a stream.
  - async: `Task DownloadFileToStreamAsync(string remotePath, Stream destination, OnProgressDelegate progress = null, CancellationToken cancellationToken = default)`
- `string[] DownloadFilesToLocal(string[] remotePaths, string localFolder, OnProgressDelegate progress = null)`: Downloads several files from the controller into a local folder. Each file is saved with its name, and existing local files are overwritten.
  - async: `Task<string[]> DownloadFilesToLocalAsync(string[] remotePaths, string localFolder, OnProgressDelegate progress = null, CancellationToken cancellationToken = default)`
- `string GetFile(string fileName)`: Downloads a text file from the robot controller and returns its content.
  - async: `Task<string> GetFileAsync(string fileName, CancellationToken cancellationToken = default)`
- `string[] GetFileList(FileExtension fileExtension)`: Lists the files of the specified type on the controller.
  - async: `Task<string[]> GetFileListAsync(FileExtension fileExtension, CancellationToken cancellationToken = default)`
- `string[] GetFileListByPattern(string pattern)`: Lists the files whose names match the specified pattern. When the pattern has a known extension (e.g. "*.JBI"), only the matching folder is listed. Otherwise, all folders of the controller are listed.
  - async: `Task<string[]> GetFileListByPatternAsync(string pattern, CancellationToken cancellationToken = default)`
- `void LoadFile(string fileName, string content)`: Uploads text content to the robot controller as a file. The file type is given by the extension of fileName (e.g. ".JBI" for a job).
  - async: `Task LoadFileAsync(string fileName, string content, CancellationToken cancellationToken = default)`
- `void UploadFile(string remotePath, byte[] data, OnProgressDelegate progress = null)`: Uploads a byte array as a file onto the controller. Only jobs (.JBI, .JBR), condition files (.CND) and general data (.DAT) can be uploaded, with the "ftp" or "rcmaster" user. An existing job is not overwritten: delete it first with DeleteFile(System.String).
  - async: `Task UploadFileAsync(string remotePath, byte[] data, OnProgressDelegate progress = null, CancellationToken cancellationToken = default)`
- `void UploadFileFromLocal(string localPath, string remotePath = null, OnProgressDelegate progress = null)`: Uploads a local file onto the controller. Only jobs (.JBI, .JBR), condition files (.CND) and general data (.DAT) can be uploaded, with the "ftp" or "rcmaster" user. An existing job is not overwritten: delete it first with DeleteFile(System.String).
  - async: `Task UploadFileFromLocalAsync(string localPath, string remotePath = null, OnProgressDelegate progress = null, CancellationToken cancellationToken = default)`
- `void UploadFileFromStream(string remotePath, Stream source, OnProgressDelegate progress = null)`: Uploads the content of a stream as a file onto the controller. The stream is read from its current position to its end. Only jobs (.JBI, .JBR), condition files (.CND) and general data (.DAT) can be uploaded, with the "ftp" or "rcmaster" user. An existing job is not overwritten: delete it first wi...
  - async: `Task UploadFileFromStreamAsync(string remotePath, Stream source, OnProgressDelegate progress = null, CancellationToken cancellationToken = default)`
- `string[] UploadFilesFromLocal(string[] localPaths, OnProgressDelegate progress = null)`: Uploads several local files onto the controller. Each file is uploaded with its local file name. The controller stores each file in the folder of its type (e.g. a ".JBI" file goes to the JOB folder). The upload stops at the first error.
  - async: `Task<string[]> UploadFilesFromLocalAsync(string[] localPaths, OnProgressDelegate progress = null, CancellationToken cancellationToken = default)`

**OnProgressDelegate** ([reference](../api/UnderAutomation.Yaskawa.Ftp.md#onprogressdelegate))

- `OnProgressDelegate(object @object, nint method)`
- `IAsyncResult BeginInvoke(double progress, AsyncCallback callback, object @object)`
- `void EndInvoke(IAsyncResult result)`
- `void Invoke(double progress)`

## What to read next

- [Transfer files and backups](how-to-transfer-files.md): a complete backup program, and which protocol to choose.
- [Kinematics models](kinematics-models.md): read the geometry of the robot from its `ALL.PRM` file.
