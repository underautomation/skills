# File management

Upload, download, delete, rename files and directories on the Fanuc robot controller via FTP.

Web page: https://underautomation.com/fanuc/documentation/ftp-file-management

Upload, download, delete, and rename files and directories on the Fanuc robot controller via FTP.

## Upload files

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Ftp;

public class FtpFileManagementUpload
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        var parameters = new ConnectionParameters("192.168.0.1");
        parameters.Ftp.Enable = true;
        parameters.Ftp.FtpUser = "";
        parameters.Ftp.FtpPassword = "";
        robot.Connect(parameters);

        // Upload a TP program to the controller (overwrites if it already exists)
        robot.Ftp.DirectFileHandling.UploadFileToController(@"C:\Programs\MyPrg.tp", "md:/MyPrg.tp");

        // Skip upload if the file already exists on the controller
        robot.Ftp.DirectFileHandling.UploadFileToController(
            @"C:\Programs\MyPrg.tp", "md:/MyPrg.tp",
            existsBehavior: FtpExistsBehavior.Skip);

        // Resume a partial upload (appends missing bytes)
        robot.Ftp.DirectFileHandling.UploadFileToController(
            @"C:\LargeFile.tp", "md:/LargeFile.tp",
            existsBehavior: FtpExistsBehavior.Append);

        // Upload from a byte array
        byte[] fileBytes = File.ReadAllBytes(@"C:\Programs\MyPrg.tp");
        robot.Ftp.DirectFileHandling.UploadFileToController(
            fileBytes, "md:/MyPrg.tp",
            existsBehavior: FtpExistsBehavior.Overwrite);

        // Upload multiple files to a directory
        robot.Ftp.DirectFileHandling.UploadFilesToController(
            new[] { @"C:\file1.tp", @"C:\file2.tp" },
            "md:/programs/");
    }
}
```

## Download files

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Ftp;

public class FtpFileManagementDownload
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        var parameters = new ConnectionParameters("192.168.0.1");
        parameters.Ftp.Enable = true;
        parameters.Ftp.FtpUser = "";
        parameters.Ftp.FtpPassword = "";
        robot.Connect(parameters);

        // Download to a local file
        robot.Ftp.DirectFileHandling.DownloadFileFromController(@"C:\Backup\Backup.va", "md:/Backup.va");

        // Download to a byte array
        byte[] data;
        robot.Ftp.DirectFileHandling.DownloadFileFromController(out data, "md:/MyPrg.tp");

        // Download multiple files
        robot.Ftp.DirectFileHandling.DownloadFilesFromController(
            @"C:\Backup\",
            new[] { "md:/file1.tp", "md:/file2.va" });
    }
}
```

## Delete, list, and manage directories

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Ftp;

public class FtpFileManagementDirectory
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        var parameters = new ConnectionParameters("192.168.0.1");
        parameters.Ftp.Enable = true;
        parameters.Ftp.FtpUser = "";
        parameters.Ftp.FtpPassword = "";
        robot.Connect(parameters);

        // Delete a file
        robot.Ftp.DirectFileHandling.DeleteFile("md:/OldProgram.tp");

        // Delete a directory and its contents
        robot.Ftp.DirectFileHandling.DeleteDirectory("md:/OldFolder");

        // Check if a directory exists
        bool exists = robot.Ftp.DirectFileHandling.DirectoryExists("md:/programs");

        // Create a directory
        robot.Ftp.DirectFileHandling.CreateDirectory("md:/NewFolder");

        // List files and directories
        FtpListItem[] items = robot.Ftp.DirectFileHandling.GetListing("md:/");
        foreach (var item in items)
        {
            Console.WriteLine($"{item.Name} ({item.Type}) - {item.Size} bytes");
        }

        // Rename or move a file
        robot.Ftp.DirectFileHandling.Rename("md:/old.tp", "md:/new.tp");
    }
}
```

## Asynchronous transfers

Each method has an asynchronous version (`UploadFileToControllerAsync`, `DownloadFileFromControllerAsync`, `DownloadBytesFromControllerAsync`, `GetListingAsync`, `FileExistsAsync`, `DeleteFileAsync`...) with an optional `CancellationToken`. They are not available on .NET Framework 3.5 and 4.0.

```csharp
using UnderAutomation.Fanuc;

