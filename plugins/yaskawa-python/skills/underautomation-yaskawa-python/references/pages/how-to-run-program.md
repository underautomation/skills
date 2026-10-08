# Run a job

Select a job of a Yaskawa controller, switch the servo on, start it and wait for its end from C# or Python. Settings of the controller and frequent errors.

Web page: https://underautomation.com/yaskawa/documentation/how-to-run-program

This article shows how to start a job of a Yaskawa Motoman controller from a PC, in C# or Python, and wait for its end. It gives a complete program that checks the mode, resets an alarm, selects the job, switches the servo on and starts it.

## Prerequisites

- The SDK is connected to the controller: see [Connect to your robot](connect.md).
- The controller is in play mode and accepts the remote commands, and the job selection is permitted: see [Prepare the controller](connect.md#prepare_the_controller).
- The job exists on the controller. To send it from the PC, see [Transfer files and backups](how-to-transfer-files.md).

## Steps

| Step                        | Method                                                           |
| --------------------------- | ---------------------------------------------------------------- |
| Check the mode              | `GetStatusInformation()`: `Play`, `CommandRemote`                |
| Reset an alarm              | `AlarmReset(AlarmResetType.Reset)`                               |
| Select the job and its line | `SelectJob(name, line)`                                          |
| One cycle or continuous     | `SetCycle(RobotCycleType.OneCycle)`                              |
| Servo on                    | `SetServo(true)`                                                 |
| Start                       | `StartJob()`                                                     |
| Follow                      | `GetExecutingJobInformation()`, `GetStatusInformation().Running` |

## Example

```python
import time
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters
from underautomation.yaskawa.high_speed_e_server.alarm_reset_type import AlarmResetType
from underautomation.yaskawa.common.robot_cycle_type import RobotCycleType

robot = YaskawaRobot()
robot.connect(ConnectParameters("192.168.0.1"))
hses = robot.high_speed_e_server

# 1. Check the mode: play and remote
status = hses.get_status_information()
if not status.play or not status.command_remote:
    raise RuntimeError("Set the controller in play mode and remote mode")

# 2. Reset a pending alarm
if status.alarming:
    hses.alarm_reset(AlarmResetType.Reset)

# 3. Select the job at its first line, one cycle, servo on, start
hses.select_job("WELD01", 0)
hses.set_cycle(RobotCycleType.OneCycle)
hses.set_servo(True)
hses.start_job()

# 4. Wait for the end of the job
while True:
    time.sleep(0.2)
    job = hses.get_executing_job_information()
    print(f"{job.name} line {job.line}")
    status = hses.get_status_information()
    if not status.running:
        break

print("Stopped on an alarm" if status.alarming else "Job done")

robot.disconnect()
```

The program stops with an error if the controller is not in play mode or not in remote mode. Then it runs the job once, prints its line every 200 ms, and says at the end whether the job ended or stopped on an alarm.

## Stop a job

Hold the robot with `SetHold(true)`: the robot stops on its path. Release the hold and call `StartJob()` to continue, or switch the servo off to end. See [Jobs](hses-jobs.md#hold_and_restart).

## With the Ethernet Server

The [Ethernet Server](ethernet-server.md) has the same steps, and waits for the end of the job in one call: `WaitForJobCompletion(seconds)` returns `true` when the job completed. There is no polling loop to write.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters

parameters = ConnectParameters("192.168.0.1")
parameters.e_server.enable = True
robot = YaskawaRobot()
robot.connect(parameters)

# Play mode, remote mode, no alarm
robot.e_server.select_job("PICK", 0)  # job and line
robot.e_server.set_servo(True)
robot.e_server.start_job()

# Blocks until the job ends, or 60 s
completed = robot.e_server.wait_for_job_completion(60)
print("Job completed" if completed else "Job stopped or timeout")

robot.disconnect()
```

## Troubleshooting

- **`Command remote not set`:** the remote mode is off. See [Prepare the controller](connect.md#prepare_the_controller).
- **`Incorrect mode`:** the controller is in teach mode. Turn the mode key to play.
- **`SelectJob` is refused:** the name has the `.JBI` extension, the job does not exist, or `JOB SELECT WHEN REMOTE AND PLAY` is not permitted.
- **`Servo OFF`:** call `SetServo(true)` before `StartJob()`.

## What to read next

- [Jobs](hses-jobs.md): the reference of the job methods.
- [Read and reset alarms](how-to-read-reset-alarms.md).
