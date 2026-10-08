# Controller: identity, clock & backup

Read controller identity and options, set the clock, the time zone and the network configuration, restart the controller, create and restore backups, read the safety state.

Web page: https://underautomation.com/abb/documentation/rws-controller

`robot.Rws.Controller` gives access to the controller itself, not to the robot program: identity, clock, network, installed options and systems, restart, backups, safety controller and virtual time. Most of these calls work on an IRC5 and on an OmniCore without changing anything in your code.

Some resources only exist on a real controller. When you call them on a RobotStudio virtual controller, the SDK throws an `RwsException` saying that the resource is not implemented, instead of a raw 404.

## Identity and information

`GetInfo` returns a summary of the controller: system time, name, type and level. `GetIdentity` returns the same name plus the controller id and the MAC address of the main network interface.

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.controller_type import ControllerType

robot = AbbController()
robot.connect("192.168.0.1")

# Overview of the controller: system time, name, type and level
info = robot.rws.controller.get_info()
print(f"{info.name} ({info.type}), level {info.level}")
print(f"Controller time (UTC) : {info.system_time}")

# Identity of the controller, with its id and its MAC address
identity = robot.rws.controller.get_identity()
print(f"Id : {identity.id}")
print(f"MAC address : {identity.mac_address}")

# The type tells a real controller from a RobotStudio virtual controller
is_virtual = identity.type == ControllerType.VirtualController
print(f"Virtual controller : {is_virtual}")

# Rename the controller. Only a real controller accepts it.
robot.rws.controller.set_identity("CELL_01")

robot.disconnect()
```

`Type` tells a real controller from a virtual one, which is useful before calling a method that needs real hardware.

| `ControllerType`    | Meaning                                                                                                                      |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `RealController`    | A physical IRC5 or OmniCore cabinet                                                                                          |
| `VirtualController` | A controller running in RobotStudio, see [Test with a RobotStudio virtual controller](virtual-controller.md) |
| `Unknown`           | The controller reported a value the SDK does not know                                                                        |

`SetIdentity` renames the controller. It works only on a real controller. The `id` argument is accepted by RWS 1.0 only, an OmniCore may ignore or refuse it.

`GetEnvironmentVariable` reads a controller environment variable such as `$TEMP` or `$HOME`, with or without the leading dollar sign. It gives the real path behind these names, which is handy before writing a file with the [file system service](rws-files.md).

**Methods of ControllerService** ([reference](../api/underautomation.abb.rws.services.md#controllerservice-robotrwscontroller))

- `get_identity() -> ControllerIdentity`: Gets the identity of the controller: name, id, type, MAC address and level (synchronous)
- `set_identity(name: str, id: str=None) -> None`: Sets the identity of the controller (synchronous) Available only on a real controller.

**ControllerInfo** ([reference](../api/underautomation.abb.rws.data.md#controllerinfo))

- `ControllerInfo()`: Initializes a new instance of the ControllerInfo class
- `system_time: datetime | None`: Current system time of the controller (UTC), if available
- `name: str`: Name of the controller
- `type: ControllerType`: Indicates whether the controller is a real or a virtual controller
- `level: ControllerLevel`: Indicates whether the controller runs at system level or in bootserver mode
- `resources: typing.List[str]`: Names of the sub resources exposed by the controller ("clock", "identity", "network", ...)

**ControllerIdentity** ([reference](../api/underautomation.abb.rws.data.md#controlleridentity))

- `ControllerIdentity()`: Initializes a new instance of the ControllerIdentity class
- `name: str`: Name of the controller
- `id: str`: Controller id, available only for a real controller
- `type: ControllerType`: Indicates whether the controller is a real or a virtual controller
- `mac_address: str`: MAC address of the controller, available only for a real controller
- `level: ControllerLevel`: Indicates whether the controller runs at system level or in bootserver mode

**ControllerType** ([reference](../api/underautomation.abb.rws.data.md#controllertype))

- Unknown: The controller type could not be determined
- RealController: Physical robot controller (RC)
- VirtualController: Virtual controller (VC), for example running in RobotStudio

**ControllerLevel** ([reference](../api/underautomation.abb.rws.data.md#controllerlevel))

- Unknown: The controller level could not be determined
- SystemLevel: A system is loaded and running (system level)
- BootLevel: The controller runs the boot application (bootserver mode)

## Date, time and time server

> **Available on** RWS 1.0 (IRC5) : yes | RWS 2.0 (OmniCore) : yes. Reading a specific time server needs an OmniCore controller

The controller clock is always UTC. `GetClock` returns a UTC `DateTime`, and `SetClock` expects one. The time zone is read and written apart, with the name used by the tz database, for example `Europe/Stockholm`.

```python
from datetime import datetime

