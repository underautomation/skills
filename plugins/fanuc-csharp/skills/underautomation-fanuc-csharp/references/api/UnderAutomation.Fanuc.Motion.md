# UnderAutomation.Fanuc.Motion

## FanucMotion

`static class FanucMotion`

Conversions between the FANUC types (positions, FINE/CNT/CR terminations, I/O types) and the types of the motion planner of namespace UnderAutomation.Robotics.Motion.

- `static Termination Cnt(int value)`: CNT termination: the next motion starts during the deceleration of this one
- `static Termination Cr(double distance)`: CR termination (corner region): the corner is replaced by a smooth curve at constant speed. Only between Cartesian motions.
- `static Termination Fine()`: FINE termination: the robot stops at the target position
- `static Trajectory FromCartesianSamples(XYZWPRPosition[] samples, double cycleTime)`: Creates a Cartesian trajectory from FANUC positions taken at a fixed period. The W, P, R angles are kept without any change, and the extended axes are used when the positions are Common.ExtendedCartesianPosition.
- `static ExtendedCartesianPosition[] SampleCartesian(Trajectory trajectory, double cycleTime)`: Samples a Cartesian trajectory at a fixed period and returns FANUC positions. The W, P, R angles stay continuous from one position to the next.
- `static DigitalSignal Signal(IOType type, int index)`: Returns the digital signal of an I/O, to write it during a trajectory (for example DO[5])
- `static CartesianPose ToCartesianPose(XYZWPRPosition position)`: Converts a FANUC position to a pose. The extended axes E1, E2 and E3 are copied when the position is an Common.ExtendedCartesianPosition.
- `static ExtendedCartesianPosition ToExtendedCartesianPosition(CartesianPose pose, XYZWPRPosition reference)`: Converts a pose to a FANUC position with extended axes (0 when the pose has no external axes).
- `static JointValues ToJointValues(JointsPosition position)`: Converts a FANUC joint position (J1 to J9) to joint values
- `static JointsPosition ToJointsPosition(JointValues values)`: Converts joint values to a FANUC joint position. Missing axes are 0.
- `static EulerConvention WprConvention { get; }`: Convention of the W, P, R angles of FANUC positions: rotation W around the fixed X axis, then P around the fixed Y axis, then R around the fixed Z axis
