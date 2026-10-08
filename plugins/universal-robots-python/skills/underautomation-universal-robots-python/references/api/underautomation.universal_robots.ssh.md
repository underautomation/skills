# underautomation.universal_robots.ssh

## SftpClient

`from underautomation.universal_robots.ssh.sftp_client import SftpClient`

Provides a client for transferring files to and from the Universal Robots controller using the SFTP protocol.

- `SftpClient()`
- `connect(ip: str, username: str, password: str, port: int=22) -> None`: Connects to the robot
- Inherited from [SftpClientBase](underautomation.universal_robots.ssh.internal.md#sftpclientbase-robotsftp): `disconnect`, `change_directory`, `change_permissions`, `create_directory`, `delete_directory`, `delete_file`, `rename_file`, `symbolic_link`, `list_directory`, `enumerate_programs`, `enumerate_installations`, `get`, `exists`, `download_file`, `upload_file`, `get_status`, `append_all_lines`, `append_all_text`, `create`, `delete`, `get_last_access_time`, `get_last_access_time_utc`, `get_last_write_time`, `get_last_write_time_utc`, `open_read`, `open_write`, `read_all_bytes`, `read_all_lines`, `read_all_text`, `read_lines`, `write_all_bytes`, `write_all_lines`, `write_all_text`, `get_attributes`, `set_attributes`, `connected`, `operation_timeout`, `buffer_size`, `working_directory`, `protocol_version`
- Inherited from [URServiceBase](underautomation.universal_robots.internal.md#urservicebase-robot): `internal_error_occured`

## SshClient

`from underautomation.universal_robots.ssh.ssh_client import SshClient`

Provides a client connection to SSH server

- `SshClient()`
- `connect(ip: str, username: str, password: str, port: int=22) -> None`: Connects to the robot
- Inherited from [SshClientBase](underautomation.universal_robots.ssh.internal.md#sshclientbase-robotssh): `disconnect`, `create_command`, `run_command`, `create_shell_stream`, `connected`
- Inherited from [URServiceBase](underautomation.universal_robots.internal.md#urservicebase-robot): `internal_error_occured`
