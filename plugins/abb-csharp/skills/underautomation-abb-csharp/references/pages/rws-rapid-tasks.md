# RAPID tasks & program execution

List RAPID tasks, start and stop program execution, follow the execution state, move the program pointer, load and unload modules.

Web page: https://underautomation.com/abb/documentation/rws-rapid-tasks

`robot.Rws.Rapid` is the service of the program the robot runs. This page covers the tasks the program is split into, starting and stopping the execution, and moving the program pointer. The variables of the program are on [RAPID variables & symbols](rws-rapid-symbols.md), the source of the modules on [RAPID modules & program files](rws-rapid-modules.md).

Reading never needs anything special. Every write of this page needs the `Rapid` [mastership](rws-mastership.md), and most of them also need the controller to be in the right operation mode. None of these resources answers while the controller runs in boot mode.

## Tasks

A controller runs one RAPID task per robot, plus the background tasks the system needs. `GetTasks` lists them all, `GetTask` returns everything the controller knows about one of them.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class RapidTaskList
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // Every RAPID task of the controller
        foreach (RapidTaskItem task in robot.Rws.Rapid.GetTasks())
        {
            Console.WriteLine(task.Name);                 // T_ROB1
            Console.WriteLine(task.Type);                 // Normal, Static or SemiStatic
            Console.WriteLine(task.TaskState);            // Linked when the program is ready to run
            Console.WriteLine(task.ExecutionState);       // Started, Stopped, Ready
            Console.WriteLine(task.Active);               // null when the controller did not report it
            Console.WriteLine(task.MotionTask);           // true for the task that drives the robot
        }

        // Everything the controller knows about one task
        RapidTaskInfo info = robot.Rws.Rapid.GetTask("T_ROB1");
        Console.WriteLine(info.ExecutionLevel);           // Normal, Trap, User, None
        Console.WriteLine(info.ExecutionCycle);           // Forever, Once, OnceDone
        Console.WriteLine(info.ExecutionMode);            // Continuous, StepIn, StepOver, ...
        Console.WriteLine(info.ProductionEntryPoint);
        Console.WriteLine(info.Trust);

        robot.Disconnect();
    }
}
```

| `RapidTaskType` | What the task is                                                        |
| --------------- | ----------------------------------------------------------------------- |
| `Normal`        | A task holding a program an operator starts and stops                   |
| `Static`        | A task started with the controller and never stopped                    |
| `SemiStatic`    | A task started with the controller and restarted at every program reset |
| `Unknown`       | The controller reported a type the SDK does not know                    |

`TaskState` says whether the task can run. Only `Linked` means that the modules of the task were turned into a runnable program. `Empty` means the task holds nothing, `Loaded` that the modules are there but not linked yet.

| `RapidTaskExecutionState` | Meaning                                     |
| ------------------------- | ------------------------------------------- |
| `Ready`                   | The task is ready to run but is not running |
| `Started`                 | The task is running                         |
| `Stopped`                 | The task was stopped before its end         |
| `Uninitialized`           | The task is not usable yet                  |

### Activate and deactivate a task

A deactivated task is not started when the program starts. The selection panel of the FlexPendant shows the same thing, `GetTaskSelection` reads it. `UserModify` says whether an operator is allowed to change the selection of that task from the pendant.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class RapidTaskActivation
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // Which tasks the operator panel has selected, and which of them an operator may change
        foreach (RapidTaskSelectionItem item in robot.Rws.Rapid.GetTaskSelection())
        {
            Console.WriteLine(item.Name + " selected=" + item.Selected + " userModify=" + item.UserModify);
        }

        // Activating or deactivating a task is a write, so it needs the mastership
        robot.Rws.Mastership.Request(MastershipDomain.Rapid);
        try
        {
            robot.Rws.Rapid.ActivateTask("T_ROB1");
            robot.Rws.Rapid.DeactivateTask("T_ROB2");

            // Same thing for every task at once
            robot.Rws.Rapid.ActivateTasks();
            robot.Rws.Rapid.DeactivateTasks();
        }
        finally
        {
            robot.Rws.Mastership.Release(MastershipDomain.Rapid);
        }

        robot.Disconnect();
    }
}
```

`GetTaskProgramPointerSyncState` and `GetTaskMotionPointerSyncState`, listed below, are described in the program pointer section of this page.

**Methods of RapidService** ([reference](../api/UnderAutomation.ABB.Rws.Services.md#rapidservice-robotrwsrapid))

- `void ActivateTask(string task)`: Activates one task (synchronous)
  - async: `Task ActivateTaskAsync(string task, CancellationToken cancellationToken = default)`
- `void ActivateTasks()`: Activates every task of the controller (synchronous)
  - async: `Task ActivateTasksAsync(CancellationToken cancellationToken = default)`
- `void DeactivateTask(string task)`: Deactivates one task (synchronous)
  - async: `Task DeactivateTaskAsync(string task, CancellationToken cancellationToken = default)`
- `void DeactivateTasks()`: Deactivates every task of the controller (synchronous)
  - async: `Task DeactivateTasksAsync(CancellationToken cancellationToken = default)`
- `RapidTaskInfo GetTask(string task)`: Gets everything the controller reports about one task (synchronous)
  - async: `Task<RapidTaskInfo> GetTaskAsync(string task, CancellationToken cancellationToken = default)`
- `RapidPointerSyncState GetTaskMotionPointerSyncState(string task)`: Gets whether the motion pointer of one task is synchronized with the others (synchronous)
  - async: `Task<RapidPointerSyncState> GetTaskMotionPointerSyncStateAsync(string task, CancellationToken cancellationToken = default)`
- `RapidPointerSyncState GetTaskProgramPointerSyncState(string task)`: Gets whether the program pointer of one task is synchronized with the others (synchronous)
  - async: `Task<RapidPointerSyncState> GetTaskProgramPointerSyncStateAsync(string task, CancellationToken cancellationToken = default)`
- `RapidTaskSelectionItem[] GetTaskSelection()`: Gets the task selection panel: which tasks are selected, and which of them an operator is allowed to change the selection of (synchronous)
  - async: `Task<RapidTaskSelectionItem[]> GetTaskSelectionAsync(CancellationToken cancellationToken = default)`
- `RapidTaskItem[] GetTasks()`: Gets every RAPID task of the controller and what each of them is doing (synchronous)
  - async: `Task<RapidTaskItem[]> GetTasksAsync(CancellationToken cancellationToken = default)`

**RapidTaskItem** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidtaskitem))