from underautomation.abb.abb_controller import AbbController

robot = AbbController()
robot.connect("192.168.0.1")

# The controller clock is always UTC
clock = robot.rws.controller.get_clock()
print(f"Controller time (UTC) : {clock}")

# Set the clock from the PC time
robot.rws.controller.set_clock(datetime.utcnow())

# Time zone, named as in the tz database
print(f"Time zone : {robot.rws.controller.get_time_zone()}")
robot.rws.controller.set_time_zone("Europe/Stockholm")

# Time server the controller synchronizes its clock with
robot.rws.controller.set_time_server("132.163.4.101")

time_server = robot.rws.controller.get_time_server()

# None when no time server is configured
if time_server is not None:
    print(f"{time_server.address} answers {time_server.time}")

robot.disconnect()
```

Instead of setting the clock from your application, you can give the controller a time server with `SetTimeServer`. `GetTimeServer` returns `null` when no time server is configured. Passing an IP address to `GetTimeServer` queries one specific server, this needs a connection opened as RWS 2.0. On an RWS 1.0 connection the SDK throws instead of quietly returning the default server.

The clock, the time zone and the time server are not settable on a virtual controller.

**Methods of ControllerService** ([reference](../api/underautomation.abb.rws.services.md#controllerservice-robotrwscontroller))

- `get_clock() -> datetime`: Gets the current system time of the controller (synchronous) The time returned by the controller is always UTC.
- `set_clock(dateTime: datetime) -> None`: Sets the system time of the controller (synchronous) The controller clock is always UTC, pass a UTC date and time.Instead of setting the time explicitly, a time server can be configured with .

**TimeServerInfo** ([reference](../api/underautomation.abb.rws.data.md#timeserverinfo))

- `TimeServerInfo()`: Initializes a new instance of the TimeServerInfo class
- `address: str`: Address of the time server
- `time: datetime | None`: Time reported by the time server (UTC), if available. Only available when connected with version 2.

## Network

`GetNetworkInterfaces` lists the IP configuration of every network interface of the controller.

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.controller_restart_mode import ControllerRestartMode
from underautomation.abb.rws.data.network_configuration_method import NetworkConfigurationMethod

robot = AbbController()
robot.connect("192.168.0.1")

# IP configuration of every network interface of the controller
interfaces = robot.rws.controller.get_network_interfaces()

for item in interfaces:
    print(f"{item.port} {item.logical_name} : {item.address} / {item.mask}")
    print(f"   gateway {item.gateway}, DHCP {item.dhcp_enabled}")

# Fixed address on the LAN adapter
robot.rws.controller.set_network_configuration(NetworkConfigurationMethod.FixIp,
                                               "192.168.0.10",
                                               "255.255.255.0",
                                               "192.168.0.254")

# Or let a DHCP server give the address
robot.rws.controller.set_network_configuration(NetworkConfigurationMethod.Dhcp)

# The new configuration is used after the next restart
robot.rws.controller.restart(ControllerRestartMode.Restart)

robot.disconnect()
```

`SetNetworkConfiguration` changes the address of the LAN adapter. **This call can cut you off from the robot.** The controller keeps its current address until the next restart, then answers on the new one. If you set a wrong address or a wrong mask, the only way back is the FlexPendant. The connected user needs the UAS grant to write the controller properties.

| `NetworkConfigurationMethod` | Meaning                                                                  |
| ---------------------------- | ------------------------------------------------------------------------ |
| `FixIp`                      | Fixed address. `address` and `mask` are required, `gateway` is optional. |
| `Dhcp`                       | The address is given by a DHCP server                                    |
| `NoIp`                       | The interface gets no address                                            |

