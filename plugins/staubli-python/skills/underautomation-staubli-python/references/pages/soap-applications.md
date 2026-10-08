# VAL 3 applications

List the VAL 3 applications of a Staubli controller, load a project from its disk, start it, stop it and unload it from a PC.

Web page: https://underautomation.com/staubli/documentation/soap-applications

This page shows how to manage the VAL 3 applications of a Staubli CS8 or CS9 controller from a PC: list them, load a project from the disk of the controller, start it, stop it and unload it. The tasks that an application creates are on the page [VAL 3 tasks](soap-tasks.md).

## List the applications

`GetValApplications()` returns the VAL 3 applications of the controller.

```python
from underautomation.staubli.staubli_controller import StaubliController

controller = StaubliController()
controller.connect("192.168.0.254")

applications = controller.soap.get_val_applications()

for application in applications:
    print(
        f"{application.name}: loaded={application.loaded} "
        f"running={application.is_running} encrypted={application.is_crypted}"
    )

controller.disconnect()
```

| Property    | Meaning                      |
| ----------- | ---------------------------- |
| `Name`      | Name of the application      |
| `Loaded`    | The application is in memory |
| `IsRunning` | The application runs         |
| `IsCrypted` | The application is encrypted |

## Load and start a project

`LoadProject(path)` loads a project from the disk of the controller, without starting it. `StartApplication(path)` starts it. The path is the one of the project file on the controller, for example `Disk://myProject/myProject.pjx`, which is the file `/usr/usrapp/myProject/myProject.pjx`. To copy a project from the PC to the controller, see [Send a VAL 3 application](files-applications.md).

```python
from underautomation.staubli.staubli_controller import StaubliController

controller = StaubliController()
controller.connect("192.168.0.254")

# Path of the project on the disk of the controller
project = "Disk://myProject/myProject.pjx"

# Load the application in memory, without starting it
controller.soap.load_project(project)

# Start it
controller.soap.start_application(project)

controller.disconnect()
```

When the controller refuses, the method throws a `CustomSoapException`. Its `ErrorCode` tells why, for example `ApplicationNotFound` or `CannotStartApplication`. See [Connect to your robot](connect.md) for the errors.

## Stop and unload

```python
from underautomation.staubli.staubli_controller import StaubliController

controller = StaubliController()
controller.connect("192.168.0.254")

# Stop the running application. It stays in memory.
controller.soap.stop_application()

# Or stop every application and remove them from memory
controller.soap.stop_and_unload_all()

controller.disconnect()
```

- `StopApplication()` stops the running application. It stays in memory.
- `StopAndUnloadAll()` stops every application and removes them from memory.

A running application can move the arm: check the state of the cell before you start or stop one from a PC.

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**Methods of SoapClientBase** ([reference](../api/underautomation.staubli.soap.internal.md#soapclientbase-controllersoap))

- `get_val_applications() -> typing.List[ValApplication]`: Get all the VAL applications available on the controller
- `start_application(applicationPath: str) -> None`: Start a VAL application on the controller
- `stop_and_unload_all() -> None`: Stop all VAL applications on the controller
- `stop_application() -> None`: Stop application on the controller
- `load_project(projectPath: str) -> None`: Load a project in memory from disk (does not start it)

**ValApplication** ([reference](../api/underautomation.staubli.soap.data.md#valapplication))

- `ValApplication()`
- `name: str`: Name of the application.
- `loaded: bool`: Indicates whether the application is loaded in memory.
- `is_crypted: bool`: Indicates whether the application is encrypted.
- `is_running: bool`: Indicates whether the application is currently running.
