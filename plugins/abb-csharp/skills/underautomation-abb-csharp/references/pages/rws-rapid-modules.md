# RAPID modules & program files

Load, save and unload RAPID programs, read and edit module source text, manage breakpoints, read build errors and modify taught positions.

Web page: https://underautomation.com/abb/documentation/rws-rapid-modules

A RAPID program is a set of modules, and a module is a text file the controller keeps in memory. `robot.Rws.Rapid` loads and saves these files, reads and rewrites their source, and reports what the controller refused when it linked them.

Everything on this page that writes needs the `Rapid` [mastership](rws-mastership.md). Editing the source of a task that is running is possible, but the controller can refuse a change that would invalidate the program pointer.

## Program files

A program is a `.pgf` file naming the modules it holds. `GetProgram` returns the program of a task, `null` when the task holds none.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class RapidProgramFiles
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // The program the task holds, null when it holds none
        RapidProgramInfo program = robot.Rws.Rapid.GetProgram("T_ROB1");
        if (program != null)
            Console.WriteLine(program.Name + ", entry point " + program.EntryPoint);

        robot.Rws.Mastership.Request(MastershipDomain.Rapid);
        try
        {
            // The program file has to be on the controller already.
            // Upload it first with robot.Rws.File.
            robot.Rws.Rapid.LoadProgram("T_ROB1", "$HOME/myprogram.pgf", RapidProgramLoadMode.Replace);

            // Write every module of the task into a directory of the controller
            robot.Rws.Rapid.SaveProgram("T_ROB1", "$HOME/myprograms");

            robot.Rws.Rapid.SetProgramName("T_ROB1", "myprogram");
            robot.Rws.Rapid.SetEntryPoint("T_ROB1", "main");

            robot.Rws.Rapid.UnloadProgram("T_ROB1");
        }
        finally
        {
            robot.Rws.Mastership.Release(MastershipDomain.Rapid);
        }

        // Loading returns before the controller has finished, so read what it refused
        foreach (RapidBuildError error in robot.Rws.Rapid.GetBuildErrors("T_ROB1"))
            Console.WriteLine(error.ModuleName + " " + error.Row + "," + error.Column + ": " + error.Error);

        robot.Disconnect();
    }
}
```

| `RapidProgramLoadMode` | What happens to the modules already loaded           |
| ---------------------- | ---------------------------------------------------- |
| `Add`                  | They are kept, the modules of the program are added  |
| `Replace`              | Everything the task holds is replaced by the program |

Points to know:

- The file has to be on the file system of the controller already. Upload it first with the [file system service](rws-files.md).
- `LoadProgram` returns before the controller has finished loading. Read the task state and the build errors afterwards, do not assume the program is ready.
- `SaveProgram` writes the modules of the task into a directory of the controller, not on your PC. Download them afterwards.
- `SetEntryPoint` sets the routine `ResetProgramPointer` goes back to, usually `main`.
- Loading one module instead of a whole program is done with `LoadModule`, see [RAPID tasks & program execution](rws-rapid-tasks.md).

**Methods of RapidService** ([reference](../api/UnderAutomation.ABB.Rws.Services.md#rapidservice-robotrwsrapid))

- `void LoadProgram(string task, string programPath, RapidProgramLoadMode loadMode = RapidProgramLoadMode.Add)`: Loads a program into a task (synchronous)
  - async: `Task LoadProgramAsync(string task, string programPath, RapidProgramLoadMode loadMode = RapidProgramLoadMode.Add, CancellationToken cancellationToken = default)`
- `void SaveProgram(string task, string path)`: Saves the program of a task to the file system of the controller (synchronous)
  - async: `Task SaveProgramAsync(string task, string path, CancellationToken cancellationToken = default)`
- `void SetEntryPoint(string task, string routine)`: Sets the routine the program pointer moves to when it is reset (synchronous)
  - async: `Task SetEntryPointAsync(string task, string routine, CancellationToken cancellationToken = default)`
- `void SetProgramName(string task, string name)`: Renames the program of a task (synchronous)
  - async: `Task SetProgramNameAsync(string task, string name, CancellationToken cancellationToken = default)`
- `void UnloadProgram(string task)`: Unloads the program of a task (synchronous)
  - async: `Task UnloadProgramAsync(string task, CancellationToken cancellationToken = default)`

**RapidProgramInfo** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidprograminfo))

- `RapidProgramInfo()`: Initializes a new instance of the Data.RapidProgramInfo class
- `string EntryPoint { get; set; }`: Routine the program pointer moves to when it is reset, null when the controller did not report it
- `string Name { get; set; }`: Name of the program, null when the controller did not report it

**RapidProgramLoadMode** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidprogramloadmode))

- Add: Keep the modules already loaded and add the ones of the program
- Replace: Replace everything the task holds with the program

## Modules of a task

`GetModules` lists the modules a task holds. `GetModule` gives the file a module came from and the properties declared on it.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class RapidModuleList
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        foreach (RapidModuleItem module in robot.Rws.Rapid.GetModules("T_ROB1"))
        {
            Console.WriteLine(module.Name + " " + module.Type);   // ProgramModule or SystemModule

            // The file the module came from and the properties declared on it
            RapidModuleInfo info = robot.Rws.Rapid.GetModule("T_ROB1", module.Name);
            Console.WriteLine(info.FileName);

            foreach (RapidModuleAttribute attribute in info.Attributes)
                Console.WriteLine("   " + attribute);             // SystemModule, NoStepIn, ...

            // How big the source is, in lines and columns
            RapidModuleExtension size = robot.Rws.Rapid.GetModuleExtension("T_ROB1", module.Name);
            Console.WriteLine(size.LineCount + " lines, " + size.MaxColumnCount + " columns");

            // A counter that only moves when the module changes, cheaper than reading it again
            Console.WriteLine(robot.Rws.Rapid.GetModuleChangeCount("T_ROB1", module.Name));
        }

        // Which of these properties this module accepts
        RapidModuleAttribute[] possible = robot.Rws.Rapid.GetPossibleModuleAttributes(
            "T_ROB1", "MainModule", RapidModuleAttribute.NoStepIn, RapidModuleAttribute.ViewOnly);
        Console.WriteLine(possible.Length);

        // Write one module as a file of the controller, the extension is added by the controller
        robot.Rws.Rapid.SaveModule("T_ROB1", "MainModule", "MainModule", "$HOME");

        robot.Disconnect();
    }
}
```