public class FtpFileManagementAsync
{
    static async Task Main()
    {
        FanucRobot robot = new FanucRobot();
        var parameters = new ConnectionParameters("192.168.0.1");
        parameters.Ftp.Enable = true;
        parameters.Ftp.FtpUser = "";
        parameters.Ftp.FtpPassword = "";
        robot.Connect(parameters);

        var files = robot.Ftp.DirectFileHandling;

        // Download a program, with the progress of the transfer (0 to 100)
        byte[] program = await files.DownloadBytesFromControllerAsync("md:/MyPrg.ls", p => Console.WriteLine($"{p:F0} %"));

        // Upload it again, cancelled after 30 seconds
        using (var cts = new CancellationTokenSource(TimeSpan.FromSeconds(30)))
        {
            await files.UploadFileToControllerAsync(program, "md:/MyPrg.ls", cancellationToken: cts.Token);
        }

        // Check and delete
        if (await files.FileExistsAsync("md:/OldPrg.ls"))
            await files.DeleteFileAsync("md:/OldPrg.ls");

        robot.Disconnect();
    }
}
```

## Errors

When the controller refuses an operation, the SDK throws an `FtpException` with the reply of the controller (`ReplyCode`, `ReplyMessage`) and, when it is known, what to do. A download that does not complete returns `false` (or `null` for `DownloadBytesFromControllerAsync`).

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Ftp;

public class FtpFileManagementErrors
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        var parameters = new ConnectionParameters("192.168.0.1");
        parameters.Ftp.Enable = true;
        parameters.Ftp.FtpUser = "";
        parameters.Ftp.FtpPassword = "";
        robot.Connect(parameters);

        try
        {
            robot.Ftp.DirectFileHandling.UploadFileToController(@"C:\Programs\MyPrg.ls", "md:/MyPrg.ls");
        }
        catch (FtpException ex) when (ex.ProgramInUse)
        {
            // The program is selected on the teach pendant or it runs:
            // select another program (teach pendant, or robot.Cgtp.SelectProgram from V9.10), then upload again
            Console.WriteLine(ex.Message);
        }
        catch (FtpException ex)
        {
            // Other refusal of the controller, for example "Operation password protected":
            // the FTP user does not have enough rights
            Console.WriteLine($"{ex.ReplyCode} {ex.ReplyMessage}");
        }

        robot.Disconnect();
    }
}
```

### Rights of the user

The password settings of the controller can restrict the rights of the FTP user. Without a user, the controller logs in at the OPERATOR level and can refuse the upload of a program with "Operation password protected". Connect with a user that has the needed level, for example INSTALL.

### Program in use

A program that is selected on the teach pendant, or that runs, cannot be replaced: the controller replies "Specified program is in use" and `FtpException.ProgramInUse` is true. Select another program, then upload again:

- on the teach pendant, with the SELECT key;
- remotely, with `robot.Cgtp.SelectProgram("OTHER")` (web server of the controller, firmware V9.10 and later). See [Programs](cgtp-programs.md).

The controller writes the modification date into the program when it is uploaded: a program downloaded after an upload can differ from the uploaded file on the date lines only.

## Complete example

```csharp
using UnderAutomation.Fanuc;

public class FtpFileManagement
{
  static void Main()
  {
    FanucRobot robot = new FanucRobot();
    ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");
    parameters.Ftp.Enable = true;
    parameters.Ftp.FtpUser = "";
    parameters.Ftp.FtpPassword = "";
    robot.Connect(parameters);

    // Upload a TP program to the controller
    robot.Ftp.DirectFileHandling.UploadFileToController(@"C:\Programs\MyPrg.tp", "md:/MyPrg.tp");

    // Download a file from the robot
    robot.Ftp.DirectFileHandling.DownloadFileFromController(@"C:\Backup\Backup.va", "md:/Backup.va");

    // Delete a file
    robot.Ftp.DirectFileHandling.DeleteFile("md:/OldProgram.tp");

    // List files in a directory
    var items = robot.Ftp.DirectFileHandling.GetListing("md:/");
    foreach (var item in items)
      Console.WriteLine($"{item.Name} ({item.Type})");

    // Create and delete directories
    robot.Ftp.DirectFileHandling.CreateDirectory("md:/NewFolder");

    // Rename a file
    robot.Ftp.DirectFileHandling.Rename("md:/old.tp", "md:/new.tp");

    // Check file existence
    bool exists = robot.Ftp.DirectFileHandling.FileExists("md:/MyPrg.tp");
  }
}
```

## API reference

