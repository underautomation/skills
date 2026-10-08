# RAPID tasks & program execution

List RAPID tasks, start and stop program execution, follow the execution state, move the program pointer, load and unload modules.

Web page: https://underautomation.com/abb/documentation/rws-rapid-tasks

`robot.Rws.Rapid` is the service of the program the robot runs. This page covers the tasks the program is split into, starting and stopping the execution, and moving the program pointer. The variables of the program are on [RAPID variables & symbols](rws-rapid-symbols.md), the source of the modules on [RAPID modules & program files](rws-rapid-modules.md).

Reading never needs anything special. Every write of this page needs the `Rapid` [mastership](rws-mastership.md), and most of them also need the controller to be in the right operation mode. None of these resources answers while the controller runs in boot mode.

## Tasks

A controller runs one RAPID task per robot, plus the background tasks the system needs. `GetTasks` lists them all, `GetTask` returns everything the controller knows about one of them.

```python
from underautomation.abb.abb_controller import AbbController

robot = AbbController()
robot.connect("192.168.0.1")

# Every RAPID task of the controller
for task in robot.rws.rapid.get_tasks():
    print(task.name)             # T_ROB1
    print(task.type)             # Normal, Static or SemiStatic
    print(task.task_state)       # Linked when the program is ready to run
    print(task.execution_state)  # Started, Stopped, Ready
    print(task.active)           # None when the controller did not report it
    print(task.motion_task)      # True for the task that drives the robot

# Everything the controller knows about one task
info = robot.rws.rapid.get_task("T_ROB1")
print(info.execution_level)   # Normal, Trap, User, None
print(info.execution_cycle)   # Forever, Once, OnceDone
print(info.execution_mode)    # Continuous, StepIn, StepOver, ...
print(info.production_entry_point)
print(info.trust)

robot.disconnect()
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

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.mastership_domain import MastershipDomain

robot = AbbController()
robot.connect("192.168.0.1")

# Which tasks the operator panel has selected, and which of them an operator may change
for item in robot.rws.rapid.get_task_selection():
    print(f"{item.name} selected={item.selected} userModify={item.user_modify}")

# Activating or deactivating a task is a write, so it needs the mastership
robot.rws.mastership.request(MastershipDomain.Rapid)
try:
    robot.rws.rapid.activate_task("T_ROB1")
    robot.rws.rapid.deactivate_task("T_ROB2")

    # Same thing for every task at once
    robot.rws.rapid.activate_tasks()
    robot.rws.rapid.deactivate_tasks()
finally:
    robot.rws.mastership.release(MastershipDomain.Rapid)

robot.disconnect()
```

`GetTaskProgramPointerSyncState` and `GetTaskMotionPointerSyncState`, listed below, are described in the program pointer section of this page.