- `RapidTaskItem()`: Initializes a new instance of the Data.RapidTaskItem class
- `bool? Active { get; set; }`: Whether the task is active, null when the controller did not report it
- `RapidTaskExecutionState ExecutionState { get; set; }`: Whether the task is running, and whether it could be
- `bool? MotionTask { get; set; }`: Whether the task can move a mechanical unit, null when the controller did not report it
- `string Name { get; set; }`: Name of the task, for example "T_ROB1"
- `RapidTaskState TaskState { get; set; }`: How far the controller has got in preparing the program of the task
- `RapidTaskType Type { get; set; }`: Kind of task, which decides when the controller runs it

**RapidTaskInfo** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidtaskinfo))

- `RapidTaskInfo()`: Initializes a new instance of the Data.RapidTaskInfo class
- `bool? BindReference { get; set; }`: Whether the task is bound to a configured task number, null when the controller did not report it
- `RapidExecutionCycle ExecutionCycle { get; set; }`: Number of cycles the task is set to run. Only reported over a connection established with version 2, and left to RapidExecutionCycle.Unknown otherwise.
- `RapidExecutionLevel ExecutionLevel { get; set; }`: Level at which the code of the task is currently executing
- `RapidTaskExecutionMode ExecutionMode { get; set; }`: Stepping mode the task was last started with
- `RapidExecutionType ExecutionType { get; set; }`: What kind of code the task is currently running
- `string ProductionEntryPoint { get; set; }`: Routine the program pointer moves to when it is reset, for example "main"
- `int? TaskId { get; set; }`: Identifier of the task, null when the controller did not report it
- `string TaskInForeground { get; set; }`: Name of the task running in the foreground, empty when there is none
- `RapidTaskTrustLevel Trust { get; set; }`: What the controller does to the system when this task stops unexpectedly
- Inherited from [RapidTaskItem](../api/UnderAutomation.ABB.Rws.Data.md#rapidtaskitem): `Name`, `Type`, `TaskState`, `ExecutionState`, `Active`, `MotionTask`

**RapidTaskSelectionItem** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidtaskselectionitem))

- `RapidTaskSelectionItem()`: Initializes a new instance of the Data.RapidTaskSelectionItem class
- `bool? MotionTask { get; set; }`: Whether the task can move a mechanical unit, null when the controller did not report it
- `string Name { get; set; }`: Name of the task, for example "T_ROB1"
- `bool? Selected { get; set; }`: Whether the task is selected, null when the controller did not report it
- `bool? UserModify { get; set; }`: Whether an operator is allowed to change the selection of this task, null when the controller did not report it

**RapidTaskType** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidtasktype))

- Normal: A task started and stopped together with the program
- SemiStatic: A task restarted from its beginning every time the controller starts
- Static: A task that keeps its program pointer where it was when the controller was switched off
- Unknown: The controller reported a type this library does not know

**RapidTaskState** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidtaskstate))

- Empty: The task holds no program
- Initiated: The task has been created but its program is not linked yet
- Linked: The program of the task is linked and ready to run
- Loaded: A program is loaded into the task but not linked yet
- Uninitialized: The task is not initialized
- Unknown: The controller reported a state this library does not know

**RapidTaskExecutionState** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidtaskexecutionstate))

- Ready: The task is ready to be started
- Started: The task is running
- Stopped: The task was running and has been stopped
- Uninitialized: The task is not initialized
- Unknown: The controller reported a state this library does not know

**RapidTaskExecutionMode** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidtaskexecutionmode))

- Continuous: The task runs without stepping
- StepBack: The task steps backwards
- StepIn: The task steps into the routine calls
- StepLast: The task steps to the last instruction
- StepOutOf: The task steps out of the current routine
- StepOver: The task steps over the routine calls
- StepWise: The task advances one instruction at a time
- Unknown: The controller reported a mode this library does not know

**RapidTaskTrustLevel** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidtasktrustlevel))

- None: The system carries on
- SystemFailure: The whole system fails
- SystemHalt: The system halts
- SystemStop: The system stops
- Unknown: The controller reported a level this library does not know

## Build a task

`BuildTask` links the modules a task holds into a runnable program. The controller accepts the request even when the program does not compile, so read `GetBuildErrors` afterwards and check that the task state became `Linked`.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class RapidBuildTask
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        robot.Rws.Mastership.Request(MastershipDomain.Rapid);
        try
        {
            // Link the modules of the task into a runnable program
            robot.Rws.Rapid.BuildTask("T_ROB1");
        }
        finally
        {
            robot.Rws.Mastership.Release(MastershipDomain.Rapid);
        }

        // The controller does not fail the build request, it reports what it refused afterwards
        foreach (RapidBuildError error in robot.Rws.Rapid.GetBuildErrors("T_ROB1"))
        {
            Console.WriteLine(error.ModuleName + " " + error.Row + "," + error.Column + ": " + error.Error);
        }

        // The task is runnable when its state is Linked
        Console.WriteLine(robot.Rws.Rapid.GetTask("T_ROB1").TaskState);

        robot.Disconnect();
    }
}
```

The build errors are described in [RAPID modules & program files](rws-rapid-modules.md).

**Methods of RapidService** ([reference](../api/UnderAutomation.ABB.Rws.Services.md#rapidservice-robotrwsrapid))

- `void BuildTask(string task)`: Links the program of a task, which is what turns the modules it holds into something runnable (synchronous) Read GetBuildErrors() afterwards to find out what the controller refused.
  - async: `Task BuildTaskAsync(string task, CancellationToken cancellationToken = default)`

## Load a module

> **Available on** RWS 1.0 (IRC5) : yes | RWS 2.0 (OmniCore) : yes. Only an OmniCore answers with the name of the module that was loaded, an IRC5 returns null.

`LoadModule` loads one module file into a task. The file has to be on the file system of the controller already, so upload it first with the [file system service](rws-files.md). Set `replace` to `true` when a module of the same name is already loaded, otherwise the controller refuses the request.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class RapidLoadModule
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        robot.Rws.Mastership.Request(MastershipDomain.Rapid);
        try
        {
            // The file has to be on the controller already. Upload it first with robot.Rws.File.
            // On OmniCore the call answers the name of what was loaded, on IRC5 it answers null.
            string loaded = robot.Rws.Rapid.LoadModule("T_ROB1", "$HOME/mymodule.mod", true);
            Console.WriteLine(loaded);

            robot.Rws.Rapid.UnloadModule("T_ROB1", "mymodule");
        }
        finally
        {
            robot.Rws.Mastership.Release(MastershipDomain.Rapid);
        }

        robot.Disconnect();
    }
}
```

