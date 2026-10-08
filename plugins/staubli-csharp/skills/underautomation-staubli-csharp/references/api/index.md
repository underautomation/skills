# API index: UnderAutomation Staubli SDK, C#

SDK version 1.0.0. One line per public type, grouped by namespace: name, then summary. Open the namespace file to read the members of a type.

## UnderAutomation.Staubli

File: [UnderAutomation.Staubli.md](UnderAutomation.Staubli.md)

- ConnectionParameters: Connection parameters
- StaubliController: Main class of the SDK that represents a connection to a Staubli robot controller

## UnderAutomation.Staubli.Common

File: [UnderAutomation.Staubli.Common.md](UnderAutomation.Staubli.Common.md)

- FileConnectParameters: Connection parameters of the file client (robot.File). With a real controller, the files are accessed through the FTP server of the controller, with the user and the password of these parameters. With a controller emulated by Staubli Robotics Suite, give the path of its .controller file as addres...
- SoapConnectParameters: SOAP connection parameters for communicating with the Staubli robot controller.

## UnderAutomation.Staubli.Files

File: [UnderAutomation.Staubli.Files.md](UnderAutomation.Staubli.Files.md)

- FileClient: Standalone client for the files of a Staubli controller: upload, download, listing and management. With a real controller, the files are accessed through the FTP server of the controller. With a controller emulated by Staubli Robotics Suite, they are accessed in the folder of its .controller file.
- FileException: Exception thrown when an operation on the files of the controller fails: the controller refused it, the file does not exist, or the communication failed. The message gives the reason and, when it is known, what to do.
- FileItem: A file or a folder of the controller
- FileItemType: Type of an item of the controller file system
- OnProgressDelegate: Reports the progress of a file transfer

## UnderAutomation.Staubli.Files.Internal

File: [UnderAutomation.Staubli.Files.Internal.md](UnderAutomation.Staubli.Files.Internal.md)

- FileClientBase: Upload, download, listing and management of the files of the controller. With a real controller, the files are accessed through the FTP server of the controller. With a controller emulated by Staubli Robotics Suite, there is no FTP server: give the path of its .controller file as address. The fil...
- FileClientInternal: File client of Staubli.StaubliController, connected by Staubli.ConnectionParameters)
- FileConnectParametersBase: Base class for the connection parameters of the file client

## UnderAutomation.Staubli.License

File: [UnderAutomation.Staubli.License.md](UnderAutomation.Staubli.License.md)

- InvalidLicenseException: Exception thrown while using the product if the license is not valid.
- LicenseInfo: Information about a license key
- LicenseState: States that can take a license

## UnderAutomation.Staubli.Soap

File: [UnderAutomation.Staubli.Soap.md](UnderAutomation.Staubli.Soap.md)

- SoapClient: SOAP client for Staubli robots

## UnderAutomation.Staubli.Soap.Data

File: [UnderAutomation.Staubli.Soap.Data.md](UnderAutomation.Staubli.Soap.Data.md)

- AboveBelowConfig: Configuration for above/below joint orientation.
- AnthroConfig: Configuration for an anthropomorphic robot (shoulder, elbow, wrist).
- BlendType: Blend mode used during motion transitions between segments.
- CartesianJointPosition: Represents the joint positions and the Cartesian position of a robot end effector.
- CartesianPosition: Represents a Cartesian position with X, Y, Z translation and Rx, Ry, Rz rotation components.
- Config: Robot configuration containing kinematic-specific settings.
- ControllerTask: Represents a task running on the controller.
- ControllerTaskState: Execution state of a controller task.
- DhParameters: Denavit-Hartenberg parameters for a single robot joint.
- DiameterAxis3: Diameter of the third axis of the robot.
- Frame: Represents a 3D transformation composed of orientation (a 3x3 rotation matrix) and position (a translation vector) in space. Used to define the pose of a robot or tool in a 3D environment. Matrix representation: [ Nx Ox Ax Px ] [ Ny Oy Ay Py ] [ Nz Oz Az Pz ] [ 0 0 0 1 ]
- IForwardKinematics: Represents the result of a forward kinematics computation.
- IMoveResult: Represents the result of a robot motion command.
- IReverseKinematics: Represents the result of a reverse (inverse) kinematics computation.
- JointRange: Minimum and maximum range of each robot joint (radians).
- Kinematic: Robot kinematic type.
- LengthAxis3: Length of the third axis of the robot.
- MotionDesc: Describes the parameters of a robot motion, including tool, frame, velocity, acceleration, blending and configuration.
- MotionReturnCode: Return code for robot motion commands.
- MountType: Robot mounting type.
- MoveType: Specifies whether the motion is absolute or relative.
- Parameter: Key-value parameter from the controller.
- PhysicalAioAttribute: Attributes for an analog I/O, including linear conversion coefficients.
- PhysicalDioAttribute: Attributes for a digital I/O.
- PhysicalIo: Represents a physical I/O on the robot.
- PhysicalIoAttribute: Physical I/O attribute containing either analog or digital specific attributes.
- PhysicalIoEnumState: Definition state of a physical I/O.
- PhysicalIoState: Current state and value of a physical I/O.
- PhysicalIoWriteResponse: Result of a physical I/O write operation.
- PositiveNegativeConfig: Positive/negative configuration for a robot joint.
- PowerReturnCode: Return code for robot power commands.
- ProgramLine: Represents a line of a VAL3 program being executed on the controller.
- ReversingResult: Result code for reverse kinematics computation.
- Robot: Represents a robot managed by the controller.
- ScaraConfig: Configuration for a SCARA robot.
- ShoulderConfig: Shoulder configuration for the robot arm.
- ValApplication: Represents a VAL3 application on the controller.
- VrbxConfig: Configuration for a VRBX-type robot.

## UnderAutomation.Staubli.Soap.Errors

File: [UnderAutomation.Staubli.Soap.Errors.md](UnderAutomation.Staubli.Soap.Errors.md)

- CustomSoapException: Custom exception class for handling SOAP errors with specific error codes and descriptions.
- SoapErrorCode: Error codes returned by the SOAP service.
- StartApplicationError: Error codes that can occur when starting an application on the controller.

## UnderAutomation.Staubli.Soap.Internal

File: [UnderAutomation.Staubli.Soap.Internal.md](UnderAutomation.Staubli.Soap.Internal.md)

- SoapClientBase: Base class for SOAP client
- SoapClientInternal: Internal class for SOAP client, do not use directly
- SoapConnectParametersBase: Base class for SOAP connection parameters
