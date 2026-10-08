# VAL 3 applications

List the VAL 3 applications of a Staubli controller, load a project from its disk, start it, stop it and unload it from a PC.

Web page: https://underautomation.com/staubli/documentation/soap-applications

This page shows how to manage the VAL 3 applications of a Staubli CS8 or CS9 controller from a PC: list them, load a project from the disk of the controller, start it, stop it and unload it. The tasks that an application creates are on the page [VAL 3 tasks](soap-tasks.md).

## List the applications

`GetValApplications()` returns the VAL 3 applications of the controller.

```csharp
using UnderAutomation.Staubli;
using UnderAutomation.Staubli.Soap.Data;

public class ApplicationList
{
    static void Main()
    {
        var controller = new StaubliController();
        controller.Connect("192.168.0.254");

        ValApplication[] applications = controller.Soap.GetValApplications();

        foreach (ValApplication application in applications)
        {
            Console.WriteLine($"{application.Name}: loaded={application.Loaded} running={application.IsRunning} encrypted={application.IsCrypted}");
        }

        controller.Disconnect();
    }
}
```

| Property    | Meaning                      |
| ----------- | ---------------------------- |
| `Name`      | Name of the application      |
| `Loaded`    | The application is in memory |
| `IsRunning` | The application runs         |
| `IsCrypted` | The application is encrypted |

## Load and start a project

`LoadProject(path)` loads a project from the disk of the controller, without starting it. `StartApplication(path)` starts it. The path is the one of the project file on the controller, for example `Disk://myProject/myProject.pjx`, which is the file `/usr/usrapp/myProject/myProject.pjx`. To copy a project from the PC to the controller, see [Send a VAL 3 application](files-applications.md).

```csharp
using UnderAutomation.Staubli;

public class ApplicationLoadStart
{
    static void Main()
    {
        var controller = new StaubliController();
        controller.Connect("192.168.0.254");

        // Path of the project on the disk of the controller
        string project = "Disk://myProject/myProject.pjx";

        // Load the application in memory, without starting it
        controller.Soap.LoadProject(project);

        // Start it
        controller.Soap.StartApplication(project);

        controller.Disconnect();
    }
}
```

When the controller refuses, the method throws a `CustomSoapException`. Its `ErrorCode` tells why, for example `ApplicationNotFound` or `CannotStartApplication`. See [Connect to your robot](connect.md) for the errors.

## Stop and unload

```csharp
using UnderAutomation.Staubli;

public class ApplicationStop
{
    static void Main()
    {
        var controller = new StaubliController();
        controller.Connect("192.168.0.254");

        // Stop the running application. It stays in memory.
        controller.Soap.StopApplication();

        // Or stop every application and remove them from memory
        controller.Soap.StopAndUnloadAll();

        controller.Disconnect();
    }
}
```

- `StopApplication()` stops the running application. It stays in memory.
- `StopAndUnloadAll()` stops every application and removes them from memory.

A running application can move the arm: check the state of the cell before you start or stop one from a PC.

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**Methods of SoapClientBase** ([reference](../api/UnderAutomation.Staubli.Soap.Internal.md#soapclientbase-controllersoap))

- `ValApplication[] GetValApplications()`: Get all the VAL applications available on the controller
- `void LoadProject(string projectPath)`: Load a project in memory from disk (does not start it)
- `void StartApplication(string applicationPath)`: Start a VAL application on the controller
- `void StopAndUnloadAll()`: Stop all VAL applications on the controller
- `void StopApplication()`: Stop application on the controller

**ValApplication** ([reference](../api/UnderAutomation.Staubli.Soap.Data.md#valapplication))

- `ValApplication()`
- `bool IsCrypted { get; set; }`: Indicates whether the application is encrypted.
- `bool IsRunning { get; set; }`: Indicates whether the application is currently running.
- `bool Loaded { get; set; }`: Indicates whether the application is loaded in memory.
- `string Name { get; set; }`: Name of the application.
