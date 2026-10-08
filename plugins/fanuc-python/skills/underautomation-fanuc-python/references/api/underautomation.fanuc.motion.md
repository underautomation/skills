# underautomation.fanuc.motion

## FanucMotion

`from underautomation.fanuc.motion.fanuc_motion import FanucMotion`

Conversions between the FANUC types (positions, FINE/CNT/CR terminations, I/O types) and the types of the motion planner of namespace UnderAutomation.Robotics.Motion.

- `static to_cartesian_pose(position: XYZWPRPosition) -> CartesianPose`: Converts a FANUC position to a pose. The extended axes E1, E2 and E3 are copied when the position is an ExtendedCartesianPosition.
- `static to_extended_cartesian_position(pose: CartesianPose, reference: XYZWPRPosition) -> ExtendedCartesianPosition`: Converts a pose to a FANUC position with extended axes (0 when the pose has no external axes).
- `static to_joint_values(position: JointsPosition) -> JointValues`: Converts a FANUC joint position (J1 to J9) to joint values
- `static to_joints_position(values: JointValues) -> JointsPosition`: Converts joint values to a FANUC joint position. Missing axes are 0.
- `static fine() -> Termination`: FINE termination: the robot stops at the target position
- `static cnt(value: int) -> Termination`: CNT termination: the next motion starts during the deceleration of this one
- `static cr(distance: float) -> Termination`: CR termination (corner region): the corner is replaced by a smooth curve at constant speed. Only between Cartesian motions.
- `static signal(type: IOType, index: int) -> DigitalSignal`: Returns the digital signal of an I/O, to write it during a trajectory (for example DO[5])
- `static from_cartesian_samples(samples: typing.List[XYZWPRPosition], cycleTime: float) -> Trajectory`: Creates a Cartesian trajectory from FANUC positions taken at a fixed period. The W, P, R angles are kept without any change, and the extended axes are used when the positions are ExtendedCartesianPosition.
- `static sample_cartesian(trajectory: Trajectory, cycleTime: float) -> typing.List[ExtendedCartesianPosition]`: Samples a Cartesian trajectory at a fixed period and returns FANUC positions. The W, P, R angles stay continuous from one position to the next.
- `static wpr_convention: EulerConvention (read only)`: Convention of the W, P, R angles of FANUC positions: rotation W around the fixed X axis, then P around the fixed Y axis, then R around the fixed Z axis
