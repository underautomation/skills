# UnderAutomation.ABB.Rws.Services

## ControllerService (robot.Rws.Controller)

`class ControllerService`

Controller Service - Provides access to the controller resources: clock, identity, network, installed systems, options, backups, safety controller and virtual time.

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
- `DateTime GetClock()`: Gets the current system time of the controller (synchronous) The time returned by the controller is always UTC.
  - async: `Task<DateTime> GetClockAsync(CancellationToken cancellationToken = default)`
- `CyclicBrakeCheckStatus GetCyclicBrakeCheckStatus(int driveNumber)`: Gets the cyclic brake check status of a mechanical unit (synchronous)
  - async: `Task<CyclicBrakeCheckStatus> GetCyclicBrakeCheckStatusAsync(int driveNumber, CancellationToken cancellationToken = default)`
- `string GetEnvironmentVariable(string name)`: Gets the value of a controller environment variable (synchronous)
  - async: `Task<string> GetEnvironmentVariableAsync(string name, CancellationToken cancellationToken = default)`
- `ControllerIdentity GetIdentity()`: Gets the identity of the controller: name, id, type, MAC address and level (synchronous)
  - async: `Task<ControllerIdentity> GetIdentityAsync(CancellationToken cancellationToken = default)`
- `ControllerInfo GetInfo()`: Gets an overview of the controller resources (synchronous) Contains the current system time, the controller identity and the list of available sub resources.
  - async: `Task<ControllerInfo> GetInfoAsync(CancellationToken cancellationToken = default)`
- `string[] GetInstalledSystems()`: Gets the names of the systems installed on the controller (synchronous)
  - async: `Task<string[]> GetInstalledSystemsAsync(CancellationToken cancellationToken = default)`
- `NetworkInterfaceItem[] GetNetworkInterfaces()`: Gets the IP configuration of all network interfaces of the controller (synchronous) Not applicable to a virtual controller.
  - async: `Task<NetworkInterfaceItem[]> GetNetworkInterfacesAsync(CancellationToken cancellationToken = default)`
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
- `TimeServerInfo GetTimeServer(string serverIp = null)`: Gets the time server used by the controller to synchronize its clock (synchronous) Available only on a real controller.
  - async: `Task<TimeServerInfo> GetTimeServerAsync(string serverIp = null, CancellationToken cancellationToken = default)`
- `string GetTimeZone()`: Gets the time zone used by the controller (synchronous)
  - async: `Task<string> GetTimeZoneAsync(CancellationToken cancellationToken = default)`
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
- `bool HasOption(string option)`: Verifies whether an option is present on the controller (synchronous) The option name is case sensitive, for example "SAFEMOVEPRO".
  - async: `Task<bool> HasOptionAsync(string option, CancellationToken cancellationToken = default)`
- `void InvalidateSafetyConfiguration()`: Removes the validation information from the safety configuration file (synchronous) Requires the UAS grant UAS_SAFETY_SERVICES.
  - async: `Task InvalidateSafetyConfigurationAsync(CancellationToken cancellationToken = default)`
- `bool IsRobotWareVersionCompatible(string robotWareVersion)`: Checks whether a RobotWare version is compatible with the controller hardware (synchronous) Supported only on a real controller.
  - async: `Task<bool> IsRobotWareVersionCompatibleAsync(string robotWareVersion, CancellationToken cancellationToken = default)`
- `void LoadSafetyConfiguration(string filePath)`: Loads a safety configuration file into the controller (synchronous) The configuration file must already exist on the controller file system. Use ControllerService.GetSafetyLoadOperationStatus to check whether loading is currently allowed.
  - async: `Task LoadSafetyConfigurationAsync(string filePath, CancellationToken cancellationToken = default)`
- `void Restart(ControllerRestartMode mode, bool useImplicitMastership = true)`: Restarts or shuts down the controller (synchronous)
  - async: `Task RestartAsync(ControllerRestartMode mode, bool useImplicitMastership = true, CancellationToken cancellationToken = default)`
- `void RestoreBackup(string backupPath, BackupRestoreIgnore ignore = BackupRestoreIgnore.None, bool deleteDirectory = true, bool includeControllerSettings = true, bool includeSafetySettings = true, BackupRestoreInclude include = BackupRestoreInclude.All)`: Restores a backup stored on the controller file system (synchronous) When the backup can be restored, the controller restarts. Requires the UAS grant to restore a backup. Use Data.BackupRestoreInclude) first to detect mismatches.
  - async: `Task RestoreBackupAsync(string backupPath, BackupRestoreIgnore ignore = BackupRestoreIgnore.None, bool deleteDirectory = true, bool includeControllerSettings = true, bool includeSafetySettings = true, BackupRestoreInclude include = BackupRestoreInclude.All, CancellationToken cancellationToken = default)`
- `void RunVirtualTime()`: Executes the virtual time according to the current state of the virtual time server (synchronous) Supported only on a virtual controller.
  - async: `Task RunVirtualTimeAsync(CancellationToken cancellationToken = default)`
- `void SetClock(DateTime dateTime)`: Sets the system time of the controller (synchronous) The controller clock is always UTC, pass a UTC date and time. Instead of setting the time explicitly, a time server can be configured with SetTimeServer(System.String).
  - async: `Task SetClockAsync(DateTime dateTime, CancellationToken cancellationToken = default)`
- `void SetIdentity(string name, string id = null)`: Sets the identity of the controller (synchronous) Available only on a real controller.
  - async: `Task SetIdentityAsync(string name, string id = null, CancellationToken cancellationToken = default)`
- `void SetLanguage(string language)`: Sets the language of the controller (synchronous)
  - async: `Task SetLanguageAsync(string language, CancellationToken cancellationToken = default)`
- `void SetNetworkConfiguration(NetworkConfigurationMethod method, string address = null, string mask = null, string gateway = null)`: Sets the IP configuration of the LAN adapter of the controller (synchronous) The controller must be restarted for the change to take effect. Requires the UAS grant UAS_CONTROLLER_PROPERTIES_WRITE. Not supported by a virtual controller.
  - async: `Task SetNetworkConfigurationAsync(NetworkConfigurationMethod method, string address = null, string mask = null, string gateway = null, CancellationToken cancellationToken = default)`
- `void SetSafetyMode(SafetyMode mode)`: Sets the safety mode of the controller (synchronous) The controller must be in manual mode.
  - async: `Task SetSafetyModeAsync(SafetyMode mode, CancellationToken cancellationToken = default)`
- `void SetTimeServer(string timeServer)`: Sets the time server used by the controller to synchronize its clock (synchronous) Available only on a real controller.
  - async: `Task SetTimeServerAsync(string timeServer, CancellationToken cancellationToken = default)`
- `void SetTimeZone(string timeZone)`: Sets the time zone used by the controller (synchronous) Available only on a real controller.
  - async: `Task SetTimeZoneAsync(string timeZone, CancellationToken cancellationToken = default)`
- `void SetVirtualTimeSlice(int milliseconds)`: Sets the time slice of the virtual controller, in milliseconds (synchronous) The minimum value is 10 ms, lower values are replaced by the controller with the default value of 10 ms. Supported only on a virtual controller.
  - async: `Task SetVirtualTimeSliceAsync(int milliseconds, CancellationToken cancellationToken = default)`
- `void SetVirtualTimeSpeed(int speed)`: Sets the speed of the virtual time, in percent relative to real time (synchronous) 100 makes the virtual time run approximately at real time speed, -1 runs it as fast as possible. Supported only on a virtual controller.
  - async: `Task SetVirtualTimeSpeedAsync(int speed, CancellationToken cancellationToken = default)`
- `void SetVirtualTimeState(VirtualTimeState state)`: Sets the state of the virtual time server (synchronous) Supported only on a virtual controller.
  - async: `Task SetVirtualTimeStateAsync(VirtualTimeState state, CancellationToken cancellationToken = default)`

## ElogService (robot.Rws.Elog)

`class ElogService`

Event Log Service - Provides access to the messages the controller logs: the list of the log domains, the messages they hold, and the operations that clear them or dump them to a file. None of these resources is available while the controller runs in bootserver mode.

- `void ClearAllMessages()`: Deletes every message of every event log domain (synchronous)
  - async: `Task ClearAllMessagesAsync(CancellationToken cancellationToken = default)`
- `void ClearMessages(int domain)`: Deletes every message of one event log domain (synchronous)
  - async: `Task ClearMessagesAsync(int domain, CancellationToken cancellationToken = default)`
- `ElogDomain GetDomain(int domain)`: Gets the number of messages one event log domain holds and the number it can hold (synchronous)
  - async: `Task<ElogDomain> GetDomainAsync(int domain, CancellationToken cancellationToken = default)`
- `ElogDomain[] GetDomains(string language = null)`: Gets every event log domain of the controller, with the number of messages each one holds (synchronous)
  - async: `Task<ElogDomain[]> GetDomainsAsync(string language = null, CancellationToken cancellationToken = default)`
- `ElogMessage GetMessage(int domain, int sequenceNumber, string language = null)`: Gets one message of an event log domain (synchronous)
  - async: `Task<ElogMessage> GetMessageAsync(int domain, int sequenceNumber, string language = null, CancellationToken cancellationToken = default)`
