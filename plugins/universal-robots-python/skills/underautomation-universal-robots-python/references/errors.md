# Errors of the Universal Robots SDK (Python)

SDK version 9.4.0. The exceptions of the SDK, and the pages that describe when they are raised. The message of an exception says what failed: read it first, then the page of the feature.

The SDK raises the .NET exception. It is a Python exception: catch it with `except Exception as e` and read `str(e)`, or catch its .NET type, imported from its .NET namespace as shown below (the package loads the .NET library first).

Its members keep their .NET names: `e.Message`, `e.InnerException`. The classes of the same name in the `underautomation.universal_robots` modules are not Python exceptions: `except` on one of them raises a `TypeError`. The reference of each exception lists its members.

## ConnectException

Exception thrown when connection to the robot fails

Catch: `from UnderAutomation.UniversalRobots.Common import ConnectException`, then `except ConnectException as e`.

Reference: [underautomation.universal_robots.common](api/underautomation.universal_robots.common.md#connectexception)

Pages that describe it: [get-started-python](pages/get-started-python.md), [connect](pages/connect.md), [how-to-get-position](pages/how-to-get-position.md), [how-to-transfer-files](pages/how-to-transfer-files.md).

## RtdeOverrunException

Exception thrown when RTDE data cannot be consumed fast enough, causing the input buffer to fill up. This typically occurs when the OutputDataReceived event handler takes longer to execute than the interval between RTDE messages.

Catch: `from UnderAutomation.UniversalRobots.Internal import RtdeOverrunException`, then `except RtdeOverrunException as e`.

Reference: [underautomation.universal_robots.internal](api/underautomation.universal_robots.internal.md#rtdeoverrunexception)

## InvalidLicenseException

Exception thrown while using the product if the license is not valid.

Catch: `from UnderAutomation.UniversalRobots.License import InvalidLicenseException`, then `except InvalidLicenseException as e`.

Reference: [underautomation.universal_robots.license](api/underautomation.universal_robots.license.md#invalidlicenseexception)

Pages that describe it: [get-started-python](pages/get-started-python.md), [connect](pages/connect.md), [license](pages/license.md).

## SftpPathNotFoundException

The exception that is thrown when file or directory is not found.

Catch: `from UnderAutomation.UniversalRobots.Ssh.Tools.Common import SftpPathNotFoundException`, then `except SftpPathNotFoundException as e`.

Reference: [underautomation.universal_robots.ssh.tools.common](api/underautomation.universal_robots.ssh.tools.common.md#sftppathnotfoundexception)

Pages that describe it: [how-to-transfer-files](pages/how-to-transfer-files.md).

## SftpPermissionDeniedException

The exception that is thrown when operation permission is denied.

Catch: `from UnderAutomation.UniversalRobots.Ssh.Tools.Common import SftpPermissionDeniedException`, then `except SftpPermissionDeniedException as e`.

Reference: [underautomation.universal_robots.ssh.tools.common](api/underautomation.universal_robots.ssh.tools.common.md#sftppermissiondeniedexception)

## SshAuthenticationException

The exception that is thrown when authentication failed.

Catch: `from UnderAutomation.UniversalRobots.Ssh.Tools.Common import SshAuthenticationException`, then `except SshAuthenticationException as e`.

Reference: [underautomation.universal_robots.ssh.tools.common](api/underautomation.universal_robots.ssh.tools.common.md#sshauthenticationexception)

Pages that describe it: [how-to-transfer-files](pages/how-to-transfer-files.md).

## SshConnectionException

The exception that is thrown when connection was terminated.

Catch: `from UnderAutomation.UniversalRobots.Ssh.Tools.Common import SshConnectionException`, then `except SshConnectionException as e`.

Reference: [underautomation.universal_robots.ssh.tools.common](api/underautomation.universal_robots.ssh.tools.common.md#sshconnectionexception)

## SshException

The exception that is thrown when SSH exception occurs.

Catch: `from UnderAutomation.UniversalRobots.Ssh.Tools.Common import SshException`, then `except SshException as e`.

Reference: [underautomation.universal_robots.ssh.tools.common](api/underautomation.universal_robots.ssh.tools.common.md#sshexception)

## SshOperationTimeoutException

The exception that is thrown when operation is timed out.

Catch: `from UnderAutomation.UniversalRobots.Ssh.Tools.Common import SshOperationTimeoutException`, then `except SshOperationTimeoutException as e`.

Reference: [underautomation.universal_robots.ssh.tools.common](api/underautomation.universal_robots.ssh.tools.common.md#sshoperationtimeoutexception)

## SshPassPhraseNullOrEmptyException

The exception that is thrown when pass phrase for key file is empty or null

Catch: `from UnderAutomation.UniversalRobots.Ssh.Tools.Common import SshPassPhraseNullOrEmptyException`, then `except SshPassPhraseNullOrEmptyException as e`.

Reference: [underautomation.universal_robots.ssh.tools.common](api/underautomation.universal_robots.ssh.tools.common.md#sshpassphrasenulloremptyexception)
