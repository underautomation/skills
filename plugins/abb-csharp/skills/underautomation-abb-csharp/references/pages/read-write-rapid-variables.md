# Read & write RAPID variables

Read and write a RAPID num, bool, string, robtarget or a custom record from C#, on IRC5 and on OmniCore.

Web page: https://underautomation.com/abb/documentation/read-write-rapid-variables

To read a RAPID variable from C#, call `robot.Rws.Rapid.GetSymbolValue(path)`. To write one, take the RAPID mastership and call `SetSymbolValue(path, value)`. Values travel as text, written the way RAPID writes them: a `num` is `"42"`, a `bool` is `"TRUE"`, a `robtarget` is one bracketed line.

> **Available on** RWS 1.0 (IRC5) : yes | RWS 2.0 (OmniCore) : yes.

## The path of a variable

A variable is named by its path in the RAPID tree: the task, the module, then the name of the symbol. `reg1` and the other predefined registers live in the built-in module `user`.

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

Variables, persistents and constants are read the same way. A persistent is the usual choice for data exchanged with a PC, because its value survives a program restart.

## Read a num, a bool or a string

Reading needs no mastership. The value comes back in `RapidSymbolValue.Value`, as text.

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

Two details cost time when they are discovered late:

- RAPID writes numbers with a dot as decimal separator. Parse with `CultureInfo.InvariantCulture`, otherwise a French or German machine reads `1.5` as `15`.
- A `string` carries its RAPID quotes. Trim them.

## Write a value

Writing needs the RAPID mastership. Take it, write, give it back in a `finally` block.

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

A value the controller refuses, a text where a number is expected for example, fails with the HTTP status code 400. A write attempted without the mastership fails with 403.

`SetSymbolValue` changes the value the program uses now. `SetSymbolInitialValue` changes the value written in the declaration, which is what the variable goes back to when the module is reloaded.

## Check a value before writing it

`ValidateSymbolValue` asks the controller whether it would accept a text for a given RAPID type, without writing anything. It answers `false` instead of throwing, so it fits well after a user input.

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

## Arrays and records

An array and a record are both one value, written between brackets. An array of three `num` is `[1,2,3]`. A `robtarget` is `[trans, rot, robconf, extax]`, where the first two fields are records themselves. There is no partial write: you read the whole value, change what you need, and write the whole value back.

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

## Parse a record into an object

The SDK gives the text as the controller wrote it and does not take it apart, because a record can be any type you declared. Splitting the top level of a bracketed value is enough to read an array, a `robtarget`, or your own record.

```csharp
using System.Globalization;
using System.Text;
using UnderAutomation.ABB;
using UnderAutomation.ABB.Common;

public class HowToRapidArraysAndRecords
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // An array of num arrives as one bracketed text : [1,2.5,3]
        string arrayText = robot.Rws.Rapid.GetSymbolValue("RAPID/T_ROB1/MainModule/myArray").Value;
        string[] items = SplitRapidValue(arrayText);

        double[] numbers = new double[items.Length];
        for (int i = 0; i < items.Length; i++)
            numbers[i] = double.Parse(items[i], CultureInfo.InvariantCulture);

        // Writing takes the same text back. The whole array is written at once.
        robot.Rws.Rapid.SetSymbolValue("RAPID/T_ROB1/MainModule/myArray", "[1,2.5,3]");

        // A record is bracketed too, and its fields can be records themselves.
        // A robtarget is [trans, rot, robconf, extax].
        string targetText = robot.Rws.Rapid.GetSymbolValue("RAPID/T_ROB1/MainModule/pHome").Value;
        string[] fields = SplitRapidValue(targetText);

        string[] trans = SplitRapidValue(fields[0]);   // [515,0,712]
        string[] rot = SplitRapidValue(fields[1]);     // [0.707107,0,0.707107,0]

        RobTarget home = new RobTarget();
        home.X = double.Parse(trans[0], CultureInfo.InvariantCulture);
        home.Y = double.Parse(trans[1], CultureInfo.InvariantCulture);
        home.Z = double.Parse(trans[2], CultureInfo.InvariantCulture);
        home.Orientation = new Quaternion(double.Parse(rot[0], CultureInfo.InvariantCulture),
                                          double.Parse(rot[1], CultureInfo.InvariantCulture),
                                          double.Parse(rot[2], CultureInfo.InvariantCulture),
                                          double.Parse(rot[3], CultureInfo.InvariantCulture));

        Console.WriteLine($"pHome is at X={home.X} Y={home.Y} Z={home.Z}");

        // Writing the record back : move it 10 mm up and rebuild the text.
        // The two last fields are kept as they were read.
        home.Z += 10;
        string newValue = "[" + FormatTrans(home) + "," + FormatRot(home) + "," + fields[2] + "," + fields[3] + "]";

        // Ask the controller whether it accepts the text before writing it
        if (robot.Rws.Rapid.ValidateSymbolValue("T_ROB1", "robtarget", newValue))
            robot.Rws.Rapid.SetSymbolValue("RAPID/T_ROB1/MainModule/pHome", newValue);

        robot.Disconnect();
    }

    // Splits the top level of a RAPID value : "[[1,2],3]" gives "[1,2]" and "3".
    // A value that is not bracketed is returned as a single element.
    static string[] SplitRapidValue(string value)
    {
        string text = value == null ? "" : value.Trim();

        if (!text.StartsWith("[") || !text.EndsWith("]"))
            return new string[] { text };

        text = text.Substring(1, text.Length - 2);

        List<string> parts = new List<string>();
        StringBuilder current = new StringBuilder();
        int depth = 0;
        bool inString = false;

        foreach (char c in text)
        {
            if (c == '"') inString = !inString;

            if (!inString && c == '[') depth++;
            if (!inString && c == ']') depth--;

            if (!inString && c == ',' && depth == 0)
            {
                parts.Add(current.ToString().Trim());
                current.Length = 0;
            }
            else
            {
                current.Append(c);
            }
        }

        if (current.Length > 0)
            parts.Add(current.ToString().Trim());

        return parts.ToArray();
    }

    // RAPID always writes numbers with a dot, so does the invariant culture
    static string Number(double value)
    {
        return value.ToString(CultureInfo.InvariantCulture);
    }

    static string FormatTrans(RobTarget target)
    {
        return "[" + Number(target.X) + "," + Number(target.Y) + "," + Number(target.Z) + "]";
    }

    static string FormatRot(RobTarget target)
    {
        Quaternion q = target.Orientation;
        return "[" + Number(q.Q1) + "," + Number(q.Q2) + "," + Number(q.Q3) + "," + Number(q.Q4) + "]";
    }
}
```

