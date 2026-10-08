# File system

Browse the controller file system, download and upload files, create, copy, rename and delete files and directories.

Web page: https://underautomation.com/abb/documentation/rws-files

`robot.Rws.File` gives access to the file system of the controller: browse it, download and upload files, and create, rename, copy or delete files and directories. Nothing has to be shared or mounted on the PC.

Paths are the ones used on the controller. The environment variables of the controller are accepted where a path is expected, `$home` and `$temp` for example, and they behave as directories. `robot.Rws.Controller.GetEnvironmentVariable` gives the real path behind such a name.

## Browse the file system

`ListDirectory` returns a `DirectoryListing` with the files, the subdirectories and, at the root, the storage devices of the controller. The complete content is always returned, however many entries the directory holds.

```python
from underautomation.abb.abb_controller import AbbController

robot = AbbController()
robot.connect("192.168.0.1")

# The root lists the storage devices of the controller
root = robot.rws.file.list_directory("/")

for device in root.devices:
    print(f"{device.name} ({device.device_type}) {device.free_space}/{device.total_space} bytes")

# A directory lists its files and its subdirectories
listing = robot.rws.file.list_directory("$home")
print(f"{listing.directory_count} directories, {listing.file_count} files")

for directory in listing.directories:
    print(f"[DIR] {directory.name}")

for file in listing.files:
    print(f"{file.name} {file.size} bytes, modified {file.modification_date}")

robot.disconnect()
```

Pass `"/"` or null to list the root. The root is where the storage devices are, with their free and total space. A `DeviceItem` has a `DeviceType`: `Fixed` for an internal disk, `Removable` for a USB key, `RamDisk`, `Remote` for a network storage, `Unknown` otherwise.

`FileCount`, `DirectoryCount`, `DeviceCount` and `TotalCount` are computed by the SDK, they save a null check on the three arrays.

## One class per kind of item

`FileItem`, `DirectoryItem` and `DeviceItem` all derive from `FileSystemItem`, which carries the name and the dates. There is no flag saying what an item is, the type itself says it.

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.device_item import DeviceItem
from underautomation.abb.rws.data.directory_item import DirectoryItem
from underautomation.abb.rws.data.file_item import FileItem

robot = AbbController()
robot.connect("192.168.0.1")

listing = robot.rws.file.list_directory("/")

# The three lists hold subclasses of the same base class
items = list(listing.directories) + list(listing.files) + list(listing.devices)

for item in items:
    # name, creation_date and modification_date come from the base class
    line = f"{item.name} {item.modification_date} "

    # What the item really is, is found with a type test, not with a flag
    if isinstance(item, FileItem):
        line += f"file of {item.size} bytes"
    elif isinstance(item, DirectoryItem):
        line += f"directory, read only: {item.is_read_only}"
    elif isinstance(item, DeviceItem):
        line += f"device of type {item.device_type}, {item.free_space} bytes free"

    print(line)

robot.disconnect()
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

```python
from underautomation.abb.abb_controller import AbbController

robot = AbbController()
robot.connect("192.168.0.1")

# A binary file, as a list of bytes
data = robot.rws.file.get_file_as_bytes("$home/backup.zip")

# A text file, decoded by your code. UTF-8 is the usual encoding.
text = bytes(robot.rws.file.get_file_as_bytes("$home/notes.txt")).decode("utf-8")

# Another encoding when the file is not UTF-8
latin = bytes(robot.rws.file.get_file_as_bytes("$home/notes.txt")).decode("iso-8859-1")

# Straight to a file of the PC, without keeping the content in memory
robot.rws.file.get_file_to_destination("$home/backup.zip", r"C:\temp\backup.zip")

robot.disconnect()
```

Use `GetFileAsText` for a RAPID module, a configuration file or a log. Use the bytes or the stream for a backup archive or any binary content. The synchronous `GetFileAsReadonlyStream` buffers the whole content in memory first, for compatibility with .NET Framework 3.5 and 4.0. `GetFileAsReadonlyStreamAsync` reads from the network as you read the stream, which is the one to use for a large file.

## Upload a file

The four upload methods mirror the downloads. An existing file is replaced.

```python
from underautomation.abb.abb_controller import AbbController

robot = AbbController()
robot.connect("192.168.0.1")

# From a string, encoded by your code. UTF-8 is the usual encoding.
robot.rws.file.upload_file_from_bytes("$home/notes.txt", "Written by the SDK".encode("utf-8"))

# From raw bytes
robot.rws.file.upload_file_from_bytes("$home/data.bin", bytes([1, 2, 3, 4]))

# From a file of the PC, for a large file
robot.rws.file.upload_file_from_path("$home/MyModule.mod", r"C:\temp\MyModule.mod")

robot.disconnect()
```

`UploadFileFromText` writes UTF-8 by default, pass an `Encoding` for another one. `UploadFileFromStream` sends the content as it reads it, so a large file does not have to be loaded in memory.

Create the destination directory first with `CreateDirectory` when it does not exist yet.

## Create, rename, copy and delete

