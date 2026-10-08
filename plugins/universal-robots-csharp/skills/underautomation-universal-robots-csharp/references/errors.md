# Errors of the Universal Robots SDK (C#)

SDK version 9.4.0. The exceptions of the SDK, and the pages that describe when they are thrown. The message of an exception says what failed: read it first, then the page of the feature.

## ConnectException

`class ConnectException : Exception, ISerializable`

Exception thrown when connection to the robot fails

Reference: [UnderAutomation.UniversalRobots.Common](api/UnderAutomation.UniversalRobots.Common.md#connectexception)

Pages that describe it: [connect](pages/connect.md), [how-to-get-position](pages/how-to-get-position.md), [how-to-transfer-files](pages/how-to-transfer-files.md).

## RtdeOverrunException

`class RtdeOverrunException : Exception, ISerializable`

Exception thrown when RTDE data cannot be consumed fast enough, causing the input buffer to fill up. This typically occurs when the OutputDataReceived event handler takes longer to execute than the interval between RTDE messages.

Reference: [UnderAutomation.UniversalRobots.Internal](api/UnderAutomation.UniversalRobots.Internal.md#rtdeoverrunexception)

## InvalidLicenseException

`class InvalidLicenseException : Exception, ISerializable`

Exception thrown while using the product if the license is not valid.

Reference: [UnderAutomation.UniversalRobots.License](api/UnderAutomation.UniversalRobots.License.md#invalidlicenseexception)

Pages that describe it: [connect](pages/connect.md), [license](pages/license.md).

## SftpPathNotFoundException

`class SftpPathNotFoundException : SshException, ISerializable`

The exception that is thrown when file or directory is not found.

Reference: [UnderAutomation.UniversalRobots.Ssh.Tools.Common](api/UnderAutomation.UniversalRobots.Ssh.Tools.Common.md#sftppathnotfoundexception)

Pages that describe it: [how-to-transfer-files](pages/how-to-transfer-files.md).

## SftpPermissionDeniedException

`class SftpPermissionDeniedException : SshException, ISerializable`

The exception that is thrown when operation permission is denied.

Reference: [UnderAutomation.UniversalRobots.Ssh.Tools.Common](api/UnderAutomation.UniversalRobots.Ssh.Tools.Common.md#sftppermissiondeniedexception)

## SshAuthenticationException

`class SshAuthenticationException : SshException, ISerializable`

The exception that is thrown when authentication failed.

Reference: [UnderAutomation.UniversalRobots.Ssh.Tools.Common](api/UnderAutomation.UniversalRobots.Ssh.Tools.Common.md#sshauthenticationexception)

Pages that describe it: [how-to-transfer-files](pages/how-to-transfer-files.md).

## SshConnectionException

`class SshConnectionException : SshException, ISerializable`

The exception that is thrown when connection was terminated.

Reference: [UnderAutomation.UniversalRobots.Ssh.Tools.Common](api/UnderAutomation.UniversalRobots.Ssh.Tools.Common.md#sshconnectionexception)

## SshException

`class SshException : Exception, ISerializable`

The exception that is thrown when SSH exception occurs.

Reference: [UnderAutomation.UniversalRobots.Ssh.Tools.Common](api/UnderAutomation.UniversalRobots.Ssh.Tools.Common.md#sshexception)

## SshOperationTimeoutException

`class SshOperationTimeoutException : SshException, ISerializable`

The exception that is thrown when operation is timed out.

Reference: [UnderAutomation.UniversalRobots.Ssh.Tools.Common](api/UnderAutomation.UniversalRobots.Ssh.Tools.Common.md#sshoperationtimeoutexception)

## SshPassPhraseNullOrEmptyException

`class SshPassPhraseNullOrEmptyException : SshException, ISerializable`

The exception that is thrown when pass phrase for key file is empty or null

Reference: [UnderAutomation.UniversalRobots.Ssh.Tools.Common](api/UnderAutomation.UniversalRobots.Ssh.Tools.Common.md#sshpassphrasenulloremptyexception)