| `RapidModuleAttribute` | What the module declares                                           |
| ---------------------- | ------------------------------------------------------------------ |
| `SystemModule`         | The module belongs to the system, it is not saved with the program |
| `ReadOnly`             | The source cannot be changed                                       |
| `ViewOnly`             | The source can be read but not changed                             |
| `NoView`               | The source cannot even be read                                     |
| `NoStepIn`             | Stepping does not enter the routines of the module                 |
| `Encoded`              | The source is stored encoded                                       |

`GetModuleChangeCount` returns a counter that only moves when the module changes. Comparing it with the previous reading is much cheaper than downloading the source again to find out that nothing moved. `GetModuleExtension` gives the number of lines and the longest line of the source.

### Read and edit the source

> **Available on** RWS 1.0 (IRC5) : yes | RWS 2.0 (OmniCore) : yes. On an IRC5 reading the whole source costs two requests and DeclaredLength stays empty.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class RapidModuleSource
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // The whole source of the module
        RapidModuleText source = robot.Rws.Rapid.GetModuleText("T_ROB1", "MainModule");
        Console.WriteLine(source.Text);
        Console.WriteLine(source.ChangeCount);

        // Only a few lines. Rows and columns are counted from 1, and the controller clamps
        // the end of the range to what the module really holds.
        Console.WriteLine(robot.Rws.Rapid.GetModuleTextRange("T_ROB1", "MainModule", 1, 1, 10, 1));

        // Where a piece of text sits, Found is false when it is nowhere
        RapidTextPosition found = robot.Rws.Rapid.SearchModuleText("T_ROB1", "MainModule", "MoveJ");
        Console.WriteLine(found.Found + " " + found.Row + "," + found.Column);

        robot.Rws.Mastership.Request(MastershipDomain.Rapid);
        try
        {
            // Insert one line after a range, leaving the rest of the module alone
            RapidSetTextRangeResult result = robot.Rws.Rapid.SetModuleTextRange(
                "T_ROB1", "MainModule",
                RapidTextReplaceMode.After, RapidTextQueryMode.Try,
                5, 1, 5, 1,
                "    reg1 := 0;\r\n");

            // Rewriting the line that declares the module renames it
            Console.WriteLine(result.ModuleRenamed + " " + result.NewModuleName);

            // Replace the whole source
            robot.Rws.Rapid.SetModuleText("T_ROB1", "MainModule",
                "MODULE MainModule\r\n  PROC main()\r\n  ENDPROC\r\nENDMODULE\r\n");
        }
        finally
        {
            robot.Rws.Mastership.Release(MastershipDomain.Rapid);
        }

        robot.Disconnect();
    }
}
```

Rows and columns are counted from 1, not from 0. The controller clamps the end of a range to what the module really holds, so a range running past the last line is not an error.

`SetModuleTextRange` writes into a range and returns what the controller did with the change.

| `RapidTextReplaceMode` | Where the new text goes                                |
| ---------------------- | ------------------------------------------------------ |
| `Replace`              | The range is replaced by the new text                  |
| `Before`               | The new text is inserted before the range, which stays |
| `After`                | The new text is inserted after the range, which stays  |

| `RapidTextQueryMode` | When the program pointer would become invalid                  |
| -------------------- | -------------------------------------------------------------- |
| `Try`                | The controller refuses the change                              |
| `Force`              | The controller applies it anyway and drops the program pointer |

Rewriting the line that declares the module renames it. This is why the result carries `ModuleRenamed` and `NewModuleName`. Use the new name in the calls that follow, the old one no longer exists.

`SearchModuleText` reports row and column 0 when it finds nothing, it does not fail. Test `Found` rather than the row.

`SaveModule` writes one module as a file of the controller. The controller adds the extension itself, so pass `MainModule` and not `MainModule.mod`.

**Methods of RapidService** ([reference](../api/UnderAutomation.ABB.Rws.Services.md#rapidservice-robotrwsrapid))

- `RapidModuleInfo GetModule(string task, string module)`: Gets the file a module came from and the properties declared on it (synchronous)
  - async: `Task<RapidModuleInfo> GetModuleAsync(string task, string module, CancellationToken cancellationToken = default)`
- `int GetModuleChangeCount(string task, string module)`: Gets the counter the controller increments whenever a module changes (synchronous) Comparing it with what a previous reading gave is cheaper than fetching the source again to find out that nothing changed.
  - async: `Task<int> GetModuleChangeCountAsync(string task, string module, CancellationToken cancellationToken = default)`
- `RapidModuleExtension GetModuleExtension(string task, string module)`: Gets how many lines and columns the source of a module holds (synchronous) This is what it takes to ask for the whole of it with Int32%2cSystem.Int32).
  - async: `Task<RapidModuleExtension> GetModuleExtensionAsync(string task, string module, CancellationToken cancellationToken = default)`
- `RapidModuleSymbol GetModuleSymbol(string task, string module, int row, int column)`: Gets the declaration the controller finds at a position of a module (synchronous)
  - async: `Task<RapidModuleSymbol> GetModuleSymbolAsync(string task, string module, int row, int column, CancellationToken cancellationToken = default)`
- `RapidModuleText GetModuleText(string task, string module)`: Gets the source of a module (synchronous)
  - async: `Task<RapidModuleText> GetModuleTextAsync(string task, string module, CancellationToken cancellationToken = default)`
- `string GetModuleTextRange(string task, string module, int startRow, int startColumn, int endRow, int endColumn)`: Gets a range of the source of a module (synchronous)
  - async: `Task<string> GetModuleTextRangeAsync(string task, string module, int startRow, int startColumn, int endRow, int endColumn, CancellationToken cancellationToken = default)`
- `RapidModuleItem[] GetModules(string task)`: Gets the modules loaded into a task (synchronous)
  - async: `Task<RapidModuleItem[]> GetModulesAsync(string task, CancellationToken cancellationToken = default)`
- `RapidModuleAttribute[] GetPossibleModuleAttributes(string task, string module, params RapidModuleAttribute[] attributes)`: Gets which of the requested properties may be declared on a module (synchronous)
  - async: `Task<RapidModuleAttribute[]> GetPossibleModuleAttributesAsync(string task, string module, RapidModuleAttribute[] attributes, CancellationToken cancellationToken = default)`
- `void SaveModule(string task, string module, string name, string path)`: Saves a module to the file system of the controller (synchronous)
  - async: `Task SaveModuleAsync(string task, string module, string name, string path, CancellationToken cancellationToken = default)`
- `RapidTextPosition SearchModuleText(string task, string module, string text, int startRow = 1, int startColumn = 1)`: Finds where a piece of text sits in the source of a module (synchronous)
  - async: `Task<RapidTextPosition> SearchModuleTextAsync(string task, string module, string text, int startRow = 1, int startColumn = 1, CancellationToken cancellationToken = default)`
- `void SetModuleText(string task, string module, string text)`: Replaces the whole source of a module (synchronous)
  - async: `Task SetModuleTextAsync(string task, string module, string text, CancellationToken cancellationToken = default)`
- `RapidSetTextRangeResult SetModuleTextRange(string task, string module, RapidTextReplaceMode replaceMode, RapidTextQueryMode queryMode, int startRow, int startColumn, int endRow, int endColumn, string text)`: Writes text into a range of the source of a module (synchronous)
  - async: `Task<RapidSetTextRangeResult> SetModuleTextRangeAsync(string task, string module, RapidTextReplaceMode replaceMode, RapidTextQueryMode queryMode, int startRow, int startColumn, int endRow, int endColumn, string text, CancellationToken cancellationToken = default)`

**RapidModuleItem** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidmoduleitem))

- `RapidModuleItem()`: Initializes a new instance of the Data.RapidModuleItem class
- `string Name { get; set; }`: Name of the module, for example "MainModule"
- `RapidModuleType Type { get; set; }`: Whether the module belongs to the program or to the system

**RapidModuleInfo** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidmoduleinfo))

- `RapidModuleInfo()`: Initializes a new instance of the Data.RapidModuleInfo class
- `int AttributeCount { get; }`: Number of properties declared on the module
- `RapidModuleAttribute[] Attributes { get; set; }`: Properties declared on the module, empty when it declares none
- `string FileName { get; set; }`: Name of the file the module was loaded from, for example "MainModule.mod"
- Inherited from [RapidModuleItem](../api/UnderAutomation.ABB.Rws.Data.md#rapidmoduleitem): `Name`, `Type`

**RapidModuleText** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidmoduletext))

- `RapidModuleText()`: Initializes a new instance of the Data.RapidModuleText class
- `int? ChangeCount { get; set; }`: Counter the controller increments whenever the module changes, null when it did not report it
- `int? DeclaredLength { get; set; }`: Length the controller declares for the module, null when it did not report it. This is the size the controller reserves for the module and not the length of RapidModuleText.Text, so the two normally differ.
- `string Text { get; set; }`: Source of the module

**RapidModuleExtension** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidmoduleextension))

- `RapidModuleExtension()`: Initializes a new instance of the Data.RapidModuleExtension class
- `int? ChangeCount { get; set; }`: Counter the controller increments whenever the module changes, null when it did not report it
- `int? LineCount { get; set; }`: Number of lines the module holds, null when the controller did not report it
- `int? MaxColumnCount { get; set; }`: Length of the longest line of the module, null when the controller did not report it

**RapidSetTextRangeResult** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidsettextrangeresult))

- `RapidSetTextRangeResult()`: Initializes a new instance of the Data.RapidSetTextRangeResult class
- `int? ChangeCount { get; set; }`: Counter the controller incremented for the change, null when it did not report it
- `bool ModuleRenamed { get; set; }`: Whether the change renamed the module
- `string NewModuleName { get; set; }`: Name the module now has, empty when the change did not rename it

**RapidTextPosition** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidtextposition))

- `RapidTextPosition()`: Initializes a new instance of the Data.RapidTextPosition class
- `int Column { get; set; }`: Column of the position, 0 when the search found nothing
- `bool Found { get; }`: Whether the position points at something, which it does not when a search found nothing
- `int Row { get; set; }`: Line of the position, 0 when the search found nothing

**RapidModuleType** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidmoduletype))

- ProgramModule: A module of the program, saved and loaded with it
- SystemModule: A module of the system, which survives loading another program
- Unknown: The controller reported a type this library does not know

**RapidModuleAttribute** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidmoduleattribute))

- Encoded: The source of the module is encoded and cannot be read back
- NoStepIn: Execution may not step into the routines of the module
- NoView: The source of the module may not be displayed
- ReadOnly: The module may not be changed
- SystemModule: The module belongs to the system rather than to the program
- Unknown: The controller reported an attribute this library does not know
- ViewOnly: The source may be displayed but not changed

**RapidTextReplaceMode** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidtextreplacemode))

- After: Insert the new text after the range, leaving it in place
- Before: Insert the new text before the range, leaving it in place
- Replace: Replace the range with the new text

**RapidTextQueryMode** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidtextquerymode))

- Force: Apply the change even when it invalidates the program pointer
- Try: Apply the change only when the program pointer survives it

## Build errors

Linking a program never fails the request itself. The controller accepts it, then reports what it refused. `GetBuildErrors` returns one entry per error, with the module, the position and the message.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class RapidBuildErrors
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // The controller answers at most thirty errors at a time, read the next ones by paging
        int start = 0;
        RapidBuildError[] errors = robot.Rws.Rapid.GetBuildErrors("T_ROB1", start, 30);

        while (errors.Length > 0)
        {
            foreach (RapidBuildError error in errors)
            {
                Console.WriteLine(error.ModuleName + " " + error.Row + "," + error.Column);
                Console.WriteLine("   " + error.Error);
            }

            start += errors.Length;
            errors = robot.Rws.Rapid.GetBuildErrors("T_ROB1", start, 30);
        }

        // An empty answer and a task state of Linked mean the program is runnable
        Console.WriteLine(robot.Rws.Rapid.GetTask("T_ROB1").TaskState);

        robot.Disconnect();
    }
}
```

