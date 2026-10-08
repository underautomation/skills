# Upload, download & backup files

Transfer TP programs, variable files, and backups between your PC and a Fanuc controller using FTP or CGTP.

Web page: https://underautomation.com/fanuc/documentation/upload-download-backup-files

Upload, download, and backup controller files on your Fanuc robot using FTP and CGTP.

## FTP : Full file management

FTP provides complete file management: upload, download, delete, rename, and directory operations.

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

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common;
using UnderAutomation.Fanuc.Common.Files.Variables;
using UnderAutomation.Fanuc.Ftp;

public class UploadDownloadBackupFilesFtp
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        robot.Connect("192.168.0.1");

        // Backup: list all files and download
        FtpListItem[] files = robot.Ftp.DirectFileHandling.GetListing("md:/");
        foreach (var file in files)
        {
            robot.Ftp.DirectFileHandling.DownloadFileFromController($"backup/{file.Name}", $"md:/{file.Name}");
        }

        // Upload a .tp file
        robot.Ftp.DirectFileHandling.UploadFileToController("C:/programs/MY_PROGRAM.tp", "md:/MY_PROGRAM.tp");

        // Download specific variable files
        robot.Ftp.DirectFileHandling.DownloadFileFromController(out byte[] numreg, "md:/numreg.va");
        robot.Ftp.DirectFileHandling.DownloadFileFromController(out byte[] posreg, "md:/posreg.va");

        // Or use convenience methods
        NumregFile regs = robot.Ftp.KnownVariableFiles.GetNumregFile();
    }
}
```

## CGTP : File download via HTTP

CGTP provides file listing and download through the robot's web server:

```csharp
using System;
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Cgtp;

public class UploadDownloadBackupFilesCgtp
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        robot.Connect("192.168.0.1");

        // List TP programs
        CgtpAsciiFileItem[] programs = robot.Cgtp.Http.ListTpPrograms();

        // Download a file as string
        string content = robot.Cgtp.Http.DownloadAsString("numreg.va");

        // Download a file as bytes
        byte[] data = robot.Cgtp.Http.DownloadAsBytes("posreg.va");

        // List files via CGTP protocol
        string[] files = robot.Cgtp.ListFiles("MD:");
    }
}
```

See also: [CGTP Alarms, comments & files](cgtp-alarms-files.md)

## Protocol comparison

| Feature | FTP | CGTP |
|---------|-----|------|
| **Upload** | Yes | No |
| **Download** | Yes | Yes |
| **Delete** | Yes | Only jobs |
| **Rename** | Yes | Only jobs |
| **Directory ops** | Yes | No |
| **List files** | Yes | Yes |
| **Authentication** | Optional | Optional |
