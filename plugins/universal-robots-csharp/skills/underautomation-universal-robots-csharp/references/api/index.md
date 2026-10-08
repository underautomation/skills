# API index: UnderAutomation Universal Robots SDK, C#

SDK version 9.4.0. One line per public type, grouped by namespace: name, then summary. Open the namespace file to read the members of a type.

## UnderAutomation.UniversalRobots

File: [UnderAutomation.UniversalRobots.md](UnderAutomation.UniversalRobots.md)

- ConnectParameters: Contains parameters to connect to the robot
- UR: Main entry point for connecting to and interacting with a Universal Robots controller. Provides access to all communication interfaces: Primary Interface, Dashboard, RTDE, SSH, SFTP, XML-RPC, Socket Communication, Interpreter Mode, and REST API.

## UnderAutomation.UniversalRobots.Common

File: [UnderAutomation.UniversalRobots.Common.md](UnderAutomation.UniversalRobots.Common.md)

- AnalogRanges: Analog units of analog inputs and outputs
- CartesianCoordinates: Represents a cartesian pose with 3 translations and 3 rotations
- ConnectException: Exception thrown when connection to the robot fails
- ControlModes: Robot control modes
- ControllerBoxTypes: Controller box types
- DashboardConnectParameters: Setup Dashboard Client
- DigitalOutputConfigurations: Digital output configuration (NPN, PNP, Push/Pull)
- GlobalVariable: Describes a global variable
- GlobalVariableTypes: Possible types of a variable
- GlobalVariableValue: Describes a typed variable value
- IUrDhParameters: Denavit–Hartenberg (DH) parameters for Universal Robots with only the relevant parameters
- InternalErrorEventArgs: Describes an internal error
- InterpreterModeConnectParameters: Setup Interpreter Mode Client
- JointModes: Joint modes
- JointsDoubleValues: Represents a set of 6 double-precision values, one per robot joint. Typically used for angles (radians), velocities, currents, etc.
- JointsIntValues: Represents a set of 6 integer values, one per robot joint. Typically used for joint modes, statuses, or other discrete joint data.
- JointsValues<T>: Vector 6 of double values representing each robot joint
- OutputModes: Digital output modes
- PackageEventArgs: Base class of all received data packages
- Pose: Represents a UR pose
- PrimaryInterfaceConnectParameters: Setup Primary Interface Client communication
- RestConnectParameters: Configuration parameters for REST API connection (PolyscopeX only)
- RobotModels: Model of a UR robot
- RobotModelsExtended: Model of a UR robot (including e-Series and extended payload models)
- RobotModes: Robot running modes
- RobotSubTypes: Robot sub type (e-Serie or CB-Serie)
- RtdeConnectParameters: Setup RTDE (Real-Time Data Exchange) client communication
- SafetyStatus: Safety modes
- SocketCommunicationConnectParameters: Setup socket communication server
- SshConnectParameters: Setup SSH client
- StatusCode: Status code that describes an internal error or an internal action
- ToolModes: Tool modes
- Vector3D: Represents a three-dimensional vector with X, Y, and Z components.
- XmlRpcConnectParameters: Setup XML-RPC server

## UnderAutomation.UniversalRobots.Dashboard

File: [UnderAutomation.UniversalRobots.Dashboard.md](UnderAutomation.UniversalRobots.Dashboard.md)

- CommandResponse<T>: Answer returned by a command which contains a typed value.
- CommandResponse: Generic answer returned by a command
- DashboardClient: Client for the Universal Robots Dashboard Server protocol. Enables remote control of the robot (load/play/stop programs, power on/off, etc.) via TCP commands on port 29999.
- OperationalModes: Enumerates all robot operational modes
- PolyscopeVersion: Describes a Polyscope version (robot controller firmware).
- ProgramSaveState: Represents the save state of the currently loaded program on the Universal Robots controller.
- ProgramState: Describes a program state (its running state and its name)
- ProgramStates: Enumerate possible states of a program.
- UserRoles: Enumerates all user roles

## UnderAutomation.UniversalRobots.Dashboard.Internal