`UnloadModule` takes the name of the module, not the name of the file. A module that was never saved is lost when it is unloaded.

Loading a whole program instead of one module is done with `LoadProgram`, see [RAPID modules & program files](rws-rapid-modules.md).

**Methods of RapidService** ([reference](../api/UnderAutomation.ABB.Rws.Services.md#rapidservice-robotrwsrapid))

- `string LoadModule(string task, string modulePath, bool replace = false)`: Loads a module file into a task (synchronous)
  - async: `Task<string> LoadModuleAsync(string task, string modulePath, bool replace = false, CancellationToken cancellationToken = default)`
- `void UnloadModule(string task, string module)`: Unloads a module from a task (synchronous)
  - async: `Task UnloadModuleAsync(string task, string module, CancellationToken cancellationToken = default)`

## Start and stop the program

Starting a program from your application fails when one of these conditions is not met:

1. The controller is in automatic mode, or in manual mode with the enabling device held. The mode is read with the [control panel service](rws-panel.md).
2. The motors are on, `Panel.SetControllerState(ControllerState.MotorsOn)`.
3. The task is active and its state is `Linked`.
4. The program pointer is set, which `ResetProgramPointer` does for every task.
5. Your connection holds the `Rapid` [mastership](rws-mastership.md).

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class RapidStartProgram
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // 1. The controller has to be in automatic mode
        if (robot.Rws.Panel.GetOperationMode() != OperationMode.Automatic)
            throw new Exception("Turn the key of the controller to automatic mode");

        robot.Rws.Mastership.Request(MastershipDomain.Rapid);
        try
        {
            // 2. Motors on
            robot.Rws.Panel.SetControllerState(ControllerState.MotorsOn);

            // 3. Program pointer back to the entry point of every task
            robot.Rws.Rapid.ResetProgramPointer();

            // 4. Start
            robot.Rws.Rapid.Start(RapidRegainMode.Continue,
                                  RapidExecutionMode.Continue,
                                  RapidExecutionCycle.Forever,
                                  RapidStartCondition.None,
                                  false,   // do not stop at breakpoints
                                  false);  // normal tasks only
        }
        finally
        {
            robot.Rws.Mastership.Release(MastershipDomain.Rapid);
        }

        // 5. Check that it really started, the call above only means the request was accepted
        RapidExecutionInfo execution = robot.Rws.Rapid.GetExecutionState();
        Console.WriteLine(execution.State);   // Running or Stopped
        Console.WriteLine(execution.Cycle);   // Forever, Once, OnceDone

        robot.Disconnect();
    }
}
```

`Start` returns as soon as the controller accepts the request, not when the robot moves. Read `GetExecutionState` afterwards to know what really happened.

| `RapidRegainMode` | What the robot does when execution resumes                       |
| ----------------- | ---------------------------------------------------------------- |
| `Continue`        | Resume from the current position, without going back to the path |
| `Regain`          | Move back onto the path first                                    |
| `Clear`           | Drop the path and resume from the current position               |
| `EnterConsume`    | Resume by entering the path already computed                     |

| `RapidExecutionMode` | How far the program advances                                             |
| -------------------- | ------------------------------------------------------------------------ |
| `Continue`           | Run until something stops it                                             |
| `StepIn`             | Enter the routine called by the current instruction                      |
| `StepOver`           | Run the current instruction whole, without entering the routine it calls |
| `StepOut`            | Run until the current routine returns                                    |
| `StepBack`           | Step one instruction backwards                                           |
| `StepLast`           | Step to the last instruction                                             |
| `StepMotion`         | Step to the next motion instruction                                      |

`RapidStartCondition.CallChain` asks the controller to start only when the call chain of the program pointer is still valid, which is a way to refuse a start after the source was edited.

### Cycles and entry point

`SetExecutionCycle` takes `Once` or `Forever`, the other values of the enum are only reported by the controller. `StartFromProductionEntry` starts at the production entry point of the task instead of the current program pointer.

`AbortExecutionLevel` leaves the routine running now and goes back to the level under it. This is how a trap or a service routine started by hand is abandoned without stopping the program below it.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class RapidExecutionCycles
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        robot.Rws.Mastership.Request(MastershipDomain.Rapid);
        try
        {
            // Only Once and Forever are accepted here
            robot.Rws.Rapid.SetExecutionCycle(RapidExecutionCycle.Once);

            // Start from the production entry point instead of the current program pointer
            robot.Rws.Rapid.StartFromProductionEntry();

            // Leave the routine that is running now and go back to the level below it.
            // This is how a trap or a service routine is abandoned without stopping the program under it.
            robot.Rws.Rapid.AbortExecutionLevel("T_ROB1");
        }
        finally
        {
            robot.Rws.Mastership.Release(MastershipDomain.Rapid);
        }

        robot.Disconnect();
    }
}
```

