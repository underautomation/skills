---
name: underautomation-staubli-csharp
description: "UnderAutomation Staubli SDK for C# and .NET (NuGet UnderAutomation.Staubli). Use it when code talks to a Staubli robot controller (CS8 or CS9) or to a controller emulated by Staubli Robotics Suite from a PC, or when the user asks about the Staubli SDK, its protocols or its exceptions. Protocols of the SDK: the SOAP server of the controller (TCP port 851) and the FTP server of the controller for the files. It answers questions such as what the controller needs, how to read the joints and the Cartesian position, compute the forward and inverse kinematics, read and write the physical I/O, power the arm and send MoveJJ, MoveJC, MoveL and MoveC moves, load, start and stop VAL 3 applications, suspend and resume tasks, transfer files and VAL 3 projects, and why a CustomSoapException or another exception is thrown. It holds the documentation pages, the C# code samples and the list of every public type and member of the SDK."
metadata:
  sdk-version: 1.0.0
---

# UnderAutomation Staubli SDK for C# and .NET

The UnderAutomation Staubli SDK connects a PC to a Staubli CS8 or CS9 robot controller, or to a controller emulated by Staubli Robotics Suite (SRS), over Ethernet. Nothing is installed on the controller and no VAL 3 program has to run. The main class is `StaubliController` (namespace `UnderAutomation.Staubli`): every SOAP function is a method of `controller.Soap`, and the files of the controller are on `controller.File`.

## Before writing code

1. Run `dotnet list package` in the folder of the project. If `UnderAutomation.Staubli` is missing, ask the user before you install it with `dotnet add package UnderAutomation.Staubli`.
2. Compare its version with `sdk-version` above (1.0.0). A 4th version digit is the same release: for example NuGet 1.0.0.1 and `sdk-version` 1.0.0. If they differ, tell the user: an older package can miss members listed here, a newer one can have members that this skill does not list.
3. When you cannot run commands (claude.ai, ChatGPT), skip the check and tell the user that this skill documents version 1.0.0 of the SDK.

## Choose the function and the controller state

The SDK uses two servers of the controller: the SOAP server (the one that Staubli Robotics Suite uses) and the FTP server for the files. A generic agent does not know what each call needs on the controller. Use this table, then open the page of the topic.

| What the user wants to do | Methods | What the controller needs |
| --- | --- | --- |
| List the arms, read the controller parameters, DH parameters, joint ranges | `Soap.GetRobots`, `GetControllerParameters`, `GetDhParameters`, `GetJointRange` | A user and password of the controller. SOAP server on TCP port 851 |
| Read the joints and the Cartesian position, with a tool and a frame | `Soap.GetCurrentJointPosition`, `GetCurrentCartesianJointPosition` | Nothing more: no remote mode, no power, no VAL 3 program |
| Forward and inverse kinematics | `Soap.ForwardKinematics`, `ReverseKinematics` | A connection: the controller computes them. No offline kinematics in the SDK |
| List, read and write the physical I/O | `Soap.GetAllPhysicalIos`, `ReadIos`, `WriteIos` | A user with the right to write the output. I/O names of the boards of this controller |
| Power the arm, send joint, linear and circular moves, stop, restart, cancel | `Soap.SetPower`, `MoveJJ`, `MoveJC`, `MoveL`, `MoveC`, `StopMotion`, `RestartMotion`, `ResetMotion` | Remote mode, a user with the right to move the arm, no VAL 3 application that moves the arm |
| Load, start, stop and unload a VAL 3 application | `Soap.GetValApplications`, `LoadProject`, `StartApplication`, `StopApplication`, `StopAndUnloadAll` | The project on the disk of the controller, path `Disk://<app>/<app>.pjx` |
| List the VAL 3 tasks, suspend, resume, kill a task | `Soap.GetTasks`, `TaskSuspend`, `TaskResume`, `TaskKill` | The task name and its creator, as returned by the list |
| Upload, download, list, rename and delete files, send a VAL 3 application folder | `File.GetListing`, `UploadFileToController`, `DownloadFileFromController`, `UploadApplicationToController` | `File.Enable = true` in the connection parameters. FTP server of the controller (port 21, its own user and password). On the SRS emulator: the folder of the `.controller` file, no FTP |

