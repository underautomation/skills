# Control panel & operation mode

Read and change the operation mode, the controller state (motors on/off), the speed ratio, and the collision detection state.

Web page: https://underautomation.com/abb/documentation/rws-panel

`robot.Rws.Panel` is the control panel of the controller. It reads and changes what an operator sees on the teach pendant: the operating mode, the state of the motors, the speed the programs run at, and the collision detection.

## Operating mode

`GetOperationMode` returns the mode currently selected on the controller. The mode decides what a remote client is allowed to do. A program is normally started from the network in automatic mode only.

| `OperationMode`                | Meaning                                                           |
| ------------------------------ | ----------------------------------------------------------------- |
| `Automatic`                    | Automatic mode, the program runs without an operator in the cell  |
| `ManualReducedSpeed`           | Manual mode, the operator holds the enabling device               |
| `ManualFullSpeed`              | Manual mode at full speed                                         |
| `AutomaticChangeRequest`       | The change to automatic mode is waiting for an acknowledgement    |
| `ManualFullSpeedChangeRequest` | The change to manual full speed is waiting for an acknowledgement |
| `Init`                         | The controller is starting                                        |
| `Undefined`, `Unknown`         | The controller reports no mode, or one this library does not know |

The mode itself is selected with the key on the cabinet, an application cannot change it. What the SDK can do is confirm a change the operator has already started, with `AcknowledgeOperationMode`.

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

The controller refuses the acknowledgement when no change is waiting for one, and when the connected client is not the local client of the controller. Both cases give an `RwsException`.

`OperationModeAcknowledgement.CollisionDetection` uses the same method to confirm a collision, see below.

## Mode selector lock

> **Available on** RWS 1.0 (IRC5) : yes | RWS 2.0 (OmniCore) : yes. The controller needs the key-less mode selector option

The mode selector can be locked with a pin code, so that the mode cannot be changed until the same code is given back.

| `OperationModeLockState` | Meaning                                                                            |
| ------------------------ | ---------------------------------------------------------------------------------- |
| `Unlocked`               | The operating mode can be changed freely                                           |
| `Locked`                 | Locked, `UnlockOperationMode` releases it with the pin code it was locked with     |
| `PermanentlyLocked`      | Locked for good, the pin code no longer releases it                                |
| `PendingPermanentLock`   | A permanent lock was asked for and is not effective yet                            |
| `Error`, `Unknown`       | The controller reports an error on the lock, or a state this library does not know |

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.operation_mode_lock_state import OperationModeLockState

robot = AbbController()
robot.connect("192.168.0.1")

lock_state = robot.rws.panel.get_operation_mode_lock_state()
print(f"Mode selector : {lock_state}")

if lock_state == OperationModeLockState.Unlocked:
    # Four digits, needed again to unlock the selector
    robot.rws.panel.lock_operation_mode("1234")
elif lock_state == OperationModeLockState.Locked:
    robot.rws.panel.unlock_operation_mode("1234")

# A permanent lock cannot be released with unlock_operation_mode
robot.rws.panel.lock_operation_mode("1234", True)

robot.disconnect()
```

The pin code is exactly four digits, the SDK throws an `ArgumentException` for anything else. The permanent lock needs the grant to lock the safety controller configuration on the user account.

A controller built without the key-less mode selector option answers 403 on the three lock methods, including the read. The SDK catches that case and explains it in the message of the `RwsException`, because the controller error only says that an option is missing.

## Motors on and off

`GetControllerState` reports whether the robot can move. `SetControllerState` accepts `MotorsOn` and `MotorsOff` only, the other values are read only states of the controller and passing one throws an `ArgumentException`.

| `ControllerState`    | Meaning                                                              |
| -------------------- | -------------------------------------------------------------------- |
| `MotorsOn`           | The robot is ready to move, by jogging or by running a program       |
| `MotorsOff`          | Standby, there is no power on the motors                             |
| `Init`               | The controller is starting, it goes to `MotorsOff` when it is up     |
| `GuardStop`          | Stopped because the safety runchain is open, for example a cell door |
| `EmergencyStop`      | Stopped by the emergency stop                                        |
| `EmergencyStopReset` | The emergency stop is released, the transition is not confirmed yet  |
| `SystemFailure`      | The controller needs a restart                                       |
| `Unknown`            | The state could not be determined                                    |

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

The controller answers before the state has really changed. Read the state again until it reports `MotorsOn`, as in the example above, instead of assuming the robot is ready right after the call.

## Speed ratio

The speed ratio is the percentage of their programmed speed the programs run at. `GetSpeedRatio` returns it, `SetSpeedRatio` changes it.

```python
from underautomation.abb.abb_controller import AbbController

