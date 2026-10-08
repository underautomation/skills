---
name: underautomation-fanuc-csharp
description: "UnderAutomation Fanuc SDK for C# and .NET (NuGet UnderAutomation.Fanuc). Use it when code talks to a Fanuc robot controller (R-30iA, R-30iB, R-30iB Plus, R-50iA) or a ROBOGUIDE virtual robot from a PC, or when the user asks about the Fanuc SDK, its protocols or its exceptions. Protocols of the SDK: CGTP web server, SNPX (Robot Interface), Telnet KCL, FTP, RMI (option R912) and Stream Motion (option J519). It answers questions such as which protocol and which controller option to use, how to read and write registers, variables and I/O, how to run a TP program, read the position or the alarms, transfer files, move the robot, plan a trajectory, compute the kinematics offline, and why an exception is thrown. It holds the documentation pages, the C# code samples and the list of every public type and member of the SDK."
metadata:
  sdk-version: 7.1.0
---

# UnderAutomation Fanuc SDK for C# and .NET

The UnderAutomation Fanuc SDK connects a PC to a Fanuc robot controller (R-J3iB, R-30iA, R-30iB, R-30iB Plus, R-50iA) or to a ROBOGUIDE virtual robot over Ethernet, with nothing to install on the controller. The main class is `FanucRobot` (namespace `UnderAutomation.Fanuc`): each protocol of the controller is a property of it, enabled on its own in `ConnectionParameters`.

## Before writing code

1. Run `dotnet list package` in the folder of the project. If `UnderAutomation.Fanuc` is missing, ask the user before you install it with `dotnet add package UnderAutomation.Fanuc`.
2. Compare its version with `sdk-version` above (7.1.0). A 4th version digit is the same release: for example NuGet 7.1.0.1 and `sdk-version` 7.1.0. If they differ, tell the user: an older package can miss members listed here, a newer one can have members that this skill does not list.
3. When you cannot run commands (claude.ai, ChatGPT), skip the check and tell the user that this skill documents version 7.1.0 of the SDK.

## Choose the protocol

A generic agent does not know which protocol of the controller gives which data, nor which option it needs. Use this table, then open the page of the protocol.

| What the user wants to do | Protocol | Controller option or setting |
| --- | --- | --- |
| Read and write registers (R, PR, SR, flags), I/O, system and Karel variables, current position, alarms, task status, about 2 ms per request | SNPX | R553 "HMI Device SNPX" with the FANUC America parameters (R650 FRA). No option with the FANUC Ltd. parameters (R651 FRL). TCP port 60008 |
| Manage and run TP programs, read and write any variable, registers with their comments, simulate I/O, read the position, online kinematics, list and download files, KCL commands | CGTP (web server of the controller) | No option. Firmware V8.30 or later. Program management and position: V9.10. Run a program: V9.30. File listing: V9.40. Port 80 or 3080 |
| Send TP-like motions (joint, linear, circular, spline) from the PC, the controller plans them | RMI | R912 Remote Motion Interface. AUTO mode, teach pendant disabled. TCP port 16001 |
| Give the position at every cycle (2, 4 or 8 ms): computed paths, sensor guided motion, teleoperation | Stream Motion | J519. A TP program with `IBGN start` and `IBGN end`, run in AUTO mode at 100% override. UDP port 60015 |
| Upload, download, delete and back up files, read variable files, safety status, error history, installed options | FTP | No option. Upload of programs needs a user with enough rights (for example INSTALL) |
| Send KCL commands to a controller older than V8.30 | Telnet KCL | No option. Telnet enabled with a password. Legacy: prefer the KCL client of CGTP on V8.30 and later |
| Jog the robot in real time with a joystick or a 6D mouse | SNPX and DPM | R739 Dynamic Path Modification, plus the SNPX option above |
| Plan a trajectory, compute forward and inverse kinematics, parse controller files | Motion planner, kinematics, file parsers (offline) | No connection to a controller |

