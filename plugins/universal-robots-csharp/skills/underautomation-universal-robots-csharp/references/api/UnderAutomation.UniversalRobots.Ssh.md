# UnderAutomation.UniversalRobots.Ssh

## SftpClient

`class SftpClient : SftpClientBase`

Provides a client for transferring files to and from the Universal Robots controller using the SFTP protocol.

- `SftpClient()`
- `void Connect(string ip, string username, string password, int port = 22)`: Connects to the robot
- Inherited from [SftpClientBase](UnderAutomation.UniversalRobots.Ssh.Internal.md#sftpclientbase-robotsftp): `Disconnect`, `ChangeDirectory`, `ChangePermissions`, `CreateDirectory`, `DeleteDirectory`, `DeleteFile`, `RenameFile`, `SymbolicLink`, `ListDirectory`, `EnumeratePrograms`, `EnumerateInstallations`, `BeginListDirectory`, `EndListDirectory`, `Get`, `Exists`, `DownloadFile`, `BeginDownloadFile`, `EndDownloadFile`, `UploadFile`, `BeginUploadFile`, `EndUploadFile`, `GetStatus`, `AppendAllLines`, `AppendAllText`, `AppendText`, `Create`, `CreateText`, `Delete`, `GetLastAccessTime`, `GetLastAccessTimeUtc`, `GetLastWriteTime`, `GetLastWriteTimeUtc`, `Open`, `OpenRead`, `OpenText`, `OpenWrite`, `ReadAllBytes`, `ReadAllLines`, `ReadAllText`, `ReadLines`, `WriteAllBytes`, `WriteAllLines`, `WriteAllText`, `GetAttributes`, `SetAttributes`, `SynchronizeDirectories`, `BeginSynchronizeDirectories`, `EndSynchronizeDirectories`, `Connected`, `OperationTimeout`, `BufferSize`, `WorkingDirectory`, `ProtocolVersion`
- Inherited from [URServiceBase](UnderAutomation.UniversalRobots.Internal.md#urservicebase-robot): `InternalErrorOccured`

## SshClient

`class SshClient : SshClientBase`

Provides a client connection to SSH server

- `SshClient()`
- `void Connect(string ip, string username, string password, int port = 22)`: Connects to the robot
- Inherited from [SshClientBase](UnderAutomation.UniversalRobots.Ssh.Internal.md#sshclientbase-robotssh): `Disconnect`, `CreateCommand`, `RunCommand`, `CreateShell`, `CreateShellStream`, `Connected`
- Inherited from [URServiceBase](UnderAutomation.UniversalRobots.Internal.md#urservicebase-robot): `InternalErrorOccured`
