# UnderAutomation.Fanuc.Cgtp.BatchVariables

## CgtpBatchReadResult

`class CgtpBatchReadResult`

Result of a batch read operation.

- `string Version { get; }`: Firmware version string returned by the controller

## CgtpBatchVariables

`class CgtpBatchVariables : IList<ICgtpBatchVariable>, ICollection<ICgtpBatchVariable>, IEnumerable<ICgtpBatchVariable>, IEnumerable`

Collection of batch variables to read from or write to the controller in a single operation. Provides convenience methods to add typed variables.

- `CgtpBatchVariables()`
- `void Add(ICgtpBatchVariable item)`
- `CgtpNumericRegister AddNumericRegister(int index)`: Add a numeric register for reading. The value and comment will be populated after a batch read.
- `CgtpNumericRegister AddNumericRegisterAsInteger(int index, string comment, int value)`: Add a numeric register with an integer value and comment for writing.
- `CgtpNumericRegister AddNumericRegisterAsReal(int index, string comment, double value)`: Add a numeric register with a real (double) value and comment for writing.
- `CgtpPositionRegister AddPositionRegister(int index, int group = 1)`: Add a position register for reading. The position data will be populated after a batch read.
- `CgtpPositionRegister AddPositionRegisterAsCartesian(int index, CartesianPosition position, int group = 1, string comment = null)`: Add a position register with a Cartesian position for writing.
- `CgtpPositionRegister AddPositionRegisterAsJoint(int index, JointsPosition position, int group = 1, string comment = null)`: Add a position register with a joint position for writing.
- `void AddRange(IEnumerable<ICgtpBatchVariable> items)`: Add multiple variables at once.
- `CgtpStringRegister AddStringRegister(int index)`: Add a string register for reading. The value and comment will be populated after a batch read.
- `CgtpStringRegister AddStringRegisterWithValue(int index, string comment, string value)`: Add a string register with a value and comment for writing.
- `CgtpVariable AddVariable(string name, string programName = null)`: Add a generic variable for reading or writing. For system variables, leave programName null. Set the desired value on the returned object before performing a batch write.
- `void Clear()`
- `bool Contains(ICgtpBatchVariable item)`
- `void CopyTo(ICgtpBatchVariable[] array, int arrayIndex)`
- `int Count { get; }`
- `IEnumerator<ICgtpBatchVariable> GetEnumerator()`
- `int IndexOf(ICgtpBatchVariable item)`
- `void Insert(int index, ICgtpBatchVariable item)`
- `bool IsReadOnly { get; }`
- `ICgtpBatchVariable this[int index] { get; set; }`
- `bool Remove(ICgtpBatchVariable item)`
- `void RemoveAt(int index)`

## CgtpBatchWriteResult

`class CgtpBatchWriteResult`

Result of a batch write operation.

## CgtpNumericRegister

`class CgtpNumericRegister : NumericRegisterWithComment, ICgtpBatchVariable`

Represents a numeric register (R[]) for batch read/write operations. A numeric register always has a comment and a numeric value (integer or real).

