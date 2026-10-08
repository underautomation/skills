# Test with ROBOGUIDE

Develop without a real robot. Connect the SDK to a virtual robot of FANUC ROBOGUIDE with the folder of the robot, like to a real controller.

Web page: https://underautomation.com/fanuc/documentation/simulator

This page explains how to develop with the Fanuc SDK without a real robot, with a virtual robot of FANUC ROBOGUIDE. The virtual controller of ROBOGUIDE runs the controller software on your PC, and the SDK connects to it like to a real controller.

## Prerequisites

### Software

- ROBOGUIDE, installed on a Windows PC. It is a FANUC product, with its own license: ask your FANUC contact.
- A workcell with a robot. Use the arm and the software options of your real cell.
- The workcell open in ROBOGUIDE, with its virtual controller started.

### Options of the workcell

The options of the virtual robot are chosen when the workcell is created ("Robot options" step of the workcell creation wizard), as on a real controller:

| Protocol      | Needed in the workcell                                                                              |
| ------------- | --------------------------------------------------------------------------------------------------- |
| CGTP, FTP     | Nothing                                                                                             |
| Telnet KCL    | The KCL port, see below                                                                             |
| SNPX          | R553 "HMI Device SNPX" with the FANUC America parameters (R650 FRA). Nothing with the FANUC Ltd. parameters (R651 FRL) |
| RMI           | R912 "Remote Motion Interface"                                                                      |
| Stream Motion | J519 "Stream Motion"                                                                                |

## Connect to the virtual robot

### With the folder of the robot

Pass the folder of the robot in the workcell instead of an IP address. This folder contains the file `services.txt`, written by ROBOGUIDE: the SDK reads in it the ports of Telnet KCL, FTP, SNPX and CGTP, which are not the default ports of a real controller.

```csharp
using UnderAutomation.Fanuc;

public class SimulatorConnect
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();

        // Folder of the virtual robot in the ROBOGUIDE workcell. It contains services.txt.
        var parameters = new ConnectionParameters(@"C:\Users\you\Documents\My Workcells\CRX 10iA L\Robot_1");

        // The SDK reads the ports of these services in services.txt
        parameters.Cgtp.Enable = true;
        parameters.Ftp.Enable = true;
        parameters.Snpx.Enable = true;
        parameters.Telnet.Enable = true;
        parameters.Telnet.TelnetKclPassword = "";

        robot.Connect(parameters);

        robot.Disconnect();
    }
}
```

The folder of a robot is `<workcell folder>\Robot_1` by default, for example `C:\Users\you\Documents\My Workcells\CRX 10iA L\Robot_1`. You can also pass the path of `services.txt` itself. With several robots in the workcell, connect one `FanucRobot` per robot folder.

### From another PC

When ROBOGUIDE runs on another PC, share the folder of the workcell and pass its network path. The SDK reads `services.txt` in the share and connects to the PC named in the path.

```csharp
using UnderAutomation.Fanuc;

public class SimulatorRemote
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();

        // ROBOGUIDE runs on the PC "SIMU-PC", which shares its workcell folder.
        // The SDK reads services.txt in the share and connects to SIMU-PC.
        var parameters = new ConnectionParameters(@"\SIMU-PC\My Workcells\CRX 10iA L\Robot_1");
        parameters.Cgtp.Enable = true;
        parameters.Ftp.Enable = true;

        robot.Connect(parameters);

        robot.Disconnect();
    }
}
```

Allow the ports of `services.txt` in the firewall of the PC that runs ROBOGUIDE.

### Telnet KCL on ROBOGUIDE

The default Telnet port of a virtual robot is read-only. Enable the KCL port:

1. On the teach pendant of the virtual robot, open `MENU`, `SETUP`, `PORT INIT`.
2. Set Connector 1 to the device `KCL/CRT`.
3. Do a cold start of the virtual controller.

Without this port, `Connect` throws an exception that gives the same steps. Telnet KCL works up to ROBOGUIDE V9: ROBOGUIDE V10 does not simulate it. See [Enable Telnet on your robot](telnet-enable-on-robot.md).

## What works on ROBOGUIDE

Every feature of the SDK sends the same requests to ROBOGUIDE and to a real controller:

- registers, variables, I/O, alarms and programs, with CGTP, SNPX, Telnet KCL and FTP;
- the position of the robot and the kinematics on the controller;
- the motion with RMI and Stream Motion, when the option is in the workcell;
- the files and the diagnostics of the controller.

Use ROBOGUIDE to write and test your application, then run the same code on the real controller with its IP address.

## Differences with a real controller

- The I/O of the virtual robot are not wired: simulate the inputs (see [Control inputs & outputs](set-and-simulate-inputs-outputs.md)).
- The ports of a virtual robot are in `services.txt`. With an IP address, the SDK uses the default ports of a real controller.
- Timings are not the timings of the real controller. SNPX can answer in less than 1 ms on ROBOGUIDE: do not measure cycle times on the simulator.

## What to read next

- [Connect to your robot](connect.md): all the connection parameters.
- [Demo application](demo-app.md): try ROBOGUIDE without writing code.
- [Move robot remotely](move-robot-remotely.md): test the motion on ROBOGUIDE first.