- The SDK has no method to read or write VAL 3 variables, and no event subscription: poll the state. Do not invent methods for them. To exchange values with a VAL 3 program, use I/O or files.
- Units: joints and Cartesian rotations in radians, Cartesian X, Y, Z in meters. Convert in the code when the user works in millimeters and degrees. See [SOAP overview](references/pages/soap-overview.md).
- The `robot` argument is the index of the arm in `GetRobots()`: pass `0` for a controller with one arm.
- A move method returns when the controller has accepted the move, not when the arm has reached the target. Test `ReturnCode == MotionReturnCode.Success`, then poll the position to wait for the end. Call `ResetMotion()` after a refused move, before new moves.
- Every move takes a `MotionDesc`. Set `Frequency` to 100: the default 0 is refused by the controller. Keep the configuration of the arm with `Config = fk.Config` of the current position, otherwise the arm can take an unexpected path. Start from the values of the checked examples, for example [Move the robot from a PC](references/pages/how-to-move-robot.md): `Velocity`, `Acceleration`, `Deceleration` 0.1, `TranslationVelocity`, `RotationVelocity` 0.05. Some API summaries give these limits in percent or in mm/s: do not write larger values such as 10 or 50 because of them. Raise the values step by step on the emulator.
- `SetPower` returns a `PowerReturnCode`: test it. `OnlyInRemoteMode` means that the controller is not in remote mode. A move that returns `NotReady` usually means that the arm is not powered.
- I/O names contain the board, a backslash and the I/O, for example `BasicIO-1\%I0`. Read them with `GetAllPhysicalIos()`, never guess them. Write them as verbatim strings (`@` before the string). Check `State == PhysicalIoEnumState.Defined` before using a value that was read.
- A controller refusal throws a `CustomSoapException`: read `ErrorCode` (a `SoapErrorCode`, for example `InvalidCredentials`, `InvalidSessionIdCode`, `WriteAccessErrorCode`, `ApplicationNotFound`, `TaskNotFound`) and `Description`. No answer on the SOAP port gives a `WebException`. The ping before the connection fails with "Unable to ping robot at address ...": set `PingBeforeConnect` to `false` when ICMP is blocked. See [Connect to your robot](references/pages/connect.md).
- Starting a VAL 3 application (`Soap.StartApplication`) can move the arm: "Motion safety" applies, as for a move command.
- SRS emulator: pass the path of the `.controller` file instead of an IP address. The SOAP port is read from the configuration of the emulated controller. See [Test with the Staubli Robotics Suite emulator](references/pages/simulator.md).
- The file client has asynchronous twins (`...Async`, optional `CancellationToken`), except on .NET Framework 3.5 and 4.0. The SOAP methods are synchronous.

The how-to pages give complete programs per task: [Get the robot position](references/pages/how-to-get-position.md), [Read and write I/O](references/pages/how-to-read-write-io.md), [Move the robot from a PC](references/pages/how-to-move-robot.md) and [Run a VAL 3 program](references/pages/how-to-run-program.md).

## Connect and license

Create a `StaubliController`, then connect. `Connect(ip)` uses the default parameters: SOAP on port 851, user `default`, password `default`, file client disabled. For another user or for the files, use `ConnectionParameters`. Always disconnect at the end. See [Connect to your robot](references/pages/connect.md).

```csharp
using UnderAutomation.Staubli;

public class Connect
{
    static void Main()
    {
        var parameters = new ConnectionParameters("192.168.0.254");

        // Ping the controller first, so an unreachable controller fails in 100 ms
        parameters.PingBeforeConnect = true;

        parameters.Soap.Enable = true;
        // 0 (default): automatic, 851 on a real controller (SoapConnectParameters.DEFAULT_PORT)
        parameters.Soap.Port = 0;
        parameters.Soap.User = "default";
        parameters.Soap.Password = "default";

        var controller = new StaubliController();
        controller.Connect(parameters);

        controller.Disconnect();
    }
}
```

The SDK runs 30 days without a license key. With a key, register it once at startup, before the first connection. Without a valid license, the connection throws an `InvalidLicenseException`. See [Licensing](references/pages/license.md).

```csharp
using UnderAutomation.Staubli;
using UnderAutomation.Staubli.License;

public class License
{
    static void Main()
    {
        // Register the license once, before the first connection
        StaubliController.RegisterLicense("YourCompanyName", "YOUR_LICENSE_KEY");

        LicenseInfo info = StaubliController.LicenseInfo;

        // Number of trial days remaining
        int? evaluationDaysLeft = info.EvaluationDaysLeft;

        bool licenseValid = info.State == LicenseState.Licensed;

        // A readable description of the current state
        Console.WriteLine(info);

        // Check the license once at startup, rather than catching
        // the exception on every connection
        if (!info.IsLicensed)
        {
            Console.WriteLine(info);
            return;
        }

        try
        {
            var controller = new StaubliController();
            controller.Connect("192.168.0.254");
        }
        catch (InvalidLicenseException ex)
        {
            Console.WriteLine(ex.Message);
            Console.WriteLine(ex.LicenseInfo.State);
        }
    }
}
```

## Motion safety

- Never start a motion, a program or an output that can move the robot unless the user asked for it.
- A generated program that moves the robot does not move by default. It first prints what it will do (program, targets, speed), then asks for a typed confirmation, or it needs an explicit option such as `--run`.
- In the generated code, use the lowest speed the API allows: a low override, or low speed limits in the motion parameters (see the notes of the brand in this file). Show where to change it.
- The SDK has no speed override: the speed comes from the limits of the `MotionDesc` of each move. Start with 0.1 for the joint limits and 0.05 for the Cartesian limits, the values of [Move the robot from a PC](references/pages/how-to-move-robot.md). Never write 10 or 50, even when an API summary gives the limit in percent or in mm/s.
- When the controller allows it, tell the user to run the first test in manual mode at reduced speed, with the enabling device in hand.
- Tell the user to check the work area before the first run: nobody in the cell, no obstacle on the path, every target reachable.
- Propose a first test on a virtual robot: [Test with the Staubli Robotics Suite emulator](references/pages/simulator.md).
- The SDK does not replace the safety functions of the controller (emergency stop, safety fences, collision detection).

