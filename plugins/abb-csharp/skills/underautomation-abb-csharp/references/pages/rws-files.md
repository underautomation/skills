# File system

Browse the controller file system, download and upload files, create, copy, rename and delete files and directories.

Web page: https://underautomation.com/abb/documentation/rws-files

`robot.Rws.File` gives access to the file system of the controller: browse it, download and upload files, and create, rename, copy or delete files and directories. Nothing has to be shared or mounted on the PC.

Paths are the ones used on the controller. The environment variables of the controller are accepted where a path is expected, `$home` and `$temp` for example, and they behave as directories. `robot.Rws.Controller.GetEnvironmentVariable` gives the real path behind such a name.

## Browse the file system

`ListDirectory` returns a `DirectoryListing` with the files, the subdirectories and, at the root, the storage devices of the controller. The complete content is always returned, however many entries the directory holds.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class FileList
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // The root lists the storage devices of the controller
        DirectoryListing root = robot.Rws.File.ListDirectory("/");

        foreach (DeviceItem device in root.Devices)
        {
            Console.WriteLine($"{device.Name} ({device.DeviceType}) {device.FreeSpace}/{device.TotalSpace} bytes");
        }

        // A directory lists its files and its subdirectories
        DirectoryListing listing = robot.Rws.File.ListDirectory("$home");
        Console.WriteLine($"{listing.DirectoryCount} directories, {listing.FileCount} files");

        foreach (DirectoryItem directory in listing.Directories)
        {
            Console.WriteLine($"[DIR] {directory.Name}");
        }

        foreach (FileItem file in listing.Files)
        {
            Console.WriteLine($"{file.Name} {file.Size} bytes, modified {file.ModificationDate}");
        }

        robot.Disconnect();
    }
}
```

Pass `"/"` or null to list the root. The root is where the storage devices are, with their free and total space. A `DeviceItem` has a `DeviceType`: `Fixed` for an internal disk, `Removable` for a USB key, `RamDisk`, `Remote` for a network storage, `Unknown` otherwise.

`FileCount`, `DirectoryCount`, `DeviceCount` and `TotalCount` are computed by the SDK, they save a null check on the three arrays.

## One class per kind of item

`FileItem`, `DirectoryItem` and `DeviceItem` all derive from `FileSystemItem`, which carries the name and the dates. There is no flag saying what an item is, the type itself says it.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class FileSystemItems
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        DirectoryListing listing = robot.Rws.File.ListDirectory("/");

        // The three arrays hold subclasses of the same base class
        List<FileSystemItem> items = new List<FileSystemItem>();
        items.AddRange(listing.Directories);
        items.AddRange(listing.Files);
        items.AddRange(listing.Devices);

        foreach (FileSystemItem item in items)
        {
            // Name, CreationDate and ModificationDate come from the base class
            Console.Write($"{item.Name} {item.ModificationDate} ");

            // What the item really is, is found with a type test, not with a flag
            if (item is FileItem file)
            {
                Console.WriteLine($"file of {file.Size} bytes");
            }
            else if (item is DirectoryItem directory)
            {
                Console.WriteLine($"directory, read only: {directory.IsReadOnly}");
            }
            else if (item is DeviceItem device)
            {
                Console.WriteLine($"device of type {device.DeviceType}, {device.FreeSpace} bytes free");
            }
        }

        robot.Disconnect();
    }
}
```

`CreationDate` and `ModificationDate` are nullable, the controller does not always report them. `Size` is in bytes and only exists on a file.

## Download a file

Four methods read a file, they differ only by what you get back.

| Method                                  | Returns                                   |
| --------------------------------------- | ----------------------------------------- |
| `GetFileAsText(path, encoding)`         | `string`, UTF-8 when no encoding is given |
| `GetFileAsBytes(path)`                  | `byte[]`                                  |
| `GetFileToDestination(path, localPath)` | Nothing, the file is written on the PC    |
| `GetFileAsReadonlyStream(path)`         | A readable `Stream`                       |

```csharp
using System.Text;
using UnderAutomation.ABB;

public class FileDownload
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // A text file, UTF-8 by default
        string text = robot.Rws.File.GetFileAsText("$home/notes.txt");

        // Another encoding when the file is not UTF-8
        string latin = robot.Rws.File.GetFileAsText("$home/notes.txt", Encoding.GetEncoding("iso-8859-1"));

        // A binary file
        byte[] bytes = robot.Rws.File.GetFileAsBytes("$home/backup.zip");

        // Straight to a file of the PC
        robot.Rws.File.GetFileToDestination("$home/backup.zip", @"C:\temp\backup.zip");

        // As a stream, to copy the content without keeping a second copy of it
        using (Stream source = robot.Rws.File.GetFileAsReadonlyStream("$home/backup.zip"))
        using (FileStream destination = System.IO.File.Create(@"C:\temp\backup.zip"))
        {
            source.CopyTo(destination);
        }

        robot.Disconnect();
    }
}
```