The controller returns at most thirty errors at a time, whatever larger limit is asked for. Use `start` and `limit` to read the rest. An empty array means the program linked cleanly, and the task state then becomes `Linked`.

`BuildTask` itself is described in [RAPID tasks & program execution](rws-rapid-tasks.md).

**Methods of RapidService** ([reference](../api/UnderAutomation.ABB.Rws.Services.md#rapidservice-robotrwsrapid))

- `RapidBuildError[] GetBuildErrors(string task, int? start = null, int? limit = null)`: Gets the errors the controller found while linking the program of a task (synchronous)
  - async: `Task<RapidBuildError[]> GetBuildErrorsAsync(string task, int? start = null, int? limit = null, CancellationToken cancellationToken = default)`

**RapidBuildError** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidbuilderror))

- `RapidBuildError()`: Initializes a new instance of the Data.RapidBuildError class
- `int? Column { get; set; }`: Column the error was found at, null when the controller did not report it
- `string Error { get; set; }`: Description of the error as the controller worded it
- `int? ErrorNumber { get; set; }`: Numeric identifier of the error, null when the controller did not report it
- `string ModuleName { get; set; }`: Name of the module the error was found in
- `int? Row { get; set; }`: Line the error was found at, null when the controller did not report it

## Breakpoints

`SetBreakpoint` places a breakpoint at a position of a module. The controller snaps it to the whole instruction holding that position, so the range it answers is normally wider than what was asked for.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class RapidBreakpoints
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        robot.Rws.Mastership.Request(MastershipDomain.Rapid);
        try
        {
            // The controller snaps the breakpoint to the whole instruction holding the
            // position, so the range it answers is normally wider than what was asked for
            RapidBreakpoint placed = robot.Rws.Rapid.SetBreakpoint("T_ROB1", "MainModule", 12, 1);
            Console.WriteLine(placed.StartRow + "," + placed.StartColumn + " -> " +
                              placed.EndRow + "," + placed.EndColumn);
        }
        finally
        {
            robot.Rws.Mastership.Release(MastershipDomain.Rapid);
        }

        foreach (RapidBreakpoint breakpoint in robot.Rws.Rapid.GetBreakpoints("T_ROB1"))
            Console.WriteLine(breakpoint.ModuleName + " " + breakpoint.StartRow);

        // A breakpoint only stops the program when execution was started with stopAtBreakpoint
        robot.Rws.Rapid.Start(RapidRegainMode.Continue, RapidExecutionMode.Continue,
                              RapidExecutionCycle.Forever, RapidStartCondition.None, true, false);

        robot.Disconnect();
    }
}
```

A breakpoint only stops the program when execution was started with `stopAtBreakpoint` set to `true`, see [RAPID tasks & program execution](rws-rapid-tasks.md). Editing the source moves the positions, so read the breakpoints again after a change.

**Methods of RapidService** ([reference](../api/UnderAutomation.ABB.Rws.Services.md#rapidservice-robotrwsrapid))

- `RapidBreakpoint[] GetBreakpoints(string task, int? start = null, int? limit = null)`: Gets the breakpoints set in the program of a task (synchronous)
  - async: `Task<RapidBreakpoint[]> GetBreakpointsAsync(string task, int? start = null, int? limit = null, CancellationToken cancellationToken = default)`
- `RapidBreakpoint SetBreakpoint(string task, string module, int row, int column)`: Sets a breakpoint at a position of a module (synchronous)
  - async: `Task<RapidBreakpoint> SetBreakpointAsync(string task, string module, int row, int column, CancellationToken cancellationToken = default)`

**RapidBreakpoint** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidbreakpoint))

- `RapidBreakpoint()`: Initializes a new instance of the Data.RapidBreakpoint class
- `int? EndColumn { get; set; }`: Column the breakpoint ends at, null when the controller did not report it
- `int? EndRow { get; set; }`: Line the breakpoint ends at, null when the controller did not report it
- `string ModuleName { get; set; }`: Name of the module the breakpoint sits in, null when the controller did not report it
- `int? StartColumn { get; set; }`: Column the breakpoint starts at, null when the controller did not report it
- `int? StartRow { get; set; }`: Line the breakpoint starts at, null when the controller did not report it

## Modify a taught position

This is the teaching gesture of the FlexPendant: jog the robot where it should go, then write that position back into the motion instruction of the program.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class RapidModifyPosition
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // How many motion instructions of this range can be rewritten
        RapidModifiablePositions modifiable =
            robot.Rws.Rapid.GetModifiablePositions("T_ROB1", "MainModule", 1, 1, 40, 1);
        Console.WriteLine(modifiable.ModifiableLineCount);

        // Every one of them, in every task of the system
        foreach (RapidModifiablePositionItem item in robot.Rws.Rapid.GetAllModifiablePositions())
            Console.WriteLine(item.TaskName + "/" + item.ModuleName + " line " + item.StartRow);

        // Jog the robot where it should go, then write that position into the program
        robot.Rws.Mastership.Request(MastershipDomain.Rapid);
        try
        {
            robot.Rws.Rapid.ModifyPosition("T_ROB1", "MainModule", 12, 1, 12, 1, true, true, false);
        }
        finally
        {
            robot.Rws.Mastership.Release(MastershipDomain.Rapid);
        }

        robot.Disconnect();
    }
}
```

