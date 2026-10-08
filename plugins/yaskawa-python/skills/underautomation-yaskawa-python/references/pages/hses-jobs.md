# Jobs

List the jobs of a Yaskawa controller, select a job and start it, hold it, and read the executing job, its line and the call stack of each task.

Web page: https://underautomation.com/yaskawa/documentation/hses-jobs

This page shows how to run the jobs of a Yaskawa Motoman controller from a PC with the SDK: list them, select one, start it, hold it, and follow its execution. A job is a program of the controller, written in INFORM.

## List the jobs

The jobs are `.JBI` files of the controller. `GetFileList("*.JBI")` gives their names.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters

robot = YaskawaRobot()
robot.connect(ConnectParameters("192.168.0.1"))

import os

# Job files of the controller, for example "WELD01.JBI"
files = robot.high_speed_e_server.get_file_list("*.JBI").files

for file in files:
    print(os.path.splitext(file)[0])

robot.disconnect()
```

## Select and start a job

`SelectJob(name, line)` selects a job and the line to start from. `StartJob()` starts the selected job.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters

robot = YaskawaRobot()
robot.connect(ConnectParameters("192.168.0.1"))

# Select the job by its name, without the .JBI extension, at line 0
robot.high_speed_e_server.select_job("WELD01", 0)

# Starting needs the play mode, the remote mode and the servo on
robot.high_speed_e_server.set_servo(True)
robot.high_speed_e_server.start_job()

robot.disconnect()
```

- The name is the name of the job, without the `.JBI` extension.
- The line `0` is the start of the job.
- Starting needs the play mode, the remote mode and the servo power. Selecting needs the setting `JOB SELECT WHEN REMOTE AND PLAY`. See [Connect to your robot](connect.md#prepare_the_controller).
- The cycle mode (step, one cycle, continuous) decides what happens at the end of the job: see [Status and servo](hses-status.md#cycle_mode).

## Hold and restart

A hold stops the robot on its path and keeps the servo power. After the hold is released, `StartJob()` continues the job from the current line.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters

robot = YaskawaRobot()
robot.connect(ConnectParameters("192.168.0.1"))

# Hold the job: the robot stops on its path and keeps the servo power
robot.high_speed_e_server.set_hold(True)

# Release the hold, then start again from the current line
robot.high_speed_e_server.set_hold(False)
robot.high_speed_e_server.start_job()

robot.disconnect()
```

## Follow the execution

`GetExecutingJobInformation()` reads the name of the executing job, its line, its step and the speed override. `GetJobStack(task)` reads the call stack of a task: the master job first, then each job called with `CALL`.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters

robot = YaskawaRobot()
robot.connect(ConnectParameters("192.168.0.1"))

# Job that the controller executes, with its line and step
job = robot.high_speed_e_server.get_executing_job_information()
print(f"{job.name}, line {job.line}, step {job.step}, speed override {job.speed_override} %")

# Call stack of the master task: the outermost job first
stack = robot.high_speed_e_server.get_job_stack(0)
print(" > ".join(stack.jobs))

# Call stack of the sub task 1
sub1 = robot.high_speed_e_server.get_job_stack(1)

robot.disconnect()
```

| Argument of `GetJobStack` | Task        |
| ------------------------- | ----------- |
| `0`                       | Master task |
| `1` to `15`               | Sub tasks   |

To know when a job ends, read `GetStatusInformation().Running` in a loop: see [Run a job](how-to-run-program.md).

## Send a job to the controller

A job written or changed on the PC is sent as a file: see [Files and backup](hses-files.md). Then select it and start it as above.

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**Methods of HighSpeedEServerClientBase** ([reference](../api/underautomation.yaskawa.high_speed_e_server.internal.md#highspeedeserverclientbase-robothigh_speed_e_server))

- `get_executing_job_information() -> RobotJobData`: Reads information about the currently selected and executing job (program). Returns job name, current line, step, and speed override percentage.
- `get_job_stack(taskNumber: int=0) -> RobotJobStackData`: Reads the job call stack for a specific task on the robot controller. Returns the current nesting of CALL instructions, from the outermost job to the currently executing one.
- `start_job() -> RobotDataHeader`: Starts execution of the currently selected job. The job must be selected first using SelectJob before calling this method. Servo must be ON and the robot must not be in alarm state.
- `select_job(job: str, line: int) -> RobotDataHeader`: Selects a job for execution and optionally positions to a specific line. Call StartJob after selecting to begin execution.

**RobotJobData** ([reference](../api/underautomation.yaskawa.high_speed_e_server.md#robotjobdata))

- `name: str (read only)`: Gets the name of the currently selected/executing job. Job names can be up to 32 characters. Returns empty string if no job is selected.
- `line: int (read only)`: Gets the current line number being executed within the job. Line numbers are 1-based and correspond to the job listing.
- `step: int (read only)`: Gets the current step number within the job. Step numbers track the execution progress through motion instructions.
- `speed_override: float (read only)`: Gets the current speed override percentage (0-100). This is the global speed multiplier applied to all motions.

**RobotJobStackData** ([reference](../api/underautomation.yaskawa.high_speed_e_server.md#robotjobstackdata))

- `jobs: typing.List[str] (read only)`: Gets the job names in the call stack, outermost first. The first entry is the root job, the last entry is the currently executing job. Empty if no nested calls are active.