- Several protocols can be enabled together. Each one has its own TCP port: the firewalls between the PC and the controller must let it through.
- The speeds of the table are measured values: SNPX about 2 ms, CGTP 10 to 50 ms, Telnet and FTP 30 to 100 ms. For many values, use the batch reads of SNPX or CGTP.
- The installed options can be read with FTP: `robot.Ftp.GetSummaryDiagnostic().Features`, see [Diagnostics & variables](references/pages/ftp-diagnostics.md). This object is not a list. It has flags such as `HasSnpx`, `HasTelnet` and `HasStreamMotion`. For the other options, for example R912, search the `Name` and `OrderNo` of the items of `FeaturesList`.
- The active alarms can be read with SNPX, `robot.Snpx.ActiveAlarm.Read(1)`, or without option with CGTP, `robot.Cgtp.Http.GetAllErrorsList().FilterActiveAlarms()`. FTP has the same `GetAllErrorsList()`. See [Reset alarms remotely](references/pages/how-to-reset-fanuc-alarm-remotely.md).
- Stream Motion or RMI: RMI for a few moves that the robot plans, Stream Motion for a path that changes in real time. Both move the robot: read "Motion safety" below.
- Starting a TP program from the PC (`robot.Cgtp.RunProgram`, KCL `Run`, SNPX start signals) is a motion command: "Motion safety" applies. In the generated code, set the general override to a low value by default before the start, for example write 10 to the system variable `$MCR.$GENOVERRIDE` with `robot.Cgtp.WriteVariable`, and ask for a confirmation.
- RMI: a `ConnectException` with the message "Connection refused by controller" is not a network problem. The controller answered and refused the RMI session, and the inner `RmiException` gives the error id of the controller. Check option R912, the active alarms, and that no other RMI session is open: a session that was not ended with `Abort()` or `Disconnect()` keeps `RMI_MOVE` selected.
- ROBOGUIDE: pass the folder of the virtual robot instead of an IP address, see [Test with ROBOGUIDE](references/pages/simulator.md).

The comparison tables of the how-to pages give the details per task, for example [Access Karel program variables](references/pages/access-karel-program-variables.md), [Get current position](references/pages/get-current-position.md) and [Run a program remotely](references/pages/run-program-remotely.md).

## Connect and license

Create a `FanucRobot`, enable the protocols you need in `ConnectionParameters`, then connect. Without parameters, `Connect(ip)` enables CGTP only. Always disconnect at the end. See [Connect to your robot](references/pages/connect.md).

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common;

public class Connect
{
  static void Main()
  {
    // Create a robot instance
    FanucRobot robot = new FanucRobot();

    // Configure connection parameters
    ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");

    // Enable Telnet KCL for remote commands
    parameters.Telnet.Enable = true;
    parameters.Telnet.TelnetKclPassword = "your_password";

    // Enable FTP for file and variable access
    parameters.Ftp.Enable = true;
    parameters.Ftp.FtpUser = "";
    parameters.Ftp.FtpPassword = "";

    // Enable SNPX for high-speed register and I/O access
    parameters.Snpx.Enable = true;

    // Enable CGTP Web Server (enabled by default)
    parameters.Cgtp.Enable = true;

    // Enable RMI for remote motion commands
    parameters.Rmi.Enable = true;

    // Connect to the robot
    robot.Connect(parameters);

    // Check connection status
    bool isConnected = robot.Enabled;

    // Disconnect when done
    robot.Disconnect();
  }
}
```

The SDK runs 30 days without a license key. With a key, register it once at startup, before the first connection. Without a valid license, the connection throws an `InvalidLicenseException`. The offline features (kinematics, motion planner, file parsers) do not need a connection. See [Licensing](references/pages/license.md).

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.License;

public class License
{
    static void Main()
    {
        // Register the license once, before the first connection
        FanucRobot.RegisterLicense("YourCompanyName", "YOUR_LICENSE_KEY");

        LicenseInfo info = FanucRobot.LicenseInfo;

        // Number of trial days remaining
        int? evaluationDaysLeft = info.EvaluationDaysLeft;

        bool licenseValid = info.State == LicenseState.Licensed;

        // A readable description of the current state
        Console.WriteLine(info);

        // Check the license once at startup, rather than catching the exception
        // on every connection
        if (!FanucRobot.LicenseInfo.IsLicensed)
        {
            Console.WriteLine(FanucRobot.LicenseInfo);
            return;
        }
    }
}
```

