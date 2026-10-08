# Errors of the Staubli SDK (C#)

SDK version 1.0.0. The exceptions of the SDK, and the pages that describe when they are thrown. The message of an exception says what failed: read it first, then the page of the feature.

## FileException

`class FileException : Exception, ISerializable`

Exception thrown when an operation on the files of the controller fails: the controller refused it, the file does not exist, or the communication failed. The message gives the reason and, when it is known, what to do.

Reference: [UnderAutomation.Staubli.Files](api/UnderAutomation.Staubli.Files.md#fileexception)

Pages that describe it: [simulator](pages/simulator.md), [files-overview](pages/files-overview.md), [files-transfer](pages/files-transfer.md), [files-applications](pages/files-applications.md).

## InvalidLicenseException

`class InvalidLicenseException : Exception, ISerializable`

Exception thrown while using the product if the license is not valid.

Reference: [UnderAutomation.Staubli.License](api/UnderAutomation.Staubli.License.md#invalidlicenseexception)

Pages that describe it: [connect](pages/connect.md), [license](pages/license.md).

## CustomSoapException

`class CustomSoapException : Exception, ISerializable`

Custom exception class for handling SOAP errors with specific error codes and descriptions.

Reference: [UnderAutomation.Staubli.Soap.Errors](api/UnderAutomation.Staubli.Soap.Errors.md#customsoapexception)

Pages that describe it: [connect](pages/connect.md), [soap-applications](pages/soap-applications.md), [soap-tasks](pages/soap-tasks.md), [how-to-run-program](pages/how-to-run-program.md), [how-to-monitor-state](pages/how-to-monitor-state.md).
