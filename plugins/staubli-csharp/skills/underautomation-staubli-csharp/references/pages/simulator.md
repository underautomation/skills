# Test with the Staubli Robotics Suite emulator

Develop without a real robot. Connect the SDK to the CS8 or CS9 controller emulator of Staubli Robotics Suite, like to a real controller.

Web page: https://underautomation.com/staubli/documentation/simulator

This page explains how to develop with the Staubli SDK without a real robot, with the CS8 or CS9 controller emulator of Staubli Robotics Suite (SRS). The emulator runs the controller software on your PC, and the SDK connects to it like to a real controller.

## Prerequisites

- Staubli Robotics Suite, installed on a Windows PC. It is a Staubli product, with its own license: ask your Staubli contact.
- A cell in SRS with a controller and a robot. Use the controller generation (CS8 or CS9) and the arm of your real cell.
- The emulator of this controller, started from SRS.

## Connect to the emulator

Give the path of the `.controller` file of the emulated controller as address. SRS writes this file in the folder of the controller, inside the folder of the cell, for example `C:\Users\me\Documents\Staubli\SRS\MyCell\Controller1\Controller1.controller`.

```csharp
using UnderAutomation.Staubli;
using UnderAutomation.Staubli.Soap.Data;

public class SimulatorConnect
{
    static void Main()
    {
        // .controller file of the emulated controller, in the folder of the cell of Staubli Robotics Suite.
        // The SOAP client connects to this PC (to the PC of a UNC path), on the SOAP port of the configuration of the emulated controller.
        var parameters = new ConnectionParameters(@"C:\Users\me\Documents\Staubli\SRS\MyCell\Controller1\Controller1.controller");

        var controller = new StaubliController();
        controller.Connect(parameters);

        // Port read from the configuration of the emulated controller (851 when it is not found)
        Console.WriteLine(controller.Soap.Port);

        foreach (Robot robot in controller.Soap.GetRobots())
            Console.WriteLine($"{robot.Arm} ({robot.Kinematic})");

        controller.Disconnect();
    }
}
```

The user and the password are the ones of the emulated controller. The SDK uses `default` and `default` when you do not set them.

### Address and SOAP port

- With a local path, the SDK connects to this PC (`127.0.0.1`). With a UNC path (`\\SRS-PC\share\...\Controller1.controller`), it connects to the PC of the path: allow the SOAP port in its firewall.
- With `Soap.Port` set to `0` (the default), the SDK reads the SOAP port of the emulated controller in its network configuration, the file `usr\configs\network.cfx` next to the `.controller` file. When this file or the port is not found, it uses 851. If the emulator does not answer on 851, the message of the `WebException` says that 851 was used as a fallback: set `Soap.Port` to the port of the emulated controller.
- A path that is not a `.controller` file throws an `ArgumentException`. A `.controller` file that does not exist throws a `FileNotFoundException`.
- You can also give the address of the PC and the port, as for a real controller. The file client then needs an FTP server, and the emulator has none.

### If the connection fails

1. Check that the emulator is started in SRS, and that SRS itself can connect to it.
2. Check the SOAP port of the emulated controller in SRS. When several emulators run on one PC, they cannot all listen on the same port.
3. Set `PingBeforeConnect` to `false` if the ping is blocked.

## Files of the emulated controller

The emulator has no FTP server. It keeps the files of the emulated controller in the folder of its `.controller` file, with the same tree as a real controller (`usr`, `log`). With the `.controller` file as address and the file client enabled, `controller.File` reads and writes the files in this folder, with the same methods and the same paths as on a real controller.

```csharp
using UnderAutomation.Staubli;

public class FilesConnectSimulator
{
    static void Main()
    {
        // Controller emulated by Staubli Robotics Suite on this PC: give its .controller file.
        // The SOAP client connects to 127.0.0.1, the file client uses the folder of the .controller file.
        var parameters = new ConnectionParameters(@"C:\SRS\MyCell\Controller1\Controller1.controller");

        // Emulator on another PC: give a UNC path. The SOAP client connects to this PC.
        // var parameters = new ConnectionParameters(@"\\SRS-PC\SRS\MyCell\Controller1\Controller1.controller");

        parameters.File.Enable = true;

        var controller = new StaubliController();
        controller.Connect(parameters);

        // True: the files are read and written in the folder of the .controller file
        Console.WriteLine(controller.File.IsSimulated);
        Console.WriteLine(controller.File.ControllerFolder);

        controller.Disconnect();
    }
}
```

See [Files overview](files-overview.md).

## What works on the emulator

Every function of the SDK sends the same requests to the emulator and to a real controller:

- the robots, the controller parameters, the DH parameters and the joint ranges;
- the position and the kinematics;
- the power and the motion commands, on the emulated arm;
- the VAL 3 applications and their tasks;
- the I/O of the emulated controller;
- the files and the VAL 3 applications, in the folder of the `.controller` file.

Use the emulator to write and test your application, then run the same code on the real controller with its address.

## Differences with a real controller

- The emulated controller has the I/O boards of its configuration in SRS. Your real cell can have other boards, so the I/O names can differ. Read them with `GetAllPhysicalIos()` on each system.
- Power and motion need the remote mode on the emulated controller too. Set its operating mode in SRS.
- Timings are not the timings of the real controller: do not measure cycle times on the emulator.
- The file client uses the folder of the `.controller` file instead of FTP. `FileException.ReplyCode` is always `0` on the emulator.

## What to read next

- [Connect to your robot](connect.md): all the connection parameters and errors.
- [Demo application](demo-app.md): try the emulator without writing code.
- [Move the robot from a PC](how-to-move-robot.md): test the motion on the emulator first.
