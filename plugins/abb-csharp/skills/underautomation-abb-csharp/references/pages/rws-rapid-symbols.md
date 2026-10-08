# RAPID variables & symbols

Read and write RAPID variables, persistents and constants, search symbols in the loaded program, and validate a value before writing it.

Web page: https://underautomation.com/abb/documentation/rws-rapid-symbols

A RAPID symbol is anything the program declares: a variable, a persistent, a constant, a routine, a type, a module, a task. `robot.Rws.Rapid` reads and writes them by their path, with the same two methods for every RAPID type.

Reading a value needs nothing more than a connection. Writing one needs the `Rapid` [mastership](rws-mastership.md).

## The path of a symbol

> **Available on** RWS 1.0 (IRC5) : yes | RWS 2.0 (OmniCore) : yes. The paths, the methods and the text of the values are the same on an IRC5 and on an OmniCore.

Every symbol has a path. It starts with `RAPID`, then the task, then the module, then the name. This path is what `GetSymbolValue` and `SetSymbolValue` take.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class RapidSymbolPath
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // A variable declared in the module MainModule of the task T_ROB1
        robot.Rws.Rapid.GetSymbolValue("RAPID/T_ROB1/MainModule/myCounter");

        // reg1 and the other predefined registers live in the built-in module "user"
        robot.Rws.Rapid.GetSymbolValue("RAPID/T_ROB1/user/reg1");

        // A leading slash is accepted, it is removed by the SDK
        robot.Rws.Rapid.GetSymbolValue("/RAPID/T_ROB1/user/reg1");

        // A module of the task, and the task itself, are symbols too
        robot.Rws.Rapid.GetSymbolProperties("RAPID/T_ROB1/MainModule");
        robot.Rws.Rapid.GetSymbolProperties("RAPID/T_ROB1");

        // A RAPID type has a path of its own, without any task
        robot.Rws.Rapid.GetSymbolProperties("RAPID/robtarget");

        robot.Disconnect();
    }
}
```

| Path                                | What it names                                              |
| ----------------------------------- | ---------------------------------------------------------- |
| `RAPID/T_ROB1/MainModule/myCounter` | A variable, a persistent or a constant of a module         |
| `RAPID/T_ROB1/user/reg1`            | `reg1` to `reg5`, which live in the built-in module `user` |
| `RAPID/T_ROB1/MainModule`           | The module itself                                          |
| `RAPID/T_ROB1`                      | The task itself                                            |
| `RAPID/robtarget`                   | A RAPID type, which belongs to no task                     |

The path is case sensitive on the name of the module and on the name of the symbol. A leading slash is accepted, the SDK removes it. When no symbol has that path, the controller answers 404 and the SDK throws an `RwsException`.

If you do not know where a variable is declared, do not guess the path, search for it with `SearchSymbols`.

## Read a value

`GetSymbolValue` returns the value as the text RAPID writes it with, plus where the declaration sits in the module. There is no typed overload, a `num`, a `bool` and a `robtarget` all come back as a string.

```csharp
using System.Globalization;
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class RapidReadValue
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // A value always comes back as the text RAPID writes it with. Reading needs no mastership.
        RapidSymbolValue value = robot.Rws.Rapid.GetSymbolValue("RAPID/T_ROB1/user/reg1");
        Console.WriteLine(value.Value);                  // "42"
        Console.WriteLine(value.DeclarationPosition);    // where the declaration sits in the module

        // num and dnum: parse with the invariant culture, RAPID uses a dot as decimal separator
        double number = double.Parse(robot.Rws.Rapid.GetSymbolValue("RAPID/T_ROB1/user/reg1").Value,
                                     CultureInfo.InvariantCulture);

        // bool: the controller writes TRUE or FALSE
        bool flag = robot.Rws.Rapid.GetSymbolValue("RAPID/T_ROB1/MainModule/myFlag")
                                   .Value.Trim().Equals("TRUE", StringComparison.OrdinalIgnoreCase);

        // string: the value carries the RAPID quotes, remove them
        string text = robot.Rws.Rapid.GetSymbolValue("RAPID/T_ROB1/MainModule/myText").Value.Trim('"');

        Console.WriteLine(number + " " + flag + " " + text);

        robot.Disconnect();
    }
}
```

| RAPID type                     | What `Value` holds                                                  |
| ------------------------------ | ------------------------------------------------------------------- |
| `num`, `dnum`                  | `42`, `1.5`, `9E+09`. Always a dot as decimal separator.            |
| `bool`                         | `TRUE` or `FALSE`, in capitals                                      |
| `string`                       | The RAPID quotes are part of the value, `"hello"`                   |
| `robtarget`, `pos`, any record | The bracketed form, `[[515,0,712],[1,0,0,0],[0,0,0,0],[9E+09,...]]` |
| An array                       | One value too, `[1,2,3]`                                            |

Parse the numbers with `CultureInfo.InvariantCulture`. On a machine configured with a French or a German locale, `double.Parse("1.5")` without it gives 15.

## Write a value

`SetSymbolValue` takes the same text form. The controller checks the value against the type of the symbol and answers 400 when it does not match.

```csharp
using System.Globalization;
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class RapidWriteValue
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // Writing needs the RAPID mastership. Take it, write, give it back.
        robot.Rws.Mastership.Request(MastershipDomain.Rapid);
        try
        {
            // num: format with the invariant culture, "1,5" is refused, "1.5" is accepted
            double speed = 1.5;
            robot.Rws.Rapid.SetSymbolValue("RAPID/T_ROB1/user/reg1",
                                           speed.ToString(CultureInfo.InvariantCulture));

            // bool: TRUE or FALSE, in capitals
            robot.Rws.Rapid.SetSymbolValue("RAPID/T_ROB1/MainModule/myFlag", "TRUE");

            // string: the RAPID quotes are part of the value
            robot.Rws.Rapid.SetSymbolValue("RAPID/T_ROB1/MainModule/myText", "\"hello\"");
        }
        finally
        {
            robot.Rws.Mastership.Release(MastershipDomain.Rapid);
        }

        robot.Disconnect();
    }
}
```

What readers get wrong, in order:

- **The mastership.** Without the `Rapid` [mastership](rws-mastership.md) the controller answers 403. In manual mode it also wants the write access an operator grants from the FlexPendant.
- **The culture.** `speed.ToString()` on a French machine writes `1,5`, which the controller refuses. Always format with `CultureInfo.InvariantCulture`.
- **The quotes of a string.** The value of a RAPID `string` carries them, `"\"hello\""` and not `"hello"`.
- **A constant.** A `CONST` cannot be written while the program runs. `GetSymbolProperties` reports it, its `ReadOnly` property is `true`.
- **A local variable.** A variable declared inside a routine only exists while the routine runs.

Writing a variable does not change the declaration. After a program reset the symbol goes back to the value written in its source, see below.

**Methods of RapidService** ([reference](../api/UnderAutomation.ABB.Rws.Services.md#rapidservice-robotrwsrapid))

- `RapidSymbolValue GetSymbolValue(string symbolUrl)`: Gets the value of a RAPID symbol and where it is declared (synchronous)
  - async: `Task<RapidSymbolValue> GetSymbolValueAsync(string symbolUrl, CancellationToken cancellationToken = default)`
- `void SetSymbolInitialValue(string symbolUrl, string value)`: Sets the value a RAPID symbol is declared with, which is the one it goes back to when the program is reset (synchronous)
  - async: `Task SetSymbolInitialValueAsync(string symbolUrl, string value, CancellationToken cancellationToken = default)`
- `void SetSymbolValue(string symbolUrl, string value)`: Sets the value a RAPID symbol currently holds (synchronous)
  - async: `Task SetSymbolValueAsync(string symbolUrl, string value, CancellationToken cancellationToken = default)`

**RapidSymbolValue** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidsymbolvalue))

- `RapidSymbolValue()`: Initializes a new instance of the Data.RapidSymbolValue class
- `RapidTextRange DeclarationPosition { get; set; }`: Where the symbol is declared, null when the controller did not report it
- `RapidTextRange InitialValuePosition { get; set; }`: Where the initial value of the symbol is written, null when the controller did not report it. The controller reports zeros when the declaration carries no initial value.
- `string Value { get; set; }`: Value of the symbol, written the way RAPID writes it

**RapidTextRange** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidtextrange))

- `RapidTextRange()`: Initializes a new instance of the Data.RapidTextRange class
- `int? BeginColumn { get; set; }`: Column the range begins at, null when the controller did not report it
- `int? BeginRow { get; set; }`: Line the range begins at, null when the controller did not report it
- `int? EndColumn { get; set; }`: Column the range ends at, null when the controller did not report it
- `int? EndRow { get; set; }`: Line the range ends at, null when the controller did not report it

## Records, arrays and the initial value

A record is not taken apart by the SDK. You get the bracketed text, in the same order as the components of the type, and you write it back the same way.

```csharp
using System.Globalization;
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class RapidRecordValue
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // A record comes back in the bracketed form RAPID writes it with. The SDK does not
        // take it apart, you get the text and parse what you need.
        RapidSymbolValue target = robot.Rws.Rapid.GetSymbolValue("RAPID/T_ROB1/MainModule/pHome");
        Console.WriteLine(target.Value);
        // [[515,0,712],[0,0,1,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]]

        // An array is one value too, its elements separated by commas
        Console.WriteLine(robot.Rws.Rapid.GetSymbolValue("RAPID/T_ROB1/MainModule/myArray").Value);  // [1,2,3]

        // Build the text with the invariant culture, a comma as decimal separator is refused
        double x = 515.5, y = 0, z = 712;
        string pose = string.Format(CultureInfo.InvariantCulture,
                                    "[[{0},{1},{2}],[0,0,1,0],[0,0,0,0],[9E9,9E9,9E9,9E9,9E9,9E9]]",
                                    x, y, z);

        robot.Rws.Mastership.Request(MastershipDomain.Rapid);
        try
        {
            // The value has to carry every component the type declares
            robot.Rws.Rapid.SetSymbolValue("RAPID/T_ROB1/MainModule/pHome", pose);
        }
        finally
        {
            robot.Rws.Mastership.Release(MastershipDomain.Rapid);
        }

        robot.Disconnect();
    }
}
```

`SetSymbolInitialValue` writes the value the declaration carries, the one the symbol goes back to when the program is reset. It rewrites the source of the module, so the module counts as changed afterwards. `SetSymbolValue` only changes what the symbol holds right now.

`InitialValuePosition` of `RapidSymbolValue` says where that initial value sits in the source. The controller reports zeros when the declaration carries none.

## Check a value before writing it

`ValidateSymbolValue` asks the controller whether it would accept a value for a given type, without writing it anywhere. It returns `false` for a refused value instead of throwing, so it is what an editor uses to tell an operator that what they typed is wrong.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class RapidValidateValue
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // Ask the controller whether it would take the value, without writing it anywhere
        Console.WriteLine(robot.Rws.Rapid.ValidateSymbolValue("T_ROB1", "num", "1.5"));      // true

        // A value that does not fit the type gives false, it does not throw
        Console.WriteLine(robot.Rws.Rapid.ValidateSymbolValue("T_ROB1", "num", "hello"));    // false

        robot.Rws.Mastership.Request(MastershipDomain.Rapid);
        try
        {
            if (robot.Rws.Rapid.ValidateSymbolValue("T_ROB1", "num", "1.5"))
                robot.Rws.Rapid.SetSymbolValue("RAPID/T_ROB1/user/reg1", "1.5");

            // The value written in the declaration, the one the symbol goes back to when the
            // program is reset. This rewrites the source of the module.
            robot.Rws.Rapid.SetSymbolInitialValue("RAPID/T_ROB1/MainModule/myCounter", "0");
        }
        finally
        {
            robot.Rws.Mastership.Release(MastershipDomain.Rapid);
        }

        robot.Disconnect();
    }
}
```

