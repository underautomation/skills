# API index: UnderAutomation Yaskawa SDK, C#

SDK version 3.0.1. One line per public type, grouped by namespace: name, then summary. Open the namespace file to read the members of a type.

## UnderAutomation.Yaskawa

File: [UnderAutomation.Yaskawa.md](UnderAutomation.Yaskawa.md)

- ConnectParameters: Contains a set of connection parameters for robot communication. Supports High Speed Ethernet Server and Host Control protocols.
- YaskawaRobot: Main entry point for communicating with Yaskawa Motoman robots. This class provides methods to connect, monitor, and control the robot through multiple interfaces: High Speed Ethernet Server, Ethernet Server (Host Control over TCP), HTTP and FTP.

## UnderAutomation.Yaskawa.Common

File: [UnderAutomation.Yaskawa.Common.md](UnderAutomation.Yaskawa.Common.md)

- AlarmEntry: Default implementation of Common.IAlarmEntry.
- CartesianPosition: Cartesian position of the robot flange in the robot frame.
- ConnectException: Exception thrown when connection to a Yaskawa robot fails
- DhParameters: Denavit-Hartenberg parameters of a 6-axis Yaskawa arm (axes S, L, U, R, B, T).
- FileExtension: Represents the file types available on a Yaskawa robot controller.
- IAlarmEntry: Represents an active alarm on a Yaskawa robot controller.
- IAlarmReader: Provides access to active alarm information from the robot controller.
- ICartesianPosition: Represents a robot Cartesian position (TCP position and orientation).
- IDhParameters: Denavit-Hartenberg parameters of a 6-axis Yaskawa arm (axes S, L, U, R, B, T).
- IFileManager: Provides complete file management: read, write, list, and delete operations.
- IFileReader: Provides file read operations: download files and list directory contents.
- IFileWriter: Provides file write and delete operations on the robot controller.
- IIOAccess: Provides read/write access to robot I/O signals.
- IJobData: Represents information about the currently executing job on a Yaskawa robot controller.
- IJointAngles: Represents a joint position of a 6-axis arm in degrees, with the same signs as the pendant.
- IJointPulses: Represents a robot joint position in pulse (encoder) values.
- IMotionControl: Provides motion commands to move the robot.
- IOType: Yaskawa Motoman I/O signal type categories.
- IPositionReader: Provides access to current robot position readings.
- IRobotClient: Super-interface that combines all robot control capabilities. Implemented by High Speed Ethernet Server and Host Control clients.
- IRobotControl: Provides robot control commands: alarm reset, servo, hold, cycle, job and display.
- IStatusData: Represents the operational status of a Yaskawa robot controller. Common status flags shared across all communication protocols.
- IStatusReader: Provides access to robot status and executing job information.
- ITorqueReader: Provides access to robot axis torque readings.
- IVariableAccess: Provides typed read/write access to robot controller variables.
- IYaskawaClient: Base interface for all Yaskawa robot communication clients. Provides connection management shared across all communication protocols.
- IoHelpers: Helper methods for handling Yaskawa I/O group conversions and related utilities.
- JointsAngles: Joint angles of a 6-axis arm, in degrees, with the same signs as the pendant (axes S, L, U, R, B, T).
- KinematicsCategory: Kinematic structure of a 6-axis arm. It decides which inverse kinematics solver is used.
- RobotCycleType: Specifies the execution cycle type.
- RobotMode: Specifies the robot operation mode.

## UnderAutomation.Yaskawa.Ftp

File: [UnderAutomation.Yaskawa.Ftp.md](UnderAutomation.Yaskawa.Ftp.md)

