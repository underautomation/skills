# Choose a protocol

The four protocols of the Yaskawa SDK side by side: High Speed Ethernet Server, Ethernet Server, HTTP and FTP. Ports, tasks, speed, and code that works with two protocols.

Web page: https://underautomation.com/yaskawa/documentation/protocols

This page compares the four protocols that the Yaskawa SDK uses to talk to a Motoman controller: High Speed Ethernet Server, Ethernet Server, HTTP and FTP. It says what each one does, which ports it needs, and how to use several of them in one application.

## The four protocols

| Protocol                                                                  | Transport           | Property of `YaskawaRobot` | Enabled by default | Main use                                                      |
| ------------------------------------------------------------------------- | ------------------- | -------------------------- | ------------------ | ------------------------------------------------------------- |
| [High Speed Ethernet Server](high-speed-ethernet-server.md) | UDP 10040 and 10041 | `HighSpeedEServer`         | Yes                | Status, positions, motion, jobs, variables, I/O, files        |
| [Ethernet Server](ethernet-server.md)                 | TCP 80              | `EServer`                  | No                 | Status, positions, motion, jobs, variables, I/O, over TCP     |
| [HTTP](http.md)                                       | TCP 80              | `Http`                     | No                 | Read the file lists and the text files                        |
| [FTP](ftp.md)                                         | TCP 21              | `Ftp`                      | No                 | Download, upload and delete files, large files                |

Nothing is installed on the controller for any of them. The [offline kinematics](kinematics.md) need no protocol at all.

## Which protocol for which task

| Task                                             | First choice                | Also possible                       |
| ------------------------------------------------ | --------------------------- | ----------------------------------- |
| Read the status, the position, the alarms        | High Speed Ethernet Server  | Ethernet Server                     |
| Read and write B, I, D, R, S variables           | High Speed Ethernet Server  | Ethernet Server                     |
| Read and write P, BP, EX variables and registers | High Speed Ethernet Server  |                                     |
| Read the I/O, write the network inputs           | High Speed Ethernet Server  | Ethernet Server                     |
| Start a job and wait for its end                 | Ethernet Server (one call)  | High Speed Ethernet Server (polling) |
| Move the robot without a job                     | High Speed Ethernet Server  | Ethernet Server                     |
| Encoder temperatures, maximum torque             | Ethernet Server             |                                     |
| Download a job or a data file                    | FTP or HTTP                 | High Speed Ethernet Server          |
| Upload a job                                     | FTP                         | High Speed Ethernet Server          |
| Download a large file (`ALL.PRM`, 1.4 MB)        | FTP or HTTP (about 13 s)    | High Speed Ethernet Server (about 45 s) |
| CMOS backup                                      | High Speed Ethernet Server  |                                     |
| Only TCP passes the firewall                     | Ethernet Server, HTTP, FTP  |                                     |

The times are measured on a YRC1000micro. On the same controller, a status read takes about 10 ms with the High Speed Ethernet Server and about 20 ms with the Ethernet Server.

## Enable several protocols

Each protocol has an `Enable` flag in `ConnectParameters`. `Connect` opens every enabled protocol, `Disconnect` closes them all, and `Connected` is `true` when at least one is open.

```csharp
using UnderAutomation.Yaskawa;
using UnderAutomation.Yaskawa.Common;

public class ConnectAllProtocols
{
    static void Main()
    {
        var parameters = new ConnectParameters("192.168.0.1");

        // High Speed Ethernet Server (UDP 10040 and 10041): enabled by default
        parameters.HighSpeedEServer.Enable = true;

        // Ethernet Server (TCP 80): status, jobs, variables, I/O and moves
        parameters.EServer.Enable = true;

        // Web server of the controller (TCP 80): file lists and text files
        parameters.Http.Enable = true;

        // FTP server of the controller (TCP 21): file transfers
        parameters.Ftp.Enable = true;
        parameters.Ftp.FtpUser = "ftp"; // "anonymous" can only download

        var robot = new YaskawaRobot();
        robot.Connect(parameters);

        // One property per protocol
        var status = robot.HighSpeedEServer.GetStatusInformation();
        var jobs = robot.EServer.GetJobDirectory();
        var files = robot.Http.GetFileList(FileExtension.JOB);
        var listing = robot.Ftp.GetListing("/JOB");

        // Closes every protocol
        robot.Disconnect();
    }
}
```

### Ports to open in the firewall

| Protocol                   | Port         | Direction           |
| -------------------------- | ------------ | ------------------- |
| High Speed Ethernet Server | UDP 10040, UDP 10041 | PC to controller, and the answers |
| Ethernet Server            | TCP 80       | PC to controller    |
| HTTP                       | TCP 80       | PC to controller    |
| FTP                        | TCP 21, and the data connections of FTP | PC to controller |

The ping before the connection (`PingBeforeConnect`) also needs ICMP.

### Settings of the controller