- `ElogMessage GetMessageBySequenceNumber(int sequenceNumber, string language = null)`: Gets one message from its sequence number alone, without naming the domain it belongs to (synchronous)
  - async: `Task<ElogMessage> GetMessageBySequenceNumberAsync(int sequenceNumber, string language = null, CancellationToken cancellationToken = default)`
- `ElogMessage[] GetMessageTitles(int domain, string language, ElogMessageOrder order = ElogMessageOrder.NewestFirst, int? maxCount = null)`: Gets the messages held by one event log domain, with their short text only (synchronous)
  - async: `Task<ElogMessage[]> GetMessageTitlesAsync(int domain, string language, ElogMessageOrder order = ElogMessageOrder.NewestFirst, int? maxCount = null, CancellationToken cancellationToken = default)`
- `ElogMessage[] GetMessages(int domain, ElogMessageOrder order = ElogMessageOrder.NewestFirst, string language = null, int? maxCount = null)`: Gets the messages held by one event log domain (synchronous)
  - async: `Task<ElogMessage[]> GetMessagesAsync(int domain, ElogMessageOrder order = ElogMessageOrder.NewestFirst, string language = null, int? maxCount = null, CancellationToken cancellationToken = default)`
- `void SaveInSystemDumpFormat(string path)`: Asks the controller to write the whole event log to one file on its own file system (synchronous)
  - async: `Task SaveInSystemDumpFormatAsync(string path, CancellationToken cancellationToken = default)`

## FileService (robot.Rws.File)

`class FileService`

File Service - Provides access to the robot controller file system Compatibility: Version 1: directory operations with basic functionalityVersion 2: extended file operations

- `void CopyDirectory(string path, string newName, bool overwrite)`: Copies a directory (synchronous)
  - async: `Task CopyDirectoryAsync(string path, string newName, bool overwrite, CancellationToken cancellationToken = default)`
- `void CopyFile(string path, string newName, bool overwrite)`: Copies a file (synchronous)
  - async: `Task CopyFileAsync(string path, string newName, bool overwrite, CancellationToken cancellationToken = default)`
- `void CreateDirectory(string path, string newName)`: Creates a new directory (synchronous) The newName parameter can contain nested directory structure (e.g. "parentdir/subdir") which will create both directories if they don't exist.
  - async: `Task CreateDirectoryAsync(string path, string newName, CancellationToken cancellationToken = default)`
- `void DeleteDirectory(string path)`: Deletes a directory and all its subdirectories and files (synchronous)
  - async: `Task DeleteDirectoryAsync(string path, CancellationToken cancellationToken = default)`
- `void DeleteFile(string path)`: Deletes a file (synchronous)
  - async: `Task DeleteFileAsync(string path, CancellationToken cancellationToken = default)`
- `byte[] GetFileAsBytes(string path)`: Gets file content as raw bytes (synchronous)
  - async: `Task<byte[]> GetFileAsBytesAsync(string path, CancellationToken cancellationToken = default)`
- `Stream GetFileAsReadonlyStream(string path)`: Gets file content as a read-only stream (synchronous) For sync: Returns a read-only MemoryStream (buffered for .NET 3.5/4.0 compatibility) For true HTTP streaming with large files, use GetFileAsReadonlyStreamAsync() instead
  - async: `Task<Stream> GetFileAsReadonlyStreamAsync(string path, CancellationToken cancellationToken = default)`
- `string GetFileAsText(string path, Encoding encoding = null)`: Gets file content as text (synchronous)
  - async: `Task<string> GetFileAsTextAsync(string path, Encoding encoding = null, CancellationToken cancellationToken = default)`
- `void GetFileToDestination(string path, string localPath)`: Downloads a file to a local path (synchronous)
  - async: `Task GetFileToDestinationAsync(string path, string localPath, CancellationToken cancellationToken = default)`
- `DirectoryListing ListDirectory(string path)`: Lists contents of a directory resource (synchronous) Environment variables (e.g. $home, $temp) and devices are treated as directories. When listing the root path ("/", null, or "\\"), the response includes available devices in DirectoryListing.Devices. The complete content is always returned, how...
  - async: `Task<DirectoryListing> ListDirectoryAsync(string path, CancellationToken cancellationToken = default)`
- `void RenameDirectory(string path, string newName)`: Renames a directory (synchronous)
  - async: `Task RenameDirectoryAsync(string path, string newName, CancellationToken cancellationToken = default)`
- `void RenameFile(string path, string newName)`: Renames a file (synchronous)
  - async: `Task RenameFileAsync(string path, string newName, CancellationToken cancellationToken = default)`
- `void UploadFileFromBytes(string path, byte[] content, string contentType = null)`: Uploads a file from raw bytes (synchronous)
  - async: `Task UploadFileFromBytesAsync(string path, byte[] content, string contentType = null, CancellationToken cancellationToken = default)`
- `void UploadFileFromPath(string path, string localPath, string contentType = null)`: Uploads a local file to the controller (synchronous)
  - async: `Task UploadFileFromPathAsync(string path, string localPath, string contentType = null, CancellationToken cancellationToken = default)`
- `void UploadFileFromStream(string path, Stream contentStream, string contentType = null)`: Uploads a file from a stream (synchronous)
  - async: `Task UploadFileFromStreamAsync(string path, Stream contentStream, string contentType = null, CancellationToken cancellationToken = default)`
- `void UploadFileFromText(string path, string content, Encoding encoding = null)`: Uploads a file from text (synchronous)
  - async: `Task UploadFileFromTextAsync(string path, string content, Encoding encoding = null, CancellationToken cancellationToken = default)`

## IoService (robot.Rws.Io)

`class IoService`

I/O System Service - Provides access to the I/O resources of the controller: networks, devices and signals. None of these resources is available while the controller runs in bootserver mode.

- `IoDeviceItem GetDevice(string network, string device)`: Gets a single I/O device, including its input and output data (synchronous)
  - async: `Task<IoDeviceItem> GetDeviceAsync(string network, string device, CancellationToken cancellationToken = default)`
- `IoDeviceConfiguration GetDeviceConfiguration(string network, string device)`: Gets the runtime configuration properties of an I/O device (synchronous)
  - async: `Task<IoDeviceConfiguration> GetDeviceConfigurationAsync(string network, string device, CancellationToken cancellationToken = default)`
- `IoDeviceUpgradeInfo GetDeviceUpgradeInfo(string network, string device)`: Gets the firmware upgrade status of an I/O device and of each of its modules (synchronous) Only available on a real controller.
  - async: `Task<IoDeviceUpgradeInfo> GetDeviceUpgradeInfoAsync(string network, string device, CancellationToken cancellationToken = default)`
- `IoDeviceItem[] GetDevices()`: Gets every I/O device defined in the controller (synchronous)
  - async: `Task<IoDeviceItem[]> GetDevicesAsync(CancellationToken cancellationToken = default)`
- `IoNetworkItem GetNetwork(string network)`: Gets a single I/O network (synchronous)
  - async: `Task<IoNetworkItem> GetNetworkAsync(string network, CancellationToken cancellationToken = default)`
- `IoNetworkConfiguration GetNetworkConfiguration(string network)`: Gets the runtime configuration properties of an I/O network (synchronous)
  - async: `Task<IoNetworkConfiguration> GetNetworkConfigurationAsync(string network, CancellationToken cancellationToken = default)`
- `IoNetworkItem[] GetNetworks()`: Gets every I/O network defined in the controller (synchronous)
  - async: `Task<IoNetworkItem[]> GetNetworksAsync(CancellationToken cancellationToken = default)`
- `string[] GetResources()`: Gets the names of the I/O sub resources exposed by the controller (synchronous)
  - async: `Task<string[]> GetResourcesAsync(CancellationToken cancellationToken = default)`
- `IoSignalItem GetSignal(string network, string device, string signal)`: Gets a single I/O signal, including its physical value and time stamps (synchronous)
  - async: `Task<IoSignalItem> GetSignalAsync(string network, string device, string signal, CancellationToken cancellationToken = default)`
- `IoSignalConfiguration GetSignalConfiguration(string network, string device, string signal)`: Gets the runtime configuration properties of an I/O signal (synchronous)
  - async: `Task<IoSignalConfiguration> GetSignalConfigurationAsync(string network, string device, string signal, CancellationToken cancellationToken = default)`
- `IoSignalItem[] GetSignals()`: Gets every I/O signal defined in the controller (synchronous) A controller usually exposes several hundreds of signals. Use Nullable%7bSystem.Int32%7d) to narrow the result down to a network, a device, a category or a signal type.
  - async: `Task<IoSignalItem[]> GetSignalsAsync(CancellationToken cancellationToken = default)`
- `void InvertSignal(string network, string device, string signal, float value, bool logToEventLog = false)`: Inverts the value of an I/O signal (synchronous) Only digital and group signals can be inverted.
  - async: `Task InvertSignalAsync(string network, string device, string signal, float value, bool logToEventLog = false, CancellationToken cancellationToken = default)`