- FtpClient: Standalone FTP client for connecting directly to a Yaskawa robot controller.
- FtpConnectParameters: Connection parameters for FTP communication with the Yaskawa robot controller.
- FtpErrorReason: Reason why an FTP operation failed.
- FtpException: Exception thrown when an FTP operation on the Yaskawa controller fails. The message explains the cause and, when the logged user does not have enough rights, which user to use.
- FtpFileSystemObjectType: Type of an item on the controller file system.
- FtpListItem: Represents a file or a folder on the robot controller.
- FtpOperation: FTP operation that was running when an Ftp.FtpException was thrown.
- OnProgressDelegate: Delegate used to report file transfer progress.

## UnderAutomation.Yaskawa.Ftp.Internal

File: [UnderAutomation.Yaskawa.Ftp.Internal.md](UnderAutomation.Yaskawa.Ftp.Internal.md)

- FtpClientBase: Abstract base class that implements FTP communication with a Yaskawa robot controller. Provides file management (upload, download, list, delete) via the controller's FTP server.
- FtpClientInternal: Internal implementation of the FTP client. This class is not intended for direct use by application code. Use Yaskawa.YaskawaRobot instead.
- FtpConnectParametersInternal: FTP connection parameters with an enable flag, used by Yaskawa.ConnectParameters.

## UnderAutomation.Yaskawa.HighSpeedEServer

File: [UnderAutomation.Yaskawa.HighSpeedEServer.md](UnderAutomation.Yaskawa.HighSpeedEServer.md)

