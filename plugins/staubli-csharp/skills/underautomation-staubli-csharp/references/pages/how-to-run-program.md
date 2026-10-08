# Run a VAL 3 program

Load a VAL 3 project from the disk of the controller, start it, check its tasks and stop it, from C# or Python.

Web page: https://underautomation.com/staubli/documentation/how-to-run-program

This article shows how to start and stop a VAL 3 program of a Staubli CS8 or CS9 controller from a PC, in C# or Python. It gives a complete program that loads a project from the disk of the controller, starts it, checks its tasks and stops it.

## Prerequisites

- The SDK is connected to the controller: see [Connect to your robot](connect.md).
- The VAL 3 project is on the disk of the controller, for example `Disk://myProject/myProject.pjx`. Copy it there from the PC with `controller.File.UploadApplicationToController(...)` (see [Send a VAL 3 application](files-applications.md)), or with Staubli Robotics Suite or the pendant.
- The user of the connection has the right to start applications. If the application moves the arm, the controller is in the mode that the application needs.

## The calls

| Step                        | Method                      |
| --------------------------- | --------------------------- |
| See what is loaded and runs | `GetValApplications()`      |
| Free the memory             | `StopAndUnloadAll()`        |
| Load a project              | `LoadProject(path)`         |
| Start it                    | `StartApplication(path)`    |
| Check its tasks             | `GetTasks()`                |
| Pause or continue one task  | `TaskSuspend`, `TaskResume` |
| Stop the application        | `StopApplication()`         |

## Example

```csharp
using UnderAutomation.Staubli;
using UnderAutomation.Staubli.Soap.Data;
using UnderAutomation.Staubli.Soap.Errors;

public class HowToRunProgram
{
    static void Main()
    {
        var controller = new StaubliController();
        controller.Connect("192.168.0.254");

        string project = "Disk://myProject/myProject.pjx";

        // 1. Stop what runs, and free the memory
        controller.Soap.StopAndUnloadAll();

        // 2. Load and start the application
        try
        {
            controller.Soap.LoadProject(project);
            controller.Soap.StartApplication(project);
        }
        catch (CustomSoapException ex)
        {
            // For example ApplicationNotFound or CannotStartApplication
            Console.WriteLine($"{ex.ErrorCode}: {ex.Description}");
            return;
        }

        // 3. Check that its tasks run
        Thread.Sleep(500);
        foreach (ControllerTask task in controller.Soap.GetTasks())
            Console.WriteLine($"{task.Name}: {task.State}");

        // 4. Later, stop it
        controller.Soap.StopApplication();

        controller.Disconnect();
    }
}
```

The program:

1. stops and unloads what runs, so that the project loads in a known state;
2. loads and starts the project, and prints the reason if the controller refuses;
3. waits 500 ms and prints the state of each task;
4. stops the application.

## Follow the program

After the start, read the tasks with `GetTasks()`: `State` tells if a task runs, `ProgramLine` gives its current line, and `RuntimeError` is not `0` when the program stopped on an error. See [Monitor the state of the robot](how-to-monitor-state.md).

## Troubleshooting

- **`CustomSoapException` with `ApplicationNotFound`:** the path is wrong. Check the name of the folder and of the `.pjx` file on the disk of the controller.
- **`CustomSoapException` with `CannotStartApplication`:** the controller cannot start the project in its current state, for example because another application runs. Call `StopAndUnloadAll()` first.
- **The task stops at once:** read `RuntimeError` and `RuntimeErrorDescription` of the task.

## What to read next

- [VAL 3 applications](soap-applications.md) and [VAL 3 tasks](soap-tasks.md): the reference of these methods.
