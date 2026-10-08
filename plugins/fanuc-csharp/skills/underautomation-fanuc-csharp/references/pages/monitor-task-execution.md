# Monitor task execution

Supervise running programs, check task states, line numbers, and calling programs using SNPX, FTP, or Telnet.

Web page: https://underautomation.com/fanuc/documentation/monitor-task-execution

Monitor running tasks, program names, line numbers, and execution state on your Fanuc robot.

## SNPX

SNPX provides direct task monitoring with program name, line number, state, and caller:

```csharp
using System;
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Snpx.Internal;
using UnderAutomation.Fanuc.Common;

public class MonitorTaskExecutionSnpx
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        robot.Connect("192.168.0.1");

        // Read task 1 status
        RobotTaskStatus task = robot.Snpx.CurrentTaskStatus.Read(1);
        Console.WriteLine($"Program: {task.ProgramName}");
        Console.WriteLine($"Line: {task.LineNumber}");
        Console.WriteLine($"State: {task.State}");       // Running, Paused, Stopped
        Console.WriteLine($"Caller: {task.Caller}");
    }
}
```

See also: [SNPX Alarms & task status](snpx-alarms-tasks.md)

## FTP (offline parsing)

Download and parse the task information file:

```csharp
using System;
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common;
using UnderAutomation.Fanuc.Common.Files.Diagnosis;

public class MonitorTaskExecutionFtp
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        robot.Connect("192.168.0.1");

        ProgramStates programStates = robot.Ftp.GetProgramStates();
        foreach (TaskState task in programStates.TaskStates)
        {
            Console.WriteLine($"Task {task.Name}: {task.Status}");
            foreach (TaskHistoryData call in task.History)
                Console.WriteLine($"  {call.ProgramName} - Line {call.LineNumber}");
        }
    }
}
```

See also: [FTP Diagnostics & variables](ftp-diagnostics.md)

## Telnet KCL

Query task information using KCL commands:

```csharp
using System;
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Telnet;

public class MonitorTaskExecutionTelnet
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        robot.Connect("192.168.0.1");

        // Get task information for a program like line number, state, and more
        TaskInformationResult result = robot.Telnet.GetTaskInformation("MY_PROGRAM");
    }
}
```

See also: [Telnet Debugging & breakpoints](telnet-debugging.md)

## Protocol comparison

| Feature | SNPX | FTP | Telnet |
|---------|------|-----|--------|
| **Speed** | ~2 ms | ~100 ms | ~30 ms |
| **Program name** | Yes | Yes | Yes |
| **Line number** | Yes | Yes | Yes |
| **Task state** | Yes | Yes | Yes |
| **Caller info** | Yes | No | No |
| **Multiple tasks** | Yes (by index) | Yes (all) | Yes (all) |
