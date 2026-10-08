# Errors of the Yaskawa SDK (C#)

SDK version 3.0.1. The exceptions of the SDK, and the pages that describe when they are thrown. The message of an exception says what failed: read it first, then the page of the feature.

## ConnectException

`class ConnectException : Exception, ISerializable`

Exception thrown when connection to a Yaskawa robot fails

Reference: [UnderAutomation.Yaskawa.Common](api/UnderAutomation.Yaskawa.Common.md#connectexception)

Pages that describe it: [connect](pages/connect.md).

## FtpException

`class FtpException : Exception, ISerializable`

Exception thrown when an FTP operation on the Yaskawa controller fails. The message explains the cause and, when the logged user does not have enough rights, which user to use.

Reference: [UnderAutomation.Yaskawa.Ftp](api/UnderAutomation.Yaskawa.Ftp.md#ftpexception)

Pages that describe it: [connect](pages/connect.md), [ftp](pages/ftp.md).

## InvalidDataAnswerException

`class InvalidDataAnswerException : Exception, ISerializable`

Exception thrown when the robot controller returns an error response to a High Speed Ethernet Server command. This exception contains detailed status codes that help identify the specific error condition.

Reference: [UnderAutomation.Yaskawa.HighSpeedEServer](api/UnderAutomation.Yaskawa.HighSpeedEServer.md#invaliddataanswerexception)

Pages that describe it: [connect](pages/connect.md), [high-speed-ethernet-server](pages/high-speed-ethernet-server.md), [hses-variables](pages/hses-variables.md), [hses-files](pages/hses-files.md), [how-to-read-write-variables](pages/how-to-read-write-variables.md).

## HostControlException

`class HostControlException : Exception, ISerializable`

Exception thrown when a Host Control command fails.

Reference: [UnderAutomation.Yaskawa.HostControl](api/UnderAutomation.Yaskawa.HostControl.md#hostcontrolexception)

Pages that describe it: [connect](pages/connect.md), [ethernet-server](pages/ethernet-server.md), [eserver-jobs](pages/eserver-jobs.md), [eserver-variables-io](pages/eserver-variables-io.md).

## InvalidLicenseException

`class InvalidLicenseException : Exception, ISerializable`

Exception thrown while using the product if the license is not valid.

Reference: [UnderAutomation.Yaskawa.License](api/UnderAutomation.Yaskawa.License.md#invalidlicenseexception)

Pages that describe it: [connect](pages/connect.md), [license](pages/license.md).