File: [UnderAutomation.UniversalRobots.Dashboard.Internal.md](UnderAutomation.UniversalRobots.Dashboard.Internal.md)

- DashboardClientBase: Abstract base class providing Dashboard Server command implementations for the Universal Robots controller. Sends text-based commands over TCP and parses responses. A new TCP connection is created for each command.
- DashboardClientParametersBase: Abstract base class for Dashboard Server connection parameters, providing default port and timeout values.

## UnderAutomation.UniversalRobots.Files

File: [UnderAutomation.UniversalRobots.Files.md](UnderAutomation.UniversalRobots.Files.md)

- URArchive: Contains basic methods to encode and decode a UR archive
- URInstallation: Functions to encode and decode a *.installation file
- URProgram: Functions to compile and decompile a *.urp program file

## UnderAutomation.UniversalRobots.Internal

File: [UnderAutomation.UniversalRobots.Internal.md](UnderAutomation.UniversalRobots.Internal.md)

- DashboardClientInternal: Internal implementation of the Dashboard Server client that delegates connection to the parent UniversalRobots.UR instance.
- InterpreterModeClientInternal: Internal implementation of the Interpreter Mode client that delegates connection to the parent UniversalRobots.UR instance.
- PrimaryInterfaceClientInternal: Internal implementation of the Primary Interface client that delegates connection to the parent UniversalRobots.UR instance.
- RestClientInternal: Internal REST client for use within the UR class
- RtdeClientInternal: Internal implementation of the Real-Time Data Exchange (RTDE) client that delegates connection to the parent UniversalRobots.UR instance.
- RtdeOverrunException: Exception thrown when RTDE data cannot be consumed fast enough, causing the input buffer to fill up. This typically occurs when the OutputDataReceived event handler takes longer to execute than the interval between RTDE messages.
- SftpClientInternal: Implementation of the SSH File Transfer Protocol (SFTP) over SSH for transfering files to the robot controller
- SocketCommunicationServerInternal: Internal implementation of the socket communication server used for bidirectional data exchange with UR scripts.
- SshClientInternal: Provides a client connection to SSH server
- URServiceBase: Base class of all UR services implemented in this SDK
- XmlRpcServerInternal: Internal implementation of the XML-RPC server used to expose methods callable by URScript programs on the robot.

## UnderAutomation.UniversalRobots.InterpreterMode

File: [UnderAutomation.UniversalRobots.InterpreterMode.md](UnderAutomation.UniversalRobots.InterpreterMode.md)

- CommandResponse: Response to an Interpreter Mode command
- CommandResponseStatus: Type of response of an Interpreter Mode command
- InterpreterModeClient: Client for the Universal Robots Interpreter Mode, allowing real-time execution of URScript commands over TCP.

## UnderAutomation.UniversalRobots.InterpreterMode.Internal

File: [UnderAutomation.UniversalRobots.InterpreterMode.Internal.md](UnderAutomation.UniversalRobots.InterpreterMode.Internal.md)

- InterpreterModeClientBase: Base class for the Interpreter Mode client, providing TCP communication and built-in interpreter commands.
- InterpreterModeClientParametersBase: Base class for Interpreter Mode connection parameters.

## UnderAutomation.UniversalRobots.Kinematics

File: [UnderAutomation.UniversalRobots.Kinematics.md](UnderAutomation.UniversalRobots.Kinematics.md)