- AlarmResetType: Specifies the type of alarm reset operation to perform.
- ArmFlipInformation: Specifies the arm configuration (upper/lower) based on L and U axis positions.
- AxisFlipInformation: Specifies whether an axis angle is less than or greater than/equal to 180 degrees. Used for determining robot configuration in multi-solution situations.
- ControlGroup: Defines control group types for robot systems. Control groups organize different motion units within the robot system.
- FlipNoFlipInformation: Specifies the flip/no-flip wrist configuration.
- GetFileProgress: Contains progress information for file download (GetFile) operations. Used with the GetFileProgressDelegate callback to track download progress.
- HighSpeedEServerClient: Main client class for communicating with Yaskawa Motoman industrial robots using the High Speed Ethernet Server protocol. This class provides methods for reading robot status, positions, variables, and controlling robot operations via UDP.
- HighSpeedEServerConnectParameters: Base class defining connection parameters for the High Speed Ethernet Server communication. This class cannot be instantiated directly; use a derived class or use Connect with optional parameters. Allows customization of timeouts and ports for different network environments.
- InvalidDataAnswerException: Exception thrown when the robot controller returns an error response to a High Speed Ethernet Server command. This exception contains detailed status codes that help identify the specific error condition.
- LoadFileProgress: Contains progress information for file upload (LoadFile) operations. Used with the LoadFileProgressDelegate callback to track upload progress.
- ManagementTimeType: Specifies the type of management time data to retrieve. Different metrics track various aspects of robot operation.
- OnOffCommandType: Specifies the type of ON/OFF command to send to the robot controller. These commands control fundamental robot states that affect safety and operation.
- OrientationFlipInformation: Specifies the orientation (front/back) configuration of the robot arm. Determined by the position of the B-axis rotation center relative to the S-axis.
- PositionCommandClassification: Specifies the speed classification (units) for motion commands. Determines how the speed value is interpreted by the controller.
- PositionCommandOperationCoordinate: Specifies the coordinate system for position command interpretation. Determines how X, Y, Z, Rx, Ry, Rz values are interpreted.
- PositionCommandType: Specifies the type of position command (motion instruction) to execute. Determines the path type and whether position is absolute or incremental.
- RegardedReversePositionSpecified: Specifies how to handle position in reverse direction scenarios.
- RobotAlarmData: Contains information about a robot alarm retrieved from the controller. Alarms indicate error conditions that may require operator intervention.
- RobotAlarmDataExtended: Contains extended information about a robot alarm, including sub-code details. Provides more detailed diagnostic information than the basic RobotAlarmData.
- RobotAxisConfigData: Represents raw axis data with string values for axis configuration information. Used to retrieve axis name/type information from the robot controller.
- RobotAxisIntData: Represents raw axis data with 32-bit integer values for up to 8 axes. This is a concrete implementation commonly used for pulse-based position data.
- RobotAxisRawData<T>: Represents raw axis data with generic value type for up to 8 axes. This is the base class for position-related data structures.
- RobotBasePositionData: Represents base position data for coordinated motion with travel units or external bases. Base positions define the location of the robot's base in world coordinates or pulse values.
- RobotBasePositionType: Defines the type of base position data representation.
- RobotBasePositionVariableData: Represents data returned from reading multiple base position variables (BP variables) from the robot controller. BP variables store base position information used for coordinated motion with external axes or travel units.
- RobotByteVariableData: Represents data returned from reading multiple byte variables (B variables) from the robot controller. B variables are 8-bit unsigned integer storage locations (0-255).
- RobotControlGroup: Represents a robot control group combining a group type with an index. Used to specify which robot or station to query in multi-robot systems.
- RobotData: Base class for all robot data response objects returned by High Speed Ethernet Server commands. Contains common header information about the communication response.
- RobotDataHeader: Information about a response of the robot controller: the controller that answered, the size of the data, and the state of a transfer in several parts.
- RobotDoubleIntegerVariableData: Represents data returned from reading multiple double-precision integer variables (D variables) from the robot controller.
- RobotExternalAxisData: Represents external axis position data for positioners, travel units, or additional servo axes. External axes are coordinated with the robot motion for applications like welding positioners.
- RobotExternalAxisVariableData: Represents data returned from reading multiple external axis variables (EX variables) from the robot controller. EX variables store position data for external axes such as positioners, travel units, or additional servo axes.
- RobotFileContentData: Contains the content of a file downloaded from the robot controller. Provides methods for parsing structured file content such as job files and parameter files.
- RobotFileListData: Contains the result of a file listing operation on the robot controller. Returns an array of file names matching the specified pattern.
- RobotIOData: Represents data returned from reading multiple I/O (Input/Output) points from the robot controller. I/O addresses are organized in groups based on their function and accessibility.
- RobotIntegerVariableData: Represents data returned from reading multiple integer variables (I variables) from the robot controller. I variables are 16-bit signed integer storage locations.
- RobotJobData: Contains information about the currently executing job (program) on the robot controller. Retrieved using the executing job information reading command.
- RobotJobStackData: Contains the job call stack for a specific task on the robot controller. Represents the current nesting of CALL instructions, from the outermost job to the currently executing one. Only supported on DX200 (AY/BY/YN) controllers.
- RobotKinematicsCartesianData: Cartesian position result from a kinematics conversion. Provides named X/Y/Z and orientation properties in engineering units in addition to the raw axis values.
- RobotKinematicsJointData: Joint-space position result from a kinematics conversion. Provides the 8 joint axis values in both raw 0.0001° units and as a ready-to-use degrees array.
- RobotKinematicsPositionData: Base class for kinematic position data exchanged with the robot controller. Contains coordinate type, posture flags, tool/user numbers, and the 8 raw axis values.
- RobotManagementTimeData: Contains management time information for tracking robot operation statistics. Provides uptime and usage metrics for maintenance planning and reporting.
- RobotPluralData<T>: Represents a collection of data values returned from plural (batch) read operations. Used for reading multiple variables, registers, or I/O points in a single request.
- RobotPositionCartesianData: Represents Cartesian position data with coordinates in millimeters and degrees. This class provides human-readable position data converted from the raw protocol values.
- RobotPositionData<T>: Represents generic robot position data with axis values of the specified type. This class provides a flexible structure for storing position information that can be represented in different data formats (pulse values, Cartesian coordinates, etc.).
- RobotPositionDataType: Defines the coordinate system type for position data.
- RobotPositionIntData: Represents robot position data with 32-bit integer axis values. This is the primary type used for pulse-based position data from the High Speed Ethernet Server. Axis values are in pulse units (encoder counts) or scaled coordinate values.
- RobotPositionVariableData: Represents data returned from reading multiple position variables (P variables) from the robot controller. P variables store complete robot position data including coordinates, posture, tool and user coordinate references.
- RobotPosture: Represents the complete robot posture (form) configuration. Encodes the kinematic configuration choices that determine which of multiple inverse kinematics solutions is used to reach a Cartesian position.
- RobotRealVariableData: Represents data returned from reading multiple real variables (R variables) from the robot controller. R variables are 32-bit single-precision floating point storage locations.
- RobotRecentAlarm: Specifies which recent alarm to retrieve from the robot controller. The controller maintains a history of the most recent alarms.
- RobotRegisterData: Represents data returned from reading multiple register values from the robot controller. Registers are 16-bit signed integer storage locations used for general-purpose data.
- RobotStatusData: Contains the current operational status of the robot controller. Provides information about the robot's mode, running state, and safety conditions. Retrieved using the status information reading command.
- RobotStringVariableData: Represents data returned from reading multiple string variables (S variables) from the robot controller. S variables can be either 16-byte or 32-byte character strings depending on the command used.
- RobotSystemInformation: Contains system information about the robot controller including software version and configuration. Retrieved using the system information acquiring command.
- RobotSystemParamData: Contains a system parameter value read from the robot controller.
- RobotSystemType: Defines the types of system components that can be queried for information.
- RobotSystemTypeData: Represents a system type and index combination for querying specific robot system components. Used to specify which robot, station, or application to query in multi-robot configurations.
- SwitchingCommands: Specifies the execution mode switching command to send to the robot controller. These modes control how the robot executes programmed jobs.
- SystemParameterTypes: Specifies the category of a system parameter to read from the controller. Types S1CG, AP, and SE require a group number when reading.

