# Controller: identity, clock & backup

Read controller identity and options, set the clock, the time zone and the network configuration, restart the controller, create and restore backups, read the safety state.

Web page: https://underautomation.com/abb/documentation/rws-controller

`robot.Rws.Controller` gives access to the controller itself, not to the robot program: identity, clock, network, installed options and systems, restart, backups, safety controller and virtual time. Most of these calls work on an IRC5 and on an OmniCore without changing anything in your code.

Some resources only exist on a real controller. When you call them on a RobotStudio virtual controller, the SDK throws an `RwsException` saying that the resource is not implemented, instead of a raw 404.

## Identity and information

`GetInfo` returns a summary of the controller: system time, name, type and level. `GetIdentity` returns the same name plus the controller id and the MAC address of the main network interface.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class ControllerGetIdentity
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // Overview of the controller: system time, name, type and level
        ControllerInfo info = robot.Rws.Controller.GetInfo();
        Console.WriteLine($"{info.Name} ({info.Type}), level {info.Level}");
        Console.WriteLine($"Controller time (UTC) : {info.SystemTime}");

        // Identity of the controller, with its id and its MAC address
        ControllerIdentity identity = robot.Rws.Controller.GetIdentity();
        Console.WriteLine($"Id : {identity.Id}");
        Console.WriteLine($"MAC address : {identity.MacAddress}");

        // Type tells a real controller from a RobotStudio virtual controller
        bool isVirtual = identity.Type == ControllerType.VirtualController;
        Console.WriteLine($"Virtual controller : {isVirtual}");

        // Rename the controller. Only a real controller accepts it.
        robot.Rws.Controller.SetIdentity("CELL_01");

        robot.Disconnect();
    }
}
```

`Type` tells a real controller from a virtual one, which is useful before calling a method that needs real hardware.

| `ControllerType`    | Meaning                                                                                                                      |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `RealController`    | A physical IRC5 or OmniCore cabinet                                                                                          |
| `VirtualController` | A controller running in RobotStudio, see [Test with a RobotStudio virtual controller](virtual-controller.md) |
| `Unknown`           | The controller reported a value the SDK does not know                                                                        |

`SetIdentity` renames the controller. It works only on a real controller. The `id` argument is accepted by RWS 1.0 only, an OmniCore may ignore or refuse it.

`GetEnvironmentVariable` reads a controller environment variable such as `$TEMP` or `$HOME`, with or without the leading dollar sign. It gives the real path behind these names, which is handy before writing a file with the [file system service](rws-files.md).

**Methods of ControllerService** ([reference](../api/UnderAutomation.ABB.Rws.Services.md#controllerservice-robotrwscontroller))

- `string GetEnvironmentVariable(string name)`: Gets the value of a controller environment variable (synchronous)
  - async: `Task<string> GetEnvironmentVariableAsync(string name, CancellationToken cancellationToken = default)`
- `ControllerIdentity GetIdentity()`: Gets the identity of the controller: name, id, type, MAC address and level (synchronous)
  - async: `Task<ControllerIdentity> GetIdentityAsync(CancellationToken cancellationToken = default)`
- `ControllerInfo GetInfo()`: Gets an overview of the controller resources (synchronous) Contains the current system time, the controller identity and the list of available sub resources.
  - async: `Task<ControllerInfo> GetInfoAsync(CancellationToken cancellationToken = default)`
- `void SetIdentity(string name, string id = null)`: Sets the identity of the controller (synchronous) Available only on a real controller.
  - async: `Task SetIdentityAsync(string name, string id = null, CancellationToken cancellationToken = default)`

**ControllerInfo** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#controllerinfo))

- `ControllerInfo()`: Initializes a new instance of the Data.ControllerInfo class
- `ControllerLevel Level { get; set; }`: Indicates whether the controller runs at system level or in bootserver mode
- `string Name { get; set; }`: Name of the controller
- `string[] Resources { get; set; }`: Names of the sub resources exposed by the controller ("clock", "identity", "network", ...)
- `DateTime? SystemTime { get; set; }`: Current system time of the controller (UTC), if available
- `ControllerType Type { get; set; }`: Indicates whether the controller is a real or a virtual controller

**ControllerIdentity** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#controlleridentity))

- `ControllerIdentity()`: Initializes a new instance of the Data.ControllerIdentity class
- `string Id { get; set; }`: Controller id, available only for a real controller
- `ControllerLevel Level { get; set; }`: Indicates whether the controller runs at system level or in bootserver mode
- `string MacAddress { get; set; }`: MAC address of the controller, available only for a real controller
- `string Name { get; set; }`: Name of the controller
- `ControllerType Type { get; set; }`: Indicates whether the controller is a real or a virtual controller

**ControllerType** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#controllertype))

- RealController: Physical robot controller (RC)
- Unknown: The controller type could not be determined
- VirtualController: Virtual controller (VC), for example running in RobotStudio

**ControllerLevel** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#controllerlevel))

- BootLevel: The controller runs the boot application (bootserver mode)
- SystemLevel: A system is loaded and running (system level)
- Unknown: The controller level could not be determined

## Date, time and time server

> **Available on** RWS 1.0 (IRC5) : yes | RWS 2.0 (OmniCore) : yes. Reading a specific time server needs an OmniCore controller

The controller clock is always UTC. `GetClock` returns a UTC `DateTime`, and `SetClock` expects one. The time zone is read and written apart, with the name used by the tz database, for example `Europe/Stockholm`.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class ControllerClock
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // The controller clock is always UTC
        DateTime clock = robot.Rws.Controller.GetClock();
        Console.WriteLine($"Controller time (UTC) : {clock}");

        // Set the clock from the PC time
        robot.Rws.Controller.SetClock(DateTime.UtcNow);

        // Time zone, named as in the tz database
        Console.WriteLine($"Time zone : {robot.Rws.Controller.GetTimeZone()}");
        robot.Rws.Controller.SetTimeZone("Europe/Stockholm");

        // Time server the controller synchronizes its clock with
        robot.Rws.Controller.SetTimeServer("132.163.4.101");

        TimeServerInfo timeServer = robot.Rws.Controller.GetTimeServer();

        // null when no time server is configured
        if (timeServer != null)
        {
            Console.WriteLine($"{timeServer.Address} answers {timeServer.Time}");
        }

        robot.Disconnect();
    }
}
```