- CustomUrDhParameters: Mutable Denavit-Hartenberg parameters for a Universal Robots arm, allowing custom DH values.
- KinematicsResult: Result of a forward kinematics calculation
- KinematicsUtils: ========================================================================================================= Implementation notes : --------------------------------------------------------------------------------------------------------- This class implements forward and inverse kinematics for a 6-D...
- SingularityType: Types of singularities
- TransformationSet: Set of transformation matrices for each joint
- Ur10DhParameters: Denavit-Hartenberg parameters for the UR10 robot (CB-Series).
- Ur10eDhParameters: Denavit-Hartenberg parameters for the UR10e robot (e-Series).
- Ur12eDhParameters: Denavit-Hartenberg parameters for the UR12e robot (e-Series). Shares the same DH values as the UR10e.
- Ur15DhParameters: Denavit-Hartenberg parameters for the UR15 robot.
- Ur16eDhParameters: Denavit-Hartenberg parameters for the UR16e robot (e-Series).
- Ur18DhParameters: Denavit-Hartenberg parameters for the UR18 robot.
- Ur20DhParameters: Denavit-Hartenberg parameters for the UR20 robot.
- Ur30DhParameters: Denavit-Hartenberg parameters for the UR30 robot.
- Ur3DhParameters: Denavit-Hartenberg parameters for the UR3 robot (CB-Series).
- Ur3eDhParameters: Denavit-Hartenberg parameters for the UR3e robot (e-Series).
- Ur5DhParameters: Denavit-Hartenberg parameters for the UR5 robot (CB-Series).
- Ur5eDhParameters: Denavit-Hartenberg parameters for the UR5e robot (e-Series).
- Ur7eDhParameters: Denavit-Hartenberg parameters for the UR7e robot (e-Series). Shares the same DH values as the UR5e.
- Ur8LongDhParameters: Denavit-Hartenberg parameters for the UR8 Long robot.

## UnderAutomation.UniversalRobots.License

File: [UnderAutomation.UniversalRobots.License.md](UnderAutomation.UniversalRobots.License.md)

- InvalidLicenseException: Exception thrown while using the product if the license is not valid.
- LicenseInfo: Information about a license key
- LicenseState: States that can take a license

## UnderAutomation.UniversalRobots.PrimaryInterface

File: [UnderAutomation.UniversalRobots.PrimaryInterface.md](UnderAutomation.UniversalRobots.PrimaryInterface.md)

- AdditionalInfoPackageEventArgs: Additional information
- CalibrationDataPackageEventArgs: Calibration data
- CartesianInfoPackageEventArgs: Contains current cartesian position of the robot, including its TCP offset
- ConfigurationDataPackageEventArgs: Joint configuration
- ForceModeDataPackageEventArgs: Force mode data
- GlobalVariables: List of all global variables
- GlobalVariablesEventArgs: Event args of variable update events
- GlobalVariablesFirmwareVersion: Firmware version for variable decoding
- Interfaces: TCP ports to communicate with an UR controller
- JointConfiguration: Joint configuration
- JointData: Joint data
- JointDataPackageEventArgs: Status of each joints
- JointKinematicsInfo: Joint kinematics info, Denavit–Hartenberg (DH) parameters
- KeyMessageEventArgs: Internal robot events (such as starting or stopping a program)
- KinematicsInfoPackageEventArgs: Kinematics info
- MasterboardDataPackageEventArgs: Masterboard data
- MasterboardDigitalIO: Represents the state of digital I/O pins on the UR controller masterboard, including standard digital, configurable, and tool digital pins.
- PackageDescriptionAttribute: Describes a field of a received package
- PackageUnit: Physical units of receives measures
- PopupMessageEventArgs: Popup message that appears with the Assignment instruction or the URScript popup() function
- PrimaryInterfaceClient: Primary / Secondary interface implementation
- ProgramThread: Represents a single running thread in a UR program.
- ProgramThreadsEventArgs: Event data containing information about currently running program threads.
- RequestValueMessageEventArgs: Event data for a request value message received from the robot (assignment popup requesting user input).
- RequestedTypes: Types for popup assignment
- RobotModeDataPackageEventArgs: Information about current robot mode
- RuntimeExceptionMessageEventArgs: Reports an error in the execution of the program
- SafetyDataPackageEventArgs: Safety internal data
- SingularityInfoPackageEventArgs: Singularity info
- TextMessageEventArgs: Describes a log message sent with URScript instruction textmsg()
- ToolCommunicationInfoPackageEventArgs: Tool communication info
- ToolDataPackageEventArgs: Tool data
- ToolModeInfoPackageEventArgs: Tool mode info
- VersionEventArgs: Version information from the robot controller firmware

## UnderAutomation.UniversalRobots.PrimaryInterface.Internal

