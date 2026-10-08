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

```csharp
using UnderAutomation.Yaskawa;
using UnderAutomation.Yaskawa.Common;
using UnderAutomation.Yaskawa.HighSpeedEServer;

public class HowToRunProgram
{
    static void Main()
    {
        var robot = new YaskawaRobot();
        robot.Connect("192.168.0.1");

        // 1. Check the mode: play and remote
        RobotStatusData status = robot.HighSpeedEServer.GetStatusInformation();
        if (!status.Play || !status.CommandRemote)
            throw new InvalidOperationException("Set the controller in play mode and remote mode");

        // 2. Reset a pending alarm
        if (status.Alarming)
            robot.HighSpeedEServer.AlarmReset(AlarmResetType.Reset);

        // 3. Select the job at its first line, one cycle, servo on, start
        robot.HighSpeedEServer.SelectJob("WELD01", 0);
        robot.HighSpeedEServer.SetCycle(RobotCycleType.OneCycle);
        robot.HighSpeedEServer.SetServo(true);
        robot.HighSpeedEServer.StartJob();

        // 4. Wait for the end of the job
        do
        {
            Thread.Sleep(200);
            RobotJobData job = robot.HighSpeedEServer.GetExecutingJobInformation();
            Console.WriteLine($"{job.Name} line {job.Line}");
            status = robot.HighSpeedEServer.GetStatusInformation();
        }
        while (status.Running);

        Console.WriteLine(status.Alarming ? "Stopped on an alarm" : "Job done");

        robot.Disconnect();
    }
}
```

The program stops with an error if the controller is not in play mode or not in remote mode. Then it runs the job once, prints its line every 200 ms, and says at the end whether the job ended or stopped on an alarm.

## Stop a job

Hold the robot with `SetHold(true)`: the robot stops on its path. Release the hold and call `StartJob()` to continue, or switch the servo off to end. See [Jobs](hses-jobs.md#hold_and_restart).

## With the Ethernet Server

The [Ethernet Server](ethernet-server.md) has the same steps, and waits for the end of the job in one call: `WaitForJobCompletion(seconds)` returns `true` when the job completed. There is no polling loop to write.

```csharp
using UnderAutomation.Yaskawa;

public class EServerJobStart
{
    static void Main()
    {
        var parameters = new ConnectParameters("192.168.0.1");
        parameters.EServer.Enable = true;
        var robot = new YaskawaRobot();
        robot.Connect(parameters);

        // Play mode, remote mode, no alarm
        robot.EServer.SelectJob("PICK", 0); // job and line
        robot.EServer.SetServo(true);
        robot.EServer.StartJob();

        // Blocks until the job ends, or 60 s
        bool completed = robot.EServer.WaitForJobCompletion(60);
        Console.WriteLine(completed ? "Job completed" : "Job stopped or timeout");

        robot.Disconnect();
    }
}
```

## Troubleshooting

- **`Command remote not set`:** the remote mode is off. See [Prepare the controller](connect.md#prepare_the_controller).
- **`Incorrect mode`:** the controller is in teach mode. Turn the mode key to play.
- **`SelectJob` is refused:** the name has the `.JBI` extension, the job does not exist, or `JOB SELECT WHEN REMOTE AND PLAY` is not permitted.
- **`Servo OFF`:** call `SetServo(true)` before `StartJob()`.

## What to read next

- [Jobs](hses-jobs.md): the reference of the job methods.
- [Read and reset alarms](how-to-read-reset-alarms.md).
