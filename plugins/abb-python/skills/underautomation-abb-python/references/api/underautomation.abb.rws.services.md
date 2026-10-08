# underautomation.abb.rws.services

## ControllerService (robot.rws.controller)

`from underautomation.abb.rws.services.controller_service import ControllerService`

Controller Service - Provides access to the controller resources: clock, identity, network, installed systems, options, backups, safety controller and virtual time.

- `get_info() -> ControllerInfo`: Gets an overview of the controller resources (synchronous) Contains the current system time, the controller identity and the list of available sub resources.
- `get_environment_variable(name: str) -> str`: Gets the value of a controller environment variable (synchronous)
- `get_clock() -> datetime`: Gets the current system time of the controller (synchronous) The time returned by the controller is always UTC.
- `set_clock(dateTime: datetime) -> None`: Sets the system time of the controller (synchronous) The controller clock is always UTC, pass a UTC date and time.Instead of setting the time explicitly, a time server can be configured with .
- `get_time_zone() -> str`: Gets the time zone used by the controller (synchronous)
- `set_time_zone(timeZone: str) -> None`: Sets the time zone used by the controller (synchronous) Available only on a real controller.
- `get_time_server(serverIp: str=None) -> TimeServerInfo`: Gets the time server used by the controller to synchronize its clock (synchronous) Available only on a real controller.
- `set_time_server(timeServer: str) -> None`: Sets the time server used by the controller to synchronize its clock (synchronous) Available only on a real controller.
- `get_identity() -> ControllerIdentity`: Gets the identity of the controller: name, id, type, MAC address and level (synchronous)
- `set_identity(name: str, id: str=None) -> None`: Sets the identity of the controller (synchronous) Available only on a real controller.
- `set_language(language: str) -> None`: Sets the language of the controller (synchronous)
- `get_network_interfaces() -> typing.List[NetworkInterfaceItem]`: Gets the IP configuration of all network interfaces of the controller (synchronous) Not applicable to a virtual controller.
- `set_network_configuration(method: NetworkConfigurationMethod, address: str=None, mask: str=None, gateway: str=None) -> None`: Sets the IP configuration of the LAN adapter of the controller (synchronous) The controller must be restarted for the change to take effect. Requires the UAS grant UAS_CONTROLLER_PROPERTIES_WRITE.Not supported by a virtual controller.
- `restart(mode: ControllerRestartMode, useImplicitMastership: bool=True) -> None`: Restarts or shuts down the controller (synchronous)
- `get_installed_systems() -> typing.List[str]`: Gets the names of the systems installed on the controller (synchronous)
- `has_option(option: str) -> bool`: Verifies whether an option is present on the controller (synchronous) The option name is case sensitive, for example "SAFEMOVEPRO".
- `is_robot_ware_version_compatible(robotWareVersion: str) -> bool`: Checks whether a RobotWare version is compatible with the controller hardware (synchronous) Supported only on a real controller.
- `get_backup_resources() -> typing.List[str]`: Gets the names of the backup sub resources exposed by the controller (synchronous)
- `get_backup_info(backupPath: str) -> BackupSystemInfo`: Gets information about a backup stored on the controller file system (synchronous)
- `get_backup_state() -> BackupState`: Gets the state of the backup operation of the controller (synchronous) Used to follow a backup started with .
- `create_backup(backupPath: str, archive: bool=False) -> None`: Creates a backup of the current system on the controller file system (synchronous) The backup is created asynchronously by the controller: this method returns as soon as the request is accepted. Poll to know when the backup is finished.Requires the UAS grant UAS_BACKUP. Creating a backup may affe...
- `restore_backup(backupPath: str, ignore: BackupRestoreIgnore=BackupRestoreIgnore.None_, deleteDirectory: bool=True, includeControllerSettings: bool=True, includeSafetySettings: bool=True, include: BackupRestoreInclude=BackupRestoreInclude.All) -> None`: Restores a backup stored on the controller file system (synchronous) When the backup can be restored, the controller restarts.Requires the UAS grant to restore a backup. Use first to detect mismatches.
- `check_restore(backupPath: str, ignore: BackupRestoreIgnore=BackupRestoreIgnore.None_, includeControllerSettings: bool=True, includeSafetySettings: bool=True, include: BackupRestoreInclude=BackupRestoreInclude.All) -> CheckRestoreResult`: Checks a backup for mismatches and other problems before restoring it (synchronous)
- `get_safety_resources() -> typing.List[str]`: Gets the names of the safety sub resources exposed by the controller (synchronous)
- `get_safety_mode() -> SafetyModeStatus`: Gets the safety mode of the controller (synchronous)
- `set_safety_mode(mode: SafetyMode) -> None`: Sets the safety mode of the controller (synchronous) The controller must be in manual mode.
- `get_safety_configuration() -> SafetyConfiguration`: Gets the safety supervision configuration of the controller (synchronous)
- `load_safety_configuration(filePath: str) -> None`: Loads a safety configuration file into the controller (synchronous) The configuration file must already exist on the controller file system.Use to check whether loading is currently allowed.
- `invalidate_safety_configuration() -> None`: Removes the validation information from the safety configuration file (synchronous) Requires the UAS grant UAS_SAFETY_SERVICES.
- `get_safety_load_operation_status() -> SafetyLoadOperationStatus`: Checks whether a new safety configuration is allowed to be loaded (synchronous) The user must have the safety services privileges.
- `get_cyclic_brake_check_status(driveNumber: int) -> CyclicBrakeCheckStatus`: Gets the cyclic brake check status of a mechanical unit (synchronous)
- `get_safety_violation_info() -> SafetyViolationInfo`: Gets the safety violation details reported by the safety controller (synchronous) The user must have the safety services privileges.
- `get_virtual_time_resources() -> typing.List[str]`: Gets the names of the virtual time sub resources exposed by the controller (synchronous) Supported only on a virtual controller.
- `get_virtual_time() -> int`: Gets the current value of the virtual time, in milliseconds (synchronous) The virtual time is zeroed when the virtual controller starts. Supported only on a virtual controller.
- `get_virtual_time_speed() -> int`: Gets the speed of the virtual time, in percent relative to real time (synchronous) -1 means full speed. Supported only on a virtual controller.
- `set_virtual_time_speed(speed: int) -> None`: Sets the speed of the virtual time, in percent relative to real time (synchronous) 100 makes the virtual time run approximately at real time speed, -1 runs it as fast as possible.Supported only on a virtual controller.
- `get_virtual_time_state() -> VirtualTimeState`: Gets the state of the virtual time server (synchronous) Supported only on a virtual controller.
- `set_virtual_time_state(state: VirtualTimeState) -> None`: Sets the state of the virtual time server (synchronous) Supported only on a virtual controller.
- `get_virtual_time_slice() -> int`: Gets the time slice of the virtual controller, in milliseconds (synchronous) Supported only on a virtual controller.
- `set_virtual_time_slice(milliseconds: int) -> None`: Sets the time slice of the virtual controller, in milliseconds (synchronous) The minimum value is 10 ms, lower values are replaced by the controller with the default value of 10 ms.Supported only on a virtual controller.
- `run_virtual_time() -> None`: Executes the virtual time according to the current state of the virtual time server (synchronous) Supported only on a virtual controller.

