# underautomation.abb.common

## ExternalJoints

`from underautomation.abb.common.external_joints import ExternalJoints`

The six external axis values that travel with a robot position. An axis the robot system does not define comes back as 9E9, which is how the controller says "not in use" rather than an actual position.

- `ExternalJoints(axisA: float, axisB: float, axisC: float, axisD: float, axisE: float, axisF: float)`: Initializes the six external axes
- `axis_a: float`: Value of external axis A
- `axis_b: float`: Value of external axis B
- `axis_c: float`: Value of external axis C
- `axis_d: float`: Value of external axis D
- `axis_e: float`: Value of external axis E
- `axis_f: float`: Value of external axis F
- `static NotInUse: float`: Value the controller reports for an external axis that is not in use

## JointTarget

`from underautomation.abb.common.joint_target import JointTarget`

A robot position expressed joint by joint: the six axes of the arm and the six external axes.

- `JointTarget(robotAxes: RobotJoints, externalAxes: ExternalJoints)`: Initializes a new joint target
- `robot_axes: RobotJoints`: Values of the six axes of the robot arm. Never null.
- `external_axes: ExternalJoints`: Values of the six external axes. Never null.

## Pose

`from underautomation.abb.common.pose import Pose`

A position and the orientation the robot holds there: a Position extended with a Quaternion.

- `Pose(x: float, y: float, z: float, q1: float, q2: float, q3: float, q4: float)`: Initializes a new pose
- `orientation: Quaternion`: Orientation held at this position. Never null: a pose built without one carries the identity rotation.
- Inherited from [Position](underautomation.abb.common.md#position): `x`, `y`, `z`

## Position

`from underautomation.abb.common.position import Position`

A point in space, expressed in the coordinate system of whoever produced it. Most readings of the controller express a position in millimetres, while the kinematics calculations work in metres. The method that returns or takes a position says which one it uses.

- `Position(x: float, y: float, z: float)`: Initializes a new position
- `x: float`: Coordinate along the X axis
- `y: float`: Coordinate along the Y axis
- `z: float`: Coordinate along the Z axis

## Quaternion

`from underautomation.abb.common.quaternion import Quaternion`

An orientation in space, expressed as a unit quaternion. The controller rejects a quaternion that is not normalized, so keep ² + ² + ² + ² equal to 1.

- `Quaternion(q1: float, q2: float, q3: float, q4: float)`: Initializes a new quaternion
- `q1: float`: Real component of the quaternion
- `q2: float`: First imaginary component of the quaternion
- `q3: float`: Second imaginary component of the quaternion
- `q4: float`: Third imaginary component of the quaternion

## RobTarget

`from underautomation.abb.common.rob_target import RobTarget`

A complete robot target: a Pose extended with the axis configuration used to reach it and the external axis values that travel with it.

- `RobTarget(x: float, y: float, z: float, orientation: Quaternion, configuration: RobotConfiguration, externalAxes: ExternalJoints)`: Initializes a new target
- `configuration: RobotConfiguration`: Axis configuration used to reach the pose. Never null.
- `external_axes: ExternalJoints`: Values of the six external axes, null when the reading does not report them
- Inherited from [Pose](underautomation.abb.common.md#pose): `orientation`
- Inherited from [Position](underautomation.abb.common.md#position): `x`, `y`, `z`

## RobotConfiguration

`from underautomation.abb.common.robot_configuration import RobotConfiguration`

The axis configuration the robot uses to reach a pose. Several joint combinations reach the same tool position and orientation. The configuration names the one to use, as the quarter revolution each of the deciding axes sits in.

- `RobotConfiguration(quarter1: int, quarter4: int, quarter6: int, quarterX: int)`: Initializes a new configuration
- `quarter1: int`: Quarter revolution axis 1 sits in
- `quarter4: int`: Quarter revolution axis 4 sits in
- `quarter6: int`: Quarter revolution axis 6 sits in
- `quarter_x: int`: Index of the arm configuration, which tells the remaining joint combinations apart

## RobotJoints

`from underautomation.abb.common.robot_joints import RobotJoints`

The six joint values of a robot arm. Readings of the controller express them in degrees, while the kinematics calculations work in radians. The method that returns or takes them says which one it uses.

- `RobotJoints(axis1: float, axis2: float, axis3: float, axis4: float, axis5: float, axis6: float)`: Initializes the six axes
- `axis1: float`: Value of axis 1
- `axis2: float`: Value of axis 2
- `axis3: float`: Value of axis 3
- `axis4: float`: Value of axis 4
- `axis5: float`: Value of axis 5
- `axis6: float`: Value of axis 6