### Stop

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class RapidStopProgram
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // Stop at the end of the current instruction, normal tasks only
        robot.Rws.Rapid.Stop(RapidStopMode.Stop, RapidTaskScope.Normal);

        // Let the robot finish the cycle it is in, then stop
        robot.Rws.Rapid.Stop(RapidStopMode.Cycle, RapidTaskScope.Normal);

        // Stop everything at once, including the static and semi static tasks
        robot.Rws.Rapid.Stop(RapidStopMode.QuickStop, RapidTaskScope.AllTasks);

        // Wait until the controller confirms the program is stopped
        while (robot.Rws.Rapid.GetExecutionState().State != RapidExecutionState.Stopped)
            System.Threading.Thread.Sleep(200);

        robot.Disconnect();
    }
}
```

| `RapidStopMode` | How the program stops                              |
| --------------- | -------------------------------------------------- |
| `Cycle`         | At the end of the current cycle                    |
| `Instruction`   | At the end of the current instruction              |
| `Stop`          | As soon as the robot can decelerate along its path |
| `QuickStop`     | As fast as the robot can, leaving the path         |

`RapidTaskScope.Normal` stops the normal tasks only, `AllTasks` also stops the static and semi static ones. `Stop` returns before the robot has stopped, so wait until `GetExecutionState` reports `Stopped`.

### Hold-to-run

In manual mode the program only runs while a client keeps saying that the hold-to-run control is held. Send `Press`, then `Held` about every two seconds. The controller stops the program as soon as it stops hearing from your application.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class RapidHoldToRun
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // Manual mode only. Press, then keep sending Held, the controller stops the
        // program as soon as it stops hearing from your application.
        robot.Rws.Rapid.SetHoldToRun(RapidHoldToRunState.Press);

        robot.Rws.Rapid.Start(RapidRegainMode.Continue, RapidExecutionMode.Continue);

        for (int i = 0; i < 10; i++)
        {
            robot.Rws.Rapid.SetHoldToRun(RapidHoldToRunState.Held);
            System.Threading.Thread.Sleep(1000);
        }

        robot.Rws.Rapid.SetHoldToRun(RapidHoldToRunState.Release);

        robot.Disconnect();
    }
}
```

This is only honoured by a virtual controller, and only for a client the controller considers local. A real cabinet expects the physical device.

A complete example, with the checks around it, is given in [Start & stop a RAPID program](start-stop-rapid-program.md).

**Methods of RapidService** ([reference](../api/UnderAutomation.ABB.Rws.Services.md#rapidservice-robotrwsrapid))

- `void AbortExecutionLevel(string task)`: Abandons the routine the task is currently running and returns to the level below it (synchronous) This is how a trap or a service routine started by hand is left without stopping the program underneath it.
  - async: `Task AbortExecutionLevelAsync(string task, CancellationToken cancellationToken = default)`
- `RapidExecutionInfo GetExecutionState()`: Gets whether the controller is executing RAPID code, and how many cycles it is set to run (synchronous)
  - async: `Task<RapidExecutionInfo> GetExecutionStateAsync(CancellationToken cancellationToken = default)`
- `void ResetProgramPointer()`: Moves the program pointer of every task back to the entry point of its program (synchronous)
  - async: `Task ResetProgramPointerAsync(CancellationToken cancellationToken = default)`
- `void SetExecutionCycle(RapidExecutionCycle cycle)`: Sets how many times the program runs before stopping (synchronous)
  - async: `Task SetExecutionCycleAsync(RapidExecutionCycle cycle, CancellationToken cancellationToken = default)`
- `void SetHoldToRun(RapidHoldToRunState state)`: Drives the hold-to-run control that lets the program run in manual mode (synchronous) Send RapidHoldToRunState.Press to allow execution to start, then RapidHoldToRunState.Held about every two seconds to keep it running; the controller stops the program as soon as it stops hearing from the client....
  - async: `Task SetHoldToRunAsync(RapidHoldToRunState state, CancellationToken cancellationToken = default)`
- `void Start(RapidRegainMode regain = RapidRegainMode.Continue, RapidExecutionMode executionMode = RapidExecutionMode.Continue, RapidExecutionCycle cycle = RapidExecutionCycle.Forever, RapidStartCondition condition = RapidStartCondition.None, bool stopAtBreakpoint = false, bool allTasksBySelection = false)`: Starts executing the RAPID program from where the program pointer stands (synchronous) The controller has to be in automatic mode with the motors on, or in manual mode with the enabling device held. Reset the program pointer first with RapidService.ResetProgramPointer to start from the beginning.
  - async: `Task StartAsync(RapidRegainMode regain = RapidRegainMode.Continue, RapidExecutionMode executionMode = RapidExecutionMode.Continue, RapidExecutionCycle cycle = RapidExecutionCycle.Forever, RapidStartCondition condition = RapidStartCondition.None, bool stopAtBreakpoint = false, bool allTasksBySelection = false, CancellationToken cancellationToken = default)`
- `void StartFromProductionEntry()`: Starts executing from the production entry point of the program rather than from where the program pointer stands (synchronous)
  - async: `Task StartFromProductionEntryAsync(CancellationToken cancellationToken = default)`
- `void StartSpy(string logFile)`: Starts recording the RAPID execution trace into a file (synchronous) The trace names every instruction the controller runs, which is what it takes to find out why a program took a branch it should not have.
  - async: `Task StartSpyAsync(string logFile, CancellationToken cancellationToken = default)`
- `void Stop(RapidStopMode stopMode = RapidStopMode.Stop, RapidTaskScope scope = RapidTaskScope.Normal)`: Stops the RAPID execution (synchronous)
  - async: `Task StopAsync(RapidStopMode stopMode = RapidStopMode.Stop, RapidTaskScope scope = RapidTaskScope.Normal, CancellationToken cancellationToken = default)`
- `void StopSpy()`: Stops recording the RAPID execution trace (synchronous)
  - async: `Task StopSpyAsync(CancellationToken cancellationToken = default)`

**RapidExecutionInfo** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidexecutioninfo))

