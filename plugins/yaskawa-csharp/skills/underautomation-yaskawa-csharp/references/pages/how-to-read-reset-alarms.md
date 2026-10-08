# Read and reset alarms

Detect an alarm of a Yaskawa controller, read its code and text, reset it and check the result, from C# or Python.

Web page: https://underautomation.com/yaskawa/documentation/how-to-read-reset-alarms

This article shows how to detect an alarm of a Yaskawa Motoman controller from a PC, read its code and its text, and reset it, in C# or Python. It gives a complete program that checks the result of the reset.

## Prerequisites

- The SDK is connected to the controller: see [Connect to your robot](connect.md).
- To reset, the controller accepts the remote commands. Reading the alarms works in any mode.

## Alarm or error

| State                           | Detect                                  | Clear                               |
| ------------------------------- | --------------------------------------- | ----------------------------------- |
| Alarm: the controller stops     | `GetStatusInformation().Alarming`       | `AlarmReset(AlarmResetType.Reset)`  |
| Error: a message on the pendant | `GetStatusInformation().ErrorOccurring` | `AlarmReset(AlarmResetType.Cancel)` |

`GetAlarm` reads the code, the sub code, the time and the text of each alarm. `GetAlarmExtended` adds the texts of the sub codes.

## Example

```csharp
using UnderAutomation.Yaskawa;
using UnderAutomation.Yaskawa.HighSpeedEServer;

public class HowToReadResetAlarms
{
    static void Main()
    {
        var robot = new YaskawaRobot();
        robot.Connect("192.168.0.1");

        RobotStatusData status = robot.HighSpeedEServer.GetStatusInformation();

        if (status.Alarming || status.ErrorOccurring)
        {
            // 1. Read the alarms, the latest first
            foreach (RobotRecentAlarm which in Enum.GetValues(typeof(RobotRecentAlarm)))
            {
                RobotAlarmData alarm = robot.HighSpeedEServer.GetAlarm(which);
                if (alarm.Code != 0)
                    Console.WriteLine($"{alarm.OccurringTime} {alarm.Code} {alarm.Text}");
            }

            // 2. Remove the cause on the cell, then reset
            robot.HighSpeedEServer.AlarmReset(status.Alarming ? AlarmResetType.Reset : AlarmResetType.Cancel);

            // 3. Check that the alarm is gone
            status = robot.HighSpeedEServer.GetStatusInformation();
            Console.WriteLine(status.Alarming ? "The alarm is still active" : "Alarm reset");
        }

        robot.Disconnect();
    }
}
```

The program:

1. reads the status, and stops if there is no alarm and no error;
2. prints each alarm reported by the controller, the most recent first;
3. resets the alarm, or cancels the error;
4. reads the status again to check that the alarm is gone.

## Before the reset

A reset does not remove the cause of the alarm. If the cause is still present, the alarm comes back at once. Log the code and the text before the reset, and let an operator check the cell when the alarm concerns safety or a collision.

## With the Ethernet Server

The [Ethernet Server](ethernet-server.md) reads the error and the 4 alarms with their code, sub code and text in one call, `GetAlarmWithMessages()`. `AlarmReset()` resets the alarms and `ErrorCancel()` removes the error.

```csharp
using UnderAutomation.Yaskawa;
using UnderAutomation.Yaskawa.HostControl;

public class EServerAlarms
{
    static void Main()
    {
        var parameters = new ConnectParameters("192.168.0.1");
        parameters.EServer.Enable = true;
        var robot = new YaskawaRobot();
        robot.Connect(parameters);

        // Active error and alarms, with their text
        HostControlAlarmStringData alarms = robot.EServer.GetAlarmWithMessages();

        if (alarms.Error != null && alarms.Error.Code != 0)
            Console.WriteLine($"Error {alarms.Error.Code}: {alarms.Error.Message}");

        foreach (HostControlAlarmEntry alarm in alarms.Alarms)
        {
            if (alarm.Code != 0) // empty entries have the code 0
                Console.WriteLine($"Alarm {alarm.Code} ({alarm.SubCode}): {alarm.Message}");
        }

        // Reset the alarms, cancel the error (remote mode)
        if (alarms.AlarmCount > 0) robot.EServer.AlarmReset();
        robot.EServer.ErrorCancel();

        robot.Disconnect();
    }
}
```

## Troubleshooting

- **The reset is refused:** the remote mode is off. See [Prepare the controller](connect.md#prepare_the_controller).
- **The alarm comes back:** its cause is still present. Look for the code in the alarm manual of your controller.
- **`Code` is `0`:** there is no alarm at this position of the list.

## What to read next

- [Alarms](hses-alarms.md): the reference of the alarm methods.
- [Monitor the state of the robot](how-to-monitor-state.md).