- `void PulseSignal(string network, string device, string signal, float value, int pulses, int? activePulseLength = null, int? passivePulseLength = null, bool logToEventLog = false)`: Pulses the value of an I/O signal (synchronous) Only digital and group signals can be pulsed.
  - async: `Task PulseSignalAsync(string network, string device, string signal, float value, int pulses, int? activePulseLength = null, int? passivePulseLength = null, bool logToEventLog = false, CancellationToken cancellationToken = default)`
- `IoDeviceItem[] SearchDevices(string name = null, IoDeviceLogicalState? logicalState = null, string network = null)`: Searches the I/O devices matching a name and/or a logical state (synchronous)
  - async: `Task<IoDeviceItem[]> SearchDevicesAsync(string name = null, IoDeviceLogicalState? logicalState = null, string network = null, CancellationToken cancellationToken = default)`
- `IoNetworkItem[] SearchNetworks(string name = null, IoNetworkPhysicalState? physicalState = null)`: Searches the I/O networks matching a name and/or a physical state (synchronous)
  - async: `Task<IoNetworkItem[]> SearchNetworksAsync(string name = null, IoNetworkPhysicalState? physicalState = null, CancellationToken cancellationToken = default)`
- `IoSignalItem[] SearchSignals(IoSignalSearchCriteria criteria = null, IoSignalSearchCriteria secondCriteria = null, int? start = null, int? limit = null)`: Searches the I/O signals matching the given criteria (synchronous) The returned signals carry their name, type, category, logical value and logical state. Use Nullable%7bSystem.Int32%7d) to also get their physical value, time stamps and write access level.
  - async: `Task<IoSignalItem[]> SearchSignalsAsync(IoSignalSearchCriteria criteria = null, IoSignalSearchCriteria secondCriteria = null, int? start = null, int? limit = null, CancellationToken cancellationToken = default)`
- `IoSignalItem[] SearchSignalsExtended(IoSignalSearchCriteria criteria = null, IoSignalSearchCriteria secondCriteria = null, int? start = null, int? limit = null)`: Searches the I/O signals matching the given criteria and returns their extended properties (synchronous) In addition to Nullable%7bSystem.Int32%7d), the returned signals carry their physical value, quality, time stamps and write access level.
  - async: `Task<IoSignalItem[]> SearchSignalsExtendedAsync(IoSignalSearchCriteria criteria = null, IoSignalSearchCriteria secondCriteria = null, int? start = null, int? limit = null, CancellationToken cancellationToken = default)`
- `void SendDeviceCommand(string network, string device, string commandName, string value, int valueLength, int timeout)`: Sends a command to an I/O device (synchronous) Only available on a real controller.
  - async: `Task SendDeviceCommandAsync(string network, string device, string commandName, string value, int valueLength, int timeout, CancellationToken cancellationToken = default)`
- `void SetDeviceInputData(string network, string device, int startByte, int signalData, int dataMask)`: Writes one byte of the input data of an I/O device (synchronous) Only supported on a virtual controller.
  - async: `Task SetDeviceInputDataAsync(string network, string device, int startByte, int signalData, int dataMask, CancellationToken cancellationToken = default)`
- `void SetDeviceOutputData(string network, string device, int startByte, int signalData, int dataMask)`: Writes one byte of the output data of an I/O device (synchronous) Only supported on a virtual controller.
  - async: `Task SetDeviceOutputDataAsync(string network, string device, int startByte, int signalData, int dataMask, CancellationToken cancellationToken = default)`
- `void SetDeviceState(string network, string device, IoDeviceLogicalState logicalState)`: Enables or disables an I/O device (synchronous)
  - async: `Task SetDeviceStateAsync(string network, string device, IoDeviceLogicalState logicalState, CancellationToken cancellationToken = default)`
- `IoClientAction SetNetworkConfigurationType(string network, IoNetworkConfigurationType configurationType)`: Runs the auto configuration of an I/O network (synchronous)
  - async: `Task<IoClientAction> SetNetworkConfigurationTypeAsync(string network, IoNetworkConfigurationType configurationType, CancellationToken cancellationToken = default)`
- `void SetNetworkState(string network, IoNetworkLogicalState logicalState)`: Starts or stops an I/O network (synchronous)
  - async: `Task SetNetworkStateAsync(string network, IoNetworkLogicalState logicalState, CancellationToken cancellationToken = default)`
- `void SetSignalState(string network, string device, string signal, bool simulated)`: Simulates or stops simulating an I/O signal (synchronous) A simulated signal keeps the logical value written by the client and no longer follows its physical value.
  - async: `Task SetSignalStateAsync(string network, string device, string signal, bool simulated, CancellationToken cancellationToken = default)`
- `void SetSignalValue(string network, string device, string signal, float value, bool logToEventLog = false)`: Writes the value of an I/O signal (synchronous)
  - async: `Task SetSignalValueAsync(string network, string device, string signal, float value, bool logToEventLog = false, CancellationToken cancellationToken = default)`
- `void SetSignalValueDelayed(string network, string device, string signal, float value, int delay, bool logToEventLog = false)`: Writes the value of an I/O signal in "queued delayed" mode (synchronous) The controller queues the write and applies it once the delay has elapsed.
  - async: `Task SetSignalValueDelayedAsync(string network, string device, string signal, float value, int delay, bool logToEventLog = false, CancellationToken cancellationToken = default)`
- `void ToggleSignal(string network, string device, string signal, float value, int pulses, int? activePulseLength = null, int? passivePulseLength = null, bool logToEventLog = false)`: Pulses an I/O signal by toggling its current value (synchronous) Only digital and group signals can be toggled.
  - async: `Task ToggleSignalAsync(string network, string device, string signal, float value, int pulses, int? activePulseLength = null, int? passivePulseLength = null, bool logToEventLog = false, CancellationToken cancellationToken = default)`
- `void UnblockSignals()`: Removes the simulation of every simulated I/O signal of the controller (synchronous)
  - async: `Task UnblockSignalsAsync(CancellationToken cancellationToken = default)`

## MastershipService (robot.Rws.Mastership)

`class MastershipService`

Mastership Service - Takes and gives back the exclusive right to change a domain of the controller. Most write operations are refused unless the client holds the mastership of the domain they belong to: moving a mechanical unit needs MastershipDomain.Motion, changing the system parameters or the...

- `MastershipDomain[] GetDomains()`: Gets the domains the connected controller can give the mastership of (synchronous)
  - async: `Task<MastershipDomain[]> GetDomainsAsync(CancellationToken cancellationToken = default)`
- `MastershipInfo[] GetInfo()`: Gets who holds the mastership of every domain of the controller (synchronous)
  - async: `Task<MastershipInfo[]> GetInfoAsync(CancellationToken cancellationToken = default)`
  - async: `Task<MastershipInfo> GetInfoAsync(MastershipDomain domain, CancellationToken cancellationToken = default)`
- `MastershipInfo GetInfo(MastershipDomain domain)`: Gets who holds the mastership of one domain (synchronous)
- `void Release()`: Gives back the mastership of every domain of the controller (synchronous)
  - async: `Task ReleaseAsync(CancellationToken cancellationToken = default)`
  - async: `Task ReleaseAsync(MastershipDomain domain, CancellationToken cancellationToken = default)`
- `void Release(MastershipDomain domain)`: Gives back the mastership of one domain (synchronous)
- `void Request()`: Takes the mastership of every domain of the controller (synchronous)
  - async: `Task RequestAsync(CancellationToken cancellationToken = default)`
  - async: `Task RequestAsync(MastershipDomain domain, CancellationToken cancellationToken = default)`
- `void Request(MastershipDomain domain)`: Takes the mastership of one domain (synchronous)

## MotionSystemService (robot.Rws.MotionSystem)

`class MotionSystemService`

Motion System Service - Everything about how the robot stands and how it moves: the mechanical units of the system and their axes, where the tool currently is, the calibration and the revolution counters, jogging, the collision supervision, and the kinematics calculations that convert a pose into...

- `void ClearSmbData(string mechanicalUnit, SmbDataMemory memory)`: Erases one of the two serial measurement board data stores (synchronous)
  - async: `Task ClearSmbDataAsync(string mechanicalUnit, SmbDataMemory memory, CancellationToken cancellationToken = default)`
- `void Commutate(string mechanicalUnit, int axis)`: Commutates the motor of one axis, which teaches the controller how the rotor of that motor is oriented (synchronous) Needed once after a motor has been replaced, before the axis can be calibrated.
  - async: `Task CommutateAsync(string mechanicalUnit, int axis, CancellationToken cancellationToken = default)`
- `void FineCalibrate(string mechanicalUnit, int axis)`: Fine calibrates one axis of a mechanical unit (synchronous)
  - async: `Task FineCalibrateAsync(string mechanicalUnit, int axis, CancellationToken cancellationToken = default)`
- `JointSolution[] GetAllJointSolutions(string mechanicalUnit, Pose pose, ExternalJoints externalAxes, Pose toolFrame, RobotConfiguration configuration, bool robotHoldsWorkObject = false)`: Asks the controller for every joint combination that puts the tool at the given pose (synchronous) A six axis robot usually reaches the same pose in eight different ways, each one in a different axis configuration.
  - async: `Task<JointSolution[]> GetAllJointSolutionsAsync(string mechanicalUnit, Pose pose, ExternalJoints externalAxes, Pose toolFrame, RobotConfiguration configuration, bool robotHoldsWorkObject = false, CancellationToken cancellationToken = default)`