`GetModifiablePositions` says how many motion instructions of a range can be rewritten, `GetAllModifiablePositions` lists every one of them in every task of the system. Read one of the two before writing, so you know what is about to change.

- `checkLimits` makes the controller refuse a position outside the working range.
- `checkDeactivatedAxes` makes it refuse to rewrite an axis that is deactivated, and `allowDeactivated` rewrites it anyway.
- `ModifyAllPositions` rewrites everything at once. The controller only accepts it from a client it considers local.

Jogging the robot to the position is done with the [motion system service](rws-motion.md), and it needs the `Motion` [mastership](rws-mastership.md), which is a different domain from `Rapid`.

**Methods of RapidService** ([reference](../api/UnderAutomation.ABB.Rws.Services.md#rapidservice-robotrwsrapid))

- `RapidModifiablePositionItem[] GetAllModifiablePositions()`: Gets every motion instruction of the system whose position can be rewritten to where the robot currently stands, wherever in whichever task it sits (synchronous)
  - async: `Task<RapidModifiablePositionItem[]> GetAllModifiablePositionsAsync(CancellationToken cancellationToken = default)`
- `RapidModifiablePositions GetModifiablePositions(string task, string module, int startRow, int startColumn, int endRow, int endColumn)`: Gets how many motion instructions of a range can have their position rewritten to where the robot currently stands (synchronous)
  - async: `Task<RapidModifiablePositions> GetModifiablePositionsAsync(string task, string module, int startRow, int startColumn, int endRow, int endColumn, CancellationToken cancellationToken = default)`
- `void ModifyAllPositions(bool checkLimits = true, bool checkDeactivatedAxes = true)`: Rewrites the positions of every motion instruction of the system that can be rewritten, to where the robot currently stands (synchronous)
  - async: `Task ModifyAllPositionsAsync(bool checkLimits = true, bool checkDeactivatedAxes = true, CancellationToken cancellationToken = default)`
- `void ModifyPosition(string task, string module, int startRow, int startColumn, int endRow, int endColumn, bool checkLimits = true, bool checkDeactivatedAxes = true, bool allowDeactivated = false)`: Rewrites the positions of the motion instructions of a range to where the robot currently stands (synchronous) This is the teaching gesture: jog the robot where it should go, then write that position back into the program.
  - async: `Task ModifyPositionAsync(string task, string module, int startRow, int startColumn, int endRow, int endColumn, bool checkLimits = true, bool checkDeactivatedAxes = true, bool allowDeactivated = false, CancellationToken cancellationToken = default)`

**RapidModifiablePositions** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidmodifiablepositions))