Instead of setting the clock from your application, you can give the controller a time server with `SetTimeServer`. `GetTimeServer` returns `null` when no time server is configured. Passing an IP address to `GetTimeServer` queries one specific server, this needs a connection opened as RWS 2.0. On an RWS 1.0 connection the SDK throws instead of quietly returning the default server.

The clock, the time zone and the time server are not settable on a virtual controller.

**Methods of ControllerService** ([reference](../api/UnderAutomation.ABB.Rws.Services.md#controllerservice-robotrwscontroller))

- `DateTime GetClock()`: Gets the current system time of the controller (synchronous) The time returned by the controller is always UTC.
  - async: `Task<DateTime> GetClockAsync(CancellationToken cancellationToken = default)`
- `TimeServerInfo GetTimeServer(string serverIp = null)`: Gets the time server used by the controller to synchronize its clock (synchronous) Available only on a real controller.
  - async: `Task<TimeServerInfo> GetTimeServerAsync(string serverIp = null, CancellationToken cancellationToken = default)`
- `string GetTimeZone()`: Gets the time zone used by the controller (synchronous)
  - async: `Task<string> GetTimeZoneAsync(CancellationToken cancellationToken = default)`
- `void SetClock(DateTime dateTime)`: Sets the system time of the controller (synchronous) The controller clock is always UTC, pass a UTC date and time. Instead of setting the time explicitly, a time server can be configured with SetTimeServer(System.String).
  - async: `Task SetClockAsync(DateTime dateTime, CancellationToken cancellationToken = default)`
- `void SetTimeServer(string timeServer)`: Sets the time server used by the controller to synchronize its clock (synchronous) Available only on a real controller.
  - async: `Task SetTimeServerAsync(string timeServer, CancellationToken cancellationToken = default)`
- `void SetTimeZone(string timeZone)`: Sets the time zone used by the controller (synchronous) Available only on a real controller.
  - async: `Task SetTimeZoneAsync(string timeZone, CancellationToken cancellationToken = default)`

**TimeServerInfo** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#timeserverinfo))

- `TimeServerInfo()`: Initializes a new instance of the Data.TimeServerInfo class
- `string Address { get; set; }`: Address of the time server
- `DateTime? Time { get; set; }`: Time reported by the time server (UTC), if available. Only available when connected with version 2.

## Network

`GetNetworkInterfaces` lists the IP configuration of every network interface of the controller.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class ControllerNetwork
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // IP configuration of every network interface of the controller
        NetworkInterfaceItem[] interfaces = robot.Rws.Controller.GetNetworkInterfaces();

        foreach (NetworkInterfaceItem item in interfaces)
        {
            Console.WriteLine($"{item.Port} {item.LogicalName} : {item.Address} / {item.Mask}");
            Console.WriteLine($"   gateway {item.Gateway}, DHCP {item.DhcpEnabled}");
        }

        // Fixed address on the LAN adapter
        robot.Rws.Controller.SetNetworkConfiguration(NetworkConfigurationMethod.FixIp,
                                                     "192.168.0.10",
                                                     "255.255.255.0",
                                                     "192.168.0.254");

        // Or let a DHCP server give the address
        robot.Rws.Controller.SetNetworkConfiguration(NetworkConfigurationMethod.Dhcp);

        // The new configuration is used after the next restart
        robot.Rws.Controller.Restart(ControllerRestartMode.Restart);

        robot.Disconnect();
    }
}
```

`SetNetworkConfiguration` changes the address of the LAN adapter. **This call can cut you off from the robot.** The controller keeps its current address until the next restart, then answers on the new one. If you set a wrong address or a wrong mask, the only way back is the FlexPendant. The connected user needs the UAS grant to write the controller properties.

| `NetworkConfigurationMethod` | Meaning                                                                  |
| ---------------------------- | ------------------------------------------------------------------------ |
| `FixIp`                      | Fixed address. `address` and `mask` are required, `gateway` is optional. |
| `Dhcp`                       | The address is given by a DHCP server                                    |
| `NoIp`                       | The interface gets no address                                            |

Both methods are refused by a virtual controller.

**Methods of ControllerService** ([reference](../api/UnderAutomation.ABB.Rws.Services.md#controllerservice-robotrwscontroller))

- `NetworkInterfaceItem[] GetNetworkInterfaces()`: Gets the IP configuration of all network interfaces of the controller (synchronous) Not applicable to a virtual controller.
  - async: `Task<NetworkInterfaceItem[]> GetNetworkInterfacesAsync(CancellationToken cancellationToken = default)`
- `void SetNetworkConfiguration(NetworkConfigurationMethod method, string address = null, string mask = null, string gateway = null)`: Sets the IP configuration of the LAN adapter of the controller (synchronous) The controller must be restarted for the change to take effect. Requires the UAS grant UAS_CONTROLLER_PROPERTIES_WRITE. Not supported by a virtual controller.
  - async: `Task SetNetworkConfigurationAsync(NetworkConfigurationMethod method, string address = null, string mask = null, string gateway = null, CancellationToken cancellationToken = default)`

**NetworkInterfaceItem** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#networkinterfaceitem))

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

**NetworkConfigurationMethod** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#networkconfigurationmethod))

- Dhcp: IP address obtained from a DHCP server
- FixIp: Fixed IP address, the address, mask and gateway have to be provided
- NoIp: No IP address configured on the adapter

## Options and installed systems

`HasOption` returns `true` or `false` instead of throwing when the option is missing. The option name is case sensitive, `SAFEMOVEPRO` and not `SafeMovePro`.

```csharp
using UnderAutomation.ABB;

