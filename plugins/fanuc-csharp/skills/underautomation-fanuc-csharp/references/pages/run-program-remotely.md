# Run a program remotely

Start, pause, abort, and monitor Fanuc programs remotely using Telnet, CGTP, SNPX system variables, or RMI.

Web page: https://underautomation.com/fanuc/documentation/run-program-remotely

This article compares the ways to start, pause and abort the TP programs of a Fanuc controller from a PC with the Fanuc SDK: Telnet KCL, CGTP, RMI and SNPX. The table at the end says which protocol supports which command.

## Telnet KCL

Telnet provides the most complete program control through KCL commands:

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Telnet;

public class TelnetProgramControl
{
  static void Main()
  {
    FanucRobot robot = new FanucRobot();
    ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");
    parameters.Telnet.Enable = true;
    parameters.Telnet.TelnetKclPassword = "TELNET_PASS";
    robot.Connect(parameters);

    // Run a program
    robot.Telnet.Run("MyProgram");

    // Pause (stops at next fine point)
    robot.Telnet.Pause("MyProgram");

    // Hold (decelerates and stops at current position)
    robot.Telnet.Hold("MyProgram");

    // Resume a paused or held program
    robot.Telnet.Continue("MyProgram");

    // Abort a program
    robot.Telnet.Abort("MyProgram", force: true);

    // Abort all running programs
    robot.Telnet.AbortAll(force: true);

    // Reset alarms (same as FAULT RESET button)
    robot.Telnet.Reset();

    // Clear program variables
    robot.Telnet.ClearVars("MyProgram");
  }
}
```

See also: [Telnet Program control](telnet-program-control.md)

## CGTP Web Server

CGTP can run, select, pause, and abort programs, plus manage program properties:

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Cgtp;

public class CgtpPrograms
{
  public static void Main()
  {
    FanucRobot robot = new FanucRobot();

    ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");
    parameters.Cgtp.Enable = true;

    robot.Connect(parameters);

    // Run a program
    robot.Cgtp.RunProgram("MY_PROGRAM");

    // Run from a specific line
    robot.Cgtp.RunProgram("MY_PROGRAM", lineNum: 10);

    // Select a program
    robot.Cgtp.SelectProgram("MY_PROGRAM");

    // Abort a task
    robot.Cgtp.AbortTask("MY_PROGRAM");

    // Pause all programs
    robot.Cgtp.PauseAllPrograms();

    // Create a program
    robot.Cgtp.CreateProgram(
        progName: "NEW_PROG",
        owner: "UnderAutomation",
        comment: "Created via CGTP",
        subType: CgtpProgramSubType.Job
    );

    // Delete a program
    robot.Cgtp.DeleteProgram("OLD_PROG");

    // Rename a program
    robot.Cgtp.RenameProgram("OLD_NAME", "NEW_NAME");

    // List all TP programs
    string[] programs = robot.Cgtp.ListTpPrograms();

    // Edit source code (firmware V9.10+)
    robot.Cgtp.InsertSourceLine("MY_PROGRAM", "L P[5] 100mm/sec FINE", 3);
    robot.Cgtp.ReplaceSourceLine("MY_PROGRAM", "J P[1] 50% FINE", 5);
    robot.Cgtp.DeleteSourceLines("MY_PROGRAM", 4, 2);

    // Read program properties
    string comment = robot.Cgtp.GetProgramComment("MY_PROGRAM");
    string owner = robot.Cgtp.GetProgramOwner("MY_PROGRAM");
    bool ignorePause = robot.Cgtp.GetProgramIgnorePause("MY_PROGRAM");

    // Write program properties
    robot.Cgtp.SetProgramComment("MY_PROGRAM", "Updated comment");
    robot.Cgtp.SetProgramSubType("MY_PROGRAM", CgtpProgramSubType.Macro);
  }
}
```

See also: [CGTP Program management](cgtp-programs.md)

## RMI

RMI sends TP-equivalent motion instructions directly, without selecting a program:

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common;
using UnderAutomation.Fanuc.Rmi.Data;
using UnderAutomation.Fanuc.Rmi.TpInstructions;