## ElogService (robot.rws.elog)

`from underautomation.abb.rws.services.elog_service import ElogService`

Event Log Service - Provides access to the messages the controller logs: the list of the log domains, the messages they hold, and the operations that clear them or dump them to a file. None of these resources is available while the controller runs in bootserver mode.

- `get_domains(language: str=None) -> typing.List[ElogDomain]`: Gets every event log domain of the controller, with the number of messages each one holds (synchronous)
- `get_domain(domain: int) -> ElogDomain`: Gets the number of messages one event log domain holds and the number it can hold (synchronous)
- `get_messages(domain: int, order: ElogMessageOrder=ElogMessageOrder.NewestFirst, language: str=None, maxCount: int | None=None) -> typing.List[ElogMessage]`: Gets the messages held by one event log domain (synchronous)
- `get_message_titles(domain: int, language: str, order: ElogMessageOrder=ElogMessageOrder.NewestFirst, maxCount: int | None=None) -> typing.List[ElogMessage]`: Gets the messages held by one event log domain, with their short text only (synchronous)
- `get_message(domain: int, sequenceNumber: int, language: str=None) -> ElogMessage`: Gets one message of an event log domain (synchronous)
- `get_message_by_sequence_number(sequenceNumber: int, language: str=None) -> ElogMessage`: Gets one message from its sequence number alone, without naming the domain it belongs to (synchronous)
- `clear_messages(domain: int) -> None`: Deletes every message of one event log domain (synchronous)
- `clear_all_messages() -> None`: Deletes every message of every event log domain (synchronous)
- `save_in_system_dump_format(path: str) -> None`: Asks the controller to write the whole event log to one file on its own file system (synchronous)

## FileService (robot.rws.file)

`from underautomation.abb.rws.services.file_service import FileService`

File Service - Provides access to the robot controller file system Compatibility:Version 1: directory operations with basic functionalityVersion 2: extended file operations

- `list_directory(path: str) -> DirectoryListing`: Lists contents of a directory resource (synchronous) Environment variables (e.g. $home, $temp) and devices are treated as directories.When listing the root path ("/", null, or "\\"), the response includes available devices in .The complete content is always returned, however many entries the dire...
- `delete_directory(path: str) -> None`: Deletes a directory and all its subdirectories and files (synchronous)
- `create_directory(path: str, newName: str) -> None`: Creates a new directory (synchronous) The newName parameter can contain nested directory structure (e.g. "parentdir/subdir")which will create both directories if they don't exist.
- `rename_directory(path: str, newName: str) -> None`: Renames a directory (synchronous)
- `copy_directory(path: str, newName: str, overwrite: bool) -> None`: Copies a directory (synchronous)
- `delete_file(path: str) -> None`: Deletes a file (synchronous)
- `rename_file(path: str, newName: str) -> None`: Renames a file (synchronous)
- `copy_file(path: str, newName: str, overwrite: bool) -> None`: Copies a file (synchronous)
- `get_file_as_bytes(path: str) -> typing.List[int]`: Gets file content as raw bytes (synchronous)
- `get_file_to_destination(path: str, localPath: str) -> None`: Downloads a file to a local path (synchronous)
- `upload_file_from_bytes(path: str, content: typing.List[int], contentType: str=None) -> None`: Uploads a file from raw bytes (synchronous)
- `upload_file_from_path(path: str, localPath: str, contentType: str=None) -> None`: Uploads a local file to the controller (synchronous)

## IoService (robot.rws.io)

`from underautomation.abb.rws.services.io_service import IoService`

I/O System Service - Provides access to the I/O resources of the controller: networks, devices and signals. None of these resources is available while the controller runs in bootserver mode.