File: [UnderAutomation.UniversalRobots.PrimaryInterface.Internal.md](UnderAutomation.UniversalRobots.PrimaryInterface.Internal.md)

- PrimaryInterfaceClientBase: Base class for the Primary/Secondary Interface client. Manages the TCP connection, decodes incoming binary data packets, and raises events for each decoded sub-package.
- PrimaryInterfaceCommands: Handles Primary interface commands
- PrimaryInterfaceParametersBase: Parameters to setup a Primary/secondary interface connection
- PrimaryInterfaceScript: Handles Primary interface send script feature
- RawPackageReceivedEventArgs: Event args for raw package received

## UnderAutomation.UniversalRobots.Rest

File: [UnderAutomation.UniversalRobots.Rest.md](UnderAutomation.UniversalRobots.Rest.md)

- ProgramStateAction: Actions available for changing the program state via REST API
- ProgramStateResponse: Response from GET /program/v1/state endpoint
- RestApiResponse<T>: Generic response from a REST API call with typed value
- RestApiResponse: Response from a REST API call
- RestApiVersion: REST API version for PolyscopeX robots
- RestClient: Standalone REST API client for PolyscopeX robots. Use this class when you want to interact with the REST API independently from the main UR class.
- RestProgramState: Program state values returned by the REST API
- RobotStateAction: Actions available for changing the robot's operational state via REST API

## UnderAutomation.UniversalRobots.Rest.Internal

File: [UnderAutomation.UniversalRobots.Rest.Internal.md](UnderAutomation.UniversalRobots.Rest.Internal.md)

- RestClientBase: Base implementation of the REST API client for PolyscopeX robots
- RestClientParametersBase: Base parameters for REST API client configuration

## UnderAutomation.UniversalRobots.Rtde

File: [UnderAutomation.UniversalRobots.Rtde.md](UnderAutomation.UniversalRobots.Rtde.md)

- IRtdeRegistersValue: Interface for accessing individual register values within a register array by index.
- RTDEStates: Represents the current state of the RTDE connection lifecycle.
- RtdeBaseValues<T>: Generic abstract base class for getting and setting RTDE variable values identified by enum T.
- RtdeBaseValues: Abstract base class holding a collection of Rtde.RtdeValue instances representing RTDE variable values.
- RtdeBasicRequestEventArgs: Event arguments for a basic RTDE request/response exchange indicating whether the request was accepted by the robot controller.
- RtdeBitRegistersValue: RTDE bit register array (64 registers, indices 64–127) for exchanging boolean flags with the robot.
- RtdeClient: Standalone RTDE client for exchanging real-time data with a Universal Robots controller on TCP port 30004.
- RtdeClientParameters: Parameters for configuring the standalone Rtde.RtdeClient connection to a Universal Robots controller via the RTDE protocol.
- RtdeControlPackageSetupInputsEventArgs: Event arguments raised when the robot acknowledges the RTDE input recipe setup.
- RtdeControlPackageSetupOutputsEventArgs: Event arguments raised when the robot acknowledges the RTDE output recipe setup.
- RtdeDataDescription<T>: Abstract base class that describes a single RTDE variable, including its name, data type, and array layout.
- RtdeDataPackageEventArgs: Event arguments for an RTDE output data package received from the robot at the subscribed frequency.
- RtdeDoubleRegistersValue: RTDE double register array (48 registers, indices 0–47) for exchanging 64-bit floating-point values with the robot.
- RtdeInputData
- RtdeInputDataDescription: Describes a single RTDE input variable (client-to-robot), including its protocol name, type, and array information.
- RtdeInputSetup: Defines the set of RTDE input variables (client-to-robot) to subscribe to as a recipe.
- RtdeInputSetupItem: Represents a single RTDE input variable (client-to-robot) in an input recipe.
- RtdeInputValues: Holds the current values for all RTDE input variables (client-to-robot). Use this to prepare data before calling Rtde.RtdeInputValues).
- RtdeInputsDescription
- RtdeIntRegistersValue: RTDE integer register array (48 registers, indices 0–47) for exchanging 32-bit integer values with the robot.
- RtdeOutputData
- RtdeOutputDataDescription: Describes a single RTDE output variable (robot-to-client), including its protocol name, type, and array information.
- RtdeOutputSetup: Defines the set of RTDE output variables (robot-to-client) to subscribe to as a recipe. The RtdeOutputData.Timestamp variable is added by default.
- RtdeOutputSetupItem: Represents a single RTDE output variable (robot-to-client) in an output recipe.
- RtdeOutputValues: Holds the current values for all RTDE output variables (robot-to-client). Updated automatically when data is received from the robot.
- RtdeOutputsDescription
- RtdeProtocolVersionEventArgs: Event arguments indicating which RTDE protocol version was negotiated with the robot.
- RtdeRegistersValue<T>: Abstract base for a fixed-size register array of type T exchanged through RTDE.
- RtdeTextMessageEventArgs: Event arguments for a text message received from the robot via the RTDE interface.
- RtdeTypes: RTDE data types used to describe the wire format of each RTDE variable.
- RtdeValue<T>: Strongly-typed RTDE variable value of type T.
- RtdeValue: Abstract base class for a single RTDE variable value exchanged between the client and the robot.
- RtdeVersions: RTDE version numbers