- `RapidModifiablePositions()`: Initializes a new instance of the Data.RapidModifiablePositions class
- `int? EndColumn { get; set; }`: Column the modifiable range ends at, null when the controller did not report it
- `int? EndRow { get; set; }`: Line the modifiable range ends at, null when the controller did not report it
- `int ModifiableLineCount { get; set; }`: Number of motion instructions of the range whose position can be rewritten
- `int? StartColumn { get; set; }`: Column the modifiable range starts at, null when the controller did not report it
- `int? StartRow { get; set; }`: Line the modifiable range starts at, null when the controller did not report it

**RapidModifiablePositionItem** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidmodifiablepositionitem))

- `RapidModifiablePositionItem()`: Initializes a new instance of the Data.RapidModifiablePositionItem class
- `int? EndColumn { get; set; }`: Column the instruction ends at, null when the controller did not report it
- `int? EndRow { get; set; }`: Line the instruction ends at, null when the controller did not report it
- `string ModuleName { get; set; }`: Name of the module holding the instruction
- `int? StartColumn { get; set; }`: Column the instruction starts at, null when the controller did not report it
- `int? StartRow { get; set; }`: Line the instruction starts at, null when the controller did not report it
- `string TaskName { get; set; }`: Name of the task holding the module

## Write an editor

