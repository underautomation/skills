# Alarms & task status

Read active alarms, alarm history, clear alarms, monitor running tasks, and read/write comments via SNPX.

Web page: https://underautomation.com/fanuc/documentation/snpx-alarms-tasks

SNPX lets you read active alarms, browse alarm history, clear alarms, monitor running tasks, and read/write register and I/O comments.

## Alarms

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Snpx.Internal;
using UnderAutomation.Fanuc.Snpx;

public class SnpxAlarmsTasksAlarms
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        var parameters = new ConnectionParameters("192.168.0.1");
        parameters.Snpx.Enable = true;
        robot.Connect(parameters);

        // Active alarm
        RobotAlarm activeAlarm = robot.Snpx.ActiveAlarm.Read(1);
        Console.WriteLine($"Alarm: {activeAlarm.Message}");
        Console.WriteLine($"Severity: {activeAlarm.Severity}");
        Console.WriteLine($"Time: {activeAlarm.Time}");

        // Alarm history
        RobotAlarm histAlarm = robot.Snpx.AlarmHistory.Read(10);

        // Clear alarms
        robot.Snpx.ClearAlarms();
    }
}
```

## Task status and comments

Monitor running program tasks by index (1-based). Comments are short descriptions associated with registers or I/O ports.

Available comment types: `Register`, `PositionRegister`, `StringRegister`, `DI`, `DO`, `RI`, `RO`, `UI`, `UO`, `SI`, `SO`, `WI`, `WO`, `WSI`, `WSO`, `GI`, `GO`, `AI`, `AO`, `Flag`.

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Snpx.Internal;
using UnderAutomation.Fanuc.Snpx;

public class SnpxAlarmsTasksStatus
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        var parameters = new ConnectionParameters("192.168.0.1");
        parameters.Snpx.Enable = true;
        robot.Connect(parameters);

        // Task status
        RobotTaskStatus task = robot.Snpx.CurrentTaskStatus.Read(1);
        Console.WriteLine($"Program: {task.ProgramName}");
        Console.WriteLine($"Line: {task.LineNumber}");
        Console.WriteLine($"State: {task.State}");       // Stopped, Paused, Running
        Console.WriteLine($"Caller: {task.Caller}");

        // Read and write comments
        string comment = robot.Snpx.Comments.Read(CommentType.Register, 5);
        string longComment = robot.Snpx.Comments.Read(CommentType.Register, 5, 24);
        robot.Snpx.Comments.Write(CommentType.PositionRegister, 1, "Home Position", 16);
    }
}
```

## Complete example

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Snpx.Internal;
using UnderAutomation.Fanuc.Snpx;

public class SnpxAlarmsTasks
{
  public static void Main()
  {
    FanucRobot robot = new FanucRobot();

    ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");
    parameters.Snpx.Enable = true;

    robot.Connect(parameters);

    // --- Active alarm ---
    RobotAlarm activeAlarm = robot.Snpx.ActiveAlarm.Read(1);
    Console.WriteLine($"Alarm: {activeAlarm.Message}");
    Console.WriteLine($"Severity: {activeAlarm.Severity}");
    Console.WriteLine($"Time: {activeAlarm.Time}");

    // --- Alarm history ---
    RobotAlarm histAlarm = robot.Snpx.AlarmHistory.Read(10);
    Console.WriteLine($"History #{10}: {histAlarm.Message}");

    // --- Clear alarms ---
    robot.Snpx.ClearAlarms();

    // --- Task status ---
    RobotTaskStatus task = robot.Snpx.CurrentTaskStatus.Read(1);
    Console.WriteLine($"Program: {task.ProgramName}");
    Console.WriteLine($"Line: {task.LineNumber}");
    Console.WriteLine($"State: {task.State}");
    Console.WriteLine($"Caller: {task.Caller}");

    // --- Read and write comments ---
    string comment = robot.Snpx.Comments.Read(CommentType.Register, 5);
    robot.Snpx.Comments.Write(CommentType.PositionRegister, 1, "Home Position", 16);
  }
}
```

## API reference

**RobotAlarm** ([reference](../api/UnderAutomation.Fanuc.Snpx.Internal.md#robotalarm))

- `RobotAlarm()`
- `AlarmId CauseId { get; set; }`: Cause Category
- `string CauseMessage { get; set; }`: Cause message
- `short CauseNumber { get; set; }`: Cause Number
- `static RobotAlarm FromBytes(byte[] bytes, Languages language, int start = 0)`: Creates a Internal.RobotAlarm from a byte array.
- `AlarmId Id { get; set; }`: Alarm Category
- `string Message { get; set; }`: Error Message
- `short Number { get; set; }`: Alarm Number
- `AlarmSeverity Severity { get; set; }`: Alarm Severity
- `string SeverityMessage { get; set; }`: Severity message
- `DateTime Time { get; set; }`: Occurrence Time

**AlarmSeverity** ([reference](../api/UnderAutomation.Fanuc.Snpx.Internal.md#alarmseverity))

- ABORT_G: Global abort level alarm.
- ABORT_L: Local abort level alarm.
- NONE: No severity.
- PAUSE_G: Global pause level alarm.
- PAUSE_L: Local pause level alarm.
- SERVO: Servo error alarm.
- SERVO2: Servo error level 2 alarm.
- STOP_G: Global stop level alarm.
- STOP_L: Local stop level alarm.
- SYSTEM: System level alarm.
- WARN: Warning level alarm.

**RobotTaskStatus** ([reference](../api/UnderAutomation.Fanuc.Snpx.Internal.md#robottaskstatus))

- `RobotTaskStatus()`
- `string Caller { get; set; }`: Gets or sets the name of the calling program.
- `static RobotTaskStatus FromBytes(byte[] bytes, Languages language, int start = 0)`: Creates a Internal.RobotTaskStatus from a byte array.
- `short LineNumber { get; set; }`: Gets or sets the current line number in the program.
- `string ProgramName { get; set; }`: Gets or sets the name of the program being executed.
- `RobotTaskState State { get; set; }`: Gets or sets the current execution state of the task.

**RobotTaskState** ([reference](../api/UnderAutomation.Fanuc.Snpx.Internal.md#robottaskstate))

- Paused: Task is paused.
- Running: Task is running.
- Stopped: Task is stopped.

**CommentType** ([reference](../api/UnderAutomation.Fanuc.Snpx.Internal.md#commenttype))

- AI: Analog Input.
- AO: Analog Output.
- DI: Digital Input.
- DO: Digital Output.
- Flag: Flag
- GI: Group Input.
- GO: Group Output.
- PositionRegister: Position register PR[].
- RI: Remote Input.
- RO: Remote Output.
- Register: Numeric register R[].
- SI: System Input.
- SO: System Output.
- StringRegister: String register SR[].
- UI: User Input.
- UO: User Output.
- WI: Weld Input.
- WO: Weld Output.
- WSI: Wire Stick Input.
- WSO: Wire Stick Output.
