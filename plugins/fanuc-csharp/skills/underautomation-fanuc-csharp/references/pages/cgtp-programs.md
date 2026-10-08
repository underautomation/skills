# Program management

Create, delete, rename, run, pause, abort programs and manage their attributes (comment, owner, subtype) via CGTP.

Web page: https://underautomation.com/fanuc/documentation/cgtp-programs

CGTP provides rich program management features: create, delete, rename, run, pause, configure program properties, list programs, and edit source code.

## List programs

Retrieve all TP or Karel programs on the controller, filtered by type and sub-type. You can also list all TP programs at once, regardless of their sub-type.

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Cgtp;

public class CgtpProgramsList
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        robot.Connect("192.168.0.1");

        // List all TP programs on the controller (all sub-types)
        string[] allTpPrograms = robot.Cgtp.ListTpPrograms();
        foreach (string prog in allTpPrograms)
        {
            Console.WriteLine(prog);
        }

        // List TP programs of a specific sub-type
        string[] jobs = robot.Cgtp.ListPrograms(CgtpProgramType.Tp, CgtpProgramSubType.Job);
        string[] macros = robot.Cgtp.ListPrograms(CgtpProgramType.Tp, CgtpProgramSubType.Macro);

        // List Karel programs
        string[] karelPrograms = robot.Cgtp.ListPrograms(CgtpProgramType.Karel, CgtpProgramSubType.None);
    }
}
```

## Source code editing

Insert, replace, or delete lines in a TP program directly on the controller. Requires firmware **V9.10+**.

```csharp
using UnderAutomation.Fanuc;

public class CgtpProgramsSourceEdit
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        robot.Connect("192.168.0.1");

        // Insert a new line before line 3 in program MY_PROGRAM
        robot.Cgtp.InsertSourceLine("MY_PROGRAM", "L P[5] 100mm/sec FINE", 3);

        // Replace the content of line 5
        robot.Cgtp.ReplaceSourceLine("MY_PROGRAM", "J P[1] 50% FINE", 5);

        // Delete 2 lines starting at line 4
        robot.Cgtp.DeleteSourceLines("MY_PROGRAM", 4, 2);

        // Delete a single line
        robot.Cgtp.DeleteSourceLines("MY_PROGRAM", 1);
    }
}
```

## Run a program

Run a specific program starting from a given line (default: line 1). Requires firmware **V9.30+**.

Prefer `RunProgram` to `robot.Cgtp.Kcl.Run`: it can start at a given line, and it throws a `CgtpException` when the controller refuses the command. `Kcl.Run` returns no result. See [KCL commands](cgtp-kcl.md).

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Cgtp;

public class CgtpProgramsRun
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        robot.Connect("192.168.0.1");

        // Run program from line 1
        robot.Cgtp.RunProgram("MY_PROGRAM");

        // Run from a specific line
        robot.Cgtp.RunProgram("MY_PROGRAM", lineNum: 10);

        // Select a program
        robot.Cgtp.SelectProgram("MY_PROGRAM");

        // Change the currently active program
        robot.Cgtp.ChangeActiveProgram("MY_PROGRAM");

        // Abort a specific task
        robot.Cgtp.AbortTask("MY_PROGRAM");

        // Pause all running programs
        robot.Cgtp.PauseAllPrograms();
    }
}
```


## Create a program

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Cgtp;

public class CgtpProgramsManage
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        robot.Connect("192.168.0.1");

        // Create a program
        robot.Cgtp.CreateProgram(
            progName: "NEW_PROG",
            owner: "UnderAutomation",
            comment: "Created via CGTP",
            defaultGroup: 1,
            subType: CgtpProgramSubType.Job);

        // Delete
        robot.Cgtp.DeleteProgram("OLD_PROG");

        // Rename
        robot.Cgtp.RenameProgram("OLD_NAME", "NEW_NAME");

        // Program properties
        string comment = robot.Cgtp.GetProgramComment("MY_PROGRAM");
        robot.Cgtp.SetProgramComment("MY_PROGRAM", "Updated comment");
        string owner = robot.Cgtp.GetProgramOwner("MY_PROGRAM");
        robot.Cgtp.SetProgramOwner("MY_PROGRAM", "Admin");
        int stack = robot.Cgtp.GetProgramStackSize("MY_PROGRAM");
        robot.Cgtp.SetProgramStackSize("MY_PROGRAM", 200);
        robot.Cgtp.SetProgramIgnorePause("MY_PROGRAM", true);
        robot.Cgtp.SetProgramWriteProtect("MY_PROGRAM", true);
        robot.Cgtp.SetProgramSubType("MY_PROGRAM", CgtpProgramSubType.Macro);
    }
}
```

Available sub-types: `None`, `Job`, `Process`, `Macro`, `Condition`.

## Pause, abort, resume, get and set attributes

CGTP allows you to completely manage programs on the robot, including creation, deletion, renaming, and execution control. Here's a complete example demonstrating these features:

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

## API reference

**CgtpProgramType** ([reference](../api/UnderAutomation.Fanuc.Cgtp.md#cgtpprogramtype))

- Karel: Karel program
- Tp: TP program
**CgtpProgramSubType** ([reference](../api/UnderAutomation.Fanuc.Cgtp.md#cgtpprogramsubtype))

- Condition: Condition handler program.
- Job: Job program.
- Macro: Macro program.
- None: No specific sub-type.
- Process: Process program.