**RapidTaskItem** ([reference](../api/underautomation.abb.rws.data.md#rapidtaskitem))

- `RapidTaskItem()`: Initializes a new instance of the RapidTaskItem class
- `name: str`: Name of the task, for example "T_ROB1"
- `type: RapidTaskType`: Kind of task, which decides when the controller runs it
- `task_state: RapidTaskState`: How far the controller has got in preparing the program of the task
- `execution_state: RapidTaskExecutionState`: Whether the task is running, and whether it could be
- `active: bool | None`: Whether the task is active, null when the controller did not report it
- `motion_task: bool | None`: Whether the task can move a mechanical unit, null when the controller did not report it

**RapidTaskInfo** ([reference](../api/underautomation.abb.rws.data.md#rapidtaskinfo))

- `RapidTaskInfo()`: Initializes a new instance of the RapidTaskInfo class
- `trust: RapidTaskTrustLevel`: What the controller does to the system when this task stops unexpectedly
- `task_id: int | None`: Identifier of the task, null when the controller did not report it
- `execution_level: RapidExecutionLevel`: Level at which the code of the task is currently executing
- `execution_mode: RapidTaskExecutionMode`: Stepping mode the task was last started with
- `execution_type: RapidExecutionType`: What kind of code the task is currently running
- `execution_cycle: RapidExecutionCycle`: Number of cycles the task is set to run. Only reported over a connection established with version 2, and left to otherwise.
- `production_entry_point: str`: Routine the program pointer moves to when it is reset, for example "main"
- `bind_reference: bool | None`: Whether the task is bound to a configured task number, null when the controller did not report it
- `task_in_foreground: str`: Name of the task running in the foreground, empty when there is none
- Inherited from [RapidTaskItem](../api/underautomation.abb.rws.data.md#rapidtaskitem): `name`, `type`, `task_state`, `execution_state`, `active`, `motion_task`

**RapidTaskSelectionItem** ([reference](../api/underautomation.abb.rws.data.md#rapidtaskselectionitem))

- `RapidTaskSelectionItem()`: Initializes a new instance of the RapidTaskSelectionItem class
- `name: str`: Name of the task, for example "T_ROB1"
- `selected: bool | None`: Whether the task is selected, null when the controller did not report it
- `motion_task: bool | None`: Whether the task can move a mechanical unit, null when the controller did not report it
- `user_modify: bool | None`: Whether an operator is allowed to change the selection of this task, null when the controller did not report it

**RapidTaskType** ([reference](../api/underautomation.abb.rws.data.md#rapidtasktype))

- Unknown: The controller reported a type this library does not know
- Normal: A task started and stopped together with the program
- Static: A task that keeps its program pointer where it was when the controller was switched off
- SemiStatic: A task restarted from its beginning every time the controller starts

**RapidTaskState** ([reference](../api/underautomation.abb.rws.data.md#rapidtaskstate))

- Unknown: The controller reported a state this library does not know
- Empty: The task holds no program
- Initiated: The task has been created but its program is not linked yet
- Linked: The program of the task is linked and ready to run
- Loaded: A program is loaded into the task but not linked yet
- Uninitialized: The task is not initialized

**RapidTaskExecutionState** ([reference](../api/underautomation.abb.rws.data.md#rapidtaskexecutionstate))

- Unknown: The controller reported a state this library does not know
- Ready: The task is ready to be started
- Stopped: The task was running and has been stopped
- Started: The task is running
- Uninitialized: The task is not initialized

**RapidTaskExecutionMode** ([reference](../api/underautomation.abb.rws.data.md#rapidtaskexecutionmode))

- Unknown: The controller reported a mode this library does not know
- Continuous: The task runs without stepping
- StepOver: The task steps over the routine calls
- StepIn: The task steps into the routine calls
- StepOutOf: The task steps out of the current routine
- StepBack: The task steps backwards
- StepLast: The task steps to the last instruction
- StepWise: The task advances one instruction at a time

**RapidTaskTrustLevel** ([reference](../api/underautomation.abb.rws.data.md#rapidtasktrustlevel))

- Unknown: The controller reported a level this library does not know
- None_: The system carries on
- SystemFailure: The whole system fails
- SystemHalt: The system halts
- SystemStop: The system stops

## Build a task

`BuildTask` links the modules a task holds into a runnable program. The controller accepts the request even when the program does not compile, so read `GetBuildErrors` afterwards and check that the task state became `Linked`.

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.mastership_domain import MastershipDomain

robot = AbbController()
robot.connect("192.168.0.1")

robot.rws.mastership.request(MastershipDomain.Rapid)
try:
    # Link the modules of the task into a runnable program
    robot.rws.rapid.build_task("T_ROB1")
finally:
    robot.rws.mastership.release(MastershipDomain.Rapid)

# The controller does not fail the build request, it reports what it refused afterwards
for error in robot.rws.rapid.get_build_errors("T_ROB1"):
    print(f"{error.module_name} {error.row},{error.column}: {error.error}")

# The task is runnable when its state is Linked
print(robot.rws.rapid.get_task("T_ROB1").task_state)

robot.disconnect()
```

The build errors are described in [RAPID modules & program files](rws-rapid-modules.md).



## Load a module

> **Available on** RWS 1.0 (IRC5) : yes | RWS 2.0 (OmniCore) : yes. Only an OmniCore answers with the name of the module that was loaded, an IRC5 returns null.

`LoadModule` loads one module file into a task. The file has to be on the file system of the controller already, so upload it first with the [file system service](rws-files.md). Set `replace` to `true` when a module of the same name is already loaded, otherwise the controller refuses the request.

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.mastership_domain import MastershipDomain

robot = AbbController()
robot.connect("192.168.0.1")

robot.rws.mastership.request(MastershipDomain.Rapid)
try:
    # The file has to be on the controller already. Upload it first with robot.rws.file.
    # On OmniCore the call answers the name of what was loaded, on IRC5 it answers None.
    loaded = robot.rws.rapid.load_module("T_ROB1", "$HOME/mymodule.mod", True)
    print(loaded)

    robot.rws.rapid.unload_module("T_ROB1", "mymodule")
finally:
    robot.rws.mastership.release(MastershipDomain.Rapid)

robot.disconnect()
```

`UnloadModule` takes the name of the module, not the name of the file. A module that was never saved is lost when it is unloaded.

Loading a whole program instead of one module is done with `LoadProgram`, see [RAPID modules & program files](rws-rapid-modules.md).



## Start and stop the program

Starting a program from your application fails when one of these conditions is not met:

1. The controller is in automatic mode, or in manual mode with the enabling device held. The mode is read with the [control panel service](rws-panel.md).
2. The motors are on, `Panel.SetControllerState(ControllerState.MotorsOn)`.
3. The task is active and its state is `Linked`.
4. The program pointer is set, which `ResetProgramPointer` does for every task.
5. Your connection holds the `Rapid` [mastership](rws-mastership.md).

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.controller_state import ControllerState
from underautomation.abb.rws.data.mastership_domain import MastershipDomain
from underautomation.abb.rws.data.operation_mode import OperationMode
from underautomation.abb.rws.data.rapid_execution_cycle import RapidExecutionCycle
from underautomation.abb.rws.data.rapid_execution_mode import RapidExecutionMode
from underautomation.abb.rws.data.rapid_regain_mode import RapidRegainMode
from underautomation.abb.rws.data.rapid_start_condition import RapidStartCondition

robot = AbbController()
robot.connect("192.168.0.1")

# 1. The controller has to be in automatic mode
if robot.rws.panel.get_operation_mode() != OperationMode.Automatic:
    raise Exception("Turn the key of the controller to automatic mode")

robot.rws.mastership.request(MastershipDomain.Rapid)
try:
    # 2. Motors on
    robot.rws.panel.set_controller_state(ControllerState.MotorsOn)

    # 3. Program pointer back to the entry point of every task
    robot.rws.rapid.reset_program_pointer()

    # 4. Start
    robot.rws.rapid.start(RapidRegainMode.Continue_,
                          RapidExecutionMode.Continue_,
                          RapidExecutionCycle.Forever,
                          RapidStartCondition.None_,
                          False,   # do not stop at breakpoints
                          False)   # normal tasks only
finally:
    robot.rws.mastership.release(MastershipDomain.Rapid)

# 5. Check that it really started, the call above only means the request was accepted
execution = robot.rws.rapid.get_execution_state()
print(execution.state)  # Running or Stopped
print(execution.cycle)  # Forever, Once, OnceDone

robot.disconnect()
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

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.mastership_domain import MastershipDomain
from underautomation.abb.rws.data.rapid_execution_cycle import RapidExecutionCycle

robot = AbbController()
robot.connect("192.168.0.1")

robot.rws.mastership.request(MastershipDomain.Rapid)
try:
    # Only Once and Forever are accepted here
    robot.rws.rapid.set_execution_cycle(RapidExecutionCycle.Once)

    # Start from the production entry point instead of the current program pointer
    robot.rws.rapid.start_from_production_entry()

    # Leave the routine that is running now and go back to the level below it.
    # This is how a trap or a service routine is abandoned without stopping the program under it.
    robot.rws.rapid.abort_execution_level("T_ROB1")
finally:
    robot.rws.mastership.release(MastershipDomain.Rapid)

robot.disconnect()
```

### Stop

```python
import time

from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.rapid_execution_state import RapidExecutionState
from underautomation.abb.rws.data.rapid_stop_mode import RapidStopMode
from underautomation.abb.rws.data.rapid_task_scope import RapidTaskScope

robot = AbbController()
robot.connect("192.168.0.1")

# Stop at the end of the current instruction, normal tasks only
robot.rws.rapid.stop(RapidStopMode.Stop, RapidTaskScope.Normal)

# Let the robot finish the cycle it is in, then stop
robot.rws.rapid.stop(RapidStopMode.Cycle, RapidTaskScope.Normal)

# Stop everything at once, including the static and semi static tasks
robot.rws.rapid.stop(RapidStopMode.QuickStop, RapidTaskScope.AllTasks)

# Wait until the controller confirms the program is stopped
while robot.rws.rapid.get_execution_state().state != RapidExecutionState.Stopped:
    time.sleep(0.2)

robot.disconnect()
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

```python
import time

from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.rapid_execution_mode import RapidExecutionMode
from underautomation.abb.rws.data.rapid_hold_to_run_state import RapidHoldToRunState
from underautomation.abb.rws.data.rapid_regain_mode import RapidRegainMode

robot = AbbController()
robot.connect("192.168.0.1")

# Manual mode only. Press, then keep sending Held, the controller stops the
# program as soon as it stops hearing from your application.
robot.rws.rapid.set_hold_to_run(RapidHoldToRunState.Press)

robot.rws.rapid.start(RapidRegainMode.Continue_, RapidExecutionMode.Continue_)

for i in range(10):
    robot.rws.rapid.set_hold_to_run(RapidHoldToRunState.Held)
    time.sleep(1)

robot.rws.rapid.set_hold_to_run(RapidHoldToRunState.Release)

robot.disconnect()
```

This is only honoured by a virtual controller, and only for a client the controller considers local. A real cabinet expects the physical device.

A complete example, with the checks around it, is given in [Start & stop a RAPID program](start-stop-rapid-program.md).

**Methods of RapidService** ([reference](../api/underautomation.abb.rws.services.md#rapidservice-robotrwsrapid))

- `start(regain: RapidRegainMode=RapidRegainMode.Continue_, executionMode: RapidExecutionMode=RapidExecutionMode.Continue_, cycle: RapidExecutionCycle=RapidExecutionCycle.Forever, condition: RapidStartCondition=RapidStartCondition.None_, stopAtBreakpoint: bool=False, allTasksBySelection: b...`: Starts executing the RAPID program from where the program pointer stands (synchronous) The controller has to be in automatic mode with the motors on, or in manual mode with the enabling device held. Reset the program pointer first with to start from the beginning.
- `start_from_production_entry() -> None`: Starts executing from the production entry point of the program rather than from where the program pointer stands (synchronous)
- `stop(stopMode: RapidStopMode=RapidStopMode.Stop, scope: RapidTaskScope=RapidTaskScope.Normal) -> None`: Stops the RAPID execution (synchronous)
- `start_spy(logFile: str) -> None`: Starts recording the RAPID execution trace into a file (synchronous) The trace names every instruction the controller runs, which is what it takes to find out why a program took a branch it should not have.
- `stop_spy() -> None`: Stops recording the RAPID execution trace (synchronous)

**RapidExecutionInfo** ([reference](../api/underautomation.abb.rws.data.md#rapidexecutioninfo))

- `RapidExecutionInfo()`: Initializes a new instance of the RapidExecutionInfo class
- `state: RapidExecutionState`: Whether RAPID code is currently running
- `cycle: RapidExecutionCycle`: Number of cycles the program is set to run

**RapidExecutionState** ([reference](../api/underautomation.abb.rws.data.md#rapidexecutionstate))

- Unknown: The controller reported a state this library does not know
- Running: RAPID execution is running
- Stopped: RAPID execution is stopped

**RapidExecutionCycle** ([reference](../api/underautomation.abb.rws.data.md#rapidexecutioncycle))

- Unknown: The controller reported a cycle this library does not know
- Forever: The program runs again every time it reaches its end
- AsIs: The cycle currently configured is left untouched
- Once: The program runs once and stops at its end
- OnceDone: The program was asked to run once and has finished doing so

**RapidExecutionMode** ([reference](../api/underautomation.abb.rws.data.md#rapidexecutionmode))

- Continue_: Run until something stops it
- StepIn: Step into the routine called by the current instruction
- StepOver: Run the current instruction whole, without entering the routine it calls
- StepOut: Run until the current routine returns
- StepBack: Step one instruction backwards
- StepLast: Step to the last instruction
- StepMotion: Step to the next motion instruction

**RapidRegainMode** ([reference](../api/underautomation.abb.rws.data.md#rapidregainmode))

- Continue_: Resume from the current position without moving back to the path
- Regain: Move back onto the path before resuming
- Clear: Drop the path and resume from the current position
- EnterConsume: Resume by entering the consumption of the already generated path

**RapidStopMode** ([reference](../api/underautomation.abb.rws.data.md#rapidstopmode))

- Cycle: Stop when the current cycle ends
- Instruction: Stop when the current instruction ends
- Stop: Stop as soon as the robot can decelerate along its path
- QuickStop: Stop as fast as the robot can, leaving the path

**RapidStartCondition** ([reference](../api/underautomation.abb.rws.data.md#rapidstartcondition))

- None_: Start without any additional check
- CallChain: Start only when the call chain of the program pointer is still valid

**RapidTaskScope** ([reference](../api/underautomation.abb.rws.data.md#rapidtaskscope))

- Normal: Apply to the tasks the task selection panel has enabled
- AllTasks: Apply to every task of the system

**RapidHoldToRunState** ([reference](../api/underautomation.abb.rws.data.md#rapidholdtorunstate))

- Press: Ask for execution to be allowed to start
- Held: Confirm that execution may keep running, which has to be repeated about every two seconds
- Release: Stop execution immediately

## Execution trace

The controller can write every instruction it runs into a file. It is the fastest way to find out why a program took a branch it should not have. The two calls take the mastership by themselves, your code does not have to.

```python
import time

from underautomation.abb.abb_controller import AbbController

robot = AbbController()
robot.connect("192.168.0.1")

# The trace names every instruction the controller runs. No mastership needed,
# the controller takes it by itself for these two calls.
robot.rws.rapid.start_spy("$HOME/trace.log")

print(robot.rws.rapid.get_spy_status())  # Logging or NotLogging

time.sleep(5)

robot.rws.rapid.stop_spy()

# Then download the file with the file service
trace = bytes(robot.rws.file.get_file_as_bytes("$HOME/trace.log")).decode("utf-8")
print(trace)

robot.disconnect()
```

The file is written on the controller, download it afterwards with the [file system service](rws-files.md). A trace grows fast, do not leave it running.



**RapidSpyStatus** ([reference](../api/underautomation.abb.rws.data.md#rapidspystatus))

- Unknown: The controller reported a status this library does not know
- Logging: The execution trace is being written
- NotLogging: No execution trace is being written

## Program pointer and motion pointer

Each task has two pointers. The program pointer says which instruction runs next, the motion pointer which one the robot is really executing. They drift apart because the controller plans the path ahead of the movement.

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.mastership_domain import MastershipDomain

robot = AbbController()
robot.connect("192.168.0.1")

# Where the two pointers of the task stand
pointers = robot.rws.rapid.get_pointers("T_ROB1")

if pointers.program_pointer.available:
    print(pointers.program_pointer.module + "/" + pointers.program_pointer.routine)
    print(f"{pointers.program_pointer.begin_row},{pointers.program_pointer.begin_column}")

# The motion pointer is behind the program pointer, the controller plans the path
# ahead of the movement. It is not available in a task that has not moved yet.
print(pointers.motion_pointer.available)

# The piece of source the program pointer covers. The controller refuses the request
# when the task has no program pointer, reset it or start the program first.
position = robot.rws.rapid.get_program_counter_position("T_ROB1")
print(f"{position.module} {position.start_line},{position.start_column}")

# Moving the pointer is a write, it needs the RAPID mastership
robot.rws.mastership.request(MastershipDomain.Rapid)
try:
    # To the beginning of a routine. The module name is used by an IRC5 only,
    # an OmniCore looks the routine up in the whole task.
    robot.rws.rapid.set_program_pointer_to_routine("T_ROB1", "MainModule", "main")

    # To a service routine, which has to be entered at user level
    robot.rws.rapid.set_program_pointer_to_routine_url("T_ROB1", "RAPID/T_ROB1/BASEFUN/LoadIdentify", True)

    # To one position of the source. The routine name is used by an IRC5 only,
    # an OmniCore works it out from the position itself.
    robot.rws.rapid.set_program_pointer_to_cursor("T_ROB1", "MainModule", "main", 12, 1)

    # One instruction forward or backward, automatic mode only
    robot.rws.rapid.set_program_pointer_to_next_instruction("T_ROB1")
    robot.rws.rapid.set_program_pointer_to_previous_instruction("T_ROB1")
finally:
    robot.rws.mastership.release(MastershipDomain.Rapid)

robot.disconnect()
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

```python
from underautomation.abb.abb_controller import AbbController

robot = AbbController()
robot.connect("192.168.0.1")

# For the whole controller
program = robot.rws.rapid.get_program_pointer_sync_state()
motion = robot.rws.rapid.get_motion_pointer_sync_state()
print(f"{program} / {motion}")  # On or Off

# For one task
print(robot.rws.rapid.get_task_program_pointer_sync_state("T_ROB1"))
print(robot.rws.rapid.get_task_motion_pointer_sync_state("T_ROB1"))

# Two counters that say whether anything changed in the task, cheaper than
# downloading the modules again to find out that nothing moved
counters = robot.rws.rapid.get_structural_change_count("T_ROB1")
print(counters.change_count)
print(counters.structural_change_count)

robot.disconnect()
```



**RapidPointers** ([reference](../api/underautomation.abb.rws.data.md#rapidpointers))

- `RapidPointers()`: Initializes a new instance of the RapidPointers class
- `program_pointer: RapidPointerPosition`: Instruction the task will execute next
- `motion_pointer: RapidPointerPosition`: Instruction the robot is currently moving for

**RapidPointerPosition** ([reference](../api/underautomation.abb.rws.data.md#rapidpointerposition))

- `RapidPointerPosition()`: Initializes a new instance of the RapidPointerPosition class
- `available: bool`: Whether the controller reported a position for this pointer at all
- `module: str`: Name of the module the pointer stands in
- `routine: str`: Name of the routine the pointer stands in
- `begin_row: int | None`: Line the pointer begins at, null when the controller did not report it
- `begin_column: int | None`: Column the pointer begins at, null when the controller did not report it
- `end_row: int | None`: Line the pointer ends at, null when the controller did not report it
- `end_column: int | None`: Column the pointer ends at, null when the controller did not report it
- `change_count: int | None`: How many times the pointer has been moved, null when the controller did not report it
- `execution_type: RapidExecutionType`: What kind of code the pointer is standing in

**RapidProgramCounterPosition** ([reference](../api/underautomation.abb.rws.data.md#rapidprogramcounterposition))

- `RapidProgramCounterPosition()`: Initializes a new instance of the RapidProgramCounterPosition class
- `module: str`: Name of the module the pointer stands in
- `routine: str`: Name of the routine the pointer stands in
- `start_line: int | None`: Line the pointed instruction starts at, null when the controller did not report it
- `start_column: int | None`: Column the pointed instruction starts at, null when the controller did not report it
- `end_line: int | None`: Line the pointed instruction ends at, null when the controller did not report it
- `end_column: int | None`: Column the pointed instruction ends at, null when the controller did not report it

**RapidPointerSyncState** ([reference](../api/underautomation.abb.rws.data.md#rapidpointersyncstate))

- Unknown: The controller reported a state this library does not know
- On: The pointers are synchronized
- Off: The pointers are not synchronized

**RapidStructuralChangeCount** ([reference](../api/underautomation.abb.rws.data.md#rapidstructuralchangecount))

- `RapidStructuralChangeCount()`: Initializes a new instance of the RapidStructuralChangeCount class
- `change_count: int | None`: Counter the controller increments whenever anything relevant changes in the task
- `structural_change_count: int | None`: Counter the controller increments when a module is loaded, unloaded or renamed. A rename counts as an unload followed by a load.

**RapidExecutionType** ([reference](../api/underautomation.abb.rws.data.md#rapidexecutiontype))

- Unknown: The controller reported a type this library does not know
- None_: Nothing is running
- Normal: The normal program is running
- Interrupt: An interrupt is running
- ExternalInterrupt: An external interrupt is running
- UserRoutine: A user routine is running
- EventRoutine: An event routine is running

## Call stack

`GetActivationRecord` reads one frame of the call stack. Frame 1 holds the program pointer, and the number grows towards the entry point of the program. The controller refuses the request when the task has no program pointer, or when the stack is not that deep.

```python
from underautomation.abb.abb_controller import AbbController

robot = AbbController()
robot.connect("192.168.0.1")

# Frame 1 is the one holding the program pointer, the number grows towards the entry point
for frame in range(1, 6):
    record = robot.rws.rapid.get_activation_record("T_ROB1", frame)

    print(record.routine_url)
    print(f"{record.begin_row},{record.begin_column}")
    print(record.execution_level)

# The routines the program pointer may be moved to, service routines included
for routine in robot.rws.rapid.get_service_routines("T_ROB1"):
    print(f"{routine.name} -> {routine.url} service={routine.is_service_routine}")

robot.disconnect()
```

| `RapidExecutionLevel` | Where execution stands                                  |
| --------------------- | ------------------------------------------------------- |
| `Normal`              | In the program itself                                   |
| `Trap`                | In a trap routine                                       |
| `User`                | In a routine started by hand, such as a service routine |
| `None`                | Nothing is running at this level                        |
| `Unknown`             | The controller reported a level the SDK does not know   |



**RapidActivationRecord** ([reference](../api/underautomation.abb.rws.data.md#rapidactivationrecord))

- `RapidActivationRecord()`: Initializes a new instance of the RapidActivationRecord class
- `execution_level: RapidExecutionLevel`: Level at which this frame is executing
- `begin_row: int | None`: Line the executing statement starts at, null when the controller did not report it
- `begin_column: int | None`: Column the executing statement starts at, null when the controller did not report it
- `end_row: int | None`: Line the executing statement ends at, null when the controller did not report it
- `end_column: int | None`: Column the executing statement ends at, null when the controller did not report it
- `stack_url: str`: Path identifying this stack frame, which the UI instruction resources also take
- `routine_url: str`: Path of the routine this frame is executing

**RapidServiceRoutineItem** ([reference](../api/underautomation.abb.rws.data.md#rapidserviceroutineitem))

- `RapidServiceRoutineItem()`: Initializes a new instance of the RapidServiceRoutineItem class
- `name: str`: Name of the routine, for example "LoadIdentify"
- `url: str`: Path of the routine, which RapidService.SetProgramPointerToRoutineUrl() takes
- `is_service_routine: bool | None`: Whether this is a service routine rather than an ordinary one, null when the controller did not report it

**RapidExecutionLevel** ([reference](../api/underautomation.abb.rws.data.md#rapidexecutionlevel))

- Unknown: The controller reported a level this library does not know
- None_: Nothing is executing
- Normal: The normal user code is executing
- Trap: A trap routine is executing
- User: A user routine is executing

## Answer an operator dialogue

A RAPID program can stop and ask the operator something. The controller then reports one pending instruction, and the program waits until it is answered. `GetActiveUiInstruction` returns `null` when nothing is pending.

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.mastership_domain import MastershipDomain

robot = AbbController()
robot.connect("192.168.0.1")

# None when the program is not asking the operator for anything right now
question = robot.rws.rapid.get_active_ui_instruction()

if question is not None:
    print(question.instruction)  # name of the RAPID instruction waiting
    print(question.message)
    print(question.event)        # Send, Post or Abort

    # What the program passed in, and what it is waiting for. The names of the
    # parameters depend on the instruction, so read them before writing one.
    for parameter in robot.rws.rapid.get_ui_instruction_parameters(question.stack_url):
        print(f"{parameter.name} = {parameter.value}")

    # Answering is a write, so it needs the mastership
    robot.rws.mastership.request(MastershipDomain.Rapid)
    try:
        # Write the parameter carrying the answer, then the one marking it as completed
        robot.rws.rapid.set_ui_instruction_parameter(question.stack_url, "TPCompleted", "TRUE")
    finally:
        robot.rws.mastership.release(MastershipDomain.Rapid)

    print(robot.rws.rapid.get_ui_instruction_parameter(question.stack_url, "TPCompleted"))

robot.disconnect()
```

The names of the parameters depend on the instruction the program used, so read them with `GetUiInstructionParameters` before writing one. The answer is written first, then the parameter marking the dialogue as completed. Writing a parameter needs the `Rapid` mastership, and fails when the instruction is no longer pending.



**RapidUiInstruction** ([reference](../api/underautomation.abb.rws.data.md#rapiduiinstruction))

- `RapidUiInstruction()`: Initializes a new instance of the RapidUiInstruction class
- `instruction: str`: Name of the RAPID instruction that opened the dialogue, for example "TPReadNum"
- `event: RapidUiInstructionEvent`: What the instruction is asking of the client
- `stack_url: str`: Path identifying the call, which the parameter methods take
- `execution_level: RapidExecutionLevel`: Level at which the instruction is executing
- `message: str`: Text the instruction displays

**RapidUiInstructionParameter** ([reference](../api/underautomation.abb.rws.data.md#rapiduiinstructionparameter))

- `RapidUiInstructionParameter()`: Initializes a new instance of the RapidUiInstructionParameter class
- `name: str`: Name of the parameter, for example "TPCompleted"
- `value: str`: Value of the parameter, written the way RAPID writes it

**RapidUiInstructionEvent** ([reference](../api/underautomation.abb.rws.data.md#rapiduiinstructionevent))

- Unknown: The controller reported an event this library does not know
- Send: The instruction is waiting for an answer
- Post: The instruction only displays something and expects no answer
- Abort: The instruction has been abandoned and no answer is expected any more

## Signals renamed by the program

A RAPID program can give another name to an I/O signal. `GetAliasIo` lists these names as long as the program declaring them is loaded. The signals themselves are read and written with the [I/O service](rws-io.md).

```python
from underautomation.abb.abb_controller import AbbController

robot = AbbController()
robot.connect("192.168.0.1")

# The signals a loaded program gave another name to. Empty when no program declares any.
for alias in robot.rws.rapid.get_alias_io():
    print(f"{alias.alias_name} -> {alias.signal_name} ({alias.type})")

robot.disconnect()
```



**RapidAliasIoItem** ([reference](../api/underautomation.abb.rws.data.md#rapidaliasioitem))

- `RapidAliasIoItem()`: Initializes a new instance of the RapidAliasIoItem class
- `alias_name: str`: Name the RAPID program refers to the signal by
- `signal_name: str`: Name of the I/O signal the alias points at
- `type: IoSignalType`: Type of the aliased signal

## Position of the robot

The position of the robot, its mechanical units and the external axes of a task are read from the [motion system service](rws-motion.md).

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).
