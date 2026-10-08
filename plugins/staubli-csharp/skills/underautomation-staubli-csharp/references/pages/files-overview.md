# Files overview

Access the files of a CS8 or CS9 controller: FTP server of a real controller, or .controller file of a controller emulated by Staubli Robotics Suite. Connection, paths, /usr/usrapp and errors.

Web page: https://underautomation.com/staubli/documentation/files-overview

This page explains how the Staubli SDK accesses the files of a CS8 or CS9 controller, real or emulated by Staubli Robotics Suite: the connection, the paths and the errors. The file client `controller.File` uploads, downloads, lists and manages the files, and sends complete VAL 3 applications.

## Real or emulated controller

The same methods work on both, with the same paths. Only the address changes.

### Real controller

The file client uses the FTP server of the controller. Give its IP address, and the user and the password of the FTP server.

```csharp
using UnderAutomation.Staubli;

public class FilesConnect
{
    static void Main()
    {
        var parameters = new ConnectionParameters("192.168.0.254");

        // The file client is disabled by default
        parameters.File.Enable = true;

        // User and password of the FTP server of the controller
        parameters.File.User = "default";
        parameters.File.Password = "default";

        var controller = new StaubliController();
        controller.Connect(parameters);

        // False with a real controller: the files go through FTP
        Console.WriteLine(controller.File.IsSimulated);

        controller.Disconnect();
    }
}
```

### Emulated controller

The emulator of Staubli Robotics Suite (SRS) has no FTP server. It keeps the files of the emulated controller in the folder of its `.controller` file, with the same tree as a real controller (`usr`, `log`). Give the path of the `.controller` file as address:

- **Local path** (`C:\...\MyCell\Controller1\Controller1.controller`): the emulator runs on this PC. The SOAP client connects to `127.0.0.1`.
- **UNC path** (`\\SRS-PC\share\...\Controller1\Controller1.controller`): the emulator runs on another PC. The SOAP client connects to this PC, and the files go through the Windows share.

A path that is not a `.controller` file is refused. The SOAP port of the emulated controller is read from its configuration: see [Test with the Staubli Robotics Suite emulator](simulator.md).

```csharp
using UnderAutomation.Staubli;

public class FilesConnectSimulator
{
    static void Main()
    {
        // Controller emulated by Staubli Robotics Suite on this PC: give its .controller file.
        // The SOAP client connects to 127.0.0.1, the file client uses the folder of the .controller file.
        var parameters = new ConnectionParameters(@"C:\SRS\MyCell\Controller1\Controller1.controller");

        // Emulator on another PC: give a UNC path. The SOAP client connects to this PC.
        // var parameters = new ConnectionParameters(@"\\SRS-PC\SRS\MyCell\Controller1\Controller1.controller");

        parameters.File.Enable = true;

        var controller = new StaubliController();
        controller.Connect(parameters);

        // True: the files are read and written in the folder of the .controller file
        Console.WriteLine(controller.File.IsSimulated);
        Console.WriteLine(controller.File.ControllerFolder);

        controller.Disconnect();
    }
}
```

`IsSimulated` tells which mode is used. With an emulated controller, `ControllerFile` gives the full path of the `.controller` file and `ControllerFolder` the folder of the files, and the user and the password are not used.

## Connection parameters

| Parameter        | Default     | Meaning                                                       |
| ---------------- | ----------- | ------------------------------------------------------------- |
| `File.Enable`    | `false`     | Connect the file client                                       |
| `File.User`      | `"default"` | User of the FTP server of the controller                      |
| `File.Password`  | `"default"` | Password of this user                                         |
| `File.Port`      | `21`        | Port of the FTP server (`FileConnectParameters.DEFAULT_PORT`) |
| `File.TimeoutMs` | `30000`     | Timeout of the FTP connection and of the transfers, in ms     |

Set `Soap.Enable` to `false` to use the file client alone. The SOAP parameters are on the page [Connect to your robot](connect.md).

## Paths on the controller

The paths are the paths of the controller, with `/` as separator: `/usr/usrapp/myApp/myApp.pjx`. A path that does not start with `/` is relative to the root of the controller. With an emulated controller, the root is the folder of the `.controller` file: a path cannot go outside of it.

| Folder              | Content                                                                                   |
| ------------------- | ----------------------------------------------------------------------------------------- |
| `/usr/usrapp`       | The VAL 3 applications, one sub-folder per application (`FileClientBase.USER_APP_FOLDER`) |
| `/usr/usrapp/myApp` | The files of the application `myApp`: `myApp.pjx`, its programs and its data              |

The project path `Disk://myApp/myApp.pjx` of the SOAP methods (`LoadProject`, `StartApplication`) is the file `/usr/usrapp/myApp/myApp.pjx`.