- `get_resources() -> typing.List[str]`: Gets the names of the I/O sub resources exposed by the controller (synchronous)
- `get_networks() -> typing.List[IoNetworkItem]`: Gets every I/O network defined in the controller (synchronous)
- `get_network(network: str) -> IoNetworkItem`: Gets a single I/O network (synchronous)
- `search_networks(name: str=None, physicalState: IoNetworkPhysicalState | None=None) -> typing.List[IoNetworkItem]`: Searches the I/O networks matching a name and/or a physical state (synchronous)
- `get_network_configuration(network: str) -> IoNetworkConfiguration`: Gets the runtime configuration properties of an I/O network (synchronous)
- `set_network_configuration_type(network: str, configurationType: IoNetworkConfigurationType) -> IoClientAction`: Runs the auto configuration of an I/O network (synchronous)
- `set_network_state(network: str, logicalState: IoNetworkLogicalState) -> None`: Starts or stops an I/O network (synchronous)
- `get_devices() -> typing.List[IoDeviceItem]`: Gets every I/O device defined in the controller (synchronous)
- `get_device(network: str, device: str) -> IoDeviceItem`: Gets a single I/O device, including its input and output data (synchronous)
- `search_devices(name: str=None, logicalState: IoDeviceLogicalState | None=None, network: str=None) -> typing.List[IoDeviceItem]`: Searches the I/O devices matching a name and/or a logical state (synchronous)
- `get_device_configuration(network: str, device: str) -> IoDeviceConfiguration`: Gets the runtime configuration properties of an I/O device (synchronous)
- `get_device_upgrade_info(network: str, device: str) -> IoDeviceUpgradeInfo`: Gets the firmware upgrade status of an I/O device and of each of its modules (synchronous) Only available on a real controller.
- `set_device_state(network: str, device: str, logicalState: IoDeviceLogicalState) -> None`: Enables or disables an I/O device (synchronous)
- `set_device_input_data(network: str, device: str, startByte: int, signalData: int, dataMask: int) -> None`: Writes one byte of the input data of an I/O device (synchronous) Only supported on a virtual controller.
- `set_device_output_data(network: str, device: str, startByte: int, signalData: int, dataMask: int) -> None`: Writes one byte of the output data of an I/O device (synchronous) Only supported on a virtual controller.
- `send_device_command(network: str, device: str, commandName: str, value: str, valueLength: int, timeout: int) -> None`: Sends a command to an I/O device (synchronous) Only available on a real controller.
- `get_signals() -> typing.List[IoSignalItem]`: Gets every I/O signal defined in the controller (synchronous) A controller usually exposes several hundreds of signals. Use to narrow the result down to a network, a device, a category or a signal type.
- `get_signal(network: str, device: str, signal: str) -> IoSignalItem`: Gets a single I/O signal, including its physical value and time stamps (synchronous)
- `get_signal_configuration(network: str, device: str, signal: str) -> IoSignalConfiguration`: Gets the runtime configuration properties of an I/O signal (synchronous)
- `set_signal_value(network: str, device: str, signal: str, value: float, logToEventLog: bool=False) -> None`: Writes the value of an I/O signal (synchronous)
- `set_signal_value_delayed(network: str, device: str, signal: str, value: float, delay: int, logToEventLog: bool=False) -> None`: Writes the value of an I/O signal in "queued delayed" mode (synchronous) The controller queues the write and applies it once the delay has elapsed.
- `invert_signal(network: str, device: str, signal: str, value: float, logToEventLog: bool=False) -> None`: Inverts the value of an I/O signal (synchronous) Only digital and group signals can be inverted.
- `pulse_signal(network: str, device: str, signal: str, value: float, pulses: int, activePulseLength: int | None=None, passivePulseLength: int | None=None, logToEventLog: bool=False) -> None`: Pulses the value of an I/O signal (synchronous) Only digital and group signals can be pulsed.
- `toggle_signal(network: str, device: str, signal: str, value: float, pulses: int, activePulseLength: int | None=None, passivePulseLength: int | None=None, logToEventLog: bool=False) -> None`: Pulses an I/O signal by toggling its current value (synchronous) Only digital and group signals can be toggled.
- `set_signal_state(network: str, device: str, signal: str, simulated: bool) -> None`: Simulates or stops simulating an I/O signal (synchronous) A simulated signal keeps the logical value written by the client and no longer follows its physical value.
- `search_signals(criteria: IoSignalSearchCriteria=None, secondCriteria: IoSignalSearchCriteria=None, start: int | None=None, limit: int | None=None) -> typing.List[IoSignalItem]`: Searches the I/O signals matching the given criteria (synchronous) The returned signals carry their name, type, category, logical value and logical state. Use to also get their physical value, time stamps and write access level.
- `search_signals_extended(criteria: IoSignalSearchCriteria=None, secondCriteria: IoSignalSearchCriteria=None, start: int | None=None, limit: int | None=None) -> typing.List[IoSignalItem]`: Searches the I/O signals matching the given criteria and returns their extended properties (synchronous) In addition to , the returned signals carry their physical value, quality, time stamps and write access level.
- `unblock_signals() -> None`: Removes the simulation of every simulated I/O signal of the controller (synchronous)

## MastershipService (robot.rws.mastership)

`from underautomation.abb.rws.services.mastership_service import MastershipService`

Mastership Service - Takes and gives back the exclusive right to change a domain of the controller. Most write operations are refused unless the client holds the mastership of the domain they belong to: moving a mechanical unit needs , changing the system parameters or the RAPID programs needs .O...

- `get_domains() -> typing.List[MastershipDomain]`: Gets the domains the connected controller can give the mastership of (synchronous)
- `get_info(domain: MastershipDomain) -> MastershipInfo`: Gets who holds the mastership of one domain (synchronous)
- `get_info() -> typing.List[MastershipInfo]`: Gets who holds the mastership of every domain of the controller (synchronous)
- `request(domain: MastershipDomain) -> None`: Takes the mastership of one domain (synchronous)
- `request() -> None`: Takes the mastership of every domain of the controller (synchronous)
- `release(domain: MastershipDomain) -> None`: Gives back the mastership of one domain (synchronous)
- `release() -> None`: Gives back the mastership of every domain of the controller (synchronous)