- `AxisInfo GetAxis(string mechanicalUnit, int axis)`: Gets the state of one axis of a mechanical unit (synchronous)
  - async: `Task<AxisInfo> GetAxisAsync(string mechanicalUnit, int axis, CancellationToken cancellationToken = default)`
- `int GetAxisCount(string mechanicalUnit)`: Gets how many axes a mechanical unit has (synchronous)
  - async: `Task<int> GetAxisCountAsync(string mechanicalUnit, CancellationToken cancellationToken = default)`
- `Pose GetAxisPose(string mechanicalUnit, int axis)`: Gets where one axis of a mechanical unit sits (synchronous) The position is expressed in millimetres.
  - async: `Task<Pose> GetAxisPoseAsync(string mechanicalUnit, int axis, CancellationToken cancellationToken = default)`
- `BaseFrame GetBaseFrame(string mechanicalUnit)`: Gets where the base of a mechanical unit sits (synchronous) The position is expressed in millimetres.
  - async: `Task<BaseFrame> GetBaseFrameAsync(string mechanicalUnit, CancellationToken cancellationToken = default)`
- `CalibrationInfo GetCalibrationInfo(string mechanicalUnit)`: Gets how each joint of a mechanical unit was calibrated (synchronous)
  - async: `Task<CalibrationInfo> GetCalibrationInfoAsync(string mechanicalUnit, CancellationToken cancellationToken = default)`
- `RobTarget GetCartesianPosition(string mechanicalUnit, CoordinateSystem coordinateSystem = CoordinateSystem.Base, string tool = null, string workObject = null, bool logErrors = false)`: Gets where the tool of a mechanical unit currently is, without the external axes (synchronous) The position is expressed in millimetres.
  - async: `Task<RobTarget> GetCartesianPositionAsync(string mechanicalUnit, CoordinateSystem coordinateSystem = CoordinateSystem.Base, string tool = null, string workObject = null, bool logErrors = false, CancellationToken cancellationToken = default)`
- `bool GetCollisionPredictionMode()`: Tells whether the controller predicts collisions before they happen (synchronous) Collision prediction stops the robot before it hits something it knows about, where the motion supervision only reacts once the arm meets an unexpected resistance.
  - async: `Task<bool> GetCollisionPredictionModeAsync(CancellationToken cancellationToken = default)`
- `MotionSystemErrorState GetErrorState()`: Gets the last error the motion system ran into, and how many errors it has counted (synchronous) Most of these errors are raised by a jogging request the controller could not honour, and stay reported until a new one replaces them.
  - async: `Task<MotionSystemErrorState> GetErrorStateAsync(CancellationToken cancellationToken = default)`
- `MotionSystemInfo GetInfo()`: Gets an overview of the motion system: the mechanical unit jogging applies to, the change counter and the payload and accuracy settings (synchronous)
  - async: `Task<MotionSystemInfo> GetInfoAsync(CancellationToken cancellationToken = default)`
- `JointTarget GetJointTarget(string mechanicalUnit, bool alwaysRead = false)`: Gets the joint values a mechanical unit currently stands at (synchronous) The robot axes are expressed in degrees.
  - async: `Task<JointTarget> GetJointTargetAsync(string mechanicalUnit, bool alwaysRead = false, CancellationToken cancellationToken = default)`
- `JointTarget GetJointsFromCartesian(string mechanicalUnit, Pose pose, ExternalJoints externalAxes, Pose toolFrame, JointTarget previousJoints, RobotConfiguration configuration, bool robotHoldsWorkObject = false, bool logErrors = false)`: Asks the controller which joint values put the tool at the given pose, staying close to the joint values the robot is already in (synchronous)
  - async: `Task<JointTarget> GetJointsFromCartesianAsync(string mechanicalUnit, Pose pose, ExternalJoints externalAxes, Pose toolFrame, JointTarget previousJoints, RobotConfiguration configuration, bool robotHoldsWorkObject = false, bool logErrors = false, CancellationToken cancellationToken = default)`
- `JointTarget GetJointsFromPose(string mechanicalUnit, Pose pose, ExternalJoints externalAxes, Pose toolFrame, JointTarget previousJoints, RobotConfiguration configuration, bool robotHoldsWorkObject = false, bool logErrors = false)`: Asks the controller which joint values put the tool at the given pose (synchronous)
  - async: `Task<JointTarget> GetJointsFromPoseAsync(string mechanicalUnit, Pose pose, ExternalJoints externalAxes, Pose toolFrame, JointTarget previousJoints, RobotConfiguration configuration, bool robotHoldsWorkObject = false, bool logErrors = false, CancellationToken cancellationToken = default)`
- `LeadThroughStatus GetLeadThrough(string mechanicalUnit)`: Tells whether an operator can push the arm of a mechanical unit around by hand (synchronous)
  - async: `Task<LeadThroughStatus> GetLeadThroughAsync(string mechanicalUnit, CancellationToken cancellationToken = default)`
- `MechanicalUnitInfo GetMechanicalUnit(string mechanicalUnit)`: Gets everything the controller knows about one mechanical unit (synchronous)
  - async: `Task<MechanicalUnitInfo> GetMechanicalUnitAsync(string mechanicalUnit, CancellationToken cancellationToken = default)`
- `MechanicalUnitItem[] GetMechanicalUnits()`: Lists the mechanical units of the motion system (synchronous)
  - async: `Task<MechanicalUnitItem[]> GetMechanicalUnitsAsync(CancellationToken cancellationToken = default)`
- `MotionSupervision GetMotionSupervision(string mechanicalUnit)`: Gets the collision detection settings that apply while a mechanical unit is jogged (synchronous)
  - async: `Task<MotionSupervision> GetMotionSupervisionAsync(string mechanicalUnit, CancellationToken cancellationToken = default)`
- `MotorCalibrationName[] GetMotorCalibrationNames(string mechanicalUnit)`: Gets the name each joint of a mechanical unit carries, and the name of its calibration data (synchronous)
  - async: `Task<MotorCalibrationName[]> GetMotorCalibrationNamesAsync(string mechanicalUnit, CancellationToken cancellationToken = default)`
- `bool GetNonMotionExecutionMode()`: Tells whether the controller runs RAPID programs without moving the robot (synchronous) In that mode the program executes normally but every motion instruction is skipped, which is how a program is tested without the robot leaving its position.
  - async: `Task<bool> GetNonMotionExecutionModeAsync(CancellationToken cancellationToken = default)`
- `PathSupervision GetPathSupervision(string mechanicalUnit)`: Gets the collision detection settings that apply while a mechanical unit follows a programmed path (synchronous)
  - async: `Task<PathSupervision> GetPathSupervisionAsync(string mechanicalUnit, CancellationToken cancellationToken = default)`
- `RobotJoints GetPhysicalJoints(string mechanicalUnit)`: Gets the physical joint values of a mechanical unit, as its measurement system reads them (synchronous)
  - async: `Task<RobotJoints> GetPhysicalJointsAsync(string mechanicalUnit, CancellationToken cancellationToken = default)`
- `RobTarget GetPoseFromJoints(string mechanicalUnit, Pose toolFrame, JointTarget joints, bool robotHoldsWorkObject = false, bool logErrors = false)`: Asks the controller where the tool would be if the robot stood at the given joint values, without moving it there (synchronous)
  - async: `Task<RobTarget> GetPoseFromJointsAsync(string mechanicalUnit, Pose toolFrame, JointTarget joints, bool robotHoldsWorkObject = false, bool logErrors = false, CancellationToken cancellationToken = default)`
- `RobTarget GetRobTarget(string mechanicalUnit, CoordinateSystem coordinateSystem = CoordinateSystem.Base, string tool = null, string workObject = null)`: Gets where the tool of a mechanical unit currently is (synchronous) The position is expressed in millimetres.
  - async: `Task<RobTarget> GetRobTargetAsync(string mechanicalUnit, CoordinateSystem coordinateSystem = CoordinateSystem.Base, string tool = null, string workObject = null, CancellationToken cancellationToken = default)`
- `SmbData GetSmbData(string mechanicalUnit)`: Gets the serial measurement board data of a mechanical unit, as held by the controller cabinet and by the robot itself (synchronous) The two copies are meant to agree. When they do not, one of them is written over the other with Data.SmbDataTransfer).
  - async: `Task<SmbData> GetSmbDataAsync(string mechanicalUnit, CancellationToken cancellationToken = default)`
- `bool HasChanged(int changeCount)`: Tells whether the motion system changed since it reported the given change count (synchronous) Reading MotionSystemInfo.ChangeCount once and asking this afterwards is cheaper than fetching the whole state again to find out that nothing moved.
  - async: `Task<bool> HasChangedAsync(int changeCount, CancellationToken cancellationToken = default)`
- `void Jog(RobotJoints axes, int changeCount, JogIncrementMode incrementMode = JogIncrementMode.None)`: Moves the mechanical unit currently selected for jogging (synchronous) The unit is the one SetJoggingMechanicalUnit(System.String) chose, and how the six values are interpreted depends on its jog mode: axis by axis, along the axes of a coordinate system, and so on.
  - async: `Task JogAsync(RobotJoints axes, int changeCount, JogIncrementMode incrementMode = JogIncrementMode.None, CancellationToken cancellationToken = default)`