robot = AbbController()
robot.connect("192.168.0.1")

speed_ratio = robot.rws.panel.get_speed_ratio()
print(f"The programs run at {speed_ratio} % of their programmed speed")

# Percentage between 0 and 100, accepted in automatic mode only
robot.rws.panel.set_speed_ratio(25)

# Take the mastership yourself when several writes follow each other.
# The .NET API takes every domain in one call, in Python they are taken one by one.
domains = robot.rws.mastership.get_domains()

for domain in domains:
    robot.rws.mastership.request(domain)

try:
    robot.rws.panel.set_speed_ratio(100, False)
finally:
    for domain in domains:
        robot.rws.mastership.release(domain)

robot.disconnect()
```

The value is between 0 and 100, the controller answers 400 for anything else. The controller accepts the change in automatic mode.

On an OmniCore, writing the speed ratio needs the mastership. The SDK takes it for the time of the request, this is what the `useImplicitMastership` argument does. Set it to `false` when your own code already holds the [mastership](rws-mastership.md), otherwise the controller refuses a second request on a domain you already hold. An IRC5 needs no mastership here and ignores the argument.

## Collision detection

`GetCollisionDetectionState` tells whether the robot stopped because it touched something.

| `CollisionDetectionState` | Meaning                                                 |
| ------------------------- | ------------------------------------------------------- |
| `Init`                    | No collision since the controller started               |
| `Triggered`               | A collision was detected and is waiting to be confirmed |
| `Confirmed`               | A detected collision was confirmed                      |
| `TriggeredAcknowledged`   | A detected collision was acknowledged by an operator    |
| `Unknown`                 | The state could not be determined                       |

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.collision_detection_state import CollisionDetectionState
from underautomation.abb.rws.data.operation_mode_acknowledgement import OperationModeAcknowledgement

robot = AbbController()
robot.connect("192.168.0.1")

state = robot.rws.panel.get_collision_detection_state()

if state == CollisionDetectionState.Triggered or state == CollisionDetectionState.Confirmed:
    print("A collision was detected, the robot is stopped")

    # Acknowledge the collision from the application
    robot.rws.panel.acknowledge_operation_mode(OperationModeAcknowledgement.CollisionDetection)

robot.disconnect()
```

A collision is acknowledged with `AcknowledgeOperationMode`, the same method as an operating mode change, with `OperationModeAcknowledgement.CollisionDetection`.

## Language and restart

`SetLanguage` changes the language the controller writes its messages in, with a two letter code such as `en`, `de` or `sv`. The language must be installed on the controller, otherwise the request fails. The [controller service](rws-controller.md) changes the same setting with its own `SetLanguage`, either one can be used.

`Restart` restarts the controller. The control panel accepts `Restart`, `IStart`, `PStart` and `BStart`. Use `robot.Rws.Controller.Restart` for the other modes, they are described on the [controller page](rws-controller.md).

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.controller_restart_mode import ControllerRestartMode

robot = AbbController()
robot.connect("192.168.0.1")

# Language the controller reports its messages in.
# The language must be installed on the controller.
robot.rws.panel.set_language("en")

