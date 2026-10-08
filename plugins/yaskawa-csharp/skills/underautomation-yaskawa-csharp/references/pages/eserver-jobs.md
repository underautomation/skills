# Jobs

List the jobs of a Yaskawa controller through the Ethernet Server, select and start a job, wait for its end in one call, set the master job and delete jobs.

Web page: https://underautomation.com/yaskawa/documentation/eserver-jobs

This page shows how to list, select, start and follow the jobs of a Yaskawa Motoman controller through the Ethernet Server, and how to wait for the end of a job in one call. It covers the YRC1000 and YRC1000micro controllers.

## List the jobs

`GetJobDirectory(filter)` returns the names of the jobs, without the `.JBI` extension. The filter accepts `*`: `"*"` (default) lists every job, `"VISION*"` the jobs whose name starts with `VISION`. `GetExecutingJobInformation()` reads the job that is executed, with its line and step.

```csharp
using UnderAutomation.Yaskawa;
using UnderAutomation.Yaskawa.HostControl;

public class EServerJobList
{
    static void Main()
    {
        var parameters = new ConnectParameters("192.168.0.1");
        parameters.EServer.Enable = true;
        var robot = new YaskawaRobot();
        robot.Connect(parameters);

        // Names of every job, without extension
        HostControlJobDirectoryData all = robot.EServer.GetJobDirectory();
        foreach (string name in all.JobNames)
            Console.WriteLine(name);

        // Jobs whose name starts with VISION
        HostControlJobDirectoryData vision = robot.EServer.GetJobDirectory("VISION*");

        // Executing job: name, line and step
        HostControlJobData job = robot.EServer.GetExecutingJobInformation();
        Console.WriteLine($"{job.Name}, line {job.Line}, step {job.Step}");

        robot.Disconnect();
    }
}
```

On a YRC1000micro with 7 jobs, `GetJobDirectory()` answers in about 20 ms.

## Start a job and wait for its end

### Prerequisites

- The controller is in play mode and in remote mode.
- No alarm is active, no hold is on.
- The job exists on the controller. To send a job, see [FTP](ftp-transfer.md).

### Example

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

1. `SelectJob(name, line)` selects the job and the line to start from (0 to 9999).
2. `SetServo(true)` switches the servo power on.
3. `StartJob()` starts the selected job. `StartJob(name)` selects and starts a job in one call.
4. `WaitForJobCompletion(seconds)` blocks until the job ends. It returns `true` when the job completed, `false` when it was stopped or when the time is over. `-1` waits without limit, the maximum is 32767 s.

`WaitForJobCompletion` throws a `HostControlException` when the job stops because of a hold, an alarm or the servo power. Catch it to know why the job did not end.

## Master job and tasks

```csharp
using UnderAutomation.Yaskawa;

public class EServerJobManage
{
    static void Main()
    {
        var parameters = new ConnectParameters("192.168.0.1");
        parameters.EServer.Enable = true;
        var robot = new YaskawaRobot();
        robot.Connect(parameters);

        // Master job: the job of the master task, selected at startup
        robot.EServer.SetMasterJob("MAIN");

        // Start a job by its name, without SelectJob first
        robot.EServer.StartJob("MAIN");

        // Task of the next job commands (0 = master task, 1 to 15 = sub tasks)
        robot.EServer.SetTask(0);

        // Delete a job of the controller: there is no undo
        robot.EServer.DeleteJob("OLDJOB");

        robot.Disconnect();
    }
}
```

| Method                | Effect                                                                  |
| --------------------- | ----------------------------------------------------------------------- |
| `SetMasterJob(name)`  | Sets the master job and selects it for execution                        |
| `SetTask(task)`       | Task of the next job commands: 0 is the master task, 1 to 15 the sub tasks |
| `DeleteJob(name)`     | Deletes a job. `"*"` deletes every job. There is no undo                |

Download the jobs before you delete them: see [Transfer files and backups](how-to-transfer-files.md).

## Relative jobs

`ConvertToRelativeJob(name, coordinateSystem)` converts a job to a relative job in a frame, and `ConvertToStandardJob` converts it back. They need the relative job function on the controller.

## Reference

**Methods of HostControlClientBase** ([reference](../api/UnderAutomation.Yaskawa.HostControl.Internal.md#hostcontrolclientbase-roboteserver))

- `HostControlResponse ConvertToRelativeJob(string jobName, HostControlCoordinateSystem coordinateSystem)`: Converts a specified job to a relative job of a specified coordinate system. Requires the relative job function on the robot controller.
- `HostControlResponse ConvertToStandardJob(string jobName, int convertingMethod, int referencePositionVariable)`: Converts a specified job to a standard job (pulse job). Requires the relative job function on the robot controller.
- `HostControlResponse DeleteJob(string jobName)`: Deletes a specified job from the robot controller.
- `HostControlJobData GetExecutingJobInformation()`: Reads information about the currently selected and executing job (program). Returns job name, current line, and step.
- `HostControlJobDirectoryData GetJobDirectory(string jobNameFilter = "*")`: Reads the job directory listing from the robot controller.
- `HostControlResponse SelectJob(string jobName, int line)`: Sets the job name and line number for execution.
- `HostControlResponse SetMasterJob(string jobName)`: Sets a specified job as the master job and execution job.
- `HostControlResponse SetTask(int task)`: Changes the current task selection.
- `HostControlResponse StartJob(string jobName = null)`: Starts job execution. Starts the currently selected job, or starts a specific job if specified.
- `bool WaitForJobCompletion(int timeoutSeconds = -1)`: Waits for the current job to complete or the specified timeout to elapse. No response is sent until the job completes or the timeout expires.

**HostControlJobDirectoryData** ([reference](../api/UnderAutomation.Yaskawa.HostControl.md#hostcontroljobdirectorydata))

- `List<string> JobNames { get; }`: Gets or sets the list of job names in the directory.
- Inherited from [HostControlResponse](../api/UnderAutomation.Yaskawa.HostControl.md#hostcontrolresponse): `ResponseCode`, `Command`, `Success`, `ErrorMessage`

**HostControlJobData** ([reference](../api/UnderAutomation.Yaskawa.HostControl.md#hostcontroljobdata))

- `int Line { get; }`: Gets or sets the current line number within the job (0-9999).
- `string Name { get; }`: Gets or sets the name of the currently executing job.
- `int Step { get; }`: Gets or sets the current step number within the job (1-9998).
- Inherited from [HostControlResponse](../api/UnderAutomation.Yaskawa.HostControl.md#hostcontrolresponse): `ResponseCode`, `Command`, `Success`, `ErrorMessage`

## What to read next

- [Run a job](how-to-run-program.md): the same task with the High Speed Ethernet Server, and the frequent errors.
- [Variables and I/O](eserver-variables-io.md): exchange data with the job.
