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

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class BackupCreate
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // The controller creates the backup in the background, this call returns immediately
        robot.Rws.Controller.CreateBackup("$temp/mybackup");

        // Poll the state until the controller is done
        BackupState state = robot.Rws.Controller.GetBackupState();

        while (state == BackupState.BackupInProgress)
        {
            Thread.Sleep(1000);
            state = robot.Rws.Controller.GetBackupState();
        }

        if (state != BackupState.BackupReady)
        {
            Console.WriteLine($"The backup failed : {state}");
            return;
        }

        // What the backup contains
        BackupSystemInfo backup = robot.Rws.Controller.GetBackupInfo("$temp/mybackup");
        Console.WriteLine($"{backup.SystemName}, RobotWare {backup.RobotWareVersion}");
        Console.WriteLine($"{backup.OptionCount} option(s) : {string.Join(", ", backup.Options)}");

        robot.Disconnect();
    }
}
```

Points to know before running this on a production cell:

- The user account needs the UAS grant to create a backup.
- Creating a backup can affect RAPID execution and can stop the system. Do it between two cycles, not during one.
- The destination has to be inside the controller file system. Environment variables are allowed, written `$temp/mybackup` or `~temp/mybackup`. The backup cannot be created under `$home`, and cannot take the name of an environment variable directory.
- A destination that already exists is refused with the HTTP status code 409.

`GetBackupInfo(path)` reads the system name, the versions and the option list out of a backup already stored on the controller, without restoring anything. Use it to check that a backup matches the robot before you send it back.

## Download the backup to your PC

The backup sits on the controller until you copy it. The file service walks the directory and downloads each file.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class HowToBackupDownload
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        string backupPath = "$temp/mybackup";

        // 1. Ask the controller for a backup and wait until it is finished
        robot.Rws.Controller.CreateBackup(backupPath);

        BackupState state = robot.Rws.Controller.GetBackupState();

        while (state == BackupState.BackupInProgress || state == BackupState.InitState)
        {
            Thread.Sleep(1000);
            state = robot.Rws.Controller.GetBackupState();
        }

        if (state != BackupState.BackupReady)
            throw new Exception($"The backup failed : {state}");

        // 2. A backup is a directory on the controller. Copy it to the PC, file by file.
        DownloadDirectory(robot, backupPath, @"C:\backups\mybackup");

        robot.Disconnect();
    }

    // Copies a directory of the controller and everything under it to a directory of the PC
    static void DownloadDirectory(AbbController robot, string controllerPath, string localPath)
    {
        Directory.CreateDirectory(localPath);

        DirectoryListing listing = robot.Rws.File.ListDirectory(controllerPath);

        foreach (FileItem file in listing.Files)
        {
            robot.Rws.File.GetFileToDestination(controllerPath + "/" + file.Name,
                                                Path.Combine(localPath, file.Name));
        }

        foreach (DirectoryItem directory in listing.Directories)
        {
            DownloadDirectory(robot, controllerPath + "/" + directory.Name,
                              Path.Combine(localPath, directory.Name));
        }
    }
}
```

A backup created with `archive: true` is a single file, downloaded with one call to `GetFileToDestination`. Delete the copy left on the controller with `robot.Rws.File.DeleteDirectory(...)` when you no longer need it, `$temp` is not unlimited.

The other file operations, listing, uploading, renaming and deleting, are described on the [file system page](rws-files.md).

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

## Send a backup back to the controller

A restore reads the backup from the controller file system, so a backup kept on the PC has to be uploaded first. Recreate the directory tree and upload the files one by one.

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

## Check the backup, then restore it

`CheckRestore` looks for the mismatches and the missing files before anything is changed. `IsAccepted` is the property to test, and `Path` names the file the controller complains about when it reports one.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class BackupRestore
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // Check the backup before restoring it
        CheckRestoreResult check = robot.Rws.Controller.CheckRestore("$temp/mybackup");

        if (!check.IsAccepted)
        {
            Console.WriteLine($"The backup cannot be restored : {check.Status} {check.Path}");
            return;
        }

        // The controller restarts as soon as the restore is accepted
        robot.Rws.Controller.RestoreBackup("$temp/mybackup");

        // A backup taken on another controller has a different system id.
        // Ignore the mismatch to restore it anyway, and keep the backup folder.
        robot.Rws.Controller.RestoreBackup("$temp/mybackup",
                                           BackupRestoreIgnore.SystemId,
                                           false);

        // Restore only the RAPID modules, not the configuration
        robot.Rws.Controller.RestoreBackup("$temp/mybackup",
                                           BackupRestoreIgnore.All,
                                           true,
                                           true,
                                           true,
                                           BackupRestoreInclude.Modules);

        robot.Disconnect();
    }
}
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