## Rules for the agent

- Use only the types and members listed in `references/api`. Search `references/api/index.md` for a type, then open the file of its namespace.
- If a member seems missing, do not guess it: read the XML documentation of the NuGet package: `~/.nuget/packages/underautomation.staubli/<version>/lib/<framework>/UnderAutomation.Staubli.xml`.
- Start from the code samples of `references/pages`: they compile against this version of the SDK.
- For an exception, read `references/errors.md`.
- When the answer depends on the controller (model, software version, options, settings), ask the user.

## Index of the references

- [API index](references/api/index.md): every public type, with the file of its namespace.
- [Errors](references/errors.md): exceptions of the SDK, when they are thrown, what to check.
- [Get started: Get started with .NET](references/pages/get-started-net.md): Add the Staubli SDK to a C# or VB.NET project from NuGet or as a DLL, and write a first program for a CS8 or CS9 controller. One managed DLL, no dependency, .NET Framework 3.5 to .NET 10.
- [Get started: Try the SDK with the demo application](references/pages/demo-app.md): A Windows application, one executable and open source, that calls every function of the SDK. Test what your Staubli controller answers before you write any code.
- [Get started: Connect to your robot](references/pages/connect.md): Connect to a CS8 or CS9 controller over its SOAP server: network, port, user and password, connection parameters, errors and disconnection.
- [Get started: Test with the Staubli Robotics Suite emulator](references/pages/simulator.md): Develop without a real robot. Connect the SDK to the CS8 or CS9 controller emulator of Staubli Robotics Suite, like to a real controller.
- [Get started: Licensing](references/pages/license.md): The 30 day trial, the license key and RegisterLicense, the license states, the maintenance and the source license of the Staubli SDK.
- [SOAP: SOAP overview](references/pages/soap-overview.md): The SOAP server of CS8 and CS9 controllers, what the SDK does with it, the units, and the list of topics: robots, position, kinematics, motion, I/O, applications and tasks.
- [SOAP: Controller and robots](references/pages/soap-controller.md): List the robots of a Staubli controller, read the controller parameters, the Denavit-Hartenberg parameters and the joint ranges of each arm.
- [SOAP: Position](references/pages/soap-position.md): Read the current joints and the Cartesian position of a Staubli robot, for the flange or a tool, in the world frame or in another frame.
- [SOAP: Kinematics](references/pages/soap-kinematics.md): Compute the forward and inverse kinematics of a Staubli robot on the controller, with the configuration of the arm and the joint ranges.
- [SOAP: Motion](references/pages/soap-motion.md): Power the arm, set the motion descriptor, send MoveJJ, MoveJC, MoveL and MoveC moves, then stop, restart or cancel them.
- [SOAP: Inputs and outputs](references/pages/soap-io.md): List the physical I/O of a Staubli controller, read several I/O in one request and write outputs, without a VAL 3 program.
- [SOAP: VAL 3 applications](references/pages/soap-applications.md): List the VAL 3 applications of a Staubli controller, load a project from its disk, start it, stop it and unload it from a PC.
- [SOAP: VAL 3 tasks](references/pages/soap-tasks.md): List the VAL 3 tasks with their state, program line and runtime error, then suspend, resume or kill a task.
- [Files: Files overview](references/pages/files-overview.md): Access the files of a CS8 or CS9 controller: FTP server of a real controller, or .controller file of a controller emulated by Staubli Robotics Suite. Connection, paths, /usr/usrapp and errors.
- [Files: List and transfer files](references/pages/files-transfer.md): List the files of a Staubli controller, upload and download files, create, rename and delete files and folders, with synchronous and asynchronous methods.
- [Files: Send a VAL 3 application](references/pages/files-applications.md): Send the folder of a VAL 3 application to /usr/usrapp on the controller in one call, then load and start it with the SOAP methods.
- [How-To Articles: Get the robot position](references/pages/how-to-get-position.md): Read the position of a Staubli robot from C# or Python: joints, flange or tool position, and which method to choose. Complete program included.
- [How-To Articles: Read and write I/O](references/pages/how-to-read-write-io.md): Find the I/O names, wait for an input and switch an output of a Staubli CS8 or CS9 controller from C# or Python.
- [How-To Articles: Move the robot from a PC](references/pages/how-to-move-robot.md): Power the arm and move a Staubli robot in a straight line from C# or Python, without a VAL 3 program. Which move to choose, and the frequent errors.
- [How-To Articles: Run a VAL 3 program](references/pages/how-to-run-program.md): Load a VAL 3 project from the disk of the controller, start it, check its tasks and stop it, from C# or Python.
- [How-To Articles: Monitor the state of the robot](references/pages/how-to-monitor-state.md): Poll the applications and the VAL 3 tasks of a Staubli controller, print each change of state and each runtime error.
