# UnderAutomation.Staubli.Soap.Errors

## CustomSoapException

`class CustomSoapException : Exception, ISerializable`

Custom exception class for handling SOAP errors with specific error codes and descriptions.

- `string Description { get; }`: A human-readable description of the error, providing additional context about the failure.
- `SoapErrorCode ErrorCode { get; }`: The error code as an enum value, parsed from the ErrorCodeText.
- `string ErrorCodeText { get; }`: The error code text as received from the SOAP response, formatted as a kebab-case string.
- `string Message { get; }`: Gets the error message that describes the current exception.

## SoapErrorCode

`enum SoapErrorCode`

Error codes returned by the SOAP service.

- ApplicationNotFound: The specified application was not found.
- CannotStartApplication: Cannot start the application.
- ClientAlreadyConnected: A client is already connected.
- ClientCommunicationError: Client communication error.
- InvalidCredentials: The provided credentials are invalid.
- InvalidRobotIdCode: The specified robot ID is invalid.
- InvalidSessionIdCode: The session ID is invalid or expired.
- IoWriteAccessErrorCode: I/O write access error.
- IoWriteAccessErrorValidation: I/O write access validation error.
- IoWriteAccessErrorWorkingMode: I/O write access error due to working mode.
- MismatchedCode: Mismatched code error.
- ProgramLineNotFound: The specified program line was not found.
- ProgramNotFound: The specified program was not found.
- ReadAccessErrorCode: Read access error.
- SchedulingModeError: Scheduling mode error.
- SetPosNotSimulCode: Cannot set position outside simulation mode.
- SinReturnCodeNok: SIN return code indicates failure.
- StackFrameNotFound: The specified stack frame was not found.
- TaskAlreadyLocked: The task is already locked by another client.
- TaskNotFound: The specified task was not found.
- Unknown: Unknown or unrecognized error code.
- WriteAccessErrorCode: Write access error.

## StartApplicationError

`enum StartApplicationError`

Error codes that can occur when starting an application on the controller.

- DataAlreadyExists: The data already exists.
- DataBusy: The data is currently busy.
- DataInvalidName: The data name is invalid.
- DataInvalidSize: The data size is invalid.
- DataNotAnArray: The data is not an array.
- DataNotFound: The required data was not found.
- LibraryBusy: The library is currently busy.
- LibraryInvalidZip: The library ZIP file is invalid.
- MemoryFull: Not enough memory to start the application.
- ProjectAliasAlreadyUsed: The project alias is already in use.
- ProjectAlreadyEnding: The project is already ending.
- ProjectAlreadyExists: The project already exists.
- ProjectAlreadyRunning: The project is already running.
- ProjectBusy: The project is currently busy.
- ProjectCircularReference: A circular reference was detected in the project.
- ProjectCodeError: A code error occurred in the project.
- ProjectDataError: A data error occurred in the project.
- ProjectDefaultStackTooSmall: The default stack size is too small.
- ProjectFileError: A file error occurred in the project.
- ProjectFilemanagerNotFound: The file manager was not found.
- ProjectInconsistantResolvedSymbol: An inconsistent resolved symbol was found.
- ProjectInterfaceStillUsed: An interface is still in use.
- ProjectInterfaceTaskNotKilled: An interface task has not been killed.
- ProjectInvalidAlias: The project alias is invalid.
- ProjectInvalidDestructor: The project destructor is invalid.
- ProjectInvalidMain: The project main entry point is invalid.
- ProjectInvalidName: The project name is invalid.
- ProjectInvalidProject: The project is invalid.
- ProjectInvalidTypename: The type name is invalid.
- ProjectLibraryError: A library error occurred in the project.
- ProjectLocked: The project is locked.
- ProjectTypeBusy: The type is currently busy.
- ProjectTypeProjectError: A type project error occurred.
- ProjectTypenameAlreadyUsed: The type name is already in use.
- ProjectUnresolvedSymbol: An unresolved symbol was found in the project.
- ProjectUsedAsStruct: The project is used as a struct.
- RoutineAlreadyExists: The routine already exists.
- RoutineBusy: The routine is currently busy.
- RoutineInvalidName: The routine name is invalid.
- RoutineInvalidParamPosition: The routine parameter position is invalid.
- RoutineNameTooLong: The routine name is too long.
- RoutineNotFound: The routine was not found.
- StartRoutineNotFound: The start routine was not found.
- StopRoutineNotFound: The stop routine was not found.