Use `GetFileAsText` for a RAPID module, a configuration file or a log. Use the bytes or the stream for a backup archive or any binary content. The synchronous `GetFileAsReadonlyStream` buffers the whole content in memory first, for compatibility with .NET Framework 3.5 and 4.0. `GetFileAsReadonlyStreamAsync` reads from the network as you read the stream, which is the one to use for a large file.

## Upload a file

The four upload methods mirror the downloads. An existing file is replaced.

```csharp
using UnderAutomation.ABB;

public class FileUpload
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // From a string, UTF-8 by default
        robot.Rws.File.UploadFileFromText("$home/notes.txt", "Written by the SDK");

        // From raw bytes
        robot.Rws.File.UploadFileFromBytes("$home/data.bin", new byte[] { 1, 2, 3, 4 });

        // From a file of the PC
        robot.Rws.File.UploadFileFromPath("$home/MyModule.mod", @"C:\temp\MyModule.mod");

        // From a stream, for a large file
        using (FileStream source = System.IO.File.OpenRead(@"C:\temp\MyModule.mod"))
        {
            robot.Rws.File.UploadFileFromStream("$home/MyModule.mod", source);
        }

        robot.Disconnect();
    }
}
```

`UploadFileFromText` writes UTF-8 by default, pass an `Encoding` for another one. `UploadFileFromStream` sends the content as it reads it, so a large file does not have to be loaded in memory.

Create the destination directory first with `CreateDirectory` when it does not exist yet.

## Create, rename, copy and delete

```csharp
using UnderAutomation.ABB;

public class FileManage
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // Directories. The new name can be nested, the missing levels are created.
        robot.Rws.File.CreateDirectory("$home", "MyApp/Logs");
        robot.Rws.File.RenameDirectory("$home/MyApp/Logs", "Archive");
        robot.Rws.File.CopyDirectory("$home/MyApp/Archive", "Archive2", true);
        robot.Rws.File.DeleteDirectory("$home/MyApp/Archive2");

        // Files. The third argument of the copy overwrites an existing target.
        robot.Rws.File.RenameFile("$home/notes.txt", "notes-old.txt");
        robot.Rws.File.CopyFile("$home/notes-old.txt", "notes-backup.txt", true);
        robot.Rws.File.DeleteFile("$home/notes-old.txt");

        robot.Disconnect();
    }
}
```

A few points to know:

- `CreateDirectory` takes the parent directory and the new name. The name can be nested, and the missing levels are created.
- The new name of a rename or a copy is relative to the directory the item is in. An absolute path on the controller is also accepted.
- The copy methods take an `overwrite` argument. With `false`, the controller refuses to replace an existing target.
- `DeleteDirectory` deletes the directory and its content. There is no recycle bin on the controller, a deleted file is gone.

The controller protects part of its file system. A write in a read only location fails with an `RwsException`, and `IsReadOnly` on the item tells you before you try. The user account also needs the matching UAS grant.

## Around the file system

Other services write files on the controller and leave them for this one to read:

- [Controller](rws-controller.md) writes a backup in a folder of the controller. Browse that folder and download its files, as shown in [Backup & restore a controller](backup-restore-controller.md).
- [Event log](rws-elog.md) writes the whole log to one file with `SaveInSystemDumpFormat`.
- [RAPID modules](rws-rapid-modules.md) loads a module from a path on the controller, so a module written from the PC is uploaded first and loaded afterwards.

Nothing here needs the [mastership](rws-mastership.md), the file system is not one of its domains. Loading into RAPID what you uploaded does need it.

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## API reference