## UnderAutomation.UniversalRobots.Rtde.Internal

File: [UnderAutomation.UniversalRobots.Rtde.Internal.md](UnderAutomation.UniversalRobots.Rtde.Internal.md)

- RtdeClientBase: Base class common to all RTDE clients
- RtdeParametersBase: Base parameters to set up RTDE
- RtdeSetup<T, U>: Base class for an RTDE recipe, a collection of T setup items that describe which RTDE variables to exchange.
- RtdeSetupItem<T>: Abstract base class representing a single RTDE variable in a recipe, identified by an enum value of type T and an optional register index.

## UnderAutomation.UniversalRobots.SocketCommunication

File: [UnderAutomation.UniversalRobots.SocketCommunication.md](UnderAutomation.UniversalRobots.SocketCommunication.md)

- ISocketHandler: Interface for classes that support socket messages
- SocketClient: Represent a UR robot connected with URScript function socket_open()
- SocketClientConnectionEventArgs: Event args raised when a socket client is connected with socket_open()
- SocketClientDisconnectionEventArgs: Event args raised when a socket client disconnects
- SocketCommunicationServer: Represents a Socket Communication server to which the robot can connect
- SocketGetVarEventArgs: Event args raised when a socket message sent with socket_get_var() is received
- SocketRequestEventArgs: Event args raised when a socket message is received

## UnderAutomation.UniversalRobots.SocketCommunication.Internal

File: [UnderAutomation.UniversalRobots.SocketCommunication.Internal.md](UnderAutomation.UniversalRobots.SocketCommunication.Internal.md)

- SocketCommunicationParametersBase: Base parameters for socket communication server configuration
- SocketCommunicationServerBase.SocketClientConnectionEventHandler: Event handler of a robot that connects with socket_open()
- SocketCommunicationServerBase.SocketClientDisconnectionEventHandler: Event handler when the robot socket disconnects
- SocketCommunicationServerBase.SocketGetVarEventHandler: Event handler of a socket message sent with socket_get_var()
- SocketCommunicationServerBase.SocketRequestEventHandler: Event handler of a socket message received from robot
- SocketCommunicationServerBase: Base for Socket communication server

## UnderAutomation.UniversalRobots.Ssh

File: [UnderAutomation.UniversalRobots.Ssh.md](UnderAutomation.UniversalRobots.Ssh.md)

- SftpClient: Provides a client for transferring files to and from the Universal Robots controller using the SFTP protocol.
- SshClient: Provides a client connection to SSH server

## UnderAutomation.UniversalRobots.Ssh.Internal

File: [UnderAutomation.UniversalRobots.Ssh.Internal.md](UnderAutomation.UniversalRobots.Ssh.Internal.md)

- SftpClientBase: Implementation of the SSH File Transfer Protocol (SFTP) over SSH for transfering files to the robot controller
- SshClientBase: Provides a client connection to SSH server
- SshParametersBase: Base class for SSH and SFTP connection parameters, including credentials and port configuration.

