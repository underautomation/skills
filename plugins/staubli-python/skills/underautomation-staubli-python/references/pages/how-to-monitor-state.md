# Monitor the state of the robot

Poll the applications and the VAL 3 tasks of a Staubli controller, print each change of state and each runtime error.

Web page: https://underautomation.com/staubli/documentation/how-to-monitor-state

This article shows how to monitor a Staubli CS8 or CS9 controller from a PC, in C# or Python: which applications run, the state of each VAL 3 task, and the runtime errors. It gives a complete program that polls the controller and prints each change.

## Prerequisites

- The SDK is connected to the controller: see [Connect to your robot](connect.md).
- Reading the state needs no right to change anything, and no VAL 3 program.

## What to read

| Information                     | Method                               | Field                                     |
| ------------------------------- | ------------------------------------ | ----------------------------------------- |
| Applications loaded and running | `GetValApplications()`               | `Loaded`, `IsRunning`                     |
| State of each task              | `GetTasks()`                         | `State`: `Idle`, `Running`, `Stopped`...  |
| Current line of a task          | `GetTasks()`                         | `ProgramLine`                             |
| Runtime error of a task         | `GetTasks()`                         | `RuntimeError`, `RuntimeErrorDescription` |
| Position of the arm             | `GetCurrentCartesianJointPosition()` | `JointsPosition`, `CartesianPosition`     |
| State of an input or output     | `ReadIos(names)`                     | `Value`                                   |

The SDK has no events for these values: poll them in a loop.

## Example

```python
import time
from datetime import datetime

from underautomation.staubli.staubli_controller import StaubliController

controller = StaubliController()
controller.connect("192.168.0.254")

last_states = {}

# Poll the controller every 500 ms
while controller.enabled:
    # Applications that run
    running = ", ".join(a.name for a in controller.soap.get_val_applications() if a.is_running)

    for task in controller.soap.get_tasks():
        # Report a change of state
        previous = last_states.get(task.name)
        if previous != task.state:
            before = previous.name if previous is not None else "-"
            print(f"{datetime.now():%H:%M:%S} {task.name}: {before} -> {task.state.name}")
        last_states[task.name] = task.state

        # Report a runtime error of a VAL 3 task
        if task.runtime_error != 0:
            print(f"{task.name} error {task.runtime_error}: {task.runtime_error_description}")

    time.sleep(0.5)
```

The program reads the applications and the tasks every 500 ms. It prints a line when the state of a task changes, and when a task has a runtime error. It runs while the connection is open.

## Choose the polling period

Each method call is one request. A loop with two calls every 500 ms sends 4 requests per second. Measure the duration of a request on your cell, then choose a period that leaves the controller and the network free for the other clients, like Staubli Robotics Suite. For values that change fast, read them in one call: `GetCurrentCartesianJointPosition` gives the joints and the Cartesian position together, `ReadIos` reads several I/O together.

## Troubleshooting

- **`WebException` after a while:** the network or the controller did not answer. Catch the exception, wait, and connect again.
- **`CustomSoapException` with `InvalidSessionIdCode`:** the session has expired, for example after a restart of the controller. Connect again.

## What to read next

- [VAL 3 tasks](soap-tasks.md): the fields of a task.
- [Run a VAL 3 program](how-to-run-program.md).
- [Read and write I/O](how-to-read-write-io.md).
