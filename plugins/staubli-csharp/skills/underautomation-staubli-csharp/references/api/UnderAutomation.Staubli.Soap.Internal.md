# UnderAutomation.Staubli.Soap.Internal

## SoapClientBase (controller.Soap)

`abstract class SoapClientBase`

Base class for SOAP client

- `void Disconnect()`: Disconnect SOAP client from robot
- `bool Enabled { get; }`: Check if the SOAP client is connected to a robot
- `IForwardKinematics ForwardKinematics(int robot, double[] joints)`: Calculate the forward kinematics of a robot based on its joint positions
- `PhysicalIo[] GetAllPhysicalIos()`: Get all the physical I/O values of the controller
- `Parameter[] GetControllerParameters()`: Get the current Cartesian position of a robot end effector
- `CartesianJointPosition GetCurrentCartesianJointPosition(int robot = 0, CartesianPosition tool = null, CartesianPosition frame = null)`: Get the Cartesian position and joint positions of a robot
- `double[] GetCurrentJointPosition(int robot = 0)`: Get the current joint position of a robot
- `DhParameters[] GetDhParameters(int robot = 0)`: Get Robot DH parameters
- `JointRange GetJointRange(int robot = 0)`: Get the range Min-Max of each joint of a robot
- `Robot[] GetRobots()`: Get all the robots handled by this controller
- `ControllerTask[] GetTasks()`: Get all the tasks available on the controller
- `ValApplication[] GetValApplications()`: Get all the VAL applications available on the controller
- `string Ip { get; }`: Connected robot IP address or host name
- `void LoadProject(string projectPath)`: Load a project in memory from disk (does not start it)
- `IMoveResult MoveC(int robot, Frame frameB, Frame frameC, MotionDesc mdesc)`: Move the robot to a target position using a Cartesian path
- `IMoveResult MoveJC(int robot, Frame frame, MotionDesc mdesc)`: Move the robot to a target position using a Cartesian path with joint constraints
- `IMoveResult MoveJJ(int robot, double[] joints, MotionDesc mdesc)`: Move the robot to a target position using joint positions
- `IMoveResult MoveL(int robot, Frame frame, MotionDesc mdesc)`: Move the robot to a target position using a linear path in Cartesian space
- `int Port { get; }`: SOAP TCP port
- `PhysicalIoState[] ReadIos(string[] ios)`: Read the state of specified physical I/Os
- `MotionReturnCode ResetMotion()`: Reset the motion of the robot
- `MotionReturnCode RestartMotion()`: Restart the motion of the robot
- `IReverseKinematics ReverseKinematics(int robot, double[] joint, Frame target, Config config, JointRange jointRange)`: Calculate the reverse kinematics of a robot to reach a target position and orientation
- `int SessionId { get; }`: Session ID for the SOAP connection
- `PowerReturnCode SetPower(bool power)`: Set the power state of the robot (controller mut be in remote mode)
- `void StartApplication(string applicationPath)`: Start a VAL application on the controller
- `void StopAndUnloadAll()`: Stop all VAL applications on the controller
- `void StopApplication()`: Stop application on the controller
- `MotionReturnCode StopMotion()`: Stop the motion of the robot immediately
- `void TaskKill(string taskName, string createdBy)`: Kill a task on the controller
- `void TaskResume(string taskName, string createdBy)`: Resume a task on the controller
- `void TaskSuspend(string taskName, string createdBy)`: Suspend a task on the controller
- `PhysicalIoWriteResponse[] WriteIos(string[] ios, double[] values)`: Write values to specified physical I/Os

## SoapClientInternal (controller.Soap)

`class SoapClientInternal : SoapClientBase`

Internal class for SOAP client, do not use directly

- Inherited from [SoapClientBase](UnderAutomation.Staubli.Soap.Internal.md#soapclientbase-controllersoap): `Disconnect`, `GetRobots`, `GetCurrentCartesianJointPosition`, `GetCurrentJointPosition`, `GetControllerParameters`, `GetValApplications`, `GetJointRange`, `GetAllPhysicalIos`, `GetDhParameters`, `GetTasks`, `ReadIos`, `StartApplication`, `StopAndUnloadAll`, `StopApplication`, `TaskKill`, `TaskResume`, `TaskSuspend`, `WriteIos`, `LoadProject`, `ForwardKinematics`, `ReverseKinematics`, `MoveC`, `MoveJC`, `MoveJJ`, `MoveL`, `ResetMotion`, `RestartMotion`, `StopMotion`, `SetPower`, `Ip`, `Port`, `SessionId`, `Enabled`

## SoapConnectParametersBase

`class SoapConnectParametersBase`

Base class for SOAP connection parameters

- `SoapConnectParametersBase()`
- `string Password { get; set; }`: Password for the SOAP service (default: default)
- `int Port { get; set; }`: Port of the SOAP service. Default: 0 (automatic). With 0, the SDK uses 851 for a real controller, and the SOAP port of the network configuration of a controller emulated by Staubli Robotics Suite (851 when it is not found).
- `string User { get; set; }`: Username for the SOAP service (default: default)
