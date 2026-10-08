# UnderAutomation.Fanuc.Rmi.TpInstructions

## CallProgramTpInstruction

`class CallProgramTpInstruction : RmiInstructionBase`

Instruction for a CALL program instruction. Pass to TpInstructions.RmiInstructionBase). Requires MajorVersion &gt;= 4.

- `CallProgramTpInstruction()`
- `string ProgramName { get; set; }`: Name of the TP program to call.

## CartesianMotionTpInstructionBase

`abstract class CartesianMotionTpInstructionBase : FullMotionTpInstructionBase`

Extends TpInstructions.FullMotionTpInstructionBase with a Cartesian target position. Base class for all Cartesian motion instruction types.

- `CartesianPositionWithUserFrame Target { get; set; }`: Target Cartesian position, configuration, and active frame/tool numbers.
- Inherited from [FullMotionTpInstructionBase](UnderAutomation.Fanuc.Rmi.TpInstructions.md#fullmotiontpinstructionbase): `Acc`, `OffsetPrNumber`, `VisionPrNumber`, `LcbType`, `LcbValue`, `PortType`, `PortNumber`, `PortValue`, `ToolOffsetPrNumber`
- Inherited from [MotionTpInstructionBase](UnderAutomation.Fanuc.Rmi.TpInstructions.md#motiontpinstructionbase): `Speed`, `TermType`, `TermValue`

## CircularMotionTpInstruction

`class CircularMotionTpInstruction : CartesianMotionTpInstructionBase`

Instruction for a circular motion (C in TP), Cartesian target representation. Pass to TpInstructions.RmiInstructionBase).

- `CircularMotionTpInstruction()`
- `bool Mrot { get; set; }`: When true, enables coordinated motion (MROT).
- `bool NoBlend { get; set; }`: When true, disables blending with the next instruction.
- `RmiLinearSpeedType SpeedType { get; set; }`: Speed unit (mm/s, inch/min, or time).
- `CartesianPositionWithUserFrame Via { get; set; }`: Via-point Cartesian position that defines the arc.
- `bool WristJoint { get; set; }`: When true, enables wrist-joint mode for this motion.
- Inherited from [CartesianMotionTpInstructionBase](UnderAutomation.Fanuc.Rmi.TpInstructions.md#cartesianmotiontpinstructionbase): `Target`
- Inherited from [FullMotionTpInstructionBase](UnderAutomation.Fanuc.Rmi.TpInstructions.md#fullmotiontpinstructionbase): `Acc`, `OffsetPrNumber`, `VisionPrNumber`, `LcbType`, `LcbValue`, `PortType`, `PortNumber`, `PortValue`, `ToolOffsetPrNumber`
- Inherited from [MotionTpInstructionBase](UnderAutomation.Fanuc.Rmi.TpInstructions.md#motiontpinstructionbase): `Speed`, `TermType`, `TermValue`

## CircularRelativeTpInstruction

`class CircularRelativeTpInstruction : CartesianMotionTpInstructionBase`

Instruction for an incremental circular motion (C in TP), Cartesian delta representation. Pass to TpInstructions.RmiInstructionBase).

- `CircularRelativeTpInstruction()`
- `bool Mrot { get; set; }`: When true, enables coordinated motion (MROT).
- `bool NoBlend { get; set; }`: When true, disables blending with the next instruction.
- `RmiLinearSpeedType SpeedType { get; set; }`: Speed unit (mm/s, inch/min, or time).
- `CartesianPositionWithUserFrame Via { get; set; }`: Via-point delta that defines the arc.
- `bool WristJoint { get; set; }`: When true, enables wrist-joint mode for this motion.
- Inherited from [CartesianMotionTpInstructionBase](UnderAutomation.Fanuc.Rmi.TpInstructions.md#cartesianmotiontpinstructionbase): `Target`
- Inherited from [FullMotionTpInstructionBase](UnderAutomation.Fanuc.Rmi.TpInstructions.md#fullmotiontpinstructionbase): `Acc`, `OffsetPrNumber`, `VisionPrNumber`, `LcbType`, `LcbValue`, `PortType`, `PortNumber`, `PortValue`, `ToolOffsetPrNumber`
- Inherited from [MotionTpInstructionBase](UnderAutomation.Fanuc.Rmi.TpInstructions.md#motiontpinstructionbase): `Speed`, `TermType`, `TermValue`

## FullMotionTpInstructionBase

`abstract class FullMotionTpInstructionBase : MotionTpInstructionBase`

Extends TpInstructions.MotionTpInstructionBase with the full set of optional motion modifiers shared by all non-simplified instruction types.

- `byte? Acc { get; set; }`: Optional acceleration override (1-100 %). null uses the controller default.
- `string LcbType { get; set; }`: Lock-and-continue (LCB) condition type string. null disables LCB.
- `short? LcbValue { get; set; }`: Lock-and-continue (LCB) condition value. Required when FullMotionTpInstructionBase.LcbType is set.
- `short? OffsetPrNumber { get; set; }`: Offset position register number. null disables offset.
- `short? PortNumber { get; set; }`: Digital output port number. Required when FullMotionTpInstructionBase.PortType is set.
- `RmiPortType? PortType { get; set; }`: Digital output port type to trigger at the end of this motion. null disables output.
- `RmiOnOff? PortValue { get; set; }`: Digital output port value. Required when FullMotionTpInstructionBase.PortType is set.
- `short? ToolOffsetPrNumber { get; set; }`: Tool-offset position register number. null disables tool offset. Requires MajorVersion &gt;= 4.
- `short? VisionPrNumber { get; set; }`: Vision offset position register number. null disables vision offset.
- Inherited from [MotionTpInstructionBase](UnderAutomation.Fanuc.Rmi.TpInstructions.md#motiontpinstructionbase): `Speed`, `TermType`, `TermValue`

## JRepMotionTpInstructionBase

`abstract class JRepMotionTpInstructionBase : FullMotionTpInstructionBase`

Extends TpInstructions.FullMotionTpInstructionBase with a joint-angle target. Base class for all joint-representation motion instruction types.

- `JointsPosition Joints { get; set; }`: Target joint angles in degrees.
- Inherited from [FullMotionTpInstructionBase](UnderAutomation.Fanuc.Rmi.TpInstructions.md#fullmotiontpinstructionbase): `Acc`, `OffsetPrNumber`, `VisionPrNumber`, `LcbType`, `LcbValue`, `PortType`, `PortNumber`, `PortValue`, `ToolOffsetPrNumber`
- Inherited from [MotionTpInstructionBase](UnderAutomation.Fanuc.Rmi.TpInstructions.md#motiontpinstructionbase): `Speed`, `TermType`, `TermValue`

## JointMotionJRepTpInstruction

`class JointMotionJRepTpInstruction : JRepMotionTpInstructionBase`

Instruction for a joint motion (J in TP), joint-angle representation, full options. Pass to TpInstructions.RmiInstructionBase).

- `JointMotionJRepTpInstruction()`
- `bool Mrot { get; set; }`: When true, enables coordinated motion (MROT).
- `bool NoBlend { get; set; }`: When true, disables blending with the next instruction.
- `RmiJointSpeedType SpeedType { get; set; }`: Speed unit (percent override or time).
- Inherited from [JRepMotionTpInstructionBase](UnderAutomation.Fanuc.Rmi.TpInstructions.md#jrepmotiontpinstructionbase): `Joints`
- Inherited from [FullMotionTpInstructionBase](UnderAutomation.Fanuc.Rmi.TpInstructions.md#fullmotiontpinstructionbase): `Acc`, `OffsetPrNumber`, `VisionPrNumber`, `LcbType`, `LcbValue`, `PortType`, `PortNumber`, `PortValue`, `ToolOffsetPrNumber`
- Inherited from [MotionTpInstructionBase](UnderAutomation.Fanuc.Rmi.TpInstructions.md#motiontpinstructionbase): `Speed`, `TermType`, `TermValue`

## JointMotionTpInstruction

`class JointMotionTpInstruction : CartesianMotionTpInstructionBase`

Instruction for a joint motion (J in TP), Cartesian target representation. Pass to TpInstructions.RmiInstructionBase).

- `JointMotionTpInstruction()`
- `bool Mrot { get; set; }`: When true, enables coordinated motion (MROT).
- `bool NoBlend { get; set; }`: When true, disables blending with the next instruction.
- `RmiJointSpeedType SpeedType { get; set; }`: Speed unit (percent override or time).
- Inherited from [CartesianMotionTpInstructionBase](UnderAutomation.Fanuc.Rmi.TpInstructions.md#cartesianmotiontpinstructionbase): `Target`
- Inherited from [FullMotionTpInstructionBase](UnderAutomation.Fanuc.Rmi.TpInstructions.md#fullmotiontpinstructionbase): `Acc`, `OffsetPrNumber`, `VisionPrNumber`, `LcbType`, `LcbValue`, `PortType`, `PortNumber`, `PortValue`, `ToolOffsetPrNumber`
- Inherited from [MotionTpInstructionBase](UnderAutomation.Fanuc.Rmi.TpInstructions.md#motiontpinstructionbase): `Speed`, `TermType`, `TermValue`

## JointRelativeJRepTpInstruction

`class JointRelativeJRepTpInstruction : JRepMotionTpInstructionBase`

Instruction for an incremental joint motion (J in TP), joint-angle representation, full options. Pass to TpInstructions.RmiInstructionBase).

- `JointRelativeJRepTpInstruction()`
- `bool Mrot { get; set; }`: When true, enables coordinated motion (MROT).
- `bool NoBlend { get; set; }`: When true, disables blending with the next instruction.
- `RmiJointSpeedType SpeedType { get; set; }`: Speed unit (percent override or time).
- Inherited from [JRepMotionTpInstructionBase](UnderAutomation.Fanuc.Rmi.TpInstructions.md#jrepmotiontpinstructionbase): `Joints`
- Inherited from [FullMotionTpInstructionBase](UnderAutomation.Fanuc.Rmi.TpInstructions.md#fullmotiontpinstructionbase): `Acc`, `OffsetPrNumber`, `VisionPrNumber`, `LcbType`, `LcbValue`, `PortType`, `PortNumber`, `PortValue`, `ToolOffsetPrNumber`
- Inherited from [MotionTpInstructionBase](UnderAutomation.Fanuc.Rmi.TpInstructions.md#motiontpinstructionbase): `Speed`, `TermType`, `TermValue`

## JointRelativeTpInstruction

`class JointRelativeTpInstruction : CartesianMotionTpInstructionBase`

Instruction for an incremental joint motion (J in TP), Cartesian delta representation. Pass to TpInstructions.RmiInstructionBase).

- `JointRelativeTpInstruction()`
- `bool Mrot { get; set; }`: When true, enables coordinated motion (MROT).
- `bool NoBlend { get; set; }`: When true, disables blending with the next instruction.
- `RmiJointSpeedType SpeedType { get; set; }`: Speed unit (percent override or time).
- Inherited from [CartesianMotionTpInstructionBase](UnderAutomation.Fanuc.Rmi.TpInstructions.md#cartesianmotiontpinstructionbase): `Target`
- Inherited from [FullMotionTpInstructionBase](UnderAutomation.Fanuc.Rmi.TpInstructions.md#fullmotiontpinstructionbase): `Acc`, `OffsetPrNumber`, `VisionPrNumber`, `LcbType`, `LcbValue`, `PortType`, `PortNumber`, `PortValue`, `ToolOffsetPrNumber`
- Inherited from [MotionTpInstructionBase](UnderAutomation.Fanuc.Rmi.TpInstructions.md#motiontpinstructionbase): `Speed`, `TermType`, `TermValue`

## LinearMotionJRepTpInstruction

`class LinearMotionJRepTpInstruction : JRepMotionTpInstructionBase`

Instruction for a linear motion (L in TP), joint-angle representation. Pass to TpInstructions.RmiInstructionBase).

- `LinearMotionJRepTpInstruction()`
- `int? Alim { get; set; }`: Acceleration limit value. null uses the controller default. Requires MajorVersion &gt;= 5 and the R921 option.
- `short? AlimReg { get; set; }`: Acceleration limit register number. null disables register-based limit. Requires MajorVersion &gt;= 5 and the R921 option.
- `bool Mrot { get; set; }`: When true, enables coordinated motion (MROT).
- `bool NoBlend { get; set; }`: When true, disables blending with the next instruction. Requires MajorVersion &gt;= 5.
- `RmiLinearSpeedType SpeedType { get; set; }`: Speed unit (mm/s, inch/min, or time).
- `bool WristJoint { get; set; }`: When true, enables wrist-joint mode for this motion.
- Inherited from [JRepMotionTpInstructionBase](UnderAutomation.Fanuc.Rmi.TpInstructions.md#jrepmotiontpinstructionbase): `Joints`
- Inherited from [FullMotionTpInstructionBase](UnderAutomation.Fanuc.Rmi.TpInstructions.md#fullmotiontpinstructionbase): `Acc`, `OffsetPrNumber`, `VisionPrNumber`, `LcbType`, `LcbValue`, `PortType`, `PortNumber`, `PortValue`, `ToolOffsetPrNumber`
- Inherited from [MotionTpInstructionBase](UnderAutomation.Fanuc.Rmi.TpInstructions.md#motiontpinstructionbase): `Speed`, `TermType`, `TermValue`

## LinearMotionTpInstruction

`class LinearMotionTpInstruction : CartesianMotionTpInstructionBase`

Instruction for a linear motion (L in TP), Cartesian target representation. Pass to TpInstructions.RmiInstructionBase).

- `LinearMotionTpInstruction()`
- `int? Alim { get; set; }`: Acceleration limit value. null uses the controller default. Requires MajorVersion &gt;= 5 and the R921 option.
- `short? AlimReg { get; set; }`: Acceleration limit register number. null disables register-based limit. Requires MajorVersion &gt;= 5 and the R921 option.
- `bool Mrot { get; set; }`: When true, enables coordinated motion (MROT).
- `bool NoBlend { get; set; }`: When true, disables blending with the next instruction. Requires MajorVersion &gt;= 5.
- `RmiLinearSpeedType SpeedType { get; set; }`: Speed unit (mm/s, inch/min, or time).
- `bool WristJoint { get; set; }`: When true, enables wrist-joint mode for this motion.
- Inherited from [CartesianMotionTpInstructionBase](UnderAutomation.Fanuc.Rmi.TpInstructions.md#cartesianmotiontpinstructionbase): `Target`
- Inherited from [FullMotionTpInstructionBase](UnderAutomation.Fanuc.Rmi.TpInstructions.md#fullmotiontpinstructionbase): `Acc`, `OffsetPrNumber`, `VisionPrNumber`, `LcbType`, `LcbValue`, `PortType`, `PortNumber`, `PortValue`, `ToolOffsetPrNumber`
- Inherited from [MotionTpInstructionBase](UnderAutomation.Fanuc.Rmi.TpInstructions.md#motiontpinstructionbase): `Speed`, `TermType`, `TermValue`

## LinearRelativeJRepTpInstruction

`class LinearRelativeJRepTpInstruction : JRepMotionTpInstructionBase`

Instruction for an incremental linear motion (L in TP), joint-angle representation. Pass to TpInstructions.RmiInstructionBase).

- `LinearRelativeJRepTpInstruction()`
- `int? Alim { get; set; }`: Acceleration limit value. null uses the controller default. Requires MajorVersion &gt;= 5 and the R921 option.
- `short? AlimReg { get; set; }`: Acceleration limit register number. null disables register-based limit. Requires MajorVersion &gt;= 5 and the R921 option.
- `bool Mrot { get; set; }`: When true, enables coordinated motion (MROT).
- `bool NoBlend { get; set; }`: When true, disables blending with the next instruction. Requires MajorVersion &gt;= 5.
- `RmiLinearSpeedType SpeedType { get; set; }`: Speed unit (mm/s, inch/min, or time).
- `bool WristJoint { get; set; }`: When true, enables wrist-joint mode for this motion.
- Inherited from [JRepMotionTpInstructionBase](UnderAutomation.Fanuc.Rmi.TpInstructions.md#jrepmotiontpinstructionbase): `Joints`
- Inherited from [FullMotionTpInstructionBase](UnderAutomation.Fanuc.Rmi.TpInstructions.md#fullmotiontpinstructionbase): `Acc`, `OffsetPrNumber`, `VisionPrNumber`, `LcbType`, `LcbValue`, `PortType`, `PortNumber`, `PortValue`, `ToolOffsetPrNumber`
- Inherited from [MotionTpInstructionBase](UnderAutomation.Fanuc.Rmi.TpInstructions.md#motiontpinstructionbase): `Speed`, `TermType`, `TermValue`

## LinearRelativeTpInstruction

`class LinearRelativeTpInstruction : CartesianMotionTpInstructionBase`

Instruction for an incremental linear motion (L in TP), Cartesian delta representation. Pass to TpInstructions.RmiInstructionBase).

- `LinearRelativeTpInstruction()`
- `int? Alim { get; set; }`: Acceleration limit value. null uses the controller default. Requires MajorVersion &gt;= 5 and the R921 option.
- `short? AlimReg { get; set; }`: Acceleration limit register number. null disables register-based limit. Requires MajorVersion &gt;= 5 and the R921 option.
- `bool Mrot { get; set; }`: When true, enables coordinated motion (MROT).
- `bool NoBlend { get; set; }`: When true, disables blending with the next instruction. Requires MajorVersion &gt;= 5.
- `RmiLinearSpeedType SpeedType { get; set; }`: Speed unit (mm/s, inch/min, or time).
- `bool WristJoint { get; set; }`: When true, enables wrist-joint mode for this motion.
- Inherited from [CartesianMotionTpInstructionBase](UnderAutomation.Fanuc.Rmi.TpInstructions.md#cartesianmotiontpinstructionbase): `Target`
- Inherited from [FullMotionTpInstructionBase](UnderAutomation.Fanuc.Rmi.TpInstructions.md#fullmotiontpinstructionbase): `Acc`, `OffsetPrNumber`, `VisionPrNumber`, `LcbType`, `LcbValue`, `PortType`, `PortNumber`, `PortValue`, `ToolOffsetPrNumber`
- Inherited from [MotionTpInstructionBase](UnderAutomation.Fanuc.Rmi.TpInstructions.md#motiontpinstructionbase): `Speed`, `TermType`, `TermValue`

## MotionTpInstructionBase

`abstract class MotionTpInstructionBase : RmiInstructionBase`

Base class for all RMI motion instructions. Carries the three parameters that are mandatory on every motion instruction.

- `short Speed { get; set; }`: Speed value whose unit is defined by the concrete subclass.
- `RmiTerminationType TermType { get; set; }`: Termination type (FINE, CNT, or CR).
- `byte TermValue { get; set; }`: Termination value (0 for FINE, 1-100 for CNT, radius for CR).

## RmiInstructionBase

`abstract class RmiInstructionBase`

Base class for all RMI TP instructions. Pass an instance to TpInstructions.RmiInstructionBase) to queue the instruction on the controller.

## SetPayloadTpInstruction

`class SetPayloadTpInstruction : RmiInstructionBase`

Instruction for a PAYLOAD[n] schedule selection. Pass to TpInstructions.RmiInstructionBase).

- `SetPayloadTpInstruction()`
- `byte ScheduleNumber { get; set; }`: Payload schedule number to activate.

## SetUFrameTpInstruction

`class SetUFrameTpInstruction : RmiInstructionBase`

Instruction for a UFRAME_NUM = n assignment. Pass to TpInstructions.RmiInstructionBase).

- `SetUFrameTpInstruction()`
- `byte FrameNumber { get; set; }`: User frame number to activate.

## SetUToolTpInstruction

`class SetUToolTpInstruction : RmiInstructionBase`

Instruction for a UTOOL_NUM = n assignment. Pass to TpInstructions.RmiInstructionBase).

- `SetUToolTpInstruction()`
- `byte ToolNumber { get; set; }`: Tool frame number to activate.

## SplineMotionJRepTpInstruction

`class SplineMotionJRepTpInstruction : JRepMotionTpInstructionBase`

Instruction for a spline motion with joint-angle representation. Pass to TpInstructions.RmiInstructionBase). Requires MajorVersion &gt;= 7.

- `SplineMotionJRepTpInstruction()`
- `RmiJointSpeedType SpeedType { get; set; }`: Speed unit (percent override or time).
- Inherited from [JRepMotionTpInstructionBase](UnderAutomation.Fanuc.Rmi.TpInstructions.md#jrepmotiontpinstructionbase): `Joints`
- Inherited from [FullMotionTpInstructionBase](UnderAutomation.Fanuc.Rmi.TpInstructions.md#fullmotiontpinstructionbase): `Acc`, `OffsetPrNumber`, `VisionPrNumber`, `LcbType`, `LcbValue`, `PortType`, `PortNumber`, `PortValue`, `ToolOffsetPrNumber`
- Inherited from [MotionTpInstructionBase](UnderAutomation.Fanuc.Rmi.TpInstructions.md#motiontpinstructionbase): `Speed`, `TermType`, `TermValue`

## SplineMotionTpInstruction

`class SplineMotionTpInstruction : CartesianMotionTpInstructionBase`

Instruction for a spline motion with a Cartesian target. Pass to TpInstructions.RmiInstructionBase). Requires MajorVersion &gt;= 7.

- `SplineMotionTpInstruction()`
- `RmiLinearSpeedType SpeedType { get; set; }`: Speed unit (mm/s, inch/min, or time).
- Inherited from [CartesianMotionTpInstructionBase](UnderAutomation.Fanuc.Rmi.TpInstructions.md#cartesianmotiontpinstructionbase): `Target`
- Inherited from [FullMotionTpInstructionBase](UnderAutomation.Fanuc.Rmi.TpInstructions.md#fullmotiontpinstructionbase): `Acc`, `OffsetPrNumber`, `VisionPrNumber`, `LcbType`, `LcbValue`, `PortType`, `PortNumber`, `PortValue`, `ToolOffsetPrNumber`
- Inherited from [MotionTpInstructionBase](UnderAutomation.Fanuc.Rmi.TpInstructions.md#motiontpinstructionbase): `Speed`, `TermType`, `TermValue`

## WaitDinTpInstruction

`class WaitDinTpInstruction : RmiInstructionBase`

Instruction for a WAIT DI[n] = value condition. Pass to TpInstructions.RmiInstructionBase).

- `WaitDinTpInstruction()`
- `short PortNumber { get; set; }`: Digital input port number to wait on.
- `RmiOnOff Value { get; set; }`: Expected port state that releases the wait.

## WaitTimeTpInstruction

`class WaitTimeTpInstruction : RmiInstructionBase`

Instruction for a WAIT t (sec) time delay. Pass to TpInstructions.RmiInstructionBase).

- `WaitTimeTpInstruction()`
- `double Seconds { get; set; }`: Duration to wait, in seconds.