## Motion safety

- Never start a motion, a program or an output that can move the robot unless the user asked for it.
- A generated program that moves the robot does not move by default. It first prints what it will do (program, targets, speed), then asks for a typed confirmation, or it needs an explicit option such as `--run`.
- In the generated code, use the lowest speed the API allows: a low override, or low speed limits in the motion parameters (see the notes of the brand in this file). Show where to change it.
- When the controller allows it, tell the user to run the first test in manual mode at reduced speed, with the enabling device in hand.
- Tell the user to check the work area before the first run: nobody in the cell, no obstacle on the path, every target reachable.
- Propose a first test on a virtual robot: [Test with ROBOGUIDE](references/pages/simulator.md).
- The SDK does not replace the safety functions of the controller (emergency stop, safety fences, collision detection).

## Rules for the agent

- Use only the types and members listed in `references/api`. Search `references/api/index.md` for a type, then open the file of its namespace.
- If a member seems missing, do not guess it: read the XML documentation of the NuGet package: `~/.nuget/packages/underautomation.fanuc/<version>/lib/<framework>/UnderAutomation.Fanuc.xml`.
- Start from the code samples of `references/pages`: they compile against this version of the SDK.
- For an exception, read `references/errors.md`.
- When the answer depends on the controller (model, software version, options, settings), ask the user.

## Index of the references