- `void SetAxisPose(string mechanicalUnit, int axis, Pose pose)`: Declares where one axis of a mechanical unit sits (synchronous) The position is expressed in millimetres.
  - async: `Task SetAxisPoseAsync(string mechanicalUnit, int axis, Pose pose, CancellationToken cancellationToken = default)`
- `void SetBaseFrame(string mechanicalUnit, Pose baseFrame)`: Declares where the base of a mechanical unit sits (synchronous) The position is expressed in millimetres.
  - async: `Task SetBaseFrameAsync(string mechanicalUnit, Pose baseFrame, CancellationToken cancellationToken = default)`
- `void SetCollisionPredictionMode(bool enabled)`: Switches collision prediction on or off (synchronous)
  - async: `Task SetCollisionPredictionModeAsync(bool enabled, CancellationToken cancellationToken = default)`
- `void SetJoggingMechanicalUnit(string mechanicalUnit)`: Chooses which mechanical unit the jogging commands apply to (synchronous)
  - async: `Task SetJoggingMechanicalUnitAsync(string mechanicalUnit, CancellationToken cancellationToken = default)`
- `void SetLeadThrough(string mechanicalUnit, bool active)`: Lets an operator push the arm of a mechanical unit around by hand, or stops letting them (synchronous)
  - async: `Task SetLeadThroughAsync(string mechanicalUnit, bool active, CancellationToken cancellationToken = default)`
- `void SetMechanicalUnit(string mechanicalUnit, string tool = null, string workObject = null, string payload = null, string totalPayload = null, MechanicalUnitMode? mode = null, JogMode? jogMode = null, CoordinateSystem? coordinateSystem = null)`: Changes one or several properties of a mechanical unit (synchronous) Every argument but the unit name is optional; leave the ones you do not want to touch null. At least one of them has to be given.
  - async: `Task SetMechanicalUnitAsync(string mechanicalUnit, string tool = null, string workObject = null, string payload = null, string totalPayload = null, MechanicalUnitMode? mode = null, JogMode? jogMode = null, CoordinateSystem? coordinateSystem = null, CancellationToken cancellationToken = default)`
- `void SetMechanicalUnitPosition(string mechanicalUnit, JointTarget position)`: Places a mechanical unit at the given joint values without moving it there (synchronous) Only a virtual controller accepts this: it teleports the simulated robot, which a real one cannot do.
  - async: `Task SetMechanicalUnitPositionAsync(string mechanicalUnit, JointTarget position, CancellationToken cancellationToken = default)`
- `void SetMotionSupervisionLevel(string mechanicalUnit, int sensitivity)`: Sets how sensitive the jogging collision detection of a mechanical unit is (synchronous)
  - async: `Task SetMotionSupervisionLevelAsync(string mechanicalUnit, int sensitivity, CancellationToken cancellationToken = default)`
- `void SetMotionSupervisionMode(string mechanicalUnit, bool enabled)`: Switches the jogging collision detection of a mechanical unit on or off (synchronous)
  - async: `Task SetMotionSupervisionModeAsync(string mechanicalUnit, bool enabled, CancellationToken cancellationToken = default)`
- `void SetNonMotionExecutionMode(bool enabled)`: Chooses whether the controller runs RAPID programs without moving the robot (synchronous)
  - async: `Task SetNonMotionExecutionModeAsync(bool enabled, CancellationToken cancellationToken = default)`
- `void SetPathSupervisionLevel(string mechanicalUnit, int level)`: Sets how sensitive the path collision detection of a mechanical unit is (synchronous)
  - async: `Task SetPathSupervisionLevelAsync(string mechanicalUnit, int level, CancellationToken cancellationToken = default)`
- `void SetPathSupervisionMode(string mechanicalUnit, bool enabled)`: Switches the path collision detection of a mechanical unit on or off (synchronous)
  - async: `Task SetPathSupervisionModeAsync(string mechanicalUnit, bool enabled, CancellationToken cancellationToken = default)`
- `void SetPositionTarget(RobTarget target)`: Sends the robot to a cartesian target (synchronous) The position is expressed in millimetres, in the coordinate system currently active for the mechanical unit selected for jogging.
  - async: `Task SetPositionTargetAsync(RobTarget target, CancellationToken cancellationToken = default)`
- `void SetSmbData(string mechanicalUnit, SmbDataTransfer direction)`: Copies one of the two serial measurement board data stores over the other (synchronous)
  - async: `Task SetSmbDataAsync(string mechanicalUnit, SmbDataTransfer direction, CancellationToken cancellationToken = default)`
- `void SynchronizeAxisRevolutionCounter(string mechanicalUnit, int axis)`: Synchronizes the revolution counter of one axis, telling the controller that the axis stands at its synchronization mark (synchronous)
  - async: `Task SynchronizeAxisRevolutionCounterAsync(string mechanicalUnit, int axis, CancellationToken cancellationToken = default)`
- `void UpdateRevolutionCounter(string mechanicalUnit, int axis)`: Updates the revolution counter of one axis of a mechanical unit (synchronous)
  - async: `Task UpdateRevolutionCounterAsync(string mechanicalUnit, int axis, CancellationToken cancellationToken = default)`

## PanelService (robot.Rws.Panel)

`class PanelService`

Panel Service - Exposes what an operator reads and acts on from the control panel of the controller: the controller state, the operating mode and its selector lock, the speed ratio, the collision detection state, the language of the controller and its restart. None of these resources is available...

- `void AcknowledgeOperationMode(OperationModeAcknowledgement acknowledgement)`: Confirms a pending operating mode change (synchronous) The controller waits for this confirmation whenever the mode selector is turned, unless it is configured to acknowledge the change on its own.
  - async: `Task AcknowledgeOperationModeAsync(OperationModeAcknowledgement acknowledgement, CancellationToken cancellationToken = default)`
- `CollisionDetectionState GetCollisionDetectionState()`: Gets the collision detection state of the controller (synchronous)
  - async: `Task<CollisionDetectionState> GetCollisionDetectionStateAsync(CancellationToken cancellationToken = default)`
- `ControllerState GetControllerState()`: Gets the state of the controller (synchronous)
  - async: `Task<ControllerState> GetControllerStateAsync(CancellationToken cancellationToken = default)`
- `OperationMode GetOperationMode()`: Gets the operating mode the controller runs in (synchronous)
  - async: `Task<OperationMode> GetOperationModeAsync(CancellationToken cancellationToken = default)`
- `OperationModeLockState GetOperationModeLockState()`: Gets the lock state of the operating mode selector (synchronous)
  - async: `Task<OperationModeLockState> GetOperationModeLockStateAsync(CancellationToken cancellationToken = default)`
- `int GetSpeedRatio()`: Gets the speed ratio the controller runs the programs at (synchronous)
  - async: `Task<int> GetSpeedRatioAsync(CancellationToken cancellationToken = default)`
- `void LockOperationMode(string pin, bool permanent = false)`: Locks the operating mode selector with a pin code (synchronous)
  - async: `Task LockOperationModeAsync(string pin, bool permanent = false, CancellationToken cancellationToken = default)`
- `void Restart(ControllerRestartMode mode, bool useImplicitMastership = true)`: Restarts the controller (synchronous)
  - async: `Task RestartAsync(ControllerRestartMode mode, bool useImplicitMastership = true, CancellationToken cancellationToken = default)`
- `void SetControllerState(ControllerState state)`: Turns the motors of the robot on or off (synchronous)
  - async: `Task SetControllerStateAsync(ControllerState state, CancellationToken cancellationToken = default)`
- `void SetLanguage(string languageCode)`: Sets the language the controller reports its messages in (synchronous)
  - async: `Task SetLanguageAsync(string languageCode, CancellationToken cancellationToken = default)`
- `void SetSpeedRatio(int speedRatio, bool useImplicitMastership = true)`: Sets the speed ratio the controller runs the programs at (synchronous) Only accepted while the controller runs in automatic mode.
  - async: `Task SetSpeedRatioAsync(int speedRatio, bool useImplicitMastership = true, CancellationToken cancellationToken = default)`
- `void UnlockOperationMode(string pin)`: Releases the lock of the operating mode selector (synchronous)
  - async: `Task UnlockOperationModeAsync(string pin, CancellationToken cancellationToken = default)`

## RapidService (robot.Rws.Rapid)

`class RapidService`

RAPID Service - Everything about the program the robot runs: the tasks it is split into, the modules and the source they hold, the symbols the program declares and the values they carry, where the program pointer stands, and starting, stopping and stepping the execution. None of these resources i...

- `void AbortExecutionLevel(string task)`: Abandons the routine the task is currently running and returns to the level below it (synchronous) This is how a trap or a service routine started by hand is left without stopping the program underneath it.
  - async: `Task AbortExecutionLevelAsync(string task, CancellationToken cancellationToken = default)`
- `void ActivateTask(string task)`: Activates one task (synchronous)
  - async: `Task ActivateTaskAsync(string task, CancellationToken cancellationToken = default)`
