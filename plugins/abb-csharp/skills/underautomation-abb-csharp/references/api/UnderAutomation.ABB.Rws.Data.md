# UnderAutomation.ABB.Rws.Data

## AxisInfo

`class AxisInfo`

State of one axis of a mechanical unit. Returned by MotionSystemService.GetAxis().

- `AxisInfo()`: Initializes a new instance of the Data.AxisInfo class
- `int? LogicalAxis { get; set; }`: Logical joint number of the axis, null when the controller did not report it
- `int Number { get; set; }`: Number of the axis inside its mechanical unit, starting at 1
- `MechanicalUnitStatus Status { get; set; }`: Calibration and synchronization state of the axis

## BackupRestoreIgnore

`enum BackupRestoreIgnore`

Mismatches between a backup and the current system that are ignored when restoring

- All: All mismatches are ignored
- None: No mismatch is ignored
- SystemId: A mismatch between the system id of the backup and the system id of the current system is ignored
- TemplateId: A mismatch between the template id of the backup and the template id of the current system is ignored

## BackupRestoreInclude

`enum BackupRestoreInclude`

Content included when restoring a backup

- All: Restore configuration files and RAPID modules
- Cfg: Restore configuration files only
- Modules: Restore RAPID modules only

## BackupState

`enum BackupState`

State of the backup operation of the controller

- BackupInProgress: A backup operation is running
- BackupReady: The backup operation finished successfully
- ErrorDuringBackup: The backup operation failed
- InitState: A backup operation has been initialized
- Invalid: The backup state is invalid
- None: No backup operation
- Unknown: The backup state could not be determined

## BackupSystemInfo

`class BackupSystemInfo`

Information about a backup stored on the controller file system. Returned by ControllerService.GetBackupInfo(backupPath).

- `BackupSystemInfo()`: Initializes a new instance of the Data.BackupSystemInfo class
- `int OptionCount { get; }`: Number of options installed on the backed up system
- `string[] Options { get; set; }`: Options installed on the backed up system
- `string RobotControlVersion { get; set; }`: RobotControl version of the backed up system. Only available when connected with version 2.
- `string RobotOsVersion { get; set; }`: RobotOS version of the backed up system. Only available when connected with version 2.
- `string RobotWareVersion { get; set; }`: RobotWare version of the backed up system. Only available when connected with version 1.
- `string SystemName { get; set; }`: Name of the backed up system

## BaseFrame

`class BaseFrame : Pose`

Where the base of a mechanical unit sits, and what kind of base it is: a Common.Pose extended with the type of the frame. Returned by MotionSystemService.GetBaseFrame(). The position is expressed in millimetres.

