# Troubleshooting & best practices

Handle Stream Motion errors, understand the usual MOTN alarms, and follow the good practices for smooth and reliable motions.

Web page: https://underautomation.com/fanuc/documentation/stream-motion-troubleshooting

When the robot receives a position it cannot follow, it stops immediately with an alarm and the TP program leaves `IBGN start`. This page lists the usual causes and the good practices to avoid them.

## Handle errors in your application

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common;
using UnderAutomation.Fanuc.Motion;
using UnderAutomation.Fanuc.StreamMotion;
using UnderAutomation.Fanuc.StreamMotion.Data;

public class StreamMotionTroubleshootingErrors
{
    static void Main()
    {
        var robot = new FanucRobot();
        var parameters = new ConnectionParameters("192.168.0.1");
        parameters.StreamMotion.Enable = true;
        robot.Connect(parameters);
        var sm = robot.StreamMotion;

        // Errors of the communication thread
        sm.ErrorOccurred += (sender, e) => Console.WriteLine($"Error: {e.Exception.Message}");

        // No more positions while the robot was moving: it was stopped smoothly
        sm.Underrun += (sender, e) => Console.WriteLine($"Underrun after motion {e.MotionId}");

        // A session ended by an alarm on the robot
        sm.SessionEnded += (sender, e) =>
        {
            if (e.Reason == SessionEndReason.ProgramStopped)
                Console.WriteLine("The TP program stopped: check the alarms of the robot");
        };

        try
        {
            sm.StartMonitoring();
        }
        catch (StreamMotionException ex)
        {
            // For example NoStatus: wrong IP address, $STMO.$PHYS_PORT, or protocol version too high
            Console.WriteLine($"{ex.Error}: {ex.Message}");
        }

        robot.Disconnect();
    }
}
```

- `ErrorOccurred` reports the errors of the communication thread, for example a lost connection or a callback that failed.
- `Underrun` is raised when the robot was moving and no more positions were available: the client stopped it smoothly.
- `SessionEnded` with the reason `ProgramStopped` means that the program left `IBGN start`, often because of an alarm. Read the active alarms with [CGTP or SNPX](how-to-reset-fanuc-alarm-remotely.md).
- `StreamMotionException.Error` tells the kind of error thrown by a method (`NoStatus`, `VersionMismatch`, `StartMismatch`, `SourceBusy`...).

## Common alarms

The number of an alarm can change with the software version of the controller.

| Alarm | Cause | Solution |
| --- | --- | --- |
| Joint velocity, acceleration or jerk limit exceeded | The positions are too fast for the robot | Plan the motion with the [motion planner](motion.md), or check your positions with `Check()` before sending them |
| MOTN-603 Receiving interval over | Positions arrived too late: the PC was busy or the network was slow | Increase `BufferLeadTime`, keep `HighPriority`, use a wired network with little traffic |
| MOTN-607 | Protocol version not supported by the controller | Set `ProtocolVersion` to `$STMO.$USABLE_VER` or lower |
| MOTN-615 | Servo off is enabled for the group | Set `$PARAM_GROUP[1].$SV_OFF_ENB[*]` to `FALSE` |
| MOTN-623 | Resume offset is enabled | Disable the resume offset |
| MOTN-625 Abnormal position | The first position is far from the position of the robot | Start each trajectory at `QueueEndJointPosition` or `QueueEndCartesianPosition` |
| MOTN-018 Position not reachable | Cartesian position in another frame than the one expected by the robot | Some controllers expect the position of the active tool: select a tool frame equal to zero, or use joint positions |
| PRIO-023 | An I/O that is not assigned was written | Check the type and the index of the I/O |

## Good practices

- **Plan within the limits.** Use the motion planner, which respects the velocity, acceleration and jerk of each axis. For positions computed by your application, call `Check()` with the communication cycle of the robot.
- **Keep a small margin with protocol version 1.** Positions are sent in single precision: the rounding adds a little noise to the jerk. Use about 99% of the limits, or protocol version 2 for joint motions.
- **Prefer joint positions for large changes of orientation**, especially at 2 ms. Cartesian positions are always sent in single precision.
- **Choose prudent Cartesian limits.** The SDK cannot check the joint limits of a Cartesian motion: the same Cartesian speed can be fine in one pose and too fast for the wrist in another one. Validate them on the robot or in ROBOGUIDE.
- **Read the limits before running the TP program.** Some controllers do not answer while a program waits on `IBGN start`.
- **Start from the right position.** Always build a trajectory from `QueueEndJointPosition` or `QueueEndCartesianPosition`.
- **Use a dedicated wired network.** Stream Motion sends one packet every cycle (up to 500 per second). Avoid Wi-Fi and heavy traffic on the same port.
- **Finish the session.** Call `Finish()` so that the program continues after `IBGN end`. `Disconnect()` also stops the robot smoothly and finishes the session.
- **Test in ROBOGUIDE first.** Stream Motion works with the virtual controllers of ROBOGUIDE when the J519 option is loaded.

## Check the quality of the communication

`Statistics` gives the number of status received and lost, the positions sent, the underruns, and the time between two status. A high `MaxStatusInterval` or many lost status show a PC or network problem.