## MotionSystemService (robot.rws.motion_system)

`from underautomation.abb.rws.services.motion_system_service import MotionSystemService`

Motion System Service - Everything about how the robot stands and how it moves: the mechanical units of the system and their axes, where the tool currently is, the calibration and the revolution counters, jogging, the collision supervision, and the kinematics calculations that convert a pose into...

- `get_calibration_info(mechanicalUnit: str) -> CalibrationInfo`: Gets how each joint of a mechanical unit was calibrated (synchronous)
- `get_motor_calibration_names(mechanicalUnit: str) -> typing.List[MotorCalibrationName]`: Gets the name each joint of a mechanical unit carries, and the name of its calibration data (synchronous)
- `get_smb_data(mechanicalUnit: str) -> SmbData`: Gets the serial measurement board data of a mechanical unit, as held by the controller cabinet and by the robot itself (synchronous) The two copies are meant to agree. When they do not, one of them is written over the other with .
- `set_smb_data(mechanicalUnit: str, direction: SmbDataTransfer) -> None`: Copies one of the two serial measurement board data stores over the other (synchronous)
- `clear_smb_data(mechanicalUnit: str, memory: SmbDataMemory) -> None`: Erases one of the two serial measurement board data stores (synchronous)
- `get_info() -> MotionSystemInfo`: Gets an overview of the motion system: the mechanical unit jogging applies to, the change counter and the payload and accuracy settings (synchronous)
- `has_changed(changeCount: int) -> bool`: Tells whether the motion system changed since it reported the given change count (synchronous) Reading once and asking this afterwards is cheaper than fetching the whole state again to find out that nothing moved.
- `get_error_state() -> MotionSystemErrorState`: Gets the last error the motion system ran into, and how many errors it has counted (synchronous) Most of these errors are raised by a jogging request the controller could not honour, and stay reported until a new one replaces them.
- `get_non_motion_execution_mode() -> bool`: Tells whether the controller runs RAPID programs without moving the robot (synchronous) In that mode the program executes normally but every motion instruction is skipped, which is how a program is tested without the robot leaving its position.
- `set_non_motion_execution_mode(enabled: bool) -> None`: Chooses whether the controller runs RAPID programs without moving the robot (synchronous)
- `get_collision_prediction_mode() -> bool`: Tells whether the controller predicts collisions before they happen (synchronous) Collision prediction stops the robot before it hits something it knows about, where the motion supervision only reacts once the arm meets an unexpected resistance.
- `set_collision_prediction_mode(enabled: bool) -> None`: Switches collision prediction on or off (synchronous)
- `jog(axes: RobotJoints, changeCount: int, incrementMode: JogIncrementMode=JogIncrementMode.None_) -> None`: Moves the mechanical unit currently selected for jogging (synchronous) The unit is the one chose, and how the six values are interpreted depends on its jog mode: axis by axis, along the axes of a coordinate system, and so on.
- `set_jogging_mechanical_unit(mechanicalUnit: str) -> None`: Chooses which mechanical unit the jogging commands apply to (synchronous)
- `set_position_target(target: RobTarget) -> None`: Sends the robot to a cartesian target (synchronous) The position is expressed in millimetres, in the coordinate system currently active for the mechanical unit selected for jogging.
- `get_pose_from_joints(mechanicalUnit: str, toolFrame: Pose, joints: JointTarget, robotHoldsWorkObject: bool=False, logErrors: bool=False) -> RobTarget`: Asks the controller where the tool would be if the robot stood at the given joint values, without moving it there (synchronous)
- `get_joints_from_cartesian(mechanicalUnit: str, pose: Pose, externalAxes: ExternalJoints, toolFrame: Pose, previousJoints: JointTarget, configuration: RobotConfiguration, robotHoldsWorkObject: bool=False, logErrors: bool=False) -> JointTarget`: Asks the controller which joint values put the tool at the given pose, staying close to the joint values the robot is already in (synchronous)
- `get_joints_from_pose(mechanicalUnit: str, pose: Pose, externalAxes: ExternalJoints, toolFrame: Pose, previousJoints: JointTarget, configuration: RobotConfiguration, robotHoldsWorkObject: bool=False, logErrors: bool=False) -> JointTarget`: Asks the controller which joint values put the tool at the given pose (synchronous)
- `get_all_joint_solutions(mechanicalUnit: str, pose: Pose, externalAxes: ExternalJoints, toolFrame: Pose, configuration: RobotConfiguration, robotHoldsWorkObject: bool=False) -> typing.List[JointSolution]`: Asks the controller for every joint combination that puts the tool at the given pose (synchronous) A six axis robot usually reaches the same pose in eight different ways, each one in a different axis configuration.
- `get_mechanical_units() -> typing.List[MechanicalUnitItem]`: Lists the mechanical units of the motion system (synchronous)
- `get_mechanical_unit(mechanicalUnit: str) -> MechanicalUnitInfo`: Gets everything the controller knows about one mechanical unit (synchronous)
- `set_mechanical_unit(mechanicalUnit: str, tool: str=None, workObject: str=None, payload: str=None, totalPayload: str=None, mode: MechanicalUnitMode | None=None, jogMode: JogMode | None=None, coordinateSystem: CoordinateSystem | None=None) -> None`: Changes one or several properties of a mechanical unit (synchronous) Every argument but the unit name is optional; leave the ones you do not want to touch null. At least one of them has to be given.
- `get_axis_count(mechanicalUnit: str) -> int`: Gets how many axes a mechanical unit has (synchronous)
- `get_axis(mechanicalUnit: str, axis: int) -> AxisInfo`: Gets the state of one axis of a mechanical unit (synchronous)
- `get_axis_pose(mechanicalUnit: str, axis: int) -> Pose`: Gets where one axis of a mechanical unit sits (synchronous) The position is expressed in millimetres.
- `set_axis_pose(mechanicalUnit: str, axis: int, pose: Pose) -> None`: Declares where one axis of a mechanical unit sits (synchronous) The position is expressed in millimetres.
- `commutate(mechanicalUnit: str, axis: int) -> None`: Commutates the motor of one axis, which teaches the controller how the rotor of that motor is oriented (synchronous) Needed once after a motor has been replaced, before the axis can be calibrated.
- `synchronize_axis_revolution_counter(mechanicalUnit: str, axis: int) -> None`: Synchronizes the revolution counter of one axis, telling the controller that the axis stands at its synchronization mark (synchronous)
- `update_revolution_counter(mechanicalUnit: str, axis: int) -> None`: Updates the revolution counter of one axis of a mechanical unit (synchronous)
- `fine_calibrate(mechanicalUnit: str, axis: int) -> None`: Fine calibrates one axis of a mechanical unit (synchronous)
- `get_base_frame(mechanicalUnit: str) -> BaseFrame`: Gets where the base of a mechanical unit sits (synchronous) The position is expressed in millimetres.
- `set_base_frame(mechanicalUnit: str, baseFrame: Pose) -> None`: Declares where the base of a mechanical unit sits (synchronous) The position is expressed in millimetres.
- `get_rob_target(mechanicalUnit: str, coordinateSystem: CoordinateSystem=CoordinateSystem.Base, tool: str=None, workObject: str=None) -> RobTarget`: Gets where the tool of a mechanical unit currently is (synchronous) The position is expressed in millimetres.
- `get_cartesian_position(mechanicalUnit: str, coordinateSystem: CoordinateSystem=CoordinateSystem.Base, tool: str=None, workObject: str=None, logErrors: bool=False) -> RobTarget`: Gets where the tool of a mechanical unit currently is, without the external axes (synchronous) The position is expressed in millimetres.
- `get_joint_target(mechanicalUnit: str, alwaysRead: bool=False) -> JointTarget`: Gets the joint values a mechanical unit currently stands at (synchronous) The robot axes are expressed in degrees.
- `get_physical_joints(mechanicalUnit: str) -> RobotJoints`: Gets the physical joint values of a mechanical unit, as its measurement system reads them (synchronous)
- `set_mechanical_unit_position(mechanicalUnit: str, position: JointTarget) -> None`: Places a mechanical unit at the given joint values without moving it there (synchronous) Only a virtual controller accepts this: it teleports the simulated robot, which a real one cannot do.
- `get_lead_through(mechanicalUnit: str) -> LeadThroughStatus`: Tells whether an operator can push the arm of a mechanical unit around by hand (synchronous)
- `set_lead_through(mechanicalUnit: str, active: bool) -> None`: Lets an operator push the arm of a mechanical unit around by hand, or stops letting them (synchronous)
- `get_motion_supervision(mechanicalUnit: str) -> MotionSupervision`: Gets the collision detection settings that apply while a mechanical unit is jogged (synchronous)
- `set_motion_supervision_mode(mechanicalUnit: str, enabled: bool) -> None`: Switches the jogging collision detection of a mechanical unit on or off (synchronous)
- `set_motion_supervision_level(mechanicalUnit: str, sensitivity: int) -> None`: Sets how sensitive the jogging collision detection of a mechanical unit is (synchronous)
- `get_path_supervision(mechanicalUnit: str) -> PathSupervision`: Gets the collision detection settings that apply while a mechanical unit follows a programmed path (synchronous)
- `set_path_supervision_mode(mechanicalUnit: str, enabled: bool) -> None`: Switches the path collision detection of a mechanical unit on or off (synchronous)
- `set_path_supervision_level(mechanicalUnit: str, level: int) -> None`: Sets how sensitive the path collision detection of a mechanical unit is (synchronous)

