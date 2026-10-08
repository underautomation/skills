# API index: UnderAutomation ABB SDK, C#

SDK version 1.1.0. One line per public type, grouped by namespace: name, then summary. Open the namespace file to read the members of a type.

## UnderAutomation.ABB

File: [UnderAutomation.ABB.md](UnderAutomation.ABB.md)

- AbbController: Main class of the SDK that represents a connection to an ABB robot controller
- ConnectionParameters: Connection parameters for an ABB robot controller

## UnderAutomation.ABB.Common

File: [UnderAutomation.ABB.Common.md](UnderAutomation.ABB.Common.md)

- ExternalJoints: The six external axis values that travel with a robot position. An axis the robot system does not define comes back as 9E9, which is how the controller says "not in use" rather than an actual position.
- JointTarget: A robot position expressed joint by joint: the six axes of the arm and the six external axes.
- Pose: A position and the orientation the robot holds there: a Common.Position extended with a Common.Quaternion.
- Position: A point in space, expressed in the coordinate system of whoever produced it. Most readings of the controller express a position in millimetres, while the kinematics calculations work in metres. The method that returns or takes a position says which one it uses.
- Quaternion: An orientation in space, expressed as a unit quaternion. The controller rejects a quaternion that is not normalized, so keep Quaternion.Q1² + Quaternion.Q2² + Quaternion.Q3² + Quaternion.Q4² equal to 1.
- RobTarget: A complete robot target: a Common.Pose extended with the axis configuration used to reach it and the external axis values that travel with it.
- RobotConfiguration: The axis configuration the robot uses to reach a pose. Several joint combinations reach the same tool position and orientation. The configuration names the one to use, as the quarter revolution each of the deciding axes sits in.
- RobotJoints: The six joint values of a robot arm. Readings of the controller express them in degrees, while the kinematics calculations work in radians. The method that returns or takes them says which one it uses.

## UnderAutomation.ABB.Discovery

File: [UnderAutomation.ABB.Discovery.md](UnderAutomation.ABB.Discovery.md)

- DiscoveredController: An ABB robot controller found on the local network. Returned by Discover(System.Int32).

## UnderAutomation.ABB.License

File: [UnderAutomation.ABB.License.md](UnderAutomation.ABB.License.md)

- InvalidLicenseException: Exception thrown while using the product if the license is not valid.
- LicenseInfo: Information about a license key
- LicenseState: States that can take a license

## UnderAutomation.ABB.Rws

File: [UnderAutomation.ABB.Rws.md](UnderAutomation.ABB.Rws.md)

- RwsClient: Standalone public RWS client for ABB robot controllers. Supports both RWS v1 and v2. Use this class when you want to connect to a robot without using the ABB.AbbController class.
- RwsConnectParameters: Connection parameters for ABB Robot Web Services (RWS). Supports both RWS v1 and v2.
- RwsException: Exception thrown when an RWS API request fails. Compatible with RWS v1 and v2.
- RwsVersion: Version of the ABB Robot Web Services (RWS) protocol exposed by the robot controller. The two versions differ in URL shapes, parameter placement and media types, so the client has to know which one it talks to. Pick the value that matches the controller generation.

## UnderAutomation.ABB.Rws.Data

File: [UnderAutomation.ABB.Rws.Data.md](UnderAutomation.ABB.Rws.Data.md)

