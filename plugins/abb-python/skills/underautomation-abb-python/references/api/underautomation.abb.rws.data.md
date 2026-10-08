# underautomation.abb.rws.data

## AxisInfo

`from underautomation.abb.rws.data.axis_info import AxisInfo`

State of one axis of a mechanical unit. Returned by MotionSystemService.GetAxis().

- `AxisInfo()`: Initializes a new instance of the AxisInfo class
- `number: int`: Number of the axis inside its mechanical unit, starting at 1
- `status: MechanicalUnitStatus`: Calibration and synchronization state of the axis
- `logical_axis: int | None`: Logical joint number of the axis, null when the controller did not report it

## BackupRestoreIgnore

`from underautomation.abb.rws.data.backup_restore_ignore import BackupRestoreIgnore`

Mismatches between a backup and the current system that are ignored when restoring

- None_: No mismatch is ignored
- All: All mismatches are ignored
- SystemId: A mismatch between the system id of the backup and the system id of the current system is ignored
- TemplateId: A mismatch between the template id of the backup and the template id of the current system is ignored

## BackupRestoreInclude

`from underautomation.abb.rws.data.backup_restore_include import BackupRestoreInclude`

Content included when restoring a backup

- All: Restore configuration files and RAPID modules
- Cfg: Restore configuration files only
- Modules: Restore RAPID modules only

## BackupState

`from underautomation.abb.rws.data.backup_state import BackupState`

State of the backup operation of the controller

- Unknown: The backup state could not be determined
- None_: No backup operation
- InitState: A backup operation has been initialized
- BackupInProgress: A backup operation is running
- BackupReady: The backup operation finished successfully
- ErrorDuringBackup: The backup operation failed
- Invalid: The backup state is invalid

## BackupSystemInfo

`from underautomation.abb.rws.data.backup_system_info import BackupSystemInfo`

Information about a backup stored on the controller file system. Returned by ControllerService.GetBackupInfo(backupPath).

- `BackupSystemInfo()`: Initializes a new instance of the BackupSystemInfo class
- `system_name: str`: Name of the backed up system
- `robot_ware_version: str`: RobotWare version of the backed up system. Only available when connected with version 1.
- `robot_control_version: str`: RobotControl version of the backed up system. Only available when connected with version 2.
- `robot_os_version: str`: RobotOS version of the backed up system. Only available when connected with version 2.
- `options: typing.List[str]`: Options installed on the backed up system
- `option_count: int (read only)`: Number of options installed on the backed up system

## BaseFrame

`from underautomation.abb.rws.data.base_frame import BaseFrame`

Where the base of a mechanical unit sits, and what kind of base it is: a Pose extended with the type of the frame. Returned by MotionSystemService.GetBaseFrame(). The position is expressed in millimetres.