public class RunProgramRemotelyRmi
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");
        parameters.Rmi.Enable = true;
        robot.Connect(parameters);

        // Start the RMI_MOVE program on the controller
        robot.Rmi.Initialize();

        // Send a linear motion, the SDK gives the sequence ID
        robot.Rmi.SendTpInstruction(new LinearMotionTpInstruction
        {
            SpeedType = RmiLinearSpeedType.MmSec,
            Speed = 100,
            TermType = RmiTerminationType.Fine,
            Target = new CartesianPositionWithUserFrame(500, 200, 300, 0, 90, 0, 1, 0)
        });

        // Pause, continue, then stop the RMI_MOVE program
        robot.Rmi.Pause();
        robot.Rmi.Continue();
        robot.Rmi.Abort();

        robot.Disconnect();
    }
}
```

See also: [RMI overview](rmi.md)

## SNPX (indirect)

### Select the program

Set the program name using the `$SHELL_WRK.$CUST_NAME` system variable. Do not include the `.TP` extension. The code is at the end of this section.

### Enable remote control

To allow external control, set the system variable `$RMT_MASTER` to `1`, and `$REMOTE_CFG.$REMOTE_TYPE` to `1`: the master device is then KCL, which allows a program to be started from the PC. The same values are needed to run a program with Telnet KCL or CGTP.

### Option 1: start with a system variable (Production Start Method = OTHER)

When **Production Start Method** is set to **OTHER**, trigger the start by setting `$SHELL_WRK.$CUST_START` to `1`.

The controller automatically clears this bit once it acknowledges the command.

### Option 2: UOP Cycle Start (Production Start Method = UOP)

This method uses the UI (User Input) signals, which also give the other commands of the next section.

**Step 1: map the UI signals to flags.** Open `MENU`, `I/O`, `UOP`, select `UI`, then `CONFIG`.

Link UI signals to Flags (Rack 34, Slot 1):

| Configuration | Result |
|---------------|--------|
| UI[1-8] to Rack 34, Slot 1, Start 1 | UI[1]=F[1], UI[2]=F[2], ... UI[8]=F[8] |
| UI[1-8] to Rack 34, Slot 1, Start 4 | UI[1]=F[4], UI[2]=F[5], ... UI[8]=F[11] |
| UI[6-6] to Rack 34, Slot 1, Start 9 | UI[6]=F[9] |

> The mapping is **bidirectional**: read UI state from flags, or write to flags to change UI state.

**Cold start** the controller after configuration.

**Step 2: pulse the Cycle Start flag.** To start the program, pulse the flag mapped to UI[6:Cycle Start].

## Controlling Program Execution via UOP

The UI signals of the UOP interface control the execution:

| UI Signal | Name | Function | Code Example |
|-----------|------|----------|--------------|
| UI[2] | Hold | Pause program execution | `robot.Snpx.Flags.Write(2, false);` |
| UI[4] | Cycle Stop | Stop the current cycle | `robot.Snpx.Flags.Write(4, false);` |
| UI[5] | Fault Reset | Clear active alarms | `robot.Snpx.Flags.Write(5, true);` |
| UI[6] | Cycle Start | Start/resume program | `robot.Snpx.Flags.Write(6, true);` |
| UI[18] | Prod Start | Alternative production start | `robot.Snpx.Flags.Write(18, true);` |

> **Note:** You can also configure **RSR**, **PNS**, or **STYLE** as the Production Start Method and use UI[9-16] bound to flags to start associated programs. Refer to FANUC manuals for specific bit patterns.

```csharp
using UnderAutomation.Fanuc;

public class RunProgramRemotelySnpx
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        robot.Connect("192.168.0.1");

        // Clear any existing alarms
        robot.Snpx.ClearAlarms();

        // Enable remote control (1 = KCL)
        robot.Snpx.IntegerSystemVariables.Write("$RMT_MASTER", 1);

        // Select the program to run
        string programName = "MY_PROGRAM";
        robot.Snpx.StringSystemVariables.Write("$SHELL_WRK.$CUST_NAME", programName);
        Console.WriteLine($"Selected program: {programName}");

        // Start the program (using system variable method)
        Console.WriteLine("Starting program...");
        robot.Snpx.IntegerSystemVariables.Write("$SHELL_WRK.$CUST_START", 1); // or you can set the flag for UOP cycle start if that's your configured method
    }
}
```

## Protocol comparison

| Feature | Telnet | CGTP | RMI | SNPX |
|---------|--------|------|-----|------|
| **Run program** | Yes | Yes (V9.30+) | Via motion commands | Indirect (variables) |
| **Pause** | Yes (Hold) | Yes | Yes | No |
| **Continue** | Yes | No | Yes | No |
| **Abort** | Yes | Yes | Yes | No |
| **Select/Deselect** | Yes | Yes | N/A | No |
| **Create/Delete** | No | Yes | No | No |