- [API index](references/api/index.md): every public type, with the file of its namespace.
- [Errors](references/errors.md): exceptions of the SDK, when they are thrown, what to check.
- [Get started: Get started with .NET](references/pages/get-started-net.md): Add the Fanuc SDK to a C# or VB.NET project from NuGet or as a DLL, and write a first program for a Fanuc controller or ROBOGUIDE. One managed DLL, .NET Framework 3.5 to .NET Standard 2.1.
- [Get started: Try the SDK with the demo application](references/pages/demo-app.md): A Windows application, one executable and open source, that calls the features of the SDK. Test what your Fanuc controller answers before you write any code.
- [Get started: Connect to your robot](references/pages/connect.md): The protocols of the SDK, their options and setup on the controller, the connection parameters, and the connection to a real Fanuc robot or to ROBOGUIDE.
- [Get started: Test with ROBOGUIDE](references/pages/simulator.md): Develop without a real robot. Connect the SDK to a virtual robot of FANUC ROBOGUIDE with the folder of the robot, like to a real controller.
- [Get started: Licensing](references/pages/license.md): The 30 day trial, the license key and RegisterLicense, the license states, the maintenance and the source license of the Fanuc SDK.
- [CGTP: CGTP overview](references/pages/cgtp.md): CGTP is an HTTP-based protocol providing the richest feature set: program management, variables, registers, I/O, kinematics, batch operations, and file access.
- [CGTP: Program management](references/pages/cgtp-programs.md): Create, delete, rename, run, pause, abort programs and manage their attributes (comment, owner, subtype) via CGTP.
- [CGTP: Registers & variables](references/pages/cgtp-registers-variables.md): Read and write numeric, position, and string registers, system variables, and perform batch operations via CGTP.
- [CGTP: Inputs & Outputs](references/pages/cgtp-io.md): Read, write, simulate, and unsimulate digital, analog, group, and robot I/O ports via CGTP.
- [CGTP: Position & kinematics](references/pages/cgtp-position-kinematics.md): Read current Cartesian and joint positions, and compute forward and inverse kinematics directly on the controller via CGTP.
- [CGTP: Alarms, comments & files](references/pages/cgtp-alarms-files.md): Manage user alarms, read/write register and I/O comments, list and download files from the controller via CGTP.
- [CGTP: KCL commands](references/pages/cgtp-kcl.md): Send KCL commands through the web server instead of Telnet. Unsafe commands without result, and when to use RunProgram.
- [SNPX: SNPX overview](references/pages/snpx.md): SNPX (also known as RobotIF or SRTP) is a high-speed protocol for reading and writing registers, variables, I/O signals, alarms, and positions in less than 2 ms.
- [SNPX: Registers](references/pages/snpx-registers.md): Read and write numeric registers (R[]), position registers (PR[]), string registers (SR[]), and flags (F[]) via SNPX.
- [SNPX: Inputs & Outputs](references/pages/snpx-io.md): Read and write digital signals (SDI, SDO, RDI, RDO, UI, UO, SI, SO, WI, WO) and numeric I/O (GI, GO, AI, AO) via SNPX.
- [SNPX: System variables](references/pages/snpx-variables.md): Read and write integer, real, position, and string system variables on the Fanuc controller via SNPX.
- [SNPX: Current position](references/pages/snpx-position.md): Read the current robot position in world coordinates or user frame coordinates, for single or multi-group controllers.
- [SNPX: Alarms & task status](references/pages/snpx-alarms-tasks.md): Read active alarms, alarm history, clear alarms, monitor running tasks, and read/write comments via SNPX.
- [SNPX: Batch reading](references/pages/snpx-batch.md): Read groups of registers, variables, or signals in a single command for maximum performance using SNPX batch assignments.
- [Telnet: Telnet overview](references/pages/telnet.md): Telnet KCL (Keyboard Command Line) sends commands to a Fanuc robot: run programs, reset alarms, read and write variables, control I/O ports.
- [Telnet: Enable Telnet on your robot](references/pages/telnet-enable-on-robot.md): TELNET is natively available on ROBOGUIDE and all Fanuc robots without any option. Learn how to enable it step by step.
- [Telnet: Program control via Telnet](references/pages/telnet-program-control.md): Run, pause, hold, continue, and abort TP and Karel programs remotely using Telnet KCL commands.
- [Telnet: Variables & I/O via Telnet](references/pages/telnet-variables-io.md): Read and write system variables, set output ports, simulate and unsimulate input ports using Telnet KCL.
- [Telnet: Debugging & breakpoints](references/pages/telnet-debugging.md): Add, remove, and manage breakpoints on TP and Karel programs. Step through code line by line using Telnet KCL.
- [FTP: FTP overview](references/pages/ftp.md): FTP provides access to internal controller files including variables, programs, diagnostics, safety status, and current position.
- [FTP: File management](references/pages/ftp-file-management.md): Upload, download, delete, rename files and directories on the Fanuc robot controller via FTP.
- [FTP: Diagnostics & variables](references/pages/ftp-diagnostics.md): Read safety status, current position, I/O state, installed features, error history, registers, and system variables via FTP.
- [RMI: RMI overview](references/pages/rmi.md): RMI (Remote Motion Interface) is a TCP-based protocol for sending motion commands, managing frames, and controlling the robot remotely.
- [RMI: Motion commands](references/pages/rmi-motion.md): Send linear, joint, and circular motion commands with configurable speed, termination type, and acceleration via RMI.
- [RMI: Frames, I/O & status](references/pages/rmi-frames-io.md): Manage user frames and tools, read/write I/O, read positions, set speed override, and get controller status via RMI.
- [Stream Motion: Stream Motion overview](references/pages/stream-motion.md): Stream Motion (J519 option) gives the position of the robot at every communication cycle (2 to 8 ms). Requirements, TP program, protocol versions and quick start.
- [Stream Motion: Connection, status & session](references/pages/stream-motion-session.md): Connect to the robot, read its status and its velocity, acceleration and jerk limits, and run one or several Stream Motion sessions.
- [Stream Motion: Send trajectories](references/pages/stream-motion-trajectories.md): Queue joint or Cartesian trajectories, send your own positions, and control the motion with override, pause and abort.
- [Stream Motion: Real-time control](references/pages/stream-motion-real-time.md): Make the robot follow a target that changes at any time, or compute the position of the robot at every cycle with a callback.
- [Stream Motion: I/O during motion](references/pages/stream-motion-io.md): Read and write digital I/O with each position sent to the robot, and switch outputs at a precise point of a trajectory.
- [Stream Motion: Troubleshooting & best practices](references/pages/stream-motion-troubleshooting.md): Handle Stream Motion errors, understand the usual MOTN alarms, and follow the good practices for smooth and reliable motions.
- [Motion: Motion planner overview](references/pages/motion.md): Create smooth robot trajectories offline, with velocity, acceleration and jerk limits, using FANUC motion instructions (J, L, C, FINE, CNT, CR).
- [Motion: Joint & Cartesian motions](references/pages/motion-moves.md): Chain joint, linear and circular motions with FINE, CNT and CR terminations, waits and I/O, in tool and user frames.
- [Motion: Splines & shapes](references/pages/motion-splines-shapes.md): Pass through a list of points with a smooth spline, and draw circles, rectangles, polygons, helices and spirals in any plane.
- [Motion: Trajectories from points](references/pages/motion-trajectory-from-points.md): Create trajectories from your own positions, sampled or timed, check them against the limits of the robot, and slow them down if needed.
- [Motion: Frames & orientations](references/pages/motion-frames-orientations.md): Convert W, P, R angles to quaternions, interpolate orientations, and change frames between flange, tool, user frame and world frame.
- [Offline tools: Forward & Inverse Kinematics](references/pages/kinematics.md): Perform forward and inverse kinematics calculations offline for FANUC industrial robots and CRX cobots using DH parameters.
- [Offline tools: Offline file parsing](references/pages/offline-file-parsing.md): Parse and decode Fanuc variable files (.va), error lists (.ls), I/O state, safety status, and current position files without a robot connection.
- [How-To Articles: Read & write registers](references/pages/how-to-read-write-fanuc-registers.md): Compare all methods to read and write numeric, position, and string registers on a Fanuc robot: SNPX, FTP, CGTP, and Telnet.
- [How-To Articles: Get current position](references/pages/get-current-position.md): Retrieve the current robot position (joint and Cartesian) using SNPX, FTP, CGTP, or Telnet. Compare approaches and choose the best for your use case.
- [How-To Articles: Control inputs & outputs](references/pages/set-and-simulate-inputs-outputs.md): Set, read, simulate, and unsimulate I/O ports on a Fanuc robot using SNPX, CGTP, or Telnet. Compare port types and methods.
- [How-To Articles: Run a program remotely](references/pages/run-program-remotely.md): Start, pause, abort, and monitor Fanuc programs remotely using Telnet, CGTP, SNPX system variables, or RMI.
- [How-To Articles: Reset alarms remotely](references/pages/how-to-reset-fanuc-alarm-remotely.md): Clear and reset alarms on a Fanuc robot using SNPX, Telnet, or CGTP. Read active alarms and alarm history.
- [How-To Articles: Read & write system variables](references/pages/read-write-system-variables.md): Access and modify Fanuc system variables ($RMT_MASTER, $MCR.$GENOVERRIDE, etc.) using Telnet, SNPX, CGTP, or FTP.
- [How-To Articles: Monitor task execution](references/pages/monitor-task-execution.md): Supervise running programs, check task states, line numbers, and calling programs using SNPX, FTP, or Telnet.
- [How-To Articles: Move robot remotely](references/pages/move-robot-remotely.md): Move a Fanuc robot from an external application using RMI motion commands, Stream Motion real-time streaming, or DPM with SNPX.
- [How-To Articles: Upload, download & backup files](references/pages/upload-download-backup-files.md): Transfer TP programs, variable files, and backups between your PC and a Fanuc controller using FTP or CGTP.
- [How-To Articles: Read & write I/O comments](references/pages/read-write-io-comments.md): Read and write comments (descriptions) for registers and I/O ports using SNPX or CGTP.
- [How-To Articles: Access Karel program variables](references/pages/access-karel-program-variables.md): Read and write Karel program variables using SNPX ($[Program]Variable syntax), CGTP, or FTP variable files.
- [How-To Articles: Optimize with batch operations](references/pages/optimize-performance-batch-operations.md): Maximize read/write performance using SNPX batch assignments and CGTP batch variables for high-frequency data exchange.
- [How-To Articles: Move robot with mouse](references/pages/move-robot-with-mouse.md): Control a FANUC robot in real time using Dynamic Path Modification (DPM) and SNPX. Ideal for joystick or 6D mouse teleoperation setups.
- [How-To Articles: TP editor with breakpoints](references/pages/tp-editor-with-breakpoints.md): Prototype your own TP Editor with syntax highlighting and breakpoint debugging using Telnet and FTP features.