Both methods are refused by a virtual controller.

**Methods of ControllerService** ([reference](../api/underautomation.abb.rws.services.md#controllerservice-robotrwscontroller))

- `get_network_interfaces() -> typing.List[NetworkInterfaceItem]`: Gets the IP configuration of all network interfaces of the controller (synchronous) Not applicable to a virtual controller.
- `set_network_configuration(method: NetworkConfigurationMethod, address: str=None, mask: str=None, gateway: str=None) -> None`: Sets the IP configuration of the LAN adapter of the controller (synchronous) The controller must be restarted for the change to take effect. Requires the UAS grant UAS_CONTROLLER_PROPERTIES_WRITE.Not supported by a virtual controller.

**NetworkInterfaceItem** ([reference](../api/underautomation.abb.rws.data.md#networkinterfaceitem))

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

**NetworkConfigurationMethod** ([reference](../api/underautomation.abb.rws.data.md#networkconfigurationmethod))

- FixIp: Fixed IP address, the address, mask and gateway have to be provided
- Dhcp: IP address obtained from a DHCP server
- NoIp: No IP address configured on the adapter

## Options and installed systems

`HasOption` returns `true` or `false` instead of throwing when the option is missing. The option name is case sensitive, `SAFEMOVEPRO` and not `SafeMovePro`.

```python
from underautomation.abb.abb_controller import AbbController

robot = AbbController()
robot.connect("192.168.0.1")

# Is an option installed? The name is case sensitive.
has_safe_move = robot.rws.controller.has_option("SAFEMOVEPRO")
print(f"SafeMove Pro : {has_safe_move}")

# Systems installed on the controller
systems = robot.rws.controller.get_installed_systems()
print("Installed systems : " + ", ".join(systems))

# Value of a controller environment variable
temp = robot.rws.controller.get_environment_variable("$TEMP")
print(f"$TEMP is {temp}")

# Would this RobotWare version run on this hardware?
compatible = robot.rws.controller.is_robot_ware_version_compatible("6.03.0101")
print(f"Compatible : {compatible}")

robot.disconnect()
```

`GetInstalledSystems` returns the names of the systems installed on the controller, and `IsRobotWareVersionCompatible` says whether a given RobotWare version would run on this hardware. Both need a real controller.

`SetLanguage` changes the language the controller writes its messages in, with a code such as `en`, `de` or `sv`. The language must be installed, otherwise the controller answers 400. The same setting is also reachable from the [control panel service](rws-panel.md).

The RobotWare version and the full list of installed options and products are read from the [system service](rws-system.md).



## Restart

**`Restart` stops the robot.** A running RAPID program is interrupted, the motors go off and the controller reboots. Depending on the mode, the RAPID programs or the system settings can also be lost. Do not call it on a production cell without knowing what the mode does.

```python
import time

from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.controller_restart_mode import ControllerRestartMode

robot = AbbController()
robot.connect("192.168.0.1")

# Warm restart of the controller
robot.rws.controller.restart(ControllerRestartMode.Restart)

# The controller closes the connection while it reboots
robot.disconnect()

# Try to reconnect until the controller answers again
while True:
    try:
        robot.connect("192.168.0.1")
        break
    except Exception:
        time.sleep(5)

print(robot.rws.panel.get_controller_state())

robot.disconnect()
```

| `ControllerRestartMode` | What the controller does                                                              |
| ----------------------- | ------------------------------------------------------------------------------------- |
| `Restart`               | Warm restart. The system and the RAPID programs are kept.                             |
| `Shutdown`              | The controller stops and stays off. Someone has to power it on again.                 |
| `IStart`                | The system restarts with its default settings                                         |
| `PStart`                | The system restarts and the RAPID programs are removed                                |
| `BStart`                | The system restarts from the state stored at the last shutdown                        |
| `XStart`                | The controller restarts to the boot application, where another system can be selected |

The request returns as soon as the controller accepts it. The connection is then lost, and every following request fails until the controller is up again. Call `Disconnect`, wait, and connect again.

On an OmniCore, the restart needs the mastership on all domains. The SDK takes it for you, this is what the `useImplicitMastership` argument does. Set it to `false` when you already hold the [mastership](rws-mastership.md). An IRC5 needs no mastership here and ignores the argument.

The [control panel service](rws-panel.md) also has a `Restart` method, with the same modes.

**Methods of ControllerService** ([reference](../api/underautomation.abb.rws.services.md#controllerservice-robotrwscontroller))

- `restart(mode: ControllerRestartMode, useImplicitMastership: bool=True) -> None`: Restarts or shuts down the controller (synchronous)

**ControllerRestartMode** ([reference](../api/underautomation.abb.rws.data.md#controllerrestartmode))

- Restart: The controller will be restarted. The state is saved and any changed system parameter settings will be activated after the restart.
- Shutdown: The main computer will be shut down. Should be used if the controller UPS is broken.
- XStart: The controller will be restarted and the Boot Application will be started. The current system is saved and deactivated (the controller is non-functional, for advanced maintenance only).
- IStart: The controller will be restarted. The current system parameter settings and RAPID programs will be discarded, and the original system installation settings will be used.
- PStart: The controller will be restarted. The current RAPID programs and data will be discarded, but not the system parameter settings.
- BStart: The controller will be restarted. The last automatically saved system state will be loaded. Should be used to recover from a system crash.

## Backup and restore

A backup is a folder written by the controller on its own file system. Creating one is asynchronous: `CreateBackup` returns as soon as the controller accepts the request, and you follow the progress with `GetBackupState`.

```python
import time

from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.backup_state import BackupState

robot = AbbController()
robot.connect("192.168.0.1")

# The controller creates the backup in the background, this call returns immediately
robot.rws.controller.create_backup("$temp/mybackup")

# Poll the state until the controller is done
state = robot.rws.controller.get_backup_state()

while state == BackupState.BackupInProgress:
    time.sleep(1)
    state = robot.rws.controller.get_backup_state()

if state != BackupState.BackupReady:
    print(f"The backup failed : {state}")
    raise SystemExit(1)

# What the backup contains
backup = robot.rws.controller.get_backup_info("$temp/mybackup")
print(f"{backup.system_name}, RobotWare {backup.robot_ware_version}")
print("Options : " + ", ".join(backup.options))

robot.disconnect()
```

The destination path must be on the controller file system. Environment variables are allowed, `$temp/mybackup` or `~temp/mybackup` both work. The folder must not exist yet, and it cannot be created under `$HOME`. Creating a backup can stop the RAPID execution, so do not do it in the middle of a production cycle. The connected user needs the backup grant.

| `BackupState`                             | Meaning                              |
| ----------------------------------------- | ------------------------------------ |
| `BackupInProgress`                        | The controller is writing the backup |
| `BackupReady`                             | The last backup finished correctly   |
| `ErrorDuringBackup`                       | The last backup failed               |
| `None`, `InitState`, `Invalid`, `Unknown` | No usable backup state is reported   |

`GetBackupInfo` reads the content of a backup folder without restoring it: system name, RobotWare version and the options the backed up system was built with.

To copy the backup on your PC, download the files with the [file system service](rws-files.md). A complete example is given in [Backup & restore a controller](backup-restore-controller.md).

### Restore

**`RestoreBackup` replaces the current system and restarts the controller.** The RAPID programs, the configuration and, when asked, the safety settings of the running system are overwritten. Check the backup first with `CheckRestore`, which reports the mismatches without touching anything.

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.backup_restore_ignore import BackupRestoreIgnore
from underautomation.abb.rws.data.backup_restore_include import BackupRestoreInclude

robot = AbbController()
robot.connect("192.168.0.1")

# Check the backup before restoring it
check = robot.rws.controller.check_restore("$temp/mybackup")

if not check.is_accepted:
    print(f"The backup cannot be restored : {check.status} {check.path}")
    raise SystemExit(1)

# The controller restarts as soon as the restore is accepted
robot.rws.controller.restore_backup("$temp/mybackup")

# A backup taken on another controller has a different system id.
# Ignore the mismatch to restore it anyway, and keep the backup folder.
robot.rws.controller.restore_backup("$temp/mybackup",
                                    BackupRestoreIgnore.SystemId,
                                    False)

# Restore only the RAPID modules, not the configuration
robot.rws.controller.restore_backup("$temp/mybackup",
                                    BackupRestoreIgnore.All,
                                    True,
                                    True,
                                    True,
                                    BackupRestoreInclude.Modules)

robot.disconnect()
```

| `CheckRestoreStatus`         | Meaning                                                  |
| ---------------------------- | -------------------------------------------------------- |
| `Accepted`                   | The backup can be restored as it is                      |
| `RestoreMismatchSystemId`    | The backup comes from another controller                 |
| `RestoreMismatchTemplateId`  | The backup was made from another system template         |
| `DirectoryNotComplete`       | The backup folder misses files, `Path` names one of them |
| `ConfigurationDataIncorrect` | A configuration file of the backup cannot be read        |

`BackupRestoreIgnore` says which mismatches are accepted anyway: `None`, `SystemId`, `TemplateId` or `All`. `BackupRestoreInclude` limits what is restored: `All`, `Cfg` for the configuration only, or `Modules` for the RAPID modules only.

`includeControllerSettings` is used by RobotWare 6. RobotWare 7 does not restore the controller settings and ignores the flag.

`GetBackupResources` returns the names of the backup sub resources the controller exposes. It is mainly useful to know what this particular controller supports.

**Methods of ControllerService** ([reference](../api/underautomation.abb.rws.services.md#controllerservice-robotrwscontroller))

- `get_backup_resources() -> typing.List[str]`: Gets the names of the backup sub resources exposed by the controller (synchronous)
- `get_backup_info(backupPath: str) -> BackupSystemInfo`: Gets information about a backup stored on the controller file system (synchronous)
- `get_backup_state() -> BackupState`: Gets the state of the backup operation of the controller (synchronous) Used to follow a backup started with .
- `create_backup(backupPath: str, archive: bool=False) -> None`: Creates a backup of the current system on the controller file system (synchronous) The backup is created asynchronously by the controller: this method returns as soon as the request is accepted. Poll to know when the backup is finished.Requires the UAS grant UAS_BACKUP. Creating a backup may affe...
- `restore_backup(backupPath: str, ignore: BackupRestoreIgnore=BackupRestoreIgnore.None_, deleteDirectory: bool=True, includeControllerSettings: bool=True, includeSafetySettings: bool=True, include: BackupRestoreInclude=BackupRestoreInclude.All) -> None`: Restores a backup stored on the controller file system (synchronous) When the backup can be restored, the controller restarts.Requires the UAS grant to restore a backup. Use first to detect mismatches.
- `check_restore(backupPath: str, ignore: BackupRestoreIgnore=BackupRestoreIgnore.None_, includeControllerSettings: bool=True, includeSafetySettings: bool=True, include: BackupRestoreInclude=BackupRestoreInclude.All) -> CheckRestoreResult`: Checks a backup for mismatches and other problems before restoring it (synchronous)

**BackupSystemInfo** ([reference](../api/underautomation.abb.rws.data.md#backupsysteminfo))

- `BackupSystemInfo()`: Initializes a new instance of the BackupSystemInfo class
- `system_name: str`: Name of the backed up system
- `robot_ware_version: str`: RobotWare version of the backed up system. Only available when connected with version 1.
- `robot_control_version: str`: RobotControl version of the backed up system. Only available when connected with version 2.
- `robot_os_version: str`: RobotOS version of the backed up system. Only available when connected with version 2.
- `options: typing.List[str]`: Options installed on the backed up system
- `option_count: int (read only)`: Number of options installed on the backed up system

**BackupState** ([reference](../api/underautomation.abb.rws.data.md#backupstate))

- Unknown: The backup state could not be determined
- None_: No backup operation
- InitState: A backup operation has been initialized
- BackupInProgress: A backup operation is running
- BackupReady: The backup operation finished successfully
- ErrorDuringBackup: The backup operation failed
- Invalid: The backup state is invalid

**CheckRestoreResult** ([reference](../api/underautomation.abb.rws.data.md#checkrestoreresult))

- `CheckRestoreResult()`: Initializes a new instance of the CheckRestoreResult class
- `status: CheckRestoreStatus`: Status of the check
- `is_accepted: bool (read only)`: Indicates whether the backup can be restored
- `path: str`: File missing or corrupted in the backup, if reported by the controller

**CheckRestoreStatus** ([reference](../api/underautomation.abb.rws.data.md#checkrestorestatus))

- Unknown: The status could not be determined
- Accepted: The backup is accepted and can be restored
- RestoreMismatchSystemId: The backup was not created from the current system, there might be differences in active options and selected languages
- RestoreMismatchTemplateId: The current system and the backed up system may be generated from different key ids, possibly with different robot types
- DirectoryNotComplete: The backup directory is not complete
- ConfigurationDataIncorrect: Error in the configuration data of the backup

**BackupRestoreIgnore** ([reference](../api/underautomation.abb.rws.data.md#backuprestoreignore))

- None_: No mismatch is ignored
- All: All mismatches are ignored
- SystemId: A mismatch between the system id of the backup and the system id of the current system is ignored
- TemplateId: A mismatch between the template id of the backup and the template id of the current system is ignored

**BackupRestoreInclude** ([reference](../api/underautomation.abb.rws.data.md#backuprestoreinclude))

- All: Restore configuration files and RAPID modules
- Cfg: Restore configuration files only
- Modules: Restore RAPID modules only

## Safety

These methods talk to the safety controller. They need the Safety Module option (SafeMove) on the controller and the safety grants on the user account. Without them the controller answers 403, and the SDK throws an `RwsException` that says which of the two is probably missing.

```python
from underautomation.abb.abb_controller import AbbController

robot = AbbController()
robot.connect("192.168.0.1")

# Current safety mode of the controller
mode = robot.rws.controller.get_safety_mode()
print(f"Safety mode : {mode.mode}, user data {mode.user_data}")

# Versions and checksum of the loaded safety configuration
configuration = robot.rws.controller.get_safety_configuration()
print(f"{configuration.name} created on {configuration.creation_date} by {configuration.created_by}")
print(f"Checksum : {configuration.checksum}")

# What the safety controller reports about the last violation
violation = robot.rws.controller.get_safety_violation_info()
print(f"{violation.violation_number} violations, type {violation.violation_type}")

# Cyclic brake check of the drive number 1
brake_check = robot.rws.controller.get_cyclic_brake_check_status(1)
print(f"Brake check : {brake_check.status}, last result {brake_check.last_brake_check_status}")

robot.disconnect()
```

`GetSafetyMode` returns the current mode and the user data that goes with it. `SetSafetyMode` accepts `Active`, `Commissioning` and `Service`. The other values, `ModeError` and `Unknown`, are reported by the controller and cannot be requested. The controller must be in manual mode.

Loading a safety configuration is a two step operation. `GetSafetyLoadOperationStatus` says whether the controller accepts it right now, then `LoadSafetyConfiguration` reads a file that already exists on the controller file system.

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.safety_load_operation_status import SafetyLoadOperationStatus
from underautomation.abb.rws.data.safety_mode import SafetyMode

robot = AbbController()
robot.connect("192.168.0.1")

# A safety configuration can only be loaded in some controller states
status = robot.rws.controller.get_safety_load_operation_status()

if status == SafetyLoadOperationStatus.Ok:
    # The file is already on the controller file system
    robot.rws.controller.load_safety_configuration("$home/safety.xml")
else:
    print(f"A safety configuration cannot be loaded now : {status}")

# The controller must be in manual mode to change the safety mode
robot.rws.controller.set_safety_mode(SafetyMode.Commissioning)

# Removes the validation information of the current safety configuration
robot.rws.controller.invalidate_safety_configuration()

robot.disconnect()
```

| `SafetyLoadOperationStatus`  | Why loading is refused                 |
| ---------------------------- | -------------------------------------- |
| `Ok`                         | A configuration can be loaded          |
| `OptionNotPresent`           | The safety option is not installed     |
| `NotInManualMode`            | The controller is not in manual mode   |
| `NotInMotorsOff`             | The motors are on                      |
| `CurrentConfigurationLocked` | The configuration in use is locked     |
| `UserGrantMissing`           | The connected user has no safety grant |

`InvalidateSafetyConfiguration` removes the validation information of the configuration file. **After that the safety configuration has to be validated again before the robot can run.**

`GetCyclicBrakeCheckStatus` takes the drive number of a mechanical unit and returns when the next brake check is due and how the last one ended. `GetSafetyViolationInfo` gives the details of the last violation seen by the safety controller.

**Methods of ControllerService** ([reference](../api/underautomation.abb.rws.services.md#controllerservice-robotrwscontroller))

- `get_safety_resources() -> typing.List[str]`: Gets the names of the safety sub resources exposed by the controller (synchronous)
- `get_safety_mode() -> SafetyModeStatus`: Gets the safety mode of the controller (synchronous)
- `set_safety_mode(mode: SafetyMode) -> None`: Sets the safety mode of the controller (synchronous) The controller must be in manual mode.
- `get_safety_configuration() -> SafetyConfiguration`: Gets the safety supervision configuration of the controller (synchronous)
- `load_safety_configuration(filePath: str) -> None`: Loads a safety configuration file into the controller (synchronous) The configuration file must already exist on the controller file system.Use to check whether loading is currently allowed.
- `invalidate_safety_configuration() -> None`: Removes the validation information from the safety configuration file (synchronous) Requires the UAS grant UAS_SAFETY_SERVICES.
- `get_safety_load_operation_status() -> SafetyLoadOperationStatus`: Checks whether a new safety configuration is allowed to be loaded (synchronous) The user must have the safety services privileges.
- `get_safety_violation_info() -> SafetyViolationInfo`: Gets the safety violation details reported by the safety controller (synchronous) The user must have the safety services privileges.

**SafetyModeStatus** ([reference](../api/underautomation.abb.rws.data.md#safetymodestatus))

- `SafetyModeStatus()`: Initializes a new instance of the SafetyModeStatus class
- `mode: SafetyMode`: Current safety mode
- `user_data: int | None`: User data associated with the safety mode, if reported by the controller

**SafetyMode** ([reference](../api/underautomation.abb.rws.data.md#safetymode))

- Unknown: The safety mode could not be determined
- Active: The safety configuration is active and supervised
- Commissioning: Commissioning mode, used while configuring the safety controller
- Service: Service mode
- ModeError: The safety controller reports a mode error

**SafetyConfiguration** ([reference](../api/underautomation.abb.rws.data.md#safetyconfiguration))

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

**SafetyLoadOperationStatus** ([reference](../api/underautomation.abb.rws.data.md#safetyloadoperationstatus))

- Unknown: The status could not be determined
- Ok: Loading a new safety configuration is allowed
- OptionNotPresent: The safety option is not present on the controller (SCORCH_ERR_OPTION_NOT_PRESENT)
- NotInManualMode: The controller is not in manual mode (SCORCH_ERR_NOT_IN_MANUAL_MODE)
- NotInMotorsOff: The motors are not switched off (SCORCH_ERR_NOT_IN_MOTORS_OFF)
- CurrentConfigurationLocked: The current safety configuration is locked (SCORCH_ERR_CURRENT_CONFIG_LOCKED)
- UserGrantMissing: The user does not have the required grant (SCORCH_ERR_USER_GRANT_IS_MISSING)

**SafetyViolationInfo** ([reference](../api/underautomation.abb.rws.data.md#safetyviolationinfo))

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

**SafetyViolationType** ([reference](../api/underautomation.abb.rws.data.md#safetyviolationtype))

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

**CyclicBrakeCheckStatus** ([reference](../api/underautomation.abb.rws.data.md#cyclicbrakecheckstatus))

- `CyclicBrakeCheckStatus()`: Initializes a new instance of the CyclicBrakeCheckStatus class
- `drive_number: int`: Drive number of the mechanical unit this status belongs to
- `next_brake_check_time: int | None`: Remaining time before the next brake check is required, if reported by the controller
- `last_brake_check_status: CyclicBrakeCheckTestStatus`: Result of the last brake check
- `status: CyclicBrakeCheckState`: Current cyclic brake check state

**CyclicBrakeCheckState** ([reference](../api/underautomation.abb.rws.data.md#cyclicbrakecheckstate))

- Unknown: The state could not be determined
- Ok: No brake check is needed (CBC_STATUS_OK)
- PreWarning: A brake check will soon be required (CBC_STATUS_PREWARNING)
- Required: A brake check is required (CBC_STATUS_REQUIRE_CBC)

**CyclicBrakeCheckTestStatus** ([reference](../api/underautomation.abb.rws.data.md#cyclicbrakecheckteststatus))

- Unknown: The test status could not be determined
- Ok: The last brake check succeeded (CBC_TEST_OK)
- Warning: The last brake check ended with a warning (CBC_TEST_WARNING)
- Error: The last brake check failed (CBC_TEST_ERROR)
- Undefined: No brake check has been performed yet (CBC_TEST_UNDEFINED)

## Virtual time

A RobotStudio virtual controller does not run in real time. It runs a simulation clock, the virtual time, that you can slow down, speed up or advance step by step. These methods make sense only on a virtual controller, a real one has no such clock.

```python
from underautomation.abb.abb_controller import AbbController
from underautomation.abb.rws.data.virtual_time_state import VirtualTimeState

robot = AbbController()
robot.connect("127.0.0.1")

# Milliseconds elapsed since the virtual controller started
virtual_time = robot.rws.controller.get_virtual_time()
print(f"Virtual time : {virtual_time} ms")

# 100 is about real time, -1 runs the simulation as fast as possible
robot.rws.controller.set_virtual_time_speed(100)
print(f"Speed : {robot.rws.controller.get_virtual_time_speed()} %")

# Duration of one step, 10 ms minimum
robot.rws.controller.set_virtual_time_slice(50)
print(f"Time slice : {robot.rws.controller.get_virtual_time_slice()} ms")

# Run the virtual time one step at a time
robot.rws.controller.set_virtual_time_state(VirtualTimeState.RunSlice)
robot.rws.controller.run_virtual_time()

state = robot.rws.controller.get_virtual_time_state()
print(f"State : {state}")

# Let the simulation run freely again
robot.rws.controller.set_virtual_time_state(VirtualTimeState.FreeRun)

robot.disconnect()
```

`GetVirtualTime` returns the milliseconds elapsed since the virtual controller started. `GetVirtualTimeSpeed` and `SetVirtualTimeSpeed` work in percent of the real time: `100` is about real time, `-1` runs the simulation as fast as the PC can. The time slice is the duration of one step, 10 ms minimum.

| `VirtualTimeState` | Meaning                                                                       |
| ------------------ | ----------------------------------------------------------------------------- |
| `Stop`             | The virtual time does not advance                                             |
| `FreeRun`          | The virtual time runs continuously                                            |
| `RunSlice`         | Each call to `RunVirtualTime` advances the clock by one time slice            |
| `NextEvent`        | Each call to `RunVirtualTime` advances the clock to the next controller event |
| `Unknown`          | The controller reported a value the SDK does not know                         |

`Unknown` is only returned by `GetVirtualTimeState`, it cannot be set. `RunVirtualTime` executes the virtual time according to the current state, so it is used with `RunSlice` and `NextEvent`.

Running a simulation faster than real time makes tests shorter, but the robot then reacts faster than your application. Read [Test with a RobotStudio virtual controller](virtual-controller.md) before using it in automated tests.



**VirtualTimeState** ([reference](../api/underautomation.abb.rws.data.md#virtualtimestate))

- Unknown: The state could not be determined
- Stop: Virtual time is stopped (VTSTOP)
- FreeRun: Virtual time runs freely (VTFREERUN)
- RunSlice: Virtual time runs one time slice at a time (VTRUNSLICE)
- NextEvent: Virtual time runs until the next event (VTNEXTEVENT)

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).