To read the current position of the robot as a `RobTarget` object rather than as text, use the motion system instead. See [Get the robot position](get-robot-position.md).

## Find the variables of a program

You do not always know the module a variable is declared in. `SearchSymbols` walks the loaded program and returns the symbols matching a criteria: a name pattern, a data type, a kind of symbol, one block or the whole task.

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

## Reading many values

There is no batch read, one variable is one request. A loop over 200 variables is 200 requests, which is slow on a controller that also has a program to run. When a lot of data has to be published, group it in one RAPID record or one array and read that in a single call.

## Going further

- [RAPID variables & symbols](rws-rapid-symbols.md), the complete reference of the symbol methods
- [Mastership](rws-mastership.md), when and how to take the write lock
- [Start & stop a RAPID program](start-stop-rapid-program.md)
- [RAPID modules & program files](rws-rapid-modules.md), to load a module that declares your variables

**Methods of RapidService** ([reference](../api/UnderAutomation.ABB.Rws.Services.md#rapidservice-robotrwsrapid))

- `RapidModuleSymbol GetModuleSymbol(string task, string module, int row, int column)`: Gets the declaration the controller finds at a position of a module (synchronous)
  - async: `Task<RapidModuleSymbol> GetModuleSymbolAsync(string task, string module, int row, int column, CancellationToken cancellationToken = default)`
- `RapidSymbolProperties GetSymbolProperties(string symbolUrl)`: Gets what a RAPID symbol is declared as (synchronous)
  - async: `Task<RapidSymbolProperties> GetSymbolPropertiesAsync(string symbolUrl, CancellationToken cancellationToken = default)`
- `RapidSymbolValue GetSymbolValue(string symbolUrl)`: Gets the value of a RAPID symbol and where it is declared (synchronous)
  - async: `Task<RapidSymbolValue> GetSymbolValueAsync(string symbolUrl, CancellationToken cancellationToken = default)`
- `RapidSymbolProperties[] SearchSymbols(RapidSymbolSearchCriteria criteria)`: Finds the RAPID symbols matching a set of criteria (synchronous)
  - async: `Task<RapidSymbolProperties[]> SearchSymbolsAsync(RapidSymbolSearchCriteria criteria, CancellationToken cancellationToken = default)`
- `void SetSymbolInitialValue(string symbolUrl, string value)`: Sets the value a RAPID symbol is declared with, which is the one it goes back to when the program is reset (synchronous)
  - async: `Task SetSymbolInitialValueAsync(string symbolUrl, string value, CancellationToken cancellationToken = default)`
- `void SetSymbolValue(string symbolUrl, string value)`: Sets the value a RAPID symbol currently holds (synchronous)
  - async: `Task SetSymbolValueAsync(string symbolUrl, string value, CancellationToken cancellationToken = default)`
- `bool ValidateSymbolValue(string task, string dataType, string value)`: Asks the controller whether a value would be accepted for a given RAPID type, without writing it anywhere (synchronous) This is what an editor uses to tell an operator that what they typed is wrong before the write is attempted.
  - async: `Task<bool> ValidateSymbolValueAsync(string task, string dataType, string value, CancellationToken cancellationToken = default)`

**RapidSymbolValue** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidsymbolvalue))

- `RapidSymbolValue()`: Initializes a new instance of the Data.RapidSymbolValue class
- `RapidTextRange DeclarationPosition { get; set; }`: Where the symbol is declared, null when the controller did not report it
- `RapidTextRange InitialValuePosition { get; set; }`: Where the initial value of the symbol is written, null when the controller did not report it. The controller reports zeros when the declaration carries no initial value.
- `string Value { get; set; }`: Value of the symbol, written the way RAPID writes it

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
