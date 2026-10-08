# Robot Web Services overview

Robot Web Services (RWS) is the REST interface of ABB robot controllers. One API covers RWS 1.0 on IRC5 and RWS 2.0 on OmniCore.

Web page: https://underautomation.com/abb/documentation/rws

Robot Web Services (RWS) is the HTTP interface an ABB controller exposes on the network. The SDK wraps it in nine services, reachable from `robot.Rws` once the connection is open. Nothing has to be installed on the robot.

## Quick tour

Every service is a property of `robot.Rws`. Read operations need no special right, they only need a valid user account.

```python
from underautomation.abb.abb_controller import AbbController

robot = AbbController()
robot.connect("192.168.0.1")

# Identity of the controller and version of the system it runs
print(robot.rws.controller.get_identity().name)
print(robot.rws.system.get_info().version_name)

# Operation mode and motors state
print(robot.rws.panel.get_operation_mode())
print(robot.rws.panel.get_controller_state())

# RAPID tasks and their execution state
for task in robot.rws.rapid.get_tasks():
    print(f"{task.name} : {task.execution_state}")

# I/O signals
for signal in robot.rws.io.get_signals():
    print(f"{signal.name} = {signal.logical_value}")

# Current position of the robot
print(robot.rws.motion_system.get_rob_target("ROB_1"))

robot.disconnect()
```

## The nine services

| Service                  | What it does                                                                                               | Page                                              |
| ------------------------ | ---------------------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| `robot.Rws.Controller`   | Controller identity, clock and time zone, network configuration, restart, backup and restore, safety state | [Controller](rws-controller.md)   |
| `robot.Rws.Panel`        | Operation mode, motors on and off, speed ratio, collision detection                                        | [Control panel](rws-panel.md)     |
| `robot.Rws.Rapid`        | RAPID tasks, program execution, modules, variables and symbols                                             | [RAPID tasks](rws-rapid-tasks.md) |
| `robot.Rws.Io`           | Digital, analog and group signals, I/O devices and networks                                                | [I/O](rws-io.md)                  |
| `robot.Rws.MotionSystem` | Robot position, jogging, kinematics, mechanical units, calibration                                         | [Motion system](rws-motion.md)    |
| `robot.Rws.File`         | File system of the controller, download and upload                                                         | [File system](rws-files.md)       |
| `robot.Rws.Elog`         | Event log of the controller                                                                                | [Event log](rws-elog.md)          |
| `robot.Rws.Mastership`   | Write lock of the controller                                                                               | [Mastership](rws-mastership.md)   |
| `robot.Rws.System`       | System version, options, products, robot types, energy counters                                            | [System](rws-system.md)           |

The RAPID service is large, so it is documented on three pages: [tasks and execution](rws-rapid-tasks.md), [variables and symbols](rws-rapid-symbols.md), [modules and programs](rws-rapid-modules.md).

## Two versions, one API

RWS exists in two versions. RWS 1.0 runs on IRC5 controllers with RobotWare 6, RWS 2.0 on OmniCore controllers with RobotWare 7. The version is chosen at connection time with the `RwsVersion` enum, and the SDK handles the differences internally.

Your code stays the same on both. A few operations only exist on one of the two, they are marked on each page with an availability badge. See [IRC5 or OmniCore: which RWS version](irc5-vs-omnicore.md) for the comparison.

## Mastership, the write lock

Reading is always allowed. Writing is not: the controller gives the right to change a domain to one client at a time, and this right is called the mastership. Take it before a write, give it back right after, so the operator can still use the teach pendant. A write attempted without it fails with the HTTP status code 403.

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.mastership_domain import MastershipDomain

robot = AbbController()
robot.connect("192.168.0.1")

# Reading never needs the mastership
value = robot.rws.rapid.get_symbol_value("RAPID/T_ROB1/user/reg1")

# Writing does. Take it as late as possible and give it back in a finally block
robot.rws.mastership.request(MastershipDomain.Rapid)
try:
    robot.rws.rapid.set_symbol_value("RAPID/T_ROB1/user/reg1", "5")
finally:
    robot.rws.mastership.release(MastershipDomain.Rapid)

print(value)
robot.disconnect()
```

Two calls take the mastership for you, `Panel.SetSpeedRatio` and `Controller.Restart`. The full rules are on the [Mastership](rws-mastership.md) page.

## Errors

Every failure of an RWS call is reported as an `RwsException`. It carries the HTTP status code in `StatusCode`, and the error the controller described in `RwsErrorCode`, `RwsErrorMessage` and `ResponseBody`.

```python
from underautomation.abb.abb_controller import AbbController
from UnderAutomation.ABB.Rws import RwsException

robot = AbbController()
robot.connect("192.168.0.1")

try:
    robot.rws.io.set_signal_value("Local", "PANEL", "DO_Gripper", 1)
except RwsException as ex:
    # The exception comes from the .NET runtime, so its members keep their original names.
    # StatusCode is the HTTP status code the controller answered
    if ex.StatusCode == 403:
        print("Mastership is held elsewhere, or the user account lacks the grant")
    elif ex.StatusCode == 404:
        print("This signal does not exist on this controller")
    else:
        print(f"RWS error {ex.StatusCode} : {ex.RwsErrorMessage}")

robot.disconnect()
```

| Status | Usual meaning                                                              |
| ------ | -------------------------------------------------------------------------- |
| 400    | The controller refused the value, for example a speed ratio out of range   |
| 403    | Mastership is held elsewhere, or the user account lacks the UAS grant      |
| 404    | The resource does not exist on this controller, often a wrong `RwsVersion` |
| 500    | The controller could not run the operation in its current state            |
| 503    | The controller has no free session left                                    |

A parsing failure is reported as an `RwsException` too, so a single `catch` covers the whole SDK.

## Synchronous and asynchronous

Every service method exists twice. The synchronous version is always available. The asynchronous one has the same name followed by `Async`, returns a `Task` and takes an optional `CancellationToken`.



The asynchronous methods are not compiled for .NET Framework 3.5 and 4.0, which have no `async` and `await`. Everything else works on those versions.

## Sessions

Each connection uses one session on the controller. An OmniCore accepts around 70 of them at the same time. An application that connects in a loop without calling `Disconnect` exhausts them, and every following request then answers 503. Connect once, keep the object, disconnect when your application closes.