public class ControllerOptions
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // Is an option installed? The name is case sensitive.
        bool hasSafeMove = robot.Rws.Controller.HasOption("SAFEMOVEPRO");
        Console.WriteLine($"SafeMove Pro : {hasSafeMove}");

        // Systems installed on the controller
        string[] systems = robot.Rws.Controller.GetInstalledSystems();
        Console.WriteLine($"Installed systems : {string.Join(", ", systems)}");

        // Value of a controller environment variable
        string temp = robot.Rws.Controller.GetEnvironmentVariable("$TEMP");
        Console.WriteLine($"$TEMP is {temp}");

        // Would this RobotWare version run on this hardware?
        bool compatible = robot.Rws.Controller.IsRobotWareVersionCompatible("6.03.0101");
        Console.WriteLine($"Compatible : {compatible}");

        robot.Disconnect();
    }
}
```

`GetInstalledSystems` returns the names of the systems installed on the controller, and `IsRobotWareVersionCompatible` says whether a given RobotWare version would run on this hardware. Both need a real controller.

`SetLanguage` changes the language the controller writes its messages in, with a code such as `en`, `de` or `sv`. The language must be installed, otherwise the controller answers 400. The same setting is also reachable from the [control panel service](rws-panel.md).

The RobotWare version and the full list of installed options and products are read from the [system service](rws-system.md).

**Methods of ControllerService** ([reference](../api/UnderAutomation.ABB.Rws.Services.md#controllerservice-robotrwscontroller))

- `string[] GetInstalledSystems()`: Gets the names of the systems installed on the controller (synchronous)
  - async: `Task<string[]> GetInstalledSystemsAsync(CancellationToken cancellationToken = default)`
- `bool HasOption(string option)`: Verifies whether an option is present on the controller (synchronous) The option name is case sensitive, for example "SAFEMOVEPRO".
  - async: `Task<bool> HasOptionAsync(string option, CancellationToken cancellationToken = default)`
- `bool IsRobotWareVersionCompatible(string robotWareVersion)`: Checks whether a RobotWare version is compatible with the controller hardware (synchronous) Supported only on a real controller.
  - async: `Task<bool> IsRobotWareVersionCompatibleAsync(string robotWareVersion, CancellationToken cancellationToken = default)`
- `void SetLanguage(string language)`: Sets the language of the controller (synchronous)
  - async: `Task SetLanguageAsync(string language, CancellationToken cancellationToken = default)`

## Restart

**`Restart` stops the robot.** A running RAPID program is interrupted, the motors go off and the controller reboots. Depending on the mode, the RAPID programs or the system settings can also be lost. Do not call it on a production cell without knowing what the mode does.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class ControllerRestart
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // Warm restart of the controller
        robot.Rws.Controller.Restart(ControllerRestartMode.Restart);

        // The controller closes the connection while it reboots
        robot.Disconnect();

        // Try to reconnect until the controller answers again
        while (true)
        {
            try
            {
                robot.Connect("192.168.0.1");
                break;
            }
            catch (Exception)
            {
                Thread.Sleep(5000);
            }
        }

        Console.WriteLine(robot.Rws.Panel.GetControllerState());

        robot.Disconnect();
    }
}
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

**Methods of ControllerService** ([reference](../api/UnderAutomation.ABB.Rws.Services.md#controllerservice-robotrwscontroller))

- `void Restart(ControllerRestartMode mode, bool useImplicitMastership = true)`: Restarts or shuts down the controller (synchronous)
  - async: `Task RestartAsync(ControllerRestartMode mode, bool useImplicitMastership = true, CancellationToken cancellationToken = default)`

**ControllerRestartMode** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#controllerrestartmode))

- BStart: The controller will be restarted. The last automatically saved system state will be loaded. Should be used to recover from a system crash.
- IStart: The controller will be restarted. The current system parameter settings and RAPID programs will be discarded, and the original system installation settings will be used.
- PStart: The controller will be restarted. The current RAPID programs and data will be discarded, but not the system parameter settings.
- Restart: The controller will be restarted. The state is saved and any changed system parameter settings will be activated after the restart.
- Shutdown: The main computer will be shut down. Should be used if the controller UPS is broken.
- XStart: The controller will be restarted and the Boot Application will be started. The current system is saved and deactivated (the controller is non-functional, for advanced maintenance only).

## Backup and restore

A backup is a folder written by the controller on its own file system. Creating one is asynchronous: `CreateBackup` returns as soon as the controller accepts the request, and you follow the progress with `GetBackupState`.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class BackupCreate
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // The controller creates the backup in the background, this call returns immediately
        robot.Rws.Controller.CreateBackup("$temp/mybackup");

        // Poll the state until the controller is done
        BackupState state = robot.Rws.Controller.GetBackupState();

        while (state == BackupState.BackupInProgress)
        {
            Thread.Sleep(1000);
            state = robot.Rws.Controller.GetBackupState();
        }

        if (state != BackupState.BackupReady)
        {
            Console.WriteLine($"The backup failed : {state}");
            return;
        }

        // What the backup contains
        BackupSystemInfo backup = robot.Rws.Controller.GetBackupInfo("$temp/mybackup");
        Console.WriteLine($"{backup.SystemName}, RobotWare {backup.RobotWareVersion}");
        Console.WriteLine($"{backup.OptionCount} option(s) : {string.Join(", ", backup.Options)}");

        robot.Disconnect();
    }
}
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

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class BackupRestore
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // Check the backup before restoring it
        CheckRestoreResult check = robot.Rws.Controller.CheckRestore("$temp/mybackup");

        if (!check.IsAccepted)
        {
            Console.WriteLine($"The backup cannot be restored : {check.Status} {check.Path}");
            return;
        }

        // The controller restarts as soon as the restore is accepted
        robot.Rws.Controller.RestoreBackup("$temp/mybackup");

        // A backup taken on another controller has a different system id.
        // Ignore the mismatch to restore it anyway, and keep the backup folder.
        robot.Rws.Controller.RestoreBackup("$temp/mybackup",
                                           BackupRestoreIgnore.SystemId,
                                           false);

        // Restore only the RAPID modules, not the configuration
        robot.Rws.Controller.RestoreBackup("$temp/mybackup",
                                           BackupRestoreIgnore.All,
                                           true,
                                           true,
                                           true,
                                           BackupRestoreInclude.Modules);

        robot.Disconnect();
    }
}
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

**Methods of ControllerService** ([reference](../api/UnderAutomation.ABB.Rws.Services.md#controllerservice-robotrwscontroller))

- `CheckRestoreResult CheckRestore(string backupPath, BackupRestoreIgnore ignore = BackupRestoreIgnore.None, bool includeControllerSettings = true, bool includeSafetySettings = true, BackupRestoreInclude include = BackupRestoreInclude.All)`: Checks a backup for mismatches and other problems before restoring it (synchronous)
  - async: `Task<CheckRestoreResult> CheckRestoreAsync(string backupPath, BackupRestoreIgnore ignore = BackupRestoreIgnore.None, bool includeControllerSettings = true, bool includeSafetySettings = true, BackupRestoreInclude include = BackupRestoreInclude.All, CancellationToken cancellationToken = default)`
- `void CreateBackup(string backupPath, bool archive = false)`: Creates a backup of the current system on the controller file system (synchronous) The backup is created asynchronously by the controller: this method returns as soon as the request is accepted. Poll ControllerService.GetBackupState to know when the backup is finished. Requires the UAS grant UAS_...
  - async: `Task CreateBackupAsync(string backupPath, bool archive = false, CancellationToken cancellationToken = default)`
- `BackupSystemInfo GetBackupInfo(string backupPath)`: Gets information about a backup stored on the controller file system (synchronous)
  - async: `Task<BackupSystemInfo> GetBackupInfoAsync(string backupPath, CancellationToken cancellationToken = default)`
- `string[] GetBackupResources()`: Gets the names of the backup sub resources exposed by the controller (synchronous)
  - async: `Task<string[]> GetBackupResourcesAsync(CancellationToken cancellationToken = default)`
- `BackupState GetBackupState()`: Gets the state of the backup operation of the controller (synchronous) Used to follow a backup started with String%2cSystem.Boolean).
  - async: `Task<BackupState> GetBackupStateAsync(CancellationToken cancellationToken = default)`
- `void RestoreBackup(string backupPath, BackupRestoreIgnore ignore = BackupRestoreIgnore.None, bool deleteDirectory = true, bool includeControllerSettings = true, bool includeSafetySettings = true, BackupRestoreInclude include = BackupRestoreInclude.All)`: Restores a backup stored on the controller file system (synchronous) When the backup can be restored, the controller restarts. Requires the UAS grant to restore a backup. Use Data.BackupRestoreInclude) first to detect mismatches.
  - async: `Task RestoreBackupAsync(string backupPath, BackupRestoreIgnore ignore = BackupRestoreIgnore.None, bool deleteDirectory = true, bool includeControllerSettings = true, bool includeSafetySettings = true, BackupRestoreInclude include = BackupRestoreInclude.All, CancellationToken cancellationToken = default)`

**BackupSystemInfo** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#backupsysteminfo))

- `BackupSystemInfo()`: Initializes a new instance of the Data.BackupSystemInfo class
- `int OptionCount { get; }`: Number of options installed on the backed up system
- `string[] Options { get; set; }`: Options installed on the backed up system
- `string RobotControlVersion { get; set; }`: RobotControl version of the backed up system. Only available when connected with version 2.
- `string RobotOsVersion { get; set; }`: RobotOS version of the backed up system. Only available when connected with version 2.
- `string RobotWareVersion { get; set; }`: RobotWare version of the backed up system. Only available when connected with version 1.
- `string SystemName { get; set; }`: Name of the backed up system

**BackupState** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#backupstate))

- BackupInProgress: A backup operation is running
- BackupReady: The backup operation finished successfully
- ErrorDuringBackup: The backup operation failed
- InitState: A backup operation has been initialized
- Invalid: The backup state is invalid
- None: No backup operation
- Unknown: The backup state could not be determined

**CheckRestoreResult** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#checkrestoreresult))

- `CheckRestoreResult()`: Initializes a new instance of the Data.CheckRestoreResult class
- `bool IsAccepted { get; }`: Indicates whether the backup can be restored
- `string Path { get; set; }`: File missing or corrupted in the backup, if reported by the controller
- `CheckRestoreStatus Status { get; set; }`: Status of the check

**CheckRestoreStatus** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#checkrestorestatus))

- Accepted: The backup is accepted and can be restored
- ConfigurationDataIncorrect: Error in the configuration data of the backup
- DirectoryNotComplete: The backup directory is not complete
- RestoreMismatchSystemId: The backup was not created from the current system, there might be differences in active options and selected languages
- RestoreMismatchTemplateId: The current system and the backed up system may be generated from different key ids, possibly with different robot types
- Unknown: The status could not be determined

**BackupRestoreIgnore** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#backuprestoreignore))

- All: All mismatches are ignored
- None: No mismatch is ignored
- SystemId: A mismatch between the system id of the backup and the system id of the current system is ignored
- TemplateId: A mismatch between the template id of the backup and the template id of the current system is ignored

**BackupRestoreInclude** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#backuprestoreinclude))

- All: Restore configuration files and RAPID modules
- Cfg: Restore configuration files only
- Modules: Restore RAPID modules only

## Safety

These methods talk to the safety controller. They need the Safety Module option (SafeMove) on the controller and the safety grants on the user account. Without them the controller answers 403, and the SDK throws an `RwsException` that says which of the two is probably missing.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class SafetyStatus
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // Current safety mode of the controller
        SafetyModeStatus mode = robot.Rws.Controller.GetSafetyMode();
        Console.WriteLine($"Safety mode : {mode.Mode}, user data {mode.UserData}");

        // Versions and checksum of the loaded safety configuration
        SafetyConfiguration configuration = robot.Rws.Controller.GetSafetyConfiguration();
        Console.WriteLine($"{configuration.Name} created on {configuration.CreationDate} by {configuration.CreatedBy}");
        Console.WriteLine($"Checksum : {configuration.Checksum}");

        // What the safety controller reports about the last violation
        SafetyViolationInfo violation = robot.Rws.Controller.GetSafetyViolationInfo();
        Console.WriteLine($"{violation.ViolationNumber} violation(s), type {violation.ViolationType}");

        // Cyclic brake check of the drive number 1
        CyclicBrakeCheckStatus brakeCheck = robot.Rws.Controller.GetCyclicBrakeCheckStatus(1);
        Console.WriteLine($"Brake check : {brakeCheck.Status}, last result {brakeCheck.LastBrakeCheckStatus}");

        robot.Disconnect();
    }
}
```