- `RapidExecutionInfo()`: Initializes a new instance of the Data.RapidExecutionInfo class
- `RapidExecutionCycle Cycle { get; set; }`: Number of cycles the program is set to run
- `RapidExecutionState State { get; set; }`: Whether RAPID code is currently running

**RapidExecutionState** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidexecutionstate))

- Running: RAPID execution is running
- Stopped: RAPID execution is stopped
- Unknown: The controller reported a state this library does not know

**RapidExecutionCycle** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidexecutioncycle))

- AsIs: The cycle currently configured is left untouched
- Forever: The program runs again every time it reaches its end
- Once: The program runs once and stops at its end
- OnceDone: The program was asked to run once and has finished doing so
- Unknown: The controller reported a cycle this library does not know

**RapidExecutionMode** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidexecutionmode))

- Continue: Run until something stops it
- StepBack: Step one instruction backwards
- StepIn: Step into the routine called by the current instruction
- StepLast: Step to the last instruction
- StepMotion: Step to the next motion instruction
- StepOut: Run until the current routine returns
- StepOver: Run the current instruction whole, without entering the routine it calls

**RapidRegainMode** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidregainmode))

- Clear: Drop the path and resume from the current position
- Continue: Resume from the current position without moving back to the path
- EnterConsume: Resume by entering the consumption of the already generated path
- Regain: Move back onto the path before resuming

**RapidStopMode** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidstopmode))

- Cycle: Stop when the current cycle ends
- Instruction: Stop when the current instruction ends
- QuickStop: Stop as fast as the robot can, leaving the path
- Stop: Stop as soon as the robot can decelerate along its path

**RapidStartCondition** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidstartcondition))

- CallChain: Start only when the call chain of the program pointer is still valid
- None: Start without any additional check

**RapidTaskScope** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidtaskscope))

- AllTasks: Apply to every task of the system
- Normal: Apply to the tasks the task selection panel has enabled

**RapidHoldToRunState** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidholdtorunstate))

- Held: Confirm that execution may keep running, which has to be repeated about every two seconds
- Press: Ask for execution to be allowed to start
- Release: Stop execution immediately

## Execution trace

The controller can write every instruction it runs into a file. It is the fastest way to find out why a program took a branch it should not have. The two calls take the mastership by themselves, your code does not have to.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class RapidSpy
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // The trace names every instruction the controller runs. No mastership needed,
        // the controller takes it by itself for these two calls.
        robot.Rws.Rapid.StartSpy("$HOME/trace.log");

        Console.WriteLine(robot.Rws.Rapid.GetSpyStatus());   // Logging or NotLogging

        System.Threading.Thread.Sleep(5000);

        robot.Rws.Rapid.StopSpy();

        // Then download the file with the file service
        string trace = robot.Rws.File.GetFileAsText("$HOME/trace.log");
        Console.WriteLine(trace);

        robot.Disconnect();
    }
}
```

The file is written on the controller, download it afterwards with the [file system service](rws-files.md). A trace grows fast, do not leave it running.

**Methods of RapidService** ([reference](../api/UnderAutomation.ABB.Rws.Services.md#rapidservice-robotrwsrapid))

- `RapidSpyStatus GetSpyStatus()`: Gets whether the controller is recording the RAPID execution trace to a file (synchronous)
  - async: `Task<RapidSpyStatus> GetSpyStatusAsync(CancellationToken cancellationToken = default)`

**RapidSpyStatus** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidspystatus))

- Logging: The execution trace is being written
- NotLogging: No execution trace is being written
- Unknown: The controller reported a status this library does not know

## Program pointer and motion pointer

Each task has two pointers. The program pointer says which instruction runs next, the motion pointer which one the robot is really executing. They drift apart because the controller plans the path ahead of the movement.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class RapidProgramPointer
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // Where the two pointers of the task stand
        RapidPointers pointers = robot.Rws.Rapid.GetPointers("T_ROB1");

        if (pointers.ProgramPointer.Available)
        {
            Console.WriteLine(pointers.ProgramPointer.Module + "/" + pointers.ProgramPointer.Routine);
            Console.WriteLine(pointers.ProgramPointer.BeginRow + "," + pointers.ProgramPointer.BeginColumn);
        }

        // The motion pointer is behind the program pointer, the controller plans the path
        // ahead of the movement. It is not available in a task that has not moved yet.
        Console.WriteLine(pointers.MotionPointer.Available);

        // The piece of source the program pointer covers. The controller refuses the request
        // when the task has no program pointer, reset it or start the program first.
        RapidProgramCounterPosition position = robot.Rws.Rapid.GetProgramCounterPosition("T_ROB1");
        Console.WriteLine(position.Module + " " + position.StartLine + "," + position.StartColumn);

        // Moving the pointer is a write, it needs the RAPID mastership
        robot.Rws.Mastership.Request(MastershipDomain.Rapid);
        try
        {
            // To the beginning of a routine. The module name is used by an IRC5 only,
            // an OmniCore looks the routine up in the whole task.
            robot.Rws.Rapid.SetProgramPointerToRoutine("T_ROB1", "MainModule", "main");

            // To a service routine, which has to be entered at user level
            robot.Rws.Rapid.SetProgramPointerToRoutineUrl("T_ROB1", "RAPID/T_ROB1/BASEFUN/LoadIdentify", true);

            // To one position of the source. The routine name is used by an IRC5 only,
            // an OmniCore works it out from the position itself.
            robot.Rws.Rapid.SetProgramPointerToCursor("T_ROB1", "MainModule", "main", 12, 1);

            // One instruction forward or backward, automatic mode only
            robot.Rws.Rapid.SetProgramPointerToNextInstruction("T_ROB1");
            robot.Rws.Rapid.SetProgramPointerToPreviousInstruction("T_ROB1");
        }
        finally
        {
            robot.Rws.Mastership.Release(MastershipDomain.Rapid);
        }

        robot.Disconnect();
    }
}
```

> **Available on** RWS 1.0 (IRC5) : yes | RWS 2.0 (OmniCore) : yes. An IRC5 needs the module and the routine name, an OmniCore works them out from the position alone.

