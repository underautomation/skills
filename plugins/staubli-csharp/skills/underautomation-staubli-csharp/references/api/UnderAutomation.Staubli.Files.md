# UnderAutomation.Staubli.Files

## FileClient

`class FileClient : FileClientBase`

Standalone client for the files of a Staubli controller: upload, download, listing and management. With a real controller, the files are accessed through the FTP server of the controller. With a controller emulated by Staubli Robotics Suite, they are accessed in the folder of its .controller file.

- `FileClient()`: Create a new instance of FileClient
- `void Connect(string address, string user, string password, int port = 21, int timeoutMs = 30000)`: Connect to a controller
  - async: `Task ConnectAsync(string address, string user, string password, int port = 21, int timeoutMs = 30000, CancellationToken cancellationToken = default)`
- Inherited from [FileClientBase](UnderAutomation.Staubli.Files.Internal.md#fileclientbase-controllerfile): `USER_APP_FOLDER`, `Disconnect`, `GetListing`, `GetFileInfo`, `FileExists`, `DirectoryExists`, `CreateDirectory`, `DeleteFile`, `DeleteDirectory`, `Rename`, `GetListingAsync`, `GetFileInfoAsync`, `FileExistsAsync`, `DirectoryExistsAsync`, `CreateDirectoryAsync`, `DeleteFileAsync`, `DeleteDirectoryAsync`, `RenameAsync`, `UploadFileToController`, `UploadBytesToController`, `UploadStreamToController`, `UploadFileToControllerAsync`, `UploadBytesToControllerAsync`, `UploadStreamToControllerAsync`, `UploadApplicationToController`, `UploadApplicationToControllerAsync`, `DownloadFileFromController`, `DownloadBytesFromController`, `DownloadStreamFromController`, `DownloadFileFromControllerAsync`, `DownloadBytesFromControllerAsync`, `DownloadStreamFromControllerAsync`, `Ip`, `Port`, `ControllerFile`, `ControllerFolder`, `IsSimulated`, `Enabled`

## FileException

`class FileException : Exception, ISerializable`

Exception thrown when an operation on the files of the controller fails: the controller refused it, the file does not exist, or the communication failed. The message gives the reason and, when it is known, what to do.

- `string RemotePath { get; }`: Path of the file or folder on the controller concerned by the operation. Null when the operation has no path.
- `int ReplyCode { get; }`: FTP reply code returned by the controller (for example 550). 0 when the controller did not reply, and with an emulated controller.
- `string ReplyMessage { get; }`: Reply text returned by the controller. Null when the controller did not reply, and with an emulated controller.

## FileItem

`class FileItem`

A file or a folder of the controller

- `string FullName { get; }`: Full path of the file or folder on the controller (for example "/usr/usrapp/myApp/myApp.pjx")
- `DateTime Modified { get; }`: Date and time of the last modification, as given by the controller. With a controller emulated by Staubli Robotics Suite, local time of the computer.
- `string Name { get; }`: Name of the file or folder, without its path (for example "myApp.pjx")
- `long Size { get; }`: Size of the file in bytes. 0 for a folder, and 0 when the controller does not give the size.
- `FileItemType Type { get; }`: File or folder

## FileItemType

`enum FileItemType`

Type of an item of the controller file system

- Directory: A folder
- File: A file

## OnProgressDelegate

`delegate void OnProgressDelegate(double progress)`

Reports the progress of a file transfer

- `OnProgressDelegate(object @object, nint method)`
- `IAsyncResult BeginInvoke(double progress, AsyncCallback callback, object @object)`
- `void EndInvoke(IAsyncResult result)`
- `void Invoke(double progress)`
