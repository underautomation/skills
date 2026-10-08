# VAL 3 tasks

List the VAL 3 tasks with their state, program line and runtime error, then suspend, resume or kill a task.

Web page: https://underautomation.com/staubli/documentation/soap-tasks

This page shows how to follow and control the VAL 3 tasks of a Staubli CS8 or CS9 controller: list them with their state, their program line and their runtime error, then suspend, resume or kill a task.

## List the tasks

`GetTasks()` returns every task of the controller.

```python
from underautomation.staubli.staubli_controller import StaubliController

controller = StaubliController()
controller.connect("192.168.0.254")

tasks = controller.soap.get_tasks()

for task in tasks:
    # state: Idle, Transition, Running, Stepping, Stopped
    print(f"{task.name} ({task.state.name}), priority {task.priority}, created by {task.created_by}")

    # Line of the VAL 3 program that the task executes
    line = task.program_line
    if line is not None:
        print(f"  {line.program_name}:{line.line_number} {line.line_content}")

    # Runtime error of the task, 0 when there is none
    if task.runtime_error != 0:
        print(f"  Error {task.runtime_error}: {task.runtime_error_description}")

controller.disconnect()
```

| Property                  | Meaning                                                        |
| ------------------------- | -------------------------------------------------------------- |
| `Name`                    | Name of the task                                               |
| `CreatedBy`               | The project that created the task                              |
| `State`                   | `Idle`, `Transition`, `Running`, `Stepping` or `Stopped`       |
| `Priority`                | Priority of the task                                           |
| `ProgramLine`             | Application, program, line number and text of the current line |
| `RuntimeError`            | Code of the runtime error of the task, `0` when there is none  |
| `RuntimeErrorDescription` | Text of the runtime error                                      |

`RuntimeError` is the way to detect that a VAL 3 program stopped on an error. See [Monitor the state of the robot](how-to-monitor-state.md).

## Suspend, resume and kill

A task is identified by its name and by the project that created it: pass `Name` and `CreatedBy` as they come from `GetTasks()`.

```python
from underautomation.staubli.staubli_controller import StaubliController

controller = StaubliController()
controller.connect("192.168.0.254")

# A task is identified by its name and by the project that created it
task = next(t for t in controller.soap.get_tasks() if t.name == "myTask")

# Pause the task
controller.soap.task_suspend(task.name, task.created_by)

# Continue it
controller.soap.task_resume(task.name, task.created_by)

# Stop it for good
controller.soap.task_kill(task.name, task.created_by)

controller.disconnect()
```

- `TaskSuspend` pauses the task.
- `TaskResume` continues a suspended task.
- `TaskKill` stops the task for good.

When the task does not exist, the method throws a `CustomSoapException` with the code `TaskNotFound`.

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**Methods of SoapClientBase** ([reference](../api/underautomation.staubli.soap.internal.md#soapclientbase-controllersoap))

- `get_tasks() -> typing.List[ControllerTask]`: Get all the tasks available on the controller
- `task_kill(taskName: str, createdBy: str) -> None`: Kill a task on the controller
- `task_resume(taskName: str, createdBy: str) -> None`: Resume a task on the controller
- `task_suspend(taskName: str, createdBy: str) -> None`: Suspend a task on the controller

**ControllerTask** ([reference](../api/underautomation.staubli.soap.data.md#controllertask))

- `ControllerTask()`: Initializes a new instance of the ControllerTask class.
- `name: str`: Name of the task.
- `state: ControllerTaskState`: Current execution state of the task.
- `priority: int`: Priority level of the task.
- `created_by: str`: Name of the entity that created the task.
- `runtime_error: int`: Runtime error code (0 if no error).
- `runtime_error_description: str`: Human-readable description of the runtime error.
- `program_line: ProgramLine`: Current program line being executed by the task.

**ControllerTaskState** ([reference](../api/underautomation.staubli.soap.data.md#controllertaskstate))

- Idle: Task is idle and not executing.
- Transition: Task is transitioning between states.
- Running: Task is currently running.
- Stepping: Task is executing step by step.
- Stopped: Task is stopped.

**ProgramLine** ([reference](../api/underautomation.staubli.soap.data.md#programline))

- `ProgramLine()`: Initializes a new instance of the ProgramLine class.
- `application_name: str`: Name of the application containing the program.
- `program_name: str`: Name of the program.
- `line_number: int`: Line number currently being executed.
- `line_content: str`: Content of the line being executed.