`SetProgramPointerToRoutine` takes a module name and `SetProgramPointerToCursor` a routine name. An IRC5 refuses the request without them, an OmniCore ignores them and finds the routine by itself. Pass them in both cases, your code then works on the two generations.

A few things to know before moving the pointer:

- Moving the pointer needs the `Rapid` [mastership](rws-mastership.md), and the program has to be stopped.
- `SetProgramPointerToNextInstruction` and `SetProgramPointerToPreviousInstruction` are refused outside automatic mode.
- A service routine has to be entered at user level, so pass `true` for `userLevel`. `GetServiceRoutines` gives the paths `SetProgramPointerToRoutineUrl` takes.
- `GetProgramCounterPosition` is refused when the task has no program pointer at all. Reset it or start the program first.
- `GetProgram` returns the name of the program the task holds and the routine `ResetProgramPointer` goes back to.

### Synchronization and change counters

`GetProgramPointerSyncState` and `GetMotionPointerSyncState` say whether the pointers of the tasks are synchronized with each other, for the whole controller or for one task. `GetStructuralChangeCount` returns two counters that only move when something changed in the task, which is cheaper than downloading the modules again to find out that nothing moved.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class RapidPointerSync
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // For the whole controller
        RapidPointerSyncState program = robot.Rws.Rapid.GetProgramPointerSyncState();
        RapidPointerSyncState motion = robot.Rws.Rapid.GetMotionPointerSyncState();
        Console.WriteLine(program + " / " + motion);   // On or Off

        // For one task
        Console.WriteLine(robot.Rws.Rapid.GetTaskProgramPointerSyncState("T_ROB1"));
        Console.WriteLine(robot.Rws.Rapid.GetTaskMotionPointerSyncState("T_ROB1"));

        // Two counters that say whether anything changed in the task, cheaper than
        // downloading the modules again to find out that nothing moved
        RapidStructuralChangeCount counters = robot.Rws.Rapid.GetStructuralChangeCount("T_ROB1");
        Console.WriteLine(counters.ChangeCount);
        Console.WriteLine(counters.StructuralChangeCount);

        robot.Disconnect();
    }
}
```

**Methods of RapidService** ([reference](../api/UnderAutomation.ABB.Rws.Services.md#rapidservice-robotrwsrapid))

- `RapidPointerSyncState GetMotionPointerSyncState()`: Gets whether the motion pointers of every task are synchronized with each other (synchronous)
  - async: `Task<RapidPointerSyncState> GetMotionPointerSyncStateAsync(CancellationToken cancellationToken = default)`
- `RapidPointers GetPointers(string task)`: Gets where the program pointer and the motion pointer of a task stand (synchronous) The program pointer says which instruction runs next, the motion pointer which one the robot is actually executing; they drift apart because the controller plans the path ahead of the movement.
  - async: `Task<RapidPointers> GetPointersAsync(string task, CancellationToken cancellationToken = default)`
- `RapidProgramInfo GetProgram(string task)`: Gets the program loaded into a task (synchronous)
  - async: `Task<RapidProgramInfo> GetProgramAsync(string task, CancellationToken cancellationToken = default)`
- `RapidProgramCounterPosition GetProgramCounterPosition(string task)`: Gets which piece of source the program pointer of a task points at (synchronous)
  - async: `Task<RapidProgramCounterPosition> GetProgramCounterPositionAsync(string task, CancellationToken cancellationToken = default)`
- `RapidPointerSyncState GetProgramPointerSyncState()`: Gets whether the program pointers of every task are synchronized with each other (synchronous)
  - async: `Task<RapidPointerSyncState> GetProgramPointerSyncStateAsync(CancellationToken cancellationToken = default)`
- `RapidStructuralChangeCount GetStructuralChangeCount(string task)`: Gets the two counters a task keeps of what has changed in it (synchronous) Comparing them with what a previous reading gave is cheaper than fetching the modules again to find out that nothing moved.
  - async: `Task<RapidStructuralChangeCount> GetStructuralChangeCountAsync(string task, CancellationToken cancellationToken = default)`
- `void SetProgramPointerToCursor(string task, string module, string routine, int row, int column)`: Moves the program pointer of a task to a position of a module (synchronous)
  - async: `Task SetProgramPointerToCursorAsync(string task, string module, string routine, int row, int column, CancellationToken cancellationToken = default)`
- `void SetProgramPointerToNextInstruction(string task)`: Moves the program pointer of a task forward by one instruction (synchronous)
  - async: `Task SetProgramPointerToNextInstructionAsync(string task, CancellationToken cancellationToken = default)`
- `void SetProgramPointerToPreviousInstruction(string task)`: Moves the program pointer of a task back by one instruction (synchronous)
  - async: `Task SetProgramPointerToPreviousInstructionAsync(string task, CancellationToken cancellationToken = default)`
- `void SetProgramPointerToRoutine(string task, string module, string routine, bool userLevel = false)`: Moves the program pointer of a task to the beginning of a routine (synchronous)
  - async: `Task SetProgramPointerToRoutineAsync(string task, string module, string routine, bool userLevel = false, CancellationToken cancellationToken = default)`
- `void SetProgramPointerToRoutineUrl(string task, string routineUrl, bool userLevel = false)`: Moves the program pointer of a task to a routine named by its path (synchronous) This is what the paths GetServiceRoutines() reports are for.
  - async: `Task SetProgramPointerToRoutineUrlAsync(string task, string routineUrl, bool userLevel = false, CancellationToken cancellationToken = default)`

**RapidPointers** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidpointers))

- `RapidPointers()`: Initializes a new instance of the Data.RapidPointers class
- `RapidPointerPosition MotionPointer { get; set; }`: Instruction the robot is currently moving for
- `RapidPointerPosition ProgramPointer { get; set; }`: Instruction the task will execute next

**RapidPointerPosition** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidpointerposition))

- `RapidPointerPosition()`: Initializes a new instance of the Data.RapidPointerPosition class
- `bool Available { get; set; }`: Whether the controller reported a position for this pointer at all
- `int? BeginColumn { get; set; }`: Column the pointer begins at, null when the controller did not report it
- `int? BeginRow { get; set; }`: Line the pointer begins at, null when the controller did not report it
- `int? ChangeCount { get; set; }`: How many times the pointer has been moved, null when the controller did not report it
- `int? EndColumn { get; set; }`: Column the pointer ends at, null when the controller did not report it
- `int? EndRow { get; set; }`: Line the pointer ends at, null when the controller did not report it
- `RapidExecutionType ExecutionType { get; set; }`: What kind of code the pointer is standing in
- `string Module { get; set; }`: Name of the module the pointer stands in
- `string Routine { get; set; }`: Name of the routine the pointer stands in

**RapidProgramCounterPosition** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidprogramcounterposition))

- `RapidProgramCounterPosition()`: Initializes a new instance of the Data.RapidProgramCounterPosition class
- `int? EndColumn { get; set; }`: Column the pointed instruction ends at, null when the controller did not report it
- `int? EndLine { get; set; }`: Line the pointed instruction ends at, null when the controller did not report it
- `string Module { get; set; }`: Name of the module the pointer stands in
- `string Routine { get; set; }`: Name of the routine the pointer stands in
- `int? StartColumn { get; set; }`: Column the pointed instruction starts at, null when the controller did not report it
- `int? StartLine { get; set; }`: Line the pointed instruction starts at, null when the controller did not report it

**RapidPointerSyncState** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidpointersyncstate))

- Off: The pointers are not synchronized
- On: The pointers are synchronized
- Unknown: The controller reported a state this library does not know

**RapidStructuralChangeCount** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidstructuralchangecount))

- `RapidStructuralChangeCount()`: Initializes a new instance of the Data.RapidStructuralChangeCount class
- `int? ChangeCount { get; set; }`: Counter the controller increments whenever anything relevant changes in the task
- `int? StructuralChangeCount { get; set; }`: Counter the controller increments when a module is loaded, unloaded or renamed. A rename counts as an unload followed by a load.

**RapidExecutionType** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidexecutiontype))

- EventRoutine: An event routine is running
- ExternalInterrupt: An external interrupt is running
- Interrupt: An interrupt is running
- None: Nothing is running
- Normal: The normal program is running
- Unknown: The controller reported a type this library does not know
- UserRoutine: A user routine is running

## Call stack

`GetActivationRecord` reads one frame of the call stack. Frame 1 holds the program pointer, and the number grows towards the entry point of the program. The controller refuses the request when the task has no program pointer, or when the stack is not that deep.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class RapidCallStack
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // Frame 1 is the one holding the program pointer, the number grows towards the entry point
        for (int frame = 1; frame <= 5; frame++)
        {
            RapidActivationRecord record = robot.Rws.Rapid.GetActivationRecord("T_ROB1", frame);

            Console.WriteLine(record.RoutineUrl);
            Console.WriteLine(record.BeginRow + "," + record.BeginColumn);
            Console.WriteLine(record.ExecutionLevel);
        }

        // The routines the program pointer may be moved to, service routines included
        foreach (RapidServiceRoutineItem routine in robot.Rws.Rapid.GetServiceRoutines("T_ROB1"))
        {
            Console.WriteLine(routine.Name + " -> " + routine.Url + " service=" + routine.IsServiceRoutine);
        }

        robot.Disconnect();
    }
}
```

