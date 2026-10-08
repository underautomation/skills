# Access Karel program variables

Read and write Karel program variables using SNPX ($[Program]Variable syntax), CGTP, or FTP variable files.

Web page: https://underautomation.com/fanuc/documentation/access-karel-program-variables

Read and write variables inside Karel programs running on your Fanuc robot.

## SNPX

SNPX accesses Karel variables using the `$[ProgramName]VariableName` naming convention:

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common;

public class AccessKarelProgramVariablesSnpx
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        robot.Connect("192.168.0.1");

        // Read a Karel integer variable
        int myVar = robot.Snpx.IntegerSystemVariables.Read("$[MyKarelProg]my_variable");

        // Write a Karel integer variable
        robot.Snpx.IntegerSystemVariables.Write("$[MyKarelProg]my_variable", 42);

        // Read a Karel real variable
        float realVar = robot.Snpx.RealSystemVariables.Read("$[MyKarelProg]speed_ratio");

        // Read a Karel position variable
        Position posVar = robot.Snpx.PositionSystemVariables.Read("$[MyKarelProg]target_pos");

        // Read a Karel string variable
        string strVar = robot.Snpx.StringSystemVariables.Read("$[MyKarelProg]status_msg");
    }
}
```

See also: [SNPX System variables](snpx-variables.md)

## CGTP Web Server

CGTP reads and writes Karel program variables using the `progName` parameter:

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Cgtp;

public class AccessKarelProgramVariablesCgtp
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        robot.Connect("192.168.0.1");

        // Read a Karel variable
        CgtpVariableValue var = robot.Cgtp.ReadVariable("my_variable", progName: "MyKarelProg");
        int intVal = var.IntegerValue;

        // Write a Karel variable
        robot.Cgtp.WriteVariable("my_variable", 42, progName: "MyKarelProg");

        // Read as string
        string raw = robot.Cgtp.ReadVariableAsString("speed_ratio", progName: "MyKarelProg");
    }
}
```

See also: [CGTP Registers & variables](cgtp-registers-variables.md)

## Telnet

Telnet allows you to read and write a karel program variable 

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common;

public class AccessKarelProgramVariablesFtp
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        robot.Connect("192.168.0.1");

        GetVariableResult result = robot.Telnet.GetVariable("VAR_NAME", "KarelProgramName");
    }
}
```


## Protocol comparison

| Feature | SNPX | CGTP | Telnet |
|---------|------|------|-----|
| **Speed** | ~2 ms | ~50 ms | ~100 ms |
| **Typed read** | Yes (4 types) | Yes (auto-detect) | Yes (file parse) |
| **Write** | Yes | Yes | No |
| **Batch read** | Yes | Yes | Yes (all at once) |
| **All variable types** | Integer, Real, Position, String | All | All |