Any other failure, a type that does not exist for example, is still reported as an `RwsException`.

**Methods of RapidService** ([reference](../api/UnderAutomation.ABB.Rws.Services.md#rapidservice-robotrwsrapid))

- `bool ValidateSymbolValue(string task, string dataType, string value)`: Asks the controller whether a value would be accepted for a given RAPID type, without writing it anywhere (synchronous) This is what an editor uses to tell an operator that what they typed is wrong before the write is attempted.
  - async: `Task<bool> ValidateSymbolValueAsync(string task, string dataType, string value, CancellationToken cancellationToken = default)`

## Search symbols

`SearchSymbols` walks the program and returns the symbols matching a set of criteria. It is the way to list the `robtarget` of a module, to find every persistent of a task, or to check that a variable exists before writing it.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class RapidSearchSymbols
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // Always give a starting point, a search without any criterion walks the whole system
        RapidSymbolSearchCriteria criteria = new RapidSymbolSearchCriteria();
        criteria.View = RapidSymbolSearchView.Block;
        criteria.BlockUrl = "RAPID/T_ROB1";
        criteria.Recursive = true;
        criteria.NamePattern = "^p[0-9]+$";        // regular expression on the name
        criteria.DataType = "robtarget";

        // Only the first entry is sent, search again for another kind
        criteria.SymbolTypes = new RapidSymbolType[] { RapidSymbolType.Persistent };

        foreach (RapidSymbolProperties symbol in robot.Rws.Rapid.SearchSymbols(criteria))
        {
            Console.WriteLine(symbol.Name + " (" + symbol.DataType + ")");

            // SymbolUrl is the path the other symbol methods take
            Console.WriteLine(robot.Rws.Rapid.GetSymbolValue(symbol.SymbolUrl).Value);
        }

        // What one symbol is declared as, without reading its value
        RapidSymbolProperties properties = robot.Rws.Rapid.GetSymbolProperties("RAPID/T_ROB1/user/reg1");
        Console.WriteLine(properties.SymbolType);   // Variable, Persistent, Constant, ...
        Console.WriteLine(properties.DataType);     // num
        Console.WriteLine(properties.ReadOnly);     // null when the controller did not report it

        robot.Disconnect();
    }
}
```

Always set `BlockUrl`. A search with no criterion at all walks the whole system and takes seconds.

| `RapidSymbolSearchView` | Where the search looks                                                                           |
| ----------------------- | ------------------------------------------------------------------------------------------------ |
| `Block`                 | In the block named by `BlockUrl`, and in what it contains when `Recursive` is `true`             |
| `Scope`                 | In what is visible from a position of the source, which needs `PositionRow` and `PositionColumn` |
| `Stack`                 | In what is visible from a frame of the call stack, which needs the program pointer to be set     |
| `Undefined`             | Let the controller decide                                                                        |

`SymbolTypes` filters on the kind of symbol: `Variable`, `Persistent`, `Constant`, `Function`, `Procedure`, `Trap`, `Module`, and the others of `RapidSymbolType`. The controller keeps only one kind per search, so only the first entry of the array is sent. Search once per kind when you need several.

`NamePattern` is a regular expression, not a wildcard. `DataType` takes the name of a RAPID type, for example `robtarget`.

`GetSymbolProperties` returns the same information for one symbol: its kind, its type, whether it is local to its module, whether it is read only. A property the controller did not report comes back as `null`, so test the nullable properties before using them.

**Methods of RapidService** ([reference](../api/UnderAutomation.ABB.Rws.Services.md#rapidservice-robotrwsrapid))

- `RapidSymbolProperties GetSymbolProperties(string symbolUrl)`: Gets what a RAPID symbol is declared as (synchronous)
  - async: `Task<RapidSymbolProperties> GetSymbolPropertiesAsync(string symbolUrl, CancellationToken cancellationToken = default)`
- `RapidSymbolProperties[] SearchSymbols(RapidSymbolSearchCriteria criteria)`: Finds the RAPID symbols matching a set of criteria (synchronous)
  - async: `Task<RapidSymbolProperties[]> SearchSymbolsAsync(RapidSymbolSearchCriteria criteria, CancellationToken cancellationToken = default)`

**RapidSymbolProperties** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidsymbolproperties))

- `RapidSymbolProperties()`: Initializes a new instance of the Data.RapidSymbolProperties class
- `string DataType { get; set; }`: Name of the type of the symbol, for example "num"
- `string Dimension { get; set; }`: Size of each array dimension as the controller worded it, empty when the symbol is not an array
- `int? Dimensions { get; set; }`: Number of array dimensions of the symbol, null when the controller did not report it
- `bool? Heap { get; set; }`: Whether the symbol is allocated on the heap, null when the controller did not report it
- `bool? Linked { get; set; }`: Whether the declaration is complete, null when the controller did not report it
- `bool? Local { get; set; }`: Whether the symbol is local to its module, null when the controller did not report it
- `string Name { get; set; }`: Name of the symbol, for example "reg1"
- `bool? Named { get; set; }`: Whether the symbol is named, null when the controller did not report it
- `bool? ReadOnly { get; set; }`: Whether the symbol may not be written, null when the controller did not report it
- `string Storage { get; set; }`: How the controller stores the symbol, for example "loaded"
- `RapidSymbolType SymbolType { get; set; }`: What kind of symbol this is
- `string SymbolUrl { get; set; }`: Path of the symbol, which the other symbol methods take
- `bool? TaskVariable { get; set; }`: Whether the symbol is global within its task, null when the controller did not report it
- `string TypeUrl { get; set; }`: Path of the type of the symbol, for example "RAPID/num"

**RapidSymbolSearchCriteria** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidsymbolsearchcriteria))

- `RapidSymbolSearchCriteria()`: Initializes a new instance of the Data.RapidSymbolSearchCriteria class
- `string BlockUrl { get; set; }`: Path the search starts from, for example "RAPID/T_ROB1"
- `string DataType { get; set; }`: Name of the type a symbol has to have to be kept, for example "robtarget"
- `string NamePattern { get; set; }`: Regular expression the name of a symbol has to match to be kept
- `bool? OnlyUsed { get; set; }`: Whether only the symbols the program actually refers to are kept, null to leave it to the controller
- `int? PositionColumn { get; set; }`: Column the search starts from, used together with RapidSymbolSearchView.Scope
- `int? PositionRow { get; set; }`: Line the search starts from, used together with RapidSymbolSearchView.Scope
- `bool? Recursive { get; set; }`: Whether the search also walks what the starting point contains, null to leave it to the controller
- `bool? SkipShared { get; set; }`: Whether the symbols shared between tasks are skipped, null to leave it to the controller
- `int? StackFrame { get; set; }`: Frame of the call stack the search starts from, used together with RapidSymbolSearchView.Stack
- `RapidSymbolType[] SymbolTypes { get; set; }`: Kinds of symbol the search keeps, empty to keep every kind
- `RapidSymbolVariableType VariableType { get; set; }`: Which variables the search keeps, by what may be done with them
- `RapidSymbolSearchView View { get; set; }`: Which part of the system the search walks

**RapidSymbolType** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidsymboltype))

- Alias: An alias of another type
- Any: Any of the other types, which a search uses to mean that it does not filter on the type
- Atomic: A built-in type such as num or string
- Constant: A constant
- ForVariable: The loop variable of a FOR statement
- Function: A function
- Label: A label
- Module: A module
- Parameter: A parameter of a routine
- Persistent: A persistent variable, whose value survives a restart
- Procedure: A procedure
- Record: A record type
- RecordComponent: One component of a record
- Task: A task
- Trap: A trap routine
- Undefined: The type is not defined
- Unknown: The controller reported a type this library does not know
- Variable: A variable

**RapidSymbolSearchView** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidsymbolsearchview))

- Block: Search the block the search path names, and optionally what it contains
- Scope: Search what is visible from a position of the source, which the search path and the position both have to be given for
- Stack: Search what is visible from a frame of the call stack, which needs the program pointer to be set
- Undefined: Let the controller decide

**RapidSymbolVariableType** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidsymbolvariabletype))

- Any: Any of them
- Loop: Only the loop variables
- ReadOnly: Only the variables that can be read but not written
- ReadWrite: Only the variables that can be read and written
- Undefined: Let the controller decide

## Persistent variables shared between tasks

A `PERS` declared in several tasks holds the same value in all of them, as long as the module is synchronized with the others. `GetSyncPersStatus` reports it, `SyncPersistentVariables` does the synchronization.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class RapidPersistentSync
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // A persistent declared in several tasks holds the same value everywhere, as long as
        // the module is synchronized with the other tasks declaring it
        Console.WriteLine(robot.Rws.Rapid.GetSyncPersStatus("T_ROB1", "MainModule"));

        robot.Rws.Mastership.Request(MastershipDomain.Rapid);
        try
        {
            robot.Rws.Rapid.SyncPersistentVariables("T_ROB1", "MainModule");
        }
        finally
        {
            robot.Rws.Mastership.Release(MastershipDomain.Rapid);
        }

        robot.Disconnect();
    }
}
```

