# Start & stop a RAPID program

Start, stop and reset a RAPID program remotely: motors on, program pointer, execution cycle, and how to check that it really started.

Web page: https://underautomation.com/abb/documentation/start-stop-rapid-program

Starting a RAPID program from C# is `robot.Rws.Rapid.Start(...)`, and stopping it is `robot.Rws.Rapid.Stop(...)`. The call itself is one line. What takes the time is the state the controller has to be in before it accepts to start, and checking afterwards that the program really runs.

> **Available on** RWS 1.0 (IRC5) : yes | RWS 2.0 (OmniCore) : yes.

## What the controller needs before it starts

A start that fails with the HTTP status code 500 almost always means one of these is missing.

| Condition                  | How to get there                                                                 |
| -------------------------- | -------------------------------------------------------------------------------- |
| Automatic mode             | turn the key on the controller, `Panel.GetOperationMode()` tells you where it is |
| Motors on                  | `Panel.SetControllerState(ControllerState.MotorsOn)`                             |
| RAPID mastership           | `Mastership.Request(MastershipDomain.Rapid)`                                     |
| A program loaded and built | `Rapid.GetTask("T_ROB1").TaskState` is `Linked`                                  |
| A program pointer          | `Rapid.ResetProgramPointer()`, or move it where you want                         |

In manual mode a program can also be started, but the operator has to hold the enabling device of the teach pendant. A remote start in manual mode is refused as soon as they release it.

## Operation mode

The mode is set with the physical key, it cannot be changed over the network. What you can do is read it, and acknowledge a change the operator has requested.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class PanelOperationMode
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        OperationMode mode = robot.Rws.Panel.GetOperationMode();

        switch (mode)
        {
            case OperationMode.Automatic:
                Console.WriteLine("Automatic mode, a program can be started remotely");
                break;

            case OperationMode.ManualReducedSpeed:
            case OperationMode.ManualFullSpeed:
                Console.WriteLine("Manual mode, the operator holds the enabling device");
                break;

            case OperationMode.AutomaticChangeRequest:
                // The key was turned to automatic, the change waits for a confirmation
                robot.Rws.Panel.AcknowledgeOperationMode(OperationModeAcknowledgement.Automatic);
                break;

            case OperationMode.ManualFullSpeedChangeRequest:
                robot.Rws.Panel.AcknowledgeOperationMode(OperationModeAcknowledgement.ManualFullSpeed);
                break;
        }

        robot.Disconnect();
    }
}
```

## Motors on

The state change is not immediate. Ask for it, then wait until the controller reports it.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class PanelMotors
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        ControllerState state = robot.Rws.Panel.GetControllerState();
        Console.WriteLine($"Controller state : {state}");

        if (state == ControllerState.MotorsOff)
        {
            // The robot can move once the motors are on
            robot.Rws.Panel.SetControllerState(ControllerState.MotorsOn);
        }

        // The state change is not immediate, wait for the controller to report it
        while (robot.Rws.Panel.GetControllerState() != ControllerState.MotorsOn)
        {
            Thread.Sleep(200);
        }

        // Motors off puts the robot back in standby, it cannot move any more
        robot.Rws.Panel.SetControllerState(ControllerState.MotorsOff);

        robot.Disconnect();
    }
}
```

## The program pointer

The program starts from where the program pointer stands, not from the beginning. `ResetProgramPointer()` puts the pointer of every task back on its entry point, usually `main`. To start somewhere else, move the pointer to a routine or to a position in the source.

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

## Start

`Start` takes six arguments. The defaults suit a normal production start: resume the path, run continuously, forever, on the normal tasks only.

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

| Argument              | What it decides                                                                              |
| --------------------- | -------------------------------------------------------------------------------------------- |
| `regain`              | what the robot does about the distance between where it stands and where the path expects it |
| `executionMode`       | how far the program advances before stopping again, `Continue` or one of the step modes      |
| `cycle`               | `Forever`, or `Once` for a single cycle                                                      |
| `condition`           | `CallChain` makes the controller check the call chain before starting                        |
| `stopAtBreakpoint`    | whether execution stops on the breakpoints of the program                                    |
| `allTasksBySelection` | start every task enabled in the selection panel, not only the normal tasks                   |

## Check that it really started