- `void ActivateTasks()`: Activates every task of the controller (synchronous)
  - async: `Task ActivateTasksAsync(CancellationToken cancellationToken = default)`
- `void BuildTask(string task)`: Links the program of a task, which is what turns the modules it holds into something runnable (synchronous) Read GetBuildErrors() afterwards to find out what the controller refused.
  - async: `Task BuildTaskAsync(string task, CancellationToken cancellationToken = default)`
- `void DeactivateTask(string task)`: Deactivates one task (synchronous)
  - async: `Task DeactivateTaskAsync(string task, CancellationToken cancellationToken = default)`
- `void DeactivateTasks()`: Deactivates every task of the controller (synchronous)
  - async: `Task DeactivateTasksAsync(CancellationToken cancellationToken = default)`
- `RapidActivationRecord GetActivationRecord(string task, int stackFrame = 1)`: Gets one frame of the call stack of a task: which routine is running and where execution stands in it (synchronous)
  - async: `Task<RapidActivationRecord> GetActivationRecordAsync(string task, int stackFrame = 1, CancellationToken cancellationToken = default)`
- `RapidUiInstruction GetActiveUiInstruction()`: Gets the dialogue a running RAPID program is currently asking an operator for (synchronous) Answering it means writing its parameters with String%2cSystem.String), addressed by the path this returns.
  - async: `Task<RapidUiInstruction> GetActiveUiInstructionAsync(CancellationToken cancellationToken = default)`
- `RapidAliasIoItem[] GetAliasIo(int? start = null, int? limit = null)`: Gets the I/O signals a running RAPID program has given an alias to (synchronous)
  - async: `Task<RapidAliasIoItem[]> GetAliasIoAsync(int? start = null, int? limit = null, CancellationToken cancellationToken = default)`
- `RapidModifiablePositionItem[] GetAllModifiablePositions()`: Gets every motion instruction of the system whose position can be rewritten to where the robot currently stands, wherever in whichever task it sits (synchronous)
  - async: `Task<RapidModifiablePositionItem[]> GetAllModifiablePositionsAsync(CancellationToken cancellationToken = default)`
- `RapidBreakpoint[] GetBreakpoints(string task, int? start = null, int? limit = null)`: Gets the breakpoints set in the program of a task (synchronous)
  - async: `Task<RapidBreakpoint[]> GetBreakpointsAsync(string task, int? start = null, int? limit = null, CancellationToken cancellationToken = default)`
- `RapidBuildError[] GetBuildErrors(string task, int? start = null, int? limit = null)`: Gets the errors the controller found while linking the program of a task (synchronous)
  - async: `Task<RapidBuildError[]> GetBuildErrorsAsync(string task, int? start = null, int? limit = null, CancellationToken cancellationToken = default)`
- `RapidExecutionInfo GetExecutionState()`: Gets whether the controller is executing RAPID code, and how many cycles it is set to run (synchronous)
  - async: `Task<RapidExecutionInfo> GetExecutionStateAsync(CancellationToken cancellationToken = default)`
- `RapidExternalJointStates GetExternalJointStates(string task)`: Gets what each of the six external joints of a task is doing (synchronous) This is what says how to read the corresponding value of GetJointTarget(System.String): a joint reported as not active carries no meaningful position.
  - async: `Task<RapidExternalJointStates> GetExternalJointStatesAsync(string task, CancellationToken cancellationToken = default)`
- `RapidInstructionTemplate GetInstructionTemplate(string task, string module, string name, bool isDataType = false, int? row = null, int? column = null, int? parameterNumber = null, int? alternativeNumber = null)`: Gets the template the controller suggests for an instruction or a data type: the arguments to write and the values to write them with (synchronous) This is what an editor uses to insert a complete, valid instruction rather than a bare keyword.
  - async: `Task<RapidInstructionTemplate> GetInstructionTemplateAsync(string task, string module, string name, bool isDataType = false, int? row = null, int? column = null, int? parameterNumber = null, int? alternativeNumber = null, CancellationToken cancellationToken = default)`
- `JointTarget GetJointTarget(string task)`: Gets the joint values of the robot of a task (synchronous)
  - async: `Task<JointTarget> GetJointTargetAsync(string task, CancellationToken cancellationToken = default)`
- `RapidMechanicalUnitItem[] GetMechanicalUnits(string task)`: Gets the mechanical units the positions of a task are expressed in (synchronous)
  - async: `Task<RapidMechanicalUnitItem[]> GetMechanicalUnitsAsync(string task, CancellationToken cancellationToken = default)`
- `RapidModifiablePositions GetModifiablePositions(string task, string module, int startRow, int startColumn, int endRow, int endColumn)`: Gets how many motion instructions of a range can have their position rewritten to where the robot currently stands (synchronous)
  - async: `Task<RapidModifiablePositions> GetModifiablePositionsAsync(string task, string module, int startRow, int startColumn, int endRow, int endColumn, CancellationToken cancellationToken = default)`
- `RapidModuleInfo GetModule(string task, string module)`: Gets the file a module came from and the properties declared on it (synchronous)
  - async: `Task<RapidModuleInfo> GetModuleAsync(string task, string module, CancellationToken cancellationToken = default)`
- `int GetModuleChangeCount(string task, string module)`: Gets the counter the controller increments whenever a module changes (synchronous) Comparing it with what a previous reading gave is cheaper than fetching the source again to find out that nothing changed.
  - async: `Task<int> GetModuleChangeCountAsync(string task, string module, CancellationToken cancellationToken = default)`
- `RapidModuleExtension GetModuleExtension(string task, string module)`: Gets how many lines and columns the source of a module holds (synchronous) This is what it takes to ask for the whole of it with Int32%2cSystem.Int32).
  - async: `Task<RapidModuleExtension> GetModuleExtensionAsync(string task, string module, CancellationToken cancellationToken = default)`
- `RapidModuleSymbol GetModuleSymbol(string task, string module, int row, int column)`: Gets the declaration the controller finds at a position of a module (synchronous)
  - async: `Task<RapidModuleSymbol> GetModuleSymbolAsync(string task, string module, int row, int column, CancellationToken cancellationToken = default)`
- `RapidModuleText GetModuleText(string task, string module)`: Gets the source of a module (synchronous)
  - async: `Task<RapidModuleText> GetModuleTextAsync(string task, string module, CancellationToken cancellationToken = default)`
- `string GetModuleTextRange(string task, string module, int startRow, int startColumn, int endRow, int endColumn)`: Gets a range of the source of a module (synchronous)
  - async: `Task<string> GetModuleTextRangeAsync(string task, string module, int startRow, int startColumn, int endRow, int endColumn, CancellationToken cancellationToken = default)`
- `RapidModuleItem[] GetModules(string task)`: Gets the modules loaded into a task (synchronous)
  - async: `Task<RapidModuleItem[]> GetModulesAsync(string task, CancellationToken cancellationToken = default)`
- `RapidPointerSyncState GetMotionPointerSyncState()`: Gets whether the motion pointers of every task are synchronized with each other (synchronous)
  - async: `Task<RapidPointerSyncState> GetMotionPointerSyncStateAsync(CancellationToken cancellationToken = default)`
- `RapidObjectChild GetObjectChildren(string task, string module, int startLine, int startColumn, int endLine, int endColumn)`: Gets the parts a RAPID object is made of and where each of them sits in the source (synchronous) Pass the whole span of the object to get its parts; an editor uses this to know where the name, the attributes and the declaration lists of a module begin and end.
  - async: `Task<RapidObjectChild> GetObjectChildrenAsync(string task, string module, int startLine, int startColumn, int endLine, int endColumn, CancellationToken cancellationToken = default)`
- `RapidObjectListExtension GetObjectListExtension(string symbolUrl, RapidObjectListType type = RapidObjectListType.Statements)`: Gets where one of the lists a RAPID object holds sits in the source: the span of the whole list, and the spans of its first and last elements (synchronous) An editor uses this to jump to the beginning or the end of a list without reading the whole module.
  - async: `Task<RapidObjectListExtension> GetObjectListExtensionAsync(string symbolUrl, RapidObjectListType type = RapidObjectListType.Statements, CancellationToken cancellationToken = default)`
- `RapidPalletItem[] GetPallet(string task, int palletNumber, int? start = null, int? limit = null)`: Gets the entries of one category of the instruction palette (synchronous)
  - async: `Task<RapidPalletItem[]> GetPalletAsync(string task, int palletNumber, int? start = null, int? limit = null, CancellationToken cancellationToken = default)`
- `RapidPalletHeadItem[] GetPalletHeads(string task, int? start = null, int? limit = null)`: Gets the categories of the instruction palette an editor offers (synchronous)
  - async: `Task<RapidPalletHeadItem[]> GetPalletHeadsAsync(string task, int? start = null, int? limit = null, CancellationToken cancellationToken = default)`
- `RapidPointers GetPointers(string task)`: Gets where the program pointer and the motion pointer of a task stand (synchronous) The program pointer says which instruction runs next, the motion pointer which one the robot is actually executing; they drift apart because the controller plans the path ahead of the movement.
  - async: `Task<RapidPointers> GetPointersAsync(string task, CancellationToken cancellationToken = default)`