## Standalone file client

`FileClient` connects without `StaubliController`. Its address is an IP or the path of a `.controller` file, as above.

```csharp
using UnderAutomation.Staubli.Files;

public class FilesStandalone
{
    static void Main()
    {
        var files = new FileClient();

        // Real controller: IP, FTP user and password (port 21 by default)
        files.Connect("192.168.0.254", "default", "default");

        // Or the .controller file of a controller emulated by Staubli Robotics Suite (the user and the password are not used)
        // files.Connect(@"C:\SRS\MyCell\Controller1\Controller1.controller", null, null);

        foreach (FileItem item in files.GetListing("/usr/usrapp"))
            Console.WriteLine(item.Name);

        files.Disconnect();
    }
}
```

## Errors

```csharp
using UnderAutomation.Staubli;
using UnderAutomation.Staubli.Files;

public class FilesErrors
{
    static void Main()
    {
        var parameters = new ConnectionParameters("192.168.0.254");
        parameters.File.Enable = true;
        var controller = new StaubliController();

        try
        {
            controller.Connect(parameters);
            byte[] content = controller.File.DownloadBytesFromController("/usr/usrapp/myApp/myApp.pjx");
        }
        catch (FileException ex)
        {
            // Connection refused, file not found, or operation refused by the controller
            Console.WriteLine(ex.Message);

            // FTP reply of the controller, 0 and null when there is none
            Console.WriteLine($"{ex.RemotePath} {ex.ReplyCode} {ex.ReplyMessage}");
        }
        catch (DirectoryNotFoundException ex)
        {
            // The address is a folder that does not exist
            Console.WriteLine(ex.Message);
        }

        controller.Disconnect();
    }
}
```

| Exception                    | When                                                                                        |
| ---------------------------- | ------------------------------------------------------------------------------------------- |
| `FileException`              | The FTP connection failed, the file does not exist, or the controller refused the operation |
| `ArgumentException`          | The address is a path but not a `.controller` file, or a path goes outside of its folder    |
| `FileNotFoundException`      | The `.controller` file does not exist                                                       |
| `InvalidOperationException`  | A method is called before the connection, or after `Disconnect`                             |

When the FTP connection fails, the message of `FileException` also reminds that an emulated controller needs the path of its `.controller` file. `ReplyCode` and `ReplyMessage` give the reply of the FTP server of the controller, when there is one. The errors of the local files of your PC (for example a local file that does not exist) are not converted.

## Reference