`Start` returns as soon as the controller accepted the request. It does not mean the program runs: the controller can still refuse it, or stop it on the first error. Poll the execution state until it reports `Running`, with a timeout.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class HowToWaitRapidStarted
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // Start returns as soon as the controller accepted the request. It does not mean the
        // program runs : the controller can still refuse it, or stop it on the first error.
        robot.Rws.Mastership.Request(MastershipDomain.Rapid);
        try
        {
            robot.Rws.Rapid.Start(RapidRegainMode.Continue, RapidExecutionMode.Continue,
                                  RapidExecutionCycle.Forever, RapidStartCondition.None, false, false);
        }
        finally
        {
            robot.Rws.Mastership.Release(MastershipDomain.Rapid);
        }

        if (!WaitRunning(robot, 5000))
            throw new Exception("The program did not start, look at the event log of the controller");

        // The task that drives the robot has its own state, more precise than the global one
        RapidTaskInfo task = robot.Rws.Rapid.GetTask("T_ROB1");
        Console.WriteLine(task.ExecutionState);     // Started
        Console.WriteLine(task.ExecutionType);      // what kind of code is running now

        // Where the program pointer stands, so you can tell a running program from a blocked one
        RapidPointers pointers = robot.Rws.Rapid.GetPointers("T_ROB1");
        Console.WriteLine(pointers.ProgramPointer);

        robot.Disconnect();
    }

    // Polls the execution state until the program runs, or the timeout expires
    static bool WaitRunning(AbbController robot, int timeoutMs)
    {
        DateTime limit = DateTime.UtcNow.AddMilliseconds(timeoutMs);

        while (DateTime.UtcNow < limit)
        {
            if (robot.Rws.Rapid.GetExecutionState().State == RapidExecutionState.Running)
                return true;

            Thread.Sleep(200);
        }

        return false;
    }
}
```

`GetExecutionState()` covers the whole controller. `GetTask("T_ROB1")` is more precise, it gives the state, the execution level and the kind of code each task is running.

## Run once instead of forever

The number of cycles can also be set before starting, and read back per task.

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

## Stop

`Stop` takes a stop mode and a scope. Stopping needs no mastership.

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

| `RapidStopMode` | Effect                                     |
| --------------- | ------------------------------------------ |
| `Cycle`         | finish the current cycle, then stop        |
| `Instruction`   | finish the current instruction, then stop  |
| `Stop`          | stop at the end of the current instruction |
| `QuickStop`     | stop as fast as the program allows         |

`RapidTaskScope.Normal` stops the normal tasks. `AllTasks` also stops the static and semi static tasks, which usually run all the time and are not meant to be stopped by an application.

A stop is not an emergency stop. The emergency stop is a hardware circuit, it is not something an application on the network can trigger.

## Going further

- [RAPID tasks & program execution](rws-rapid-tasks.md), the complete reference
- [Control panel & operation mode](rws-panel.md)
- [Mastership](rws-mastership.md)
- [Read & write RAPID variables](read-write-rapid-variables.md), to pass parameters to the program before starting it

**Methods of RapidService** ([reference](../api/UnderAutomation.ABB.Rws.Services.md#rapidservice-robotrwsrapid))

- `void AbortExecutionLevel(string task)`: Abandons the routine the task is currently running and returns to the level below it (synchronous) This is how a trap or a service routine started by hand is left without stopping the program underneath it.
  - async: `Task AbortExecutionLevelAsync(string task, CancellationToken cancellationToken = default)`
- `RapidExecutionInfo GetExecutionState()`: Gets whether the controller is executing RAPID code, and how many cycles it is set to run (synchronous)
  - async: `Task<RapidExecutionInfo> GetExecutionStateAsync(CancellationToken cancellationToken = default)`
- `void SetExecutionCycle(RapidExecutionCycle cycle)`: Sets how many times the program runs before stopping (synchronous)
  - async: `Task SetExecutionCycleAsync(RapidExecutionCycle cycle, CancellationToken cancellationToken = default)`

**RapidExecutionInfo** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidexecutioninfo))

- `RapidExecutionInfo()`: Initializes a new instance of the Data.RapidExecutionInfo class
- `RapidExecutionCycle Cycle { get; set; }`: Number of cycles the program is set to run
- `RapidExecutionState State { get; set; }`: Whether RAPID code is currently running

**RapidExecutionCycle** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidexecutioncycle))

- AsIs: The cycle currently configured is left untouched
- Forever: The program runs again every time it reaches its end
- Once: The program runs once and stops at its end
- OnceDone: The program was asked to run once and has finished doing so
- Unknown: The controller reported a cycle this library does not know

**RapidStopMode** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#rapidstopmode))

- Cycle: Stop when the current cycle ends
- Instruction: Stop when the current instruction ends
- QuickStop: Stop as fast as the robot can, leaving the path
- Stop: Stop as soon as the robot can decelerate along its path

**ControllerState** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#controllerstate))

- EmergencyStop: The robot is stopped because the emergency stop was activated
- EmergencyStopReset: The robot is ready to leave the emergency stop state: the emergency stop is no longer activated, but the state transition is not confirmed yet.
- GuardStop: The robot is stopped because the safety runchain is opened, for instance because a door of its cell is open
- Init: The robot is starting up. It will shift to ControllerState.MotorsOff once it has started.
- MotorsOff: The robot is in a standby state where there is no power to its motors. The state has to be shifted to ControllerState.MotorsOn before the robot can move.
- MotorsOn: The robot is ready to move, either by jogging or by running programs
- SystemFailure: The robot is in a system failure state and requires a restart
- Unknown: The state could not be determined