## PanelService (robot.rws.panel)

`from underautomation.abb.rws.services.panel_service import PanelService`

Panel Service - Exposes what an operator reads and acts on from the control panel of the controller: the controller state, the operating mode and its selector lock, the speed ratio, the collision detection state, the language of the controller and its restart. None of these resources is available...

- `get_controller_state() -> ControllerState`: Gets the state of the controller (synchronous)
- `set_controller_state(state: ControllerState) -> None`: Turns the motors of the robot on or off (synchronous)
- `get_operation_mode() -> OperationMode`: Gets the operating mode the controller runs in (synchronous)
- `acknowledge_operation_mode(acknowledgement: OperationModeAcknowledgement) -> None`: Confirms a pending operating mode change (synchronous) The controller waits for this confirmation whenever the mode selector is turned, unless it is configured to acknowledge the change on its own.
- `get_operation_mode_lock_state() -> OperationModeLockState`: Gets the lock state of the operating mode selector (synchronous)
- `lock_operation_mode(pin: str, permanent: bool=False) -> None`: Locks the operating mode selector with a pin code (synchronous)
- `unlock_operation_mode(pin: str) -> None`: Releases the lock of the operating mode selector (synchronous)
- `get_speed_ratio() -> int`: Gets the speed ratio the controller runs the programs at (synchronous)
- `set_speed_ratio(speedRatio: int, useImplicitMastership: bool=True) -> None`: Sets the speed ratio the controller runs the programs at (synchronous) Only accepted while the controller runs in automatic mode.
- `get_collision_detection_state() -> CollisionDetectionState`: Gets the collision detection state of the controller (synchronous)
- `set_language(languageCode: str) -> None`: Sets the language the controller reports its messages in (synchronous)
- `restart(mode: ControllerRestartMode, useImplicitMastership: bool=True) -> None`: Restarts the controller (synchronous)

