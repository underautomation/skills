# Errors of the Staubli SDK (Python)

SDK version 1.0.0. The exceptions of the SDK, and the pages that describe when they are raised. The message of an exception says what failed: read it first, then the page of the feature.

The SDK raises the .NET exception. It is a Python exception: catch it with `except Exception as e` and read `str(e)`, or catch its .NET type, imported from its .NET namespace as shown below (the package loads the .NET library first).

Its members keep their .NET names: `e.Message`, `e.InnerException`. The classes of the same name in the `underautomation.staubli` modules are not Python exceptions: `except` on one of them raises a `TypeError`. The reference of each exception lists its members.

## FileException

Exception thrown when an operation on the files of the controller fails: the controller refused it, the file does not exist, or the communication failed. The message gives the reason and, when it is known, what to do.

Catch: `from UnderAutomation.Staubli.Files import FileException`, then `except FileException as e`.

Reference: [underautomation.staubli.files](api/underautomation.staubli.files.md#fileexception)

Pages that describe it: [simulator](pages/simulator.md), [files-overview](pages/files-overview.md), [files-transfer](pages/files-transfer.md), [files-applications](pages/files-applications.md).

## InvalidLicenseException

Exception thrown while using the product if the license is not valid.

Catch: `from UnderAutomation.Staubli.License import InvalidLicenseException`, then `except InvalidLicenseException as e`.

Reference: [underautomation.staubli.license](api/underautomation.staubli.license.md#invalidlicenseexception)

Pages that describe it: [get-started-python](pages/get-started-python.md), [connect](pages/connect.md), [license](pages/license.md).

## CustomSoapException

Custom exception class for handling SOAP errors with specific error codes and descriptions.

Catch: `from UnderAutomation.Staubli.Soap.Errors import CustomSoapException`, then `except CustomSoapException as e`.

Reference: [underautomation.staubli.soap.errors](api/underautomation.staubli.soap.errors.md#customsoapexception)

Pages that describe it: [get-started-python](pages/get-started-python.md), [connect](pages/connect.md), [soap-applications](pages/soap-applications.md), [soap-tasks](pages/soap-tasks.md), [how-to-run-program](pages/how-to-run-program.md), [how-to-monitor-state](pages/how-to-monitor-state.md).