- `RapidModuleAttribute[] GetPossibleModuleAttributes(string task, string module, params RapidModuleAttribute[] attributes)`: Gets which of the requested properties may be declared on a module (synchronous)
  - async: `Task<RapidModuleAttribute[]> GetPossibleModuleAttributesAsync(string task, string module, RapidModuleAttribute[] attributes, CancellationToken cancellationToken = default)`
- `RapidPreferredDataTypeItem[] GetPreferredDataTypes(string task, string instruction, string parameter)`: Gets the data types the controller suggests for one argument of an instruction (synchronous) An editor uses this to offer only the types that fit where the operator is typing.
  - async: `Task<RapidPreferredDataTypeItem[]> GetPreferredDataTypesAsync(string task, string instruction, string parameter, CancellationToken cancellationToken = default)`
- `RapidProgramInfo GetProgram(string task)`: Gets the program loaded into a task (synchronous)
  - async: `Task<RapidProgramInfo> GetProgramAsync(string task, CancellationToken cancellationToken = default)`
- `RapidProgramCounterPosition GetProgramCounterPosition(string task)`: Gets which piece of source the program pointer of a task points at (synchronous)
  - async: `Task<RapidProgramCounterPosition> GetProgramCounterPositionAsync(string task, CancellationToken cancellationToken = default)`
- `RapidPointerSyncState GetProgramPointerSyncState()`: Gets whether the program pointers of every task are synchronized with each other (synchronous)
  - async: `Task<RapidPointerSyncState> GetProgramPointerSyncStateAsync(CancellationToken cancellationToken = default)`
- `RobTarget GetRobTarget(string task, string tool = null, string workObject = null)`: Gets where the tool of a task currently stands, as a position and an orientation (synchronous)
  - async: `Task<RobTarget> GetRobTargetAsync(string task, string tool = null, string workObject = null, CancellationToken cancellationToken = default)`
- `RapidRoutineInfo GetRoutine(string task, string module, int row, int column)`: Gets the routine the controller finds called at a position of a module (synchronous)
  - async: `Task<RapidRoutineInfo> GetRoutineAsync(string task, string module, int row, int column, CancellationToken cancellationToken = default)`
- `RapidRoutineArgument[] GetRoutineArguments(string task, string module, int row, int column, int? mark = null, int? limit = null)`: Gets the arguments of the routine call found at a position of a module (synchronous)
  - async: `Task<RapidRoutineArgument[]> GetRoutineArgumentsAsync(string task, string module, int row, int column, int? mark = null, int? limit = null, CancellationToken cancellationToken = default)`
- `RapidServiceRoutineItem[] GetServiceRoutines(string task, int? start = null, int? limit = null)`: Gets the routines of a task the program pointer can be moved to (synchronous)
  - async: `Task<RapidServiceRoutineItem[]> GetServiceRoutinesAsync(string task, int? start = null, int? limit = null, CancellationToken cancellationToken = default)`
- `RapidSpyStatus GetSpyStatus()`: Gets whether the controller is recording the RAPID execution trace to a file (synchronous)
  - async: `Task<RapidSpyStatus> GetSpyStatusAsync(CancellationToken cancellationToken = default)`
- `RapidStructuralChangeCount GetStructuralChangeCount(string task)`: Gets the two counters a task keeps of what has changed in it (synchronous) Comparing them with what a previous reading gave is cheaper than fetching the modules again to find out that nothing moved.
  - async: `Task<RapidStructuralChangeCount> GetStructuralChangeCountAsync(string task, CancellationToken cancellationToken = default)`
- `RapidSymbolProperties GetSymbolProperties(string symbolUrl)`: Gets what a RAPID symbol is declared as (synchronous)
  - async: `Task<RapidSymbolProperties> GetSymbolPropertiesAsync(string symbolUrl, CancellationToken cancellationToken = default)`
- `RapidSymbolValue GetSymbolValue(string symbolUrl)`: Gets the value of a RAPID symbol and where it is declared (synchronous)
  - async: `Task<RapidSymbolValue> GetSymbolValueAsync(string symbolUrl, CancellationToken cancellationToken = default)`
- `bool GetSyncPersStatus(string task, string module)`: Gets whether the persistent variables of a module are kept synchronized with the other tasks declaring them (synchronous)
  - async: `Task<bool> GetSyncPersStatusAsync(string task, string module, CancellationToken cancellationToken = default)`
- `RapidTaskInfo GetTask(string task)`: Gets everything the controller reports about one task (synchronous)
  - async: `Task<RapidTaskInfo> GetTaskAsync(string task, CancellationToken cancellationToken = default)`
- `RapidPointerSyncState GetTaskMotionPointerSyncState(string task)`: Gets whether the motion pointer of one task is synchronized with the others (synchronous)
  - async: `Task<RapidPointerSyncState> GetTaskMotionPointerSyncStateAsync(string task, CancellationToken cancellationToken = default)`
- `RapidPointerSyncState GetTaskProgramPointerSyncState(string task)`: Gets whether the program pointer of one task is synchronized with the others (synchronous)
  - async: `Task<RapidPointerSyncState> GetTaskProgramPointerSyncStateAsync(string task, CancellationToken cancellationToken = default)`
- `RapidTaskSelectionItem[] GetTaskSelection()`: Gets the task selection panel: which tasks are selected, and which of them an operator is allowed to change the selection of (synchronous)
  - async: `Task<RapidTaskSelectionItem[]> GetTaskSelectionAsync(CancellationToken cancellationToken = default)`
- `RapidTaskItem[] GetTasks()`: Gets every RAPID task of the controller and what each of them is doing (synchronous)
  - async: `Task<RapidTaskItem[]> GetTasksAsync(CancellationToken cancellationToken = default)`
- `string GetUiInstructionParameter(string stackUrl, string parameter)`: Gets the value of one parameter of a pending UI instruction (synchronous)
  - async: `Task<string> GetUiInstructionParameterAsync(string stackUrl, string parameter, CancellationToken cancellationToken = default)`
- `RapidUiInstructionParameter[] GetUiInstructionParameters(string stackUrl)`: Gets every parameter of a pending UI instruction: what the program passed in, and what it is waiting for (synchronous)
  - async: `Task<RapidUiInstructionParameter[]> GetUiInstructionParametersAsync(string stackUrl, CancellationToken cancellationToken = default)`
- `string LoadModule(string task, string modulePath, bool replace = false)`: Loads a module file into a task (synchronous)
  - async: `Task<string> LoadModuleAsync(string task, string modulePath, bool replace = false, CancellationToken cancellationToken = default)`
- `void LoadProgram(string task, string programPath, RapidProgramLoadMode loadMode = RapidProgramLoadMode.Add)`: Loads a program into a task (synchronous)
  - async: `Task LoadProgramAsync(string task, string programPath, RapidProgramLoadMode loadMode = RapidProgramLoadMode.Add, CancellationToken cancellationToken = default)`
- `void ModifyAllPositions(bool checkLimits = true, bool checkDeactivatedAxes = true)`: Rewrites the positions of every motion instruction of the system that can be rewritten, to where the robot currently stands (synchronous)
  - async: `Task ModifyAllPositionsAsync(bool checkLimits = true, bool checkDeactivatedAxes = true, CancellationToken cancellationToken = default)`
- `void ModifyPosition(string task, string module, int startRow, int startColumn, int endRow, int endColumn, bool checkLimits = true, bool checkDeactivatedAxes = true, bool allowDeactivated = false)`: Rewrites the positions of the motion instructions of a range to where the robot currently stands (synchronous) This is the teaching gesture: jog the robot where it should go, then write that position back into the program.
  - async: `Task ModifyPositionAsync(string task, string module, int startRow, int startColumn, int endRow, int endColumn, bool checkLimits = true, bool checkDeactivatedAxes = true, bool allowDeactivated = false, CancellationToken cancellationToken = default)`
- `void ResetProgramPointer()`: Moves the program pointer of every task back to the entry point of its program (synchronous)
  - async: `Task ResetProgramPointerAsync(CancellationToken cancellationToken = default)`
- `void SaveModule(string task, string module, string name, string path)`: Saves a module to the file system of the controller (synchronous)
  - async: `Task SaveModuleAsync(string task, string module, string name, string path, CancellationToken cancellationToken = default)`
- `void SaveProgram(string task, string path)`: Saves the program of a task to the file system of the controller (synchronous)
  - async: `Task SaveProgramAsync(string task, string path, CancellationToken cancellationToken = default)`
- `RapidTextPosition SearchModuleText(string task, string module, string text, int startRow = 1, int startColumn = 1)`: Finds where a piece of text sits in the source of a module (synchronous)
  - async: `Task<RapidTextPosition> SearchModuleTextAsync(string task, string module, string text, int startRow = 1, int startColumn = 1, CancellationToken cancellationToken = default)`
- `RapidSymbolProperties[] SearchSymbols(RapidSymbolSearchCriteria criteria)`: Finds the RAPID symbols matching a set of criteria (synchronous)
  - async: `Task<RapidSymbolProperties[]> SearchSymbolsAsync(RapidSymbolSearchCriteria criteria, CancellationToken cancellationToken = default)`