**FtpDirectFileHandling** ([reference](../api/UnderAutomation.Fanuc.Ftp.Internal.md#ftpdirectfilehandling-robotftpdirectfilehandling))

- `void CreateDirectory(string path)`: Creates a directory on the controller. If the preceding directories do not exist, then they are created.
- `void DeleteDirectory(string path)`: Deletes the specified directory and all its contents.
- `void DeleteFile(string path)`: Deletes a file on the controller
- `bool DirectoryExists(string path)`: Tests if the specified directory exists on the controller. This method works by trying to change the working directory to the path specified. If it succeeds, the directory is changed back to the old working directory and true is returned. False is returned otherwise and since the CWD failed it is...
- `bool DownloadFileFromController(out byte[] outBytes, string remotePath, OnProgressDelegate progress = null)`: Downloads the specified file and return the raw byte array. High-level API that takes care of various edge cases internally. Supports very large files since it downloads data in chunks.
- `bool DownloadFileFromController(Stream outStream, string remotePath, OnProgressDelegate progress = null)`: Downloads the specified file into the specified stream. High-level API that takes care of various edge cases internally. Supports very large files since it downloads data in chunks.
- `bool DownloadFileFromController(string localPath, string remotePath, OnProgressDelegate progress = null)`: Downloads the specified file onto the local file system. High-level API that takes care of various edge cases internally. Supports very large files since it downloads data in chunks. It overwrites the file if it already exists.
- `string[] DownloadFilesFromController(string localDir, string[] remotePaths, OnProgressDelegate progress = null)`: Downloads the specified files into a local single directory. High-level API that takes care of various edge cases internally. Supports very large files since it downloads data in chunks. A file that fails is skipped: it is not in the returned list.
- `bool FileExists(string path)`: Checks if a file exists on the controller.
- `FtpListItem[] GetListing(string path)`: Gets a file listing from the controller. Each Ftp.FtpListItem object returned contains information about the file that was able to be retrieved.
- `FtpListItem GetObjectInfo(string path)`: Returns information about a file system object. Returns null if the controller response can't be parsed or the controller returns a failure completion code. No exception is thrown on error because that would negate the usefulness of this method for checking for the existence of an object.
- `void Rename(string path, string dest)`: Renames an object on the remote file system. Throws exceptions if the file does not exist, or if the destination file already exists.
- `bool UploadFileToController(byte[] fileData, string remotePath, bool createRemoteDir = false, OnProgressDelegate progress = null, FtpExistsBehavior existsBehavior = FtpExistsBehavior.Overwrite)`: Uploads the specified byte array as a file onto the controller. High-level API that takes care of various edge cases internally. Supports very large files since it uploads data in chunks. It overwrites file if it already exists.
- `bool UploadFileToController(Stream fileStream, string remotePath, bool createRemoteDir = false, OnProgressDelegate progress = null, FtpExistsBehavior existsBehavior = FtpExistsBehavior.Overwrite)`: Uploads the specified stream as a file onto the controller. High-level API that takes care of various edge cases internally. Supports very large files since it uploads data in chunks. It overwrites file if it already exists.
- `bool UploadFileToController(string localPath, string remotePath, bool createRemoteDir = false, OnProgressDelegate progress = null, FtpExistsBehavior existsBehavior = FtpExistsBehavior.Overwrite)`: Uploads the specified file directly onto the controller. High-level API that takes care of various edge cases internally. Supports very large files since it uploads data in chunks.
- `string[] UploadFilesToController(string[] localPaths, string remoteDir, OnProgressDelegate progress = null)`: Uploads the given file paths to a single folder on the controller. All files are placed directly into the given folder regardless of their path on the local filesystem. High-level API that takes care of various edge cases internally. Supports very large files since it uploads data in chunks. A fi...

**FtpListItem** ([reference](../api/UnderAutomation.Fanuc.Ftp.md#ftplistitem))

- `int Chmod { get; }`: Gets the file permissions in the CHMOD format.
- `DateTime Created { get; }`: Gets the created date of the object.
- `string FullName { get; }`: Gets the full path name to the object.
- `DateTime Modified { get; }`: Gets the last write time of the object.
- `string Name { get; }`: Gets name to the object.
- `long Size { get; }`: Gets the size of the object. Only a few files (like *.tp or *.df) have a size that can be retrieved, for most files this is 0 even if they are not empty. For directories this is always 0.
- `FtpFileSystemObjectType Type { get; }`: Gets the type of file system object.

**FtpException** ([reference](../api/UnderAutomation.Fanuc.Ftp.md#ftpexception))

- `bool ProgramInUse { get; }`: True when the controller refused the operation because the program is in use: it is selected on the teach pendant or it runs. Select another program before you upload or delete it.
- `string RemotePath { get; }`: Path of the file or folder on the controller concerned by the operation. Null when the operation has no path.
- `int ReplyCode { get; }`: FTP reply code returned by the controller (for example 550). 0 when the controller did not reply.
- `string ReplyMessage { get; }`: Reply text returned by the controller (for example "Specified program is in use"). Null when the controller did not reply.