The last group of methods exists for the applications that edit RAPID, not for the ones that drive a robot. They give what an editor needs: what is declared at a position, the arguments of a call, a complete instruction ready to be written, and the palette an operator picks an instruction from.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class RapidSourceNavigation
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // What is declared at this position of the source, null when nothing is
        RapidModuleSymbol symbol = robot.Rws.Rapid.GetModuleSymbol("T_ROB1", "MainModule", 12, 5);
        if (symbol != null)
            Console.WriteLine(symbol.Name + " " + symbol.SymbolType + " " + symbol.DataType);

        // The routine called at this position, and the arguments of that call
        RapidRoutineInfo routine = robot.Rws.Rapid.GetRoutine("T_ROB1", "MainModule", 12, 5);
        Console.WriteLine(routine.Name + " " + routine.ParameterCount);

        foreach (RapidRoutineArgument argument in
                 robot.Rws.Rapid.GetRoutineArguments("T_ROB1", "MainModule", 12, 5))
        {
            Console.WriteLine(argument.DataType + " at " + argument.StartRow + "," + argument.StartColumn);
        }

        // A complete instruction ready to be written, instead of a bare keyword
        RapidInstructionTemplate template = robot.Rws.Rapid.GetInstructionTemplate("T_ROB1", "MainModule", "MoveJ");
        foreach (RapidInstructionTemplateArgument argument in template.Arguments)
            Console.WriteLine(argument.Name + " = " + argument.Value + " (" + argument.DataType + ")");

        // Where the parts of an object begin and end, given the whole span of that object
        RapidObjectChild children = robot.Rws.Rapid.GetObjectChildren("T_ROB1", "MainModule", 1, 1, 40, 1);
        foreach (RapidObjectChildRange range in children.Ranges)
            Console.WriteLine(range.Name + ": " + range.Range);

        // Where one of the lists an object holds sits, without reading the module
        RapidObjectListExtension list = robot.Rws.Rapid.GetObjectListExtension(
            "RAPID/T_ROB1/MainModule", RapidObjectListType.RoutineDeclarations);
        Console.WriteLine(list.List + " first " + list.First + " last " + list.Last);

        robot.Disconnect();
    }
}
```

`GetModuleSymbol` returns the declaration found at a position, `null` when there is none. `GetRoutine` and `GetRoutineArguments` work on a position sitting on a routine call, and the controller refuses the request when it does not.

`GetInstructionTemplate` returns a complete instruction with the arguments the controller suggests, instead of a bare keyword. `GetObjectChildren` and `GetObjectListExtension` give where the parts of an object begin and end, which is how an editor jumps to the declarations of a module without reading the whole source.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class RapidEditorPalette
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // Categories of the instruction palette, the same ones an editor shows
        foreach (RapidPalletHeadItem head in robot.Rws.Rapid.GetPalletHeads("T_ROB1"))
        {
            Console.WriteLine(head.Number + ": " + head.Name);

            // Instructions of that category
            foreach (RapidPalletItem item in robot.Rws.Rapid.GetPallet("T_ROB1", head.Number.Value))
                Console.WriteLine("   " + item.Name + " " + item.Instruction);
        }

        // Types the controller suggests for one argument of an instruction
        foreach (RapidPreferredDataTypeItem type in
                 robot.Rws.Rapid.GetPreferredDataTypes("T_ROB1", "AliasIO", "FromSignal"))
        {
            Console.WriteLine(type.Name + " (" + type.DataType + ")");
        }

        robot.Disconnect();
    }
}
```

`GetPalletHeads` returns the categories of the instruction palette, `GetPallet` the instructions of one category, and `GetPreferredDataTypes` the types that fit one argument of an instruction.

