# underautomation.staubli.soap.internal

## SoapClientBase (controller.soap)

`from underautomation.staubli.soap.internal.soap_client_base import SoapClientBase`

Base class for SOAP client

- `disconnect() -> None`: Disconnect SOAP client from robot
- `get_robots() -> typing.List[Robot]`: Get all the robots handled by this controller
- `get_current_cartesian_joint_position(robot: int=0, tool: CartesianPosition=None, frame: CartesianPosition=None) -> CartesianJointPosition`: Get the Cartesian position and joint positions of a robot
- `get_current_joint_position(robot: int=0) -> typing.List[float]`: Get the current joint position of a robot
- `get_controller_parameters() -> typing.List[Parameter]`: Get the current Cartesian position of a robot end effector
- `get_val_applications() -> typing.List[ValApplication]`: Get all the VAL applications available on the controller
- `get_joint_range(robot: int=0) -> JointRange`: Get the range Min-Max of each joint of a robot
- `get_all_physical_ios() -> typing.List[PhysicalIo]`: Get all the physical I/O values of the controller
- `get_dh_parameters(robot: int=0) -> typing.List[DhParameters]`: Get Robot DH parameters
- `get_tasks() -> typing.List[ControllerTask]`: Get all the tasks available on the controller
- `read_ios(ios: typing.List[str]) -> typing.List[PhysicalIoState]`: Read the state of specified physical I/Os
- `start_application(applicationPath: str) -> None`: Start a VAL application on the controller
- `stop_and_unload_all() -> None`: Stop all VAL applications on the controller
- `stop_application() -> None`: Stop application on the controller
- `task_kill(taskName: str, createdBy: str) -> None`: Kill a task on the controller
- `task_resume(taskName: str, createdBy: str) -> None`: Resume a task on the controller
- `task_suspend(taskName: str, createdBy: str) -> None`: Suspend a task on the controller
- `write_ios(ios: typing.List[str], values: typing.List[float]) -> typing.List[PhysicalIoWriteResponse]`: Write values to specified physical I/Os
- `load_project(projectPath: str) -> None`: Load a project in memory from disk (does not start it)
- `forward_kinematics(robot: int, joints: typing.List[float]) -> IForwardKinematics`: Calculate the forward kinematics of a robot based on its joint positions
- `reverse_kinematics(robot: int, joint: typing.List[float], target: Frame, config: Config, jointRange: JointRange) -> IReverseKinematics`: Calculate the reverse kinematics of a robot to reach a target position and orientation
- `move_c(robot: int, frameB: Frame, frameC: Frame, mdesc: MotionDesc) -> IMoveResult`: Move the robot to a target position using a Cartesian path
- `move_jc(robot: int, frame: Frame, mdesc: MotionDesc) -> IMoveResult`: Move the robot to a target position using a Cartesian path with joint constraints
- `move_jj(robot: int, joints: typing.List[float], mdesc: MotionDesc) -> IMoveResult`: Move the robot to a target position using joint positions
- `move_l(robot: int, frame: Frame, mdesc: MotionDesc) -> IMoveResult`: Move the robot to a target position using a linear path in Cartesian space
- `reset_motion() -> MotionReturnCode`: Reset the motion of the robot
- `restart_motion() -> MotionReturnCode`: Restart the motion of the robot
- `stop_motion() -> MotionReturnCode`: Stop the motion of the robot immediately
- `set_power(power: bool) -> PowerReturnCode`: Set the power state of the robot (controller mut be in remote mode)
- `ip: str (read only)`: Connected robot IP address or host name
- `port: int (read only)`: SOAP TCP port
- `session_id: int (read only)`: Session ID for the SOAP connection
- `enabled: bool (read only)`: Check if the SOAP client is connected to a robot

## SoapClientInternal (controller.soap)

`from underautomation.staubli.soap.internal.soap_client_internal import SoapClientInternal`

Internal class for SOAP client, do not use directly

- Inherited from [SoapClientBase](underautomation.staubli.soap.internal.md#soapclientbase-controllersoap): `disconnect`, `get_robots`, `get_current_cartesian_joint_position`, `get_current_joint_position`, `get_controller_parameters`, `get_val_applications`, `get_joint_range`, `get_all_physical_ios`, `get_dh_parameters`, `get_tasks`, `read_ios`, `start_application`, `stop_and_unload_all`, `stop_application`, `task_kill`, `task_resume`, `task_suspend`, `write_ios`, `load_project`, `forward_kinematics`, `reverse_kinematics`, `move_c`, `move_jc`, `move_jj`, `move_l`, `reset_motion`, `restart_motion`, `stop_motion`, `set_power`, `ip`, `port`, `session_id`, `enabled`

## SoapConnectParametersBase

`from underautomation.staubli.soap.internal.soap_connect_parameters_base import SoapConnectParametersBase`

Base class for SOAP connection parameters

- `SoapConnectParametersBase()`
- `user: str`: Username for the SOAP service (default: default)
- `password: str`: Password for the SOAP service (default: default)
- `port: int`: Port of the SOAP service. Default: 0 (automatic). With 0, the SDK uses 851 for a real controller, and the SOAP port of the network configuration of a controller emulated by Staubli Robotics Suite (851 when it is not found).
