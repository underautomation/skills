# Jobs

List the jobs of a Yaskawa controller through the Ethernet Server, select and start a job, wait for its end in one call, set the master job and delete jobs.

Web page: https://underautomation.com/yaskawa/documentation/eserver-jobs

This page shows how to list, select, start and follow the jobs of a Yaskawa Motoman controller through the Ethernet Server, and how to wait for the end of a job in one call. It covers the YRC1000 and YRC1000micro controllers.

## List the jobs

`GetJobDirectory(filter)` returns the names of the jobs, without the `.JBI` extension. The filter accepts `*`: `"*"` (default) lists every job, `"VISION*"` the jobs whose name starts with `VISION`. `GetExecutingJobInformation()` reads the job that is executed, with its line and step.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters

parameters = ConnectParameters("192.168.0.1")
parameters.e_server.enable = True
robot = YaskawaRobot()
robot.connect(parameters)

# Names of every job, without extension
all_jobs = robot.e_server.get_job_directory()
for name in all_jobs.job_names:
    print(name)

# Jobs whose name starts with VISION
vision = robot.e_server.get_job_directory("VISION*")

# Executing job: name, line and step
job = robot.e_server.get_executing_job_information()
print(f"{job.name}, line {job.line}, step {job.step}")

robot.disconnect()
```

On a YRC1000micro with 7 jobs, `GetJobDirectory()` answers in about 20 ms.

## Start a job and wait for its end

### Prerequisites

- The controller is in play mode and in remote mode.
- No alarm is active, no hold is on.
- The job exists on the controller. To send a job, see [FTP](ftp-transfer.md).

### Example

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

1. `SelectJob(name, line)` selects the job and the line to start from (0 to 9999).
2. `SetServo(true)` switches the servo power on.
3. `StartJob()` starts the selected job. `StartJob(name)` selects and starts a job in one call.
4. `WaitForJobCompletion(seconds)` blocks until the job ends. It returns `true` when the job completed, `false` when it was stopped or when the time is over. `-1` waits without limit, the maximum is 32767 s.

`WaitForJobCompletion` throws a `HostControlException` when the job stops because of a hold, an alarm or the servo power. Catch it to know why the job did not end.

## Master job and tasks

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters

parameters = ConnectParameters("192.168.0.1")
parameters.e_server.enable = True
robot = YaskawaRobot()
robot.connect(parameters)

# Master job: the job of the master task, selected at startup
robot.e_server.set_master_job("MAIN")

# Start a job by its name, without select_job first
robot.e_server.start_job("MAIN")

# Task of the next job commands (0 = master task, 1 to 15 = sub tasks)
robot.e_server.set_task(0)

# Delete a job of the controller: there is no undo
robot.e_server.delete_job("OLDJOB")

robot.disconnect()
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

**Methods of HostControlClientBase** ([reference](../api/underautomation.yaskawa.host_control.internal.md#hostcontrolclientbase-robote_server))

- `get_executing_job_information() -> HostControlJobData`: Reads information about the currently selected and executing job (program). Returns job name, current line, and step.
- `start_job(jobName: str=None) -> HostControlResponse`: Starts job execution. Starts the currently selected job, or starts a specific job if specified.
- `get_job_directory(jobNameFilter: str="*") -> HostControlJobDirectoryData`: Reads the job directory listing from the robot controller.
- `delete_job(jobName: str) -> HostControlResponse`: Deletes a specified job from the robot controller.
- `set_master_job(jobName: str) -> HostControlResponse`: Sets a specified job as the master job and execution job.
- `select_job(jobName: str, line: int) -> HostControlResponse`: Sets the job name and line number for execution.
- `wait_for_job_completion(timeoutSeconds: int=-1) -> bool`: Waits for the current job to complete or the specified timeout to elapse. No response is sent until the job completes or the timeout expires.
- `convert_to_relative_job(jobName: str, coordinateSystem: HostControlCoordinateSystem) -> HostControlResponse`: Converts a specified job to a relative job of a specified coordinate system. Requires the relative job function on the robot controller.
- `convert_to_standard_job(jobName: str, convertingMethod: int, referencePositionVariable: int) -> HostControlResponse`: Converts a specified job to a standard job (pulse job). Requires the relative job function on the robot controller.

**HostControlJobDirectoryData** ([reference](../api/underautomation.yaskawa.host_control.md#hostcontroljobdirectorydata))

- `job_names: typing.Any (read only)`: Gets or sets the list of job names in the directory.
- Inherited from [HostControlResponse](../api/underautomation.yaskawa.host_control.md#hostcontrolresponse): `response_code`, `command`, `success`, `error_message`

**HostControlJobData** ([reference](../api/underautomation.yaskawa.host_control.md#hostcontroljobdata))

- `name: str (read only)`: Gets or sets the name of the currently executing job.
- `line: int (read only)`: Gets or sets the current line number within the job (0-9999).
- `step: int (read only)`: Gets or sets the current step number within the job (1-9998).
- Inherited from [HostControlResponse](../api/underautomation.yaskawa.host_control.md#hostcontrolresponse): `response_code`, `command`, `success`, `error_message`

## What to read next

- [Run a job](how-to-run-program.md): the same task with the High Speed Ethernet Server, and the frequent errors.
- [Variables and I/O](eserver-variables-io.md): exchange data with the job.