**Methods of RapidService** ([reference](../api/UnderAutomation.ABB.Rws.Services.md#rapidservice-robotrwsrapid))

- `RapidInstructionTemplate GetInstructionTemplate(string task, string module, string name, bool isDataType = false, int? row = null, int? column = null, int? parameterNumber = null, int? alternativeNumber = null)`: Gets the template the controller suggests for an instruction or a data type: the arguments to write and the values to write them with (synchronous) This is what an editor uses to insert a complete, valid instruction rather than a bare keyword.
  - async: `Task<RapidInstructionTemplate> GetInstructionTemplateAsync(string task, string module, string name, bool isDataType = false, int? row = null, int? column = null, int? parameterNumber = null, int? alternativeNumber = null, CancellationToken cancellationToken = default)`
- `RapidObjectChild GetObjectChildren(string task, string module, int startLine, int startColumn, int endLine, int endColumn)`: Gets the parts a RAPID object is made of and where each of them sits in the source (synchronous) Pass the whole span of the object to get its parts; an editor uses this to know where the name, the attributes and the declaration lists of a module begin and end.
  - async: `Task<RapidObjectChild> GetObjectChildrenAsync(string task, string module, int startLine, int startColumn, int endLine, int endColumn, CancellationToken cancellationToken = default)`
- `RapidObjectListExtension GetObjectListExtension(string symbolUrl, RapidObjectListType type = RapidObjectListType.Statements)`: Gets where one of the lists a RAPID object holds sits in the source: the span of the whole list, and the spans of its first and last elements (synchronous) An editor uses this to jump to the beginning or the end of a list without reading the whole module.
  - async: `Task<RapidObjectListExtension> GetObjectListExtensionAsync(string symbolUrl, RapidObjectListType type = RapidObjectListType.Statements, CancellationToken cancellationToken = default)`
- `RapidPalletItem[] GetPallet(string task, int palletNumber, int? start = null, int? limit = null)`: Gets the entries of one category of the instruction palette (synchronous)
  - async: `Task<RapidPalletItem[]> GetPalletAsync(string task, int palletNumber, int? start = null, int? limit = null, CancellationToken cancellationToken = default)`
- `RapidPalletHeadItem[] GetPalletHeads(string task, int? start = null, int? limit = null)`: Gets the categories of the instruction palette an editor offers (synchronous)
  - async: `Task<RapidPalletHeadItem[]> GetPalletHeadsAsync(string task, int? start = null, int? limit = null, CancellationToken cancellationToken = default)`
- `RapidPreferredDataTypeItem[] GetPreferredDataTypes(string task, string instruction, string parameter)`: Gets the data types the controller suggests for one argument of an instruction (synchronous) An editor uses this to offer only the types that fit where the operator is typing.
  - async: `Task<RapidPreferredDataTypeItem[]> GetPreferredDataTypesAsync(string task, string instruction, string parameter, CancellationToken cancellationToken = default)`
- `RapidRoutineInfo GetRoutine(string task, string module, int row, int column)`: Gets the routine the controller finds called at a position of a module (synchronous)
  - async: `Task<RapidRoutineInfo> GetRoutineAsync(string task, string module, int row, int column, CancellationToken cancellationToken = default)`
- `RapidRoutineArgument[] GetRoutineArguments(string task, string module, int row, int column, int? mark = null, int? limit = null)`: Gets the arguments of the routine call found at a position of a module (synchronous)
  - async: `Task<RapidRoutineArgument[]> GetRoutineArgumentsAsync(string task, string module, int row, int column, int? mark = null, int? limit = null, CancellationToken cancellationToken = default)`

**RapidModuleSymbol** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidmodulesymbol))

- `RapidModuleSymbol()`: Initializes a new instance of the Data.RapidModuleSymbol class
- `string DataType { get; set; }`: Name of the type of the symbol, for example "robtarget"
- `int? Dimensions { get; set; }`: Number of array dimensions of the symbol, null when the controller did not report it
- `bool? Heap { get; set; }`: Whether the symbol is allocated on the heap, null when the controller did not report it
- `bool? Linked { get; set; }`: Whether the declaration is complete, null when the controller did not report it
- `bool? Local { get; set; }`: Whether the symbol is local to its module, null when the controller did not report it
- `string Name { get; set; }`: Name of the declared symbol
- `int? ReferenceCount { get; set; }`: How many times the symbol is referred to, null when the controller did not report it
- `int? Storage { get; set; }`: How the controller stores the symbol, null when it did not report it
- `RapidSymbolType SymbolType { get; set; }`: What kind of symbol was declared
- `string SymbolUrl { get; set; }`: Path of the symbol, which the symbol resources take
- `string TypeUrl { get; set; }`: Path of the type of the symbol
- `string Version { get; set; }`: Version the controller stamps on the declaration

**RapidRoutineInfo** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidroutineinfo))

- `RapidRoutineInfo()`: Initializes a new instance of the Data.RapidRoutineInfo class
- `bool? Local { get; set; }`: Whether the routine is local to its module, null when the controller did not report it
- `string Name { get; set; }`: Name of the routine
- `bool? Named { get; set; }`: Whether the routine is named, null when the controller did not report it
- `int? ParameterCount { get; set; }`: Number of parameters the routine takes, null when the controller did not report it. The controller reports -1 when the parameter list is not linked yet.
- `RapidSymbolType SymbolType { get; set; }`: Whether the routine is a procedure, a function or a trap
- `string SymbolUrl { get; set; }`: Path of the routine, which the program pointer resources take

**RapidRoutineArgument** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidroutineargument))

- `RapidRoutineArgument()`: Initializes a new instance of the Data.RapidRoutineArgument class
- `int? AlternateArgument { get; set; }`: Which alternative of the parameter this argument fills, null when the controller did not report it
- `string DataType { get; set; }`: Type of the argument, for example "num"
- `int? EndColumn { get; set; }`: Column the argument ends at, null when the controller did not report it
- `int? EndRow { get; set; }`: Line the argument ends at, null when the controller did not report it
- `int? ListLength { get; set; }`: Length of the argument list, null when the controller did not report it
- `int? ListNumber { get; set; }`: Position of the argument in the argument list, null when the controller did not report it
- `string ObjectType { get; set; }`: What the argument is, for example a required argument or a name reference
- `int? ParameterNumber { get; set; }`: Position of the argument in the call, counted from 0
- `int? StartColumn { get; set; }`: Column the argument starts at, null when the controller did not report it
- `int? StartRow { get; set; }`: Line the argument starts at, null when the controller did not report it