- `bool Exists { get; }`: Indicates whether a value was returned by the controller during a batch read. False if the variable was not found.
- `int Index { get; }`: 1-based index of the numeric register
- `bool IsReadOnly { get; }`: Indicates whether the variable is read-only on the controller and cannot be written with CGTP
- `bool IsUninitialized { get; }`: Indicates whether the variable is uninitialized on the controller
- `string Name { get; }`: Full variable name (e.g. "$NUMREG[1]", "$POSREG[1,2]", "$RMT_MASTER")
- `string Program { get; }`: Program name that owns this variable
- `string StringValue { get; }`: Raw string value as read from or to be written to the controller
- Inherited from [NumericRegisterWithComment](UnderAutomation.Fanuc.Common.md#numericregisterwithcomment): `Comment`
- Inherited from [NumericRegister](UnderAutomation.Fanuc.Common.md#numericregister): `IsInteger`, `IntegerValue`, `RealValue`

## CgtpPositionRegister

`class CgtpPositionRegister : PositionRegisterWithComment, ICgtpBatchVariable`

Represents a position register (PR[]) for batch read/write operations.

- `int Axes { get; set; }`: Number of axes
- `bool Exists { get; }`: Indicates whether a value was returned by the controller during a batch read. False if the variable was not found.
- `int Group { get; set; }`: Motion group number (first dimension of POSREG[group,index])
- `int Index { get; set; }`: 1-based index of the position register (second dimension of POSREG[group,index])
- `bool IsReadOnly { get; }`: Indicates whether the variable is read-only on the controller and cannot be written with CGTP
- `bool IsUninitialized { get; }`: Indicates whether the variable is uninitialized on the controller
- `string Name { get; }`: Full variable name (e.g. "$NUMREG[1]", "$POSREG[1,2]", "$RMT_MASTER")
- `string Program { get; }`: Program name that owns this variable
- `string StringValue { get; }`: Raw string value as read from or to be written to the controller
- `int UFrame { get; set; }`: User frame number. -1 means unset (stored as 255 on the controller).
- `int UTool { get; set; }`: User tool number. -1 means unset (stored as 255 on the controller).
- Inherited from [PositionRegisterWithComment](UnderAutomation.Fanuc.Common.md#positionregisterwithcomment): `Parse`, `Comment`
- Inherited from [PositionRegister](UnderAutomation.Fanuc.Common.md#positionregister): `JointsPosition`, `CartesianPosition`

## CgtpStringRegister

`class CgtpStringRegister : StringRegisterWithComment, ICgtpBatchVariable`

Represents a string register (SR[]) for batch read/write operations. A string register always has a comment and a string value.

- `bool Exists { get; }`: Indicates whether a value was returned by the controller during a batch read. False if the variable was not found.
- `int Index { get; }`: 1-based index of the string register
- `bool IsReadOnly { get; }`: Indicates whether the variable is read-only on the controller and cannot be written with CGTP
- `bool IsUninitialized { get; }`: Indicates whether the variable is uninitialized on the controller
- `string Name { get; }`: Full variable name (e.g. "$NUMREG[1]", "$POSREG[1,2]", "$RMT_MASTER")
- `string Program { get; }`: Program name that owns this variable
- `string StringValue { get; }`: Raw string value as read from or to be written to the controller
- Inherited from [StringRegisterWithComment](UnderAutomation.Fanuc.Common.md#stringregisterwithcomment): `Comment`, `Value`

## CgtpStructureField

`class CgtpStructureField`

Represents a FIELD or ARRAY node inside a structured variable response.

- `CgtpStructureField()`
- `CgtpStructureField[] Children { get; set; }`: Child nodes (FIELD and ARRAY elements). Null if this is a leaf node.
- `bool IsArray { get; set; }`: True if this node was an ARRAY element, false if it was a FIELD
- `bool IsReadOnly { get; set; }`: Whether this node is read-only on the controller
- `string Name { get; set; }`: Field or array element name
- `string StringValue { get; set; }`: Text content of this node. Null if this node has children.

## CgtpVariable

`class CgtpVariable : ICgtpBatchVariable`

Represents a generic controller variable for batch read/write operations. Supports scalar values (integer, real, boolean, string, position, vector, configuration) and structured values (FIELD/ARRAY hierarchies).

- `bool BooleanValue { get; set; }`: Gets or sets the value as a boolean. Setting this property updates CgtpVariable.StringValue.
- `CartesianPositionVariable CartesianPositionValue { get; set; }`: Gets or sets the value as a Cartesian position. Setting this property updates CgtpVariable.StringValue.
- `Configuration ConfigurationValue { get; set; }`: Gets or sets the value as a robot configuration. Setting this property updates CgtpVariable.StringValue.
- `bool Exists { get; }`: Indicates whether a value was returned by the controller during a batch read. False if the variable was not found.
- `int IntegerValue { get; set; }`: Gets or sets the value as an integer. Setting this property updates CgtpVariable.StringValue.
- `bool IsReadOnly { get; }`: Indicates whether the variable is read-only on the controller and cannot be written with CGTP
- `bool IsUninitialized { get; }`: Indicates whether the variable is uninitialized on the controller
- `JointPositionVariable JointPositionValue { get; set; }`: Gets or sets the value as a joint position. Setting this property updates CgtpVariable.StringValue.
- `string Name { get; }`: Full variable name (e.g. "$NUMREG[1]", "$POSREG[1,2]", "$RMT_MASTER")
- `string Program { get; }`: Program name that owns this variable
- `double RealValue { get; set; }`: Gets or sets the value as a double. Setting this property updates CgtpVariable.StringValue.
- `string StringValue { get; set; }`
- `CgtpStructureField StructureValue { get; set; }`: Structured value returned for complex variables (with FIELD/ARRAY children). Null for scalar variables. When writing, if this is not null each leaf field is written independently.
- `VectorVariable VectorValue { get; set; }`: Gets or sets the value as a 3D vector. Setting this property updates CgtpVariable.StringValue.

## ICgtpBatchVariable

`interface ICgtpBatchVariable`

Common interface for all batch variable types used with batch read/write operations.

- `bool Exists { get; }`: Indicates whether a value was returned by the controller during a batch read. False if the variable was not found.
- `bool IsReadOnly { get; }`: Indicates whether the variable is read-only on the controller and cannot be written with CGTP
- `bool IsUninitialized { get; }`: Indicates whether the variable is uninitialized on the controller
- `string Name { get; }`: Full variable name (e.g. "$NUMREG[1]", "$POSREG[1,2]", "$RMT_MASTER")
- `string Program { get; }`: Program name that owns this variable
- `string StringValue { get; }`: Raw string value as read from or to be written to the controller