- `BaseFrame()`: Initializes a new base frame at the origin, with no rotation
- `string Type { get; set; }`: Kind of base frame the controller reports, for example "IRBRobot"
- Inherited from [Pose](UnderAutomation.ABB.Common.md#pose): `Orientation`
- Inherited from [Position](UnderAutomation.ABB.Common.md#position): `X`, `Y`, `Z`

## CalibrationInfo

`class CalibrationInfo`

How a mechanical unit was calibrated, joint by joint. Returned by MotionSystemService.GetCalibrationInfo().

- `CalibrationInfo()`: Initializes a new instance of the Data.CalibrationInfo class
- `int? ActiveJointCount { get; set; }`: Number of joints of the unit that are in use, null when the controller did not report it
- `string CalibrationMethodUsed { get; set; }`: Name of the calibration method the unit was last calibrated with, for example "AxisCalibration"
- `int? CalibrationWindowType { get; set; }`: Kind of calibration window the controller offers for this unit, null when the controller did not report it
- `int ExistingJointCount { get; }`: Number of joints that exist on the unit, counted from CalibrationInfo.Joints
- `int? JointCount { get; set; }`: Number of entries in CalibrationInfo.Joints, which is fixed and larger than CalibrationInfo.ActiveJointCount. Null when the controller did not report it.
- `CalibrationJointInfo[] Joints { get; set; }`: One entry per joint slot of the unit, the unused ones marked as such. Never null.

## CalibrationJointInfo

`class CalibrationJointInfo`

How one joint of a mechanical unit was calibrated. Held by Data.CalibrationInfo.

- `CalibrationJointInfo()`: Initializes a new instance of the Data.CalibrationJointInfo class
- `string CurrentCalibrationMethod { get; set; }`: Method the joint is currently calibrated with
- `bool Exists { get; set; }`: Whether the joint exists on this mechanical unit. The controller always answers with a fixed number of entries and marks the unused ones, which carry no name at all.
- `string FactoryCalibrationMethod { get; set; }`: Method the joint was calibrated with in the factory
- `string JointName { get; set; }`: Name of the joint, for example "rob1_1", empty for an entry that does not exist

## CheckRestoreResult

`class CheckRestoreResult`

Result of a backup restore check. Returned by ControllerService.CheckRestore(...).

- `CheckRestoreResult()`: Initializes a new instance of the Data.CheckRestoreResult class
- `bool IsAccepted { get; }`: Indicates whether the backup can be restored
- `string Path { get; set; }`: File missing or corrupted in the backup, if reported by the controller
- `CheckRestoreStatus Status { get; set; }`: Status of the check

## CheckRestoreStatus

`enum CheckRestoreStatus`

Result status of a backup restore check

- Accepted: The backup is accepted and can be restored
- ConfigurationDataIncorrect: Error in the configuration data of the backup
- DirectoryNotComplete: The backup directory is not complete
- RestoreMismatchSystemId: The backup was not created from the current system, there might be differences in active options and selected languages
- RestoreMismatchTemplateId: The current system and the backed up system may be generated from different key ids, possibly with different robot types
- Unknown: The status could not be determined

## CollisionDetectionState

`enum CollisionDetectionState`

State of the collision detection of the robot controller

- Confirmed: A detected collision has been confirmed
- Init: No collision has been detected since the controller started
- Triggered: A collision has been detected and is waiting to be confirmed
- TriggeredAcknowledged: A detected collision has been acknowledged by an operator
- Unknown: The collision detection state could not be determined

## ControllerIdentity

`class ControllerIdentity`

Identity of the robot controller. Returned by ControllerService.GetIdentity().

- `ControllerIdentity()`: Initializes a new instance of the Data.ControllerIdentity class
- `string Id { get; set; }`: Controller id, available only for a real controller
- `ControllerLevel Level { get; set; }`: Indicates whether the controller runs at system level or in bootserver mode
- `string MacAddress { get; set; }`: MAC address of the controller, available only for a real controller
- `string Name { get; set; }`: Name of the controller
- `ControllerType Type { get; set; }`: Indicates whether the controller is a real or a virtual controller

## ControllerInfo

`class ControllerInfo`

Overview of the controller resources. Returned by ControllerService.GetInfo().

- `ControllerInfo()`: Initializes a new instance of the Data.ControllerInfo class
- `ControllerLevel Level { get; set; }`: Indicates whether the controller runs at system level or in bootserver mode
- `string Name { get; set; }`: Name of the controller
- `string[] Resources { get; set; }`: Names of the sub resources exposed by the controller ("clock", "identity", "network", ...)
- `DateTime? SystemTime { get; set; }`: Current system time of the controller (UTC), if available
- `ControllerType Type { get; set; }`: Indicates whether the controller is a real or a virtual controller

## ControllerLevel

`enum ControllerLevel`

Level the controller is currently running at

- BootLevel: The controller runs the boot application (bootserver mode)
- SystemLevel: A system is loaded and running (system level)
- Unknown: The controller level could not be determined

## ControllerRestartMode

`enum ControllerRestartMode`

Restart mode of the robot controller

- BStart: The controller will be restarted. The last automatically saved system state will be loaded. Should be used to recover from a system crash.
- IStart: The controller will be restarted. The current system parameter settings and RAPID programs will be discarded, and the original system installation settings will be used.
- PStart: The controller will be restarted. The current RAPID programs and data will be discarded, but not the system parameter settings.
- Restart: The controller will be restarted. The state is saved and any changed system parameter settings will be activated after the restart.
- Shutdown: The main computer will be shut down. Should be used if the controller UPS is broken.
- XStart: The controller will be restarted and the Boot Application will be started. The current system is saved and deactivated (the controller is non-functional, for advanced maintenance only).

## ControllerState

`enum ControllerState`

State of the robot controller, as reported by the control panel

- EmergencyStop: The robot is stopped because the emergency stop was activated
- EmergencyStopReset: The robot is ready to leave the emergency stop state: the emergency stop is no longer activated, but the state transition is not confirmed yet.
- GuardStop: The robot is stopped because the safety runchain is opened, for instance because a door of its cell is open
- Init: The robot is starting up. It will shift to ControllerState.MotorsOff once it has started.
- MotorsOff: The robot is in a standby state where there is no power to its motors. The state has to be shifted to ControllerState.MotorsOn before the robot can move.
- MotorsOn: The robot is ready to move, either by jogging or by running programs
- SystemFailure: The robot is in a system failure state and requires a restart
- Unknown: The state could not be determined

## ControllerType

`enum ControllerType`

Type of the robot controller (real or virtual)

- RealController: Physical robot controller (RC)
- Unknown: The controller type could not be determined
- VirtualController: Virtual controller (VC), for example running in RobotStudio

## CoordinateSystem

`enum CoordinateSystem`

Reference frame a cartesian position is expressed in

- Base: The base frame of the mechanical unit
- Tool: The frame of the active tool
- Unknown: The controller reported a frame this library does not know
- WorkObject: The frame of the active work object
- World: The world frame, shared by every mechanical unit of the system

## CyclicBrakeCheckState

`enum CyclicBrakeCheckState`

Cyclic brake check state of a mechanical unit

- Ok: No brake check is needed (CBC_STATUS_OK)
- PreWarning: A brake check will soon be required (CBC_STATUS_PREWARNING)
- Required: A brake check is required (CBC_STATUS_REQUIRE_CBC)
- Unknown: The state could not be determined

## CyclicBrakeCheckStatus

`class CyclicBrakeCheckStatus`

Cyclic brake check status of a mechanical unit. Returned by ControllerService.GetCyclicBrakeCheckStatus(driveNumber).

- `CyclicBrakeCheckStatus()`: Initializes a new instance of the Data.CyclicBrakeCheckStatus class
- `int DriveNumber { get; set; }`: Drive number of the mechanical unit this status belongs to
- `CyclicBrakeCheckTestStatus LastBrakeCheckStatus { get; set; }`: Result of the last brake check
- `long? NextBrakeCheckTime { get; set; }`: Remaining time before the next brake check is required, if reported by the controller
- `CyclicBrakeCheckState Status { get; set; }`: Current cyclic brake check state

## CyclicBrakeCheckTestStatus

`enum CyclicBrakeCheckTestStatus`

Result of the last cyclic brake check test

- Error: The last brake check failed (CBC_TEST_ERROR)
- Ok: The last brake check succeeded (CBC_TEST_OK)
- Undefined: No brake check has been performed yet (CBC_TEST_UNDEFINED)
- Unknown: The test status could not be determined
- Warning: The last brake check ended with a warning (CBC_TEST_WARNING)

## DeviceItem

`class DeviceItem : FileSystemItem`

Represents a device entry in the robot controller file system (e.g. C:, hd0a). Devices are returned alongside files and directories when listing the root path ("/") or any directory that contains mounted devices.

- `DeviceItem()`: Initializes a new instance of the Data.DeviceItem class
- `DeviceType DeviceType { get; set; }`: Type of device (Fixed, Removable, RamDisk, Remote)
- `long FreeSpace { get; set; }`: Free storage space in bytes
- `bool IsEnabled { get; set; }`: Indicates if the device is enabled
- `bool IsReadOnly { get; set; }`: Indicates if the device is read-only
- `long TotalSpace { get; set; }`: Total storage space in bytes
- Inherited from [FileSystemItem](UnderAutomation.ABB.Rws.Data.md#filesystemitem): `Name`, `CreationDate`, `ModificationDate`

## DeviceType

`enum DeviceType`

Represents the type of storage device

- Fixed: Fixed storage device (hard drive)
- RamDisk: RAM disk
- Remote: Remote or network storage
- Removable: Removable storage device (USB, SD card, etc.)
- Unknown: Unknown device type

## DirectoryItem

`class DirectoryItem : FileSystemItem`

Represents a directory entry in the robot controller file system.

- `DirectoryItem()`: Initializes a new instance of the Data.DirectoryItem class
- `bool IsReadOnly { get; set; }`: Indicates if the directory is read-only
- Inherited from [FileSystemItem](UnderAutomation.ABB.Rws.Data.md#filesystemitem): `Name`, `CreationDate`, `ModificationDate`

## DirectoryListing

`class DirectoryListing`

Represents a directory listing containing files, subdirectories, and devices. Returned by FileService.ListDirectory(path). When listing the root path ("/"), the DirectoryListing.Devices array contains available storage devices (C:, hd0a, etc.). When listing a subdirectory, only DirectoryListing.F...

- `DirectoryListing(string path)`: Initializes a new instance of the Data.DirectoryListing class
- `int DeviceCount { get; }`: Number of devices in this listing
- `DeviceItem[] Devices { get; set; }`: Devices available in this listing (typically only present at root "/")
- `DirectoryItem[] Directories { get; set; }`: Subdirectories contained in this directory
- `int DirectoryCount { get; }`: Number of subdirectories in this listing
- `int FileCount { get; }`: Number of files in this listing
- `FileItem[] Files { get; set; }`: Files contained in this directory
- `string Path { get; }`: Path that was listed
- `int TotalCount { get; }`: Total number of items (files + directories + devices)

## ElogDomain

`class ElogDomain`

One event log domain of the controller, for example the common, the operational or the safety log. Returned by ElogService.GetDomains() and ElogService.GetDomain().

- `ElogDomain()`: Initializes a new instance of the Data.ElogDomain class
- `int? BufferSize { get; set; }`: Number of messages the domain can hold before the oldest ones are discarded, null when the controller did not report it
- `int? MessageCount { get; set; }`: Number of messages currently held by the domain, null when the controller did not report it
- `string Name { get; set; }`: Name of the domain, for example "Operational" or "Safety". Only filled when a language was asked for, null otherwise.
- `int Number { get; set; }`: Number identifying the domain, which is the value to pass to the methods reading its messages

## ElogMessage

`class ElogMessage`

One message of the controller event log. Returned by ElogService.GetMessages(), ElogService.GetMessageTitles(), ElogService.GetMessage() and ElogService.GetMessageBySequenceNumber(). The texts (ElogMessage.Title, ElogMessage.Description, ElogMessage.Consequences, ElogMessage.Causes and ElogMessag...

- `ElogMessage()`: Initializes a new instance of the Data.ElogMessage class
- `string Actions { get; set; }`: Text describing the recommended actions. Only filled when a language was asked for.
- `int ArgumentCount { get; }`: Number of arguments of the message
- `ElogMessageArgument[] Arguments { get; set; }`: Values the controller substitutes into the text of the message
- `string Causes { get; set; }`: Text describing the probable causes of the event. Only filled when a language was asked for.
- `int? Code { get; set; }`: Number identifying the kind of event, the one printed on the teach pendant
- `string Consequences { get; set; }`: Text describing what the event implies for the robot. Only filled when a language was asked for.
- `string Description { get; set; }`: Long text describing what happened. Only filled when a language was asked for.
- `int? DomainNumber { get; set; }`: Number of the domain the message belongs to, null when the controller did not report it
- `int? SequenceNumber { get; set; }`: Number identifying the message inside its domain. Messages are numbered in the order they were logged, so a higher number is a more recent message.
- `string SourceName { get; set; }`: Part of the controller that logged the message, for example "MC0"
- `DateTime? Timestamp { get; set; }`: Moment the event was logged, null when the controller did not report it
- `string Title { get; set; }`: Short text of the message. Only filled when a language was asked for.
- `ElogMessageType Type { get; set; }`: Severity of the message

## ElogMessageArgument

`class ElogMessageArgument`

One argument of an event log message. The arguments are the values the controller substitutes into the text of the message, for example the name of the task that was started. Held by ElogMessage.Arguments.

- `ElogMessageArgument()`: Initializes a new instance of the Data.ElogMessageArgument class
- `int Index { get; set; }`: Position of the argument in the message, starting at 1
- `string Type { get; set; }`: Type of the argument reported by the controller, for example "string", "long" or "float"
- `string Value { get; set; }`: Value of the argument, always as text

## ElogMessageOrder

`enum ElogMessageOrder`

Order in which the event log messages of a domain are returned

- NewestFirst: Most recent message first
- OldestFirst: Oldest message first

## ElogMessageType

`enum ElogMessageType`

Severity of an event log message

- Error: Error event
- Information: State change, or informational event
- Unknown: The message type could not be determined
- Warning: Warning event

## FileItem

`class FileItem : FileSystemItem`

Represents a file entry in the robot controller file system.

- `FileItem()`: Initializes a new instance of the Data.FileItem class
- `bool IsReadOnly { get; set; }`: Indicates if the file is read-only
- `long Size { get; set; }`: File size in bytes
- Inherited from [FileSystemItem](UnderAutomation.ABB.Rws.Data.md#filesystemitem): `Name`, `CreationDate`, `ModificationDate`

## FileSystemItem

`abstract class FileSystemItem`

Abstract base class for all file system items returned by the File Service. Derived classes: Data.FileItem, Data.DirectoryItem, Data.DeviceItem

- `DateTime? CreationDate { get; set; }`: Creation date of the resource, if available
- `DateTime? ModificationDate { get; set; }`: Last modification date of the resource, if available
- `string Name { get; set; }`: Name of the item (file name, directory name, or device name such as "C:")

## IoClientAction

`enum IoClientAction`

Action the client is expected to take after an I/O network auto configuration, returned by IoService.SetNetworkConfigurationType(). Only available when connected with version 2.

- Info: The user should be informed of the configuration result
- None: Nothing to do
- Restart: The controller has to be restarted for the configuration to take effect
- Unknown: The controller did not report any client action. Always returned when connected with version 1, which does not report this information.

## IoDeviceConfiguration

`class IoDeviceConfiguration`

Runtime configuration properties of an I/O device. Returned by IoService.GetDeviceConfiguration().

- `IoDeviceConfiguration()`: Initializes a new instance of the Data.IoDeviceConfiguration class
- `bool? DenyDeactivate { get; set; }`: Whether deactivating the device is denied
- `string DeviceAddress { get; set; }`: Address of the device on its network, "-" when the network has no addressing
- `string DeviceName { get; set; }`: Name of the device, for example "DN_Internal_Device"
- `int? InputBits { get; set; }`: Number of input bits of the device, null when not reported
- `bool? LocalAuto { get; set; }`: Whether a local client can access the device in auto mode
- `bool? LocalManual { get; set; }`: Whether a local client can access the device in manual mode
- `string NetworkName { get; set; }`: Name of the industrial network the device belongs to, for example "DeviceNet"
- `int? OutputBits { get; set; }`: Number of output bits of the device, null when not reported
- `bool? Rapid { get; set; }`: Whether a RAPID client can access the device in both manual and auto mode
- `bool? RemoteAuto { get; set; }`: Whether a remote client can access the device in auto mode
- `bool? RemoteManual { get; set; }`: Whether a remote client can access the device in manual mode

## IoDeviceItem

`class IoDeviceItem`

I/O device (unit) connected to an I/O network of the robot controller. Returned by IoService.GetDevices(), IoService.GetDevice() and IoService.SearchDevices().

- `IoDeviceItem()`: Initializes a new instance of the Data.IoDeviceItem class
- `string Address { get; set; }`: Address of the device on its network, "-" when the network has no addressing
- `string InputData { get; set; }`: Input data of the device, as an hexadecimal string (for example "1FFFE063"). Only reported when reading a single device with IoService.GetDevice().
- `string InputMask { get; set; }`: Input mask of the device, as an hexadecimal string. A bit set to zero is an input bit that is not written. Only reported when reading a single device with IoService.GetDevice().
- `IoDeviceLogicalState LogicalState { get; set; }`: Logical state of the device
- `string Name { get; set; }`: Name of the device, for example "DRV_1" or "PANEL"
- `string NetworkName { get; set; }`: Name of the network the device is connected to, for example "Local"
- `string OutputData { get; set; }`: Output data of the device, as an hexadecimal string (for example "0000000E"). Only reported when reading a single device with IoService.GetDevice().
- `string OutputMask { get; set; }`: Output mask of the device, as an hexadecimal string. A bit set to zero is an output bit that is not written. Only reported when reading a single device with IoService.GetDevice().
- `string Path { get; set; }`: Full path of the device, "{network}/{device}" (for example "Local/DRV_1")
- `IoDevicePhysicalState PhysicalState { get; set; }`: Physical state of the device
- `string Type { get; set; }`: Type of the device, for example "DRV_1_TYPE". Not reported by every controller, null when absent. A virtual controller leaves it out.

## IoDeviceLogicalState

`enum IoDeviceLogicalState`

Logical state of an I/O device

- Disabled: The device is disabled
- Enabled: The device is enabled
- Unknown: The logical state could not be determined

## IoDevicePhysicalState

`enum IoDevicePhysicalState`

Physical state of an I/O device

- Deactivated: The device is deactivated
- Error: The device reports an error
- Halted: The device is halted
- Init: The device is initializing
- Running: The device is running
- Startup: The device is starting up
- Unconfigured: The device is not configured
- Unconnected: The device is not connected
- Unknown: The physical state could not be determined

## IoDeviceUpgradeInfo

`class IoDeviceUpgradeInfo`

Firmware upgrade status of an I/O device and of each of its modules. Returned by IoService.GetDeviceUpgradeInfo(). Only applicable to a real controller.

- `IoDeviceUpgradeInfo()`: Initializes a new instance of the Data.IoDeviceUpgradeInfo class
- `int ModuleCount { get; }`: Number of modules reported by the controller
- `IoFirmwareModuleInfo[] Modules { get; set; }`: Firmware status of each module of the device, empty when the controller reported none
- `IoFirmwareUpgradeState State { get; set; }`: Overall progress of the firmware upgrade of the device
- `IoFirmwareUpgradeStatus Status { get; set; }`: Overall result of the firmware upgrade of the device

## IoFirmwareModuleInfo

`class IoFirmwareModuleInfo`

Firmware upgrade status of one module of an I/O device. Returned by IoService.GetDeviceUpgradeInfo().

- `IoFirmwareModuleInfo()`: Initializes a new instance of the Data.IoFirmwareModuleInfo class
- `string HardwareRevision { get; set; }`: Hardware revision of the module, for example "C.1"
- `string Index { get; set; }`: Index of the module inside the device ("0", "1", ...)
- `string LatestProgramNameAvailable { get; set; }`: Name of the latest program available for the module
- `string ProgramName { get; set; }`: Name of the program installed on the module, for example "A_HYPIOM_B_3_8"
- `string SerialNumber { get; set; }`: Serial number of the module
- `IoFirmwareUpgradeState State { get; set; }`: Progress of the firmware upgrade of this module
- `IoFirmwareUpgradeStatus Status { get; set; }`: Result of the firmware upgrade of this module

## IoFirmwareUpgradeState

`enum IoFirmwareUpgradeState`

Progress of a firmware upgrade of an I/O device

- Allocate: The upgrade resources are being allocated
- Automatic: The upgrade is performed automatically
- Check: The upgraded firmware is being verified
- Deallocate: The upgrade resources are being released
- Finished: The upgrade is finished
- Info: The firmware information is being collected
- Manual: The upgrade has to be started manually
- Running: The upgrade is running
- RunningBurnInProgress: The firmware is being written to the device
- RunningCheckInProgress: The firmware is being checked
- RunningEndReceived: The device acknowledged the end of the upgrade
- RunningEraseInProgress: The device memory is being erased
- RunningStartReceived: The device acknowledged the start of the upgrade
- Start: The upgrade is starting
- Unknown: The state is unknown, or could not be parsed

## IoFirmwareUpgradeStatus

`enum IoFirmwareUpgradeStatus`

Result of a firmware upgrade of an I/O device

- Error: The upgrade failed
- Ok: The upgrade finished, the firmware was already up to date
- Pending: The upgrade is pending
- Unknown: The controller did not report a status, or it could not be parsed
- Upgraded: The upgrade finished, the firmware was updated

## IoNetworkConfiguration

`class IoNetworkConfiguration`

Runtime configuration properties of an I/O network. Returned by IoService.GetNetworkConfiguration().

- `IoNetworkConfiguration()`: Initializes a new instance of the Data.IoNetworkConfiguration class
- `string NetworkAddress { get; set; }`: Industrial network address, "-" when the network has no addressing
- `string NetworkName { get; set; }`: Name of the network, for example "Local"
- `string NetworkType { get; set; }`: Type of the network, for example "Local" or "LOC"

## IoNetworkConfigurationType

`enum IoNetworkConfigurationType`

Configuration type applied to an I/O network by IoService.SetNetworkConfigurationType()

- Bits: Configure the signals of the network
- Both: Configure both the signals and the signal groups
- Groups: Configure the signal groups of the network
- Scan: Scan the network for connected devices
- Units: Configure the devices of the network

## IoNetworkItem

`class IoNetworkItem`

I/O network defined in the robot controller. Returned by IoService.GetNetworks(), IoService.GetNetwork() and IoService.SearchNetworks().

- `IoNetworkItem()`: Initializes a new instance of the Data.IoNetworkItem class
- `IoNetworkLogicalState LogicalState { get; set; }`: Logical state of the network
- `string Name { get; set; }`: Name of the network, for example "Local", "Virtual" or "EtherNetIP"
- `string Path { get; set; }`: Full path of the network, which is its name for a network (for example "Local")
- `IoNetworkPhysicalState PhysicalState { get; set; }`: Physical state of the network

## IoNetworkLogicalState

`enum IoNetworkLogicalState`

Logical state of an I/O network

- Started: The network is started
- Stopped: The network is stopped
- Unknown: The logical state could not be determined

## IoNetworkPhysicalState

`enum IoNetworkPhysicalState`

Physical state of an I/O network

- Error: The network reports an error
- Halted: The network is halted
- Init: The network is initializing
- Running: The network is running
- Startup: The network is starting up
- Unknown: The physical state could not be determined

## IoSignalConfiguration

`class IoSignalConfiguration`

Runtime configuration properties of an I/O signal. Returned by IoService.GetSignalConfiguration().

- `IoSignalConfiguration()`: Initializes a new instance of the Data.IoSignalConfiguration class
- `bool? LocalAuto { get; set; }`: Whether a local client can write the signal in auto mode
- `bool? LocalManual { get; set; }`: Whether a local client can write the signal in manual mode
- `bool? Rapid { get; set; }`: Whether a RAPID client can write the signal in both manual and auto mode
- `bool? RemoteAuto { get; set; }`: Whether a remote client can write the signal in auto mode
- `bool? RemoteManual { get; set; }`: Whether a remote client can write the signal in manual mode
- `bool? SetByDeviceTransfer { get; set; }`: Whether the bits of this signal are set by a device transfer operation. Not reported by every controller, null when absent from the response.
- `int? SignalBits { get; set; }`: Number of bits of the signal, null when not reported
- `string SignalName { get; set; }`: Name of the signal, for example "DRV1CHAIN2"

## IoSignalItem

`class IoSignalItem`

I/O signal defined in the robot controller. Returned by IoService.GetSignals(), IoService.GetSignal(), IoService.SearchSignals() and IoService.SearchSignalsExtended(). Depending on the method used, only a subset of the properties is filled in: the signal lists carry the name, type, category, logi...

- `IoSignalItem()`: Initializes a new instance of the Data.IoSignalItem class
- `string Category { get; set; }`: Category the signal belongs to, for example "safety"
- `string DeviceName { get; set; }`: Name of the device the signal is connected to, for example "DRV_1"
- `IoSignalLogicalState LogicalState { get; set; }`: Logical state of the signal (simulated or not)
- `long? LogicalTimeMicroseconds { get; set; }`: Microseconds part of the global time at which the logical value was updated, null when not reported
- `long? LogicalTimeSeconds { get; set; }`: Seconds part of the global time at which the logical value was updated, null when not reported
- `float? LogicalValue { get; set; }`: Logical value of the signal, null when the controller did not report it
- `string Name { get; set; }`: Name of the signal, for example "DRV1BRAKE"
- `string NetworkName { get; set; }`: Name of the network the signal belongs to, for example "Local"
- `string Path { get; set; }`: Full path of the signal, "{network}/{device}/{signal}" (for example "Local/DRV_1/DRV1BRAKE")
- `IoSignalPhysicalState PhysicalState { get; set; }`: Physical state of the signal. Only reported when reading a single signal with IoService.GetSignal().
- `long? PhysicalTimeMicroseconds { get; set; }`: Microseconds part of the global time at which the physical value was updated, null when not reported
- `long? PhysicalTimeSeconds { get; set; }`: Seconds part of the global time at which the physical value was updated, null when not reported
- `float? PhysicalValue { get; set; }`: Physical value of the signal, null when the controller did not report it. Only reported by IoService.GetSignal() and IoService.SearchSignalsExtended().
- `string Quality { get; set; }`: Quality of the signal, reported as a numeric code by IoService.GetSignal() and as a textual value (for example "good") by IoService.SearchSignalsExtended()
- `IoSignalType Type { get; set; }`: Type of the signal
- `string WriteAccessLevel { get; set; }`: Access level required to write the signal, for example "None". Only reported by IoService.SearchSignalsExtended().

## IoSignalLogicalState

`enum IoSignalLogicalState`

Logical state of an I/O signal

- NotSimulated: The signal is not simulated
- Simulated: The signal is simulated: its logical value is forced and no longer follows the physical value
- Unknown: The logical state could not be determined

## IoSignalPhysicalState

`enum IoSignalPhysicalState`

Physical state of an I/O signal

- Invalid: The physical value of the signal is not valid
- Unknown: The physical state could not be determined
- Valid: The physical value of the signal is valid

## IoSignalSearchCriteria

`class IoSignalSearchCriteria`

Criteria used to search I/O signals with IoService.SearchSignals() and IoService.SearchSignalsExtended(). Every property is optional: the properties left to null are not sent to the controller, and an empty criteria matches every signal. Two criteria can be combined by passing a second instance t...

- `IoSignalSearchCriteria()`: Initializes a new instance of the Data.IoSignalSearchCriteria class
- `bool? Blocked { get; set; }`: Whether only the blocked (simulated) signals are searched
- `string Category { get; set; }`: Category of the searched signals, for example "safety"
- `string CategoryPrefix { get; set; }`: Category prefix of the searched signals
- `string DeviceName { get; set; }`: Name of the device the searched signals are connected to
- `bool? Invert { get; set; }`: Whether the criteria is inverted: the signals matching it are excluded from the result
- `string Name { get; set; }`: Name of the searched signals
- `string NetworkName { get; set; }`: Name of the network the searched signals belong to
- `IoSignalType? Type { get; set; }`: Type of the searched signals, null to search every type

## IoSignalType

`enum IoSignalType`

Type of an I/O signal

- AnalogInput: Analog input
- AnalogOutput: Analog output
- DigitalInput: Digital input
- DigitalOutput: Digital output
- GroupInput: Group input
- GroupOutput: Group output
- Unknown: The signal type could not be determined

## JogIncrementMode

`enum JogIncrementMode`

Size of the step a jogging command moves the robot by

- Large: One large step
- Medium: One medium step
- None: The robot moves for as long as the command is repeated, with no fixed step
- Small: One small step
- User: One step of the size configured in the system parameters

## JogMode

`enum JogMode`

How the jogging commands sent to a mechanical unit are interpreted

- Align: The tool is aligned with the closest axis of the active coordinate system
- AxisGroup1: Each command moves one axis of the first axis group
- AxisGroup2: Each command moves one axis of the second axis group
- Cartesian: The tool is moved along the axes of the active coordinate system
- ConfigurationJog: The robot changes axis configuration without moving the tool center point
- GoToPosition: The robot moves to a given position
- Unknown: The controller reported a mode this library does not know

## JointSolution

`class JointSolution : JointTarget`

One of the joint combinations that reach a given pose: a Common.JointTarget extended with the axis configuration it corresponds to. Returned by MotionSystemService.GetAllJointSolutions(). The joint values are expressed in radians.

- `JointSolution()`: Initializes a new solution with every axis at zero
- `RobotConfiguration Configuration { get; set; }`: Axis configuration this solution corresponds to. Never null.
- Inherited from [JointTarget](UnderAutomation.ABB.Common.md#jointtarget): `RobotAxes`, `ExternalAxes`

## LeadThroughStatus

`enum LeadThroughStatus`

Whether an operator can push the robot arm around by hand

- Active: The arm gives way when pushed
- Inactive: The arm holds its position
- Unknown: The controller reported a state this library does not know

## MastershipDomain

`enum MastershipDomain`

Domain of the controller a client can take the mastership of. Mastership is what a client has to hold before it is allowed to change anything in a domain. Only one client at a time holds it, and it stays held until the client releases it or its connection ends. The two connection versions do not...

- Configuration: The system parameters of the controller. On a connection established with version 2, where it is not a domain of its own, this is the same domain as MastershipDomain.Edit.
- Edit: Everything that changes the system itself: its configuration and its RAPID programs. On a connection established with version 1, where the two are separate domains, asking for this one takes MastershipDomain.Configuration and MastershipDomain.Rapid together.
- Motion: The movement of the robot: jogging, the mechanical units and everything that makes an axis move
- Rapid: The RAPID programs and their data. On a connection established with version 2, where it is not a domain of its own, this is the same domain as MastershipDomain.Edit.

## MastershipHolder

`enum MastershipHolder`

Who holds the mastership of a domain

- Internal: The controller itself holds it, while it runs an operation that must not be interrupted
- Local: A device attached to the controller holds it, the teach pendant for instance
- None: Nobody holds the mastership, it is free to be taken
- Remote: A client connected over the network holds it, possibly this one
- Unknown: The controller reported a holder this library does not know

## MastershipInfo

`class MastershipInfo`

State of the mastership of one domain: who holds it, and whether this connection is the holder. Returned by MastershipService.GetInfo().

- `MastershipInfo()`: Initializes a new instance of the Data.MastershipInfo class
- `string Alias { get; set; }`: Alternate name of the location of the holder, null when nobody holds the mastership
- `string Application { get; set; }`: Name of the application holding the mastership, null when nobody holds it
- `MastershipDomain Domain { get; set; }`: Domain this state describes
- `bool HeldByMe { get; set; }`: Whether this connection is the one holding the mastership, and is therefore allowed to write in the domain
- `MastershipHolder Holder { get; set; }`: Who holds the mastership of the domain
- `string Location { get; set; }`: Where the holder is, as it declared itself, null when nobody holds the mastership
- `long? UserId { get; set; }`: Identifier the controller gave the user holding the mastership, null when nobody holds it

## MechanicalUnitInfo

`class MechanicalUnitInfo`

Everything the controller knows about one mechanical unit. Returned by MotionSystemService.GetMechanicalUnit().

- `MechanicalUnitInfo()`: Initializes a new instance of the Data.MechanicalUnitInfo class
- `int? Axes { get; set; }`: Number of axes of the unit, null when the controller did not report it
- `CoordinateSystem CoordinateSystem { get; set; }`: Reference frame the cartesian positions of the unit are expressed in
- `string HasIntegratedUnit { get; set; }`: Name of the mechanical unit integrated into this one. A unit that integrates no other one is reported with a placeholder name rather than an empty value.
- `string IsIntegratedUnit { get; set; }`: Name of the mechanical unit this one is integrated into. A unit that is integrated into no other one is reported with a placeholder name rather than an empty value.
- `JogMode JogMode { get; set; }`: How the jogging commands sent to the unit are interpreted
- `MechanicalUnitMode Mode { get; set; }`: Whether the unit is activated
- `string Name { get; set; }`: Name of the mechanical unit, for example "ROB_1"
- `string PayloadName { get; set; }`: Name of the active payload
- `MechanicalUnitStatus Status { get; set; }`: Calibration and synchronization state of the unit
- `string TaskName { get; set; }`: Name of the RAPID task that drives the unit
- `string ToolName { get; set; }`: Name of the active tool
- `int? TotalAxes { get; set; }`: Number of axes of the unit and of the units integrated with it, null when the controller did not report it
- `string TotalPayloadName { get; set; }`: Name of the active total payload, which is the payload plus the load of the tool
- `MechanicalUnitType Type { get; set; }`: Kind of mechanical unit
- `string WorkObjectName { get; set; }`: Name of the active work object

## MechanicalUnitItem

`class MechanicalUnitItem`

One mechanical unit of the motion system, as listed by MotionSystemService.GetMechanicalUnits(). Only the few properties the list carries are filled in. Read the unit itself with MotionSystemService.GetMechanicalUnit() to get a Data.MechanicalUnitInfo.

- `MechanicalUnitItem()`: Initializes a new instance of the Data.MechanicalUnitItem class
- `bool? ActivationAllowed { get; set; }`: Whether the unit can be activated, null when the controller did not report it
- `int? DriveModule { get; set; }`: Number of the drive module the unit is connected to, null when the controller did not report it
- `MechanicalUnitMode Mode { get; set; }`: Whether the unit is activated
- `string Name { get; set; }`: Name of the mechanical unit, for example "ROB_1"

## MechanicalUnitMode

`enum MechanicalUnitMode`

Whether a mechanical unit is activated and can be moved

- Activated: The mechanical unit is activated and takes part in the motion
- Deactivated: The mechanical unit is deactivated and stays where it is
- Unknown: The controller reported a mode this library does not know

## MechanicalUnitStatus

`enum MechanicalUnitStatus`

Calibration and synchronization state of a mechanical unit or of one of its axes

- Initiated: The unit is starting up
- Locked: The unit is locked and refuses to move
- LockedShow: The unit is locked, and the controller shows it as such
- NotAbsoluteSynchronized: One or several absolute measurement axes are not synchronized
- NotCalibrated: The unit has never been calibrated
- NotCommutated: One or several motors have not been commutated
- NotRelativeSynchronized: One or several relative measurement axes are not synchronized
- Synchronized: The unit is calibrated and synchronized, and can be moved
- Undefined: The controller knows the unit but does not report its state
- Unknown: The controller reported a state this library does not know

## MechanicalUnitType

`enum MechanicalUnitType`

Kind of mechanical unit the controller drives

- None: No mechanical unit
- Robot: A robot arm without a tool center point, which can only be moved axis by axis
- Single: A single external axis, such as a track or a positioner
- TcpRobot: A robot arm holding a tool center point, which can be moved in cartesian coordinates
- Undefined: The controller knows the unit but does not report what it is
- Unknown: The controller reported a type this library does not know

## MotionErrorState

`enum MotionErrorState`

Last error the motion system ran into, most of them raised by a jogging request it could not honour

- ErroneousToolMass: A load definition carries a negative mass
- InvalidJogMotionType: The requested jogging mode is not valid
- MechanicalUnitNotActive: A mechanical unit was jogged whose activation failed
- Ok: No error
- RobotHoldMismatch: The tool and the work object disagree on which one the robot holds
- UncalibratedJogMotionType: An uncalibrated robot was jogged in a mode that needs its calibration
- Unknown: The controller reported an error this library does not know
- UnnormalizedQuaternion: A quaternion that is not normalized reached the jogging task, from a tool, a load or a work object
- WorkObjectMechanicalUnitNotFound: A mechanical unit used in coordinated jogging was not found

## MotionSupervision

`class MotionSupervision`

Collision detection settings of one mechanical unit while it is jogged. Returned by MotionSystemService.GetMotionSupervision().

- `MotionSupervision()`: Initializes a new instance of the Data.MotionSupervision class
- `bool? Enabled { get; set; }`: Whether the supervision is switched on, null when the controller did not report it
- `int? Level { get; set; }`: Sensitivity of the supervision, as a percentage: the lower the value, the sooner a collision is reported. Null when the controller did not report it.

## MotionSystemErrorState

`class MotionSystemErrorState`

Error state of the motion system, and how many errors it has counted. Returned by MotionSystemService.GetErrorState().

- `MotionSystemErrorState()`: Initializes a new instance of the Data.MotionSystemErrorState class
- `int? Count { get; set; }`: Number of errors counted since the controller started, incremented on every new error, null when the controller did not report it
- `string RawState { get; set; }`: Error state exactly as the controller reported it, useful when MotionSystemErrorState.State is MotionErrorState.Unknown
- `MotionErrorState State { get; set; }`: Last error the motion system ran into

## MotionSystemInfo

`class MotionSystemInfo`

Overview of the motion system of the controller. Returned by MotionSystemService.GetInfo().

- `MotionSystemInfo()`: Initializes a new instance of the Data.MotionSystemInfo class
- `bool? AbsoluteAccuracyActive { get; set; }`: Whether absolute accuracy is switched on, null when the controller did not report it
- `int? ChangeCount { get; set; }`: Counter the controller increments on every change of the motion system. Pass it to MotionSystemService.HasChanged() to find out whether anything moved since a previous reading, without fetching the whole state again.
- `string MechanicalUnitName { get; set; }`: Name of the mechanical unit the jogging commands currently apply to
- `bool? ModalPayloadMode { get; set; }`: Whether the payload of the robot is set by the running program rather than by the mechanical unit, null when the controller did not report it
- `int? PollRate { get; set; }`: Rate at which the controller refreshes the motion system state, null when it did not report it

## MotorCalibrationName

`class MotorCalibrationName`

Names one joint of a mechanical unit carries: the joint itself and the calibration data attached to it. Returned by MotionSystemService.GetMotorCalibrationNames().

- `MotorCalibrationName()`: Initializes a new instance of the Data.MotorCalibrationName class
- `string CalibrationName { get; set; }`: Name of the calibration data of the joint, usually the same as MotorCalibrationName.JointName
- `string JointName { get; set; }`: Name of the joint, for example "rob1_1"
- `int Number { get; set; }`: Number of the joint inside its mechanical unit, starting at 1

## NetworkConfigurationMethod

`enum NetworkConfigurationMethod`

IP configuration method of a controller LAN adapter

- Dhcp: IP address obtained from a DHCP server
- FixIp: Fixed IP address, the address, mask and gateway have to be provided
- NoIp: No IP address configured on the adapter

## NetworkInterfaceItem

`class NetworkInterfaceItem`

Network interface of the robot controller. Returned by ControllerService.GetNetworkInterfaces().

- `NetworkInterfaceItem()`: Initializes a new instance of the Data.NetworkInterfaceItem class
- `string Address { get; set; }`: IP address of the interface
- `bool? DhcpEnabled { get; set; }`: DHCP status of the interface, if reported by the controller
- `string Gateway { get; set; }`: Default gateway of the interface, if applicable
- `string LogicalName { get; set; }`: Logical name of the interface, for example "WAN", "LAN1" or "SERVICE"
- `string Mask { get; set; }`: Subnet mask of the interface
- `string Network { get; set; }`: Network the interface belongs to ("Public", "Private", "Ability", "Drive"). Only available when connected with version 2.
- `string Port { get; set; }`: Physical port of the interface, for example "X6" or "X23"
- `string PrimaryDns { get; set; }`: Primary DNS server of the interface. Only available when connected with version 2.
- `string SecondaryDns { get; set; }`: Secondary DNS server of the interface. Only available when connected with version 2.

## OperationMode

`enum OperationMode`

Operating mode selected on the robot controller

- Automatic: Automatic mode
- AutomaticChangeRequest: A change to the automatic mode has been requested and is waiting to be acknowledged
- Init: The controller is initializing
- ManualFullSpeed: Manual mode at full speed
- ManualFullSpeedChangeRequest: A change to the manual full speed mode has been requested and is waiting to be acknowledged
- ManualReducedSpeed: Manual mode at reduced speed
- Undefined: The controller reports an undefined operating mode
- Unknown: The operating mode could not be determined

## OperationModeAcknowledgement

`enum OperationModeAcknowledgement`

Pending change that an operating mode acknowledgement confirms

- Automatic: Confirms the switch to the automatic mode
- CollisionDetection: Confirms a collision detection
- ManualFullSpeed: Confirms the switch to the manual full speed mode

## OperationModeLockState

`enum OperationModeLockState`

Lock state of the operating mode selector

- Error: The controller reports an error on the mode selector lock
- Locked: The operating mode is locked and can be unlocked again with the pin code it was locked with
- PendingPermanentLock: A permanent lock has been requested and is not effective yet
- PermanentlyLocked: The operating mode is permanently locked
- Unknown: The lock state could not be determined
- Unlocked: The operating mode can be changed freely

## PathSupervision

`class PathSupervision`

Collision detection settings of one mechanical unit while it follows a programmed path. Returned by MotionSystemService.GetPathSupervision().

- `PathSupervision()`: Initializes a new instance of the Data.PathSupervision class
- `bool? Enabled { get; set; }`: Whether the supervision is switched on, null when the controller did not report it
- `int? Level { get; set; }`: Sensitivity of the supervision, as a percentage: the lower the value, the sooner a collision is reported. Null when the controller did not report it.

## RapidActivationRecord

`class RapidActivationRecord`

One frame of the call stack of a task: which routine is running and where the execution stands in it. Returned by RapidService.GetActivationRecord(). Frame 1 is the routine holding the program pointer, and the number grows towards the entry point of the program.

- `RapidActivationRecord()`: Initializes a new instance of the Data.RapidActivationRecord class
- `int? BeginColumn { get; set; }`: Column the executing statement starts at, null when the controller did not report it
- `int? BeginRow { get; set; }`: Line the executing statement starts at, null when the controller did not report it
- `int? EndColumn { get; set; }`: Column the executing statement ends at, null when the controller did not report it
- `int? EndRow { get; set; }`: Line the executing statement ends at, null when the controller did not report it
- `RapidExecutionLevel ExecutionLevel { get; set; }`: Level at which this frame is executing
- `string RoutineUrl { get; set; }`: Path of the routine this frame is executing
- `string StackUrl { get; set; }`: Path identifying this stack frame, which the UI instruction resources also take

## RapidAliasIoItem

`class RapidAliasIoItem`

An I/O signal a running RAPID program has given an alias to with the AliasIO instruction. Returned by RapidService.GetAliasIo(). The controller only knows about an alias while the program that declares it is loaded, so this list is empty on a controller holding no such program.

- `RapidAliasIoItem()`: Initializes a new instance of the Data.RapidAliasIoItem class
- `string AliasName { get; set; }`: Name the RAPID program refers to the signal by
- `string SignalName { get; set; }`: Name of the I/O signal the alias points at
- `IoSignalType Type { get; set; }`: Type of the aliased signal

## RapidBreakpoint

`class RapidBreakpoint`

A breakpoint set in the program of a task. Returned by RapidService.GetBreakpoints() and RapidService.SetBreakpoint(). The controller answers a write with the range it actually snapped the breakpoint to, which is the whole instruction containing the requested position rather than the position its...

- `RapidBreakpoint()`: Initializes a new instance of the Data.RapidBreakpoint class
- `int? EndColumn { get; set; }`: Column the breakpoint ends at, null when the controller did not report it
- `int? EndRow { get; set; }`: Line the breakpoint ends at, null when the controller did not report it
- `string ModuleName { get; set; }`: Name of the module the breakpoint sits in, null when the controller did not report it
- `int? StartColumn { get; set; }`: Column the breakpoint starts at, null when the controller did not report it
- `int? StartRow { get; set; }`: Line the breakpoint starts at, null when the controller did not report it

## RapidBuildError

`class RapidBuildError`

An error the controller found while linking the program of a task. Returned by RapidService.GetBuildErrors().

- `RapidBuildError()`: Initializes a new instance of the Data.RapidBuildError class
- `int? Column { get; set; }`: Column the error was found at, null when the controller did not report it
- `string Error { get; set; }`: Description of the error as the controller worded it
- `int? ErrorNumber { get; set; }`: Numeric identifier of the error, null when the controller did not report it
- `string ModuleName { get; set; }`: Name of the module the error was found in
- `int? Row { get; set; }`: Line the error was found at, null when the controller did not report it

## RapidExecutionCycle

`enum RapidExecutionCycle`

How many times the controller runs the program before stopping

- AsIs: The cycle currently configured is left untouched
- Forever: The program runs again every time it reaches its end
- Once: The program runs once and stops at its end
- OnceDone: The program was asked to run once and has finished doing so
- Unknown: The controller reported a cycle this library does not know

## RapidExecutionInfo

`class RapidExecutionInfo`

Overall RAPID execution state of the controller. Returned by RapidService.GetExecutionState().

- `RapidExecutionInfo()`: Initializes a new instance of the Data.RapidExecutionInfo class
- `RapidExecutionCycle Cycle { get; set; }`: Number of cycles the program is set to run
- `RapidExecutionState State { get; set; }`: Whether RAPID code is currently running

## RapidExecutionLevel

`enum RapidExecutionLevel`

Level at which the code of a task is currently executing

- None: Nothing is executing
- Normal: The normal user code is executing
- Trap: A trap routine is executing
- Unknown: The controller reported a level this library does not know
- User: A user routine is executing

## RapidExecutionMode

`enum RapidExecutionMode`

How far the program advances when execution is started

- Continue: Run until something stops it
- StepBack: Step one instruction backwards
- StepIn: Step into the routine called by the current instruction
- StepLast: Step to the last instruction
- StepMotion: Step to the next motion instruction
- StepOut: Run until the current routine returns
- StepOver: Run the current instruction whole, without entering the routine it calls

## RapidExecutionState

`enum RapidExecutionState`

Whether the controller is currently executing RAPID code

- Running: RAPID execution is running
- Stopped: RAPID execution is stopped
- Unknown: The controller reported a state this library does not know

## RapidExecutionType

`enum RapidExecutionType`

What kind of code a task is currently running

- EventRoutine: An event routine is running
- ExternalInterrupt: An external interrupt is running
- Interrupt: An interrupt is running
- None: Nothing is running
- Normal: The normal program is running
- Unknown: The controller reported a type this library does not know
- UserRoutine: A user routine is running

## RapidExternalJointStates

`class RapidExternalJointStates`

What each of the six external joints of a task is doing, which says how to read the corresponding value of an external axis. Returned by RapidService.GetExternalJointStates(). A joint reported as RapidJointState.NotActive carries no meaningful position.

- `RapidExternalJointStates()`: Initializes a new instance of the Data.RapidExternalJointStates class
- `RapidJointState Joint1 { get; set; }`: State of the first external joint
- `RapidJointState Joint2 { get; set; }`: State of the second external joint
- `RapidJointState Joint3 { get; set; }`: State of the third external joint
- `RapidJointState Joint4 { get; set; }`: State of the fourth external joint
- `RapidJointState Joint5 { get; set; }`: State of the fifth external joint
- `RapidJointState Joint6 { get; set; }`: State of the sixth external joint

## RapidHoldToRunState

`enum RapidHoldToRunState`

State of the hold-to-run control that gates RAPID execution in manual mode

- Held: Confirm that execution may keep running, which has to be repeated about every two seconds
- Press: Ask for execution to be allowed to start
- Release: Stop execution immediately

## RapidInstructionTemplate

`class RapidInstructionTemplate`

The template the controller suggests for an instruction or a data type: the arguments to write and the values to write them with. Returned by RapidService.GetInstructionTemplate(). An editor uses it to insert a complete, valid instruction rather than a bare keyword.

- `RapidInstructionTemplate()`: Initializes a new instance of the Data.RapidInstructionTemplate class
- `int? ArgumentCount { get; set; }`: Number of arguments the controller reported, null when it did not report it
- `RapidInstructionTemplateArgument[] Arguments { get; set; }`: The suggested arguments
- `bool? Complete { get; set; }`: Whether every argument has been reported, null when the controller did not report it
- `int? Mark { get; set; }`: Index the controller started reporting from, null when it did not report it
- `int? SelectedParameter { get; set; }`: Argument the controller suggests selecting first, null when it did not report it
- `string Version { get; set; }`: Version the controller stamps on the template

## RapidInstructionTemplateArgument

`class RapidInstructionTemplateArgument`

One argument of the template the controller suggests for an instruction or a data type. Carried by Data.RapidInstructionTemplate.

- `RapidInstructionTemplateArgument()`: Initializes a new instance of the Data.RapidInstructionTemplateArgument class
- `int? ArgumentNumber { get; set; }`: Position of the argument, null when the controller did not report it
- `string DataType { get; set; }`: Type of the argument, for example "robtarget"
- `bool? DeclarationNeeded { get; set; }`: Whether inserting the instruction also needs a declaration to be created for this argument, null when the controller did not report it
- `int? Dimensions { get; set; }`: Number of array dimensions of the argument, null when the controller did not report it
- `bool? Local { get; set; }`: Whether the suggested symbol is local to its module, null when the controller did not report it
- `string Name { get; set; }`: Name of the argument, for example "ToPoint"
- `string ObjectType { get; set; }`: How the suggested symbol is declared, for example "CONST" or "TASK PERS"
- `bool? Required { get; set; }`: Whether the argument has to be given, null when the controller did not report it
- `string Symbol { get; set; }`: Name of the symbol the argument refers to, empty when the argument is written as a literal
- `string Value { get; set; }`: Value the argument is suggested with, written the way RAPID writes it

## RapidJointState

`enum RapidJointState`

What an external joint of a task is doing

- Linear: The joint moves along a line
- NoPosition: The joint is active but has no position
- NotActive: The joint is not active
- Rotating: The joint turns
- Unknown: The controller reported a state this library does not know

## RapidMechanicalUnitItem

`class RapidMechanicalUnitItem`

A mechanical unit the positions of a task are expressed in. Returned by RapidService.GetMechanicalUnits(). This is the view the RAPID task has of the unit; MotionSystemService.GetMechanicalUnits() answers with everything the motion system knows about the same units.

- `RapidMechanicalUnitItem()`: Initializes a new instance of the Data.RapidMechanicalUnitItem class
- `MechanicalUnitMode Mode { get; set; }`: Whether the unit is activated
- `string Name { get; set; }`: Name of the unit, for example "ROB_1"
- `MechanicalUnitType Type { get; set; }`: Kind of unit

## RapidModifiablePositionItem

`class RapidModifiablePositionItem`

One motion instruction of the system whose position can be rewritten to where the robot currently stands, wherever in whichever task it sits. Returned by RapidService.GetAllModifiablePositions().

- `RapidModifiablePositionItem()`: Initializes a new instance of the Data.RapidModifiablePositionItem class
- `int? EndColumn { get; set; }`: Column the instruction ends at, null when the controller did not report it
- `int? EndRow { get; set; }`: Line the instruction ends at, null when the controller did not report it
- `string ModuleName { get; set; }`: Name of the module holding the instruction
- `int? StartColumn { get; set; }`: Column the instruction starts at, null when the controller did not report it
- `int? StartRow { get; set; }`: Line the instruction starts at, null when the controller did not report it
- `string TaskName { get; set; }`: Name of the task holding the module

## RapidModifiablePositions

`class RapidModifiablePositions`

How many motion instructions of a range can have their position rewritten to where the robot currently stands, and which range they cover. Returned by RapidService.GetModifiablePositions(). The controller leaves the range empty when it found nothing modifiable.

- `RapidModifiablePositions()`: Initializes a new instance of the Data.RapidModifiablePositions class
- `int? EndColumn { get; set; }`: Column the modifiable range ends at, null when the controller did not report it
- `int? EndRow { get; set; }`: Line the modifiable range ends at, null when the controller did not report it
- `int ModifiableLineCount { get; set; }`: Number of motion instructions of the range whose position can be rewritten
- `int? StartColumn { get; set; }`: Column the modifiable range starts at, null when the controller did not report it
- `int? StartRow { get; set; }`: Line the modifiable range starts at, null when the controller did not report it

## RapidModuleAttribute

`enum RapidModuleAttribute`

A property declared on a module, which restricts what may be done with it

- Encoded: The source of the module is encoded and cannot be read back
- NoStepIn: Execution may not step into the routines of the module
- NoView: The source of the module may not be displayed
- ReadOnly: The module may not be changed
- SystemModule: The module belongs to the system rather than to the program
- Unknown: The controller reported an attribute this library does not know
- ViewOnly: The source may be displayed but not changed

## RapidModuleExtension

`class RapidModuleExtension`

How big the source of a module is, which is what it takes to ask for the whole of it as a range. Returned by RapidService.GetModuleExtension().

- `RapidModuleExtension()`: Initializes a new instance of the Data.RapidModuleExtension class
- `int? ChangeCount { get; set; }`: Counter the controller increments whenever the module changes, null when it did not report it
- `int? LineCount { get; set; }`: Number of lines the module holds, null when the controller did not report it
- `int? MaxColumnCount { get; set; }`: Length of the longest line of the module, null when the controller did not report it

## RapidModuleInfo

`class RapidModuleInfo : RapidModuleItem`

Everything the controller reports about one module. Returned by RapidService.GetModule(); the module lists only carry the properties of the Data.RapidModuleItem base class.

- `RapidModuleInfo()`: Initializes a new instance of the Data.RapidModuleInfo class
- `int AttributeCount { get; }`: Number of properties declared on the module
- `RapidModuleAttribute[] Attributes { get; set; }`: Properties declared on the module, empty when it declares none
- `string FileName { get; set; }`: Name of the file the module was loaded from, for example "MainModule.mod"
- Inherited from [RapidModuleItem](UnderAutomation.ABB.Rws.Data.md#rapidmoduleitem): `Name`, `Type`

## RapidModuleItem

`class RapidModuleItem`

A module loaded into a task, as listed by RapidService.GetModules(). RapidService.GetModule() returns a Data.RapidModuleInfo, which adds the file the module came from and the attributes declared on it.

- `RapidModuleItem()`: Initializes a new instance of the Data.RapidModuleItem class
- `string Name { get; set; }`: Name of the module, for example "MainModule"
- `RapidModuleType Type { get; set; }`: Whether the module belongs to the program or to the system

## RapidModuleSymbol

`class RapidModuleSymbol`

The declaration the controller finds at a given position of a module. Returned by RapidService.GetModuleSymbol(), which returns null when there is no declaration at that position.

- `RapidModuleSymbol()`: Initializes a new instance of the Data.RapidModuleSymbol class
- `string DataType { get; set; }`: Name of the type of the symbol, for example "robtarget"
- `int? Dimensions { get; set; }`: Number of array dimensions of the symbol, null when the controller did not report it
- `bool? Heap { get; set; }`: Whether the symbol is allocated on the heap, null when the controller did not report it
- `bool? Linked { get; set; }`: Whether the declaration is complete, null when the controller did not report it
- `bool? Local { get; set; }`: Whether the symbol is local to its module, null when the controller did not report it
- `string Name { get; set; }`: Name of the declared symbol
- `int? ReferenceCount { get; set; }`: How many times the symbol is referred to, null when the controller did not report it
- `int? Storage { get; set; }`: How the controller stores the symbol, null when it did not report it
- `RapidSymbolType SymbolType { get; set; }`: What kind of symbol was declared
- `string SymbolUrl { get; set; }`: Path of the symbol, which the symbol resources take
- `string TypeUrl { get; set; }`: Path of the type of the symbol
- `string Version { get; set; }`: Version the controller stamps on the declaration

## RapidModuleText

`class RapidModuleText`

The source of a module and the counters that go with it. Returned by RapidService.GetModuleText().

- `RapidModuleText()`: Initializes a new instance of the Data.RapidModuleText class
- `int? ChangeCount { get; set; }`: Counter the controller increments whenever the module changes, null when it did not report it
- `int? DeclaredLength { get; set; }`: Length the controller declares for the module, null when it did not report it. This is the size the controller reserves for the module and not the length of RapidModuleText.Text, so the two normally differ.
- `string Text { get; set; }`: Source of the module

## RapidModuleType

`enum RapidModuleType`

Whether a module belongs to the program or to the system

- ProgramModule: A module of the program, saved and loaded with it
- SystemModule: A module of the system, which survives loading another program
- Unknown: The controller reported a type this library does not know

## RapidObjectChild

`class RapidObjectChild`

The parts a RAPID object is made of, and where each of them sits in the source. Returned by RapidService.GetObjectChildren(). Which parts the controller reports depends entirely on what the object is: a module answers with its name, its attributes and its declaration lists, a routine with somethi...

- `RapidObjectChild()`: Initializes a new instance of the Data.RapidObjectChild class
- `RapidTextRange GetRange(string name)`: Returns the span of one part by its name, null when the controller did not report it
- `string ObjectType { get; set; }`: What the object is, for example "module"
- `int RangeCount { get; }`: Number of parts the controller reported
- `RapidObjectChildRange[] Ranges { get; set; }`: The parts of the object, including the ones it does not hold, whose span is then empty

## RapidObjectChildRange

`class RapidObjectChildRange`

One named part of a RAPID object, and where it sits in the source. Carried by Data.RapidObjectChild.

- `RapidObjectChildRange()`: Initializes a new instance of the Data.RapidObjectChildRange class
- `bool IsPresent { get; }`: Whether the controller reported a real span for the part, which it does not when the object does not hold it
- `string Name { get; set; }`: Name of the part as the controller worded it, for example "data-decl" or "endmod"
- `RapidTextRange Range { get; set; }`: Where the part sits in the source

## RapidObjectListExtension

`class RapidObjectListExtension`

Where one of the lists of a RAPID object sits in the source: the span of the whole list, and the spans of its first and last elements. Returned by RapidService.GetObjectListExtension(). An editor uses it to jump to the beginning or the end of a list without reading the module. The controller repo...

- `RapidObjectListExtension()`: Initializes a new instance of the Data.RapidObjectListExtension class
- `RapidTextRange First { get; set; }`: Span of the first element of the list
- `RapidTextRange Last { get; set; }`: Span of the last element of the list
- `RapidTextRange List { get; set; }`: Span of the whole list

## RapidObjectListType

`enum RapidObjectListType`

Which of the lists a RAPID object holds is being asked about

- Attributes: The attributes it declares
- BackwardStatements: The statements of its BACKWARD handler
- DataDeclarations: The data declarations it holds
- ErrorStatements: The statements of its ERROR handler
- ParameterDeclarations: The parameter declarations it holds
- RoutineDeclarations: The routine declarations it holds
- Statements: The statements of the object
- TypeDeclarations: The type declarations it holds
- UndoStatements: The statements of its UNDO handler

## RapidPalletHeadItem

`class RapidPalletHeadItem`

One category of the instruction palette the FlexPendant editor offers, for example "Prog.Flow". Returned by RapidService.GetPalletHeads(); its RapidPalletHeadItem.Number is what RapidService.GetPallet() takes.

- `RapidPalletHeadItem()`: Initializes a new instance of the Data.RapidPalletHeadItem class
- `string Name { get; set; }`: Name of the category, for example "Motion&amp;Proc."
- `int? Number { get; set; }`: Number identifying the category, null when the controller did not report it

## RapidPalletItem

`class RapidPalletItem`

One entry of an instruction palette category, which an editor offers as something the operator can insert at the cursor. Returned by RapidService.GetPallet().

- `RapidPalletItem()`: Initializes a new instance of the Data.RapidPalletItem class
- `int? Alternative { get; set; }`: Alternative of the parameter the entry preselects, null when the controller did not report it
- `string Instruction { get; set; }`: Instruction the entry inserts
- `int? Keyword { get; set; }`: Whether the entry is a language keyword rather than an instruction, null when the controller did not report it
- `string Name { get; set; }`: Name shown for the entry, for example "MoveJ"
- `int? Parameter { get; set; }`: Parameter the entry preselects, null when the controller did not report it

## RapidPointerPosition

`class RapidPointerPosition`

Where one of the two pointers of a task stands. Carried by Data.RapidPointers. RapidPointerPosition.Available tells apart a pointer that is really placed somewhere from one the controller could not report, which happens for the motion pointer whenever the task has not moved yet.

- `RapidPointerPosition()`: Initializes a new instance of the Data.RapidPointerPosition class
- `bool Available { get; set; }`: Whether the controller reported a position for this pointer at all
- `int? BeginColumn { get; set; }`: Column the pointer begins at, null when the controller did not report it
- `int? BeginRow { get; set; }`: Line the pointer begins at, null when the controller did not report it
- `int? ChangeCount { get; set; }`: How many times the pointer has been moved, null when the controller did not report it
- `int? EndColumn { get; set; }`: Column the pointer ends at, null when the controller did not report it
- `int? EndRow { get; set; }`: Line the pointer ends at, null when the controller did not report it
- `RapidExecutionType ExecutionType { get; set; }`: What kind of code the pointer is standing in
- `string Module { get; set; }`: Name of the module the pointer stands in
- `string Routine { get; set; }`: Name of the routine the pointer stands in

## RapidPointerSyncState

`enum RapidPointerSyncState`

Whether the pointers of every task are synchronized with each other

- Off: The pointers are not synchronized
- On: The pointers are synchronized
- Unknown: The controller reported a state this library does not know

## RapidPointers

`class RapidPointers`

The program pointer and the motion pointer of a task, read in one request. Returned by RapidService.GetPointers(). The program pointer says which instruction runs next, the motion pointer which one the robot is actually executing; they drift apart because the controller plans the path ahead of th...

- `RapidPointers()`: Initializes a new instance of the Data.RapidPointers class
- `RapidPointerPosition MotionPointer { get; set; }`: Instruction the robot is currently moving for
- `RapidPointerPosition ProgramPointer { get; set; }`: Instruction the task will execute next

## RapidPreferredDataTypeItem

`class RapidPreferredDataTypeItem`

A data type the controller suggests for one argument of an instruction, so that an editor can offer the operator the types that fit where the cursor stands. Returned by RapidService.GetPreferredDataTypes().

- `RapidPreferredDataTypeItem()`: Initializes a new instance of the Data.RapidPreferredDataTypeItem class
- `string DataType { get; set; }`: Data type of the suggestion
- `string Name { get; set; }`: Name of the suggestion, for example "signaldi"

## RapidProgramCounterPosition

`class RapidProgramCounterPosition`

Where the program pointer of a task stands, expressed as the piece of source it points at. Returned by RapidService.GetProgramCounterPosition(). The controller refuses the request when the task has no program pointer set, so reset it or start the program first.

- `RapidProgramCounterPosition()`: Initializes a new instance of the Data.RapidProgramCounterPosition class
- `int? EndColumn { get; set; }`: Column the pointed instruction ends at, null when the controller did not report it
- `int? EndLine { get; set; }`: Line the pointed instruction ends at, null when the controller did not report it
- `string Module { get; set; }`: Name of the module the pointer stands in
- `string Routine { get; set; }`: Name of the routine the pointer stands in
- `int? StartColumn { get; set; }`: Column the pointed instruction starts at, null when the controller did not report it
- `int? StartLine { get; set; }`: Line the pointed instruction starts at, null when the controller did not report it

## RapidProgramInfo

`class RapidProgramInfo`

The program loaded into a task. Returned by RapidService.GetProgram(), which returns null when the task holds no program at all.

- `RapidProgramInfo()`: Initializes a new instance of the Data.RapidProgramInfo class
- `string EntryPoint { get; set; }`: Routine the program pointer moves to when it is reset, null when the controller did not report it
- `string Name { get; set; }`: Name of the program, null when the controller did not report it

## RapidProgramLoadMode

`enum RapidProgramLoadMode`

What happens to the modules already in a task when a program is loaded into it

- Add: Keep the modules already loaded and add the ones of the program
- Replace: Replace everything the task holds with the program

## RapidRegainMode

`enum RapidRegainMode`

What the robot does about the distance between where it stands and where the path it is about to resume expects it to be

- Clear: Drop the path and resume from the current position
- Continue: Resume from the current position without moving back to the path
- EnterConsume: Resume by entering the consumption of the already generated path
- Regain: Move back onto the path before resuming

## RapidRoutineArgument

`class RapidRoutineArgument`

One argument of the routine call found at a given position of a module, and where it sits in the source. Returned by RapidService.GetRoutineArguments().

- `RapidRoutineArgument()`: Initializes a new instance of the Data.RapidRoutineArgument class
- `int? AlternateArgument { get; set; }`: Which alternative of the parameter this argument fills, null when the controller did not report it
- `string DataType { get; set; }`: Type of the argument, for example "num"
- `int? EndColumn { get; set; }`: Column the argument ends at, null when the controller did not report it
- `int? EndRow { get; set; }`: Line the argument ends at, null when the controller did not report it
- `int? ListLength { get; set; }`: Length of the argument list, null when the controller did not report it
- `int? ListNumber { get; set; }`: Position of the argument in the argument list, null when the controller did not report it
- `string ObjectType { get; set; }`: What the argument is, for example a required argument or a name reference
- `int? ParameterNumber { get; set; }`: Position of the argument in the call, counted from 0
- `int? StartColumn { get; set; }`: Column the argument starts at, null when the controller did not report it
- `int? StartRow { get; set; }`: Line the argument starts at, null when the controller did not report it

## RapidRoutineInfo

`class RapidRoutineInfo`

The routine the controller finds called at a given position of a module. Returned by RapidService.GetRoutine(). The controller refuses the request when the position does not sit on a routine call.

- `RapidRoutineInfo()`: Initializes a new instance of the Data.RapidRoutineInfo class
- `bool? Local { get; set; }`: Whether the routine is local to its module, null when the controller did not report it
- `string Name { get; set; }`: Name of the routine
- `bool? Named { get; set; }`: Whether the routine is named, null when the controller did not report it
- `int? ParameterCount { get; set; }`: Number of parameters the routine takes, null when the controller did not report it. The controller reports -1 when the parameter list is not linked yet.
- `RapidSymbolType SymbolType { get; set; }`: Whether the routine is a procedure, a function or a trap
- `string SymbolUrl { get; set; }`: Path of the routine, which the program pointer resources take

## RapidServiceRoutineItem

`class RapidServiceRoutineItem`

A routine of a task the program pointer can be moved to. Returned by RapidService.GetServiceRoutines().

- `RapidServiceRoutineItem()`: Initializes a new instance of the Data.RapidServiceRoutineItem class
- `bool? IsServiceRoutine { get; set; }`: Whether this is a service routine rather than an ordinary one, null when the controller did not report it
- `string Name { get; set; }`: Name of the routine, for example "LoadIdentify"
- `string Url { get; set; }`: Path of the routine, which RapidService.SetProgramPointerToRoutineUrl() takes

## RapidSetTextRangeResult

`class RapidSetTextRangeResult`

What the controller did with a change written into the source of a module. Returned by RapidService.SetModuleTextRange(). Rewriting the MODULE line renames the module, which is why the controller reports the name it ended up with.

- `RapidSetTextRangeResult()`: Initializes a new instance of the Data.RapidSetTextRangeResult class
- `int? ChangeCount { get; set; }`: Counter the controller incremented for the change, null when it did not report it
- `bool ModuleRenamed { get; set; }`: Whether the change renamed the module
- `string NewModuleName { get; set; }`: Name the module now has, empty when the change did not rename it

## RapidSpyStatus

`enum RapidSpyStatus`

Whether the controller is recording the RAPID execution trace to a file

- Logging: The execution trace is being written
- NotLogging: No execution trace is being written
- Unknown: The controller reported a status this library does not know

## RapidStartCondition

`enum RapidStartCondition`

Condition the controller checks before it starts executing

- CallChain: Start only when the call chain of the program pointer is still valid
- None: Start without any additional check

## RapidStopMode

`enum RapidStopMode`

How abruptly RAPID execution is stopped

- Cycle: Stop when the current cycle ends
- Instruction: Stop when the current instruction ends
- QuickStop: Stop as fast as the robot can, leaving the path
- Stop: Stop as soon as the robot can decelerate along its path

## RapidStructuralChangeCount

`class RapidStructuralChangeCount`

The two counters a task keeps of what has changed in it, so that a client can tell whether it needs to read the task again instead of fetching everything periodically. Returned by RapidService.GetStructuralChangeCount().

- `RapidStructuralChangeCount()`: Initializes a new instance of the Data.RapidStructuralChangeCount class
- `int? ChangeCount { get; set; }`: Counter the controller increments whenever anything relevant changes in the task
- `int? StructuralChangeCount { get; set; }`: Counter the controller increments when a module is loaded, unloaded or renamed. A rename counts as an unload followed by a load.

## RapidSymbolProperties

`class RapidSymbolProperties`

What a RAPID symbol is declared as. Returned by RapidService.GetSymbolProperties() and RapidService.SearchSymbols(). A search fills in RapidSymbolProperties.Name and leaves RapidSymbolProperties.Storage alone, a direct read does the opposite on some controllers, so treat both as optional.

- `RapidSymbolProperties()`: Initializes a new instance of the Data.RapidSymbolProperties class
- `string DataType { get; set; }`: Name of the type of the symbol, for example "num"
- `string Dimension { get; set; }`: Size of each array dimension as the controller worded it, empty when the symbol is not an array
- `int? Dimensions { get; set; }`: Number of array dimensions of the symbol, null when the controller did not report it
- `bool? Heap { get; set; }`: Whether the symbol is allocated on the heap, null when the controller did not report it
- `bool? Linked { get; set; }`: Whether the declaration is complete, null when the controller did not report it
- `bool? Local { get; set; }`: Whether the symbol is local to its module, null when the controller did not report it
- `string Name { get; set; }`: Name of the symbol, for example "reg1"
- `bool? Named { get; set; }`: Whether the symbol is named, null when the controller did not report it
- `bool? ReadOnly { get; set; }`: Whether the symbol may not be written, null when the controller did not report it
- `string Storage { get; set; }`: How the controller stores the symbol, for example "loaded"
- `RapidSymbolType SymbolType { get; set; }`: What kind of symbol this is
- `string SymbolUrl { get; set; }`: Path of the symbol, which the other symbol methods take
- `bool? TaskVariable { get; set; }`: Whether the symbol is global within its task, null when the controller did not report it
- `string TypeUrl { get; set; }`: Path of the type of the symbol, for example "RAPID/num"

## RapidSymbolSearchCriteria

`class RapidSymbolSearchCriteria`

What a symbol search looks for. Passed to RapidService.SearchSymbols(). Every property is optional; leaving one alone means the search does not filter on it. A search with no criterion at all walks the whole system, which is slow, so at least set RapidSymbolSearchCriteria.BlockUrl.

- `RapidSymbolSearchCriteria()`: Initializes a new instance of the Data.RapidSymbolSearchCriteria class
- `string BlockUrl { get; set; }`: Path the search starts from, for example "RAPID/T_ROB1"
- `string DataType { get; set; }`: Name of the type a symbol has to have to be kept, for example "robtarget"
- `string NamePattern { get; set; }`: Regular expression the name of a symbol has to match to be kept
- `bool? OnlyUsed { get; set; }`: Whether only the symbols the program actually refers to are kept, null to leave it to the controller
- `int? PositionColumn { get; set; }`: Column the search starts from, used together with RapidSymbolSearchView.Scope
- `int? PositionRow { get; set; }`: Line the search starts from, used together with RapidSymbolSearchView.Scope
- `bool? Recursive { get; set; }`: Whether the search also walks what the starting point contains, null to leave it to the controller
- `bool? SkipShared { get; set; }`: Whether the symbols shared between tasks are skipped, null to leave it to the controller
- `int? StackFrame { get; set; }`: Frame of the call stack the search starts from, used together with RapidSymbolSearchView.Stack
- `RapidSymbolType[] SymbolTypes { get; set; }`: Kinds of symbol the search keeps, empty to keep every kind
- `RapidSymbolVariableType VariableType { get; set; }`: Which variables the search keeps, by what may be done with them
- `RapidSymbolSearchView View { get; set; }`: Which part of the system the search walks

## RapidSymbolSearchView

`enum RapidSymbolSearchView`

Which part of the system a symbol search walks

- Block: Search the block the search path names, and optionally what it contains
- Scope: Search what is visible from a position of the source, which the search path and the position both have to be given for
- Stack: Search what is visible from a frame of the call stack, which needs the program pointer to be set
- Undefined: Let the controller decide

## RapidSymbolType

`enum RapidSymbolType`

What a RAPID symbol is: a value, a routine, a type or one of the structural elements of the language

- Alias: An alias of another type
- Any: Any of the other types, which a search uses to mean that it does not filter on the type
- Atomic: A built-in type such as num or string
- Constant: A constant
- ForVariable: The loop variable of a FOR statement
- Function: A function
- Label: A label
- Module: A module
- Parameter: A parameter of a routine
- Persistent: A persistent variable, whose value survives a restart
- Procedure: A procedure
- Record: A record type
- RecordComponent: One component of a record
- Task: A task
- Trap: A trap routine
- Undefined: The type is not defined
- Unknown: The controller reported a type this library does not know
- Variable: A variable

## RapidSymbolValue

`class RapidSymbolValue`

The value of a RAPID symbol and where it is declared. Returned by RapidService.GetSymbolValue(). The value is the text the controller wrote it as, which for a record is the bracketed form RAPID itself uses, for example [[515,0,712],[0.707107,0,0.707107,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,...

- `RapidSymbolValue()`: Initializes a new instance of the Data.RapidSymbolValue class
- `RapidTextRange DeclarationPosition { get; set; }`: Where the symbol is declared, null when the controller did not report it
- `RapidTextRange InitialValuePosition { get; set; }`: Where the initial value of the symbol is written, null when the controller did not report it. The controller reports zeros when the declaration carries no initial value.
- `string Value { get; set; }`: Value of the symbol, written the way RAPID writes it

## RapidSymbolVariableType

`enum RapidSymbolVariableType`

Which variables a symbol search keeps, by what may be done with them

- Any: Any of them
- Loop: Only the loop variables
- ReadOnly: Only the variables that can be read but not written
- ReadWrite: Only the variables that can be read and written
- Undefined: Let the controller decide

## RapidTaskExecutionMode

`enum RapidTaskExecutionMode`

Stepping mode a task was last started with

- Continuous: The task runs without stepping
- StepBack: The task steps backwards
- StepIn: The task steps into the routine calls
- StepLast: The task steps to the last instruction
- StepOutOf: The task steps out of the current routine
- StepOver: The task steps over the routine calls
- StepWise: The task advances one instruction at a time
- Unknown: The controller reported a mode this library does not know

## RapidTaskExecutionState

`enum RapidTaskExecutionState`

Whether a single task is running, and whether it could be

- Ready: The task is ready to be started
- Started: The task is running
- Stopped: The task was running and has been stopped
- Uninitialized: The task is not initialized
- Unknown: The controller reported a state this library does not know

## RapidTaskInfo

`class RapidTaskInfo : RapidTaskItem`

Everything the controller reports about one RAPID task. Returned by RapidService.GetTask(); the task lists only carry the properties of the Data.RapidTaskItem base class.

- `RapidTaskInfo()`: Initializes a new instance of the Data.RapidTaskInfo class
- `bool? BindReference { get; set; }`: Whether the task is bound to a configured task number, null when the controller did not report it
- `RapidExecutionCycle ExecutionCycle { get; set; }`: Number of cycles the task is set to run. Only reported over a connection established with version 2, and left to RapidExecutionCycle.Unknown otherwise.
- `RapidExecutionLevel ExecutionLevel { get; set; }`: Level at which the code of the task is currently executing
- `RapidTaskExecutionMode ExecutionMode { get; set; }`: Stepping mode the task was last started with
- `RapidExecutionType ExecutionType { get; set; }`: What kind of code the task is currently running
- `string ProductionEntryPoint { get; set; }`: Routine the program pointer moves to when it is reset, for example "main"
- `int? TaskId { get; set; }`: Identifier of the task, null when the controller did not report it
- `string TaskInForeground { get; set; }`: Name of the task running in the foreground, empty when there is none
- `RapidTaskTrustLevel Trust { get; set; }`: What the controller does to the system when this task stops unexpectedly
- Inherited from [RapidTaskItem](UnderAutomation.ABB.Rws.Data.md#rapidtaskitem): `Name`, `Type`, `TaskState`, `ExecutionState`, `Active`, `MotionTask`

## RapidTaskItem

`class RapidTaskItem`

A RAPID task of the controller, as listed by RapidService.GetTasks(). RapidService.GetTask() returns a Data.RapidTaskInfo, which adds everything the controller reports for a single task only.

- `RapidTaskItem()`: Initializes a new instance of the Data.RapidTaskItem class
- `bool? Active { get; set; }`: Whether the task is active, null when the controller did not report it
- `RapidTaskExecutionState ExecutionState { get; set; }`: Whether the task is running, and whether it could be
- `bool? MotionTask { get; set; }`: Whether the task can move a mechanical unit, null when the controller did not report it
- `string Name { get; set; }`: Name of the task, for example "T_ROB1"
- `RapidTaskState TaskState { get; set; }`: How far the controller has got in preparing the program of the task
- `RapidTaskType Type { get; set; }`: Kind of task, which decides when the controller runs it

## RapidTaskScope

`enum RapidTaskScope`

Whether an execution command applies to the normal tasks only or to every task

- AllTasks: Apply to every task of the system
- Normal: Apply to the tasks the task selection panel has enabled

## RapidTaskSelectionItem

`class RapidTaskSelectionItem`

One line of the task selection panel, telling whether a task is selected and whether an operator is allowed to change that. Returned by RapidService.GetTaskSelection().

- `RapidTaskSelectionItem()`: Initializes a new instance of the Data.RapidTaskSelectionItem class
- `bool? MotionTask { get; set; }`: Whether the task can move a mechanical unit, null when the controller did not report it
- `string Name { get; set; }`: Name of the task, for example "T_ROB1"
- `bool? Selected { get; set; }`: Whether the task is selected, null when the controller did not report it
- `bool? UserModify { get; set; }`: Whether an operator is allowed to change the selection of this task, null when the controller did not report it

## RapidTaskState

`enum RapidTaskState`

How far the controller has got in preparing the program of a task

- Empty: The task holds no program
- Initiated: The task has been created but its program is not linked yet
- Linked: The program of the task is linked and ready to run
- Loaded: A program is loaded into the task but not linked yet
- Uninitialized: The task is not initialized
- Unknown: The controller reported a state this library does not know

## RapidTaskTrustLevel

`enum RapidTaskTrustLevel`

What the controller does to the system when a task that is not a normal one stops unexpectedly

- None: The system carries on
- SystemFailure: The whole system fails
- SystemHalt: The system halts
- SystemStop: The system stops
- Unknown: The controller reported a level this library does not know

## RapidTaskType

`enum RapidTaskType`

Kind of RAPID task, which decides when the controller runs it

- Normal: A task started and stopped together with the program
- SemiStatic: A task restarted from its beginning every time the controller starts
- Static: A task that keeps its program pointer where it was when the controller was switched off
- Unknown: The controller reported a type this library does not know

## RapidTextPosition

`class RapidTextPosition`

A position in the source of a module, counted from 1. Returned by RapidService.SearchModuleText(), which reports row and column 0 when the text was not found rather than failing.

- `RapidTextPosition()`: Initializes a new instance of the Data.RapidTextPosition class
- `int Column { get; set; }`: Column of the position, 0 when the search found nothing
- `bool Found { get; }`: Whether the position points at something, which it does not when a search found nothing
- `int Row { get; set; }`: Line of the position, 0 when the search found nothing

## RapidTextQueryMode

`enum RapidTextQueryMode`

How hard the controller tries to apply a change to the source of a running task

- Force: Apply the change even when it invalidates the program pointer
- Try: Apply the change only when the program pointer survives it

## RapidTextRange

`class RapidTextRange`

A span of source between two positions, counted from 1. Used wherever the controller reports where something is declared or where a statement sits.

- `RapidTextRange()`: Initializes a new instance of the Data.RapidTextRange class
- `int? BeginColumn { get; set; }`: Column the range begins at, null when the controller did not report it
- `int? BeginRow { get; set; }`: Line the range begins at, null when the controller did not report it
- `int? EndColumn { get; set; }`: Column the range ends at, null when the controller did not report it
- `int? EndRow { get; set; }`: Line the range ends at, null when the controller did not report it

## RapidTextReplaceMode

`enum RapidTextReplaceMode`

Where new text is put relative to the range it is written against

- After: Insert the new text after the range, leaving it in place
- Before: Insert the new text before the range, leaving it in place
- Replace: Replace the range with the new text

## RapidUiInstruction

`class RapidUiInstruction`

The dialogue a running RAPID program is currently asking an operator for. Returned by RapidService.GetActiveUiInstruction(), which returns null when no instruction is pending. Answering one means writing its parameters with RapidService.SetUiInstructionParameter(), using RapidUiInstruction.StackU...

- `RapidUiInstruction()`: Initializes a new instance of the Data.RapidUiInstruction class
- `RapidUiInstructionEvent Event { get; set; }`: What the instruction is asking of the client
- `RapidExecutionLevel ExecutionLevel { get; set; }`: Level at which the instruction is executing
- `string Instruction { get; set; }`: Name of the RAPID instruction that opened the dialogue, for example "TPReadNum"
- `string Message { get; set; }`: Text the instruction displays
- `string StackUrl { get; set; }`: Path identifying the call, which the parameter methods take

## RapidUiInstructionEvent

`enum RapidUiInstructionEvent`

What a UI instruction is asking of the client

- Abort: The instruction has been abandoned and no answer is expected any more
- Post: The instruction only displays something and expects no answer
- Send: The instruction is waiting for an answer
- Unknown: The controller reported an event this library does not know

## RapidUiInstructionParameter

`class RapidUiInstructionParameter`

One parameter of the pending UI instruction: what the program passed in, or what it is waiting for. Returned by RapidService.GetUiInstructionParameters(). The parameters carrying the answer are the ones to write, typically named after a function key or after the completion flag of the instruction.

- `RapidUiInstructionParameter()`: Initializes a new instance of the Data.RapidUiInstructionParameter class
- `string Name { get; set; }`: Name of the parameter, for example "TPCompleted"
- `string Value { get; set; }`: Value of the parameter, written the way RAPID writes it

## SafetyConfiguration

`class SafetyConfiguration`

Safety supervision configuration of the controller. Returned by ControllerService.GetSafetyConfiguration().

- `SafetyConfiguration()`: Initializes a new instance of the Data.SafetyConfiguration class
- `string Checksum { get; set; }`: Checksum of the configuration, as base64 encoded data
- `string ConfigurationStatus { get; set; }`: Status of the configuration, for example "SCORCH_CONFIG_LOADED". Only available when connected with version 2.
- `string CreatedBy { get; set; }`: Author of the configuration
- `DateTime? CreationDate { get; set; }`: Creation date of the configuration, if available
- `int? FileMajorVersion { get; set; }`: Configuration file major version
- `int? FileMinorVersion { get; set; }`: Configuration file minor version
- `int? FileRevision { get; set; }`: Configuration file revision
- `string Name { get; set; }`: Name of the configuration
- `int? SoftwareMajorVersion { get; set; }`: Safety software major version
- `int? SoftwareMinorVersion { get; set; }`: Safety software minor version
- `int? SoftwareRevision { get; set; }`: Safety software revision

## SafetyLoadOperationStatus

`enum SafetyLoadOperationStatus`

Indicates whether a new safety configuration is allowed to be loaded

- CurrentConfigurationLocked: The current safety configuration is locked (SCORCH_ERR_CURRENT_CONFIG_LOCKED)
- NotInManualMode: The controller is not in manual mode (SCORCH_ERR_NOT_IN_MANUAL_MODE)
- NotInMotorsOff: The motors are not switched off (SCORCH_ERR_NOT_IN_MOTORS_OFF)
- Ok: Loading a new safety configuration is allowed
- OptionNotPresent: The safety option is not present on the controller (SCORCH_ERR_OPTION_NOT_PRESENT)
- Unknown: The status could not be determined
- UserGrantMissing: The user does not have the required grant (SCORCH_ERR_USER_GRANT_IS_MISSING)

## SafetyMode

`enum SafetyMode`

Safety mode of the safety controller

- Active: The safety configuration is active and supervised
- Commissioning: Commissioning mode, used while configuring the safety controller
- ModeError: The safety controller reports a mode error
- Service: Service mode
- Unknown: The safety mode could not be determined

## SafetyModeStatus

`class SafetyModeStatus`

Safety mode status of the controller. Returned by ControllerService.GetSafetyMode().

- `SafetyModeStatus()`: Initializes a new instance of the Data.SafetyModeStatus class
- `SafetyMode Mode { get; set; }`: Current safety mode
- `int? UserData { get; set; }`: User data associated with the safety mode, if reported by the controller

## SafetyViolationInfo

`class SafetyViolationInfo`

Safety violation details reported by the safety controller. Returned by ControllerService.GetSafetyViolationInfo().

- `SafetyViolationInfo()`: Initializes a new instance of the Data.SafetyViolationInfo class
- `int? AxisRangeActiveStatus { get; set; }`: Axis range supervision active status
- `int? AxisRangeViolationStatus { get; set; }`: Axis range violation status
- `int? DriveModuleIndex { get; set; }`: Index of the drive module involved in the violation
- `int? LastViolationInstanceId { get; set; }`: Instance id of the last violation
- `int? ToolId { get; set; }`: Id of the tool involved in the violation
- `int? ToolPositionActiveStatus { get; set; }`: Tool position supervision active status
- `int? ToolPositionViolationStatus { get; set; }`: Tool position violation status
- `int? ToolSpeedActiveStatus { get; set; }`: Tool speed supervision active status
- `int? ToolSpeedViolationStatus { get; set; }`: Tool speed violation status
- `int? Unsynchronized { get; set; }`: Indicates whether the robot is unsynchronized
- `int? UpperArmViolationStatus { get; set; }`: Upper arm violation status
- `int? ViolatingSsv { get; set; }`: Violating safety supervision value
- `int? ViolationNumber { get; set; }`: Number of violations
- `SafetyViolationType ViolationType { get; set; }`: Type of the current violation

## SafetyViolationType

`enum SafetyViolationType`

Type of safety violation reported by the safety controller

- EmergencyStop: Emergency stop triggered (empstop)
- Invalid: The safety controller reports an invalid violation
- None: No violation
- OperationalSafetyRange: Operational Safety Range (osr)
- Other: Internal error (other)
- ReducedAxisSpeed: Reduced Axis Speed in manual mode (red_axis_speed)
- ReducedToolSpeed: Reduced Tool Speed in manual mode (red_tool_speed)
- SafeAxisRange: Safe Axis Range (sar)
- SafeAxisSpeed: Safe Axis Speed (sas)
- SafeStandstill: Safe Standstill (sst)
- SafeToolSpeed: Safe Tool Speed (sts)
- SafeToolZone: Safe Tool Zone (stz)
- ToolOrientationMonitoring: Tool Orientation Monitoring (tom)
- Unknown: The violation type could not be determined
- UnsynchronizedSpeedLimit: Reduced Axis Speed due to unsynchronized robot (unsync_speed_lim)

## SmbData

`class SmbData`

Serial measurement board data of one mechanical unit, held twice: once in the controller cabinet and once in the memory of the robot itself. Returned by MotionSystemService.GetSmbData(). Comparing the cabinet properties with the robot ones tells whether the two copies still agree, which is what M...

- `SmbData()`: Initializes a new instance of the Data.SmbData class
- `SmbDataStatus CabinetAbsoluteAccuracyStatus { get; set; }`: State of the absolute accuracy data stored in the cabinet
- `SmbDataStatus CabinetAxisCalibrationStatus { get; set; }`: State of the axis calibration data stored in the cabinet
- `SmbDataStatus CabinetCalibrationStatus { get; set; }`: State of the calibration data stored in the cabinet
- `string CabinetSerialNumberHighPart { get; set; }`: High part of the serial number stored in the cabinet
- `string CabinetSerialNumberLowPart { get; set; }`: Low part of the serial number stored in the cabinet
- `bool? CabinetSerialNumberValid { get; set; }`: Whether the serial number stored in the cabinet is usable, null when the controller did not report it
- `SmbDataStatus CabinetServiceInformationStatus { get; set; }`: State of the service information data stored in the cabinet
- `int? DriveModule { get; set; }`: Number of the drive module the data belongs to, null when the controller did not report it
- `int? MeasurementBoard { get; set; }`: Number of the measurement board the data belongs to, null when the controller did not report it
- `int? MeasurementLink { get; set; }`: Number of the measurement link the data belongs to, null when the controller did not report it
- `SmbDataStatus RobotAbsoluteAccuracyStatus { get; set; }`: State of the absolute accuracy data stored in the robot
- `SmbDataStatus RobotAxisCalibrationStatus { get; set; }`: State of the axis calibration data stored in the robot
- `SmbDataStatus RobotCalibrationStatus { get; set; }`: State of the calibration data stored in the robot
- `string RobotSerialNumberHighPart { get; set; }`: High part of the serial number stored in the robot
- `string RobotSerialNumberLowPart { get; set; }`: Low part of the serial number stored in the robot
- `bool? RobotSerialNumberValid { get; set; }`: Whether the serial number stored in the robot is usable, null when the controller did not report it
- `SmbDataStatus RobotServiceInformationStatus { get; set; }`: State of the service information data stored in the robot

## SmbDataMemory

`enum SmbDataMemory`

Which of the two copies of the serial measurement board data is erased

- Controller: The copy held by the controller cabinet
- Robot: The copy held by the robot itself

## SmbDataStatus

`enum SmbDataStatus`

State of one block of serial measurement board data, on the controller side or on the robot side

- NotUsed: The robot system does not use this block of data
- NotValid: The data is missing or unusable
- Unknown: The controller reported a state this library does not know
- Valid: The data is present and the two copies agree
- ValidNotEqual: The data is present on both sides, but the two copies differ

## SmbDataTransfer

`enum SmbDataTransfer`

Which of the two copies of the serial measurement board data overwrites the other

- ControllerToRobot: The copy held by the controller cabinet is written into the robot
- RobotToController: The copy held by the robot is written into the controller cabinet

## SystemEnergy

`class SystemEnergy`

Energy the controller has consumed, for the current measurement interval and since the last reset. Returned by SystemService.GetEnergy().

- `SystemEnergy()`: Initializes a new instance of the Data.SystemEnergy class
- `double? AccumulatedEnergy { get; set; }`: Total energy consumed since the last reset, in joules, null when the controller did not report it
- `double? AveragePower { get; }`: Average power consumed during the current measurement interval, in watts. Null when the interval energy or the interval length is missing, or when the interval is empty.
- `int? ChangeCount { get; set; }`: Counter the controller increments every time a new measurement is available. Comparing it with the previous one tells whether the values changed without reading them all.
- `double? IntervalEnergy { get; set; }`: Total energy consumed during the current measurement interval, in joules, null when the controller did not report it
- `int? IntervalLength { get; set; }`: Length of the measurement interval in seconds, which the average power is computed from, null when the controller did not report it
- `bool IsMeasurementValid { get; set; }`: Whether the reported measurement is valid. When false, every energy value of this instance is meaningless and the measurement has to be read again later.
- `int MechanicalUnitCount { get; }`: Number of mechanical units the controller reported
- `SystemEnergyMechanicalUnit[] MechanicalUnits { get; set; }`: Energy consumed by each mechanical unit during the current measurement interval
- `DateTime? ResetTime { get; set; }`: Moment the accumulated energy was last reset, null when the controller did not report it
- `SystemEnergyState State { get; set; }`: State of the energy measurement
- `DateTime? TimeStamp { get; set; }`: Moment the measurement was taken, null when the controller did not report it

## SystemEnergyAxis

`class SystemEnergyAxis`

Energy consumed by one axis of a mechanical unit during the current measurement interval. Held by Data.SystemEnergyMechanicalUnit.

- `SystemEnergyAxis()`: Initializes a new instance of the Data.SystemEnergyAxis class
- `double? IntervalEnergy { get; set; }`: Energy the axis consumed during the current measurement interval, in joules, null when the controller did not report it
- `int Number { get; set; }`: Number of the axis inside its mechanical unit, starting at 1

## SystemEnergyMechanicalUnit

`class SystemEnergyMechanicalUnit`

Energy consumed by one mechanical unit, broken down per axis. Held by Data.SystemEnergy.

- `SystemEnergyMechanicalUnit()`: Initializes a new instance of the Data.SystemEnergyMechanicalUnit class
- `SystemEnergyAxis[] Axes { get; set; }`: Energy consumed by each axis of the mechanical unit during the current measurement interval
- `int AxisCount { get; }`: Number of axes the controller reported for this mechanical unit
- `string Name { get; set; }`: Name of the mechanical unit, for example "ROB_1"

## SystemEnergyState

`enum SystemEnergyState`

State of the energy measurement of the controller

- Blocked: Energy measurement is blocked and no new value is produced
- GoingToSleep: The controller is entering its low energy consumption mode
- NotPaused: Energy measurement is running
- Paused: Energy measurement is paused
- Pausing: Energy measurement is being paused
- Resuming: Energy measurement is being resumed
- Sleep: The controller is in its low energy consumption mode
- Unknown: The energy state could not be determined

## SystemInfo

`class SystemInfo`

Identity and software version of the system running on the controller. Returned by SystemService.GetInfo().

- `SystemInfo()`: Initializes a new instance of the Data.SystemInfo class
- `int? ApiCompatibilityRevision { get; set; }`: Revision of the programming interface the system is compatible with, null when the controller did not report it
- `int? Build { get; set; }`: Build number of the version, null when the controller did not report it
- `string BuildTag { get; set; }`: Free text describing the build the system was produced by, null when the controller did not report it
- `string ConfigurationTimestamp { get; set; }`: Timestamp of the configuration the system was built with, as the controller spells it. Null when the controller did not report it, which is the usual case on a virtual controller.
- `DateTime? Date { get; set; }`: Date the system was produced, null when the controller did not report it
- `string Description { get; set; }`: Description of the system, null when the controller did not report it
- `string DistributionVersion { get; set; }`: Version of the software distribution the system was installed from. Null when the controller does not report it.
- `int? Major { get; set; }`: Major number of the version, null when the controller did not report it
- `int? Minor { get; set; }`: Minor number of the version, null when the controller did not report it
- `string Name { get; set; }`: Name of the system installed on the controller
- `int OptionCount { get; }`: Number of options installed on the system
- `string[] Options { get; set; }`: Options installed on the system, in the order the controller reports them
- `int? Revision { get; set; }`: Revision number of the version, null when the controller did not report it
- `DateTime? StartTime { get; set; }`: Moment the system was last started, null when the controller did not report it
- `int? SubRevision { get; set; }`: Sub revision number of the version, null when the controller did not report it
- `string SystemId { get; set; }`: Unique identifier of the system
- `string Title { get; set; }`: Title of the system, null when the controller did not report it
- `string Type { get; set; }`: Type of the system, null when the controller did not report it
- `string Version { get; set; }`: Version of the robot software the system runs
- `string VersionName { get; set; }`: Human readable version of the robot software the system runs

## SystemProduct

`class SystemProduct`

One software product installed on the controller. Returned by SystemService.GetProducts().

- `SystemProduct()`: Initializes a new instance of the Data.SystemProduct class
- `string Name { get; set; }`: Name of the product, for example "RobotWare" or "RobotControl"
- `string Version { get; set; }`: Full version of the product, build information included. Null when the controller only reports the version name.
- `string VersionName { get; set; }`: Human readable version of the product

## TimeServerInfo

`class TimeServerInfo`

Time server used by the controller to synchronize its clock. Returned by ControllerService.GetTimeServer().

- `TimeServerInfo()`: Initializes a new instance of the Data.TimeServerInfo class
- `string Address { get; set; }`: Address of the time server
- `DateTime? Time { get; set; }`: Time reported by the time server (UTC), if available. Only available when connected with version 2.

## VirtualTimeState

`enum VirtualTimeState`

State of the virtual time server of a virtual controller

- FreeRun: Virtual time runs freely (VTFREERUN)
- NextEvent: Virtual time runs until the next event (VTNEXTEVENT)
- RunSlice: Virtual time runs one time slice at a time (VTRUNSLICE)
- Stop: Virtual time is stopped (VTSTOP)
- Unknown: The state could not be determined