**Methods of FileClientBase** ([reference](../api/UnderAutomation.Staubli.Files.Internal.md#fileclientbase-controllerfile))

- `void CreateDirectory(string path)`: Creates a folder on the controller, with its parent folders when they do not exist. Nothing is done when the folder exists.
  - async: `Task CreateDirectoryAsync(string path, CancellationToken cancellationToken = default)`
- `void DeleteDirectory(string path)`: Deletes a folder of the controller and all its content
  - async: `Task DeleteDirectoryAsync(string path, CancellationToken cancellationToken = default)`
- `void DeleteFile(string path)`: Deletes a file of the controller
  - async: `Task DeleteFileAsync(string path, CancellationToken cancellationToken = default)`
- `bool DirectoryExists(string path)`: Checks if a folder exists on the controller
  - async: `Task<bool> DirectoryExistsAsync(string path, CancellationToken cancellationToken = default)`
- `void Disconnect()`: Disconnects the client
- `byte[] DownloadBytesFromController(string remotePath, OnProgressDelegate progress = null)`: Downloads a file of the controller and returns its content
  - async: `Task<byte[]> DownloadBytesFromControllerAsync(string remotePath, OnProgressDelegate progress = null, CancellationToken cancellationToken = default)`
- `void DownloadFileFromController(string localPath, string remotePath, OnProgressDelegate progress = null)`: Downloads a file of the controller to a local file. The local file is replaced when it exists, and its folder is created when it does not exist.
  - async: `Task DownloadFileFromControllerAsync(string localPath, string remotePath, OnProgressDelegate progress = null, CancellationToken cancellationToken = default)`
- `void DownloadStreamFromController(Stream stream, string remotePath, OnProgressDelegate progress = null)`: Downloads a file of the controller and writes its content to a stream
  - async: `Task DownloadStreamFromControllerAsync(Stream stream, string remotePath, OnProgressDelegate progress = null, CancellationToken cancellationToken = default)`
- `bool FileExists(string path)`: Checks if a file exists on the controller
  - async: `Task<bool> FileExistsAsync(string path, CancellationToken cancellationToken = default)`
- `FileItem GetFileInfo(string path)`: Gets information about a file or a folder of the controller
  - async: `Task<FileItem> GetFileInfoAsync(string path, CancellationToken cancellationToken = default)`
- `FileItem[] GetListing(string path)`: Lists the files and folders of a folder of the controller
  - async: `Task<FileItem[]> GetListingAsync(string path, CancellationToken cancellationToken = default)`
- `void Rename(string path, string newPath)`: Renames or moves a file or a folder of the controller
  - async: `Task RenameAsync(string path, string newPath, CancellationToken cancellationToken = default)`
- `string UploadApplicationToController(string localAppFolder, OnProgressDelegate progress = null)`: Uploads a complete VAL 3 application to the controller. The local folder of the application, named as the application and with its project file inside (for example C:\MyApps\myApp\myApp.pjx), is copied with its sub-folders to "/usr/usrapp/myApp" (FileClientBase.USER_APP_FOLDER). When the applicat...
  - async: `Task<string> UploadApplicationToControllerAsync(string localAppFolder, OnProgressDelegate progress = null, CancellationToken cancellationToken = default)`
- `void UploadBytesToController(byte[] data, string remotePath, bool createRemoteDir = false, OnProgressDelegate progress = null)`: Uploads data as a file to the controller. The file of the controller is replaced when it exists.
  - async: `Task UploadBytesToControllerAsync(byte[] data, string remotePath, bool createRemoteDir = false, OnProgressDelegate progress = null, CancellationToken cancellationToken = default)`
- `void UploadFileToController(string localPath, string remotePath, bool createRemoteDir = false, OnProgressDelegate progress = null)`: Uploads a local file to the controller. The file of the controller is replaced when it exists.
  - async: `Task UploadFileToControllerAsync(string localPath, string remotePath, bool createRemoteDir = false, OnProgressDelegate progress = null, CancellationToken cancellationToken = default)`
- `void UploadStreamToController(Stream stream, string remotePath, bool createRemoteDir = false, OnProgressDelegate progress = null)`: Uploads the content of a stream as a file to the controller, from the current position of the stream to its end. The file of the controller is replaced when it exists.
  - async: `Task UploadStreamToControllerAsync(Stream stream, string remotePath, bool createRemoteDir = false, OnProgressDelegate progress = null, CancellationToken cancellationToken = default)`

**FileClientBase** ([reference](../api/UnderAutomation.Staubli.Files.Internal.md#fileclientbase-controllerfile))

- `string ControllerFile { get; }`: Full path of the .controller file of the controller emulated by Staubli Robotics Suite. Null with a real controller.
- `string ControllerFolder { get; }`: Full path of the folder of the .controller file: root of the files of the emulated controller. Null with a real controller.
- `void CreateDirectory(string path)`: Creates a folder on the controller, with its parent folders when they do not exist. Nothing is done when the folder exists.
  - async: `Task CreateDirectoryAsync(string path, CancellationToken cancellationToken = default)`
- `void DeleteDirectory(string path)`: Deletes a folder of the controller and all its content
  - async: `Task DeleteDirectoryAsync(string path, CancellationToken cancellationToken = default)`
- `void DeleteFile(string path)`: Deletes a file of the controller
  - async: `Task DeleteFileAsync(string path, CancellationToken cancellationToken = default)`
- `bool DirectoryExists(string path)`: Checks if a folder exists on the controller
  - async: `Task<bool> DirectoryExistsAsync(string path, CancellationToken cancellationToken = default)`
- `void Disconnect()`: Disconnects the client
- `byte[] DownloadBytesFromController(string remotePath, OnProgressDelegate progress = null)`: Downloads a file of the controller and returns its content
  - async: `Task<byte[]> DownloadBytesFromControllerAsync(string remotePath, OnProgressDelegate progress = null, CancellationToken cancellationToken = default)`
- `void DownloadFileFromController(string localPath, string remotePath, OnProgressDelegate progress = null)`: Downloads a file of the controller to a local file. The local file is replaced when it exists, and its folder is created when it does not exist.
  - async: `Task DownloadFileFromControllerAsync(string localPath, string remotePath, OnProgressDelegate progress = null, CancellationToken cancellationToken = default)`
- `void DownloadStreamFromController(Stream stream, string remotePath, OnProgressDelegate progress = null)`: Downloads a file of the controller and writes its content to a stream
  - async: `Task DownloadStreamFromControllerAsync(Stream stream, string remotePath, OnProgressDelegate progress = null, CancellationToken cancellationToken = default)`
- `bool Enabled { get; }`: True when the client is connected
- `bool FileExists(string path)`: Checks if a file exists on the controller
  - async: `Task<bool> FileExistsAsync(string path, CancellationToken cancellationToken = default)`
- `FileItem GetFileInfo(string path)`: Gets information about a file or a folder of the controller
  - async: `Task<FileItem> GetFileInfoAsync(string path, CancellationToken cancellationToken = default)`
- `FileItem[] GetListing(string path)`: Lists the files and folders of a folder of the controller
  - async: `Task<FileItem[]> GetListingAsync(string path, CancellationToken cancellationToken = default)`
- `string Ip { get; }`: IP or host name of the controller. Null with an emulated controller.
- `bool IsSimulated { get; }`: True when the files are accessed in the folder of the .controller file of a controller emulated by Staubli Robotics Suite, false when they are accessed through FTP
- `int Port { get; }`: Port of the FTP server of the controller. 0 with an emulated controller.
- `void Rename(string path, string newPath)`: Renames or moves a file or a folder of the controller
  - async: `Task RenameAsync(string path, string newPath, CancellationToken cancellationToken = default)`
- `const string USER_APP_FOLDER = "/usr/usrapp"`: Folder of the VAL 3 applications on the controller. Each application is in a sub-folder named as the application (for example "/usr/usrapp/myApp/myApp.pjx"). The project path "Disk://myApp/myApp.pjx" of robot.Soap.LoadProject(...) is this file.
- `string UploadApplicationToController(string localAppFolder, OnProgressDelegate progress = null)`: Uploads a complete VAL 3 application to the controller. The local folder of the application, named as the application and with its project file inside (for example C:\MyApps\myApp\myApp.pjx), is copied with its sub-folders to "/usr/usrapp/myApp" (FileClientBase.USER_APP_FOLDER). When the applicat...
  - async: `Task<string> UploadApplicationToControllerAsync(string localAppFolder, OnProgressDelegate progress = null, CancellationToken cancellationToken = default)`
- `void UploadBytesToController(byte[] data, string remotePath, bool createRemoteDir = false, OnProgressDelegate progress = null)`: Uploads data as a file to the controller. The file of the controller is replaced when it exists.
  - async: `Task UploadBytesToControllerAsync(byte[] data, string remotePath, bool createRemoteDir = false, OnProgressDelegate progress = null, CancellationToken cancellationToken = default)`
- `void UploadFileToController(string localPath, string remotePath, bool createRemoteDir = false, OnProgressDelegate progress = null)`: Uploads a local file to the controller. The file of the controller is replaced when it exists.
  - async: `Task UploadFileToControllerAsync(string localPath, string remotePath, bool createRemoteDir = false, OnProgressDelegate progress = null, CancellationToken cancellationToken = default)`
- `void UploadStreamToController(Stream stream, string remotePath, bool createRemoteDir = false, OnProgressDelegate progress = null)`: Uploads the content of a stream as a file to the controller, from the current position of the stream to its end. The file of the controller is replaced when it exists.
  - async: `Task UploadStreamToControllerAsync(Stream stream, string remotePath, bool createRemoteDir = false, OnProgressDelegate progress = null, CancellationToken cancellationToken = default)`

**FileConnectParameters** ([reference](../api/UnderAutomation.Staubli.Common.md#fileconnectparameters))

- `FileConnectParameters()`
- `const int DEFAULT_PORT = 21`: Default port of the FTP server
- `const int DEFAULT_TIMEOUT_MS = 30000`: Default timeout of the FTP connection and of the transfers, in milliseconds
- `bool Enable { get; set; }`: Should use this service (default: false)
- Inherited from [FileConnectParametersBase](../api/UnderAutomation.Staubli.Files.Internal.md#fileconnectparametersbase): `User`, `Password`, `Port`, `TimeoutMs`

**FileConnectParametersBase** ([reference](../api/UnderAutomation.Staubli.Files.Internal.md#fileconnectparametersbase))

- `FileConnectParametersBase()`
- `string Password { get; set; }`: Password of the user (default: default). Not used with a controller emulated by Staubli Robotics Suite.
- `int Port { get; set; }`: Port of the FTP server of the controller (default: 21)
- `int TimeoutMs { get; set; }`: Timeout of the FTP connection and of the transfers, in milliseconds (default: 30000)
- `string User { get; set; }`: User of the FTP server of the controller (default: default). Not used with a controller emulated by Staubli Robotics Suite.

**FileException** ([reference](../api/UnderAutomation.Staubli.Files.md#fileexception))

- `string RemotePath { get; }`: Path of the file or folder on the controller concerned by the operation. Null when the operation has no path.
- `int ReplyCode { get; }`: FTP reply code returned by the controller (for example 550). 0 when the controller did not reply, and with an emulated controller.
- `string ReplyMessage { get; }`: Reply text returned by the controller. Null when the controller did not reply, and with an emulated controller.