**Methods of ControllerService** ([reference](../api/UnderAutomation.ABB.Rws.Services.md#controllerservice-robotrwscontroller))

- `void CreateBackup(string backupPath, bool archive = false)`: Creates a backup of the current system on the controller file system (synchronous) The backup is created asynchronously by the controller: this method returns as soon as the request is accepted. Poll ControllerService.GetBackupState to know when the backup is finished. Requires the UAS grant UAS_...
  - async: `Task CreateBackupAsync(string backupPath, bool archive = false, CancellationToken cancellationToken = default)`
- `BackupSystemInfo GetBackupInfo(string backupPath)`: Gets information about a backup stored on the controller file system (synchronous)
  - async: `Task<BackupSystemInfo> GetBackupInfoAsync(string backupPath, CancellationToken cancellationToken = default)`
- `string[] GetBackupResources()`: Gets the names of the backup sub resources exposed by the controller (synchronous)
  - async: `Task<string[]> GetBackupResourcesAsync(CancellationToken cancellationToken = default)`
- `BackupState GetBackupState()`: Gets the state of the backup operation of the controller (synchronous) Used to follow a backup started with String%2cSystem.Boolean).
  - async: `Task<BackupState> GetBackupStateAsync(CancellationToken cancellationToken = default)`
- `void RestoreBackup(string backupPath, BackupRestoreIgnore ignore = BackupRestoreIgnore.None, bool deleteDirectory = true, bool includeControllerSettings = true, bool includeSafetySettings = true, BackupRestoreInclude include = BackupRestoreInclude.All)`: Restores a backup stored on the controller file system (synchronous) When the backup can be restored, the controller restarts. Requires the UAS grant to restore a backup. Use Data.BackupRestoreInclude) first to detect mismatches.
  - async: `Task RestoreBackupAsync(string backupPath, BackupRestoreIgnore ignore = BackupRestoreIgnore.None, bool deleteDirectory = true, bool includeControllerSettings = true, bool includeSafetySettings = true, BackupRestoreInclude include = BackupRestoreInclude.All, CancellationToken cancellationToken = default)`

**BackupState** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#backupstate))

- BackupInProgress: A backup operation is running
- BackupReady: The backup operation finished successfully
- ErrorDuringBackup: The backup operation failed
- InitState: A backup operation has been initialized
- Invalid: The backup state is invalid
- None: No backup operation
- Unknown: The backup state could not be determined

**BackupSystemInfo** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#backupsysteminfo))

- `BackupSystemInfo()`: Initializes a new instance of the Data.BackupSystemInfo class
- `int OptionCount { get; }`: Number of options installed on the backed up system
- `string[] Options { get; set; }`: Options installed on the backed up system
- `string RobotControlVersion { get; set; }`: RobotControl version of the backed up system. Only available when connected with version 2.
- `string RobotOsVersion { get; set; }`: RobotOS version of the backed up system. Only available when connected with version 2.
- `string RobotWareVersion { get; set; }`: RobotWare version of the backed up system. Only available when connected with version 1.
- `string SystemName { get; set; }`: Name of the backed up system

**CheckRestoreResult** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#checkrestoreresult))

- `CheckRestoreResult()`: Initializes a new instance of the Data.CheckRestoreResult class
- `bool IsAccepted { get; }`: Indicates whether the backup can be restored
- `string Path { get; set; }`: File missing or corrupted in the backup, if reported by the controller
- `CheckRestoreStatus Status { get; set; }`: Status of the check

**BackupRestoreIgnore** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#backuprestoreignore))

- All: All mismatches are ignored
- None: No mismatch is ignored
- SystemId: A mismatch between the system id of the backup and the system id of the current system is ignored
- TemplateId: A mismatch between the template id of the backup and the template id of the current system is ignored

**BackupRestoreInclude** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#backuprestoreinclude))

- All: Restore configuration files and RAPID modules
- Cfg: Restore configuration files only
- Modules: Restore RAPID modules only