- `RapidBreakpoint SetBreakpoint(string task, string module, int row, int column)`: Sets a breakpoint at a position of a module (synchronous)
  - async: `Task<RapidBreakpoint> SetBreakpointAsync(string task, string module, int row, int column, CancellationToken cancellationToken = default)`
- `void SetEntryPoint(string task, string routine)`: Sets the routine the program pointer moves to when it is reset (synchronous)
  - async: `Task SetEntryPointAsync(string task, string routine, CancellationToken cancellationToken = default)`
- `void SetExecutionCycle(RapidExecutionCycle cycle)`: Sets how many times the program runs before stopping (synchronous)
  - async: `Task SetExecutionCycleAsync(RapidExecutionCycle cycle, CancellationToken cancellationToken = default)`
- `void SetHoldToRun(RapidHoldToRunState state)`: Drives the hold-to-run control that lets the program run in manual mode (synchronous) Send RapidHoldToRunState.Press to allow execution to start, then RapidHoldToRunState.Held about every two seconds to keep it running; the controller stops the program as soon as it stops hearing from the client....
  - async: `Task SetHoldToRunAsync(RapidHoldToRunState state, CancellationToken cancellationToken = default)`
- `void SetModuleText(string task, string module, string text)`: Replaces the whole source of a module (synchronous)
  - async: `Task SetModuleTextAsync(string task, string module, string text, CancellationToken cancellationToken = default)`
- `RapidSetTextRangeResult SetModuleTextRange(string task, string module, RapidTextReplaceMode replaceMode, RapidTextQueryMode queryMode, int startRow, int startColumn, int endRow, int endColumn, string text)`: Writes text into a range of the source of a module (synchronous)
  - async: `Task<RapidSetTextRangeResult> SetModuleTextRangeAsync(string task, string module, RapidTextReplaceMode replaceMode, RapidTextQueryMode queryMode, int startRow, int startColumn, int endRow, int endColumn, string text, CancellationToken cancellationToken = default)`
- `void SetProgramName(string task, string name)`: Renames the program of a task (synchronous)
  - async: `Task SetProgramNameAsync(string task, string name, CancellationToken cancellationToken = default)`
- `void SetProgramPointerToCursor(string task, string module, string routine, int row, int column)`: Moves the program pointer of a task to a position of a module (synchronous)
  - async: `Task SetProgramPointerToCursorAsync(string task, string module, string routine, int row, int column, CancellationToken cancellationToken = default)`
- `void SetProgramPointerToNextInstruction(string task)`: Moves the program pointer of a task forward by one instruction (synchronous)
  - async: `Task SetProgramPointerToNextInstructionAsync(string task, CancellationToken cancellationToken = default)`
- `void SetProgramPointerToPreviousInstruction(string task)`: Moves the program pointer of a task back by one instruction (synchronous)
  - async: `Task SetProgramPointerToPreviousInstructionAsync(string task, CancellationToken cancellationToken = default)`
- `void SetProgramPointerToRoutine(string task, string module, string routine, bool userLevel = false)`: Moves the program pointer of a task to the beginning of a routine (synchronous)
  - async: `Task SetProgramPointerToRoutineAsync(string task, string module, string routine, bool userLevel = false, CancellationToken cancellationToken = default)`
- `void SetProgramPointerToRoutineUrl(string task, string routineUrl, bool userLevel = false)`: Moves the program pointer of a task to a routine named by its path (synchronous) This is what the paths GetServiceRoutines() reports are for.
  - async: `Task SetProgramPointerToRoutineUrlAsync(string task, string routineUrl, bool userLevel = false, CancellationToken cancellationToken = default)`
- `void SetSymbolInitialValue(string symbolUrl, string value)`: Sets the value a RAPID symbol is declared with, which is the one it goes back to when the program is reset (synchronous)
  - async: `Task SetSymbolInitialValueAsync(string symbolUrl, string value, CancellationToken cancellationToken = default)`
- `void SetSymbolValue(string symbolUrl, string value)`: Sets the value a RAPID symbol currently holds (synchronous)
  - async: `Task SetSymbolValueAsync(string symbolUrl, string value, CancellationToken cancellationToken = default)`
- `void SetUiInstructionParameter(string stackUrl, string parameter, string value)`: Answers a pending UI instruction by writing one of its parameters (synchronous) An instruction is normally answered by writing the parameter carrying the answer and then the one marking it as completed.
  - async: `Task SetUiInstructionParameterAsync(string stackUrl, string parameter, string value, CancellationToken cancellationToken = default)`
- `void Start(RapidRegainMode regain = RapidRegainMode.Continue, RapidExecutionMode executionMode = RapidExecutionMode.Continue, RapidExecutionCycle cycle = RapidExecutionCycle.Forever, RapidStartCondition condition = RapidStartCondition.None, bool stopAtBreakpoint = false, bool allTasksBySelection = false)`: Starts executing the RAPID program from where the program pointer stands (synchronous) The controller has to be in automatic mode with the motors on, or in manual mode with the enabling device held. Reset the program pointer first with RapidService.ResetProgramPointer to start from the beginning.
  - async: `Task StartAsync(RapidRegainMode regain = RapidRegainMode.Continue, RapidExecutionMode executionMode = RapidExecutionMode.Continue, RapidExecutionCycle cycle = RapidExecutionCycle.Forever, RapidStartCondition condition = RapidStartCondition.None, bool stopAtBreakpoint = false, bool allTasksBySelection = false, CancellationToken cancellationToken = default)`
- `void StartFromProductionEntry()`: Starts executing from the production entry point of the program rather than from where the program pointer stands (synchronous)
  - async: `Task StartFromProductionEntryAsync(CancellationToken cancellationToken = default)`
- `void StartSpy(string logFile)`: Starts recording the RAPID execution trace into a file (synchronous) The trace names every instruction the controller runs, which is what it takes to find out why a program took a branch it should not have.
  - async: `Task StartSpyAsync(string logFile, CancellationToken cancellationToken = default)`
- `void Stop(RapidStopMode stopMode = RapidStopMode.Stop, RapidTaskScope scope = RapidTaskScope.Normal)`: Stops the RAPID execution (synchronous)
  - async: `Task StopAsync(RapidStopMode stopMode = RapidStopMode.Stop, RapidTaskScope scope = RapidTaskScope.Normal, CancellationToken cancellationToken = default)`
- `void StopSpy()`: Stops recording the RAPID execution trace (synchronous)
  - async: `Task StopSpyAsync(CancellationToken cancellationToken = default)`
- `void SyncPersistentVariables(string task, string module)`: Synchronizes the persistent variables of a module with the other tasks declaring them (synchronous)
  - async: `Task SyncPersistentVariablesAsync(string task, string module, CancellationToken cancellationToken = default)`
- `void UnloadModule(string task, string module)`: Unloads a module from a task (synchronous)
  - async: `Task UnloadModuleAsync(string task, string module, CancellationToken cancellationToken = default)`
- `void UnloadProgram(string task)`: Unloads the program of a task (synchronous)
  - async: `Task UnloadProgramAsync(string task, CancellationToken cancellationToken = default)`
- `bool ValidateSymbolValue(string task, string dataType, string value)`: Asks the controller whether a value would be accepted for a given RAPID type, without writing it anywhere (synchronous) This is what an editor uses to tell an operator that what they typed is wrong before the write is attempted.
  - async: `Task<bool> ValidateSymbolValueAsync(string task, string dataType, string value, CancellationToken cancellationToken = default)`

## SystemService (robot.Rws.System)

`class SystemService`

System Service - Describes the system installed on the controller: its name and software version, the options and the products it was built with, the type of robot it drives, its license, and the energy it consumes. None of these resources is available while the controller runs in bootserver mode.

- `SystemEnergy GetEnergy()`: Gets the energy the controller consumed, for the current interval and since the last reset (synchronous)
  - async: `Task<SystemEnergy> GetEnergyAsync(CancellationToken cancellationToken = default)`
- `int? GetEnergyChangeCount()`: Gets the counter the controller increments each time a new energy measurement is available (synchronous)
  - async: `Task<int?> GetEnergyChangeCountAsync(CancellationToken cancellationToken = default)`
- `SystemInfo GetInfo()`: Gets the name, the software version and the installed options of the system (synchronous)
  - async: `Task<SystemInfo> GetInfoAsync(CancellationToken cancellationToken = default)`
- `string GetLicense()`: Gets the license the robot software runs under (synchronous)
  - async: `Task<string> GetLicenseAsync(CancellationToken cancellationToken = default)`
- `string[] GetOptions()`: Gets the options installed on the system (synchronous)
  - async: `Task<string[]> GetOptionsAsync(CancellationToken cancellationToken = default)`
- `SystemProduct[] GetProducts(string name = null)`: Gets the software products installed on the controller, with their versions (synchronous)
  - async: `Task<SystemProduct[]> GetProductsAsync(string name = null, CancellationToken cancellationToken = default)`
- `string[] GetRobotTypes()`: Gets the type of every robot the controller drives (synchronous)
  - async: `Task<string[]> GetRobotTypesAsync(CancellationToken cancellationToken = default)`
- `void ResetAccumulatedEnergy()`: Sets the accumulated energy counter of the controller back to zero (synchronous)
  - async: `Task ResetAccumulatedEnergyAsync(CancellationToken cancellationToken = default)`
