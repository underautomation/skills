# UnderAutomation.Fanuc.Snpx.Assignment

## CommentBatchAssignment

`class CommentBatchAssignment : BatchAssignment<string, CommentData>`

Batch assignment for reading multiple comments at once.

- `CommentBatchAssignment()`: Initializes a new instance of the Assignment.CommentBatchAssignment class.
- `string[] Read()`: Reads all comments assigned in this batch.
- `Assignment<CommentData>[] Assignments`: The assignments included in this batch.

## FlagBatchAssignment

`class FlagBatchAssignment : BatchAssignment<bool, int>`

Batch assignment for reading multiple flag values at once.

- `FlagBatchAssignment()`: Initializes a new instance of the Assignment.FlagBatchAssignment class.
- `bool[] Read()`: Reads all flag values assigned in this batch.
- `Assignment<int>[] Assignments`: The assignments included in this batch.

## IntegerSystemVariablesBatchAssignment

`class IntegerSystemVariablesBatchAssignment : BatchAssignment<int, string>`

Batch assignment for reading multiple integer system variables at once.

- `IntegerSystemVariablesBatchAssignment()`: Initializes a new instance of the Assignment.IntegerSystemVariablesBatchAssignment class.
- `int[] Read()`: Reads all integer system variables assigned in this batch.
- `Assignment<string>[] Assignments`: The assignments included in this batch.

## NumericRegistersBatchAssignment

`class NumericRegistersBatchAssignment : BatchAssignment<float, int>`

Batch assignment for reading multiple numeric registers at once as float

- `NumericRegistersBatchAssignment()`: Initializes a new instance of the Assignment.NumericRegistersBatchAssignment class.
- `float[] Read()`: Read all numeric registers assigned in this batch assignment.
- `Assignment<int>[] Assignments`: The assignments included in this batch.

## NumericRegistersInt16BatchAssignment

`class NumericRegistersInt16BatchAssignment : BatchAssignment<short, int>`

Batch assignment for reading multiple numeric registers at once as 16-bit integers.

- `NumericRegistersInt16BatchAssignment()`: Initializes a new instance of the Assignment.NumericRegistersInt16BatchAssignment class.
- `short[] Read()`: Read all numeric registers assigned in this batch assignment.
- `Assignment<int>[] Assignments`: The assignments included in this batch.

## NumericRegistersInt32BatchAssignment

`class NumericRegistersInt32BatchAssignment : BatchAssignment<int, int>`

Batch assignment for reading multiple numeric registers at once as 32-bit integers.

- `NumericRegistersInt32BatchAssignment()`: Initializes a new instance of the Assignment.NumericRegistersInt32BatchAssignment class.
- `int[] Read()`: Read all numeric registers assigned in this batch assignment.
- `Assignment<int>[] Assignments`: The assignments included in this batch.

## PositionRegistersBatchAssignment

`class PositionRegistersBatchAssignment : BatchAssignment<Position, int>`

Batch assignment for reading multiple position registers at once.

- `PositionRegistersBatchAssignment()`: Initializes a new instance of the Assignment.PositionRegistersBatchAssignment class.
- `Position[] Read()`: Reads all position registers assigned in this batch.
- `Assignment<int>[] Assignments`: The assignments included in this batch.

## PositionSystemVariablesBatchAssignment

`class PositionSystemVariablesBatchAssignment : BatchAssignment<Position, string>`

Batch assignment for reading multiple position system variables at once.

- `PositionSystemVariablesBatchAssignment()`: Initializes a new instance of the Assignment.PositionSystemVariablesBatchAssignment class.
- `Position[] Read()`: Reads all position system variables assigned in this batch.
- `Assignment<string>[] Assignments`: The assignments included in this batch.

## RealSystemVariablesBatchAssignment

`class RealSystemVariablesBatchAssignment : BatchAssignment<float, string>`

Batch assignment for reading multiple real (float) system variables at once.

- `RealSystemVariablesBatchAssignment()`: Initializes a new instance of the Assignment.RealSystemVariablesBatchAssignment class.
- `float[] Read()`: Reads all real system variables assigned in this batch.
- `Assignment<string>[] Assignments`: The assignments included in this batch.

## SimulationStatusBatchAssignment

`class SimulationStatusBatchAssignment : BatchAssignment<bool, SimulationData>`

Batch assignment for reading multiple I/O simulation statuses at once.

- `SimulationStatusBatchAssignment()`: Initializes a new instance of the Assignment.SimulationStatusBatchAssignment class.
- `bool[] Read()`: Reads all simulation statuses assigned in this batch.
- `Assignment<SimulationData>[] Assignments`: The assignments included in this batch.

## StringRegistersBatchAssignment

`class StringRegistersBatchAssignment : BatchAssignment<string, int>`

Batch assignment for reading multiple string registers at once.

- `StringRegistersBatchAssignment()`: Initializes a new instance of the Assignment.StringRegistersBatchAssignment class.
- `string[] Read()`: Reads all string registers assigned in this batch.
- `Assignment<int>[] Assignments`: The assignments included in this batch.

## StringSystemVariablesBatchAssignment

`class StringSystemVariablesBatchAssignment : BatchAssignment<string, string>`

Batch assignment for reading multiple string system variables at once.

- `StringSystemVariablesBatchAssignment()`: Initializes a new instance of the Assignment.StringSystemVariablesBatchAssignment class.
- `string[] Read()`: Reads all string system variables assigned in this batch.
- `Assignment<string>[] Assignments`: The assignments included in this batch.
