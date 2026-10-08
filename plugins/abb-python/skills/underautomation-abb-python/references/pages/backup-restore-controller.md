# Backup & restore a controller

Create a full controller backup, download it to your PC, check it and restore it, entirely from your application.

Web page: https://underautomation.com/abb/documentation/backup-restore-controller

A backup is made in two steps: `robot.Rws.Controller.CreateBackup(path)` asks the controller to write it on its own file system, then the file service copies it to your PC. Restoring goes the other way, and ends with a restart of the controller.

> **Available on** RWS 1.0 (IRC5) : yes | RWS 2.0 (OmniCore) : yes.

## What a backup contains

A backup holds the system parameters, the RAPID programs and modules, the calibration data and the system information of the controller. It is what you need to put a system back as it was after a hardware replacement, and what a support team asks for when something goes wrong.

A backup is a directory of files, not a single file. `CreateBackup` has an `archive` argument to store it as an archive instead.

## Create a backup

The controller writes the backup in the background. `CreateBackup` returns as soon as the request is accepted, so poll the state until the controller reports it is finished.

```python
import time

from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.backup_state import BackupState

robot = AbbController()
robot.connect("192.168.0.1")

# The controller creates the backup in the background, this call returns immediately
robot.rws.controller.create_backup("$temp/mybackup")

# Poll the state until the controller is done
state = robot.rws.controller.get_backup_state()

while state == BackupState.BackupInProgress:
    time.sleep(1)
    state = robot.rws.controller.get_backup_state()

if state != BackupState.BackupReady:
    print(f"The backup failed : {state}")
    raise SystemExit(1)

# What the backup contains
backup = robot.rws.controller.get_backup_info("$temp/mybackup")
print(f"{backup.system_name}, RobotWare {backup.robot_ware_version}")
print("Options : " + ", ".join(backup.options))

robot.disconnect()
```

Points to know before running this on a production cell:

- The user account needs the UAS grant to create a backup.
- Creating a backup can affect RAPID execution and can stop the system. Do it between two cycles, not during one.
- The destination has to be inside the controller file system. Environment variables are allowed, written `$temp/mybackup` or `~temp/mybackup`. The backup cannot be created under `$home`, and cannot take the name of an environment variable directory.
- A destination that already exists is refused with the HTTP status code 409.

`GetBackupInfo(path)` reads the system name, the versions and the option list out of a backup already stored on the controller, without restoring anything. Use it to check that a backup matches the robot before you send it back.

## Download the backup to your PC

The backup sits on the controller until you copy it. The file service walks the directory and downloads each file.

```python
import os
import time

from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.backup_state import BackupState

robot = AbbController()
robot.connect("192.168.0.1")

# Copies a directory of the controller and everything under it to a directory of the PC
def download_directory(robot, controller_path, local_path):
    os.makedirs(local_path, exist_ok=True)

    listing = robot.rws.file.list_directory(controller_path)

    for file in listing.files:
        robot.rws.file.get_file_to_destination(controller_path + "/" + file.name,
                                               os.path.join(local_path, file.name))

    for directory in listing.directories:
        download_directory(robot, controller_path + "/" + directory.name,
                           os.path.join(local_path, directory.name))

backup_path = "$temp/mybackup"

# 1. Ask the controller for a backup and wait until it is finished
robot.rws.controller.create_backup(backup_path)

state = robot.rws.controller.get_backup_state()

while state == BackupState.BackupInProgress or state == BackupState.InitState:
    time.sleep(1)
    state = robot.rws.controller.get_backup_state()

if state != BackupState.BackupReady:
    raise Exception(f"The backup failed : {state}")

# 2. A backup is a directory on the controller. Copy it to the PC, file by file.
download_directory(robot, backup_path, r"C:\backups\mybackup")

robot.disconnect()
```

A backup created with `archive: true` is a single file, downloaded with one call to `GetFileToDestination`. Delete the copy left on the controller with `robot.Rws.File.DeleteDirectory(...)` when you no longer need it, `$temp` is not unlimited.

The other file operations, listing, uploading, renaming and deleting, are described on the [file system page](rws-files.md).

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

## Send a backup back to the controller

A restore reads the backup from the controller file system, so a backup kept on the PC has to be uploaded first. Recreate the directory tree and upload the files one by one.

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

## Check the backup, then restore it

`CheckRestore` looks for the mismatches and the missing files before anything is changed. `IsAccepted` is the property to test, and `Path` names the file the controller complains about when it reports one.

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.backup_restore_ignore import BackupRestoreIgnore
from underautomation.abb.rws.data.backup_restore_include import BackupRestoreInclude

robot = AbbController()
robot.connect("192.168.0.1")

# Check the backup before restoring it
check = robot.rws.controller.check_restore("$temp/mybackup")

if not check.is_accepted:
    print(f"The backup cannot be restored : {check.status} {check.path}")
    raise SystemExit(1)

# The controller restarts as soon as the restore is accepted
robot.rws.controller.restore_backup("$temp/mybackup")