`GetSafetyMode` returns the current mode and the user data that goes with it. `SetSafetyMode` accepts `Active`, `Commissioning` and `Service`. The other values, `ModeError` and `Unknown`, are reported by the controller and cannot be requested. The controller must be in manual mode.

Loading a safety configuration is a two step operation. `GetSafetyLoadOperationStatus` says whether the controller accepts it right now, then `LoadSafetyConfiguration` reads a file that already exists on the controller file system.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class SafetyConfigure
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // A safety configuration can only be loaded in some controller states
        SafetyLoadOperationStatus status = robot.Rws.Controller.GetSafetyLoadOperationStatus();

        if (status == SafetyLoadOperationStatus.Ok)
        {
            // The file is already on the controller file system
            robot.Rws.Controller.LoadSafetyConfiguration("$home/safety.xml");
        }
        else
        {
            Console.WriteLine($"A safety configuration cannot be loaded now : {status}");
        }

        // The controller must be in manual mode to change the safety mode
        robot.Rws.Controller.SetSafetyMode(SafetyMode.Commissioning);

        // Removes the validation information of the current safety configuration
        robot.Rws.Controller.InvalidateSafetyConfiguration();

        robot.Disconnect();
    }
}
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

**Methods of ControllerService** ([reference](../api/UnderAutomation.ABB.Rws.Services.md#controllerservice-robotrwscontroller))

- `CyclicBrakeCheckStatus GetCyclicBrakeCheckStatus(int driveNumber)`: Gets the cyclic brake check status of a mechanical unit (synchronous)
  - async: `Task<CyclicBrakeCheckStatus> GetCyclicBrakeCheckStatusAsync(int driveNumber, CancellationToken cancellationToken = default)`
- `SafetyConfiguration GetSafetyConfiguration()`: Gets the safety supervision configuration of the controller (synchronous)
  - async: `Task<SafetyConfiguration> GetSafetyConfigurationAsync(CancellationToken cancellationToken = default)`
- `SafetyLoadOperationStatus GetSafetyLoadOperationStatus()`: Checks whether a new safety configuration is allowed to be loaded (synchronous) The user must have the safety services privileges.
  - async: `Task<SafetyLoadOperationStatus> GetSafetyLoadOperationStatusAsync(CancellationToken cancellationToken = default)`
- `SafetyModeStatus GetSafetyMode()`: Gets the safety mode of the controller (synchronous)
  - async: `Task<SafetyModeStatus> GetSafetyModeAsync(CancellationToken cancellationToken = default)`
- `string[] GetSafetyResources()`: Gets the names of the safety sub resources exposed by the controller (synchronous)
  - async: `Task<string[]> GetSafetyResourcesAsync(CancellationToken cancellationToken = default)`
- `SafetyViolationInfo GetSafetyViolationInfo()`: Gets the safety violation details reported by the safety controller (synchronous) The user must have the safety services privileges.
  - async: `Task<SafetyViolationInfo> GetSafetyViolationInfoAsync(CancellationToken cancellationToken = default)`
- `void InvalidateSafetyConfiguration()`: Removes the validation information from the safety configuration file (synchronous) Requires the UAS grant UAS_SAFETY_SERVICES.
  - async: `Task InvalidateSafetyConfigurationAsync(CancellationToken cancellationToken = default)`
- `void LoadSafetyConfiguration(string filePath)`: Loads a safety configuration file into the controller (synchronous) The configuration file must already exist on the controller file system. Use ControllerService.GetSafetyLoadOperationStatus to check whether loading is currently allowed.
  - async: `Task LoadSafetyConfigurationAsync(string filePath, CancellationToken cancellationToken = default)`
- `void SetSafetyMode(SafetyMode mode)`: Sets the safety mode of the controller (synchronous) The controller must be in manual mode.
  - async: `Task SetSafetyModeAsync(SafetyMode mode, CancellationToken cancellationToken = default)`

**SafetyModeStatus** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#safetymodestatus))

- `SafetyModeStatus()`: Initializes a new instance of the Data.SafetyModeStatus class
- `SafetyMode Mode { get; set; }`: Current safety mode
- `int? UserData { get; set; }`: User data associated with the safety mode, if reported by the controller

**SafetyMode** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#safetymode))

- Active: The safety configuration is active and supervised
- Commissioning: Commissioning mode, used while configuring the safety controller
- ModeError: The safety controller reports a mode error
- Service: Service mode
- Unknown: The safety mode could not be determined

**SafetyConfiguration** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#safetyconfiguration))

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

**SafetyLoadOperationStatus** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#safetyloadoperationstatus))

- CurrentConfigurationLocked: The current safety configuration is locked (SCORCH_ERR_CURRENT_CONFIG_LOCKED)
- NotInManualMode: The controller is not in manual mode (SCORCH_ERR_NOT_IN_MANUAL_MODE)
- NotInMotorsOff: The motors are not switched off (SCORCH_ERR_NOT_IN_MOTORS_OFF)
- Ok: Loading a new safety configuration is allowed
- OptionNotPresent: The safety option is not present on the controller (SCORCH_ERR_OPTION_NOT_PRESENT)
- Unknown: The status could not be determined
- UserGrantMissing: The user does not have the required grant (SCORCH_ERR_USER_GRANT_IS_MISSING)

**SafetyViolationInfo** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#safetyviolationinfo))

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

**SafetyViolationType** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#safetyviolationtype))

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

**CyclicBrakeCheckStatus** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#cyclicbrakecheckstatus))

- `CyclicBrakeCheckStatus()`: Initializes a new instance of the Data.CyclicBrakeCheckStatus class
- `int DriveNumber { get; set; }`: Drive number of the mechanical unit this status belongs to
- `CyclicBrakeCheckTestStatus LastBrakeCheckStatus { get; set; }`: Result of the last brake check
- `long? NextBrakeCheckTime { get; set; }`: Remaining time before the next brake check is required, if reported by the controller
- `CyclicBrakeCheckState Status { get; set; }`: Current cyclic brake check state

**CyclicBrakeCheckState** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#cyclicbrakecheckstate))

- Ok: No brake check is needed (CBC_STATUS_OK)
- PreWarning: A brake check will soon be required (CBC_STATUS_PREWARNING)
- Required: A brake check is required (CBC_STATUS_REQUIRE_CBC)
- Unknown: The state could not be determined

**CyclicBrakeCheckTestStatus** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#cyclicbrakecheckteststatus))

- Error: The last brake check failed (CBC_TEST_ERROR)
- Ok: The last brake check succeeded (CBC_TEST_OK)
- Undefined: No brake check has been performed yet (CBC_TEST_UNDEFINED)
- Unknown: The test status could not be determined
- Warning: The last brake check ended with a warning (CBC_TEST_WARNING)

## Virtual time

A RobotStudio virtual controller does not run in real time. It runs a simulation clock, the virtual time, that you can slow down, speed up or advance step by step. These methods make sense only on a virtual controller, a real one has no such clock.

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws.Data;

public class ControllerVirtualTime
{
    static void Main()
    {
        AbbController robot = new AbbController();
        robot.Connect("127.0.0.1");

        // Milliseconds elapsed since the virtual controller started
        long virtualTime = robot.Rws.Controller.GetVirtualTime();
        Console.WriteLine($"Virtual time : {virtualTime} ms");

        // 100 is about real time, -1 runs the simulation as fast as possible
        robot.Rws.Controller.SetVirtualTimeSpeed(100);
        Console.WriteLine($"Speed : {robot.Rws.Controller.GetVirtualTimeSpeed()} %");

        // Duration of one step, 10 ms minimum
        robot.Rws.Controller.SetVirtualTimeSlice(50);
        Console.WriteLine($"Time slice : {robot.Rws.Controller.GetVirtualTimeSlice()} ms");

        // Run the virtual time one step at a time
        robot.Rws.Controller.SetVirtualTimeState(VirtualTimeState.RunSlice);
        robot.Rws.Controller.RunVirtualTime();

        VirtualTimeState state = robot.Rws.Controller.GetVirtualTimeState();
        Console.WriteLine($"State : {state}");

        // Let the simulation run freely again
        robot.Rws.Controller.SetVirtualTimeState(VirtualTimeState.FreeRun);

        robot.Disconnect();
    }
}
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

**Methods of ControllerService** ([reference](../api/UnderAutomation.ABB.Rws.Services.md#controllerservice-robotrwscontroller))

- `long GetVirtualTime()`: Gets the current value of the virtual time, in milliseconds (synchronous) The virtual time is zeroed when the virtual controller starts. Supported only on a virtual controller.
  - async: `Task<long> GetVirtualTimeAsync(CancellationToken cancellationToken = default)`
- `string[] GetVirtualTimeResources()`: Gets the names of the virtual time sub resources exposed by the controller (synchronous) Supported only on a virtual controller.
  - async: `Task<string[]> GetVirtualTimeResourcesAsync(CancellationToken cancellationToken = default)`
- `int GetVirtualTimeSlice()`: Gets the time slice of the virtual controller, in milliseconds (synchronous) Supported only on a virtual controller.
  - async: `Task<int> GetVirtualTimeSliceAsync(CancellationToken cancellationToken = default)`
- `int GetVirtualTimeSpeed()`: Gets the speed of the virtual time, in percent relative to real time (synchronous) -1 means full speed. Supported only on a virtual controller.
  - async: `Task<int> GetVirtualTimeSpeedAsync(CancellationToken cancellationToken = default)`
- `VirtualTimeState GetVirtualTimeState()`: Gets the state of the virtual time server (synchronous) Supported only on a virtual controller.
  - async: `Task<VirtualTimeState> GetVirtualTimeStateAsync(CancellationToken cancellationToken = default)`
- `void RunVirtualTime()`: Executes the virtual time according to the current state of the virtual time server (synchronous) Supported only on a virtual controller.
  - async: `Task RunVirtualTimeAsync(CancellationToken cancellationToken = default)`
- `void SetVirtualTimeSlice(int milliseconds)`: Sets the time slice of the virtual controller, in milliseconds (synchronous) The minimum value is 10 ms, lower values are replaced by the controller with the default value of 10 ms. Supported only on a virtual controller.
  - async: `Task SetVirtualTimeSliceAsync(int milliseconds, CancellationToken cancellationToken = default)`
- `void SetVirtualTimeSpeed(int speed)`: Sets the speed of the virtual time, in percent relative to real time (synchronous) 100 makes the virtual time run approximately at real time speed, -1 runs it as fast as possible. Supported only on a virtual controller.
  - async: `Task SetVirtualTimeSpeedAsync(int speed, CancellationToken cancellationToken = default)`
- `void SetVirtualTimeState(VirtualTimeState state)`: Sets the state of the virtual time server (synchronous) Supported only on a virtual controller.
  - async: `Task SetVirtualTimeStateAsync(VirtualTimeState state, CancellationToken cancellationToken = default)`

**VirtualTimeState** ([reference](../api/UnderAutomation.ABB.Rws.Data.md#virtualtimestate))

- FreeRun: Virtual time runs freely (VTFREERUN)
- NextEvent: Virtual time runs until the next event (VTNEXTEVENT)
- RunSlice: Virtual time runs one time slice at a time (VTRUNSLICE)
- Stop: Virtual time is stopped (VTSTOP)
- Unknown: The state could not be determined

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).