- AxisInfo: State of one axis of a mechanical unit. Returned by MotionSystemService.GetAxis().
- BackupRestoreIgnore: Mismatches between a backup and the current system that are ignored when restoring
- BackupRestoreInclude: Content included when restoring a backup
- BackupState: State of the backup operation of the controller
- BackupSystemInfo: Information about a backup stored on the controller file system. Returned by ControllerService.GetBackupInfo(backupPath).
- BaseFrame: Where the base of a mechanical unit sits, and what kind of base it is: a Common.Pose extended with the type of the frame. Returned by MotionSystemService.GetBaseFrame(). The position is expressed in millimetres.
- CalibrationInfo: How a mechanical unit was calibrated, joint by joint. Returned by MotionSystemService.GetCalibrationInfo().
- CalibrationJointInfo: How one joint of a mechanical unit was calibrated. Held by Data.CalibrationInfo.
- CheckRestoreResult: Result of a backup restore check. Returned by ControllerService.CheckRestore(...).
- CheckRestoreStatus: Result status of a backup restore check
- CollisionDetectionState: State of the collision detection of the robot controller
- ControllerIdentity: Identity of the robot controller. Returned by ControllerService.GetIdentity().
- ControllerInfo: Overview of the controller resources. Returned by ControllerService.GetInfo().
- ControllerLevel: Level the controller is currently running at
- ControllerRestartMode: Restart mode of the robot controller
- ControllerState: State of the robot controller, as reported by the control panel
- ControllerType: Type of the robot controller (real or virtual)
- CoordinateSystem: Reference frame a cartesian position is expressed in
- CyclicBrakeCheckState: Cyclic brake check state of a mechanical unit
- CyclicBrakeCheckStatus: Cyclic brake check status of a mechanical unit. Returned by ControllerService.GetCyclicBrakeCheckStatus(driveNumber).
- CyclicBrakeCheckTestStatus: Result of the last cyclic brake check test
- DeviceItem: Represents a device entry in the robot controller file system (e.g. C:, hd0a). Devices are returned alongside files and directories when listing the root path ("/") or any directory that contains mounted devices.
- DeviceType: Represents the type of storage device
- DirectoryItem: Represents a directory entry in the robot controller file system.
- DirectoryListing: Represents a directory listing containing files, subdirectories, and devices. Returned by FileService.ListDirectory(path). When listing the root path ("/"), the DirectoryListing.Devices array contains available storage devices (C:, hd0a, etc.). When listing a subdirectory, only DirectoryListing.F...
- ElogDomain: One event log domain of the controller, for example the common, the operational or the safety log. Returned by ElogService.GetDomains() and ElogService.GetDomain().
- ElogMessage: One message of the controller event log. Returned by ElogService.GetMessages(), ElogService.GetMessageTitles(), ElogService.GetMessage() and ElogService.GetMessageBySequenceNumber(). The texts (ElogMessage.Title, ElogMessage.Description, ElogMessage.Consequences, ElogMessage.Causes and ElogMessag...
- ElogMessageArgument: One argument of an event log message. The arguments are the values the controller substitutes into the text of the message, for example the name of the task that was started. Held by ElogMessage.Arguments.
- ElogMessageOrder: Order in which the event log messages of a domain are returned
- ElogMessageType: Severity of an event log message
- FileItem: Represents a file entry in the robot controller file system.
- FileSystemItem: Abstract base class for all file system items returned by the File Service. Derived classes: Data.FileItem, Data.DirectoryItem, Data.DeviceItem
- IoClientAction: Action the client is expected to take after an I/O network auto configuration, returned by IoService.SetNetworkConfigurationType(). Only available when connected with version 2.
- IoDeviceConfiguration: Runtime configuration properties of an I/O device. Returned by IoService.GetDeviceConfiguration().
- IoDeviceItem: I/O device (unit) connected to an I/O network of the robot controller. Returned by IoService.GetDevices(), IoService.GetDevice() and IoService.SearchDevices().
- IoDeviceLogicalState: Logical state of an I/O device
- IoDevicePhysicalState: Physical state of an I/O device
- IoDeviceUpgradeInfo: Firmware upgrade status of an I/O device and of each of its modules. Returned by IoService.GetDeviceUpgradeInfo(). Only applicable to a real controller.
- IoFirmwareModuleInfo: Firmware upgrade status of one module of an I/O device. Returned by IoService.GetDeviceUpgradeInfo().
- IoFirmwareUpgradeState: Progress of a firmware upgrade of an I/O device
- IoFirmwareUpgradeStatus: Result of a firmware upgrade of an I/O device
- IoNetworkConfiguration: Runtime configuration properties of an I/O network. Returned by IoService.GetNetworkConfiguration().
- IoNetworkConfigurationType: Configuration type applied to an I/O network by IoService.SetNetworkConfigurationType()
- IoNetworkItem: I/O network defined in the robot controller. Returned by IoService.GetNetworks(), IoService.GetNetwork() and IoService.SearchNetworks().
- IoNetworkLogicalState: Logical state of an I/O network
- IoNetworkPhysicalState: Physical state of an I/O network
- IoSignalConfiguration: Runtime configuration properties of an I/O signal. Returned by IoService.GetSignalConfiguration().
- IoSignalItem: I/O signal defined in the robot controller. Returned by IoService.GetSignals(), IoService.GetSignal(), IoService.SearchSignals() and IoService.SearchSignalsExtended(). Depending on the method used, only a subset of the properties is filled in: the signal lists carry the name, type, category, logi...
- IoSignalLogicalState: Logical state of an I/O signal
- IoSignalPhysicalState: Physical state of an I/O signal
- IoSignalSearchCriteria: Criteria used to search I/O signals with IoService.SearchSignals() and IoService.SearchSignalsExtended(). Every property is optional: the properties left to null are not sent to the controller, and an empty criteria matches every signal. Two criteria can be combined by passing a second instance t...
- IoSignalType: Type of an I/O signal
- JogIncrementMode: Size of the step a jogging command moves the robot by
- JogMode: How the jogging commands sent to a mechanical unit are interpreted
- JointSolution: One of the joint combinations that reach a given pose: a Common.JointTarget extended with the axis configuration it corresponds to. Returned by MotionSystemService.GetAllJointSolutions(). The joint values are expressed in radians.
- LeadThroughStatus: Whether an operator can push the robot arm around by hand
- MastershipDomain: Domain of the controller a client can take the mastership of. Mastership is what a client has to hold before it is allowed to change anything in a domain. Only one client at a time holds it, and it stays held until the client releases it or its connection ends. The two connection versions do not...
- MastershipHolder: Who holds the mastership of a domain
- MastershipInfo: State of the mastership of one domain: who holds it, and whether this connection is the holder. Returned by MastershipService.GetInfo().
- MechanicalUnitInfo: Everything the controller knows about one mechanical unit. Returned by MotionSystemService.GetMechanicalUnit().
- MechanicalUnitItem: One mechanical unit of the motion system, as listed by MotionSystemService.GetMechanicalUnits(). Only the few properties the list carries are filled in. Read the unit itself with MotionSystemService.GetMechanicalUnit() to get a Data.MechanicalUnitInfo.
- MechanicalUnitMode: Whether a mechanical unit is activated and can be moved
- MechanicalUnitStatus: Calibration and synchronization state of a mechanical unit or of one of its axes
- MechanicalUnitType: Kind of mechanical unit the controller drives
- MotionErrorState: Last error the motion system ran into, most of them raised by a jogging request it could not honour
- MotionSupervision: Collision detection settings of one mechanical unit while it is jogged. Returned by MotionSystemService.GetMotionSupervision().
- MotionSystemErrorState: Error state of the motion system, and how many errors it has counted. Returned by MotionSystemService.GetErrorState().
- MotionSystemInfo: Overview of the motion system of the controller. Returned by MotionSystemService.GetInfo().
- MotorCalibrationName: Names one joint of a mechanical unit carries: the joint itself and the calibration data attached to it. Returned by MotionSystemService.GetMotorCalibrationNames().
- NetworkConfigurationMethod: IP configuration method of a controller LAN adapter
- NetworkInterfaceItem: Network interface of the robot controller. Returned by ControllerService.GetNetworkInterfaces().
- OperationMode: Operating mode selected on the robot controller
- OperationModeAcknowledgement: Pending change that an operating mode acknowledgement confirms
- OperationModeLockState: Lock state of the operating mode selector
- PathSupervision: Collision detection settings of one mechanical unit while it follows a programmed path. Returned by MotionSystemService.GetPathSupervision().
- RapidActivationRecord: One frame of the call stack of a task: which routine is running and where the execution stands in it. Returned by RapidService.GetActivationRecord(). Frame 1 is the routine holding the program pointer, and the number grows towards the entry point of the program.
- RapidAliasIoItem: An I/O signal a running RAPID program has given an alias to with the AliasIO instruction. Returned by RapidService.GetAliasIo(). The controller only knows about an alias while the program that declares it is loaded, so this list is empty on a controller holding no such program.
- RapidBreakpoint: A breakpoint set in the program of a task. Returned by RapidService.GetBreakpoints() and RapidService.SetBreakpoint(). The controller answers a write with the range it actually snapped the breakpoint to, which is the whole instruction containing the requested position rather than the position its...
- RapidBuildError: An error the controller found while linking the program of a task. Returned by RapidService.GetBuildErrors().
- RapidExecutionCycle: How many times the controller runs the program before stopping
- RapidExecutionInfo: Overall RAPID execution state of the controller. Returned by RapidService.GetExecutionState().
- RapidExecutionLevel: Level at which the code of a task is currently executing
- RapidExecutionMode: How far the program advances when execution is started
- RapidExecutionState: Whether the controller is currently executing RAPID code
- RapidExecutionType: What kind of code a task is currently running
- RapidExternalJointStates: What each of the six external joints of a task is doing, which says how to read the corresponding value of an external axis. Returned by RapidService.GetExternalJointStates(). A joint reported as RapidJointState.NotActive carries no meaningful position.
- RapidHoldToRunState: State of the hold-to-run control that gates RAPID execution in manual mode
- RapidInstructionTemplate: The template the controller suggests for an instruction or a data type: the arguments to write and the values to write them with. Returned by RapidService.GetInstructionTemplate(). An editor uses it to insert a complete, valid instruction rather than a bare keyword.
- RapidInstructionTemplateArgument: One argument of the template the controller suggests for an instruction or a data type. Carried by Data.RapidInstructionTemplate.
- RapidJointState: What an external joint of a task is doing
- RapidMechanicalUnitItem: A mechanical unit the positions of a task are expressed in. Returned by RapidService.GetMechanicalUnits(). This is the view the RAPID task has of the unit; MotionSystemService.GetMechanicalUnits() answers with everything the motion system knows about the same units.
- RapidModifiablePositionItem: One motion instruction of the system whose position can be rewritten to where the robot currently stands, wherever in whichever task it sits. Returned by RapidService.GetAllModifiablePositions().
- RapidModifiablePositions: How many motion instructions of a range can have their position rewritten to where the robot currently stands, and which range they cover. Returned by RapidService.GetModifiablePositions(). The controller leaves the range empty when it found nothing modifiable.
- RapidModuleAttribute: A property declared on a module, which restricts what may be done with it
- RapidModuleExtension: How big the source of a module is, which is what it takes to ask for the whole of it as a range. Returned by RapidService.GetModuleExtension().
- RapidModuleInfo: Everything the controller reports about one module. Returned by RapidService.GetModule(); the module lists only carry the properties of the Data.RapidModuleItem base class.
- RapidModuleItem: A module loaded into a task, as listed by RapidService.GetModules(). RapidService.GetModule() returns a Data.RapidModuleInfo, which adds the file the module came from and the attributes declared on it.
- RapidModuleSymbol: The declaration the controller finds at a given position of a module. Returned by RapidService.GetModuleSymbol(), which returns null when there is no declaration at that position.
- RapidModuleText: The source of a module and the counters that go with it. Returned by RapidService.GetModuleText().
- RapidModuleType: Whether a module belongs to the program or to the system
- RapidObjectChild: The parts a RAPID object is made of, and where each of them sits in the source. Returned by RapidService.GetObjectChildren(). Which parts the controller reports depends entirely on what the object is: a module answers with its name, its attributes and its declaration lists, a routine with somethi...
- RapidObjectChildRange: One named part of a RAPID object, and where it sits in the source. Carried by Data.RapidObjectChild.
- RapidObjectListExtension: Where one of the lists of a RAPID object sits in the source: the span of the whole list, and the spans of its first and last elements. Returned by RapidService.GetObjectListExtension(). An editor uses it to jump to the beginning or the end of a list without reading the module. The controller repo...
- RapidObjectListType: Which of the lists a RAPID object holds is being asked about
- RapidPalletHeadItem: One category of the instruction palette the FlexPendant editor offers, for example "Prog.Flow". Returned by RapidService.GetPalletHeads(); its RapidPalletHeadItem.Number is what RapidService.GetPallet() takes.
- RapidPalletItem: One entry of an instruction palette category, which an editor offers as something the operator can insert at the cursor. Returned by RapidService.GetPallet().
- RapidPointerPosition: Where one of the two pointers of a task stands. Carried by Data.RapidPointers. RapidPointerPosition.Available tells apart a pointer that is really placed somewhere from one the controller could not report, which happens for the motion pointer whenever the task has not moved yet.
- RapidPointerSyncState: Whether the pointers of every task are synchronized with each other
- RapidPointers: The program pointer and the motion pointer of a task, read in one request. Returned by RapidService.GetPointers(). The program pointer says which instruction runs next, the motion pointer which one the robot is actually executing; they drift apart because the controller plans the path ahead of th...
- RapidPreferredDataTypeItem: A data type the controller suggests for one argument of an instruction, so that an editor can offer the operator the types that fit where the cursor stands. Returned by RapidService.GetPreferredDataTypes().
- RapidProgramCounterPosition: Where the program pointer of a task stands, expressed as the piece of source it points at. Returned by RapidService.GetProgramCounterPosition(). The controller refuses the request when the task has no program pointer set, so reset it or start the program first.
- RapidProgramInfo: The program loaded into a task. Returned by RapidService.GetProgram(), which returns null when the task holds no program at all.
- RapidProgramLoadMode: What happens to the modules already in a task when a program is loaded into it
- RapidRegainMode: What the robot does about the distance between where it stands and where the path it is about to resume expects it to be
- RapidRoutineArgument: One argument of the routine call found at a given position of a module, and where it sits in the source. Returned by RapidService.GetRoutineArguments().
- RapidRoutineInfo: The routine the controller finds called at a given position of a module. Returned by RapidService.GetRoutine(). The controller refuses the request when the position does not sit on a routine call.
- RapidServiceRoutineItem: A routine of a task the program pointer can be moved to. Returned by RapidService.GetServiceRoutines().
- RapidSetTextRangeResult: What the controller did with a change written into the source of a module. Returned by RapidService.SetModuleTextRange(). Rewriting the MODULE line renames the module, which is why the controller reports the name it ended up with.
- RapidSpyStatus: Whether the controller is recording the RAPID execution trace to a file
- RapidStartCondition: Condition the controller checks before it starts executing
- RapidStopMode: How abruptly RAPID execution is stopped
- RapidStructuralChangeCount: The two counters a task keeps of what has changed in it, so that a client can tell whether it needs to read the task again instead of fetching everything periodically. Returned by RapidService.GetStructuralChangeCount().
- RapidSymbolProperties: What a RAPID symbol is declared as. Returned by RapidService.GetSymbolProperties() and RapidService.SearchSymbols(). A search fills in RapidSymbolProperties.Name and leaves RapidSymbolProperties.Storage alone, a direct read does the opposite on some controllers, so treat both as optional.
- RapidSymbolSearchCriteria: What a symbol search looks for. Passed to RapidService.SearchSymbols(). Every property is optional; leaving one alone means the search does not filter on it. A search with no criterion at all walks the whole system, which is slow, so at least set RapidSymbolSearchCriteria.BlockUrl.
- RapidSymbolSearchView: Which part of the system a symbol search walks
- RapidSymbolType: What a RAPID symbol is: a value, a routine, a type or one of the structural elements of the language
- RapidSymbolValue: The value of a RAPID symbol and where it is declared. Returned by RapidService.GetSymbolValue(). The value is the text the controller wrote it as, which for a record is the bracketed form RAPID itself uses, for example [[515,0,712],[0.707107,0,0.707107,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,...
- RapidSymbolVariableType: Which variables a symbol search keeps, by what may be done with them
- RapidTaskExecutionMode: Stepping mode a task was last started with
- RapidTaskExecutionState: Whether a single task is running, and whether it could be
- RapidTaskInfo: Everything the controller reports about one RAPID task. Returned by RapidService.GetTask(); the task lists only carry the properties of the Data.RapidTaskItem base class.
- RapidTaskItem: A RAPID task of the controller, as listed by RapidService.GetTasks(). RapidService.GetTask() returns a Data.RapidTaskInfo, which adds everything the controller reports for a single task only.
- RapidTaskScope: Whether an execution command applies to the normal tasks only or to every task
- RapidTaskSelectionItem: One line of the task selection panel, telling whether a task is selected and whether an operator is allowed to change that. Returned by RapidService.GetTaskSelection().
- RapidTaskState: How far the controller has got in preparing the program of a task
- RapidTaskTrustLevel: What the controller does to the system when a task that is not a normal one stops unexpectedly
- RapidTaskType: Kind of RAPID task, which decides when the controller runs it
- RapidTextPosition: A position in the source of a module, counted from 1. Returned by RapidService.SearchModuleText(), which reports row and column 0 when the text was not found rather than failing.
- RapidTextQueryMode: How hard the controller tries to apply a change to the source of a running task
- RapidTextRange: A span of source between two positions, counted from 1. Used wherever the controller reports where something is declared or where a statement sits.
- RapidTextReplaceMode: Where new text is put relative to the range it is written against
- RapidUiInstruction: The dialogue a running RAPID program is currently asking an operator for. Returned by RapidService.GetActiveUiInstruction(), which returns null when no instruction is pending. Answering one means writing its parameters with RapidService.SetUiInstructionParameter(), using RapidUiInstruction.StackU...
- RapidUiInstructionEvent: What a UI instruction is asking of the client
- RapidUiInstructionParameter: One parameter of the pending UI instruction: what the program passed in, or what it is waiting for. Returned by RapidService.GetUiInstructionParameters(). The parameters carrying the answer are the ones to write, typically named after a function key or after the completion flag of the instruction.
- SafetyConfiguration: Safety supervision configuration of the controller. Returned by ControllerService.GetSafetyConfiguration().
- SafetyLoadOperationStatus: Indicates whether a new safety configuration is allowed to be loaded
- SafetyMode: Safety mode of the safety controller
- SafetyModeStatus: Safety mode status of the controller. Returned by ControllerService.GetSafetyMode().
- SafetyViolationInfo: Safety violation details reported by the safety controller. Returned by ControllerService.GetSafetyViolationInfo().
- SafetyViolationType: Type of safety violation reported by the safety controller
- SmbData: Serial measurement board data of one mechanical unit, held twice: once in the controller cabinet and once in the memory of the robot itself. Returned by MotionSystemService.GetSmbData(). Comparing the cabinet properties with the robot ones tells whether the two copies still agree, which is what M...
- SmbDataMemory: Which of the two copies of the serial measurement board data is erased
- SmbDataStatus: State of one block of serial measurement board data, on the controller side or on the robot side
- SmbDataTransfer: Which of the two copies of the serial measurement board data overwrites the other
- SystemEnergy: Energy the controller has consumed, for the current measurement interval and since the last reset. Returned by SystemService.GetEnergy().
- SystemEnergyAxis: Energy consumed by one axis of a mechanical unit during the current measurement interval. Held by Data.SystemEnergyMechanicalUnit.
- SystemEnergyMechanicalUnit: Energy consumed by one mechanical unit, broken down per axis. Held by Data.SystemEnergy.
- SystemEnergyState: State of the energy measurement of the controller
- SystemInfo: Identity and software version of the system running on the controller. Returned by SystemService.GetInfo().
- SystemProduct: One software product installed on the controller. Returned by SystemService.GetProducts().
- TimeServerInfo: Time server used by the controller to synchronize its clock. Returned by ControllerService.GetTimeServer().
- VirtualTimeState: State of the virtual time server of a virtual controller

## UnderAutomation.ABB.Rws.Internal

File: [UnderAutomation.ABB.Rws.Internal.md](UnderAutomation.ABB.Rws.Internal.md)

- RwsClientBase: Base class providing HTTP communication with ABB RWS REST API. Handles Digest Authentication, request building and XML response parsing. Supports both RWS v1 and v2.
- RwsClientInternal: Internal RWS client for use by ABB.AbbController. This class is used internally and should not be instantiated directly.
- RwsConnectParametersBase: Base class for connection parameters. Contains core properties needed for RWS connection.

## UnderAutomation.ABB.Rws.Services

File: [UnderAutomation.ABB.Rws.Services.md](UnderAutomation.ABB.Rws.Services.md)

- ControllerService: Controller Service - Provides access to the controller resources: clock, identity, network, installed systems, options, backups, safety controller and virtual time.
- ElogService: Event Log Service - Provides access to the messages the controller logs: the list of the log domains, the messages they hold, and the operations that clear them or dump them to a file. None of these resources is available while the controller runs in bootserver mode.
- FileService: File Service - Provides access to the robot controller file system Compatibility: Version 1: directory operations with basic functionalityVersion 2: extended file operations
- IoService: I/O System Service - Provides access to the I/O resources of the controller: networks, devices and signals. None of these resources is available while the controller runs in bootserver mode.
- MastershipService: Mastership Service - Takes and gives back the exclusive right to change a domain of the controller. Most write operations are refused unless the client holds the mastership of the domain they belong to: moving a mechanical unit needs MastershipDomain.Motion, changing the system parameters or the...
- MotionSystemService: Motion System Service - Everything about how the robot stands and how it moves: the mechanical units of the system and their axes, where the tool currently is, the calibration and the revolution counters, jogging, the collision supervision, and the kinematics calculations that convert a pose into...
- PanelService: Panel Service - Exposes what an operator reads and acts on from the control panel of the controller: the controller state, the operating mode and its selector lock, the speed ratio, the collision detection state, the language of the controller and its restart. None of these resources is available...
- RapidService: RAPID Service - Everything about the program the robot runs: the tasks it is split into, the modules and the source they hold, the symbols the program declares and the values they carry, where the program pointer stands, and starting, stopping and stepping the execution. None of these resources i...
- SystemService: System Service - Describes the system installed on the controller: its name and software version, the options and the products it was built with, the type of robot it drives, its license, and the energy it consumes. None of these resources is available while the controller runs in bootserver mode.