## UnderAutomation.Yaskawa.HighSpeedEServer.Internal

File: [UnderAutomation.Yaskawa.HighSpeedEServer.Internal.md](UnderAutomation.Yaskawa.HighSpeedEServer.Internal.md)

- HighSpeedEServerClientBase.GetFileProgressDelegate: Delegate for receiving file download progress notifications.
- HighSpeedEServerClientBase.LoadFileProgressDelegate: Delegate for receiving file upload progress notifications.
- HighSpeedEServerClientBase: Base class of the High Speed Ethernet Server client of a Yaskawa robot controller. Provides methods for reading robot status, positions, variables, and executing commands via UDP.
- HighSpeedEServerClientInternal: Internal implementation of the High Speed Ethernet Server client. This class provides the concrete implementation used internally by the SDK.
- HighSpeedEServerConnectParametersInternal: Represents a set of High Speed Ethernet Server connection parameters

## UnderAutomation.Yaskawa.HostControl

File: [UnderAutomation.Yaskawa.HostControl.md](UnderAutomation.Yaskawa.HostControl.md)

- EServerClient: Standalone client class for communicating with Yaskawa Motoman industrial robots using the Host Control protocol via Ethernet Server (TCP). This class provides methods for reading robot status, positions, variables, and controlling robot operations.
- EServerConnectParameters: Base class defining Ethernet Server (TCP) connection parameters for the Host Control communication. This class provides configuration for TCP-based communication with YRC1000 controllers.
- HostControlAlarmData: Contains alarm information retrieved from the robot controller.
- HostControlAlarmEntry: Represents a single alarm entry with code, sub-code and text description.
- HostControlAlarmStringData: Contains alarm information with text messages retrieved from the robot controller.
- HostControlCartesianPositionData: Contains Cartesian position data (TCP position and orientation).
- HostControlCoordinateSystem: Specifies the coordinate system for position commands.
- HostControlCycleType: Specifies the execution cycle type.
- HostControlEncoderTemperatureData: Contains encoder temperature values for each robot axis. Retrieved using the RENCTMP command.
- HostControlException: Exception thrown when a Host Control command fails.
- HostControlGroupData: Contains control group information. Retrieved using the RGROUP command.
- HostControlIOData: Contains I/O signal data.
- HostControlJobData: Contains information about the currently executing job (program). Retrieved using the RJSEQ command.
- HostControlJobDirectoryData: Contains job directory listing data. Retrieved using the RJDIR command.
- HostControlJointPositionData: Contains joint position data in pulse (encoder) values.
- HostControlResponse: Base class for all robot data response objects returned by Host Control commands. Contains common response information about the communication.
- HostControlResponseCode: Specifies the interpreter error/response codes.
- HostControlRobotMode: Specifies the robot mode.
- HostControlSpeedType: Specifies the speed type for motion commands.
- HostControlStatusData: Contains the current operational status of the robot controller. Provides information about the robot's mode, running state, and safety conditions.
- HostControlSystemTimeData: Contains system time information from the robot controller. Retrieved using the RSYSTM command.
- HostControlTorqueData: Contains torque values for each robot axis. Retrieved using the RTRQ (current torque) or RMAXTRQ (maximum torque) commands.
- HostControlUserFrameData: Contains user coordinate frame data defined by three reference points (ORG, XX, XY). Retrieved using the RUFRAME command, written using the WUFRAME command.
- HostControlVariableType: Specifies the type of variable to read or write.