The commands (servo, jobs, moves, writes) of the High Speed Ethernet Server and of the Ethernet Server need the remote mode: see [Prepare the controller](connect.md#prepare_the_controller). HTTP reads in any mode. FTP needs the right account to upload or delete: see [Accounts](ftp.md#accounts).

## Write code for both protocols

The High Speed Ethernet Server and the Ethernet Server clients implement the same interfaces of the namespace `UnderAutomation.Yaskawa.Common`. A function that takes an `IRobotClient` works with `robot.HighSpeedEServer` and with `robot.EServer`.

```csharp
using UnderAutomation.Yaskawa;
using UnderAutomation.Yaskawa.Common;

public class ProtocolsCommonInterface
{
    // Works with robot.HighSpeedEServer and with robot.EServer
    static void PrintState(IRobotClient client)
    {
        IStatusData status = client.GetStatusInformation();
        ICartesianPosition tcp = client.GetRobotCartesianPosition();

        Console.WriteLine($"{client.Address}: servo {status.ServoOn}, running {status.Running}");
        Console.WriteLine($"X={tcp.X} Y={tcp.Y} Z={tcp.Z}");
    }

    static void Main()
    {
        var parameters = new ConnectParameters("192.168.0.1");
        parameters.EServer.Enable = true;

        var robot = new YaskawaRobot();
        robot.Connect(parameters);

        // The same code reads the robot through two protocols
        PrintState(robot.HighSpeedEServer);
        PrintState(robot.EServer);

        robot.Disconnect();
    }
}
```

| Interface         | Methods                                                                            |
| ----------------- | ---------------------------------------------------------------------------------- |
| `IStatusReader`   | `GetStatusInformation`, `GetExecutingJobInformation`                               |
| `IPositionReader` | `GetRobotJointPosition` (pulses), `GetRobotCartesianPosition` (mm and degrees)     |
| `IAlarmReader`    | `GetActiveAlarms`                                                                  |
| `IRobotControl`   | `AlarmReset`, `SetServo`, `SetHold`, `SetTeachPendantLockState`, `SetCycle`, `StartJob`, `SelectJob`, `Display` |
| `IIOAccess`       | `ReadIO`, `WriteIO`                                                                |
| `IVariableAccess` | Read and write the B, I, D, R and S variables                                      |
| `ITorqueReader`   | `GetTorque`                                                                        |
| `IMotionControl`  | `MoveCartesian`, `MoveJoints`                                                      |
| `IRobotClient`    | All the interfaces above                                                           |
| `IFileReader`, `IFileWriter`, `IFileManager` | `GetFile`, `GetFileList`, `LoadFile`, `DeleteFile`: High Speed Ethernet Server, HTTP (read only) and FTP |

In Python, the clients have the same method names: a function that calls `get_status_information()` works with both, without the interfaces.

## Reference

**ConnectParameters** ([reference](../api/UnderAutomation.Yaskawa.md#connectparameters))

- `ConnectParameters()`: Creates a new set of connect parameters
- `ConnectParameters(string ip)`: Creates a new set of connect parameters and defines IP property
- `EServerConnectParametersInternal EServer { get; set; }`: Ethernet Server connect parameters. Used for TCP-based Host Control communication via Ethernet Server.
- `FtpConnectParametersInternal Ftp { get; set; }`: FTP connect parameters. Used for file upload, download, listing and management via the robot's built-in FTP server.
- `HighSpeedEServerConnectParametersInternal HighSpeedEServer { get; set; }`: High Speed Ethernet Server connect parameters
- `HttpConnectParametersInternal Http { get; set; }`: HTTP connect parameters. Used for file listing and file content retrieval via the robot's built-in web server.
- `string IP { get; set; }`: IP Adress or robot host name
- `bool PingBeforeConnect { get; set; }`: Send a ping command before connecting

**IRobotClient** ([reference](../api/UnderAutomation.Yaskawa.Common.md#irobotclient))

- Inherited from [IStatusReader](../api/UnderAutomation.Yaskawa.Common.md#istatusreader): `GetStatusInformation`, `GetExecutingJobInformation`
- Inherited from [IPositionReader](../api/UnderAutomation.Yaskawa.Common.md#ipositionreader): `GetRobotJointPosition`, `GetRobotCartesianPosition`
- Inherited from [IAlarmReader](../api/UnderAutomation.Yaskawa.Common.md#ialarmreader): `GetActiveAlarms`
- Inherited from [IRobotControl](../api/UnderAutomation.Yaskawa.Common.md#irobotcontrol): `AlarmReset`, `SetServo`, `SetHold`, `SetTeachPendantLockState`, `SetCycle`, `StartJob`, `SelectJob`, `Display`
- Inherited from [IIOAccess](../api/UnderAutomation.Yaskawa.Common.md#iioaccess): `ReadIO`, `WriteIO`
- Inherited from [IVariableAccess](../api/UnderAutomation.Yaskawa.Common.md#ivariableaccess): `ReadByte`, `WriteByte`, `ReadInteger`, `WriteInteger`, `ReadDoubleInteger`, `WriteDoubleInteger`, `ReadReal`, `WriteReal`, `Read16BytesChar`, `Write16BytesChar`
- Inherited from [ITorqueReader](../api/UnderAutomation.Yaskawa.Common.md#itorquereader): `GetTorque`
- Inherited from [IMotionControl](../api/UnderAutomation.Yaskawa.Common.md#imotioncontrol): `MoveCartesian`, `MoveJoints`
- Inherited from [IYaskawaClient](../api/UnderAutomation.Yaskawa.Common.md#iyaskawaclient): `Close`, `Address`, `Connected`

**IFileManager** ([reference](../api/UnderAutomation.Yaskawa.Common.md#ifilemanager))

- Inherited from [IFileReader](../api/UnderAutomation.Yaskawa.Common.md#ifilereader): `GetFile`, `GetFileList`
- Inherited from [IFileWriter](../api/UnderAutomation.Yaskawa.Common.md#ifilewriter): `LoadFile`, `DeleteFile`
- Inherited from [IYaskawaClient](../api/UnderAutomation.Yaskawa.Common.md#iyaskawaclient): `Close`, `Address`, `Connected`

## What to read next

- [Connect to your robot](connect.md): the settings of the controller and the connection errors.
- [Ethernet Server](ethernet-server.md), [HTTP](http.md), [FTP](ftp.md): the pages of each protocol.
