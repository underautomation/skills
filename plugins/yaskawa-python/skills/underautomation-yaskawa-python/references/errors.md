# Errors of the Yaskawa SDK (Python)

SDK version 3.0.1. The exceptions of the SDK, and the pages that describe when they are raised. The message of an exception says what failed: read it first, then the page of the feature.

The SDK raises the .NET exception. It is a Python exception: catch it with `except Exception as e` and read `str(e)`, or catch its .NET type, imported from its .NET namespace as shown below (the package loads the .NET library first).

Its members keep their .NET names: `e.Message`, `e.InnerException`. The classes of the same name in the `underautomation.yaskawa` modules are not Python exceptions: `except` on one of them raises a `TypeError`. The reference of each exception lists its members.

## ConnectException

Exception thrown when connection to a Yaskawa robot fails

Catch: `from UnderAutomation.Yaskawa.Common import ConnectException`, then `except ConnectException as e`.

Reference: [underautomation.yaskawa.common](api/underautomation.yaskawa.common.md#connectexception)

Pages that describe it: [get-started-python](pages/get-started-python.md), [connect](pages/connect.md).

## FtpException

Exception thrown when an FTP operation on the Yaskawa controller fails. The message explains the cause and, when the logged user does not have enough rights, which user to use.

Catch: `from UnderAutomation.Yaskawa.Ftp import FtpException`, then `except FtpException as e`.

Reference: [underautomation.yaskawa.ftp](api/underautomation.yaskawa.ftp.md#ftpexception)

Pages that describe it: [connect](pages/connect.md), [ftp](pages/ftp.md).

## InvalidDataAnswerException

Exception thrown when the robot controller returns an error response to a High Speed Ethernet Server command. This exception contains detailed status codes that help identify the specific error condition.

Catch: `from UnderAutomation.Yaskawa.HighSpeedEServer import InvalidDataAnswerException`, then `except InvalidDataAnswerException as e`.

Reference: [underautomation.yaskawa.high_speed_e_server](api/underautomation.yaskawa.high_speed_e_server.md#invaliddataanswerexception)

Pages that describe it: [get-started-python](pages/get-started-python.md), [connect](pages/connect.md), [high-speed-ethernet-server](pages/high-speed-ethernet-server.md), [hses-variables](pages/hses-variables.md), [hses-files](pages/hses-files.md), [how-to-read-write-variables](pages/how-to-read-write-variables.md).

## HostControlException

Exception thrown when a Host Control command fails.

Catch: `from UnderAutomation.Yaskawa.HostControl import HostControlException`, then `except HostControlException as e`.

Reference: [underautomation.yaskawa.host_control](api/underautomation.yaskawa.host_control.md#hostcontrolexception)

Pages that describe it: [connect](pages/connect.md), [ethernet-server](pages/ethernet-server.md), [eserver-jobs](pages/eserver-jobs.md), [eserver-variables-io](pages/eserver-variables-io.md).

## InvalidLicenseException

Exception thrown while using the product if the license is not valid.

Catch: `from UnderAutomation.Yaskawa.License import InvalidLicenseException`, then `except InvalidLicenseException as e`.

Reference: [underautomation.yaskawa.license](api/underautomation.yaskawa.license.md#invalidlicenseexception)

Pages that describe it: [get-started-python](pages/get-started-python.md), [connect](pages/connect.md), [license](pages/license.md).
