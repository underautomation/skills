# Reset alarms remotely

Clear and reset alarms on a Fanuc robot using SNPX, Telnet, or CGTP. Read active alarms and alarm history.

Web page: https://underautomation.com/fanuc/documentation/how-to-reset-fanuc-alarm-remotely

Clear fault conditions and reset alarms on your Fanuc robot remotely using different protocols.

## SNPX

SNPX can clear alarms, read the active alarm, and browse alarm history:

```csharp
using System;
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Snpx.Internal;
using UnderAutomation.Fanuc.Common;

public class HowToResetFanucAlarmRemotelySnpx
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        robot.Connect("192.168.0.1");

        // Clear all alarms (equivalent to pressing FAULT RESET)
        robot.Snpx.ClearAlarms();

        // Read the active alarm
        RobotAlarm activeAlarm = robot.Snpx.ActiveAlarm.Read(1);
        Console.WriteLine($"Alarm: {activeAlarm.Message} (Severity: {activeAlarm.Severity})");

        // Read alarm history
        RobotAlarm histAlarm = robot.Snpx.AlarmHistory.Read(10);
    }
}
```

See also: [SNPX Alarms & task status](snpx-alarms-tasks.md)

## Telnet KCL

Telnet can reset alarms using KCL commands:

```csharp
using UnderAutomation.Fanuc;

public class HowToResetFanucAlarmRemotelyTelnet
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        robot.Connect("192.168.0.1");

        // Reset the robot (clears faults, exits HOLD)
        robot.Telnet.Reset();

        // Or use a custom KCL command
        robot.Telnet.SendCustomCommand("RESET");
    }
}
```

See also: [Telnet Program control](telnet-program-control.md)

## CGTP Web Server

CGTP can check alarm-related variables:

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Cgtp;
using UnderAutomation.Fanuc.Common;
using UnderAutomation.Fanuc.Common.Files.List;

public class HowToResetFanucAlarmRemotelyCgtp
{
  static void Main()
  {
    FanucRobot robot = new FanucRobot();
    robot.Connect("192.168.0.1");

    // Read alarm history
    ErrorList errors = robot.Cgtp.Http.GetAllErrorsList();

    // extract active alarms from the full list
    var activeAlarms = errors.FilterActiveAlarms();

    // reset alarms
    robot.Cgtp.Kcl.Reset();

    // Read user alarms definitions
    UserAlarmDefinition[] alarms = robot.Cgtp.ReadUserAlarms();

    // write user alarm definition
    robot.Cgtp.SetUserAlarmSeverity(1, 8); // Set user alarm #1 to severity 8 
    robot.Cgtp.SetComment(CgtpCommentType.UserAlarm, 1, "Overheat alarm"); // Set comment for user alarm #1
  }
}
```

See also: [CGTP Alarms, comments & files](cgtp-alarms-files.md)

## FTP (offline)

Download and parse the error log:

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common;
using UnderAutomation.Fanuc.Common.Files.List;

public class HowToResetFanucAlarmRemotelyFtp
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        robot.Connect("192.168.0.1");

        // Read alarm history via FTP 
        ErrorList errors = robot.Ftp.GetAllErrorsList();

        // extract active alarms from the full list
        errors.FilterActiveAlarms();
    }
}
```

## Protocol comparison

| Feature | SNPX | Telnet | CGTP | FTP |
|---------|------|--------|------|-----|
| **Clear alarms** | Yes | Yes | Yes | No |
| **Read active alarm** | Yes | No | Yes | Yes |
| **Alarm history** | Yes | No | Yes | Yes |
| **User alarms** | No | No | Yes | No |
