# Files and backup

List, download, upload and delete the job and data files of a Yaskawa controller, and download its CMOS backup.

Web page: https://underautomation.com/yaskawa/documentation/hses-files

This page shows how to transfer files between a PC and a Yaskawa Motoman controller with the SDK: list, download, upload and delete jobs and data files, and download the CMOS backup. The file transfers use the UDP port 10041 of the High Speed Ethernet Server.

## List the files

`GetFileList(pattern)` lists the files whose name matches a pattern with `*`.

```csharp
using UnderAutomation.Yaskawa;
using UnderAutomation.Yaskawa.HighSpeedEServer;

public class FileList
{
    static void Main()
    {
        var robot = new YaskawaRobot();
        robot.Connect("192.168.0.1");

        // Job files
        string[] jobs = robot.HighSpeedEServer.GetFileList("*.JBI").Files;

        // Variable data and condition files
        string[] dat = robot.HighSpeedEServer.GetFileList("*.DAT").Files;
        string[] cnd = robot.HighSpeedEServer.GetFileList("*.CND").Files;

        foreach (string file in jobs)
            Console.WriteLine(file);

        robot.Disconnect();
    }
}
```

| Pattern | Files                                 |
| ------- | ------------------------------------- |
| `*.JBI` | Jobs                                  |
| `*.DAT` | Data files, for example the variables |
| `*.CND` | Condition files                       |
| `*.PRM` | Parameter files                       |

## Download a file

`GetFile(name)` downloads a file. `Content` is the text of the file, `ContentRaw` its bytes. The optional callback gives the progress of large files.

```csharp
using UnderAutomation.Yaskawa;
using UnderAutomation.Yaskawa.HighSpeedEServer;

public class FileDownload
{
    static void Main()
    {
        var robot = new YaskawaRobot();
        robot.Connect("192.168.0.1");

        // Download a file, with an optional progress callback
        RobotFileContentData file = robot.HighSpeedEServer.GetFile("WELD01.JBI", progress =>
        {
            Console.WriteLine($"{progress.FileName}: {progress.DownloadedBytes} bytes");
        });

        // Text content, and the raw bytes for a binary file
        File.WriteAllText("WELD01.JBI", file.Content);
        File.WriteAllBytes("WELD01.copy.JBI", file.ContentRaw);

        robot.Disconnect();
    }
}
```

## Upload a file

`LoadFile(name, content)` sends a text file to the controller. A job sent this way appears in the job list of the controller, ready to select.

```csharp
using UnderAutomation.Yaskawa;
using UnderAutomation.Yaskawa.HighSpeedEServer;

public class FileUpload
{
    static void Main()
    {
        var robot = new YaskawaRobot();
        robot.Connect("192.168.0.1");

        string content = File.ReadAllText("WELD01.JBI");

        // Send the file to the controller, with an optional progress callback
        robot.HighSpeedEServer.LoadFile("WELD01.JBI", content, progress =>
        {
            Console.WriteLine($"{progress.LoadedBytes} / {progress.TotalBytes} bytes");
        });

        robot.Disconnect();
    }
}
```