## RapidService (robot.rws.rapid)

`from underautomation.abb.rws.services.rapid_service import RapidService`

RAPID Service - Everything about the program the robot runs: the tasks it is split into, the modules and the source they hold, the symbols the program declares and the values they carry, where the program pointer stands, and starting, stopping and stepping the execution. None of these resources i...

- `get_execution_state() -> RapidExecutionInfo`: Gets whether the controller is executing RAPID code, and how many cycles it is set to run (synchronous)
- `start(regain: RapidRegainMode=RapidRegainMode.Continue_, executionMode: RapidExecutionMode=RapidExecutionMode.Continue_, cycle: RapidExecutionCycle=RapidExecutionCycle.Forever, condition: RapidStartCondition=RapidStartCondition.None_, stopAtBreakpoint: bool=False, allTasksBySelection: b...`: Starts executing the RAPID program from where the program pointer stands (synchronous) The controller has to be in automatic mode with the motors on, or in manual mode with the enabling device held. Reset the program pointer first with to start from the beginning.
- `start_from_production_entry() -> None`: Starts executing from the production entry point of the program rather than from where the program pointer stands (synchronous)
- `stop(stopMode: RapidStopMode=RapidStopMode.Stop, scope: RapidTaskScope=RapidTaskScope.Normal) -> None`: Stops the RAPID execution (synchronous)
- `reset_program_pointer() -> None`: Moves the program pointer of every task back to the entry point of its program (synchronous)
- `set_execution_cycle(cycle: RapidExecutionCycle) -> None`: Sets how many times the program runs before stopping (synchronous)
- `set_hold_to_run(state: RapidHoldToRunState) -> None`: Drives the hold-to-run control that lets the program run in manual mode (synchronous) Send to allow execution to start, then about every two seconds to keep it running; the controller stops the program as soon as it stops hearing from the client. Send to stop it at once.
- `get_task_selection() -> typing.List[RapidTaskSelectionItem]`: Gets the task selection panel: which tasks are selected, and which of them an operator is allowed to change the selection of (synchronous)
- `get_alias_io(start: int | None=None, limit: int | None=None) -> typing.List[RapidAliasIoItem]`: Gets the I/O signals a running RAPID program has given an alias to (synchronous)
- `get_modules(task: str) -> typing.List[RapidModuleItem]`: Gets the modules loaded into a task (synchronous)
- `get_module(task: str, module: str) -> RapidModuleInfo`: Gets the file a module came from and the properties declared on it (synchronous)
- `get_module_change_count(task: str, module: str) -> int`: Gets the counter the controller increments whenever a module changes (synchronous) Comparing it with what a previous reading gave is cheaper than fetching the source again to find out that nothing changed.
- `get_module_extension(task: str, module: str) -> RapidModuleExtension`: Gets how many lines and columns the source of a module holds (synchronous) This is what it takes to ask for the whole of it with .
- `get_module_text(task: str, module: str) -> RapidModuleText`: Gets the source of a module (synchronous)
- `set_module_text(task: str, module: str, text: str) -> None`: Replaces the whole source of a module (synchronous)
- `get_module_text_range(task: str, module: str, startRow: int, startColumn: int, endRow: int, endColumn: int) -> str`: Gets a range of the source of a module (synchronous)
- `set_module_text_range(task: str, module: str, replaceMode: RapidTextReplaceMode, queryMode: RapidTextQueryMode, startRow: int, startColumn: int, endRow: int, endColumn: int, text: str) -> RapidSetTextRangeResult`: Writes text into a range of the source of a module (synchronous)
- `search_module_text(task: str, module: str, text: str, startRow: int=1, startColumn: int=1) -> RapidTextPosition`: Finds where a piece of text sits in the source of a module (synchronous)
- `get_sync_pers_status(task: str, module: str) -> bool`: Gets whether the persistent variables of a module are kept synchronized with the other tasks declaring them (synchronous)
- `sync_persistent_variables(task: str, module: str) -> None`: Synchronizes the persistent variables of a module with the other tasks declaring them (synchronous)
- `save_module(task: str, module: str, name: str, path: str) -> None`: Saves a module to the file system of the controller (synchronous)
- `get_possible_module_attributes(task: str, module: str, attributes: typing.List[RapidModuleAttribute]) -> typing.List[RapidModuleAttribute]`: Gets which of the requested properties may be declared on a module (synchronous)
- `get_module_symbol(task: str, module: str, row: int, column: int) -> RapidModuleSymbol`: Gets the declaration the controller finds at a position of a module (synchronous)
- `get_routine(task: str, module: str, row: int, column: int) -> RapidRoutineInfo`: Gets the routine the controller finds called at a position of a module (synchronous)
- `get_routine_arguments(task: str, module: str, row: int, column: int, mark: int | None=None, limit: int | None=None) -> typing.List[RapidRoutineArgument]`: Gets the arguments of the routine call found at a position of a module (synchronous)
- `get_instruction_template(task: str, module: str, name: str, isDataType: bool=False, row: int | None=None, column: int | None=None, parameterNumber: int | None=None, alternativeNumber: int | None=None) -> RapidInstructionTemplate`: Gets the template the controller suggests for an instruction or a data type: the arguments to write and the values to write them with (synchronous) This is what an editor uses to insert a complete, valid instruction rather than a bare keyword.
- `get_object_children(task: str, module: str, startLine: int, startColumn: int, endLine: int, endColumn: int) -> RapidObjectChild`: Gets the parts a RAPID object is made of and where each of them sits in the source (synchronous) Pass the whole span of the object to get its parts; an editor uses this to know where the name, the attributes and the declaration lists of a module begin and end.
- `get_modifiable_positions(task: str, module: str, startRow: int, startColumn: int, endRow: int, endColumn: int) -> RapidModifiablePositions`: Gets how many motion instructions of a range can have their position rewritten to where the robot currently stands (synchronous)
- `get_all_modifiable_positions() -> typing.List[RapidModifiablePositionItem]`: Gets every motion instruction of the system whose position can be rewritten to where the robot currently stands, wherever in whichever task it sits (synchronous)
- `modify_position(task: str, module: str, startRow: int, startColumn: int, endRow: int, endColumn: int, checkLimits: bool=True, checkDeactivatedAxes: bool=True, allowDeactivated: bool=False) -> None`: Rewrites the positions of the motion instructions of a range to where the robot currently stands (synchronous) This is the teaching gesture: jog the robot where it should go, then write that position back into the program.
- `modify_all_positions(checkLimits: bool=True, checkDeactivatedAxes: bool=True) -> None`: Rewrites the positions of every motion instruction of the system that can be rewritten, to where the robot currently stands (synchronous)
- `get_rob_target(task: str, tool: str=None, workObject: str=None) -> RobTarget`: Gets where the tool of a task currently stands, as a position and an orientation (synchronous)
- `get_joint_target(task: str) -> JointTarget`: Gets the joint values of the robot of a task (synchronous)
- `get_external_joint_states(task: str) -> RapidExternalJointStates`: Gets what each of the six external joints of a task is doing (synchronous) This is what says how to read the corresponding value of : a joint reported as not active carries no meaningful position.
- `get_mechanical_units(task: str) -> typing.List[RapidMechanicalUnitItem]`: Gets the mechanical units the positions of a task are expressed in (synchronous)
- `get_program(task: str) -> RapidProgramInfo`: Gets the program loaded into a task (synchronous)
- `load_program(task: str, programPath: str, loadMode: RapidProgramLoadMode=RapidProgramLoadMode.Add) -> None`: Loads a program into a task (synchronous)
- `unload_program(task: str) -> None`: Unloads the program of a task (synchronous)
- `save_program(task: str, path: str) -> None`: Saves the program of a task to the file system of the controller (synchronous)
- `set_program_name(task: str, name: str) -> None`: Renames the program of a task (synchronous)
- `set_entry_point(task: str, routine: str) -> None`: Sets the routine the program pointer moves to when it is reset (synchronous)
- `get_breakpoints(task: str, start: int | None=None, limit: int | None=None) -> typing.List[RapidBreakpoint]`: Gets the breakpoints set in the program of a task (synchronous)
- `set_breakpoint(task: str, module: str, row: int, column: int) -> RapidBreakpoint`: Sets a breakpoint at a position of a module (synchronous)
- `get_build_errors(task: str, start: int | None=None, limit: int | None=None) -> typing.List[RapidBuildError]`: Gets the errors the controller found while linking the program of a task (synchronous)
- `get_program_counter_position(task: str) -> RapidProgramCounterPosition`: Gets which piece of source the program pointer of a task points at (synchronous)
- `get_pointers(task: str) -> RapidPointers`: Gets where the program pointer and the motion pointer of a task stand (synchronous) The program pointer says which instruction runs next, the motion pointer which one the robot is actually executing; they drift apart because the controller plans the path ahead of the movement.
- `set_program_pointer_to_cursor(task: str, module: str, routine: str, row: int, column: int) -> None`: Moves the program pointer of a task to a position of a module (synchronous)
- `set_program_pointer_to_routine(task: str, module: str, routine: str, userLevel: bool=False) -> None`: Moves the program pointer of a task to the beginning of a routine (synchronous)
- `set_program_pointer_to_routine_url(task: str, routineUrl: str, userLevel: bool=False) -> None`: Moves the program pointer of a task to a routine named by its path (synchronous) This is what the paths GetServiceRoutines() reports are for.
- `set_program_pointer_to_next_instruction(task: str) -> None`: Moves the program pointer of a task forward by one instruction (synchronous)
- `set_program_pointer_to_previous_instruction(task: str) -> None`: Moves the program pointer of a task back by one instruction (synchronous)
- `get_symbol_properties(symbolUrl: str) -> RapidSymbolProperties`: Gets what a RAPID symbol is declared as (synchronous)
- `get_symbol_value(symbolUrl: str) -> RapidSymbolValue`: Gets the value of a RAPID symbol and where it is declared (synchronous)
- `set_symbol_value(symbolUrl: str, value: str) -> None`: Sets the value a RAPID symbol currently holds (synchronous)
- `set_symbol_initial_value(symbolUrl: str, value: str) -> None`: Sets the value a RAPID symbol is declared with, which is the one it goes back to when the program is reset (synchronous)
- `search_symbols(criteria: RapidSymbolSearchCriteria) -> typing.List[RapidSymbolProperties]`: Finds the RAPID symbols matching a set of criteria (synchronous)
- `validate_symbol_value(task: str, dataType: str, value: str) -> bool`: Asks the controller whether a value would be accepted for a given RAPID type, without writing it anywhere (synchronous) This is what an editor uses to tell an operator that what they typed is wrong before the write is attempted.
- `get_object_list_extension(symbolUrl: str, type: RapidObjectListType=RapidObjectListType.Statements) -> RapidObjectListExtension`: Gets where one of the lists a RAPID object holds sits in the source: the span of the whole list, and the spans of its first and last elements (synchronous) An editor uses this to jump to the beginning or the end of a list without reading the whole module.
- `get_tasks() -> typing.List[RapidTaskItem]`: Gets every RAPID task of the controller and what each of them is doing (synchronous)
- `get_task(task: str) -> RapidTaskInfo`: Gets everything the controller reports about one task (synchronous)
- `activate_tasks() -> None`: Activates every task of the controller (synchronous)
- `deactivate_tasks() -> None`: Deactivates every task of the controller (synchronous)
- `activate_task(task: str) -> None`: Activates one task (synchronous)
- `deactivate_task(task: str) -> None`: Deactivates one task (synchronous)
- `build_task(task: str) -> None`: Links the program of a task, which is what turns the modules it holds into something runnable (synchronous) Read GetBuildErrors() afterwards to find out what the controller refused.
- `abort_execution_level(task: str) -> None`: Abandons the routine the task is currently running and returns to the level below it (synchronous) This is how a trap or a service routine started by hand is left without stopping the program underneath it.
- `load_module(task: str, modulePath: str, replace: bool=False) -> str`: Loads a module file into a task (synchronous)
- `unload_module(task: str, module: str) -> None`: Unloads a module from a task (synchronous)
- `get_spy_status() -> RapidSpyStatus`: Gets whether the controller is recording the RAPID execution trace to a file (synchronous)
- `start_spy(logFile: str) -> None`: Starts recording the RAPID execution trace into a file (synchronous) The trace names every instruction the controller runs, which is what it takes to find out why a program took a branch it should not have.
- `stop_spy() -> None`: Stops recording the RAPID execution trace (synchronous)
- `get_program_pointer_sync_state() -> RapidPointerSyncState`: Gets whether the program pointers of every task are synchronized with each other (synchronous)
- `get_motion_pointer_sync_state() -> RapidPointerSyncState`: Gets whether the motion pointers of every task are synchronized with each other (synchronous)
- `get_task_program_pointer_sync_state(task: str) -> RapidPointerSyncState`: Gets whether the program pointer of one task is synchronized with the others (synchronous)
- `get_task_motion_pointer_sync_state(task: str) -> RapidPointerSyncState`: Gets whether the motion pointer of one task is synchronized with the others (synchronous)
- `get_structural_change_count(task: str) -> RapidStructuralChangeCount`: Gets the two counters a task keeps of what has changed in it (synchronous) Comparing them with what a previous reading gave is cheaper than fetching the modules again to find out that nothing moved.
- `get_activation_record(task: str, stackFrame: int=1) -> RapidActivationRecord`: Gets one frame of the call stack of a task: which routine is running and where execution stands in it (synchronous)
- `get_service_routines(task: str, start: int | None=None, limit: int | None=None) -> typing.List[RapidServiceRoutineItem]`: Gets the routines of a task the program pointer can be moved to (synchronous)
- `get_preferred_data_types(task: str, instruction: str, parameter: str) -> typing.List[RapidPreferredDataTypeItem]`: Gets the data types the controller suggests for one argument of an instruction (synchronous) An editor uses this to offer only the types that fit where the operator is typing.
- `get_pallet_heads(task: str, start: int | None=None, limit: int | None=None) -> typing.List[RapidPalletHeadItem]`: Gets the categories of the instruction palette an editor offers (synchronous)
- `get_pallet(task: str, palletNumber: int, start: int | None=None, limit: int | None=None) -> typing.List[RapidPalletItem]`: Gets the entries of one category of the instruction palette (synchronous)
- `get_active_ui_instruction() -> RapidUiInstruction`: Gets the dialogue a running RAPID program is currently asking an operator for (synchronous) Answering it means writing its parameters with , addressed by the path this returns.
- `get_ui_instruction_parameters(stackUrl: str) -> typing.List[RapidUiInstructionParameter]`: Gets every parameter of a pending UI instruction: what the program passed in, and what it is waiting for (synchronous)
- `get_ui_instruction_parameter(stackUrl: str, parameter: str) -> str`: Gets the value of one parameter of a pending UI instruction (synchronous)
- `set_ui_instruction_parameter(stackUrl: str, parameter: str, value: str) -> None`: Answers a pending UI instruction by writing one of its parameters (synchronous) An instruction is normally answered by writing the parameter carrying the answer and then the one marking it as completed.

## SystemService (robot.rws.system)

`from underautomation.abb.rws.services.system_service import SystemService`

System Service - Describes the system installed on the controller: its name and software version, the options and the products it was built with, the type of robot it drives, its license, and the energy it consumes. None of these resources is available while the controller runs in bootserver mode.

- `get_info() -> SystemInfo`: Gets the name, the software version and the installed options of the system (synchronous)
- `get_options() -> typing.List[str]`: Gets the options installed on the system (synchronous)
- `get_license() -> str`: Gets the license the robot software runs under (synchronous)
- `get_robot_types() -> typing.List[str]`: Gets the type of every robot the controller drives (synchronous)
- `get_products(name: str=None) -> typing.List[SystemProduct]`: Gets the software products installed on the controller, with their versions (synchronous)
- `get_energy() -> SystemEnergy`: Gets the energy the controller consumed, for the current interval and since the last reset (synchronous)
- `get_energy_change_count() -> int | None`: Gets the counter the controller increments each time a new energy measurement is available (synchronous)
- `reset_accumulated_energy() -> None`: Sets the accumulated energy counter of the controller back to zero (synchronous)
