# Controller and robots

List the robots of a Staubli controller, read the controller parameters, the Denavit-Hartenberg parameters and the joint ranges of each arm.

Web page: https://underautomation.com/staubli/documentation/soap-controller

This page shows how to read the description of a Staubli CS8 or CS9 controller and of its robots: the arms, the controller parameters, the Denavit-Hartenberg parameters and the joint ranges. These calls only read: they never change the state of the controller.

## Robots of the controller

`GetRobots()` returns one `Robot` per arm driven by the controller. The index of an arm in this array is the `robot` number that the other methods take.

```python
from underautomation.staubli.staubli_controller import StaubliController

controller = StaubliController()
controller.connect("192.168.0.254")

# The robots driven by the controller. The index in this list
# is the robot number that the other methods take.
robots = controller.soap.get_robots()

for i, robot in enumerate(robots):
    print(f"Robot {i}: {robot.arm}")  # for example TX2-60
    print(f"  Kinematic: {robot.kinematic.name}")  # Anthropomorph6, Scara...
    print(f"  Mount type: {robot.mount_type.name}")  # Floor, Ceiling, Wall
    print(f"  Tuning: {robot.tuning}")

controller.disconnect()
```

`Kinematic` gives the type of arm: `Anthropomorph6` for a 6 axis arm like the TX2 series, `Scara` for a SCARA like the TS2 series, and the other values of the `Kinematic` enumeration.

## Controller parameters

`GetControllerParameters()` returns the parameters of the controller, as key, name and value.

```python
from underautomation.staubli.staubli_controller import StaubliController

controller = StaubliController()
controller.connect("192.168.0.254")

parameters = controller.soap.get_controller_parameters()

for parameter in parameters:
    print(f"{parameter.key} | {parameter.name} = {parameter.value}")

controller.disconnect()
```

The list and the values depend on the controller and on its version. Read the list once on your controller to find the keys you need.

## Denavit-Hartenberg parameters

`GetDhParameters(robot)` returns one `DhParameters` per joint of the arm, as the controller defines its geometry.

```python
from underautomation.staubli.staubli_controller import StaubliController

controller = StaubliController()
controller.connect("192.168.0.254")

# One entry per joint of the first robot
dh = controller.soap.get_dh_parameters(0)

for i, joint in enumerate(dh):
    print(f"J{i + 1}: theta={joint.theta} d={joint.d} a={joint.a} alpha={joint.alpha} beta={joint.beta}")

controller.disconnect()
```

## Joint ranges

`GetJointRange(robot)` returns the software limits of each joint, in radians. The inverse kinematics uses them to reject a solution out of range: see [Kinematics](soap-kinematics.md).

```python
from underautomation.staubli.staubli_controller import StaubliController

controller = StaubliController()
controller.connect("192.168.0.254")

# Software limits of each joint of the first robot, in radians
joint_range = controller.soap.get_joint_range(0)

for i, (low, high) in enumerate(zip(joint_range.min, joint_range.max)):
    print(f"J{i + 1}: {low} to {high}")

controller.disconnect()
```

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference



**Robot** ([reference](../api/underautomation.staubli.soap.data.md#robot))

- `Robot()`: Initializes a new instance of the Robot class.
- `kinematic: Kinematic`: Kinematic type of the robot.
- `arm: str`: Arm model identifier.
- `tuning: str`: Tuning identifier.
- `mount_type: MountType`: Mounting type of the robot (floor, ceiling, wall).
- `length_axis3: LengthAxis3`: Length of the third axis.
- `diameter_axis3: DiameterAxis3`: Diameter of the third axis.

**Kinematic** ([reference](../api/underautomation.staubli.soap.data.md#kinematic))

- Invalid: Invalid or unknown kinematic type.
- Anthropomorph6: 6-axis anthropomorphic robot.
- Anthrioparallel6: 6-axis anthropomorphic parallel robot.
- Anthropomorph5: 5-axis anthropomorphic robot.
- Scara: SCARA robot.
- Eisenmann: Eisenmann kinematic type.

**MountType** ([reference](../api/underautomation.staubli.soap.data.md#mounttype))

- Invalid: Invalid or unknown mount type.
- Floor: Robot is floor-mounted.
- Ceiling: Robot is ceiling-mounted.
- Wall: Robot is wall-mounted.

**Parameter** ([reference](../api/underautomation.staubli.soap.data.md#parameter))

- `Parameter()`: Initializes a new instance of the Parameter class.
- `key: str`: Parameter key identifier.
- `name: str`: Display name of the parameter.
- `value: str`: Value of the parameter.

**DhParameters** ([reference](../api/underautomation.staubli.soap.data.md#dhparameters))

- `DhParameters()`: Initializes a new instance of the DhParameters class.
- `theta: float`: Joint angle theta (radians).
- `d: float`: Link offset d (m).
- `a: float`: Link length a (m).
- `alpha: float`: Link twist alpha (radians).
- `beta: float`: Joint twist beta (radians).

**JointRange** ([reference](../api/underautomation.staubli.soap.data.md#jointrange))

- `JointRange()`: Initializes a new instance of the JointRange class.
- `min: typing.List[float]`: Minimum values for each joint (radians).
- `max: typing.List[float]`: Maximum values for each joint (radians).
