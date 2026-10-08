# List and transfer files

List the files of a Staubli controller, upload and download files, create, rename and delete files and folders, with synchronous and asynchronous methods.

Web page: https://underautomation.com/staubli/documentation/files-transfer

This page shows how to list, upload, download, rename and delete the files of a Staubli CS8 or CS9 controller from a PC, with `controller.File`. The same code works on a real controller (FTP) and on the emulator of Staubli Robotics Suite (folder of its `.controller` file): see [Files overview](files-overview.md) for the connection.

## List the files

`GetListing(path)` returns the files and folders of a folder. `GetFileInfo(path)` returns one item, or `null` when it does not exist.

```csharp
using UnderAutomation.Staubli;
using UnderAutomation.Staubli.Files;

public class FilesList
{
    static void Main()
    {
        var parameters = new ConnectionParameters("192.168.0.254");
        parameters.File.Enable = true;
        var controller = new StaubliController();
        controller.Connect(parameters);

        // Content of a folder of the controller
        foreach (FileItem item in controller.File.GetListing("/usr/usrapp"))
            Console.WriteLine($"{item.FullName} {item.Type} {item.Size} bytes {item.Modified}");

        // One file or folder, null when it does not exist
        FileItem project = controller.File.GetFileInfo("/usr/usrapp/myApp/myApp.pjx");

        bool fileExists = controller.File.FileExists("/usr/usrapp/myApp/myApp.pjx");
        bool folderExists = controller.File.DirectoryExists("/usr/usrapp/myApp");

        controller.Disconnect();
    }
}
```

| Property   | Meaning                                                                |
| ---------- | ---------------------------------------------------------------------- |
| `Name`     | Name, without the path                                                 |
| `FullName` | Full path on the controller, for example `/usr/usrapp/myApp/myApp.pjx` |
| `Type`     | `FileItemType.File` or `FileItemType.Directory`                        |
| `Size`     | Size in bytes, `0` for a folder                                        |
| `Modified` | Date of the last change. With the emulator, local time of the PC       |

## Upload and download

```csharp
using System.Text;
using UnderAutomation.Staubli;

public class FilesTransfer
{
    static void Main()
    {
        var parameters = new ConnectionParameters("192.168.0.254");
        parameters.File.Enable = true;
        var controller = new StaubliController();
        controller.Connect(parameters);

        // Upload a local file. createRemoteDir: true creates the folder on the controller when it does not exist.
        controller.File.UploadFileToController(@"C:\Data\points.dat", "/usr/usrapp/myApp/points.dat", true,
            progress => Console.WriteLine($"{progress:0}%"));

        // Upload bytes
        controller.File.UploadBytesToController(Encoding.ASCII.GetBytes("1;2;3"), "/usr/usrapp/myApp/data.txt");

        // Download to a local file (replaced when it exists)
        controller.File.DownloadFileFromController(@"C:\Backup\myApp.pjx", "/usr/usrapp/myApp/myApp.pjx");

        // Download the content
        byte[] content = controller.File.DownloadBytesFromController("/usr/usrapp/myApp/data.txt");
        Console.WriteLine(Encoding.ASCII.GetString(content));

        controller.Disconnect();
    }
}
```

### Upload

- `UploadFileToController(localPath, remotePath)` sends a local file.
- `UploadBytesToController(data, remotePath)` and `UploadStreamToController(stream, remotePath)` send data from memory or a stream.
- The file of the controller is replaced when it exists. With `createRemoteDir` set to `true`, its folder is created when it does not exist.

### Download

- `DownloadFileFromController(localPath, remotePath)` writes a local file. The local file is replaced, and its folder is created.
- `DownloadBytesFromController(remotePath)` returns the content, `DownloadStreamFromController(stream, remotePath)` writes it to a stream.
- A file that does not exist on the controller throws a `FileException`. No local file is created.

The optional `progress` argument receives the percentage of the transfer, from 0 to 100.

## Folders, rename and delete

```csharp
using UnderAutomation.Staubli;

public class FilesManage
{
    static void Main()
    {
        var parameters = new ConnectionParameters("192.168.0.254");
        parameters.File.Enable = true;
        var controller = new StaubliController();
        controller.Connect(parameters);

        // Create a folder, with its parent folders
        controller.File.CreateDirectory("/usr/usrapp/myApp/backup");

        // Rename or move a file or a folder
        controller.File.Rename("/usr/usrapp/myApp/data.txt", "/usr/usrapp/myApp/backup/data.txt");

        // Delete a file
        controller.File.DeleteFile("/usr/usrapp/myApp/backup/data.txt");

        // Delete a folder and all its content
        controller.File.DeleteDirectory("/usr/usrapp/myApp/backup");

        controller.Disconnect();
    }
}
```

- `CreateDirectory` creates the parent folders too. Nothing is done when the folder exists.
- `Rename` renames or moves a file or a folder.
- `DeleteFile` and `DeleteDirectory` throw a `FileException` when the item does not exist. `DeleteDirectory` deletes all the content.

To send a complete VAL 3 application, see [Send a VAL 3 application](files-applications.md).

## Asynchronous methods

Each method has an asynchronous version, with an optional `CancellationToken`: `GetListingAsync`, `UploadFileToControllerAsync`, `DownloadBytesFromControllerAsync`... They are not available on .NET Framework 3.5 and 4.0.

```csharp
using UnderAutomation.Staubli;
using UnderAutomation.Staubli.Files;

public class FilesAsync
{
    static async Task Main()
    {
        var parameters = new ConnectionParameters("192.168.0.254");
        parameters.File.Enable = true;
        var controller = new StaubliController();
        controller.Connect(parameters);

        using var cancellation = new CancellationTokenSource(TimeSpan.FromMinutes(1));

        FileItem[] items = await controller.File.GetListingAsync("/usr/usrapp", cancellation.Token);

        await controller.File.UploadFileToControllerAsync(@"C:\Data\points.dat", "/usr/usrapp/myApp/points.dat",
            cancellationToken: cancellation.Token);

        byte[] content = await controller.File.DownloadBytesFromControllerAsync("/usr/usrapp/myApp/points.dat",
            cancellationToken: cancellation.Token);

        controller.Disconnect();
    }
}
```

## Reference

**FileItem** ([reference](../api/UnderAutomation.Staubli.Files.md#fileitem))

- `string FullName { get; }`: Full path of the file or folder on the controller (for example "/usr/usrapp/myApp/myApp.pjx")
- `DateTime Modified { get; }`: Date and time of the last modification, as given by the controller. With a controller emulated by Staubli Robotics Suite, local time of the computer.
- `string Name { get; }`: Name of the file or folder, without its path (for example "myApp.pjx")
- `long Size { get; }`: Size of the file in bytes. 0 for a folder, and 0 when the controller does not give the size.
- `FileItemType Type { get; }`: File or folder

**FileItemType** ([reference](../api/UnderAutomation.Staubli.Files.md#fileitemtype))

- Directory: A folder
- File: A file
