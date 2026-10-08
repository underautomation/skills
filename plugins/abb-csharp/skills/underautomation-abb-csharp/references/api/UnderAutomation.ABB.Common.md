# UnderAutomation.ABB.Common

## ExternalJoints

`class ExternalJoints`

The six external axis values that travel with a robot position. An axis the robot system does not define comes back as 9E9, which is how the controller says "not in use" rather than an actual position.

- `ExternalJoints()`: Initializes the six external axes to zero
- `ExternalJoints(double axisA, double axisB, double axisC, double axisD, double axisE, double axisF)`: Initializes the six external axes
- `double AxisA { get; set; }`: Value of external axis A
- `double AxisB { get; set; }`: Value of external axis B
- `double AxisC { get; set; }`: Value of external axis C
- `double AxisD { get; set; }`: Value of external axis D
- `double AxisE { get; set; }`: Value of external axis E
- `double AxisF { get; set; }`: Value of external axis F
- `const double NotInUse = 9000000000`: Value the controller reports for an external axis that is not in use

## JointTarget

`class JointTarget`

A robot position expressed joint by joint: the six axes of the arm and the six external axes.

- `JointTarget()`: Initializes a new joint target with every axis at zero
- `JointTarget(RobotJoints robotAxes, ExternalJoints externalAxes)`: Initializes a new joint target
- `ExternalJoints ExternalAxes { get; set; }`: Values of the six external axes. Never null.
- `RobotJoints RobotAxes { get; set; }`: Values of the six axes of the robot arm. Never null.

## Pose

`class Pose : Position`

A position and the orientation the robot holds there: a Common.Position extended with a Common.Quaternion.

- `Pose()`: Initializes a new pose at the origin, with no rotation
- `Pose(double x, double y, double z, double q1, double q2, double q3, double q4)`: Initializes a new pose
- `Pose(double x, double y, double z, Quaternion orientation)`: Initializes a new pose
- `Quaternion Orientation { get; set; }`: Orientation held at this position. Never null: a pose built without one carries the identity rotation.
- Inherited from [Position](UnderAutomation.ABB.Common.md#position): `X`, `Y`, `Z`

## Position

`class Position`

A point in space, expressed in the coordinate system of whoever produced it. Most readings of the controller express a position in millimetres, while the kinematics calculations work in metres. The method that returns or takes a position says which one it uses.

- `Position()`: Initializes a new position at the origin
- `Position(double x, double y, double z)`: Initializes a new position
- `double X { get; set; }`: Coordinate along the X axis
- `double Y { get; set; }`: Coordinate along the Y axis
- `double Z { get; set; }`: Coordinate along the Z axis

## Quaternion

`class Quaternion`

An orientation in space, expressed as a unit quaternion. The controller rejects a quaternion that is not normalized, so keep Quaternion.Q1² + Quaternion.Q2² + Quaternion.Q3² + Quaternion.Q4² equal to 1.

- `Quaternion()`: Initializes a new quaternion with no rotation at all (1, 0, 0, 0)
- `Quaternion(double q1, double q2, double q3, double q4)`: Initializes a new quaternion
- `double Q1 { get; set; }`: Real component of the quaternion
- `double Q2 { get; set; }`: First imaginary component of the quaternion
- `double Q3 { get; set; }`: Second imaginary component of the quaternion
- `double Q4 { get; set; }`: Third imaginary component of the quaternion

## RobTarget

`class RobTarget : Pose`

A complete robot target: a Common.Pose extended with the axis configuration used to reach it and the external axis values that travel with it.

- `RobTarget()`: Initializes a new target at the origin, with no rotation
- `RobTarget(double x, double y, double z, Quaternion orientation, RobotConfiguration configuration, ExternalJoints externalAxes)`: Initializes a new target
- `RobotConfiguration Configuration { get; set; }`: Axis configuration used to reach the pose. Never null.
- `ExternalJoints ExternalAxes { get; set; }`: Values of the six external axes, null when the reading does not report them
- Inherited from [Pose](UnderAutomation.ABB.Common.md#pose): `Orientation`
- Inherited from [Position](UnderAutomation.ABB.Common.md#position): `X`, `Y`, `Z`

## RobotConfiguration

`class RobotConfiguration`

The axis configuration the robot uses to reach a pose. Several joint combinations reach the same tool position and orientation. The configuration names the one to use, as the quarter revolution each of the deciding axes sits in.

- `RobotConfiguration()`: Initializes a new configuration with every quarter revolution set to zero
- `RobotConfiguration(int quarter1, int quarter4, int quarter6, int quarterX)`: Initializes a new configuration
- `int Quarter1 { get; set; }`: Quarter revolution axis 1 sits in
- `int Quarter4 { get; set; }`: Quarter revolution axis 4 sits in
- `int Quarter6 { get; set; }`: Quarter revolution axis 6 sits in
- `int QuarterX { get; set; }`: Index of the arm configuration, which tells the remaining joint combinations apart

## RobotJoints

`class RobotJoints`

The six joint values of a robot arm. Readings of the controller express them in degrees, while the kinematics calculations work in radians. The method that returns or takes them says which one it uses.

- `RobotJoints()`: Initializes the six axes to zero
- `RobotJoints(double axis1, double axis2, double axis3, double axis4, double axis5, double axis6)`: Initializes the six axes
- `double Axis1 { get; set; }`: Value of axis 1
- `double Axis2 { get; set; }`: Value of axis 2
- `double Axis3 { get; set; }`: Value of axis 3
- `double Axis4 { get; set; }`: Value of axis 4
- `double Axis5 { get; set; }`: Value of axis 5
- `double Axis6 { get; set; }`: Value of axis 6