```python
from underautomation.abb.abb_controller import AbbController

robot = AbbController()
robot.connect("192.168.0.1")

# Directories. The new name can be nested, the missing levels are created.
robot.rws.file.create_directory("$home", "MyApp/Logs")
robot.rws.file.rename_directory("$home/MyApp/Logs", "Archive")
robot.rws.file.copy_directory("$home/MyApp/Archive", "Archive2", True)
robot.rws.file.delete_directory("$home/MyApp/Archive2")

# Files. The third argument of the copy overwrites an existing target.
robot.rws.file.rename_file("$home/notes.txt", "notes-old.txt")
robot.rws.file.copy_file("$home/notes-old.txt", "notes-backup.txt", True)
robot.rws.file.delete_file("$home/notes-old.txt")

robot.disconnect()
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

**Methods of FileService** ([reference](../api/underautomation.abb.rws.services.md#fileservice-robotrwsfile))

- `list_directory(path: str) -> DirectoryListing`: Lists contents of a directory resource (synchronous) Environment variables (e.g. $home, $temp) and devices are treated as directories.When listing the root path ("/", null, or "\\"), the response includes available devices in .The complete content is always returned, however many entries the dire...
- `delete_directory(path: str) -> None`: Deletes a directory and all its subdirectories and files (synchronous)
- `create_directory(path: str, newName: str) -> None`: Creates a new directory (synchronous) The newName parameter can contain nested directory structure (e.g. "parentdir/subdir")which will create both directories if they don't exist.
- `rename_directory(path: str, newName: str) -> None`: Renames a directory (synchronous)
- `copy_directory(path: str, newName: str, overwrite: bool) -> None`: Copies a directory (synchronous)
- `delete_file(path: str) -> None`: Deletes a file (synchronous)
- `rename_file(path: str, newName: str) -> None`: Renames a file (synchronous)
- `copy_file(path: str, newName: str, overwrite: bool) -> None`: Copies a file (synchronous)
- `get_file_as_bytes(path: str) -> typing.List[int]`: Gets file content as raw bytes (synchronous)
- `get_file_to_destination(path: str, localPath: str) -> None`: Downloads a file to a local path (synchronous)
- `upload_file_from_bytes(path: str, content: typing.List[int], contentType: str=None) -> None`: Uploads a file from raw bytes (synchronous)
- `upload_file_from_path(path: str, localPath: str, contentType: str=None) -> None`: Uploads a local file to the controller (synchronous)

**DirectoryListing** ([reference](../api/underautomation.abb.rws.data.md#directorylisting))

- `DirectoryListing(path: str)`: Initializes a new instance of the DirectoryListing class
- `files: typing.List[FileItem]`: Files contained in this directory
- `directories: typing.List[DirectoryItem]`: Subdirectories contained in this directory
- `devices: typing.List[DeviceItem]`: Devices available in this listing (typically only present at root "/")
- `path: str (read only)`: Path that was listed
- `file_count: int (read only)`: Number of files in this listing
- `directory_count: int (read only)`: Number of subdirectories in this listing
- `device_count: int (read only)`: Number of devices in this listing
- `total_count: int (read only)`: Total number of items (files + directories + devices)

**FileSystemItem** ([reference](../api/underautomation.abb.rws.data.md#filesystemitem))

- `name: str`: Name of the item (file name, directory name, or device name such as "C:")
- `creation_date: datetime | None`: Creation date of the resource, if available
- `modification_date: datetime | None`: Last modification date of the resource, if available

**FileItem** ([reference](../api/underautomation.abb.rws.data.md#fileitem))

- `FileItem()`: Initializes a new instance of the FileItem class
- `size: int`: File size in bytes
- `is_read_only: bool`: Indicates if the file is read-only
- Inherited from [FileSystemItem](../api/underautomation.abb.rws.data.md#filesystemitem): `name`, `creation_date`, `modification_date`

**DirectoryItem** ([reference](../api/underautomation.abb.rws.data.md#directoryitem))

- `DirectoryItem()`: Initializes a new instance of the DirectoryItem class
- `is_read_only: bool`: Indicates if the directory is read-only
- Inherited from [FileSystemItem](../api/underautomation.abb.rws.data.md#filesystemitem): `name`, `creation_date`, `modification_date`

**DeviceItem** ([reference](../api/underautomation.abb.rws.data.md#deviceitem))

- `DeviceItem()`: Initializes a new instance of the DeviceItem class
- `device_type: DeviceType`: Type of device (Fixed, Removable, RamDisk, Remote)
- `total_space: int`: Total storage space in bytes
- `free_space: int`: Free storage space in bytes
- `is_enabled: bool`: Indicates if the device is enabled
- `is_read_only: bool`: Indicates if the device is read-only
- Inherited from [FileSystemItem](../api/underautomation.abb.rws.data.md#filesystemitem): `name`, `creation_date`, `modification_date`

**DeviceType** ([reference](../api/underautomation.abb.rws.data.md#devicetype))

- Fixed: Fixed storage device (hard drive)
- Removable: Removable storage device (USB, SD card, etc.)
- RamDisk: RAM disk
- Remote: Remote or network storage
- Unknown: Unknown device type
