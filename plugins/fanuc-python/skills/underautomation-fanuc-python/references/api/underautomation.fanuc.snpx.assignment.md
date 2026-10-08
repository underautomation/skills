# underautomation.fanuc.snpx.assignment

## CommentBatchAssignment

`from underautomation.fanuc.snpx.assignment.comment_batch_assignment import CommentBatchAssignment`

Batch assignment for reading multiple comments at once.

- `CommentBatchAssignment()`: Initializes a new instance of the CommentBatchAssignment class.
- `read() -> typing.List[str]`: Reads all comments assigned in this batch.
- `assignments: typing.List[Assignment1]`: The assignments included in this batch.

## FlagBatchAssignment

`from underautomation.fanuc.snpx.assignment.flag_batch_assignment import FlagBatchAssignment`

Batch assignment for reading multiple flag values at once.

- `FlagBatchAssignment()`: Initializes a new instance of the FlagBatchAssignment class.
- `read() -> typing.List[bool]`: Reads all flag values assigned in this batch.
- `assignments: typing.List[Assignment1]`: The assignments included in this batch.

## IntegerSystemVariablesBatchAssignment

`from underautomation.fanuc.snpx.assignment.integer_system_variables_batch_assignment import IntegerSystemVariablesBatchAssignment`

Batch assignment for reading multiple integer system variables at once.

- `IntegerSystemVariablesBatchAssignment()`: Initializes a new instance of the IntegerSystemVariablesBatchAssignment class.
- `read() -> typing.List[int]`: Reads all integer system variables assigned in this batch.
- `assignments: typing.List[Assignment1]`: The assignments included in this batch.

## NumericRegistersBatchAssignment

`from underautomation.fanuc.snpx.assignment.numeric_registers_batch_assignment import NumericRegistersBatchAssignment`

Batch assignment for reading multiple numeric registers at once as float

- `NumericRegistersBatchAssignment()`: Initializes a new instance of the NumericRegistersBatchAssignment class.
- `read() -> typing.List[float]`: Read all numeric registers assigned in this batch assignment.
- `assignments: typing.List[Assignment1]`: The assignments included in this batch.

## NumericRegistersInt16BatchAssignment

`from underautomation.fanuc.snpx.assignment.numeric_registers_int16_batch_assignment import NumericRegistersInt16BatchAssignment`

Batch assignment for reading multiple numeric registers at once as 16-bit integers.

- `NumericRegistersInt16BatchAssignment()`: Initializes a new instance of the NumericRegistersInt16BatchAssignment class.
- `read() -> typing.List[int]`: Read all numeric registers assigned in this batch assignment.
- `assignments: typing.List[Assignment1]`: The assignments included in this batch.

## NumericRegistersInt32BatchAssignment

`from underautomation.fanuc.snpx.assignment.numeric_registers_int32_batch_assignment import NumericRegistersInt32BatchAssignment`

Batch assignment for reading multiple numeric registers at once as 32-bit integers.

- `NumericRegistersInt32BatchAssignment()`: Initializes a new instance of the NumericRegistersInt32BatchAssignment class.
- `read() -> typing.List[int]`: Read all numeric registers assigned in this batch assignment.
- `assignments: typing.List[Assignment1]`: The assignments included in this batch.

## PositionRegistersBatchAssignment

`from underautomation.fanuc.snpx.assignment.position_registers_batch_assignment import PositionRegistersBatchAssignment`

Batch assignment for reading multiple position registers at once.

- `PositionRegistersBatchAssignment()`: Initializes a new instance of the PositionRegistersBatchAssignment class.
- `read() -> typing.List[Position]`: Reads all position registers assigned in this batch.
- `assignments: typing.List[Assignment1]`: The assignments included in this batch.

## PositionSystemVariablesBatchAssignment

`from underautomation.fanuc.snpx.assignment.position_system_variables_batch_assignment import PositionSystemVariablesBatchAssignment`

Batch assignment for reading multiple position system variables at once.

- `PositionSystemVariablesBatchAssignment()`: Initializes a new instance of the PositionSystemVariablesBatchAssignment class.
- `read() -> typing.List[Position]`: Reads all position system variables assigned in this batch.
- `assignments: typing.List[Assignment1]`: The assignments included in this batch.

## RealSystemVariablesBatchAssignment

`from underautomation.fanuc.snpx.assignment.real_system_variables_batch_assignment import RealSystemVariablesBatchAssignment`

Batch assignment for reading multiple real (float) system variables at once.

- `RealSystemVariablesBatchAssignment()`: Initializes a new instance of the RealSystemVariablesBatchAssignment class.
- `read() -> typing.List[float]`: Reads all real system variables assigned in this batch.
- `assignments: typing.List[Assignment1]`: The assignments included in this batch.

## SimulationStatusBatchAssignment

`from underautomation.fanuc.snpx.assignment.simulation_status_batch_assignment import SimulationStatusBatchAssignment`

Batch assignment for reading multiple I/O simulation statuses at once.

- `SimulationStatusBatchAssignment()`: Initializes a new instance of the SimulationStatusBatchAssignment class.
- `read() -> typing.List[bool]`: Reads all simulation statuses assigned in this batch.
- `assignments: typing.List[Assignment1]`: The assignments included in this batch.

## StringRegistersBatchAssignment

`from underautomation.fanuc.snpx.assignment.string_registers_batch_assignment import StringRegistersBatchAssignment`

Batch assignment for reading multiple string registers at once.

- `StringRegistersBatchAssignment()`: Initializes a new instance of the StringRegistersBatchAssignment class.
- `read() -> typing.List[str]`: Reads all string registers assigned in this batch.
- `assignments: typing.List[Assignment1]`: The assignments included in this batch.

## StringSystemVariablesBatchAssignment

`from underautomation.fanuc.snpx.assignment.string_system_variables_batch_assignment import StringSystemVariablesBatchAssignment`

Batch assignment for reading multiple string system variables at once.

- `StringSystemVariablesBatchAssignment()`: Initializes a new instance of the StringSystemVariablesBatchAssignment class.
- `read() -> typing.List[str]`: Reads all string system variables assigned in this batch.
- `assignments: typing.List[Assignment1]`: The assignments included in this batch.