| `RapidExecutionLevel` | Where execution stands                                  |
| --------------------- | ------------------------------------------------------- |
| `Normal`              | In the program itself                                   |
| `Trap`                | In a trap routine                                       |
| `User`                | In a routine started by hand, such as a service routine |
| `None`                | Nothing is running at this level                        |
| `Unknown`             | The controller reported a level the SDK does not know   |

**Methods of RapidService** ([reference](../api/UnderAutomation.ABB.Rws.Services.md#rapidservice-robotrwsrapid))

- `RapidActivationRecord GetActivationRecord(string task, int stackFrame = 1)`: Gets one frame of the call stack of a task: which routine is running and where execution stands in it (synchronous)
  - async: `Task<RapidActivationRecord> GetActivationRecordAsync(string task, int stackFrame = 1, CancellationToken cancellationToken = default)`
- `RapidServiceRoutineItem[] GetServiceRoutines(string task, int? start = null, int? limit = null)`: Gets the routines of a task the program pointer can be moved to (synchronous)
  - async: `Task<RapidServiceRoutineItem[]> GetServiceRoutinesAsync(string task, int? start = null, int? limit = null, CancellationToken cancellationToken = default)`

**RapidActivationRecord** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidactivationrecord))

- `RapidActivationRecord()`: Initializes a new instance of the Data.RapidActivationRecord class
- `int? BeginColumn { get; set; }`: Column the executing statement starts at, null when the controller did not report it
- `int? BeginRow { get; set; }`: Line the executing statement starts at, null when the controller did not report it
- `int? EndColumn { get; set; }`: Column the executing statement ends at, null when the controller did not report it
- `int? EndRow { get; set; }`: Line the executing statement ends at, null when the controller did not report it
- `RapidExecutionLevel ExecutionLevel { get; set; }`: Level at which this frame is executing
- `string RoutineUrl { get; set; }`: Path of the routine this frame is executing
- `string StackUrl { get; set; }`: Path identifying this stack frame, which the UI instruction resources also take

**RapidServiceRoutineItem** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidserviceroutineitem))

- `RapidServiceRoutineItem()`: Initializes a new instance of the Data.RapidServiceRoutineItem class
- `bool? IsServiceRoutine { get; set; }`: Whether this is a service routine rather than an ordinary one, null when the controller did not report it
- `string Name { get; set; }`: Name of the routine, for example "LoadIdentify"
- `string Url { get; set; }`: Path of the routine, which RapidService.SetProgramPointerToRoutineUrl() takes

**RapidExecutionLevel** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidexecutionlevel))

- None: Nothing is executing
- Normal: The normal user code is executing
- Trap: A trap routine is executing
- Unknown: The controller reported a level this library does not know
- User: A user routine is executing