- `BaseFrame()`: Initializes a new base frame at the origin, with no rotation
- `type: str`: Kind of base frame the controller reports, for example "IRBRobot"
- Inherited from [Pose](underautomation.abb.common.md#pose): `orientation`
- Inherited from [Position](underautomation.abb.common.md#position): `x`, `y`, `z`

## CalibrationInfo

`from underautomation.abb.rws.data.calibration_info import CalibrationInfo`

How a mechanical unit was calibrated, joint by joint. Returned by MotionSystemService.GetCalibrationInfo().

- `CalibrationInfo()`: Initializes a new instance of the CalibrationInfo class
- `calibration_window_type: int | None`: Kind of calibration window the controller offers for this unit, null when the controller did not report it
- `active_joint_count: int | None`: Number of joints of the unit that are in use, null when the controller did not report it
- `joint_count: int | None`: Number of entries in joints, which is fixed and larger than active_joint_count. Null when the controller did not report it.
- `calibration_method_used: str`: Name of the calibration method the unit was last calibrated with, for example "AxisCalibration"
- `joints: typing.List[CalibrationJointInfo]`: One entry per joint slot of the unit, the unused ones marked as such. Never null.
- `existing_joint_count: int (read only)`: Number of joints that exist on the unit, counted from joints

## CalibrationJointInfo

`from underautomation.abb.rws.data.calibration_joint_info import CalibrationJointInfo`

How one joint of a mechanical unit was calibrated. Held by .

- `CalibrationJointInfo()`: Initializes a new instance of the CalibrationJointInfo class
- `exists: bool`: Whether the joint exists on this mechanical unit. The controller always answers with a fixed number of entries and marks the unused ones, which carry no name at all.
- `joint_name: str`: Name of the joint, for example "rob1_1", empty for an entry that does not exist
- `factory_calibration_method: str`: Method the joint was calibrated with in the factory
- `current_calibration_method: str`: Method the joint is currently calibrated with

## CheckRestoreResult

`from underautomation.abb.rws.data.check_restore_result import CheckRestoreResult`

Result of a backup restore check. Returned by ControllerService.CheckRestore(...).

- `CheckRestoreResult()`: Initializes a new instance of the CheckRestoreResult class
- `status: CheckRestoreStatus`: Status of the check
- `is_accepted: bool (read only)`: Indicates whether the backup can be restored
- `path: str`: File missing or corrupted in the backup, if reported by the controller

## CheckRestoreStatus

`from underautomation.abb.rws.data.check_restore_status import CheckRestoreStatus`

Result status of a backup restore check

- Unknown: The status could not be determined
- Accepted: The backup is accepted and can be restored
- RestoreMismatchSystemId: The backup was not created from the current system, there might be differences in active options and selected languages
- RestoreMismatchTemplateId: The current system and the backed up system may be generated from different key ids, possibly with different robot types
- DirectoryNotComplete: The backup directory is not complete
- ConfigurationDataIncorrect: Error in the configuration data of the backup

## CollisionDetectionState

`from underautomation.abb.rws.data.collision_detection_state import CollisionDetectionState`

State of the collision detection of the robot controller

- Unknown: The collision detection state could not be determined
- Init: No collision has been detected since the controller started
- Triggered: A collision has been detected and is waiting to be confirmed
- Confirmed: A detected collision has been confirmed
- TriggeredAcknowledged: A detected collision has been acknowledged by an operator

## ControllerIdentity

`from underautomation.abb.rws.data.controller_identity import ControllerIdentity`

Identity of the robot controller. Returned by ControllerService.GetIdentity().

- `ControllerIdentity()`: Initializes a new instance of the ControllerIdentity class
- `name: str`: Name of the controller
- `id: str`: Controller id, available only for a real controller
- `type: ControllerType`: Indicates whether the controller is a real or a virtual controller
- `mac_address: str`: MAC address of the controller, available only for a real controller
- `level: ControllerLevel`: Indicates whether the controller runs at system level or in bootserver mode

## ControllerInfo

`from underautomation.abb.rws.data.controller_info import ControllerInfo`

Overview of the controller resources. Returned by ControllerService.GetInfo().

- `ControllerInfo()`: Initializes a new instance of the ControllerInfo class
- `system_time: datetime | None`: Current system time of the controller (UTC), if available
- `name: str`: Name of the controller
- `type: ControllerType`: Indicates whether the controller is a real or a virtual controller
- `level: ControllerLevel`: Indicates whether the controller runs at system level or in bootserver mode
- `resources: typing.List[str]`: Names of the sub resources exposed by the controller ("clock", "identity", "network", ...)

## ControllerLevel

`from underautomation.abb.rws.data.controller_level import ControllerLevel`

Level the controller is currently running at

- Unknown: The controller level could not be determined
- SystemLevel: A system is loaded and running (system level)
- BootLevel: The controller runs the boot application (bootserver mode)

## ControllerRestartMode

`from underautomation.abb.rws.data.controller_restart_mode import ControllerRestartMode`

Restart mode of the robot controller

- Restart: The controller will be restarted. The state is saved and any changed system parameter settings will be activated after the restart.
- Shutdown: The main computer will be shut down. Should be used if the controller UPS is broken.
- XStart: The controller will be restarted and the Boot Application will be started. The current system is saved and deactivated (the controller is non-functional, for advanced maintenance only).
- IStart: The controller will be restarted. The current system parameter settings and RAPID programs will be discarded, and the original system installation settings will be used.
- PStart: The controller will be restarted. The current RAPID programs and data will be discarded, but not the system parameter settings.
- BStart: The controller will be restarted. The last automatically saved system state will be loaded. Should be used to recover from a system crash.

## ControllerState

`from underautomation.abb.rws.data.controller_state import ControllerState`

State of the robot controller, as reported by the control panel

- Unknown: The state could not be determined
- Init: The robot is starting up. It will shift to MotorsOff once it has started.
- MotorsOff: The robot is in a standby state where there is no power to its motors. The state has to be shifted to MotorsOn before the robot can move.
- MotorsOn: The robot is ready to move, either by jogging or by running programs
- GuardStop: The robot is stopped because the safety runchain is opened, for instance because a door of its cell is open
- EmergencyStop: The robot is stopped because the emergency stop was activated
- EmergencyStopReset: The robot is ready to leave the emergency stop state: the emergency stop is no longer activated, but the state transition is not confirmed yet.
- SystemFailure: The robot is in a system failure state and requires a restart

## ControllerType

`from underautomation.abb.rws.data.controller_type import ControllerType`

Type of the robot controller (real or virtual)

- Unknown: The controller type could not be determined
- RealController: Physical robot controller (RC)
- VirtualController: Virtual controller (VC), for example running in RobotStudio

## CoordinateSystem

`from underautomation.abb.rws.data.coordinate_system import CoordinateSystem`

Reference frame a cartesian position is expressed in

- Unknown: The controller reported a frame this library does not know
- World: The world frame, shared by every mechanical unit of the system
- Base: The base frame of the mechanical unit
- Tool: The frame of the active tool
- WorkObject: The frame of the active work object

## CyclicBrakeCheckState

`from underautomation.abb.rws.data.cyclic_brake_check_state import CyclicBrakeCheckState`

Cyclic brake check state of a mechanical unit

- Unknown: The state could not be determined
- Ok: No brake check is needed (CBC_STATUS_OK)
- PreWarning: A brake check will soon be required (CBC_STATUS_PREWARNING)
- Required: A brake check is required (CBC_STATUS_REQUIRE_CBC)

## CyclicBrakeCheckStatus

`from underautomation.abb.rws.data.cyclic_brake_check_status import CyclicBrakeCheckStatus`

Cyclic brake check status of a mechanical unit. Returned by ControllerService.GetCyclicBrakeCheckStatus(driveNumber).

- `CyclicBrakeCheckStatus()`: Initializes a new instance of the CyclicBrakeCheckStatus class
- `drive_number: int`: Drive number of the mechanical unit this status belongs to
- `next_brake_check_time: int | None`: Remaining time before the next brake check is required, if reported by the controller
- `last_brake_check_status: CyclicBrakeCheckTestStatus`: Result of the last brake check
- `status: CyclicBrakeCheckState`: Current cyclic brake check state

## CyclicBrakeCheckTestStatus

`from underautomation.abb.rws.data.cyclic_brake_check_test_status import CyclicBrakeCheckTestStatus`

Result of the last cyclic brake check test

- Unknown: The test status could not be determined
- Ok: The last brake check succeeded (CBC_TEST_OK)
- Warning: The last brake check ended with a warning (CBC_TEST_WARNING)
- Error: The last brake check failed (CBC_TEST_ERROR)
- Undefined: No brake check has been performed yet (CBC_TEST_UNDEFINED)

## DeviceItem

`from underautomation.abb.rws.data.device_item import DeviceItem`

Represents a device entry in the robot controller file system (e.g. C:, hd0a). Devices are returned alongside files and directories when listing the root path ("/") or any directory that contains mounted devices.

- `DeviceItem()`: Initializes a new instance of the DeviceItem class
- `device_type: DeviceType`: Type of device (Fixed, Removable, RamDisk, Remote)
- `total_space: int`: Total storage space in bytes
- `free_space: int`: Free storage space in bytes
- `is_enabled: bool`: Indicates if the device is enabled
- `is_read_only: bool`: Indicates if the device is read-only
- Inherited from [FileSystemItem](underautomation.abb.rws.data.md#filesystemitem): `name`, `creation_date`, `modification_date`

## DeviceType

`from underautomation.abb.rws.data.device_type import DeviceType`

Represents the type of storage device

- Fixed: Fixed storage device (hard drive)
- Removable: Removable storage device (USB, SD card, etc.)
- RamDisk: RAM disk
- Remote: Remote or network storage
- Unknown: Unknown device type

## DirectoryItem

`from underautomation.abb.rws.data.directory_item import DirectoryItem`

Represents a directory entry in the robot controller file system.

- `DirectoryItem()`: Initializes a new instance of the DirectoryItem class
- `is_read_only: bool`: Indicates if the directory is read-only
- Inherited from [FileSystemItem](underautomation.abb.rws.data.md#filesystemitem): `name`, `creation_date`, `modification_date`

## DirectoryListing

`from underautomation.abb.rws.data.directory_listing import DirectoryListing`

Represents a directory listing containing files, subdirectories, and devices. Returned by FileService.ListDirectory(path).When listing the root path ("/"), the array contains available storage devices (C:, hd0a, etc.).When listing a subdirectory, only and are typically populated.

- `DirectoryListing(path: str)`: Initializes a new instance of the DirectoryListing class
- `files: typing.List[FileItem]`: Files contained in this directory
- `directories: typing.List[DirectoryItem]`: Subdirectories contained in this directory
- `devices: typing.List[DeviceItem]`: Devices available in this listing (typically only present at root "/")
- `path: str (read only)`: Path that was listed
- `file_count: int (read only)`: Number of files in this listing
- `directory_count: int (read only)`: Number of subdirectories in this listing
- `device_count: int (read only)`: Number of devices in this listing
- `total_count: int (read only)`: Total number of items (files + directories + devices)

## ElogDomain

`from underautomation.abb.rws.data.elog_domain import ElogDomain`

One event log domain of the controller, for example the common, the operational or the safety log. Returned by ElogService.GetDomains() and ElogService.GetDomain().

- `ElogDomain()`: Initializes a new instance of the ElogDomain class
- `number: int`: Number identifying the domain, which is the value to pass to the methods reading its messages
- `name: str`: Name of the domain, for example "Operational" or "Safety". Only filled when a language was asked for, null otherwise.
- `message_count: int | None`: Number of messages currently held by the domain, null when the controller did not report it
- `buffer_size: int | None`: Number of messages the domain can hold before the oldest ones are discarded, null when the controller did not report it

## ElogMessage

`from underautomation.abb.rws.data.elog_message import ElogMessage`

One message of the controller event log. Returned by ElogService.GetMessages(), ElogService.GetMessageTitles(), ElogService.GetMessage() and ElogService.GetMessageBySequenceNumber().The texts (, , , and ) are only filled when a language was asked for.

- `ElogMessage()`: Initializes a new instance of the ElogMessage class
- `domain_number: int | None`: Number of the domain the message belongs to, null when the controller did not report it
- `sequence_number: int | None`: Number identifying the message inside its domain. Messages are numbered in the order they were logged, so a higher number is a more recent message.
- `type: ElogMessageType`: Severity of the message
- `code: int | None`: Number identifying the kind of event, the one printed on the teach pendant
- `source_name: str`: Part of the controller that logged the message, for example "MC0"
- `timestamp: datetime | None`: Moment the event was logged, null when the controller did not report it
- `title: str`: Short text of the message. Only filled when a language was asked for.
- `description: str`: Long text describing what happened. Only filled when a language was asked for.
- `consequences: str`: Text describing what the event implies for the robot. Only filled when a language was asked for.
- `causes: str`: Text describing the probable causes of the event. Only filled when a language was asked for.
- `actions: str`: Text describing the recommended actions. Only filled when a language was asked for.
- `arguments: typing.List[ElogMessageArgument]`: Values the controller substitutes into the text of the message
- `argument_count: int (read only)`: Number of arguments of the message

## ElogMessageArgument

`from underautomation.abb.rws.data.elog_message_argument import ElogMessageArgument`

One argument of an event log message. The arguments are the values the controller substitutes into the text of the message, for example the name of the task that was started. Held by .

- `ElogMessageArgument()`: Initializes a new instance of the ElogMessageArgument class
- `index: int`: Position of the argument in the message, starting at 1
- `type: str`: Type of the argument reported by the controller, for example "string", "long" or "float"
- `value: str`: Value of the argument, always as text

## ElogMessageOrder

`from underautomation.abb.rws.data.elog_message_order import ElogMessageOrder`

Order in which the event log messages of a domain are returned

- NewestFirst: Most recent message first
- OldestFirst: Oldest message first

## ElogMessageType

`from underautomation.abb.rws.data.elog_message_type import ElogMessageType`

Severity of an event log message

- Unknown: The message type could not be determined
- Information: State change, or informational event
- Warning: Warning event
- Error: Error event

## FileItem

`from underautomation.abb.rws.data.file_item import FileItem`

Represents a file entry in the robot controller file system.

- `FileItem()`: Initializes a new instance of the FileItem class
- `size: int`: File size in bytes
- `is_read_only: bool`: Indicates if the file is read-only
- Inherited from [FileSystemItem](underautomation.abb.rws.data.md#filesystemitem): `name`, `creation_date`, `modification_date`

## FileSystemItem

`from underautomation.abb.rws.data.file_system_item import FileSystemItem`

Abstract base class for all file system items returned by the File Service. Derived classes: , ,

- `name: str`: Name of the item (file name, directory name, or device name such as "C:")
- `creation_date: datetime | None`: Creation date of the resource, if available
- `modification_date: datetime | None`: Last modification date of the resource, if available

## IoClientAction

`from underautomation.abb.rws.data.io_client_action import IoClientAction`

Action the client is expected to take after an I/O network auto configuration, returned by IoService.SetNetworkConfigurationType(). Only available when connected with version 2.

- Unknown: The controller did not report any client action. Always returned when connected with version 1, which does not report this information.
- None_: Nothing to do
- Info: The user should be informed of the configuration result
- Restart: The controller has to be restarted for the configuration to take effect

## IoDeviceConfiguration

`from underautomation.abb.rws.data.io_device_configuration import IoDeviceConfiguration`

Runtime configuration properties of an I/O device. Returned by IoService.GetDeviceConfiguration().

- `IoDeviceConfiguration()`: Initializes a new instance of the IoDeviceConfiguration class
- `device_name: str`: Name of the device, for example "DN_Internal_Device"
- `network_name: str`: Name of the industrial network the device belongs to, for example "DeviceNet"
- `input_bits: int | None`: Number of input bits of the device, null when not reported
- `output_bits: int | None`: Number of output bits of the device, null when not reported
- `rapid: bool | None`: Whether a RAPID client can access the device in both manual and auto mode
- `local_manual: bool | None`: Whether a local client can access the device in manual mode
- `local_auto: bool | None`: Whether a local client can access the device in auto mode
- `remote_manual: bool | None`: Whether a remote client can access the device in manual mode
- `remote_auto: bool | None`: Whether a remote client can access the device in auto mode
- `device_address: str`: Address of the device on its network, "-" when the network has no addressing
- `deny_deactivate: bool | None`: Whether deactivating the device is denied

## IoDeviceItem

`from underautomation.abb.rws.data.io_device_item import IoDeviceItem`

I/O device (unit) connected to an I/O network of the robot controller. Returned by IoService.GetDevices(), IoService.GetDevice() and IoService.SearchDevices().

- `IoDeviceItem()`: Initializes a new instance of the IoDeviceItem class
- `name: str`: Name of the device, for example "DRV_1" or "PANEL"
- `network_name: str`: Name of the network the device is connected to, for example "Local"
- `path: str`: Full path of the device, "{network}/{device}" (for example "Local/DRV_1")
- `type: str`: Type of the device, for example "DRV_1_TYPE". Not reported by every controller, null when absent. A virtual controller leaves it out.
- `physical_state: IoDevicePhysicalState`: Physical state of the device
- `logical_state: IoDeviceLogicalState`: Logical state of the device
- `address: str`: Address of the device on its network, "-" when the network has no addressing
- `input_data: str`: Input data of the device, as an hexadecimal string (for example "1FFFE063"). Only reported when reading a single device with IoService.GetDevice().
- `input_mask: str`: Input mask of the device, as an hexadecimal string. A bit set to zero is an input bit that is not written. Only reported when reading a single device with IoService.GetDevice().
- `output_data: str`: Output data of the device, as an hexadecimal string (for example "0000000E"). Only reported when reading a single device with IoService.GetDevice().
- `output_mask: str`: Output mask of the device, as an hexadecimal string. A bit set to zero is an output bit that is not written. Only reported when reading a single device with IoService.GetDevice().

## IoDeviceLogicalState

`from underautomation.abb.rws.data.io_device_logical_state import IoDeviceLogicalState`

Logical state of an I/O device

- Unknown: The logical state could not be determined
- Enabled: The device is enabled
- Disabled: The device is disabled

## IoDevicePhysicalState

`from underautomation.abb.rws.data.io_device_physical_state import IoDevicePhysicalState`

Physical state of an I/O device

- Unknown: The physical state could not be determined
- Deactivated: The device is deactivated
- Running: The device is running
- Error: The device reports an error
- Unconnected: The device is not connected
- Unconfigured: The device is not configured
- Startup: The device is starting up
- Init: The device is initializing
- Halted: The device is halted

## IoDeviceUpgradeInfo

`from underautomation.abb.rws.data.io_device_upgrade_info import IoDeviceUpgradeInfo`

Firmware upgrade status of an I/O device and of each of its modules. Returned by IoService.GetDeviceUpgradeInfo().Only applicable to a real controller.

- `IoDeviceUpgradeInfo()`: Initializes a new instance of the IoDeviceUpgradeInfo class
- `state: IoFirmwareUpgradeState`: Overall progress of the firmware upgrade of the device
- `status: IoFirmwareUpgradeStatus`: Overall result of the firmware upgrade of the device
- `modules: typing.List[IoFirmwareModuleInfo]`: Firmware status of each module of the device, empty when the controller reported none
- `module_count: int (read only)`: Number of modules reported by the controller

## IoFirmwareModuleInfo

`from underautomation.abb.rws.data.io_firmware_module_info import IoFirmwareModuleInfo`

Firmware upgrade status of one module of an I/O device. Returned by IoService.GetDeviceUpgradeInfo().

- `IoFirmwareModuleInfo()`: Initializes a new instance of the IoFirmwareModuleInfo class
- `index: str`: Index of the module inside the device ("0", "1", ...)
- `state: IoFirmwareUpgradeState`: Progress of the firmware upgrade of this module
- `status: IoFirmwareUpgradeStatus`: Result of the firmware upgrade of this module
- `program_name: str`: Name of the program installed on the module, for example "A_HYPIOM_B_3_8"
- `serial_number: str`: Serial number of the module
- `hardware_revision: str`: Hardware revision of the module, for example "C.1"
- `latest_program_name_available: str`: Name of the latest program available for the module

## IoFirmwareUpgradeState

`from underautomation.abb.rws.data.io_firmware_upgrade_state import IoFirmwareUpgradeState`

Progress of a firmware upgrade of an I/O device

- Unknown: The state is unknown, or could not be parsed
- Automatic: The upgrade is performed automatically
- Manual: The upgrade has to be started manually
- Info: The firmware information is being collected
- Allocate: The upgrade resources are being allocated
- Start: The upgrade is starting
- Running: The upgrade is running
- RunningStartReceived: The device acknowledged the start of the upgrade
- RunningCheckInProgress: The firmware is being checked
- RunningEraseInProgress: The device memory is being erased
- RunningBurnInProgress: The firmware is being written to the device
- RunningEndReceived: The device acknowledged the end of the upgrade
- Check: The upgraded firmware is being verified
- Deallocate: The upgrade resources are being released
- Finished: The upgrade is finished

## IoFirmwareUpgradeStatus

`from underautomation.abb.rws.data.io_firmware_upgrade_status import IoFirmwareUpgradeStatus`

Result of a firmware upgrade of an I/O device

- Unknown: The controller did not report a status, or it could not be parsed
- Error: The upgrade failed
- Ok: The upgrade finished, the firmware was already up to date
- Upgraded: The upgrade finished, the firmware was updated
- Pending: The upgrade is pending

## IoNetworkConfiguration

`from underautomation.abb.rws.data.io_network_configuration import IoNetworkConfiguration`

Runtime configuration properties of an I/O network. Returned by IoService.GetNetworkConfiguration().

- `IoNetworkConfiguration()`: Initializes a new instance of the IoNetworkConfiguration class
- `network_name: str`: Name of the network, for example "Local"
- `network_type: str`: Type of the network, for example "Local" or "LOC"
- `network_address: str`: Industrial network address, "-" when the network has no addressing

## IoNetworkConfigurationType

`from underautomation.abb.rws.data.io_network_configuration_type import IoNetworkConfigurationType`

Configuration type applied to an I/O network by IoService.SetNetworkConfigurationType()

- Bits: Configure the signals of the network
- Groups: Configure the signal groups of the network
- Both: Configure both the signals and the signal groups
- Scan: Scan the network for connected devices
- Units: Configure the devices of the network

## IoNetworkItem

`from underautomation.abb.rws.data.io_network_item import IoNetworkItem`

I/O network defined in the robot controller. Returned by IoService.GetNetworks(), IoService.GetNetwork() and IoService.SearchNetworks().

- `IoNetworkItem()`: Initializes a new instance of the IoNetworkItem class
- `name: str`: Name of the network, for example "Local", "Virtual" or "EtherNetIP"
- `path: str`: Full path of the network, which is its name for a network (for example "Local")
- `physical_state: IoNetworkPhysicalState`: Physical state of the network
- `logical_state: IoNetworkLogicalState`: Logical state of the network

## IoNetworkLogicalState

`from underautomation.abb.rws.data.io_network_logical_state import IoNetworkLogicalState`

Logical state of an I/O network

- Unknown: The logical state could not be determined
- Started: The network is started
- Stopped: The network is stopped

## IoNetworkPhysicalState

`from underautomation.abb.rws.data.io_network_physical_state import IoNetworkPhysicalState`

Physical state of an I/O network

- Unknown: The physical state could not be determined
- Halted: The network is halted
- Running: The network is running
- Error: The network reports an error
- Startup: The network is starting up
- Init: The network is initializing

## IoSignalConfiguration

`from underautomation.abb.rws.data.io_signal_configuration import IoSignalConfiguration`

Runtime configuration properties of an I/O signal. Returned by IoService.GetSignalConfiguration().

- `IoSignalConfiguration()`: Initializes a new instance of the IoSignalConfiguration class
- `signal_name: str`: Name of the signal, for example "DRV1CHAIN2"
- `signal_bits: int | None`: Number of bits of the signal, null when not reported
- `rapid: bool | None`: Whether a RAPID client can write the signal in both manual and auto mode
- `local_manual: bool | None`: Whether a local client can write the signal in manual mode
- `local_auto: bool | None`: Whether a local client can write the signal in auto mode
- `remote_manual: bool | None`: Whether a remote client can write the signal in manual mode
- `remote_auto: bool | None`: Whether a remote client can write the signal in auto mode
- `set_by_device_transfer: bool | None`: Whether the bits of this signal are set by a device transfer operation. Not reported by every controller, null when absent from the response.

## IoSignalItem

`from underautomation.abb.rws.data.io_signal_item import IoSignalItem`

I/O signal defined in the robot controller. Returned by IoService.GetSignals(), IoService.GetSignal(), IoService.SearchSignals() and IoService.SearchSignalsExtended().Depending on the method used, only a subset of the properties is filled in: the signal lists carry the name, type, category, logic...

- `IoSignalItem()`: Initializes a new instance of the IoSignalItem class
- `name: str`: Name of the signal, for example "DRV1BRAKE"
- `network_name: str`: Name of the network the signal belongs to, for example "Local"
- `device_name: str`: Name of the device the signal is connected to, for example "DRV_1"
- `path: str`: Full path of the signal, "{network}/{device}/{signal}" (for example "Local/DRV_1/DRV1BRAKE")
- `type: IoSignalType`: Type of the signal
- `category: str`: Category the signal belongs to, for example "safety"
- `logical_value: float | None`: Logical value of the signal, null when the controller did not report it
- `logical_state: IoSignalLogicalState`: Logical state of the signal (simulated or not)
- `physical_state: IoSignalPhysicalState`: Physical state of the signal. Only reported when reading a single signal with IoService.GetSignal().
- `physical_value: float | None`: Physical value of the signal, null when the controller did not report it. Only reported by IoService.GetSignal() and IoService.SearchSignalsExtended().
- `logical_time_seconds: int | None`: Seconds part of the global time at which the logical value was updated, null when not reported
- `logical_time_microseconds: int | None`: Microseconds part of the global time at which the logical value was updated, null when not reported
- `physical_time_seconds: int | None`: Seconds part of the global time at which the physical value was updated, null when not reported
- `physical_time_microseconds: int | None`: Microseconds part of the global time at which the physical value was updated, null when not reported
- `quality: str`: Quality of the signal, reported as a numeric code by IoService.GetSignal() and as a textual value (for example "good") by IoService.SearchSignalsExtended()
- `write_access_level: str`: Access level required to write the signal, for example "None". Only reported by IoService.SearchSignalsExtended().

## IoSignalLogicalState

`from underautomation.abb.rws.data.io_signal_logical_state import IoSignalLogicalState`

Logical state of an I/O signal

- Unknown: The logical state could not be determined
- Simulated: The signal is simulated: its logical value is forced and no longer follows the physical value
- NotSimulated: The signal is not simulated

## IoSignalPhysicalState

`from underautomation.abb.rws.data.io_signal_physical_state import IoSignalPhysicalState`

Physical state of an I/O signal

- Unknown: The physical state could not be determined
- Valid: The physical value of the signal is valid
- Invalid: The physical value of the signal is not valid

## IoSignalSearchCriteria

`from underautomation.abb.rws.data.io_signal_search_criteria import IoSignalSearchCriteria`

Criteria used to search I/O signals with IoService.SearchSignals() and IoService.SearchSignalsExtended(). Every property is optional: the properties left to null are not sent to the controller, and an empty criteria matches every signal.Two criteria can be combined by passing a second instance to...

- `IoSignalSearchCriteria()`: Initializes a new instance of the IoSignalSearchCriteria class
- `name: str`: Name of the searched signals
- `device_name: str`: Name of the device the searched signals are connected to
- `network_name: str`: Name of the network the searched signals belong to
- `category: str`: Category of the searched signals, for example "safety"
- `category_prefix: str`: Category prefix of the searched signals
- `type: IoSignalType | None`: Type of the searched signals, null to search every type
- `invert: bool | None`: Whether the criteria is inverted: the signals matching it are excluded from the result
- `blocked: bool | None`: Whether only the blocked (simulated) signals are searched

## IoSignalType

`from underautomation.abb.rws.data.io_signal_type import IoSignalType`

Type of an I/O signal

- Unknown: The signal type could not be determined
- DigitalOutput: Digital output
- DigitalInput: Digital input
- AnalogOutput: Analog output
- AnalogInput: Analog input
- GroupInput: Group input
- GroupOutput: Group output

## JogIncrementMode

`from underautomation.abb.rws.data.jog_increment_mode import JogIncrementMode`

Size of the step a jogging command moves the robot by

- None_: The robot moves for as long as the command is repeated, with no fixed step
- User: One step of the size configured in the system parameters
- Small: One small step
- Medium: One medium step
- Large: One large step

## JogMode

`from underautomation.abb.rws.data.jog_mode import JogMode`

How the jogging commands sent to a mechanical unit are interpreted

- Unknown: The controller reported a mode this library does not know
- AxisGroup1: Each command moves one axis of the first axis group
- AxisGroup2: Each command moves one axis of the second axis group
- Cartesian: The tool is moved along the axes of the active coordinate system
- Align: The tool is aligned with the closest axis of the active coordinate system
- GoToPosition: The robot moves to a given position
- ConfigurationJog: The robot changes axis configuration without moving the tool center point

## JointSolution

`from underautomation.abb.rws.data.joint_solution import JointSolution`

One of the joint combinations that reach a given pose: a JointTarget extended with the axis configuration it corresponds to. Returned by MotionSystemService.GetAllJointSolutions(). The joint values are expressed in radians.

- `JointSolution()`: Initializes a new solution with every axis at zero
- `configuration: RobotConfiguration`: Axis configuration this solution corresponds to. Never null.
- Inherited from [JointTarget](underautomation.abb.common.md#jointtarget): `robot_axes`, `external_axes`

## LeadThroughStatus

`from underautomation.abb.rws.data.lead_through_status import LeadThroughStatus`

Whether an operator can push the robot arm around by hand

- Unknown: The controller reported a state this library does not know
- Active: The arm gives way when pushed
- Inactive: The arm holds its position

## MastershipDomain

`from underautomation.abb.rws.data.mastership_domain import MastershipDomain`

Domain of the controller a client can take the mastership of. Mastership is what a client has to hold before it is allowed to change anything in a domain. Only one client at a time holds it, and it stays held until the client releases it or its connection ends.The two connection versions do not c...

- Edit: Everything that changes the system itself: its configuration and its RAPID programs. On a connection established with version 1, where the two are separate domains, asking for this one takes and together.
- Motion: The movement of the robot: jogging, the mechanical units and everything that makes an axis move
- Configuration: The system parameters of the controller. On a connection established with version 2, where it is not a domain of its own, this is the same domain as .
- Rapid: The RAPID programs and their data. On a connection established with version 2, where it is not a domain of its own, this is the same domain as .

## MastershipHolder

`from underautomation.abb.rws.data.mastership_holder import MastershipHolder`

Who holds the mastership of a domain

- Unknown: The controller reported a holder this library does not know
- None_: Nobody holds the mastership, it is free to be taken
- Remote: A client connected over the network holds it, possibly this one
- Local: A device attached to the controller holds it, the teach pendant for instance
- Internal: The controller itself holds it, while it runs an operation that must not be interrupted

## MastershipInfo

`from underautomation.abb.rws.data.mastership_info import MastershipInfo`

State of the mastership of one domain: who holds it, and whether this connection is the holder. Returned by MastershipService.GetInfo().

- `MastershipInfo()`: Initializes a new instance of the MastershipInfo class
- `domain: MastershipDomain`: Domain this state describes
- `holder: MastershipHolder`: Who holds the mastership of the domain
- `held_by_me: bool`: Whether this connection is the one holding the mastership, and is therefore allowed to write in the domain
- `user_id: int | None`: Identifier the controller gave the user holding the mastership, null when nobody holds it
- `location: str`: Where the holder is, as it declared itself, null when nobody holds the mastership
- `alias: str`: Alternate name of the location of the holder, null when nobody holds the mastership
- `application: str`: Name of the application holding the mastership, null when nobody holds it

## MechanicalUnitInfo

`from underautomation.abb.rws.data.mechanical_unit_info import MechanicalUnitInfo`

Everything the controller knows about one mechanical unit. Returned by MotionSystemService.GetMechanicalUnit().

- `MechanicalUnitInfo()`: Initializes a new instance of the MechanicalUnitInfo class
- `name: str`: Name of the mechanical unit, for example "ROB_1"
- `tool_name: str`: Name of the active tool
- `work_object_name: str`: Name of the active work object
- `payload_name: str`: Name of the active payload
- `total_payload_name: str`: Name of the active total payload, which is the payload plus the load of the tool
- `status: MechanicalUnitStatus`: Calibration and synchronization state of the unit
- `mode: MechanicalUnitMode`: Whether the unit is activated
- `jog_mode: JogMode`: How the jogging commands sent to the unit are interpreted
- `type: MechanicalUnitType`: Kind of mechanical unit
- `task_name: str`: Name of the RAPID task that drives the unit
- `coordinate_system: CoordinateSystem`: Reference frame the cartesian positions of the unit are expressed in
- `axes: int | None`: Number of axes of the unit, null when the controller did not report it
- `total_axes: int | None`: Number of axes of the unit and of the units integrated with it, null when the controller did not report it
- `is_integrated_unit: str`: Name of the mechanical unit this one is integrated into. A unit that is integrated into no other one is reported with a placeholder name rather than an empty value.
- `has_integrated_unit: str`: Name of the mechanical unit integrated into this one. A unit that integrates no other one is reported with a placeholder name rather than an empty value.

## MechanicalUnitItem

`from underautomation.abb.rws.data.mechanical_unit_item import MechanicalUnitItem`

One mechanical unit of the motion system, as listed by MotionSystemService.GetMechanicalUnits(). Only the few properties the list carries are filled in. Read the unit itself with MotionSystemService.GetMechanicalUnit() to get a .

- `MechanicalUnitItem()`: Initializes a new instance of the MechanicalUnitItem class
- `name: str`: Name of the mechanical unit, for example "ROB_1"
- `mode: MechanicalUnitMode`: Whether the unit is activated
- `activation_allowed: bool | None`: Whether the unit can be activated, null when the controller did not report it
- `drive_module: int | None`: Number of the drive module the unit is connected to, null when the controller did not report it

## MechanicalUnitMode

`from underautomation.abb.rws.data.mechanical_unit_mode import MechanicalUnitMode`

Whether a mechanical unit is activated and can be moved

- Unknown: The controller reported a mode this library does not know
- Activated: The mechanical unit is activated and takes part in the motion
- Deactivated: The mechanical unit is deactivated and stays where it is

## MechanicalUnitStatus

`from underautomation.abb.rws.data.mechanical_unit_status import MechanicalUnitStatus`

Calibration and synchronization state of a mechanical unit or of one of its axes

- Unknown: The controller reported a state this library does not know
- Initiated: The unit is starting up
- NotCommutated: One or several motors have not been commutated
- NotCalibrated: The unit has never been calibrated
- NotAbsoluteSynchronized: One or several absolute measurement axes are not synchronized
- NotRelativeSynchronized: One or several relative measurement axes are not synchronized
- Synchronized: The unit is calibrated and synchronized, and can be moved
- Locked: The unit is locked and refuses to move
- LockedShow: The unit is locked, and the controller shows it as such
- Undefined: The controller knows the unit but does not report its state

## MechanicalUnitType

`from underautomation.abb.rws.data.mechanical_unit_type import MechanicalUnitType`

Kind of mechanical unit the controller drives

- Unknown: The controller reported a type this library does not know
- None_: No mechanical unit
- TcpRobot: A robot arm holding a tool center point, which can be moved in cartesian coordinates
- Robot: A robot arm without a tool center point, which can only be moved axis by axis
- Single: A single external axis, such as a track or a positioner
- Undefined: The controller knows the unit but does not report what it is

## MotionErrorState

`from underautomation.abb.rws.data.motion_error_state import MotionErrorState`

Last error the motion system ran into, most of them raised by a jogging request it could not honour

- Unknown: The controller reported an error this library does not know
- Ok: No error
- MechanicalUnitNotActive: A mechanical unit was jogged whose activation failed
- UncalibratedJogMotionType: An uncalibrated robot was jogged in a mode that needs its calibration
- UnnormalizedQuaternion: A quaternion that is not normalized reached the jogging task, from a tool, a load or a work object
- ErroneousToolMass: A load definition carries a negative mass
- RobotHoldMismatch: The tool and the work object disagree on which one the robot holds
- WorkObjectMechanicalUnitNotFound: A mechanical unit used in coordinated jogging was not found
- InvalidJogMotionType: The requested jogging mode is not valid

## MotionSupervision

`from underautomation.abb.rws.data.motion_supervision import MotionSupervision`

Collision detection settings of one mechanical unit while it is jogged. Returned by MotionSystemService.GetMotionSupervision().

- `MotionSupervision()`: Initializes a new instance of the MotionSupervision class
- `enabled: bool | None`: Whether the supervision is switched on, null when the controller did not report it
- `level: int | None`: Sensitivity of the supervision, as a percentage: the lower the value, the sooner a collision is reported. Null when the controller did not report it.

## MotionSystemErrorState

`from underautomation.abb.rws.data.motion_system_error_state import MotionSystemErrorState`

Error state of the motion system, and how many errors it has counted. Returned by MotionSystemService.GetErrorState().

- `MotionSystemErrorState()`: Initializes a new instance of the MotionSystemErrorState class
- `state: MotionErrorState`: Last error the motion system ran into
- `raw_state: str`: Error state exactly as the controller reported it, useful when state is Unknown
- `count: int | None`: Number of errors counted since the controller started, incremented on every new error, null when the controller did not report it

## MotionSystemInfo

`from underautomation.abb.rws.data.motion_system_info import MotionSystemInfo`

Overview of the motion system of the controller. Returned by MotionSystemService.GetInfo().

- `MotionSystemInfo()`: Initializes a new instance of the MotionSystemInfo class
- `change_count: int | None`: Counter the controller increments on every change of the motion system. Pass it to MotionSystemService.HasChanged() to find out whether anything moved since a previous reading, without fetching the whole state again.
- `mechanical_unit_name: str`: Name of the mechanical unit the jogging commands currently apply to
- `poll_rate: int | None`: Rate at which the controller refreshes the motion system state, null when it did not report it
- `modal_payload_mode: bool | None`: Whether the payload of the robot is set by the running program rather than by the mechanical unit, null when the controller did not report it
- `absolute_accuracy_active: bool | None`: Whether absolute accuracy is switched on, null when the controller did not report it

## MotorCalibrationName

`from underautomation.abb.rws.data.motor_calibration_name import MotorCalibrationName`

Names one joint of a mechanical unit carries: the joint itself and the calibration data attached to it. Returned by MotionSystemService.GetMotorCalibrationNames().

- `MotorCalibrationName()`: Initializes a new instance of the MotorCalibrationName class
- `number: int`: Number of the joint inside its mechanical unit, starting at 1
- `joint_name: str`: Name of the joint, for example "rob1_1"
- `calibration_name: str`: Name of the calibration data of the joint, usually the same as joint_name

## NetworkConfigurationMethod

`from underautomation.abb.rws.data.network_configuration_method import NetworkConfigurationMethod`

IP configuration method of a controller LAN adapter

- FixIp: Fixed IP address, the address, mask and gateway have to be provided
- Dhcp: IP address obtained from a DHCP server
- NoIp: No IP address configured on the adapter

## NetworkInterfaceItem

`from underautomation.abb.rws.data.network_interface_item import NetworkInterfaceItem`

Network interface of the robot controller. Returned by ControllerService.GetNetworkInterfaces().

- `NetworkInterfaceItem()`: Initializes a new instance of the NetworkInterfaceItem class
- `port: str`: Physical port of the interface, for example "X6" or "X23"
- `logical_name: str`: Logical name of the interface, for example "WAN", "LAN1" or "SERVICE"
- `network: str`: Network the interface belongs to ("Public", "Private", "Ability", "Drive"). Only available when connected with version 2.
- `address: str`: IP address of the interface
- `mask: str`: Subnet mask of the interface
- `primary_dns: str`: Primary DNS server of the interface. Only available when connected with version 2.
- `secondary_dns: str`: Secondary DNS server of the interface. Only available when connected with version 2.
- `dhcp_enabled: bool | None`: DHCP status of the interface, if reported by the controller
- `gateway: str`: Default gateway of the interface, if applicable

## OperationMode

`from underautomation.abb.rws.data.operation_mode import OperationMode`

Operating mode selected on the robot controller

- Unknown: The operating mode could not be determined
- Init: The controller is initializing
- AutomaticChangeRequest: A change to the automatic mode has been requested and is waiting to be acknowledged
- ManualFullSpeedChangeRequest: A change to the manual full speed mode has been requested and is waiting to be acknowledged
- ManualReducedSpeed: Manual mode at reduced speed
- ManualFullSpeed: Manual mode at full speed
- Automatic: Automatic mode
- Undefined: The controller reports an undefined operating mode

## OperationModeAcknowledgement

`from underautomation.abb.rws.data.operation_mode_acknowledgement import OperationModeAcknowledgement`

Pending change that an operating mode acknowledgement confirms

- Automatic: Confirms the switch to the automatic mode
- ManualFullSpeed: Confirms the switch to the manual full speed mode
- CollisionDetection: Confirms a collision detection

## OperationModeLockState

`from underautomation.abb.rws.data.operation_mode_lock_state import OperationModeLockState`

Lock state of the operating mode selector

- Unknown: The lock state could not be determined
- Error: The controller reports an error on the mode selector lock
- Unlocked: The operating mode can be changed freely
- Locked: The operating mode is locked and can be unlocked again with the pin code it was locked with
- PermanentlyLocked: The operating mode is permanently locked
- PendingPermanentLock: A permanent lock has been requested and is not effective yet

## PathSupervision

`from underautomation.abb.rws.data.path_supervision import PathSupervision`

Collision detection settings of one mechanical unit while it follows a programmed path. Returned by MotionSystemService.GetPathSupervision().

- `PathSupervision()`: Initializes a new instance of the PathSupervision class
- `enabled: bool | None`: Whether the supervision is switched on, null when the controller did not report it
- `level: int | None`: Sensitivity of the supervision, as a percentage: the lower the value, the sooner a collision is reported. Null when the controller did not report it.

## RapidActivationRecord

`from underautomation.abb.rws.data.rapid_activation_record import RapidActivationRecord`

One frame of the call stack of a task: which routine is running and where the execution stands in it. Returned by RapidService.GetActivationRecord(). Frame 1 is the routine holding the program pointer, and the number grows towards the entry point of the program.

- `RapidActivationRecord()`: Initializes a new instance of the RapidActivationRecord class
- `execution_level: RapidExecutionLevel`: Level at which this frame is executing
- `begin_row: int | None`: Line the executing statement starts at, null when the controller did not report it
- `begin_column: int | None`: Column the executing statement starts at, null when the controller did not report it
- `end_row: int | None`: Line the executing statement ends at, null when the controller did not report it
- `end_column: int | None`: Column the executing statement ends at, null when the controller did not report it
- `stack_url: str`: Path identifying this stack frame, which the UI instruction resources also take
- `routine_url: str`: Path of the routine this frame is executing

## RapidAliasIoItem

`from underautomation.abb.rws.data.rapid_alias_io_item import RapidAliasIoItem`

An I/O signal a running RAPID program has given an alias to with the AliasIO instruction. Returned by RapidService.GetAliasIo(). The controller only knows about an alias while the program that declares it is loaded, so this list is empty on a controller holding no such program.

- `RapidAliasIoItem()`: Initializes a new instance of the RapidAliasIoItem class
- `alias_name: str`: Name the RAPID program refers to the signal by
- `signal_name: str`: Name of the I/O signal the alias points at
- `type: IoSignalType`: Type of the aliased signal

## RapidBreakpoint

`from underautomation.abb.rws.data.rapid_breakpoint import RapidBreakpoint`

A breakpoint set in the program of a task. Returned by RapidService.GetBreakpoints() and RapidService.SetBreakpoint(). The controller answers a write with the range it actually snapped the breakpoint to, which is the whole instruction containing the requested position rather than the position its...

- `RapidBreakpoint()`: Initializes a new instance of the RapidBreakpoint class
- `module_name: str`: Name of the module the breakpoint sits in, null when the controller did not report it
- `start_row: int | None`: Line the breakpoint starts at, null when the controller did not report it
- `start_column: int | None`: Column the breakpoint starts at, null when the controller did not report it
- `end_row: int | None`: Line the breakpoint ends at, null when the controller did not report it
- `end_column: int | None`: Column the breakpoint ends at, null when the controller did not report it

## RapidBuildError

`from underautomation.abb.rws.data.rapid_build_error import RapidBuildError`

An error the controller found while linking the program of a task. Returned by RapidService.GetBuildErrors().

- `RapidBuildError()`: Initializes a new instance of the RapidBuildError class
- `module_name: str`: Name of the module the error was found in
- `row: int | None`: Line the error was found at, null when the controller did not report it
- `column: int | None`: Column the error was found at, null when the controller did not report it
- `error_number: int | None`: Numeric identifier of the error, null when the controller did not report it
- `error: str`: Description of the error as the controller worded it

## RapidExecutionCycle

`from underautomation.abb.rws.data.rapid_execution_cycle import RapidExecutionCycle`

How many times the controller runs the program before stopping

- Unknown: The controller reported a cycle this library does not know
- Forever: The program runs again every time it reaches its end
- AsIs: The cycle currently configured is left untouched
- Once: The program runs once and stops at its end
- OnceDone: The program was asked to run once and has finished doing so

## RapidExecutionInfo

`from underautomation.abb.rws.data.rapid_execution_info import RapidExecutionInfo`

Overall RAPID execution state of the controller. Returned by RapidService.GetExecutionState().

- `RapidExecutionInfo()`: Initializes a new instance of the RapidExecutionInfo class
- `state: RapidExecutionState`: Whether RAPID code is currently running
- `cycle: RapidExecutionCycle`: Number of cycles the program is set to run

## RapidExecutionLevel

`from underautomation.abb.rws.data.rapid_execution_level import RapidExecutionLevel`

Level at which the code of a task is currently executing

- Unknown: The controller reported a level this library does not know
- None_: Nothing is executing
- Normal: The normal user code is executing
- Trap: A trap routine is executing
- User: A user routine is executing

## RapidExecutionMode

`from underautomation.abb.rws.data.rapid_execution_mode import RapidExecutionMode`

How far the program advances when execution is started

- Continue_: Run until something stops it
- StepIn: Step into the routine called by the current instruction
- StepOver: Run the current instruction whole, without entering the routine it calls
- StepOut: Run until the current routine returns
- StepBack: Step one instruction backwards
- StepLast: Step to the last instruction
- StepMotion: Step to the next motion instruction

## RapidExecutionState

`from underautomation.abb.rws.data.rapid_execution_state import RapidExecutionState`

Whether the controller is currently executing RAPID code

- Unknown: The controller reported a state this library does not know
- Running: RAPID execution is running
- Stopped: RAPID execution is stopped

## RapidExecutionType

`from underautomation.abb.rws.data.rapid_execution_type import RapidExecutionType`

What kind of code a task is currently running

- Unknown: The controller reported a type this library does not know
- None_: Nothing is running
- Normal: The normal program is running
- Interrupt: An interrupt is running
- ExternalInterrupt: An external interrupt is running
- UserRoutine: A user routine is running
- EventRoutine: An event routine is running

## RapidExternalJointStates

`from underautomation.abb.rws.data.rapid_external_joint_states import RapidExternalJointStates`

What each of the six external joints of a task is doing, which says how to read the corresponding value of an external axis. Returned by RapidService.GetExternalJointStates(). A joint reported as carries no meaningful position.

- `RapidExternalJointStates()`: Initializes a new instance of the RapidExternalJointStates class
- `joint1: RapidJointState`: State of the first external joint
- `joint2: RapidJointState`: State of the second external joint
- `joint3: RapidJointState`: State of the third external joint
- `joint4: RapidJointState`: State of the fourth external joint
- `joint5: RapidJointState`: State of the fifth external joint
- `joint6: RapidJointState`: State of the sixth external joint

## RapidHoldToRunState

`from underautomation.abb.rws.data.rapid_hold_to_run_state import RapidHoldToRunState`

State of the hold-to-run control that gates RAPID execution in manual mode

- Press: Ask for execution to be allowed to start
- Held: Confirm that execution may keep running, which has to be repeated about every two seconds
- Release: Stop execution immediately

## RapidInstructionTemplate

`from underautomation.abb.rws.data.rapid_instruction_template import RapidInstructionTemplate`

The template the controller suggests for an instruction or a data type: the arguments to write and the values to write them with. Returned by RapidService.GetInstructionTemplate(). An editor uses it to insert a complete, valid instruction rather than a bare keyword.

- `RapidInstructionTemplate()`: Initializes a new instance of the RapidInstructionTemplate class
- `argument_count: int | None`: Number of arguments the controller reported, null when it did not report it
- `mark: int | None`: Index the controller started reporting from, null when it did not report it
- `complete: bool | None`: Whether every argument has been reported, null when the controller did not report it
- `version: str`: Version the controller stamps on the template
- `selected_parameter: int | None`: Argument the controller suggests selecting first, null when it did not report it
- `arguments: typing.List[RapidInstructionTemplateArgument]`: The suggested arguments

## RapidInstructionTemplateArgument

`from underautomation.abb.rws.data.rapid_instruction_template_argument import RapidInstructionTemplateArgument`

One argument of the template the controller suggests for an instruction or a data type. Carried by .

- `RapidInstructionTemplateArgument()`: Initializes a new instance of the RapidInstructionTemplateArgument class
- `argument_number: int | None`: Position of the argument, null when the controller did not report it
- `required: bool | None`: Whether the argument has to be given, null when the controller did not report it
- `name: str`: Name of the argument, for example "ToPoint"
- `declaration_needed: bool | None`: Whether inserting the instruction also needs a declaration to be created for this argument, null when the controller did not report it
- `symbol: str`: Name of the symbol the argument refers to, empty when the argument is written as a literal
- `value: str`: Value the argument is suggested with, written the way RAPID writes it
- `data_type: str`: Type of the argument, for example "robtarget"
- `object_type: str`: How the suggested symbol is declared, for example "CONST" or "TASK PERS"
- `local: bool | None`: Whether the suggested symbol is local to its module, null when the controller did not report it
- `dimensions: int | None`: Number of array dimensions of the argument, null when the controller did not report it

## RapidJointState

`from underautomation.abb.rws.data.rapid_joint_state import RapidJointState`

What an external joint of a task is doing

- Unknown: The controller reported a state this library does not know
- Linear: The joint moves along a line
- Rotating: The joint turns
- NotActive: The joint is not active
- NoPosition: The joint is active but has no position

## RapidMechanicalUnitItem

`from underautomation.abb.rws.data.rapid_mechanical_unit_item import RapidMechanicalUnitItem`

A mechanical unit the positions of a task are expressed in. Returned by RapidService.GetMechanicalUnits(). This is the view the RAPID task has of the unit; MotionSystemService.GetMechanicalUnits() answers with everything the motion system knows about the same units.

- `RapidMechanicalUnitItem()`: Initializes a new instance of the RapidMechanicalUnitItem class
- `name: str`: Name of the unit, for example "ROB_1"
- `mode: MechanicalUnitMode`: Whether the unit is activated
- `type: MechanicalUnitType`: Kind of unit

## RapidModifiablePositionItem

`from underautomation.abb.rws.data.rapid_modifiable_position_item import RapidModifiablePositionItem`

One motion instruction of the system whose position can be rewritten to where the robot currently stands, wherever in whichever task it sits. Returned by RapidService.GetAllModifiablePositions().

- `RapidModifiablePositionItem()`: Initializes a new instance of the RapidModifiablePositionItem class
- `module_name: str`: Name of the module holding the instruction
- `task_name: str`: Name of the task holding the module
- `start_row: int | None`: Line the instruction starts at, null when the controller did not report it
- `start_column: int | None`: Column the instruction starts at, null when the controller did not report it
- `end_row: int | None`: Line the instruction ends at, null when the controller did not report it
- `end_column: int | None`: Column the instruction ends at, null when the controller did not report it

## RapidModifiablePositions

`from underautomation.abb.rws.data.rapid_modifiable_positions import RapidModifiablePositions`

How many motion instructions of a range can have their position rewritten to where the robot currently stands, and which range they cover. Returned by RapidService.GetModifiablePositions(). The controller leaves the range empty when it found nothing modifiable.

- `RapidModifiablePositions()`: Initializes a new instance of the RapidModifiablePositions class
- `modifiable_line_count: int`: Number of motion instructions of the range whose position can be rewritten
- `start_row: int | None`: Line the modifiable range starts at, null when the controller did not report it
- `start_column: int | None`: Column the modifiable range starts at, null when the controller did not report it
- `end_row: int | None`: Line the modifiable range ends at, null when the controller did not report it
- `end_column: int | None`: Column the modifiable range ends at, null when the controller did not report it

## RapidModuleAttribute

`from underautomation.abb.rws.data.rapid_module_attribute import RapidModuleAttribute`

A property declared on a module, which restricts what may be done with it

- Unknown: The controller reported an attribute this library does not know
- SystemModule: The module belongs to the system rather than to the program
- Encoded: The source of the module is encoded and cannot be read back
- NoView: The source of the module may not be displayed
- NoStepIn: Execution may not step into the routines of the module
- ViewOnly: The source may be displayed but not changed
- ReadOnly: The module may not be changed

## RapidModuleExtension

`from underautomation.abb.rws.data.rapid_module_extension import RapidModuleExtension`

How big the source of a module is, which is what it takes to ask for the whole of it as a range. Returned by RapidService.GetModuleExtension().

- `RapidModuleExtension()`: Initializes a new instance of the RapidModuleExtension class
- `line_count: int | None`: Number of lines the module holds, null when the controller did not report it
- `max_column_count: int | None`: Length of the longest line of the module, null when the controller did not report it
- `change_count: int | None`: Counter the controller increments whenever the module changes, null when it did not report it

## RapidModuleInfo

`from underautomation.abb.rws.data.rapid_module_info import RapidModuleInfo`

Everything the controller reports about one module. Returned by RapidService.GetModule(); the module lists only carry the properties of the base class.

- `RapidModuleInfo()`: Initializes a new instance of the RapidModuleInfo class
- `file_name: str`: Name of the file the module was loaded from, for example "MainModule.mod"
- `attributes: typing.List[RapidModuleAttribute]`: Properties declared on the module, empty when it declares none
- `attribute_count: int (read only)`: Number of properties declared on the module
- Inherited from [RapidModuleItem](underautomation.abb.rws.data.md#rapidmoduleitem): `name`, `type`

## RapidModuleItem

`from underautomation.abb.rws.data.rapid_module_item import RapidModuleItem`

A module loaded into a task, as listed by RapidService.GetModules(). RapidService.GetModule() returns a , which adds the file the module came from and the attributes declared on it.

- `RapidModuleItem()`: Initializes a new instance of the RapidModuleItem class
- `name: str`: Name of the module, for example "MainModule"
- `type: RapidModuleType`: Whether the module belongs to the program or to the system

## RapidModuleSymbol

`from underautomation.abb.rws.data.rapid_module_symbol import RapidModuleSymbol`

The declaration the controller finds at a given position of a module. Returned by RapidService.GetModuleSymbol(), which returns null when there is no declaration at that position.

- `RapidModuleSymbol()`: Initializes a new instance of the RapidModuleSymbol class
- `version: str`: Version the controller stamps on the declaration
- `name: str`: Name of the declared symbol
- `symbol_url: str`: Path of the symbol, which the symbol resources take
- `symbol_type: RapidSymbolType`: What kind of symbol was declared
- `linked: bool | None`: Whether the declaration is complete, null when the controller did not report it
- `local: bool | None`: Whether the symbol is local to its module, null when the controller did not report it
- `type_url: str`: Path of the type of the symbol
- `data_type: str`: Name of the type of the symbol, for example "robtarget"
- `dimensions: int | None`: Number of array dimensions of the symbol, null when the controller did not report it
- `storage: int | None`: How the controller stores the symbol, null when it did not report it
- `heap: bool | None`: Whether the symbol is allocated on the heap, null when the controller did not report it
- `reference_count: int | None`: How many times the symbol is referred to, null when the controller did not report it

## RapidModuleText

`from underautomation.abb.rws.data.rapid_module_text import RapidModuleText`

The source of a module and the counters that go with it. Returned by RapidService.GetModuleText().

- `RapidModuleText()`: Initializes a new instance of the RapidModuleText class
- `text: str`: Source of the module
- `change_count: int | None`: Counter the controller increments whenever the module changes, null when it did not report it
- `declared_length: int | None`: Length the controller declares for the module, null when it did not report it. This is the size the controller reserves for the module and not the length of , so the two normally differ.

## RapidModuleType

`from underautomation.abb.rws.data.rapid_module_type import RapidModuleType`

Whether a module belongs to the program or to the system

- Unknown: The controller reported a type this library does not know
- ProgramModule: A module of the program, saved and loaded with it
- SystemModule: A module of the system, which survives loading another program

## RapidObjectChild

`from underautomation.abb.rws.data.rapid_object_child import RapidObjectChild`

The parts a RAPID object is made of, and where each of them sits in the source. Returned by RapidService.GetObjectChildren(). Which parts the controller reports depends entirely on what the object is: a module answers with its name, its attributes and its declaration lists, a routine with somethi...

- `RapidObjectChild()`: Initializes a new instance of the RapidObjectChild class
- `get_range(name: str) -> RapidTextRange`: Returns the span of one part by its name, null when the controller did not report it
- `object_type: str`: What the object is, for example "module"
- `ranges: typing.List[RapidObjectChildRange]`: The parts of the object, including the ones it does not hold, whose span is then empty
- `range_count: int (read only)`: Number of parts the controller reported

## RapidObjectChildRange

`from underautomation.abb.rws.data.rapid_object_child_range import RapidObjectChildRange`

One named part of a RAPID object, and where it sits in the source. Carried by .

- `RapidObjectChildRange()`: Initializes a new instance of the RapidObjectChildRange class
- `name: str`: Name of the part as the controller worded it, for example "data-decl" or "endmod"
- `range: RapidTextRange`: Where the part sits in the source
- `is_present: bool (read only)`: Whether the controller reported a real span for the part, which it does not when the object does not hold it

## RapidObjectListExtension

`from underautomation.abb.rws.data.rapid_object_list_extension import RapidObjectListExtension`

Where one of the lists of a RAPID object sits in the source: the span of the whole list, and the spans of its first and last elements. Returned by RapidService.GetObjectListExtension(). An editor uses it to jump to the beginning or the end of a list without reading the module.The controller repor...

- `RapidObjectListExtension()`: Initializes a new instance of the RapidObjectListExtension class
- `list: RapidTextRange`: Span of the whole list
- `first: RapidTextRange`: Span of the first element of the list
- `last: RapidTextRange`: Span of the last element of the list

## RapidObjectListType

`from underautomation.abb.rws.data.rapid_object_list_type import RapidObjectListType`

Which of the lists a RAPID object holds is being asked about

- Statements: The statements of the object
- BackwardStatements: The statements of its BACKWARD handler
- ErrorStatements: The statements of its ERROR handler
- UndoStatements: The statements of its UNDO handler
- TypeDeclarations: The type declarations it holds
- DataDeclarations: The data declarations it holds
- ParameterDeclarations: The parameter declarations it holds
- RoutineDeclarations: The routine declarations it holds
- Attributes: The attributes it declares

## RapidPalletHeadItem

`from underautomation.abb.rws.data.rapid_pallet_head_item import RapidPalletHeadItem`

One category of the instruction palette the FlexPendant editor offers, for example "Prog.Flow". Returned by RapidService.GetPalletHeads(); its is what RapidService.GetPallet() takes.

- `RapidPalletHeadItem()`: Initializes a new instance of the RapidPalletHeadItem class
- `name: str`: Name of the category, for example "Motion&Proc."
- `number: int | None`: Number identifying the category, null when the controller did not report it

## RapidPalletItem

`from underautomation.abb.rws.data.rapid_pallet_item import RapidPalletItem`

One entry of an instruction palette category, which an editor offers as something the operator can insert at the cursor. Returned by RapidService.GetPallet().

- `RapidPalletItem()`: Initializes a new instance of the RapidPalletItem class
- `name: str`: Name shown for the entry, for example "MoveJ"
- `instruction: str`: Instruction the entry inserts
- `parameter: int | None`: Parameter the entry preselects, null when the controller did not report it
- `alternative: int | None`: Alternative of the parameter the entry preselects, null when the controller did not report it
- `keyword: int | None`: Whether the entry is a language keyword rather than an instruction, null when the controller did not report it

## RapidPointerPosition

`from underautomation.abb.rws.data.rapid_pointer_position import RapidPointerPosition`

Where one of the two pointers of a task stands. Carried by . tells apart a pointer that is really placed somewhere from one the controller could not report, which happens for the motion pointer whenever the task has not moved yet.

- `RapidPointerPosition()`: Initializes a new instance of the RapidPointerPosition class
- `available: bool`: Whether the controller reported a position for this pointer at all
- `module: str`: Name of the module the pointer stands in
- `routine: str`: Name of the routine the pointer stands in
- `begin_row: int | None`: Line the pointer begins at, null when the controller did not report it
- `begin_column: int | None`: Column the pointer begins at, null when the controller did not report it
- `end_row: int | None`: Line the pointer ends at, null when the controller did not report it
- `end_column: int | None`: Column the pointer ends at, null when the controller did not report it
- `change_count: int | None`: How many times the pointer has been moved, null when the controller did not report it
- `execution_type: RapidExecutionType`: What kind of code the pointer is standing in

## RapidPointerSyncState

`from underautomation.abb.rws.data.rapid_pointer_sync_state import RapidPointerSyncState`

Whether the pointers of every task are synchronized with each other

- Unknown: The controller reported a state this library does not know
- On: The pointers are synchronized
- Off: The pointers are not synchronized

## RapidPointers

`from underautomation.abb.rws.data.rapid_pointers import RapidPointers`

The program pointer and the motion pointer of a task, read in one request. Returned by RapidService.GetPointers(). The program pointer says which instruction runs next, the motion pointer which one the robot is actually executing; they drift apart because the controller plans the path ahead of th...

- `RapidPointers()`: Initializes a new instance of the RapidPointers class
- `program_pointer: RapidPointerPosition`: Instruction the task will execute next
- `motion_pointer: RapidPointerPosition`: Instruction the robot is currently moving for

## RapidPreferredDataTypeItem

`from underautomation.abb.rws.data.rapid_preferred_data_type_item import RapidPreferredDataTypeItem`

A data type the controller suggests for one argument of an instruction, so that an editor can offer the operator the types that fit where the cursor stands. Returned by RapidService.GetPreferredDataTypes().

- `RapidPreferredDataTypeItem()`: Initializes a new instance of the RapidPreferredDataTypeItem class
- `name: str`: Name of the suggestion, for example "signaldi"
- `data_type: str`: Data type of the suggestion

## RapidProgramCounterPosition

`from underautomation.abb.rws.data.rapid_program_counter_position import RapidProgramCounterPosition`

Where the program pointer of a task stands, expressed as the piece of source it points at. Returned by RapidService.GetProgramCounterPosition(). The controller refuses the request when the task has no program pointer set, so reset it or start the program first.

- `RapidProgramCounterPosition()`: Initializes a new instance of the RapidProgramCounterPosition class
- `module: str`: Name of the module the pointer stands in
- `routine: str`: Name of the routine the pointer stands in
- `start_line: int | None`: Line the pointed instruction starts at, null when the controller did not report it
- `start_column: int | None`: Column the pointed instruction starts at, null when the controller did not report it
- `end_line: int | None`: Line the pointed instruction ends at, null when the controller did not report it
- `end_column: int | None`: Column the pointed instruction ends at, null when the controller did not report it

## RapidProgramInfo

`from underautomation.abb.rws.data.rapid_program_info import RapidProgramInfo`

The program loaded into a task. Returned by RapidService.GetProgram(), which returns null when the task holds no program at all.

- `RapidProgramInfo()`: Initializes a new instance of the RapidProgramInfo class
- `name: str`: Name of the program, null when the controller did not report it
- `entry_point: str`: Routine the program pointer moves to when it is reset, null when the controller did not report it

## RapidProgramLoadMode

`from underautomation.abb.rws.data.rapid_program_load_mode import RapidProgramLoadMode`

What happens to the modules already in a task when a program is loaded into it

- Add: Keep the modules already loaded and add the ones of the program
- Replace: Replace everything the task holds with the program

## RapidRegainMode

`from underautomation.abb.rws.data.rapid_regain_mode import RapidRegainMode`

What the robot does about the distance between where it stands and where the path it is about to resume expects it to be

- Continue_: Resume from the current position without moving back to the path
- Regain: Move back onto the path before resuming
- Clear: Drop the path and resume from the current position
- EnterConsume: Resume by entering the consumption of the already generated path

## RapidRoutineArgument

`from underautomation.abb.rws.data.rapid_routine_argument import RapidRoutineArgument`

One argument of the routine call found at a given position of a module, and where it sits in the source. Returned by RapidService.GetRoutineArguments().

- `RapidRoutineArgument()`: Initializes a new instance of the RapidRoutineArgument class
- `parameter_number: int | None`: Position of the argument in the call, counted from 0
- `alternate_argument: int | None`: Which alternative of the parameter this argument fills, null when the controller did not report it
- `start_row: int | None`: Line the argument starts at, null when the controller did not report it
- `start_column: int | None`: Column the argument starts at, null when the controller did not report it
- `end_row: int | None`: Line the argument ends at, null when the controller did not report it
- `end_column: int | None`: Column the argument ends at, null when the controller did not report it
- `object_type: str`: What the argument is, for example a required argument or a name reference
- `data_type: str`: Type of the argument, for example "num"
- `list_number: int | None`: Position of the argument in the argument list, null when the controller did not report it
- `list_length: int | None`: Length of the argument list, null when the controller did not report it

## RapidRoutineInfo

`from underautomation.abb.rws.data.rapid_routine_info import RapidRoutineInfo`

The routine the controller finds called at a given position of a module. Returned by RapidService.GetRoutine(). The controller refuses the request when the position does not sit on a routine call.

- `RapidRoutineInfo()`: Initializes a new instance of the RapidRoutineInfo class
- `symbol_url: str`: Path of the routine, which the program pointer resources take
- `name: str`: Name of the routine
- `symbol_type: RapidSymbolType`: Whether the routine is a procedure, a function or a trap
- `named: bool | None`: Whether the routine is named, null when the controller did not report it
- `local: bool | None`: Whether the routine is local to its module, null when the controller did not report it
- `parameter_count: int | None`: Number of parameters the routine takes, null when the controller did not report it. The controller reports -1 when the parameter list is not linked yet.

## RapidServiceRoutineItem

`from underautomation.abb.rws.data.rapid_service_routine_item import RapidServiceRoutineItem`

A routine of a task the program pointer can be moved to. Returned by RapidService.GetServiceRoutines().

- `RapidServiceRoutineItem()`: Initializes a new instance of the RapidServiceRoutineItem class
- `name: str`: Name of the routine, for example "LoadIdentify"
- `url: str`: Path of the routine, which RapidService.SetProgramPointerToRoutineUrl() takes
- `is_service_routine: bool | None`: Whether this is a service routine rather than an ordinary one, null when the controller did not report it

## RapidSetTextRangeResult

`from underautomation.abb.rws.data.rapid_set_text_range_result import RapidSetTextRangeResult`

What the controller did with a change written into the source of a module. Returned by RapidService.SetModuleTextRange(). Rewriting the MODULE line renames the module, which is why the controller reports the name it ended up with.

- `RapidSetTextRangeResult()`: Initializes a new instance of the RapidSetTextRangeResult class
- `module_renamed: bool`: Whether the change renamed the module
- `new_module_name: str`: Name the module now has, empty when the change did not rename it
- `change_count: int | None`: Counter the controller incremented for the change, null when it did not report it

## RapidSpyStatus

`from underautomation.abb.rws.data.rapid_spy_status import RapidSpyStatus`

Whether the controller is recording the RAPID execution trace to a file

- Unknown: The controller reported a status this library does not know
- Logging: The execution trace is being written
- NotLogging: No execution trace is being written

## RapidStartCondition

`from underautomation.abb.rws.data.rapid_start_condition import RapidStartCondition`

Condition the controller checks before it starts executing

- None_: Start without any additional check
- CallChain: Start only when the call chain of the program pointer is still valid

## RapidStopMode

`from underautomation.abb.rws.data.rapid_stop_mode import RapidStopMode`

How abruptly RAPID execution is stopped

- Cycle: Stop when the current cycle ends
- Instruction: Stop when the current instruction ends
- Stop: Stop as soon as the robot can decelerate along its path
- QuickStop: Stop as fast as the robot can, leaving the path

## RapidStructuralChangeCount

`from underautomation.abb.rws.data.rapid_structural_change_count import RapidStructuralChangeCount`

The two counters a task keeps of what has changed in it, so that a client can tell whether it needs to read the task again instead of fetching everything periodically. Returned by RapidService.GetStructuralChangeCount().

- `RapidStructuralChangeCount()`: Initializes a new instance of the RapidStructuralChangeCount class
- `change_count: int | None`: Counter the controller increments whenever anything relevant changes in the task
- `structural_change_count: int | None`: Counter the controller increments when a module is loaded, unloaded or renamed. A rename counts as an unload followed by a load.

## RapidSymbolProperties

`from underautomation.abb.rws.data.rapid_symbol_properties import RapidSymbolProperties`

What a RAPID symbol is declared as. Returned by RapidService.GetSymbolProperties() and RapidService.SearchSymbols(). A search fills in and leaves alone, a direct read does the opposite on some controllers, so treat both as optional.

- `RapidSymbolProperties()`: Initializes a new instance of the RapidSymbolProperties class
- `symbol_url: str`: Path of the symbol, which the other symbol methods take
- `name: str`: Name of the symbol, for example "reg1"
- `symbol_type: RapidSymbolType`: What kind of symbol this is
- `named: bool | None`: Whether the symbol is named, null when the controller did not report it
- `data_type: str`: Name of the type of the symbol, for example "num"
- `dimensions: int | None`: Number of array dimensions of the symbol, null when the controller did not report it
- `dimension: str`: Size of each array dimension as the controller worded it, empty when the symbol is not an array
- `heap: bool | None`: Whether the symbol is allocated on the heap, null when the controller did not report it
- `linked: bool | None`: Whether the declaration is complete, null when the controller did not report it
- `local: bool | None`: Whether the symbol is local to its module, null when the controller did not report it
- `read_only: bool | None`: Whether the symbol may not be written, null when the controller did not report it
- `task_variable: bool | None`: Whether the symbol is global within its task, null when the controller did not report it
- `storage: str`: How the controller stores the symbol, for example "loaded"
- `type_url: str`: Path of the type of the symbol, for example "RAPID/num"

## RapidSymbolSearchCriteria

`from underautomation.abb.rws.data.rapid_symbol_search_criteria import RapidSymbolSearchCriteria`

What a symbol search looks for. Passed to RapidService.SearchSymbols(). Every property is optional; leaving one alone means the search does not filter on it. A search with no criterion at all walks the whole system, which is slow, so at least set .

- `RapidSymbolSearchCriteria()`: Initializes a new instance of the RapidSymbolSearchCriteria class
- `view: RapidSymbolSearchView`: Which part of the system the search walks
- `variable_type: RapidSymbolVariableType`: Which variables the search keeps, by what may be done with them
- `block_url: str`: Path the search starts from, for example "RAPID/T_ROB1"
- `recursive: bool | None`: Whether the search also walks what the starting point contains, null to leave it to the controller
- `position_row: int | None`: Line the search starts from, used together with Scope
- `position_column: int | None`: Column the search starts from, used together with Scope
- `stack_frame: int | None`: Frame of the call stack the search starts from, used together with Stack
- `only_used: bool | None`: Whether only the symbols the program actually refers to are kept, null to leave it to the controller
- `skip_shared: bool | None`: Whether the symbols shared between tasks are skipped, null to leave it to the controller
- `name_pattern: str`: Regular expression the name of a symbol has to match to be kept
- `symbol_types: typing.List[RapidSymbolType]`: Kinds of symbol the search keeps, empty to keep every kind
- `data_type: str`: Name of the type a symbol has to have to be kept, for example "robtarget"

## RapidSymbolSearchView

`from underautomation.abb.rws.data.rapid_symbol_search_view import RapidSymbolSearchView`

Which part of the system a symbol search walks

- Undefined: Let the controller decide
- Block: Search the block the search path names, and optionally what it contains
- Scope: Search what is visible from a position of the source, which the search path and the position both have to be given for
- Stack: Search what is visible from a frame of the call stack, which needs the program pointer to be set

## RapidSymbolType

`from underautomation.abb.rws.data.rapid_symbol_type import RapidSymbolType`

What a RAPID symbol is: a value, a routine, a type or one of the structural elements of the language

- Unknown: The controller reported a type this library does not know
- Undefined: The type is not defined
- Atomic: A built-in type such as num or string
- Record: A record type
- Alias: An alias of another type
- RecordComponent: One component of a record
- Constant: A constant
- Variable: A variable
- Persistent: A persistent variable, whose value survives a restart
- Parameter: A parameter of a routine
- Label: A label
- ForVariable: The loop variable of a FOR statement
- Function: A function
- Procedure: A procedure
- Trap: A trap routine
- Module: A module
- Task: A task
- Any: Any of the other types, which a search uses to mean that it does not filter on the type

## RapidSymbolValue

`from underautomation.abb.rws.data.rapid_symbol_value import RapidSymbolValue`

The value of a RAPID symbol and where it is declared. Returned by RapidService.GetSymbolValue(). The value is the text the controller wrote it as, which for a record is the bracketed form RAPID itself uses, for example [[515,0,712],[0.707107,0,0.707107,0],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,...

- `RapidSymbolValue()`: Initializes a new instance of the RapidSymbolValue class
- `value: str`: Value of the symbol, written the way RAPID writes it
- `declaration_position: RapidTextRange`: Where the symbol is declared, null when the controller did not report it
- `initial_value_position: RapidTextRange`: Where the initial value of the symbol is written, null when the controller did not report it. The controller reports zeros when the declaration carries no initial value.

## RapidSymbolVariableType

`from underautomation.abb.rws.data.rapid_symbol_variable_type import RapidSymbolVariableType`

Which variables a symbol search keeps, by what may be done with them

- Undefined: Let the controller decide
- ReadWrite: Only the variables that can be read and written
- ReadOnly: Only the variables that can be read but not written
- Loop: Only the loop variables
- Any: Any of them

## RapidTaskExecutionMode

`from underautomation.abb.rws.data.rapid_task_execution_mode import RapidTaskExecutionMode`

Stepping mode a task was last started with

- Unknown: The controller reported a mode this library does not know
- Continuous: The task runs without stepping
- StepOver: The task steps over the routine calls
- StepIn: The task steps into the routine calls
- StepOutOf: The task steps out of the current routine
- StepBack: The task steps backwards
- StepLast: The task steps to the last instruction
- StepWise: The task advances one instruction at a time

## RapidTaskExecutionState

`from underautomation.abb.rws.data.rapid_task_execution_state import RapidTaskExecutionState`

Whether a single task is running, and whether it could be

- Unknown: The controller reported a state this library does not know
- Ready: The task is ready to be started
- Stopped: The task was running and has been stopped
- Started: The task is running
- Uninitialized: The task is not initialized

## RapidTaskInfo

`from underautomation.abb.rws.data.rapid_task_info import RapidTaskInfo`

Everything the controller reports about one RAPID task. Returned by RapidService.GetTask(); the task lists only carry the properties of the base class.

- `RapidTaskInfo()`: Initializes a new instance of the RapidTaskInfo class
- `trust: RapidTaskTrustLevel`: What the controller does to the system when this task stops unexpectedly
- `task_id: int | None`: Identifier of the task, null when the controller did not report it
- `execution_level: RapidExecutionLevel`: Level at which the code of the task is currently executing
- `execution_mode: RapidTaskExecutionMode`: Stepping mode the task was last started with
- `execution_type: RapidExecutionType`: What kind of code the task is currently running
- `execution_cycle: RapidExecutionCycle`: Number of cycles the task is set to run. Only reported over a connection established with version 2, and left to otherwise.
- `production_entry_point: str`: Routine the program pointer moves to when it is reset, for example "main"
- `bind_reference: bool | None`: Whether the task is bound to a configured task number, null when the controller did not report it
- `task_in_foreground: str`: Name of the task running in the foreground, empty when there is none
- Inherited from [RapidTaskItem](underautomation.abb.rws.data.md#rapidtaskitem): `name`, `type`, `task_state`, `execution_state`, `active`, `motion_task`

## RapidTaskItem

`from underautomation.abb.rws.data.rapid_task_item import RapidTaskItem`

A RAPID task of the controller, as listed by RapidService.GetTasks(). RapidService.GetTask() returns a , which adds everything the controller reports for a single task only.

- `RapidTaskItem()`: Initializes a new instance of the RapidTaskItem class
- `name: str`: Name of the task, for example "T_ROB1"
- `type: RapidTaskType`: Kind of task, which decides when the controller runs it
- `task_state: RapidTaskState`: How far the controller has got in preparing the program of the task
- `execution_state: RapidTaskExecutionState`: Whether the task is running, and whether it could be
- `active: bool | None`: Whether the task is active, null when the controller did not report it
- `motion_task: bool | None`: Whether the task can move a mechanical unit, null when the controller did not report it

## RapidTaskScope

`from underautomation.abb.rws.data.rapid_task_scope import RapidTaskScope`

Whether an execution command applies to the normal tasks only or to every task

- Normal: Apply to the tasks the task selection panel has enabled
- AllTasks: Apply to every task of the system

## RapidTaskSelectionItem

`from underautomation.abb.rws.data.rapid_task_selection_item import RapidTaskSelectionItem`

One line of the task selection panel, telling whether a task is selected and whether an operator is allowed to change that. Returned by RapidService.GetTaskSelection().

- `RapidTaskSelectionItem()`: Initializes a new instance of the RapidTaskSelectionItem class
- `name: str`: Name of the task, for example "T_ROB1"
- `selected: bool | None`: Whether the task is selected, null when the controller did not report it
- `motion_task: bool | None`: Whether the task can move a mechanical unit, null when the controller did not report it
- `user_modify: bool | None`: Whether an operator is allowed to change the selection of this task, null when the controller did not report it

## RapidTaskState

`from underautomation.abb.rws.data.rapid_task_state import RapidTaskState`

How far the controller has got in preparing the program of a task

- Unknown: The controller reported a state this library does not know
- Empty: The task holds no program
- Initiated: The task has been created but its program is not linked yet
- Linked: The program of the task is linked and ready to run
- Loaded: A program is loaded into the task but not linked yet
- Uninitialized: The task is not initialized

## RapidTaskTrustLevel

`from underautomation.abb.rws.data.rapid_task_trust_level import RapidTaskTrustLevel`

What the controller does to the system when a task that is not a normal one stops unexpectedly

- Unknown: The controller reported a level this library does not know
- None_: The system carries on
- SystemFailure: The whole system fails
- SystemHalt: The system halts
- SystemStop: The system stops

## RapidTaskType

`from underautomation.abb.rws.data.rapid_task_type import RapidTaskType`

Kind of RAPID task, which decides when the controller runs it

- Unknown: The controller reported a type this library does not know
- Normal: A task started and stopped together with the program
- Static: A task that keeps its program pointer where it was when the controller was switched off
- SemiStatic: A task restarted from its beginning every time the controller starts

## RapidTextPosition

`from underautomation.abb.rws.data.rapid_text_position import RapidTextPosition`

A position in the source of a module, counted from 1. Returned by RapidService.SearchModuleText(), which reports row and column 0 when the text was not found rather than failing.

- `RapidTextPosition()`: Initializes a new instance of the RapidTextPosition class
- `row: int`: Line of the position, 0 when the search found nothing
- `column: int`: Column of the position, 0 when the search found nothing
- `found: bool (read only)`: Whether the position points at something, which it does not when a search found nothing

## RapidTextQueryMode

`from underautomation.abb.rws.data.rapid_text_query_mode import RapidTextQueryMode`

How hard the controller tries to apply a change to the source of a running task

- Force: Apply the change even when it invalidates the program pointer
- Try_: Apply the change only when the program pointer survives it

## RapidTextRange

`from underautomation.abb.rws.data.rapid_text_range import RapidTextRange`

A span of source between two positions, counted from 1. Used wherever the controller reports where something is declared or where a statement sits.

- `RapidTextRange()`: Initializes a new instance of the RapidTextRange class
- `begin_row: int | None`: Line the range begins at, null when the controller did not report it
- `begin_column: int | None`: Column the range begins at, null when the controller did not report it
- `end_row: int | None`: Line the range ends at, null when the controller did not report it
- `end_column: int | None`: Column the range ends at, null when the controller did not report it

## RapidTextReplaceMode

`from underautomation.abb.rws.data.rapid_text_replace_mode import RapidTextReplaceMode`

Where new text is put relative to the range it is written against

- After: Insert the new text after the range, leaving it in place
- Before: Insert the new text before the range, leaving it in place
- Replace: Replace the range with the new text

## RapidUiInstruction

`from underautomation.abb.rws.data.rapid_ui_instruction import RapidUiInstruction`

The dialogue a running RAPID program is currently asking an operator for. Returned by RapidService.GetActiveUiInstruction(), which returns null when no instruction is pending. Answering one means writing its parameters with RapidService.SetUiInstructionParameter(), using to address them.

- `RapidUiInstruction()`: Initializes a new instance of the RapidUiInstruction class
- `instruction: str`: Name of the RAPID instruction that opened the dialogue, for example "TPReadNum"
- `event: RapidUiInstructionEvent`: What the instruction is asking of the client
- `stack_url: str`: Path identifying the call, which the parameter methods take
- `execution_level: RapidExecutionLevel`: Level at which the instruction is executing
- `message: str`: Text the instruction displays

## RapidUiInstructionEvent

`from underautomation.abb.rws.data.rapid_ui_instruction_event import RapidUiInstructionEvent`

What a UI instruction is asking of the client

- Unknown: The controller reported an event this library does not know
- Send: The instruction is waiting for an answer
- Post: The instruction only displays something and expects no answer
- Abort: The instruction has been abandoned and no answer is expected any more

## RapidUiInstructionParameter

`from underautomation.abb.rws.data.rapid_ui_instruction_parameter import RapidUiInstructionParameter`

One parameter of the pending UI instruction: what the program passed in, or what it is waiting for. Returned by RapidService.GetUiInstructionParameters(). The parameters carrying the answer are the ones to write, typically named after a function key or after the completion flag of the instruction.

- `RapidUiInstructionParameter()`: Initializes a new instance of the RapidUiInstructionParameter class
- `name: str`: Name of the parameter, for example "TPCompleted"
- `value: str`: Value of the parameter, written the way RAPID writes it

## SafetyConfiguration

`from underautomation.abb.rws.data.safety_configuration import SafetyConfiguration`

Safety supervision configuration of the controller. Returned by ControllerService.GetSafetyConfiguration().

- `SafetyConfiguration()`: Initializes a new instance of the SafetyConfiguration class
- `configuration_status: str`: Status of the configuration, for example "SCORCH_CONFIG_LOADED". Only available when connected with version 2.
- `software_major_version: int | None`: Safety software major version
- `software_minor_version: int | None`: Safety software minor version
- `software_revision: int | None`: Safety software revision
- `file_major_version: int | None`: Configuration file major version
- `file_minor_version: int | None`: Configuration file minor version
- `file_revision: int | None`: Configuration file revision
- `creation_date: datetime | None`: Creation date of the configuration, if available
- `created_by: str`: Author of the configuration
- `name: str`: Name of the configuration
- `checksum: str`: Checksum of the configuration, as base64 encoded data

## SafetyLoadOperationStatus

`from underautomation.abb.rws.data.safety_load_operation_status import SafetyLoadOperationStatus`

Indicates whether a new safety configuration is allowed to be loaded

- Unknown: The status could not be determined
- Ok: Loading a new safety configuration is allowed
- OptionNotPresent: The safety option is not present on the controller (SCORCH_ERR_OPTION_NOT_PRESENT)
- NotInManualMode: The controller is not in manual mode (SCORCH_ERR_NOT_IN_MANUAL_MODE)
- NotInMotorsOff: The motors are not switched off (SCORCH_ERR_NOT_IN_MOTORS_OFF)
- CurrentConfigurationLocked: The current safety configuration is locked (SCORCH_ERR_CURRENT_CONFIG_LOCKED)
- UserGrantMissing: The user does not have the required grant (SCORCH_ERR_USER_GRANT_IS_MISSING)

## SafetyMode

`from underautomation.abb.rws.data.safety_mode import SafetyMode`

Safety mode of the safety controller

- Unknown: The safety mode could not be determined
- Active: The safety configuration is active and supervised
- Commissioning: Commissioning mode, used while configuring the safety controller
- Service: Service mode
- ModeError: The safety controller reports a mode error

## SafetyModeStatus

`from underautomation.abb.rws.data.safety_mode_status import SafetyModeStatus`

Safety mode status of the controller. Returned by ControllerService.GetSafetyMode().

- `SafetyModeStatus()`: Initializes a new instance of the SafetyModeStatus class
- `mode: SafetyMode`: Current safety mode
- `user_data: int | None`: User data associated with the safety mode, if reported by the controller

## SafetyViolationInfo

`from underautomation.abb.rws.data.safety_violation_info import SafetyViolationInfo`

Safety violation details reported by the safety controller. Returned by ControllerService.GetSafetyViolationInfo().

- `SafetyViolationInfo()`: Initializes a new instance of the SafetyViolationInfo class
- `violation_number: int | None`: Number of violations
- `violation_type: SafetyViolationType`: Type of the current violation
- `last_violation_instance_id: int | None`: Instance id of the last violation
- `unsynchronized: int | None`: Indicates whether the robot is unsynchronized
- `tool_id: int | None`: Id of the tool involved in the violation
- `drive_module_index: int | None`: Index of the drive module involved in the violation
- `violating_ssv: int | None`: Violating safety supervision value
- `tool_position_violation_status: int | None`: Tool position violation status
- `tool_position_active_status: int | None`: Tool position supervision active status
- `upper_arm_violation_status: int | None`: Upper arm violation status
- `tool_speed_violation_status: int | None`: Tool speed violation status
- `tool_speed_active_status: int | None`: Tool speed supervision active status
- `axis_range_violation_status: int | None`: Axis range violation status
- `axis_range_active_status: int | None`: Axis range supervision active status

## SafetyViolationType

`from underautomation.abb.rws.data.safety_violation_type import SafetyViolationType`

Type of safety violation reported by the safety controller

- Unknown: The violation type could not be determined
- None_: No violation
- SafeToolZone: Safe Tool Zone (stz)
- SafeAxisRange: Safe Axis Range (sar)
- SafeToolSpeed: Safe Tool Speed (sts)
- SafeAxisSpeed: Safe Axis Speed (sas)
- ToolOrientationMonitoring: Tool Orientation Monitoring (tom)
- OperationalSafetyRange: Operational Safety Range (osr)
- SafeStandstill: Safe Standstill (sst)
- ReducedToolSpeed: Reduced Tool Speed in manual mode (red_tool_speed)
- ReducedAxisSpeed: Reduced Axis Speed in manual mode (red_axis_speed)
- UnsynchronizedSpeedLimit: Reduced Axis Speed due to unsynchronized robot (unsync_speed_lim)
- EmergencyStop: Emergency stop triggered (empstop)
- Other: Internal error (other)
- Invalid: The safety controller reports an invalid violation

## SmbData

`from underautomation.abb.rws.data.smb_data import SmbData`

Serial measurement board data of one mechanical unit, held twice: once in the controller cabinet and once in the memory of the robot itself. Returned by MotionSystemService.GetSmbData(). Comparing the cabinet properties with the robot ones tells whether the two copies still agree, which is what M...

- `SmbData()`: Initializes a new instance of the SmbData class
- `cabinet_serial_number_valid: bool | None`: Whether the serial number stored in the cabinet is usable, null when the controller did not report it
- `cabinet_serial_number_high_part: str`: High part of the serial number stored in the cabinet
- `cabinet_serial_number_low_part: str`: Low part of the serial number stored in the cabinet
- `cabinet_service_information_status: SmbDataStatus`: State of the service information data stored in the cabinet
- `cabinet_absolute_accuracy_status: SmbDataStatus`: State of the absolute accuracy data stored in the cabinet
- `cabinet_calibration_status: SmbDataStatus`: State of the calibration data stored in the cabinet
- `cabinet_axis_calibration_status: SmbDataStatus`: State of the axis calibration data stored in the cabinet
- `robot_serial_number_valid: bool | None`: Whether the serial number stored in the robot is usable, null when the controller did not report it
- `robot_serial_number_high_part: str`: High part of the serial number stored in the robot
- `robot_serial_number_low_part: str`: Low part of the serial number stored in the robot
- `robot_service_information_status: SmbDataStatus`: State of the service information data stored in the robot
- `robot_absolute_accuracy_status: SmbDataStatus`: State of the absolute accuracy data stored in the robot
- `robot_calibration_status: SmbDataStatus`: State of the calibration data stored in the robot
- `robot_axis_calibration_status: SmbDataStatus`: State of the axis calibration data stored in the robot
- `drive_module: int | None`: Number of the drive module the data belongs to, null when the controller did not report it
- `measurement_link: int | None`: Number of the measurement link the data belongs to, null when the controller did not report it
- `measurement_board: int | None`: Number of the measurement board the data belongs to, null when the controller did not report it

## SmbDataMemory

`from underautomation.abb.rws.data.smb_data_memory import SmbDataMemory`

Which of the two copies of the serial measurement board data is erased

- Robot: The copy held by the robot itself
- Controller: The copy held by the controller cabinet

## SmbDataStatus

`from underautomation.abb.rws.data.smb_data_status import SmbDataStatus`

State of one block of serial measurement board data, on the controller side or on the robot side

- Unknown: The controller reported a state this library does not know
- Valid: The data is present and the two copies agree
- ValidNotEqual: The data is present on both sides, but the two copies differ
- NotValid: The data is missing or unusable
- NotUsed: The robot system does not use this block of data

## SmbDataTransfer

`from underautomation.abb.rws.data.smb_data_transfer import SmbDataTransfer`

Which of the two copies of the serial measurement board data overwrites the other

- RobotToController: The copy held by the robot is written into the controller cabinet
- ControllerToRobot: The copy held by the controller cabinet is written into the robot

## SystemEnergy

`from underautomation.abb.rws.data.system_energy import SystemEnergy`

Energy the controller has consumed, for the current measurement interval and since the last reset. Returned by SystemService.GetEnergy().

- `SystemEnergy()`: Initializes a new instance of the SystemEnergy class
- `is_measurement_valid: bool`: Whether the reported measurement is valid. When false, every energy value of this instance is meaningless and the measurement has to be read again later.
- `state: SystemEnergyState`: State of the energy measurement
- `change_count: int | None`: Counter the controller increments every time a new measurement is available. Comparing it with the previous one tells whether the values changed without reading them all.
- `time_stamp: datetime | None`: Moment the measurement was taken, null when the controller did not report it
- `reset_time: datetime | None`: Moment the accumulated energy was last reset, null when the controller did not report it
- `interval_length: int | None`: Length of the measurement interval in seconds, which the average power is computed from, null when the controller did not report it
- `interval_energy: float | None`: Total energy consumed during the current measurement interval, in joules, null when the controller did not report it
- `accumulated_energy: float | None`: Total energy consumed since the last reset, in joules, null when the controller did not report it
- `mechanical_units: typing.List[SystemEnergyMechanicalUnit]`: Energy consumed by each mechanical unit during the current measurement interval
- `average_power: float | None (read only)`: Average power consumed during the current measurement interval, in watts. Null when the interval energy or the interval length is missing, or when the interval is empty.
- `mechanical_unit_count: int (read only)`: Number of mechanical units the controller reported

## SystemEnergyAxis

`from underautomation.abb.rws.data.system_energy_axis import SystemEnergyAxis`

Energy consumed by one axis of a mechanical unit during the current measurement interval. Held by .

- `SystemEnergyAxis()`: Initializes a new instance of the SystemEnergyAxis class
- `number: int`: Number of the axis inside its mechanical unit, starting at 1
- `interval_energy: float | None`: Energy the axis consumed during the current measurement interval, in joules, null when the controller did not report it

## SystemEnergyMechanicalUnit

`from underautomation.abb.rws.data.system_energy_mechanical_unit import SystemEnergyMechanicalUnit`

Energy consumed by one mechanical unit, broken down per axis. Held by .

- `SystemEnergyMechanicalUnit()`: Initializes a new instance of the SystemEnergyMechanicalUnit class
- `name: str`: Name of the mechanical unit, for example "ROB_1"
- `axes: typing.List[SystemEnergyAxis]`: Energy consumed by each axis of the mechanical unit during the current measurement interval
- `axis_count: int (read only)`: Number of axes the controller reported for this mechanical unit

## SystemEnergyState

`from underautomation.abb.rws.data.system_energy_state import SystemEnergyState`

State of the energy measurement of the controller

- Unknown: The energy state could not be determined
- Blocked: Energy measurement is blocked and no new value is produced
- Paused: Energy measurement is paused
- NotPaused: Energy measurement is running
- Resuming: Energy measurement is being resumed
- Pausing: Energy measurement is being paused
- GoingToSleep: The controller is entering its low energy consumption mode
- Sleep: The controller is in its low energy consumption mode

## SystemInfo

`from underautomation.abb.rws.data.system_info import SystemInfo`

Identity and software version of the system running on the controller. Returned by SystemService.GetInfo().

- `SystemInfo()`: Initializes a new instance of the SystemInfo class
- `name: str`: Name of the system installed on the controller
- `version: str`: Version of the robot software the system runs
- `version_name: str`: Human readable version of the robot software the system runs
- `distribution_version: str`: Version of the software distribution the system was installed from. Null when the controller does not report it.
- `system_id: str`: Unique identifier of the system
- `start_time: datetime | None`: Moment the system was last started, null when the controller did not report it
- `major: int | None`: Major number of the version, null when the controller did not report it
- `minor: int | None`: Minor number of the version, null when the controller did not report it
- `build: int | None`: Build number of the version, null when the controller did not report it
- `revision: int | None`: Revision number of the version, null when the controller did not report it
- `sub_revision: int | None`: Sub revision number of the version, null when the controller did not report it
- `build_tag: str`: Free text describing the build the system was produced by, null when the controller did not report it
- `api_compatibility_revision: int | None`: Revision of the programming interface the system is compatible with, null when the controller did not report it
- `title: str`: Title of the system, null when the controller did not report it
- `type: str`: Type of the system, null when the controller did not report it
- `description: str`: Description of the system, null when the controller did not report it
- `date: datetime | None`: Date the system was produced, null when the controller did not report it
- `configuration_timestamp: str`: Timestamp of the configuration the system was built with, as the controller spells it. Null when the controller did not report it, which is the usual case on a virtual controller.
- `options: typing.List[str]`: Options installed on the system, in the order the controller reports them
- `option_count: int (read only)`: Number of options installed on the system

## SystemProduct

`from underautomation.abb.rws.data.system_product import SystemProduct`

One software product installed on the controller. Returned by SystemService.GetProducts().

- `SystemProduct()`: Initializes a new instance of the SystemProduct class
- `name: str`: Name of the product, for example "RobotWare" or "RobotControl"
- `version: str`: Full version of the product, build information included. Null when the controller only reports the version name.
- `version_name: str`: Human readable version of the product

## TimeServerInfo

`from underautomation.abb.rws.data.time_server_info import TimeServerInfo`

Time server used by the controller to synchronize its clock. Returned by ControllerService.GetTimeServer().

- `TimeServerInfo()`: Initializes a new instance of the TimeServerInfo class
- `address: str`: Address of the time server
- `time: datetime | None`: Time reported by the time server (UTC), if available. Only available when connected with version 2.

## VirtualTimeState

`from underautomation.abb.rws.data.virtual_time_state import VirtualTimeState`

State of the virtual time server of a virtual controller

- Unknown: The state could not be determined
- Stop: Virtual time is stopped (VTSTOP)
- FreeRun: Virtual time runs freely (VTFREERUN)
- RunSlice: Virtual time runs one time slice at a time (VTRUNSLICE)
- NextEvent: Virtual time runs until the next event (VTNEXTEVENT)