- To replace a file that exists on the controller, the parameters `RS029` and `RS214` must be `1`. See [Connect to your robot](connect.md#allow_the_file_overwrite).
- The controller checks the syntax of a job when it receives it. A job with an error is refused, with the reason in the message of the `InvalidDataAnswerException`.

## Delete a file

`DeleteFile(name)` deletes a file of the controller. There is no undo: download the file first if you may need it.

```csharp
using UnderAutomation.Yaskawa;
using UnderAutomation.Yaskawa.HighSpeedEServer;

public class FileDelete
{
    static void Main()
    {
        var robot = new YaskawaRobot();
        robot.Connect("192.168.0.1");

        // Delete a job file of the controller. There is no undo
        robot.HighSpeedEServer.DeleteFile("WELD01.JBI");

        robot.Disconnect();
    }
}
```

## CMOS backup

`BatchDataBackup()` makes the controller write its CMOS backup (jobs, parameters, settings) to `/SPDRV/CMOSBK.BIN`. Then `GetFile` downloads it.

```csharp
using UnderAutomation.Yaskawa;
using UnderAutomation.Yaskawa.HighSpeedEServer;

public class FileBackup
{
    static void Main()
    {
        var robot = new YaskawaRobot();
        robot.Connect("192.168.0.1");

        // Ask the controller to write its CMOS backup to /SPDRV/CMOSBK.BIN.
        // It takes several seconds
        robot.HighSpeedEServer.BatchDataBackup();

        // Download the backup as binary
        RobotFileContentData backup = robot.HighSpeedEServer.GetFile("/SPDRV/CMOSBK.BIN");
        File.WriteAllBytes("CMOSBK.BIN", backup.ContentRaw);

        robot.Disconnect();
    }
}
```

- The backup takes several seconds. While it runs, a download of the file fails with an `InvalidDataAnswerException`: wait and try again.
- The command needs the automatic backup function with the RAM disk as device. In management mode, select `SETUP` > `AUTO BACKUP SET` and set `DEVICE` to `RAMDISK`. If this menu is missing, start the controller in maintenance mode and set `AUTOBACKUP` to `USED` in `SYSTEM` > `SETUP` > `OPTION FUNCTION`.

## Timeouts

The file transfers wait `FileTimeoutMilliseconds` (4000 ms by default) for each answer of the controller. Increase it if large files fail on a slow network. See [Connect to your robot](connect.md#connection_parameters).

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**Methods of HighSpeedEServerClientBase** ([reference](../api/UnderAutomation.Yaskawa.HighSpeedEServer.Internal.md#highspeedeserverclientbase-robothighspeedeserver))

- `RobotDataHeader BatchDataBackup(string file = "/SPDRV/CMOSBK.BIN")`: Performs a backup of the robot's CMOS. The CMOS.BIN file is copied locally in the robot controller to "/SPDRC/CMOSBK.BIN". The operation can take several seconds to complete. After this command, the backup file can be downloaded using GetFile("/SPDRC/CMOSBK.BIN"). To enable this command : in "MAN...
- `RobotDataHeader DeleteFile(string name)`: Deletes a file from the robot controller's file system. Use with caution as deleted files cannot be recovered.
- `RobotFileContentData GetFile(string name, HighSpeedEServerClientBase.GetFileProgressDelegate onGetFileProgress = null)`: Downloads (saves) a file from the robot controller to the PC. Large files are received in multiple blocks and automatically reassembled. Special use case : to download CMOS.BIN, first perform a CMOS backup using BatchDataBackup, then use GetFile with the backup file path.
- `RobotFileListData GetFileList(string pattern)`: Retrieves a list of files matching a pattern from the robot controller. Supports wildcards for matching multiple files.
- `RobotDataHeader[] LoadFile(string name, string content, HighSpeedEServerClientBase.LoadFileProgressDelegate onLoadFileProgress = null)`: Uploads (loads) a file from the PC to the robot controller. Large files are automatically split into 479-byte chunks for transmission.

**RobotFileListData** ([reference](../api/UnderAutomation.Yaskawa.HighSpeedEServer.md#robotfilelistdata))

- `string[] Files { get; }`: Gets the array of file names returned by the listing operation. File names include extensions (e.g., "MYJOB.JBI", "SYSTEM.SYS").
- `List<RobotDataHeader> Headers { get; }`: Gets the list of response headers from multi-block transfers. File listings may span multiple UDP packets for large directories.

**RobotFileContentData** ([reference](../api/UnderAutomation.Yaskawa.HighSpeedEServer.md#robotfilecontentdata))

- `string Content { get; }`: Gets the text content of the downloaded file.
- `byte[] ContentRaw { get; }`: Gets the text content of the downloaded file.
- `string FileName { get; }`: Gets the name of the downloaded file.
- `int GetParam(string section, int parameterLine, int parameterColumn)`: Extracts an integer parameter value from a structured file section. Useful for reading values from parameter files and job data.
- `List<RobotDataHeader> Headers { get; }`: Gets the list of response headers from multi-block transfers. Large files are transferred in multiple UDP packets.

**LoadFileProgress** ([reference](../api/UnderAutomation.Yaskawa.HighSpeedEServer.md#loadfileprogress))

- `bool Completed { get; }`: Gets whether the file upload has completed successfully.
- `string FileName { get; }`: Gets the name of the file being uploaded.
- `int LoadedBytes { get; }`: Gets the number of bytes uploaded so far.
- `int TotalBytes { get; }`: Gets the total size of the file in bytes.

**GetFileProgress** ([reference](../api/UnderAutomation.Yaskawa.HighSpeedEServer.md#getfileprogress))

- `bool Completed { get; }`: Gets whether the file download has completed successfully.
- `int DownloadedBytes { get; }`: Gets the number of bytes downloaded so far.
- `string FileName { get; }`: Gets the name of the file being downloaded.