## Answer an operator dialogue

A RAPID program can stop and ask the operator something. The controller then reports one pending instruction, and the program waits until it is answered. `GetActiveUiInstruction` returns `null` when nothing is pending.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class RapidUiInstructions
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // Null when the program is not asking the operator for anything right now
        RapidUiInstruction question = robot.Rws.Rapid.GetActiveUiInstruction();

        if (question != null)
        {
            Console.WriteLine(question.Instruction);   // name of the RAPID instruction waiting
            Console.WriteLine(question.Message);
            Console.WriteLine(question.Event);         // Send, Post or Abort

            // What the program passed in, and what it is waiting for. The names of the
            // parameters depend on the instruction, so read them before writing one.
            foreach (RapidUiInstructionParameter parameter in
                     robot.Rws.Rapid.GetUiInstructionParameters(question.StackUrl))
            {
                Console.WriteLine(parameter.Name + " = " + parameter.Value);
            }

            // Answering is a write, so it needs the mastership
            robot.Rws.Mastership.Request(MastershipDomain.Rapid);
            try
            {
                // Write the parameter carrying the answer, then the one marking it as completed
                robot.Rws.Rapid.SetUiInstructionParameter(question.StackUrl, "TPCompleted", "TRUE");
            }
            finally
            {
                robot.Rws.Mastership.Release(MastershipDomain.Rapid);
            }

            Console.WriteLine(robot.Rws.Rapid.GetUiInstructionParameter(question.StackUrl, "TPCompleted"));
        }

        robot.Disconnect();
    }
}
```

The names of the parameters depend on the instruction the program used, so read them with `GetUiInstructionParameters` before writing one. The answer is written first, then the parameter marking the dialogue as completed. Writing a parameter needs the `Rapid` mastership, and fails when the instruction is no longer pending.

**Methods of RapidService** ([reference](../api/UnderAutomation.ABB.Rws.Services.md#rapidservice-robotrwsrapid))

- `RapidUiInstruction GetActiveUiInstruction()`: Gets the dialogue a running RAPID program is currently asking an operator for (synchronous) Answering it means writing its parameters with String%2cSystem.String), addressed by the path this returns.
  - async: `Task<RapidUiInstruction> GetActiveUiInstructionAsync(CancellationToken cancellationToken = default)`
- `string GetUiInstructionParameter(string stackUrl, string parameter)`: Gets the value of one parameter of a pending UI instruction (synchronous)
  - async: `Task<string> GetUiInstructionParameterAsync(string stackUrl, string parameter, CancellationToken cancellationToken = default)`
- `RapidUiInstructionParameter[] GetUiInstructionParameters(string stackUrl)`: Gets every parameter of a pending UI instruction: what the program passed in, and what it is waiting for (synchronous)
  - async: `Task<RapidUiInstructionParameter[]> GetUiInstructionParametersAsync(string stackUrl, CancellationToken cancellationToken = default)`
- `void SetUiInstructionParameter(string stackUrl, string parameter, string value)`: Answers a pending UI instruction by writing one of its parameters (synchronous) An instruction is normally answered by writing the parameter carrying the answer and then the one marking it as completed.
  - async: `Task SetUiInstructionParameterAsync(string stackUrl, string parameter, string value, CancellationToken cancellationToken = default)`

**RapidUiInstruction** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapiduiinstruction))

- `RapidUiInstruction()`: Initializes a new instance of the Data.RapidUiInstruction class
- `RapidUiInstructionEvent Event { get; set; }`: What the instruction is asking of the client
- `RapidExecutionLevel ExecutionLevel { get; set; }`: Level at which the instruction is executing
- `string Instruction { get; set; }`: Name of the RAPID instruction that opened the dialogue, for example "TPReadNum"
- `string Message { get; set; }`: Text the instruction displays
- `string StackUrl { get; set; }`: Path identifying the call, which the parameter methods take

**RapidUiInstructionParameter** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapiduiinstructionparameter))

- `RapidUiInstructionParameter()`: Initializes a new instance of the Data.RapidUiInstructionParameter class
- `string Name { get; set; }`: Name of the parameter, for example "TPCompleted"
- `string Value { get; set; }`: Value of the parameter, written the way RAPID writes it

**RapidUiInstructionEvent** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapiduiinstructionevent))

- Abort: The instruction has been abandoned and no answer is expected any more
- Post: The instruction only displays something and expects no answer
- Send: The instruction is waiting for an answer
- Unknown: The controller reported an event this library does not know

## Signals renamed by the program

A RAPID program can give another name to an I/O signal. `GetAliasIo` lists these names as long as the program declaring them is loaded. The signals themselves are read and written with the [I/O service](rws-io.md).

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class RapidAliasIo
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // The signals a loaded program gave another name to. Empty when no program declares any.
        foreach (RapidAliasIoItem alias in robot.Rws.Rapid.GetAliasIo())
        {
            Console.WriteLine(alias.AliasName + " -> " + alias.SignalName + " (" + alias.Type + ")");
        }

        robot.Disconnect();
    }
}
```

**Methods of RapidService** ([reference](../api/UnderAutomation.ABB.Rws.Services.md#rapidservice-robotrwsrapid))

- `RapidAliasIoItem[] GetAliasIo(int? start = null, int? limit = null)`: Gets the I/O signals a running RAPID program has given an alias to (synchronous)
  - async: `Task<RapidAliasIoItem[]> GetAliasIoAsync(int? start = null, int? limit = null, CancellationToken cancellationToken = default)`

**RapidAliasIoItem** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidaliasioitem))

- `RapidAliasIoItem()`: Initializes a new instance of the Data.RapidAliasIoItem class
- `string AliasName { get; set; }`: Name the RAPID program refers to the signal by
- `string SignalName { get; set; }`: Name of the I/O signal the alias points at
- `IoSignalType Type { get; set; }`: Type of the aliased signal

## Position of the robot

The position of the robot, its mechanical units and the external axes of a task are read from the [motion system service](rws-motion.md).

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).
