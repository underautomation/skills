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

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.operation_mode import OperationMode
from underautomation.abb.rws.data.operation_mode_acknowledgement import OperationModeAcknowledgement

robot = AbbController()
robot.connect("192.168.0.1")

mode = robot.rws.panel.get_operation_mode()

if mode == OperationMode.Automatic:
    print("Automatic mode, a program can be started remotely")
elif mode == OperationMode.ManualReducedSpeed or mode == OperationMode.ManualFullSpeed:
    print("Manual mode, the operator holds the enabling device")
elif mode == OperationMode.AutomaticChangeRequest:
    # The key was turned to automatic, the change waits for a confirmation
    robot.rws.panel.acknowledge_operation_mode(OperationModeAcknowledgement.Automatic)
elif mode == OperationMode.ManualFullSpeedChangeRequest:
    robot.rws.panel.acknowledge_operation_mode(OperationModeAcknowledgement.ManualFullSpeed)

robot.disconnect()
```

## Motors on

The state change is not immediate. Ask for it, then wait until the controller reports it.

```python
import time

from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.controller_state import ControllerState

robot = AbbController()
robot.connect("192.168.0.1")

state = robot.rws.panel.get_controller_state()
print(f"Controller state : {state}")

if state == ControllerState.MotorsOff:
    # The robot can move once the motors are on
    robot.rws.panel.set_controller_state(ControllerState.MotorsOn)

# The state change is not immediate, wait for the controller to report it
while robot.rws.panel.get_controller_state() != ControllerState.MotorsOn:
    time.sleep(0.2)

# Motors off puts the robot back in standby, it cannot move any more
robot.rws.panel.set_controller_state(ControllerState.MotorsOff)

robot.disconnect()
```

## The program pointer

The program starts from where the program pointer stands, not from the beginning. `ResetProgramPointer()` puts the pointer of every task back on its entry point, usually `main`. To start somewhere else, move the pointer to a routine or to a position in the source.

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

## Start

`Start` takes six arguments. The defaults suit a normal production start: resume the path, run continuously, forever, on the normal tasks only.

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

```python
import time

from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.mastership_domain import MastershipDomain
from underautomation.abb.rws.data.rapid_execution_cycle import RapidExecutionCycle
from underautomation.abb.rws.data.rapid_execution_mode import RapidExecutionMode
from underautomation.abb.rws.data.rapid_execution_state import RapidExecutionState
from underautomation.abb.rws.data.rapid_regain_mode import RapidRegainMode
from underautomation.abb.rws.data.rapid_start_condition import RapidStartCondition

robot = AbbController()
robot.connect("192.168.0.1")

# Polls the execution state until the program runs, or the timeout expires
def wait_running(robot, timeout_ms):
    limit = time.time() + timeout_ms / 1000.0

    while time.time() < limit:
        if robot.rws.rapid.get_execution_state().state == RapidExecutionState.Running:
            return True

        time.sleep(0.2)

    return False

# start returns as soon as the controller accepted the request. It does not mean the
# program runs : the controller can still refuse it, or stop it on the first error.
robot.rws.mastership.request(MastershipDomain.Rapid)
try:
    robot.rws.rapid.start(RapidRegainMode.Continue_, RapidExecutionMode.Continue_,
                          RapidExecutionCycle.Forever, RapidStartCondition.None_, False, False)
finally:
    robot.rws.mastership.release(MastershipDomain.Rapid)

if not wait_running(robot, 5000):
    raise Exception("The program did not start, look at the event log of the controller")

# The task that drives the robot has its own state, more precise than the global one
task = robot.rws.rapid.get_task("T_ROB1")
print(task.execution_state)  # Started
print(task.execution_type)   # what kind of code is running now

# Where the program pointer stands, so you can tell a running program from a blocked one
pointers = robot.rws.rapid.get_pointers("T_ROB1")
print(pointers.program_pointer)

robot.disconnect()
```

`GetExecutionState()` covers the whole controller. `GetTask("T_ROB1")` is more precise, it gives the state, the execution level and the kind of code each task is running.

## Run once instead of forever

The number of cycles can also be set before starting, and read back per task.

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

## Stop

`Stop` takes a stop mode and a scope. Stopping needs no mastership.

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

**Methods of RapidService** ([reference](../api/underautomation.abb.rws.services.md#rapidservice-robotrwsrapid))

- `get_execution_state() -> RapidExecutionInfo`: Gets whether the controller is executing RAPID code, and how many cycles it is set to run (synchronous)
- `set_execution_cycle(cycle: RapidExecutionCycle) -> None`: Sets how many times the program runs before stopping (synchronous)
- `abort_execution_level(task: str) -> None`: Abandons the routine the task is currently running and returns to the level below it (synchronous) This is how a trap or a service routine started by hand is left without stopping the program underneath it.

**RapidExecutionInfo** ([reference](../api/underautomation.abb.rws.data.md#rapidexecutioninfo))

- `RapidExecutionInfo()`: Initializes a new instance of the RapidExecutionInfo class
- `state: RapidExecutionState`: Whether RAPID code is currently running
- `cycle: RapidExecutionCycle`: Number of cycles the program is set to run

**RapidExecutionCycle** ([reference](../api/underautomation.abb.rws.data.md#rapidexecutioncycle))

- Unknown: The controller reported a cycle this library does not know
- Forever: The program runs again every time it reaches its end
- AsIs: The cycle currently configured is left untouched
- Once: The program runs once and stops at its end
- OnceDone: The program was asked to run once and has finished doing so

**RapidStopMode** ([reference](../api/underautomation.abb.rws.data.md#rapidstopmode))

- Cycle: Stop when the current cycle ends
- Instruction: Stop when the current instruction ends
- Stop: Stop as soon as the robot can decelerate along its path
- QuickStop: Stop as fast as the robot can, leaving the path

**ControllerState** ([reference](../api/underautomation.abb.rws.data.md#controllerstate))

- Unknown: The state could not be determined
- Init: The robot is starting up. It will shift to MotorsOff once it has started.
- MotorsOff: The robot is in a standby state where there is no power to its motors. The state has to be shifted to MotorsOn before the robot can move.
- MotorsOn: The robot is ready to move, either by jogging or by running programs
- GuardStop: The robot is stopped because the safety runchain is opened, for instance because a door of its cell is open
- EmergencyStop: The robot is stopped because the emergency stop was activated
- EmergencyStopReset: The robot is ready to leave the emergency stop state: the emergency stop is no longer activated, but the state transition is not confirmed yet.
- SystemFailure: The robot is in a system failure state and requires a restart