**Methods of RapidService** ([reference](../api/UnderAutomation.ABB.Rws.Services.md#rapidservice-robotrwsrapid))

- `bool GetSyncPersStatus(string task, string module)`: Gets whether the persistent variables of a module are kept synchronized with the other tasks declaring them (synchronous)
  - async: `Task<bool> GetSyncPersStatusAsync(string task, string module, CancellationToken cancellationToken = default)`
- `void SyncPersistentVariables(string task, string module)`: Synchronizes the persistent variables of a module with the other tasks declaring them (synchronous)
  - async: `Task SyncPersistentVariablesAsync(string task, string module, CancellationToken cancellationToken = default)`

## Errors you can expect

| Status | What happened                                                                                                                      |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| 400    | The value does not match the type of the symbol, or the number was formatted with a comma                                          |
| 403    | Your connection does not hold the `Rapid` [mastership](rws-mastership.md), or the user account lacks the UAS grant |
| 404    | No symbol has that path. Check the case of the module and of the name.                                                             |
| 500    | The controller cannot do it in its current state, for example writing a local variable of a routine that is not running            |

A complete example, with a `num`, a `bool`, a `string` and a `robtarget`, is given in [Read & write RAPID variables](read-write-rapid-variables.md).

The values of the RAPID symbols are the same on the two controller generations. The starting and stopping of the program that uses them is on [RAPID tasks & program execution](rws-rapid-tasks.md), and the source of the modules declaring them on [RAPID modules & program files](rws-rapid-modules.md).

## Try it in the demo application

The **RAPID (RWS)** page of the [demo application](demo-app.md) exercises these calls against a live controller, without writing any code. It is shown in [RAPID tasks & program execution](rws-rapid-tasks.md).
