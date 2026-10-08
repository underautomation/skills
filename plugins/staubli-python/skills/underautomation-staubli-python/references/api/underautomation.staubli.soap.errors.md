# underautomation.staubli.soap.errors

## CustomSoapException

`from UnderAutomation.Staubli.Soap.Errors import CustomSoapException`

Custom exception class for handling SOAP errors with specific error codes and descriptions.

The SDK raises this .NET type: catch it with `except CustomSoapException as e` after the import above. Its members keep their .NET names. The class `CustomSoapException` of the module `underautomation.staubli.soap.errors.custom_soap_exception` is not a Python exception and cannot be caught.

- `ErrorCodeText: str (read only)`: The error code text as received from the SOAP response, formatted as a kebab-case string.
- `ErrorCode: SoapErrorCode (read only)`: The error code as an enum value, parsed from the ErrorCodeText.
- `Description: str (read only)`: A human-readable description of the error, providing additional context about the failure.
- `Message: str (read only)`: Gets the error message that describes the current exception.
- Inherited from System.Exception: `InnerException`

## SoapErrorCode

`from underautomation.staubli.soap.errors.soap_error_code import SoapErrorCode`

Error codes returned by the SOAP service.

- Unknown: Unknown or unrecognized error code.
- InvalidCredentials: The provided credentials are invalid.
- TaskNotFound: The specified task was not found.
- MismatchedCode: Mismatched code error.
- ProgramNotFound: The specified program was not found.
- TaskAlreadyLocked: The task is already locked by another client.
- SinReturnCodeNok: SIN return code indicates failure.
- SchedulingModeError: Scheduling mode error.
- ApplicationNotFound: The specified application was not found.
- StackFrameNotFound: The specified stack frame was not found.
- ProgramLineNotFound: The specified program line was not found.
- ReadAccessErrorCode: Read access error.
- SetPosNotSimulCode: Cannot set position outside simulation mode.
- InvalidSessionIdCode: The session ID is invalid or expired.
- WriteAccessErrorCode: Write access error.
- CannotStartApplication: Cannot start the application.
- ClientAlreadyConnected: A client is already connected.
- IoWriteAccessErrorCode: I/O write access error.
- ClientCommunicationError: Client communication error.
- IoWriteAccessErrorValidation: I/O write access validation error.
- IoWriteAccessErrorWorkingMode: I/O write access error due to working mode.
- InvalidRobotIdCode: The specified robot ID is invalid.

## StartApplicationError

`from underautomation.staubli.soap.errors.start_application_error import StartApplicationError`

Error codes that can occur when starting an application on the controller.

- MemoryFull: Not enough memory to start the application.
- LibraryBusy: The library is currently busy.
- LibraryInvalidZip: The library ZIP file is invalid.
- DataNotFound: The required data was not found.
- DataBusy: The data is currently busy.
- DataInvalidName: The data name is invalid.
- DataAlreadyExists: The data already exists.
- DataInvalidSize: The data size is invalid.
- DataNotAnArray: The data is not an array.
- RoutineInvalidName: The routine name is invalid.
- RoutineAlreadyExists: The routine already exists.
- RoutineNameTooLong: The routine name is too long.
- RoutineInvalidParamPosition: The routine parameter position is invalid.
- RoutineNotFound: The routine was not found.
- RoutineBusy: The routine is currently busy.
- ProjectBusy: The project is currently busy.
- ProjectInvalidName: The project name is invalid.
- ProjectInvalidAlias: The project alias is invalid.
- ProjectAliasAlreadyUsed: The project alias is already in use.
- ProjectAlreadyExists: The project already exists.
- ProjectCodeError: A code error occurred in the project.
- ProjectDataError: A data error occurred in the project.
- StartRoutineNotFound: The start routine was not found.
- ProjectInvalidMain: The project main entry point is invalid.
- ProjectInvalidProject: The project is invalid.
- StopRoutineNotFound: The stop routine was not found.
- ProjectInvalidDestructor: The project destructor is invalid.
- ProjectDefaultStackTooSmall: The default stack size is too small.
- ProjectAlreadyRunning: The project is already running.
- ProjectAlreadyEnding: The project is already ending.
- ProjectLocked: The project is locked.
- ProjectFileError: A file error occurred in the project.
- ProjectFilemanagerNotFound: The file manager was not found.
- ProjectLibraryError: A library error occurred in the project.
- ProjectUnresolvedSymbol: An unresolved symbol was found in the project.
- ProjectInconsistantResolvedSymbol: An inconsistent resolved symbol was found.
- ProjectInterfaceStillUsed: An interface is still in use.
- ProjectUsedAsStruct: The project is used as a struct.
- ProjectInterfaceTaskNotKilled: An interface task has not been killed.
- ProjectInvalidTypename: The type name is invalid.
- ProjectTypenameAlreadyUsed: The type name is already in use.
- ProjectTypeProjectError: A type project error occurred.
- ProjectTypeBusy: The type is currently busy.
- ProjectCircularReference: A circular reference was detected in the project.