**Methods of FileService** ([reference](../api/UnderAutomation.ABB.Rws.Services.md#fileservice-robotrwsfile))

- `void CopyDirectory(string path, string newName, bool overwrite)`: Copies a directory (synchronous)
  - async: `Task CopyDirectoryAsync(string path, string newName, bool overwrite, CancellationToken cancellationToken = default)`
- `void CopyFile(string path, string newName, bool overwrite)`: Copies a file (synchronous)
  - async: `Task CopyFileAsync(string path, string newName, bool overwrite, CancellationToken cancellationToken = default)`
- `void CreateDirectory(string path, string newName)`: Creates a new directory (synchronous) The newName parameter can contain nested directory structure (e.g. "parentdir/subdir") which will create both directories if they don't exist.
  - async: `Task CreateDirectoryAsync(string path, string newName, CancellationToken cancellationToken = default)`
- `void DeleteDirectory(string path)`: Deletes a directory and all its subdirectories and files (synchronous)
  - async: `Task DeleteDirectoryAsync(string path, CancellationToken cancellationToken = default)`
- `void DeleteFile(string path)`: Deletes a file (synchronous)
  - async: `Task DeleteFileAsync(string path, CancellationToken cancellationToken = default)`
- `byte[] GetFileAsBytes(string path)`: Gets file content as raw bytes (synchronous)
  - async: `Task<byte[]> GetFileAsBytesAsync(string path, CancellationToken cancellationToken = default)`
- `Stream GetFileAsReadonlyStream(string path)`: Gets file content as a read-only stream (synchronous) For sync: Returns a read-only MemoryStream (buffered for .NET 3.5/4.0 compatibility) For true HTTP streaming with large files, use GetFileAsReadonlyStreamAsync() instead
  - async: `Task<Stream> GetFileAsReadonlyStreamAsync(string path, CancellationToken cancellationToken = default)`
- `string GetFileAsText(string path, Encoding encoding = null)`: Gets file content as text (synchronous)
  - async: `Task<string> GetFileAsTextAsync(string path, Encoding encoding = null, CancellationToken cancellationToken = default)`
- `void GetFileToDestination(string path, string localPath)`: Downloads a file to a local path (synchronous)
  - async: `Task GetFileToDestinationAsync(string path, string localPath, CancellationToken cancellationToken = default)`
- `DirectoryListing ListDirectory(string path)`: Lists contents of a directory resource (synchronous) Environment variables (e.g. $home, $temp) and devices are treated as directories. When listing the root path ("/", null, or "\\"), the response includes available devices in DirectoryListing.Devices. The complete content is always returned, how...
  - async: `Task<DirectoryListing> ListDirectoryAsync(string path, CancellationToken cancellationToken = default)`
- `void RenameDirectory(string path, string newName)`: Renames a directory (synchronous)
  - async: `Task RenameDirectoryAsync(string path, string newName, CancellationToken cancellationToken = default)`
- `void RenameFile(string path, string newName)`: Renames a file (synchronous)
  - async: `Task RenameFileAsync(string path, string newName, CancellationToken cancellationToken = default)`
- `void UploadFileFromBytes(string path, byte[] content, string contentType = null)`: Uploads a file from raw bytes (synchronous)
  - async: `Task UploadFileFromBytesAsync(string path, byte[] content, string contentType = null, CancellationToken cancellationToken = default)`
- `void UploadFileFromPath(string path, string localPath, string contentType = null)`: Uploads a local file to the controller (synchronous)
  - async: `Task UploadFileFromPathAsync(string path, string localPath, string contentType = null, CancellationToken cancellationToken = default)`
- `void UploadFileFromStream(string path, Stream contentStream, string contentType = null)`: Uploads a file from a stream (synchronous)
  - async: `Task UploadFileFromStreamAsync(string path, Stream contentStream, string contentType = null, CancellationToken cancellationToken = default)`
- `void UploadFileFromText(string path, string content, Encoding encoding = null)`: Uploads a file from text (synchronous)
  - async: `Task UploadFileFromTextAsync(string path, string content, Encoding encoding = null, CancellationToken cancellationToken = default)`

**DirectoryListing** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#directorylisting))

- `DirectoryListing(string path)`: Initializes a new instance of the Data.DirectoryListing class
- `int DeviceCount { get; }`: Number of devices in this listing
- `DeviceItem[] Devices { get; set; }`: Devices available in this listing (typically only present at root "/")
- `DirectoryItem[] Directories { get; set; }`: Subdirectories contained in this directory
- `int DirectoryCount { get; }`: Number of subdirectories in this listing
- `int FileCount { get; }`: Number of files in this listing
- `FileItem[] Files { get; set; }`: Files contained in this directory
- `string Path { get; }`: Path that was listed
- `int TotalCount { get; }`: Total number of items (files + directories + devices)

**FileSystemItem** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#filesystemitem))

- `DateTime? CreationDate { get; set; }`: Creation date of the resource, if available
- `DateTime? ModificationDate { get; set; }`: Last modification date of the resource, if available
- `string Name { get; set; }`: Name of the item (file name, directory name, or device name such as "C:")

**FileItem** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#fileitem))

- `FileItem()`: Initializes a new instance of the Data.FileItem class
- `bool IsReadOnly { get; set; }`: Indicates if the file is read-only
- `long Size { get; set; }`: File size in bytes
- Inherited from [FileSystemItem](../api/UnderAutomation.ABB.Rws.Data.md#filesystemitem): `Name`, `CreationDate`, `ModificationDate`

**DirectoryItem** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#directoryitem))

- `DirectoryItem()`: Initializes a new instance of the Data.DirectoryItem class
- `bool IsReadOnly { get; set; }`: Indicates if the directory is read-only
- Inherited from [FileSystemItem](../api/UnderAutomation.ABB.Rws.Data.md#filesystemitem): `Name`, `CreationDate`, `ModificationDate`

**DeviceItem** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#deviceitem))

- `DeviceItem()`: Initializes a new instance of the Data.DeviceItem class
- `DeviceType DeviceType { get; set; }`: Type of device (Fixed, Removable, RamDisk, Remote)
- `long FreeSpace { get; set; }`: Free storage space in bytes
- `bool IsEnabled { get; set; }`: Indicates if the device is enabled
- `bool IsReadOnly { get; set; }`: Indicates if the device is read-only
- `long TotalSpace { get; set; }`: Total storage space in bytes
- Inherited from [FileSystemItem](../api/UnderAutomation.ABB.Rws.Data.md#filesystemitem): `Name`, `CreationDate`, `ModificationDate`

**DeviceType** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#devicetype))

- Fixed: Fixed storage device (hard drive)
- RamDisk: RAM disk
- Remote: Remote or network storage
- Removable: Removable storage device (USB, SD card, etc.)
- Unknown: Unknown device type
