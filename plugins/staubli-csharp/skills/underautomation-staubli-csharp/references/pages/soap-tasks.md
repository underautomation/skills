# VAL 3 tasks

List the VAL 3 tasks with their state, program line and runtime error, then suspend, resume or kill a task.

Web page: https://underautomation.com/staubli/documentation/soap-tasks

This page shows how to follow and control the VAL 3 tasks of a Staubli CS8 or CS9 controller: list them with their state, their program line and their runtime error, then suspend, resume or kill a task.

## List the tasks

`GetTasks()` returns every task of the controller.

```csharp
using UnderAutomation.Staubli;
using UnderAutomation.Staubli.Soap.Data;

public class TaskList
{
    static void Main()
    {
        var controller = new StaubliController();
        controller.Connect("192.168.0.254");

        ControllerTask[] tasks = controller.Soap.GetTasks();

        foreach (ControllerTask task in tasks)
        {
            // State: Idle, Transition, Running, Stepping, Stopped
            Console.WriteLine($"{task.Name} ({task.State}), priority {task.Priority}, created by {task.CreatedBy}");

            // Line of the VAL 3 program that the task executes
            ProgramLine line = task.ProgramLine;
            if (line != null)
                Console.WriteLine($"  {line.ProgramName}:{line.LineNumber} {line.LineContent}");

            // Runtime error of the task, 0 when there is none
            if (task.RuntimeError != 0)
                Console.WriteLine($"  Error {task.RuntimeError}: {task.RuntimeErrorDescription}");
        }

        controller.Disconnect();
    }
}
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

```csharp
using UnderAutomation.Staubli;
using UnderAutomation.Staubli.Soap.Data;

public class TaskControl
{
    static void Main()
    {
        var controller = new StaubliController();
        controller.Connect("192.168.0.254");

        // A task is identified by its name and by the project that created it
        ControllerTask task = controller.Soap.GetTasks().First(t => t.Name == "myTask");

        // Pause the task
        controller.Soap.TaskSuspend(task.Name, task.CreatedBy);

        // Continue it
        controller.Soap.TaskResume(task.Name, task.CreatedBy);

        // Stop it for good
        controller.Soap.TaskKill(task.Name, task.CreatedBy);

        controller.Disconnect();
    }
}
```

- `TaskSuspend` pauses the task.
- `TaskResume` continues a suspended task.
- `TaskKill` stops the task for good.

When the task does not exist, the method throws a `CustomSoapException` with the code `TaskNotFound`.

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**Methods of SoapClientBase** ([reference](../api/UnderAutomation.Staubli.Soap.Internal.md#soapclientbase-controllersoap))

- `ControllerTask[] GetTasks()`: Get all the tasks available on the controller
- `void TaskKill(string taskName, string createdBy)`: Kill a task on the controller
- `void TaskResume(string taskName, string createdBy)`: Resume a task on the controller
- `void TaskSuspend(string taskName, string createdBy)`: Suspend a task on the controller

**ControllerTask** ([reference](../api/UnderAutomation.Staubli.Soap.Data.md#controllertask))

- `ControllerTask()`: Initializes a new instance of the Data.ControllerTask class.
- `string CreatedBy { get; set; }`: Name of the entity that created the task.
- `string Name { get; set; }`: Name of the task.
- `int Priority { get; set; }`: Priority level of the task.
- `ProgramLine ProgramLine { get; set; }`: Current program line being executed by the task.
- `int RuntimeError { get; set; }`: Runtime error code (0 if no error).
- `string RuntimeErrorDescription { get; set; }`: Human-readable description of the runtime error.
- `ControllerTaskState State { get; set; }`: Current execution state of the task.

**ControllerTaskState** ([reference](../api/UnderAutomation.Staubli.Soap.Data.md#controllertaskstate))

- Idle: Task is idle and not executing.
- Running: Task is currently running.
- Stepping: Task is executing step by step.
- Stopped: Task is stopped.
- Transition: Task is transitioning between states.

**ProgramLine** ([reference](../api/UnderAutomation.Staubli.Soap.Data.md#programline))

- `ProgramLine()`: Initializes a new instance of the Data.ProgramLine class.
- `string ApplicationName { get; set; }`: Name of the application containing the program.
- `string LineContent { get; set; }`: Content of the line being executed.
- `int LineNumber { get; set; }`: Line number currently being executed.
- `string ProgramName { get; set; }`: Name of the program.
