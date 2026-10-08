# UnderAutomation.Yaskawa.Ftp.Internal

## FtpClientBase (robot.Ftp)

`abstract class FtpClientBase : IFileManager, IFileReader, IFileWriter, IYaskawaClient`

Abstract base class that implements FTP communication with a Yaskawa robot controller. Provides file management (upload, download, list, delete) via the controller's FTP server.

- `string Address { get; }`: Gets the address of the robot controller: an IP address or a host name.
- `void Close()`: Closes the connection to the robot controller and releases resources.
- `bool Connected { get; }`: Gets a value indicating whether the client is connected to a robot controller.
- `void DeleteFile(string fileName)`: Deletes a file from the robot controller. The "anonymous" user cannot delete files.
  - async: `Task DeleteFileAsync(string fileName, CancellationToken cancellationToken = default)`
- `bool DirectoryExists(string path)`: Checks whether a folder exists on the controller.
  - async: `Task<bool> DirectoryExistsAsync(string path, CancellationToken cancellationToken = default)`
- `byte[] DownloadFile(string remotePath, OnProgressDelegate progress = null)`: Downloads a file from the controller and returns its content.
  - async: `Task<byte[]> DownloadFileAsync(string remotePath, OnProgressDelegate progress = null, CancellationToken cancellationToken = default)`
- `void DownloadFileToLocal(string remotePath, string localPath, OnProgressDelegate progress = null)`: Downloads a file from the controller and saves it on the local file system. Overwrites the local file if it already exists. The local file is not created if the download fails.
  - async: `Task DownloadFileToLocalAsync(string remotePath, string localPath, OnProgressDelegate progress = null, CancellationToken cancellationToken = default)`
- `void DownloadFileToStream(string remotePath, Stream destination, OnProgressDelegate progress = null)`: Downloads a file from the controller and writes its content into a stream.
  - async: `Task DownloadFileToStreamAsync(string remotePath, Stream destination, OnProgressDelegate progress = null, CancellationToken cancellationToken = default)`
- `string[] DownloadFilesToLocal(string[] remotePaths, string localFolder, OnProgressDelegate progress = null)`: Downloads several files from the controller into a local folder. Each file is saved with its name, and existing local files are overwritten.
  - async: `Task<string[]> DownloadFilesToLocalAsync(string[] remotePaths, string localFolder, OnProgressDelegate progress = null, CancellationToken cancellationToken = default)`
- `bool FileExists(string remotePath)`: Checks whether a file exists on the controller.
  - async: `Task<bool> FileExistsAsync(string remotePath, CancellationToken cancellationToken = default)`
- `string GetFile(string fileName)`: Downloads a text file from the robot controller and returns its content.
  - async: `Task<string> GetFileAsync(string fileName, CancellationToken cancellationToken = default)`
- `string[] GetFileList(FileExtension fileExtension)`: Lists the files of the specified type on the controller.
  - async: `Task<string[]> GetFileListAsync(FileExtension fileExtension, CancellationToken cancellationToken = default)`
- `string[] GetFileListByPattern(string pattern)`: Lists the files whose names match the specified pattern. When the pattern has a known extension (e.g. "*.JBI"), only the matching folder is listed. Otherwise, all folders of the controller are listed.
  - async: `Task<string[]> GetFileListByPatternAsync(string pattern, CancellationToken cancellationToken = default)`
- `FtpListItem[] GetListing(string path)`: Returns the files and folders at the specified path on the controller. The root contains one folder per file type (JOB, DAT, CND, SYS, PRM, LST, CSV, LOG, TXT).
  - async: `Task<FtpListItem[]> GetListingAsync(string path, CancellationToken cancellationToken = default)`
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
- `string User { get; }`: FTP user name used for the current connection.

## FtpClientInternal (robot.Ftp)

`class FtpClientInternal : FtpClientBase, IFileManager, IFileReader, IFileWriter, IYaskawaClient`

Internal implementation of the FTP client. This class is not intended for direct use by application code. Use Yaskawa.YaskawaRobot instead.

- Inherited from [FtpClientBase](UnderAutomation.Yaskawa.Ftp.Internal.md#ftpclientbase-robotftp): `Close`, `GetFile`, `GetFileList`, `GetFileListByPattern`, `GetFileAsync`, `GetFileListAsync`, `GetFileListByPatternAsync`, `LoadFile`, `DeleteFile`, `LoadFileAsync`, `DeleteFileAsync`, `UploadFile`, `UploadFileFromStream`, `UploadFileFromLocal`, `UploadFilesFromLocal`, `UploadFileAsync`, `UploadFileFromStreamAsync`, `UploadFileFromLocalAsync`, `UploadFilesFromLocalAsync`, `DownloadFile`, `DownloadFileToStream`, `DownloadFileToLocal`, `DownloadFilesToLocal`, `DownloadFileAsync`, `DownloadFileToStreamAsync`, `DownloadFileToLocalAsync`, `DownloadFilesToLocalAsync`, `FileExists`, `DirectoryExists`, `FileExistsAsync`, `DirectoryExistsAsync`, `GetListing`, `GetListingAsync`, `Address`, `Connected`, `User`

## FtpConnectParametersInternal

`class FtpConnectParametersInternal : FtpConnectParameters`

FTP connection parameters with an enable flag, used by Yaskawa.ConnectParameters.

- `FtpConnectParametersInternal()`
- `bool Enable { get; set; }`: Gets or sets a value indicating whether to establish an FTP connection when calling Yaskawa.ConnectParameters). Default: false.
- Inherited from [FtpConnectParameters](UnderAutomation.Yaskawa.Ftp.md#ftpconnectparameters): `DEFAULT_PORT`, `DEFAULT_TIMEOUT_MILLISECONDS`, `FtpUser`, `FtpPassword`, `Port`, `TimeoutMilliseconds`
