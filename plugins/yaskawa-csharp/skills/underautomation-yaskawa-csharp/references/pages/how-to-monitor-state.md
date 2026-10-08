# Monitor the state of the robot

Poll the mode, the servo, the hold, the alarms and the job of a Yaskawa controller, and print each change of state.

Web page: https://underautomation.com/yaskawa/documentation/how-to-monitor-state

This article shows how to follow the state of a Yaskawa Motoman controller from a PC, in C# or Python. It gives a complete program that reads the mode, the servo, the hold, the alarm and the job every 200 ms, and prints each change.

## Prerequisites

- The SDK is connected to the controller: see [Connect to your robot](connect.md).
- Nothing else: all these reads work in any mode.

## What to read

| Information                        | Method                              |
| ---------------------------------- | ----------------------------------- |
| Mode, servo, running, hold, alarm  | `GetStatusInformation()`            |
| Name and line of the executing job | `GetExecutingJobInformation()`      |
| Code and text of the alarm         | `GetAlarm(RobotRecentAlarm.Latest)` |
| Position of the robot              | `GetRobotCartesianPosition()`       |
| Variables written by the job       | `ReadInteger`, `ReadByte`...        |

The SDK has no event: it reads when you call it. A monitor is a loop that reads, compares with the last value, and reacts to the changes.

## Example

```csharp
using UnderAutomation.Yaskawa;
using UnderAutomation.Yaskawa.HighSpeedEServer;

public class HowToMonitorState
{
    static void Main()
    {
        var robot = new YaskawaRobot();
        robot.Connect("192.168.0.1");

        string last = null;

        // Poll every 200 ms for 1 minute and print each change
        for (int i = 0; i < 300; i++)
        {
            RobotStatusData status = robot.HighSpeedEServer.GetStatusInformation();
            RobotJobData job = robot.HighSpeedEServer.GetExecutingJobInformation();

            string mode = status.Play ? "PLAY" : status.Teach ? "TEACH" : "?";
            string state = $"{mode} servo={(status.ServoOn ? "on" : "off")} running={status.Running} " +
                           $"hold={status.InHoldStatusPendant || status.InHoldStatusExternally || status.InHoldStatusByCommand} " +
                           $"alarm={status.Alarming} job={job.Name}";

            if (state != last)
            {
                Console.WriteLine($"{DateTime.Now:HH:mm:ss} {state}");

                if (status.Alarming)
                {
                    RobotAlarmData alarm = robot.HighSpeedEServer.GetAlarm(RobotRecentAlarm.Latest);
                    Console.WriteLine($"  alarm {alarm.Code}: {alarm.Text}");
                }

                last = state;
            }

            Thread.Sleep(200);
        }

        robot.Disconnect();
    }
}
```

The program builds a line of text from the status and the job, and prints it only when it changes. When an alarm is active, it also prints the latest alarm.

## Polling period

Each read is one request. Two reads every 200 ms is 10 requests per second. Choose the period from what you need to see: 100 ms to 500 ms for a supervision screen, a few seconds for a log.

Run the loop in its own thread, so that the user interface stays responsive. One `YaskawaRobot` can be used by several threads: the SDK sends one request at a time.

## With the Ethernet Server

The same loop works with the [Ethernet Server](ethernet-server.md): `GetStatusInformation()` has the same flags. A call takes about 20 ms on a YRC1000micro, against 10 ms with the High Speed Ethernet Server: keep a polling period of 100 ms or more. To write the loop once for both protocols, use the common interfaces, see [Choose a protocol](protocols.md#write_code_for_both_protocols).

The Ethernet Server also reads the temperature of the encoders and the maximum torque of each axis, to follow the robot over a shift.

```csharp
using UnderAutomation.Yaskawa;
using UnderAutomation.Yaskawa.HostControl;

public class EServerTorque
{
    static void Main()
    {
        var parameters = new ConnectParameters("192.168.0.1");
        parameters.EServer.Enable = true;
        var robot = new YaskawaRobot();
        robot.Connect(parameters);

        // Torque of each axis, in percent of the rated torque
        HostControlTorqueData torque = robot.EServer.GetTorque();
        HostControlTorqueData maxTorque = robot.EServer.GetMaxTorque();

        // Temperature of the encoder of each axis, in degrees Celsius
        HostControlEncoderTemperatureData temperatures = robot.EServer.GetEncoderTemperature();

        for (int axis = 0; axis < 6; axis++)
            Console.WriteLine($"Axis {axis + 1}: {torque.Values[axis]} % (max {maxTorque.Values[axis]} %), {temperatures.Values[axis]} C");

        robot.Disconnect();
    }
}
```

## Troubleshooting

- **A `SocketException` from time to time:** a request did not get its answer before `DataTimeoutMilliseconds`. Catch it in the loop, count the failures, and report a lost connection after several failures in a row.
- **The job name is empty:** no job is selected.

## What to read next

- [Status and servo](hses-status.md): all the flags of the status.
- [Read and reset alarms](how-to-read-reset-alarms.md).
