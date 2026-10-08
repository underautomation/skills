# RAPID modules & program files

Load, save and unload RAPID programs, read and edit module source text, manage breakpoints, read build errors and modify taught positions.

Web page: https://underautomation.com/abb/documentation/rws-rapid-modules

A RAPID program is a set of modules, and a module is a text file the controller keeps in memory. `robot.Rws.Rapid` loads and saves these files, reads and rewrites their source, and reports what the controller refused when it linked them.

Everything on this page that writes needs the `Rapid` [mastership](rws-mastership.md). Editing the source of a task that is running is possible, but the controller can refuse a change that would invalidate the program pointer.

## Program files

A program is a `.pgf` file naming the modules it holds. `GetProgram` returns the program of a task, `null` when the task holds none.

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.mastership_domain import MastershipDomain
from underautomation.abb.rws.data.rapid_program_load_mode import RapidProgramLoadMode

robot = AbbController()
robot.connect("192.168.0.1")

# The program the task holds, None when it holds none
program = robot.rws.rapid.get_program("T_ROB1")
if program is not None:
    print(f"{program.name}, entry point {program.entry_point}")

robot.rws.mastership.request(MastershipDomain.Rapid)
try:
    # The program file has to be on the controller already.
    # Upload it first with robot.rws.file.
    robot.rws.rapid.load_program("T_ROB1", "$HOME/myprogram.pgf", RapidProgramLoadMode.Replace)

    # Write every module of the task into a directory of the controller
    robot.rws.rapid.save_program("T_ROB1", "$HOME/myprograms")

    robot.rws.rapid.set_program_name("T_ROB1", "myprogram")
    robot.rws.rapid.set_entry_point("T_ROB1", "main")

    robot.rws.rapid.unload_program("T_ROB1")
finally:
    robot.rws.mastership.release(MastershipDomain.Rapid)

# Loading returns before the controller has finished, so read what it refused
for error in robot.rws.rapid.get_build_errors("T_ROB1"):
    print(f"{error.module_name} {error.row},{error.column}: {error.error}")

robot.disconnect()
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