# Warm restart. The connection is lost as soon as the controller shuts down.
robot.rws.panel.restart(ControllerRestartMode.Restart)
robot.disconnect()
```

The connection is lost as soon as the controller starts shutting down. A call that succeeded is normally followed by failing requests until the controller is up again, so disconnect right after it and connect again later. On an OmniCore the restart needs the mastership on every domain, taken implicitly by default like for the speed ratio.

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## API reference

**Methods of PanelService** ([reference](../api/underautomation.abb.rws.services.md#panelservice-robotrwspanel))

- `get_controller_state() -> ControllerState`: Gets the state of the controller (synchronous)
- `set_controller_state(state: ControllerState) -> None`: Turns the motors of the robot on or off (synchronous)
- `get_operation_mode() -> OperationMode`: Gets the operating mode the controller runs in (synchronous)
- `acknowledge_operation_mode(acknowledgement: OperationModeAcknowledgement) -> None`: Confirms a pending operating mode change (synchronous) The controller waits for this confirmation whenever the mode selector is turned, unless it is configured to acknowledge the change on its own.
- `get_operation_mode_lock_state() -> OperationModeLockState`: Gets the lock state of the operating mode selector (synchronous)
- `lock_operation_mode(pin: str, permanent: bool=False) -> None`: Locks the operating mode selector with a pin code (synchronous)
- `unlock_operation_mode(pin: str) -> None`: Releases the lock of the operating mode selector (synchronous)
- `get_speed_ratio() -> int`: Gets the speed ratio the controller runs the programs at (synchronous)
- `set_speed_ratio(speedRatio: int, useImplicitMastership: bool=True) -> None`: Sets the speed ratio the controller runs the programs at (synchronous) Only accepted while the controller runs in automatic mode.
- `get_collision_detection_state() -> CollisionDetectionState`: Gets the collision detection state of the controller (synchronous)
- `set_language(languageCode: str) -> None`: Sets the language the controller reports its messages in (synchronous)
- `restart(mode: ControllerRestartMode, useImplicitMastership: bool=True) -> None`: Restarts the controller (synchronous)

**OperationMode** ([reference](../api/underautomation.abb.rws.data.md#operationmode))

- Unknown: The operating mode could not be determined
- Init: The controller is initializing
- AutomaticChangeRequest: A change to the automatic mode has been requested and is waiting to be acknowledged
- ManualFullSpeedChangeRequest: A change to the manual full speed mode has been requested and is waiting to be acknowledged
- ManualReducedSpeed: Manual mode at reduced speed
- ManualFullSpeed: Manual mode at full speed
- Automatic: Automatic mode
- Undefined: The controller reports an undefined operating mode

**OperationModeAcknowledgement** ([reference](../api/underautomation.abb.rws.data.md#operationmodeacknowledgement))

- Automatic: Confirms the switch to the automatic mode
- ManualFullSpeed: Confirms the switch to the manual full speed mode
- CollisionDetection: Confirms a collision detection

**OperationModeLockState** ([reference](../api/underautomation.abb.rws.data.md#operationmodelockstate))

- Unknown: The lock state could not be determined
- Error: The controller reports an error on the mode selector lock
- Unlocked: The operating mode can be changed freely
- Locked: The operating mode is locked and can be unlocked again with the pin code it was locked with
- PermanentlyLocked: The operating mode is permanently locked
- PendingPermanentLock: A permanent lock has been requested and is not effective yet

**ControllerState** ([reference](../api/underautomation.abb.rws.data.md#controllerstate))

- Unknown: The state could not be determined
- Init: The robot is starting up. It will shift to MotorsOff once it has started.
- MotorsOff: The robot is in a standby state where there is no power to its motors. The state has to be shifted to MotorsOn before the robot can move.
- MotorsOn: The robot is ready to move, either by jogging or by running programs
- GuardStop: The robot is stopped because the safety runchain is opened, for instance because a door of its cell is open
- EmergencyStop: The robot is stopped because the emergency stop was activated
- EmergencyStopReset: The robot is ready to leave the emergency stop state: the emergency stop is no longer activated, but the state transition is not confirmed yet.
- SystemFailure: The robot is in a system failure state and requires a restart

**CollisionDetectionState** ([reference](../api/underautomation.abb.rws.data.md#collisiondetectionstate))

- Unknown: The collision detection state could not be determined
- Init: No collision has been detected since the controller started
- Triggered: A collision has been detected and is waiting to be confirmed
- Confirmed: A detected collision has been confirmed
- TriggeredAcknowledged: A detected collision has been acknowledged by an operator

**ControllerRestartMode** ([reference](../api/underautomation.abb.rws.data.md#controllerrestartmode))

- Restart: The controller will be restarted. The state is saved and any changed system parameter settings will be activated after the restart.
- Shutdown: The main computer will be shut down. Should be used if the controller UPS is broken.
- XStart: The controller will be restarted and the Boot Application will be started. The current system is saved and deactivated (the controller is non-functional, for advanced maintenance only).
- IStart: The controller will be restarted. The current system parameter settings and RAPID programs will be discarded, and the original system installation settings will be used.
- PStart: The controller will be restarted. The current RAPID programs and data will be discarded, but not the system parameter settings.
- BStart: The controller will be restarted. The last automatically saved system state will be loaded. Should be used to recover from a system crash.