**RapidInstructionTemplate** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidinstructiontemplate))

- `RapidInstructionTemplate()`: Initializes a new instance of the Data.RapidInstructionTemplate class
- `int? ArgumentCount { get; set; }`: Number of arguments the controller reported, null when it did not report it
- `RapidInstructionTemplateArgument[] Arguments { get; set; }`: The suggested arguments
- `bool? Complete { get; set; }`: Whether every argument has been reported, null when the controller did not report it
- `int? Mark { get; set; }`: Index the controller started reporting from, null when it did not report it
- `int? SelectedParameter { get; set; }`: Argument the controller suggests selecting first, null when it did not report it
- `string Version { get; set; }`: Version the controller stamps on the template

**RapidInstructionTemplateArgument** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidinstructiontemplateargument))

- `RapidInstructionTemplateArgument()`: Initializes a new instance of the Data.RapidInstructionTemplateArgument class
- `int? ArgumentNumber { get; set; }`: Position of the argument, null when the controller did not report it
- `string DataType { get; set; }`: Type of the argument, for example "robtarget"
- `bool? DeclarationNeeded { get; set; }`: Whether inserting the instruction also needs a declaration to be created for this argument, null when the controller did not report it
- `int? Dimensions { get; set; }`: Number of array dimensions of the argument, null when the controller did not report it
- `bool? Local { get; set; }`: Whether the suggested symbol is local to its module, null when the controller did not report it
- `string Name { get; set; }`: Name of the argument, for example "ToPoint"
- `string ObjectType { get; set; }`: How the suggested symbol is declared, for example "CONST" or "TASK PERS"
- `bool? Required { get; set; }`: Whether the argument has to be given, null when the controller did not report it
- `string Symbol { get; set; }`: Name of the symbol the argument refers to, empty when the argument is written as a literal
- `string Value { get; set; }`: Value the argument is suggested with, written the way RAPID writes it

**RapidObjectChild** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidobjectchild))

- `RapidObjectChild()`: Initializes a new instance of the Data.RapidObjectChild class
- `RapidTextRange GetRange(string name)`: Returns the span of one part by its name, null when the controller did not report it
- `string ObjectType { get; set; }`: What the object is, for example "module"
- `int RangeCount { get; }`: Number of parts the controller reported
- `RapidObjectChildRange[] Ranges { get; set; }`: The parts of the object, including the ones it does not hold, whose span is then empty

**RapidObjectChildRange** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidobjectchildrange))

- `RapidObjectChildRange()`: Initializes a new instance of the Data.RapidObjectChildRange class
- `bool IsPresent { get; }`: Whether the controller reported a real span for the part, which it does not when the object does not hold it
- `string Name { get; set; }`: Name of the part as the controller worded it, for example "data-decl" or "endmod"
- `RapidTextRange Range { get; set; }`: Where the part sits in the source

**RapidObjectListExtension** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidobjectlistextension))

- `RapidObjectListExtension()`: Initializes a new instance of the Data.RapidObjectListExtension class
- `RapidTextRange First { get; set; }`: Span of the first element of the list
- `RapidTextRange Last { get; set; }`: Span of the last element of the list
- `RapidTextRange List { get; set; }`: Span of the whole list

**RapidObjectListType** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidobjectlisttype))

- Attributes: The attributes it declares
- BackwardStatements: The statements of its BACKWARD handler
- DataDeclarations: The data declarations it holds
- ErrorStatements: The statements of its ERROR handler
- ParameterDeclarations: The parameter declarations it holds
- RoutineDeclarations: The routine declarations it holds
- Statements: The statements of the object
- TypeDeclarations: The type declarations it holds
- UndoStatements: The statements of its UNDO handler

**RapidPalletHeadItem** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidpalletheaditem))

- `RapidPalletHeadItem()`: Initializes a new instance of the Data.RapidPalletHeadItem class
- `string Name { get; set; }`: Name of the category, for example "Motion&amp;Proc."
- `int? Number { get; set; }`: Number identifying the category, null when the controller did not report it

**RapidPalletItem** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidpalletitem))

- `RapidPalletItem()`: Initializes a new instance of the Data.RapidPalletItem class
- `int? Alternative { get; set; }`: Alternative of the parameter the entry preselects, null when the controller did not report it
- `string Instruction { get; set; }`: Instruction the entry inserts
- `int? Keyword { get; set; }`: Whether the entry is a language keyword rather than an instruction, null when the controller did not report it
- `string Name { get; set; }`: Name shown for the entry, for example "MoveJ"
- `int? Parameter { get; set; }`: Parameter the entry preselects, null when the controller did not report it

**RapidPreferredDataTypeItem** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidpreferreddatatypeitem))

- `RapidPreferredDataTypeItem()`: Initializes a new instance of the Data.RapidPreferredDataTypeItem class
- `string DataType { get; set; }`: Data type of the suggestion
- `string Name { get; set; }`: Name of the suggestion, for example "signaldi"

## What is not on this page

The values the modules declare are read and written from [RAPID variables & symbols](rws-rapid-symbols.md). Starting the program, moving the program pointer and loading one module are on [RAPID tasks & program execution](rws-rapid-tasks.md). Uploading a module file to the controller, and downloading a saved one, are on [File system](rws-files.md).

## Try it in the demo application

The **RAPID (RWS)** page of the [demo application](demo-app.md) exercises these calls against a live controller, without writing any code. It is shown in [RAPID tasks & program execution](rws-rapid-tasks.md).