**RapidProgramInfo** ([reference](../api/underautomation.abb.rws.data.md#rapidprograminfo))

- `RapidProgramInfo()`: Initializes a new instance of the RapidProgramInfo class
- `name: str`: Name of the program, null when the controller did not report it
- `entry_point: str`: Routine the program pointer moves to when it is reset, null when the controller did not report it

**RapidProgramLoadMode** ([reference](../api/underautomation.abb.rws.data.md#rapidprogramloadmode))

- Add: Keep the modules already loaded and add the ones of the program
- Replace: Replace everything the task holds with the program

## Modules of a task

`GetModules` lists the modules a task holds. `GetModule` gives the file a module came from and the properties declared on it.

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.rapid_module_attribute import RapidModuleAttribute

robot = AbbController()
robot.connect("192.168.0.1")

for module in robot.rws.rapid.get_modules("T_ROB1"):
    print(f"{module.name} {module.type}")  # ProgramModule or SystemModule

    # The file the module came from and the properties declared on it
    info = robot.rws.rapid.get_module("T_ROB1", module.name)
    print(info.file_name)

    for attribute in info.attributes:
        print("   " + str(attribute))      # SystemModule, NoStepIn, ...

    # How big the source is, in lines and columns
    size = robot.rws.rapid.get_module_extension("T_ROB1", module.name)
    print(f"{size.line_count} lines, {size.max_column_count} columns")

    # A counter that only moves when the module changes, cheaper than reading it again
    print(robot.rws.rapid.get_module_change_count("T_ROB1", module.name))

# Which of these properties this module accepts
possible = robot.rws.rapid.get_possible_module_attributes(
    "T_ROB1", "MainModule", [RapidModuleAttribute.NoStepIn, RapidModuleAttribute.ViewOnly])
print(len(possible))

# Write one module as a file of the controller, the extension is added by the controller
robot.rws.rapid.save_module("T_ROB1", "MainModule", "MainModule", "$HOME")

robot.disconnect()
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

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.mastership_domain import MastershipDomain
from underautomation.abb.rws.data.rapid_text_query_mode import RapidTextQueryMode
from underautomation.abb.rws.data.rapid_text_replace_mode import RapidTextReplaceMode

robot = AbbController()
robot.connect("192.168.0.1")

# The whole source of the module
source = robot.rws.rapid.get_module_text("T_ROB1", "MainModule")
print(source.text)
print(source.change_count)

# Only a few lines. Rows and columns are counted from 1, and the controller clamps
# the end of the range to what the module really holds.
print(robot.rws.rapid.get_module_text_range("T_ROB1", "MainModule", 1, 1, 10, 1))

# Where a piece of text sits, found is False when it is nowhere
found = robot.rws.rapid.search_module_text("T_ROB1", "MainModule", "MoveJ")
print(f"{found.found} {found.row},{found.column}")

robot.rws.mastership.request(MastershipDomain.Rapid)
try:
    # Insert one line after a range, leaving the rest of the module alone
    result = robot.rws.rapid.set_module_text_range(
        "T_ROB1", "MainModule",
        RapidTextReplaceMode.After, RapidTextQueryMode.Try_,
        5, 1, 5, 1,
        "    reg1 := 0;\r\n")

    # Rewriting the line that declares the module renames it
    print(f"{result.module_renamed} {result.new_module_name}")

    # Replace the whole source
    robot.rws.rapid.set_module_text("T_ROB1", "MainModule",
        "MODULE MainModule\r\n  PROC main()\r\n  ENDPROC\r\nENDMODULE\r\n")
finally:
    robot.rws.mastership.release(MastershipDomain.Rapid)

robot.disconnect()
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



**RapidModuleItem** ([reference](../api/underautomation.abb.rws.data.md#rapidmoduleitem))

- `RapidModuleItem()`: Initializes a new instance of the RapidModuleItem class
- `name: str`: Name of the module, for example "MainModule"
- `type: RapidModuleType`: Whether the module belongs to the program or to the system

**RapidModuleInfo** ([reference](../api/underautomation.abb.rws.data.md#rapidmoduleinfo))

- `RapidModuleInfo()`: Initializes a new instance of the RapidModuleInfo class
- `file_name: str`: Name of the file the module was loaded from, for example "MainModule.mod"
- `attributes: typing.List[RapidModuleAttribute]`: Properties declared on the module, empty when it declares none
- `attribute_count: int (read only)`: Number of properties declared on the module
- Inherited from [RapidModuleItem](../api/underautomation.abb.rws.data.md#rapidmoduleitem): `name`, `type`

**RapidModuleText** ([reference](../api/underautomation.abb.rws.data.md#rapidmoduletext))

- `RapidModuleText()`: Initializes a new instance of the RapidModuleText class
- `text: str`: Source of the module
- `change_count: int | None`: Counter the controller increments whenever the module changes, null when it did not report it
- `declared_length: int | None`: Length the controller declares for the module, null when it did not report it. This is the size the controller reserves for the module and not the length of , so the two normally differ.

**RapidModuleExtension** ([reference](../api/underautomation.abb.rws.data.md#rapidmoduleextension))

- `RapidModuleExtension()`: Initializes a new instance of the RapidModuleExtension class
- `line_count: int | None`: Number of lines the module holds, null when the controller did not report it
- `max_column_count: int | None`: Length of the longest line of the module, null when the controller did not report it
- `change_count: int | None`: Counter the controller increments whenever the module changes, null when it did not report it

**RapidSetTextRangeResult** ([reference](../api/underautomation.abb.rws.data.md#rapidsettextrangeresult))

- `RapidSetTextRangeResult()`: Initializes a new instance of the RapidSetTextRangeResult class
- `module_renamed: bool`: Whether the change renamed the module
- `new_module_name: str`: Name the module now has, empty when the change did not rename it
- `change_count: int | None`: Counter the controller incremented for the change, null when it did not report it

**RapidTextPosition** ([reference](../api/underautomation.abb.rws.data.md#rapidtextposition))

- `RapidTextPosition()`: Initializes a new instance of the RapidTextPosition class
- `row: int`: Line of the position, 0 when the search found nothing
- `column: int`: Column of the position, 0 when the search found nothing
- `found: bool (read only)`: Whether the position points at something, which it does not when a search found nothing

**RapidModuleType** ([reference](../api/underautomation.abb.rws.data.md#rapidmoduletype))

- Unknown: The controller reported a type this library does not know
- ProgramModule: A module of the program, saved and loaded with it
- SystemModule: A module of the system, which survives loading another program

**RapidModuleAttribute** ([reference](../api/underautomation.abb.rws.data.md#rapidmoduleattribute))

- Unknown: The controller reported an attribute this library does not know
- SystemModule: The module belongs to the system rather than to the program
- Encoded: The source of the module is encoded and cannot be read back
- NoView: The source of the module may not be displayed
- NoStepIn: Execution may not step into the routines of the module
- ViewOnly: The source may be displayed but not changed
- ReadOnly: The module may not be changed

**RapidTextReplaceMode** ([reference](../api/underautomation.abb.rws.data.md#rapidtextreplacemode))

- After: Insert the new text after the range, leaving it in place
- Before: Insert the new text before the range, leaving it in place
- Replace: Replace the range with the new text

**RapidTextQueryMode** ([reference](../api/underautomation.abb.rws.data.md#rapidtextquerymode))

- Force: Apply the change even when it invalidates the program pointer
- Try_: Apply the change only when the program pointer survives it

## Build errors

Linking a program never fails the request itself. The controller accepts it, then reports what it refused. `GetBuildErrors` returns one entry per error, with the module, the position and the message.

```python
from underautomation.abb.abb_controller import AbbController

robot = AbbController()
robot.connect("192.168.0.1")

# The controller answers at most thirty errors at a time, read the next ones by paging
start = 0
errors = robot.rws.rapid.get_build_errors("T_ROB1", start, 30)

while len(errors) > 0:
    for error in errors:
        print(f"{error.module_name} {error.row},{error.column}")
        print("   " + error.error)

    start += len(errors)
    errors = robot.rws.rapid.get_build_errors("T_ROB1", start, 30)

# An empty answer and a task state of Linked mean the program is runnable
print(robot.rws.rapid.get_task("T_ROB1").task_state)

robot.disconnect()
```

The controller returns at most thirty errors at a time, whatever larger limit is asked for. Use `start` and `limit` to read the rest. An empty array means the program linked cleanly, and the task state then becomes `Linked`.

`BuildTask` itself is described in [RAPID tasks & program execution](rws-rapid-tasks.md).



**RapidBuildError** ([reference](../api/underautomation.abb.rws.data.md#rapidbuilderror))

- `RapidBuildError()`: Initializes a new instance of the RapidBuildError class
- `module_name: str`: Name of the module the error was found in
- `row: int | None`: Line the error was found at, null when the controller did not report it
- `column: int | None`: Column the error was found at, null when the controller did not report it
- `error_number: int | None`: Numeric identifier of the error, null when the controller did not report it
- `error: str`: Description of the error as the controller worded it

## Breakpoints

`SetBreakpoint` places a breakpoint at a position of a module. The controller snaps it to the whole instruction holding that position, so the range it answers is normally wider than what was asked for.

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.mastership_domain import MastershipDomain
from underautomation.abb.rws.data.rapid_execution_cycle import RapidExecutionCycle
from underautomation.abb.rws.data.rapid_execution_mode import RapidExecutionMode
from underautomation.abb.rws.data.rapid_regain_mode import RapidRegainMode
from underautomation.abb.rws.data.rapid_start_condition import RapidStartCondition

robot = AbbController()
robot.connect("192.168.0.1")

robot.rws.mastership.request(MastershipDomain.Rapid)
try:
    # The controller snaps the breakpoint to the whole instruction holding the
    # position, so the range it answers is normally wider than what was asked for
    placed = robot.rws.rapid.set_breakpoint("T_ROB1", "MainModule", 12, 1)
    print(f"{placed.start_row},{placed.start_column} -> {placed.end_row},{placed.end_column}")
finally:
    robot.rws.mastership.release(MastershipDomain.Rapid)

for breakpoint in robot.rws.rapid.get_breakpoints("T_ROB1"):
    print(f"{breakpoint.module_name} {breakpoint.start_row}")

# A breakpoint only stops the program when execution was started with stopAtBreakpoint
robot.rws.rapid.start(RapidRegainMode.Continue_, RapidExecutionMode.Continue_,
                      RapidExecutionCycle.Forever, RapidStartCondition.None_, True, False)

robot.disconnect()
```

A breakpoint only stops the program when execution was started with `stopAtBreakpoint` set to `true`, see [RAPID tasks & program execution](rws-rapid-tasks.md). Editing the source moves the positions, so read the breakpoints again after a change.

**Methods of RapidService** ([reference](../api/underautomation.abb.rws.services.md#rapidservice-robotrwsrapid))

- `get_breakpoints(task: str, start: int | None=None, limit: int | None=None) -> typing.List[RapidBreakpoint]`: Gets the breakpoints set in the program of a task (synchronous)
- `set_breakpoint(task: str, module: str, row: int, column: int) -> RapidBreakpoint`: Sets a breakpoint at a position of a module (synchronous)

**RapidBreakpoint** ([reference](../api/underautomation.abb.rws.data.md#rapidbreakpoint))

- `RapidBreakpoint()`: Initializes a new instance of the RapidBreakpoint class
- `module_name: str`: Name of the module the breakpoint sits in, null when the controller did not report it
- `start_row: int | None`: Line the breakpoint starts at, null when the controller did not report it
- `start_column: int | None`: Column the breakpoint starts at, null when the controller did not report it
- `end_row: int | None`: Line the breakpoint ends at, null when the controller did not report it
- `end_column: int | None`: Column the breakpoint ends at, null when the controller did not report it

## Modify a taught position

This is the teaching gesture of the FlexPendant: jog the robot where it should go, then write that position back into the motion instruction of the program.

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.mastership_domain import MastershipDomain

robot = AbbController()
robot.connect("192.168.0.1")

# How many motion instructions of this range can be rewritten
modifiable = robot.rws.rapid.get_modifiable_positions("T_ROB1", "MainModule", 1, 1, 40, 1)
print(modifiable.modifiable_line_count)

# Every one of them, in every task of the system
for item in robot.rws.rapid.get_all_modifiable_positions():
    print(f"{item.task_name}/{item.module_name} line {item.start_row}")

# Jog the robot where it should go, then write that position into the program
robot.rws.mastership.request(MastershipDomain.Rapid)
try:
    robot.rws.rapid.modify_position("T_ROB1", "MainModule", 12, 1, 12, 1, True, True, False)
finally:
    robot.rws.mastership.release(MastershipDomain.Rapid)

robot.disconnect()
```

`GetModifiablePositions` says how many motion instructions of a range can be rewritten, `GetAllModifiablePositions` lists every one of them in every task of the system. Read one of the two before writing, so you know what is about to change.

- `checkLimits` makes the controller refuse a position outside the working range.
- `checkDeactivatedAxes` makes it refuse to rewrite an axis that is deactivated, and `allowDeactivated` rewrites it anyway.
- `ModifyAllPositions` rewrites everything at once. The controller only accepts it from a client it considers local.

Jogging the robot to the position is done with the [motion system service](rws-motion.md), and it needs the `Motion` [mastership](rws-mastership.md), which is a different domain from `Rapid`.



**RapidModifiablePositions** ([reference](../api/underautomation.abb.rws.data.md#rapidmodifiablepositions))

- `RapidModifiablePositions()`: Initializes a new instance of the RapidModifiablePositions class
- `modifiable_line_count: int`: Number of motion instructions of the range whose position can be rewritten
- `start_row: int | None`: Line the modifiable range starts at, null when the controller did not report it
- `start_column: int | None`: Column the modifiable range starts at, null when the controller did not report it
- `end_row: int | None`: Line the modifiable range ends at, null when the controller did not report it
- `end_column: int | None`: Column the modifiable range ends at, null when the controller did not report it

**RapidModifiablePositionItem** ([reference](../api/underautomation.abb.rws.data.md#rapidmodifiablepositionitem))

- `RapidModifiablePositionItem()`: Initializes a new instance of the RapidModifiablePositionItem class
- `module_name: str`: Name of the module holding the instruction
- `task_name: str`: Name of the task holding the module
- `start_row: int | None`: Line the instruction starts at, null when the controller did not report it
- `start_column: int | None`: Column the instruction starts at, null when the controller did not report it
- `end_row: int | None`: Line the instruction ends at, null when the controller did not report it
- `end_column: int | None`: Column the instruction ends at, null when the controller did not report it

## Write an editor

The last group of methods exists for the applications that edit RAPID, not for the ones that drive a robot. They give what an editor needs: what is declared at a position, the arguments of a call, a complete instruction ready to be written, and the palette an operator picks an instruction from.

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.rapid_object_list_type import RapidObjectListType

robot = AbbController()
robot.connect("192.168.0.1")

# What is declared at this position of the source, None when nothing is
symbol = robot.rws.rapid.get_module_symbol("T_ROB1", "MainModule", 12, 5)
if symbol is not None:
    print(f"{symbol.name} {symbol.symbol_type} {symbol.data_type}")

# The routine called at this position, and the arguments of that call
routine = robot.rws.rapid.get_routine("T_ROB1", "MainModule", 12, 5)
print(f"{routine.name} {routine.parameter_count}")

for argument in robot.rws.rapid.get_routine_arguments("T_ROB1", "MainModule", 12, 5):
    print(f"{argument.data_type} at {argument.start_row},{argument.start_column}")

# A complete instruction ready to be written, instead of a bare keyword
template = robot.rws.rapid.get_instruction_template("T_ROB1", "MainModule", "MoveJ")
for argument in template.arguments:
    print(f"{argument.name} = {argument.value} ({argument.data_type})")

# Where the parts of an object begin and end, given the whole span of that object
children = robot.rws.rapid.get_object_children("T_ROB1", "MainModule", 1, 1, 40, 1)
for item in children.ranges:
    print(f"{item.name}: {item.range}")

# Where one of the lists an object holds sits, without reading the module
object_list = robot.rws.rapid.get_object_list_extension(
    "RAPID/T_ROB1/MainModule", RapidObjectListType.RoutineDeclarations)
print(f"{object_list.list} first {object_list.first} last {object_list.last}")

robot.disconnect()
```

`GetModuleSymbol` returns the declaration found at a position, `null` when there is none. `GetRoutine` and `GetRoutineArguments` work on a position sitting on a routine call, and the controller refuses the request when it does not.

`GetInstructionTemplate` returns a complete instruction with the arguments the controller suggests, instead of a bare keyword. `GetObjectChildren` and `GetObjectListExtension` give where the parts of an object begin and end, which is how an editor jumps to the declarations of a module without reading the whole source.

```python
from underautomation.abb.abb_controller import AbbController

robot = AbbController()
robot.connect("192.168.0.1")

# Categories of the instruction palette, the same ones an editor shows
for head in robot.rws.rapid.get_pallet_heads("T_ROB1"):
    print(f"{head.number}: {head.name}")

    # Instructions of that category
    for item in robot.rws.rapid.get_pallet("T_ROB1", head.number):
        print(f"   {item.name} {item.instruction}")

# Types the controller suggests for one argument of an instruction
for data_type in robot.rws.rapid.get_preferred_data_types("T_ROB1", "AliasIO", "FromSignal"):
    print(f"{data_type.name} ({data_type.data_type})")

robot.disconnect()
```

`GetPalletHeads` returns the categories of the instruction palette, `GetPallet` the instructions of one category, and `GetPreferredDataTypes` the types that fit one argument of an instruction.



**RapidModuleSymbol** ([reference](../api/underautomation.abb.rws.data.md#rapidmodulesymbol))

- `RapidModuleSymbol()`: Initializes a new instance of the RapidModuleSymbol class
- `version: str`: Version the controller stamps on the declaration
- `name: str`: Name of the declared symbol
- `symbol_url: str`: Path of the symbol, which the symbol resources take
- `symbol_type: RapidSymbolType`: What kind of symbol was declared
- `linked: bool | None`: Whether the declaration is complete, null when the controller did not report it
- `local: bool | None`: Whether the symbol is local to its module, null when the controller did not report it
- `type_url: str`: Path of the type of the symbol
- `data_type: str`: Name of the type of the symbol, for example "robtarget"
- `dimensions: int | None`: Number of array dimensions of the symbol, null when the controller did not report it
- `storage: int | None`: How the controller stores the symbol, null when it did not report it
- `heap: bool | None`: Whether the symbol is allocated on the heap, null when the controller did not report it
- `reference_count: int | None`: How many times the symbol is referred to, null when the controller did not report it

**RapidRoutineInfo** ([reference](../api/underautomation.abb.rws.data.md#rapidroutineinfo))

- `RapidRoutineInfo()`: Initializes a new instance of the RapidRoutineInfo class
- `symbol_url: str`: Path of the routine, which the program pointer resources take
- `name: str`: Name of the routine
- `symbol_type: RapidSymbolType`: Whether the routine is a procedure, a function or a trap
- `named: bool | None`: Whether the routine is named, null when the controller did not report it
- `local: bool | None`: Whether the routine is local to its module, null when the controller did not report it
- `parameter_count: int | None`: Number of parameters the routine takes, null when the controller did not report it. The controller reports -1 when the parameter list is not linked yet.

**RapidRoutineArgument** ([reference](../api/underautomation.abb.rws.data.md#rapidroutineargument))

- `RapidRoutineArgument()`: Initializes a new instance of the RapidRoutineArgument class
- `parameter_number: int | None`: Position of the argument in the call, counted from 0
- `alternate_argument: int | None`: Which alternative of the parameter this argument fills, null when the controller did not report it
- `start_row: int | None`: Line the argument starts at, null when the controller did not report it
- `start_column: int | None`: Column the argument starts at, null when the controller did not report it
- `end_row: int | None`: Line the argument ends at, null when the controller did not report it
- `end_column: int | None`: Column the argument ends at, null when the controller did not report it
- `object_type: str`: What the argument is, for example a required argument or a name reference
- `data_type: str`: Type of the argument, for example "num"
- `list_number: int | None`: Position of the argument in the argument list, null when the controller did not report it
- `list_length: int | None`: Length of the argument list, null when the controller did not report it

**RapidInstructionTemplate** ([reference](../api/underautomation.abb.rws.data.md#rapidinstructiontemplate))

- `RapidInstructionTemplate()`: Initializes a new instance of the RapidInstructionTemplate class
- `argument_count: int | None`: Number of arguments the controller reported, null when it did not report it
- `mark: int | None`: Index the controller started reporting from, null when it did not report it
- `complete: bool | None`: Whether every argument has been reported, null when the controller did not report it
- `version: str`: Version the controller stamps on the template
- `selected_parameter: int | None`: Argument the controller suggests selecting first, null when it did not report it
- `arguments: typing.List[RapidInstructionTemplateArgument]`: The suggested arguments

**RapidInstructionTemplateArgument** ([reference](../api/underautomation.abb.rws.data.md#rapidinstructiontemplateargument))

- `RapidInstructionTemplateArgument()`: Initializes a new instance of the RapidInstructionTemplateArgument class
- `argument_number: int | None`: Position of the argument, null when the controller did not report it
- `required: bool | None`: Whether the argument has to be given, null when the controller did not report it
- `name: str`: Name of the argument, for example "ToPoint"
- `declaration_needed: bool | None`: Whether inserting the instruction also needs a declaration to be created for this argument, null when the controller did not report it
- `symbol: str`: Name of the symbol the argument refers to, empty when the argument is written as a literal
- `value: str`: Value the argument is suggested with, written the way RAPID writes it
- `data_type: str`: Type of the argument, for example "robtarget"
- `object_type: str`: How the suggested symbol is declared, for example "CONST" or "TASK PERS"
- `local: bool | None`: Whether the suggested symbol is local to its module, null when the controller did not report it
- `dimensions: int | None`: Number of array dimensions of the argument, null when the controller did not report it

**RapidObjectChild** ([reference](../api/underautomation.abb.rws.data.md#rapidobjectchild))

- `RapidObjectChild()`: Initializes a new instance of the RapidObjectChild class
- `get_range(name: str) -> RapidTextRange`: Returns the span of one part by its name, null when the controller did not report it
- `object_type: str`: What the object is, for example "module"
- `ranges: typing.List[RapidObjectChildRange]`: The parts of the object, including the ones it does not hold, whose span is then empty
- `range_count: int (read only)`: Number of parts the controller reported

**RapidObjectChildRange** ([reference](../api/underautomation.abb.rws.data.md#rapidobjectchildrange))

- `RapidObjectChildRange()`: Initializes a new instance of the RapidObjectChildRange class
- `name: str`: Name of the part as the controller worded it, for example "data-decl" or "endmod"
- `range: RapidTextRange`: Where the part sits in the source
- `is_present: bool (read only)`: Whether the controller reported a real span for the part, which it does not when the object does not hold it

**RapidObjectListExtension** ([reference](../api/underautomation.abb.rws.data.md#rapidobjectlistextension))

- `RapidObjectListExtension()`: Initializes a new instance of the RapidObjectListExtension class
- `list: RapidTextRange`: Span of the whole list
- `first: RapidTextRange`: Span of the first element of the list
- `last: RapidTextRange`: Span of the last element of the list

**RapidObjectListType** ([reference](../api/underautomation.abb.rws.data.md#rapidobjectlisttype))

- Statements: The statements of the object
- BackwardStatements: The statements of its BACKWARD handler
- ErrorStatements: The statements of its ERROR handler
- UndoStatements: The statements of its UNDO handler
- TypeDeclarations: The type declarations it holds
- DataDeclarations: The data declarations it holds
- ParameterDeclarations: The parameter declarations it holds
- RoutineDeclarations: The routine declarations it holds
- Attributes: The attributes it declares

**RapidPalletHeadItem** ([reference](../api/underautomation.abb.rws.data.md#rapidpalletheaditem))

- `RapidPalletHeadItem()`: Initializes a new instance of the RapidPalletHeadItem class
- `name: str`: Name of the category, for example "Motion&Proc."
- `number: int | None`: Number identifying the category, null when the controller did not report it

**RapidPalletItem** ([reference](../api/underautomation.abb.rws.data.md#rapidpalletitem))

- `RapidPalletItem()`: Initializes a new instance of the RapidPalletItem class
- `name: str`: Name shown for the entry, for example "MoveJ"
- `instruction: str`: Instruction the entry inserts
- `parameter: int | None`: Parameter the entry preselects, null when the controller did not report it
- `alternative: int | None`: Alternative of the parameter the entry preselects, null when the controller did not report it
- `keyword: int | None`: Whether the entry is a language keyword rather than an instruction, null when the controller did not report it

**RapidPreferredDataTypeItem** ([reference](../api/underautomation.abb.rws.data.md#rapidpreferreddatatypeitem))

- `RapidPreferredDataTypeItem()`: Initializes a new instance of the RapidPreferredDataTypeItem class
- `name: str`: Name of the suggestion, for example "signaldi"
- `data_type: str`: Data type of the suggestion

## What is not on this page

The values the modules declare are read and written from [RAPID variables & symbols](rws-rapid-symbols.md). Starting the program, moving the program pointer and loading one module are on [RAPID tasks & program execution](rws-rapid-tasks.md). Uploading a module file to the controller, and downloading a saved one, are on [File system](rws-files.md).

## Try it in the demo application

The **RAPID (RWS)** page of the [demo application](demo-app.md) exercises these calls against a live controller, without writing any code. It is shown in [RAPID tasks & program execution](rws-rapid-tasks.md).