## UnderAutomation.Yaskawa.HostControl.Internal

File: [UnderAutomation.Yaskawa.HostControl.Internal.md](UnderAutomation.Yaskawa.HostControl.Internal.md)

- EServerClientInternal: Internal implementation of the Host Control client for Ethernet Server (TCP) communication. Supports YRC1000 and compatible controllers.
- EServerConnectParametersInternal: Connection parameters for Host Control Ethernet Server (TCP) communication. Use this class to configure network settings for TCP connection to YRC1000 and compatible controllers.
- HostControlClientBase: Base class implementing the Host Control protocol for Yaskawa robot communication. Provides methods for reading robot status, positions, variables, and executing commands.
- HostControlConnectParametersBase: Base class defining connection parameters for the Host Control communication. This class cannot be instantiated directly; use HostControl.EServerConnectParameters instead.

## UnderAutomation.Yaskawa.Http

File: [UnderAutomation.Yaskawa.Http.md](UnderAutomation.Yaskawa.Http.md)

- FileDescription: Describes a file available on the robot controller.
- HttpClient: Standalone client class for communicating with Yaskawa Motoman industrial robots via HTTP. Provides file listing and file content retrieval from the robot controller's built-in web server.
- HttpConnectParameters: Connection parameters for HTTP communication with the robot controller.

## UnderAutomation.Yaskawa.Http.Internal

File: [UnderAutomation.Yaskawa.Http.Internal.md](UnderAutomation.Yaskawa.Http.Internal.md)

- HttpClientBase: Base class implementing HTTP communication with Yaskawa robot controllers. Provides file listing and file content retrieval via the controller's built-in HTTP server.
- HttpClientInternal: Internal implementation of the HTTP client. This class is not intended for direct use by application code. Use Yaskawa.YaskawaRobot instead.
- HttpConnectParametersInternal: Connection parameters for HTTP communication with the robot controller, with enable flag.

## UnderAutomation.Yaskawa.Kinematics

File: [UnderAutomation.Yaskawa.Kinematics.md](UnderAutomation.Yaskawa.Kinematics.md)

- ArmKinematicModels: Yaskawa Robot Known Arm Models
- KinematicsUtils: Forward and inverse kinematics of 6-axis Yaskawa arms.

## UnderAutomation.Yaskawa.License

File: [UnderAutomation.Yaskawa.License.md](UnderAutomation.Yaskawa.License.md)

- InvalidLicenseException: Exception thrown while using the product if the license is not valid.
- LicenseInfo: Information about a license key
- LicenseState: States that can take a license