# A backup taken on another controller has a different system id.
# Ignore the mismatch to restore it anyway, and keep the backup folder.
robot.rws.controller.restore_backup("$temp/mybackup",
                                    BackupRestoreIgnore.SystemId,
                                    False)

# Restore only the RAPID modules, not the configuration
robot.rws.controller.restore_backup("$temp/mybackup",
                                    BackupRestoreIgnore.All,
                                    True,
                                    True,
                                    True,
                                    BackupRestoreInclude.Modules)

robot.disconnect()
```

A backup taken on another controller has a different system id, and the check refuses it. `BackupRestoreIgnore.SystemId` restores it anyway, `BackupRestoreIgnore.All` ignores every mismatch. Ignoring a mismatch on purpose is normal when you move a system to a replacement cabinet, it is a mistake when you did not expect one.

`BackupRestoreInclude` limits what is restored. `All` restores everything, `Modules` only the RAPID modules, `Cfg` only the configuration.

**The controller restarts as soon as the restore is accepted.** Your connection is lost, and the robot is unavailable for the time of the restart. Warn the operator, and reconnect afterwards instead of reusing the same session.

RobotWare 7 does not restore the controller settings and ignores that flag. The other arguments behave the same on both controller generations.

## A backup routine that runs on its own

Put together, a scheduled backup is: connect, create the backup, wait for `BackupReady`, download the directory, delete it from the controller, disconnect. Keep one folder per date on the PC, and read `GetBackupInfo` before deleting anything, so a backup that failed silently does not replace a good one.

## Going further

- [Controller: identity, clock & backup](rws-controller.md), the complete reference
- [File system](rws-files.md), to browse, upload and delete files on the controller
- [Connect to your robot](connect.md), for the user account and its grants

**Methods of ControllerService** ([reference](../api/underautomation.abb.rws.services.md#controllerservice-robotrwscontroller))

- `get_backup_resources() -> typing.List[str]`: Gets the names of the backup sub resources exposed by the controller (synchronous)
- `get_backup_info(backupPath: str) -> BackupSystemInfo`: Gets information about a backup stored on the controller file system (synchronous)
- `get_backup_state() -> BackupState`: Gets the state of the backup operation of the controller (synchronous) Used to follow a backup started with .
- `create_backup(backupPath: str, archive: bool=False) -> None`: Creates a backup of the current system on the controller file system (synchronous) The backup is created asynchronously by the controller: this method returns as soon as the request is accepted. Poll to know when the backup is finished.Requires the UAS grant UAS_BACKUP. Creating a backup may affe...
- `restore_backup(backupPath: str, ignore: BackupRestoreIgnore=BackupRestoreIgnore.None_, deleteDirectory: bool=True, includeControllerSettings: bool=True, includeSafetySettings: bool=True, include: BackupRestoreInclude=BackupRestoreInclude.All) -> None`: Restores a backup stored on the controller file system (synchronous) When the backup can be restored, the controller restarts.Requires the UAS grant to restore a backup. Use first to detect mismatches.

**BackupState** ([reference](../api/underautomation.abb.rws.data.md#backupstate))

- Unknown: The backup state could not be determined
- None_: No backup operation
- InitState: A backup operation has been initialized
- BackupInProgress: A backup operation is running
- BackupReady: The backup operation finished successfully
- ErrorDuringBackup: The backup operation failed
- Invalid: The backup state is invalid

**BackupSystemInfo** ([reference](../api/underautomation.abb.rws.data.md#backupsysteminfo))

- `BackupSystemInfo()`: Initializes a new instance of the BackupSystemInfo class
- `system_name: str`: Name of the backed up system
- `robot_ware_version: str`: RobotWare version of the backed up system. Only available when connected with version 1.
- `robot_control_version: str`: RobotControl version of the backed up system. Only available when connected with version 2.
- `robot_os_version: str`: RobotOS version of the backed up system. Only available when connected with version 2.
- `options: typing.List[str]`: Options installed on the backed up system
- `option_count: int (read only)`: Number of options installed on the backed up system

**CheckRestoreResult** ([reference](../api/underautomation.abb.rws.data.md#checkrestoreresult))

- `CheckRestoreResult()`: Initializes a new instance of the CheckRestoreResult class
- `status: CheckRestoreStatus`: Status of the check
- `is_accepted: bool (read only)`: Indicates whether the backup can be restored
- `path: str`: File missing or corrupted in the backup, if reported by the controller

**BackupRestoreIgnore** ([reference](../api/underautomation.abb.rws.data.md#backuprestoreignore))

- None_: No mismatch is ignored
- All: All mismatches are ignored
- SystemId: A mismatch between the system id of the backup and the system id of the current system is ignored
- TemplateId: A mismatch between the template id of the backup and the template id of the current system is ignored

**BackupRestoreInclude** ([reference](../api/underautomation.abb.rws.data.md#backuprestoreinclude))

- All: Restore configuration files and RAPID modules
- Cfg: Restore configuration files only
- Modules: Restore RAPID modules only
