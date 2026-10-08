# UnderAutomation.Staubli.Files.Internal

## FileClientBase (controller.File)

`abstract class FileClientBase`

Upload, download, listing and management of the files of the controller. With a real controller, the files are accessed through the FTP server of the controller. With a controller emulated by Staubli Robotics Suite, there is no FTP server: give the path of its .controller file as address. The fil...

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

## FileClientInternal (controller.File)

`class FileClientInternal : FileClientBase`

File client of Staubli.StaubliController, connected by Staubli.ConnectionParameters)

- Inherited from [FileClientBase](UnderAutomation.Staubli.Files.Internal.md#fileclientbase-controllerfile): `USER_APP_FOLDER`, `Disconnect`, `GetListing`, `GetFileInfo`, `FileExists`, `DirectoryExists`, `CreateDirectory`, `DeleteFile`, `DeleteDirectory`, `Rename`, `GetListingAsync`, `GetFileInfoAsync`, `FileExistsAsync`, `DirectoryExistsAsync`, `CreateDirectoryAsync`, `DeleteFileAsync`, `DeleteDirectoryAsync`, `RenameAsync`, `UploadFileToController`, `UploadBytesToController`, `UploadStreamToController`, `UploadFileToControllerAsync`, `UploadBytesToControllerAsync`, `UploadStreamToControllerAsync`, `UploadApplicationToController`, `UploadApplicationToControllerAsync`, `DownloadFileFromController`, `DownloadBytesFromController`, `DownloadStreamFromController`, `DownloadFileFromControllerAsync`, `DownloadBytesFromControllerAsync`, `DownloadStreamFromControllerAsync`, `Ip`, `Port`, `ControllerFile`, `ControllerFolder`, `IsSimulated`, `Enabled`

## FileConnectParametersBase

`class FileConnectParametersBase`

Base class for the connection parameters of the file client

- `FileConnectParametersBase()`
- `string Password { get; set; }`: Password of the user (default: default). Not used with a controller emulated by Staubli Robotics Suite.
- `int Port { get; set; }`: Port of the FTP server of the controller (default: 21)
- `int TimeoutMs { get; set; }`: Timeout of the FTP connection and of the transfers, in milliseconds (default: 30000)
- `string User { get; set; }`: User of the FTP server of the controller (default: default). Not used with a controller emulated by Staubli Robotics Suite.
