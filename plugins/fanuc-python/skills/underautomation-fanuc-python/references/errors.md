# Errors of the Fanuc SDK (Python)

SDK version 7.1.0. The exceptions of the SDK, and the pages that describe when they are raised. The message of an exception says what failed: read it first, then the page of the feature.

The SDK raises the .NET exception. It is a Python exception: catch it with `except Exception as e` and read `str(e)`, or catch its .NET type, imported from its .NET namespace as shown below (the package loads the .NET library first).

Its members keep their .NET names: `e.Message`, `e.InnerException`. The classes of the same name in the `underautomation.fanuc` modules are not Python exceptions: `except` on one of them raises a `TypeError`. The reference of each exception lists its members.

## CgtpException

Represents an error returned by the FANUC controller via CGTP.

Catch: `from UnderAutomation.Fanuc.Cgtp import CgtpException`, then `except CgtpException as e`.

Reference: [underautomation.fanuc.cgtp](api/underautomation.fanuc.cgtp.md#cgtpexception)

Pages that describe it: [cgtp-programs](pages/cgtp-programs.md), [cgtp-kcl](pages/cgtp-kcl.md).

## ConnectException

Exception thrown when connection to the robot fails

Catch: `from UnderAutomation.Fanuc.Common import ConnectException`, then `except ConnectException as e`.

Reference: [underautomation.fanuc.common](api/underautomation.fanuc.common.md#connectexception)

Pages that describe it: [rmi](pages/rmi.md).

## FtpException

Exception thrown when the controller refuses an FTP operation, or when the FTP communication fails. The message gives the reply of the controller and, when it is known, what to do.

Catch: `from UnderAutomation.Fanuc.Ftp import FtpException`, then `except FtpException as e`.

Members (.NET names): `ProgramInUse`, `RemotePath`, `ReplyCode`, `ReplyMessage`, `Message`, `InnerException`.

Pages that describe it: [ftp](pages/ftp.md), [ftp-file-management](pages/ftp-file-management.md).

## InvalidLicenseException

Exception thrown while using the product if the license is not valid.

Catch: `from UnderAutomation.Fanuc.License import InvalidLicenseException`, then `except InvalidLicenseException as e`.

Reference: [underautomation.fanuc.license](api/underautomation.fanuc.license.md#invalidlicenseexception)

Pages that describe it: [get-started-python](pages/get-started-python.md), [license](pages/license.md).

## RmiException

Represents an error reported by the FANUC RMI controller or thrown by the client runtime.

Catch: `from UnderAutomation.Fanuc.Rmi import RmiException`, then `except RmiException as e`.

Reference: [underautomation.fanuc.rmi](api/underautomation.fanuc.rmi.md#rmiexception)

Pages that describe it: [rmi](pages/rmi.md).

## StreamMotionException

Error raised by the Stream Motion client

Catch: `from UnderAutomation.Fanuc.StreamMotion import StreamMotionException`, then `except StreamMotionException as e`.

Reference: [underautomation.fanuc.stream_motion](api/underautomation.fanuc.stream_motion.md#streammotionexception)

Pages that describe it: [stream-motion](pages/stream-motion.md), [stream-motion-session](pages/stream-motion-session.md), [stream-motion-troubleshooting](pages/stream-motion-troubleshooting.md).

## Troubleshooting: stream-motion-troubleshooting

When the robot receives a position it cannot follow, it stops immediately with an alarm and the TP program leaves `IBGN start`. This page lists the usual causes and the good practices to avoid them.

### Handle errors in your application

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters
from underautomation.fanuc.stream_motion.data.session_end_reason import SessionEndReason

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.stream_motion.enable = True
robot.connect(parameters)
sm = robot.stream_motion

## Errors of the communication thread
def on_error(sender, e):
    print(f"Error: {e.exception}")

## No more positions while the robot was moving: it was stopped smoothly
def on_underrun(sender, e):
    print(f"Underrun after motion {e.motion_id}")

## A session ended by an alarm on the robot
def on_session_ended(sender, e):
    if e.reason == SessionEndReason.ProgramStopped:
        print("The TP program stopped: check the alarms of the robot")

sm.error_occurred(on_error)
sm.underrun(on_underrun)
sm.session_ended(on_session_ended)

try:
    sm.start_monitoring()
except Exception as ex:
    # For example NoStatus: wrong IP address, $STMO.$PHYS_PORT, or protocol version too high
    print(f"Error: {ex}")

robot.disconnect()
```

- `ErrorOccurred` reports the errors of the communication thread, for example a lost connection or a callback that failed.
- `Underrun` is raised when the robot was moving and no more positions were available: the client stopped it smoothly.
- `SessionEnded` with the reason `ProgramStopped` means that the program left `IBGN start`, often because of an alarm. Read the active alarms with [CGTP or SNPX](pages/how-to-reset-fanuc-alarm-remotely.md).
- `StreamMotionException.Error` tells the kind of error thrown by a method (`NoStatus`, `VersionMismatch`, `StartMismatch`, `SourceBusy`...).

### Common alarms

The number of an alarm can change with the software version of the controller.

| Alarm | Cause | Solution |
| --- | --- | --- |
| Joint velocity, acceleration or jerk limit exceeded | The positions are too fast for the robot | Plan the motion with the [motion planner](pages/motion.md), or check your positions with `Check()` before sending them |
| MOTN-603 Receiving interval over | Positions arrived too late: the PC was busy or the network was slow | Increase `BufferLeadTime`, keep `HighPriority`, use a wired network with little traffic |
| MOTN-607 | Protocol version not supported by the controller | Set `ProtocolVersion` to `$STMO.$USABLE_VER` or lower |
| MOTN-615 | Servo off is enabled for the group | Set `$PARAM_GROUP[1].$SV_OFF_ENB[*]` to `FALSE` |
| MOTN-623 | Resume offset is enabled | Disable the resume offset |
| MOTN-625 Abnormal position | The first position is far from the position of the robot | Start each trajectory at `QueueEndJointPosition` or `QueueEndCartesianPosition` |
| MOTN-018 Position not reachable | Cartesian position in another frame than the one expected by the robot | Some controllers expect the position of the active tool: select a tool frame equal to zero, or use joint positions |
| PRIO-023 | An I/O that is not assigned was written | Check the type and the index of the I/O |

### Good practices

- **Plan within the limits.** Use the motion planner, which respects the velocity, acceleration and jerk of each axis. For positions computed by your application, call `Check()` with the communication cycle of the robot.
- **Keep a small margin with protocol version 1.** Positions are sent in single precision: the rounding adds a little noise to the jerk. Use about 99% of the limits, or protocol version 2 for joint motions.
- **Prefer joint positions for large changes of orientation**, especially at 2 ms. Cartesian positions are always sent in single precision.
- **Choose prudent Cartesian limits.** The SDK cannot check the joint limits of a Cartesian motion: the same Cartesian speed can be fine in one pose and too fast for the wrist in another one. Validate them on the robot or in ROBOGUIDE.
- **Read the limits before running the TP program.** Some controllers do not answer while a program waits on `IBGN start`.
- **Start from the right position.** Always build a trajectory from `QueueEndJointPosition` or `QueueEndCartesianPosition`.
- **Use a dedicated wired network.** Stream Motion sends one packet every cycle (up to 500 per second). Avoid Wi-Fi and heavy traffic on the same port.
- **Finish the session.** Call `Finish()` so that the program continues after `IBGN end`. `Disconnect()` also stops the robot smoothly and finishes the session.
- **Test in ROBOGUIDE first.** Stream Motion works with the virtual controllers of ROBOGUIDE when the J519 option is loaded.

### Check the quality of the communication

`Statistics` gives the number of status received and lost, the positions sent, the underruns, and the time between two status. A high `MaxStatusInterval` or many lost status show a PC or network problem.
