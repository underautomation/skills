# Alarms

Read up to 4 alarms of a Yaskawa controller with their code, text and time, read the sub codes, then reset the alarms or cancel an error.

Web page: https://underautomation.com/yaskawa/documentation/hses-alarms

This page shows how to read the alarms of a Yaskawa Motoman controller with the SDK, and how to reset them from a PC. It covers every controller with the High Speed Ethernet Server.

## Read the alarms

The controller reports up to 4 alarms. `GetAlarm(which)` reads one of them, with its code, its text and the time it occurred.

```csharp
using UnderAutomation.Yaskawa;
using UnderAutomation.Yaskawa.HighSpeedEServer;

public class AlarmRead
{
    static void Main()
    {
        var robot = new YaskawaRobot();
        robot.Connect("192.168.0.1");

        // The controller reports up to 4 alarms, the most recent first
        foreach (RobotRecentAlarm which in Enum.GetValues(typeof(RobotRecentAlarm)))
        {
            RobotAlarmData alarm = robot.HighSpeedEServer.GetAlarm(which);

            // Code 0 means that there is no alarm at this position
            if (alarm.Code == 0) continue;

            Console.WriteLine($"{which}: {alarm.Code} {alarm.Text} at {alarm.OccurringTime} (data {alarm.Data}, type {alarm.Type})");
        }

        robot.Disconnect();
    }
}
```

| Property        | Content                                                           |
| --------------- | ----------------------------------------------------------------- |
| `Code`          | Alarm number, as shown on the pendant. `0` when there is no alarm |
| `Data`          | Sub code of the alarm                                             |
| `Type`          | Type of the sub code                                              |
| `OccurringTime` | Date and time of the alarm, as a text of the controller           |
| `Text`          | Name of the alarm                                                 |

`RobotRecentAlarm.Latest` is the most recent alarm, `FourthLatest` the oldest of the four. `GetStatusInformation().Alarming` tells if an alarm is active, in one short request: test it first, then read the alarms.

The meaning of each code and the action to take are in the alarm manual of your controller.

## Read the sub codes

`GetAlarmExtended(which)` returns the same values, plus the texts of the sub codes. Use it to log the full context of an alarm.

```csharp
using UnderAutomation.Yaskawa;
using UnderAutomation.Yaskawa.HighSpeedEServer;

public class AlarmReadExtended
{
    static void Main()
    {
        var robot = new YaskawaRobot();
        robot.Connect("192.168.0.1");

        // Same as GetAlarm, plus the sub code texts of the alarm
        RobotAlarmDataExtended alarm = robot.HighSpeedEServer.GetAlarmExtended(RobotRecentAlarm.Latest);

        Console.WriteLine($"{alarm.Code} {alarm.Text} at {alarm.OccurringTime}");
        Console.WriteLine($"Information: {alarm.AdditionnalInformation}");
        Console.WriteLine($"Sub data: {alarm.SubData}");

        robot.Disconnect();
    }
}
```

## Reset an alarm

`AlarmReset(type)` resets the alarms or cancels an error. It needs the remote mode. Remove the cause first: an alarm whose cause is still present comes back.

```csharp
using UnderAutomation.Yaskawa;
using UnderAutomation.Yaskawa.HighSpeedEServer;

public class AlarmReset
{
    static void Main()
    {
        var robot = new YaskawaRobot();
        robot.Connect("192.168.0.1");

        RobotStatusData status = robot.HighSpeedEServer.GetStatusInformation();

        // Reset the alarms, once their cause is removed
        if (status.Alarming)
            robot.HighSpeedEServer.AlarmReset(AlarmResetType.Reset);

        // Cancel an error (a message that does not stop the controller)
        if (status.ErrorOccurring)
            robot.HighSpeedEServer.AlarmReset(AlarmResetType.Cancel);

        robot.Disconnect();
    }
}
```

| `AlarmResetType` | Use                                                               |
| ---------------- | ----------------------------------------------------------------- |
| `Reset`          | Reset the alarms (`GetStatusInformation().Alarming`)              |
| `Cancel`         | Cancel an error message (`GetStatusInformation().ErrorOccurring`) |

A complete program, with the check after the reset, is in [Read and reset alarms](how-to-read-reset-alarms.md).

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**Methods of HighSpeedEServerClientBase** ([reference](../api/UnderAutomation.Yaskawa.HighSpeedEServer.Internal.md#highspeedeserverclientbase-robothighspeedeserver))

- `RobotDataHeader AlarmReset(AlarmResetType type)`: Resets alarms or cancels errors on the robot controller. Use Reset to clear alarm conditions after resolving the cause. Use Cancel for recoverable errors that don't require alarm reset.
- `RobotAlarmData GetAlarm(RobotRecentAlarm alarm)`: Reads alarm information from the robot controller. Retrieves alarm code, type, occurrence time, and descriptive text.
- `RobotAlarmDataExtended GetAlarmExtended(RobotRecentAlarm alarm)`: Retrieves extended alarm information including sub-code character strings. Provides more detailed information than GetAlarm for troubleshooting.

**RobotAlarmData** ([reference](../api/UnderAutomation.Yaskawa.HighSpeedEServer.md#robotalarmdata))

- `int Code { get; }`: Gets the alarm code identifying the specific alarm type. Alarm codes are documented in the robot's maintenance manual.
- `int Data { get; }`: Gets additional alarm data providing context about the alarm. The meaning depends on the specific alarm code.
- `string OccurringTime { get; }`: Gets the timestamp when the alarm occurred. Format: "YYYY/MM/DD HH:MM:SS" (16 characters).
- `string Text { get; }`: Gets the alarm message text describing the alarm condition. Maximum 32 characters.
- `int Type { get; }`: Gets the alarm type/category classification.

**RobotAlarmDataExtended** ([reference](../api/UnderAutomation.Yaskawa.HighSpeedEServer.md#robotalarmdataextended))

- `string AdditionnalInformation { get; }`: Gets additional information about the alarm condition. Maximum 16 characters.
- `string SubData { get; }`: Gets the sub-code data providing detailed error context. Maximum 96 characters.
- `string SubDataReverse { get; }`: Gets the reversed sub-code data. Maximum 96 characters.
- Inherited from [RobotAlarmData](../api/UnderAutomation.Yaskawa.HighSpeedEServer.md#robotalarmdata): `Code`, `Data`, `Type`, `OccurringTime`, `Text`

**RobotRecentAlarm** ([reference](../api/UnderAutomation.Yaskawa.HighSpeedEServer.md#robotrecentalarm))

- FourthLatest: The fourth most recent alarm.
- Latest: The most recent (current) alarm.
- SecondLatest: The second most recent alarm.
- ThirdLatest: The third most recent alarm.

**AlarmResetType** ([reference](../api/UnderAutomation.Yaskawa.HighSpeedEServer.md#alarmresettype))

- Cancel: Cancel the current error. Used for recoverable errors.
- Reset: Reset the current alarm. Requires the alarm condition to be resolved.