## UnderAutomation.UniversalRobots.Ssh.Tools

File: [UnderAutomation.UniversalRobots.Ssh.Tools.md](UnderAutomation.UniversalRobots.Ssh.Tools.md)

- ExpectAction: Specifies behavior for expected expression
- Shell: Represents instance of the SSH shell object
- ShellStream: Contains operation for working with SSH Shell.
- SshCommand: Represents SSH command that can be executed.

## UnderAutomation.UniversalRobots.Ssh.Tools.Common

File: [UnderAutomation.UniversalRobots.Ssh.Tools.Common.md](UnderAutomation.UniversalRobots.Ssh.Tools.Common.md)

- ExceptionEventArgs: Provides data for the ErrorOccured events.
- SftpPathNotFoundException: The exception that is thrown when file or directory is not found.
- SftpPermissionDeniedException: The exception that is thrown when operation permission is denied.
- ShellDataEventArgs: Provides data for Shell DataReceived event
- SshAuthenticationException: The exception that is thrown when authentication failed.
- SshConnectionException: The exception that is thrown when connection was terminated.
- SshException: The exception that is thrown when SSH exception occurs.
- SshOperationTimeoutException: The exception that is thrown when operation is timed out.
- SshPassPhraseNullOrEmptyException: The exception that is thrown when pass phrase for key file is empty or null
- TerminalModes: Specifies the initial assignments of the opcode values that are used in the 'encoded terminal modes' valu

## UnderAutomation.UniversalRobots.Ssh.Tools.Sftp

File: [UnderAutomation.UniversalRobots.Ssh.Tools.Sftp.md](UnderAutomation.UniversalRobots.Ssh.Tools.Sftp.md)

- SftpFile: Represents SFTP file information
- SftpFileAttributes: Contains SFTP file attributes.
- SftpFileStream: Exposes a IO.Stream around a remote SFTP file, supporting both synchronous and asynchronous read and write operations.
- SftpFileSytemInformation: Contains File system information exposed by statvfs@openssh.com request.

## UnderAutomation.UniversalRobots.XmlRpc

File: [UnderAutomation.UniversalRobots.XmlRpc.md](UnderAutomation.UniversalRobots.XmlRpc.md)

- XmlRpcArrayValue: Represents an array of XmlRpcValue that can be exchange with the robot via XML-RPC
- XmlRpcBooleanValue: Represents a boolean value that can be exchange with the robot via XML-RPC
- XmlRpcDoubleValue: Represents a double value that can be exchange with the robot via XML-RPC
- XmlRpcEventArg: Represents a request that has just been received from the robot
- XmlRpcIntegerValue: Represents an integer value that can be exchange with the robot via XML-RPC
- XmlRpcPoseValue: Represents a pose value that can be exchange with the robot via XML-RPC
- XmlRpcServer: XML-RPC server that receives remote procedure calls from the robot's URScript programs.
- XmlRpcStringValue: Represents a string value that can be exchange with the robot via XML-RPC
- XmlRpcStructMember: Member of a structure exchanged via XML-RPC
- XmlRpcStructValue: Represents a structure that can be exchange with the robot via XML-RPC
- XmlRpcType: All supported types that can be transmitted by XML-RPC
- XmlRpcUnknownValue: Represents an unknown XML-RPC argument that has been received from the robot You can decode it yourself with the XML property
- XmlRpcValue: Base class of all elements transmitted by XML-RPC. The XmlRpcValue.Type property indicates the type into which this object can be cast to obtain the value.

## UnderAutomation.UniversalRobots.XmlRpc.Internal

File: [UnderAutomation.UniversalRobots.XmlRpc.Internal.md](UnderAutomation.UniversalRobots.XmlRpc.Internal.md)

- XmlRpcParametersBase: Base class for XML-RPC connection parameters.
- XmlRpcServerBase.XmlRpcServerRequestEventHandler: Event raised when a XML-RPC request is sent by the robot and received.
- XmlRpcServerBase: Base class providing XML-RPC server functionality for receiving remote procedure calls from a Universal Robots controller.
