# underautomation.fanuc.rmi.tp_instructions

## CallProgramTpInstruction

`from underautomation.fanuc.rmi.tp_instructions.call_program_tp_instruction import CallProgramTpInstruction`

Instruction for a CALL program instruction. Pass to send_tp_instruction(). Requires MajorVersion >= 4.

- `CallProgramTpInstruction()`
- `program_name: str`: Name of the TP program to call.

## CartesianMotionTpInstructionBase

`from underautomation.fanuc.rmi.tp_instructions.cartesian_motion_tp_instruction_base import CartesianMotionTpInstructionBase`

Extends FullMotionTpInstructionBase with a Cartesian target position. Base class for all Cartesian motion instruction types.

- `target: CartesianPositionWithUserFrame`: Target Cartesian position, configuration, and active frame/tool numbers.
- Inherited from [FullMotionTpInstructionBase](underautomation.fanuc.rmi.tp_instructions.md#fullmotiontpinstructionbase): `acc`, `offset_pr_number`, `vision_pr_number`, `lcb_type`, `lcb_value`, `port_type`, `port_number`, `port_value`, `tool_offset_pr_number`
- Inherited from [MotionTpInstructionBase](underautomation.fanuc.rmi.tp_instructions.md#motiontpinstructionbase): `speed`, `term_type`, `term_value`

## CircularMotionTpInstruction

`from underautomation.fanuc.rmi.tp_instructions.circular_motion_tp_instruction import CircularMotionTpInstruction`

Instruction for a circular motion (C in TP), Cartesian target representation. Pass to send_tp_instruction().

- `CircularMotionTpInstruction()`
- `speed_type: RmiLinearSpeedType`: Speed unit (mm/s, inch/min, or time).
- `via: CartesianPositionWithUserFrame`: Via-point Cartesian position that defines the arc.
- `wrist_joint: bool`: When true, enables wrist-joint mode for this motion.
- `mrot: bool`: When true, enables coordinated motion (MROT).
- `no_blend: bool`: When true, disables blending with the next instruction.
- Inherited from [CartesianMotionTpInstructionBase](underautomation.fanuc.rmi.tp_instructions.md#cartesianmotiontpinstructionbase): `target`
- Inherited from [FullMotionTpInstructionBase](underautomation.fanuc.rmi.tp_instructions.md#fullmotiontpinstructionbase): `acc`, `offset_pr_number`, `vision_pr_number`, `lcb_type`, `lcb_value`, `port_type`, `port_number`, `port_value`, `tool_offset_pr_number`
- Inherited from [MotionTpInstructionBase](underautomation.fanuc.rmi.tp_instructions.md#motiontpinstructionbase): `speed`, `term_type`, `term_value`

## CircularRelativeTpInstruction

`from underautomation.fanuc.rmi.tp_instructions.circular_relative_tp_instruction import CircularRelativeTpInstruction`

Instruction for an incremental circular motion (C in TP), Cartesian delta representation. Pass to send_tp_instruction().

- `CircularRelativeTpInstruction()`
- `speed_type: RmiLinearSpeedType`: Speed unit (mm/s, inch/min, or time).
- `via: CartesianPositionWithUserFrame`: Via-point delta that defines the arc.
- `wrist_joint: bool`: When true, enables wrist-joint mode for this motion.
- `mrot: bool`: When true, enables coordinated motion (MROT).
- `no_blend: bool`: When true, disables blending with the next instruction.
- Inherited from [CartesianMotionTpInstructionBase](underautomation.fanuc.rmi.tp_instructions.md#cartesianmotiontpinstructionbase): `target`
- Inherited from [FullMotionTpInstructionBase](underautomation.fanuc.rmi.tp_instructions.md#fullmotiontpinstructionbase): `acc`, `offset_pr_number`, `vision_pr_number`, `lcb_type`, `lcb_value`, `port_type`, `port_number`, `port_value`, `tool_offset_pr_number`
- Inherited from [MotionTpInstructionBase](underautomation.fanuc.rmi.tp_instructions.md#motiontpinstructionbase): `speed`, `term_type`, `term_value`

## FullMotionTpInstructionBase

`from underautomation.fanuc.rmi.tp_instructions.full_motion_tp_instruction_base import FullMotionTpInstructionBase`

Extends MotionTpInstructionBase with the full set of optional motion modifiers shared by all non-simplified instruction types.

- `acc: int | None`: Optional acceleration override (1-100 %). null uses the controller default.
- `offset_pr_number: int | None`: Offset position register number. null disables offset.
- `vision_pr_number: int | None`: Vision offset position register number. null disables vision offset.
- `lcb_type: str`: Lock-and-continue (LCB) condition type string. null disables LCB.
- `lcb_value: int | None`: Lock-and-continue (LCB) condition value. Required when lcb_type is set.
- `port_type: RmiPortType | None`: Digital output port type to trigger at the end of this motion. null disables output.
- `port_number: int | None`: Digital output port number. Required when port_type is set.
- `port_value: RmiOnOff | None`: Digital output port value. Required when port_type is set.
- `tool_offset_pr_number: int | None`: Tool-offset position register number. null disables tool offset. Requires MajorVersion >= 4.
- Inherited from [MotionTpInstructionBase](underautomation.fanuc.rmi.tp_instructions.md#motiontpinstructionbase): `speed`, `term_type`, `term_value`

## JRepMotionTpInstructionBase

`from underautomation.fanuc.rmi.tp_instructions.j_rep_motion_tp_instruction_base import JRepMotionTpInstructionBase`

Extends FullMotionTpInstructionBase with a joint-angle target. Base class for all joint-representation motion instruction types.

- `joints: JointsPosition`: Target joint angles in degrees.
- Inherited from [FullMotionTpInstructionBase](underautomation.fanuc.rmi.tp_instructions.md#fullmotiontpinstructionbase): `acc`, `offset_pr_number`, `vision_pr_number`, `lcb_type`, `lcb_value`, `port_type`, `port_number`, `port_value`, `tool_offset_pr_number`
- Inherited from [MotionTpInstructionBase](underautomation.fanuc.rmi.tp_instructions.md#motiontpinstructionbase): `speed`, `term_type`, `term_value`

## JointMotionJRepTpInstruction

`from underautomation.fanuc.rmi.tp_instructions.joint_motion_j_rep_tp_instruction import JointMotionJRepTpInstruction`

Instruction for a joint motion (J in TP), joint-angle representation, full options. Pass to send_tp_instruction().

- `JointMotionJRepTpInstruction()`
- `speed_type: RmiJointSpeedType`: Speed unit (percent override or time).
- `mrot: bool`: When true, enables coordinated motion (MROT).
- `no_blend: bool`: When true, disables blending with the next instruction.
- Inherited from [JRepMotionTpInstructionBase](underautomation.fanuc.rmi.tp_instructions.md#jrepmotiontpinstructionbase): `joints`
- Inherited from [FullMotionTpInstructionBase](underautomation.fanuc.rmi.tp_instructions.md#fullmotiontpinstructionbase): `acc`, `offset_pr_number`, `vision_pr_number`, `lcb_type`, `lcb_value`, `port_type`, `port_number`, `port_value`, `tool_offset_pr_number`
- Inherited from [MotionTpInstructionBase](underautomation.fanuc.rmi.tp_instructions.md#motiontpinstructionbase): `speed`, `term_type`, `term_value`

## JointMotionTpInstruction

`from underautomation.fanuc.rmi.tp_instructions.joint_motion_tp_instruction import JointMotionTpInstruction`

Instruction for a joint motion (J in TP), Cartesian target representation. Pass to send_tp_instruction().

- `JointMotionTpInstruction()`
- `speed_type: RmiJointSpeedType`: Speed unit (percent override or time).
- `mrot: bool`: When true, enables coordinated motion (MROT).
- `no_blend: bool`: When true, disables blending with the next instruction.
- Inherited from [CartesianMotionTpInstructionBase](underautomation.fanuc.rmi.tp_instructions.md#cartesianmotiontpinstructionbase): `target`
- Inherited from [FullMotionTpInstructionBase](underautomation.fanuc.rmi.tp_instructions.md#fullmotiontpinstructionbase): `acc`, `offset_pr_number`, `vision_pr_number`, `lcb_type`, `lcb_value`, `port_type`, `port_number`, `port_value`, `tool_offset_pr_number`
- Inherited from [MotionTpInstructionBase](underautomation.fanuc.rmi.tp_instructions.md#motiontpinstructionbase): `speed`, `term_type`, `term_value`

## JointRelativeJRepTpInstruction

`from underautomation.fanuc.rmi.tp_instructions.joint_relative_j_rep_tp_instruction import JointRelativeJRepTpInstruction`

Instruction for an incremental joint motion (J in TP), joint-angle representation, full options. Pass to send_tp_instruction().

- `JointRelativeJRepTpInstruction()`
- `speed_type: RmiJointSpeedType`: Speed unit (percent override or time).
- `mrot: bool`: When true, enables coordinated motion (MROT).
- `no_blend: bool`: When true, disables blending with the next instruction.
- Inherited from [JRepMotionTpInstructionBase](underautomation.fanuc.rmi.tp_instructions.md#jrepmotiontpinstructionbase): `joints`
- Inherited from [FullMotionTpInstructionBase](underautomation.fanuc.rmi.tp_instructions.md#fullmotiontpinstructionbase): `acc`, `offset_pr_number`, `vision_pr_number`, `lcb_type`, `lcb_value`, `port_type`, `port_number`, `port_value`, `tool_offset_pr_number`
- Inherited from [MotionTpInstructionBase](underautomation.fanuc.rmi.tp_instructions.md#motiontpinstructionbase): `speed`, `term_type`, `term_value`

## JointRelativeTpInstruction

`from underautomation.fanuc.rmi.tp_instructions.joint_relative_tp_instruction import JointRelativeTpInstruction`

Instruction for an incremental joint motion (J in TP), Cartesian delta representation. Pass to send_tp_instruction().

- `JointRelativeTpInstruction()`
- `speed_type: RmiJointSpeedType`: Speed unit (percent override or time).
- `mrot: bool`: When true, enables coordinated motion (MROT).
- `no_blend: bool`: When true, disables blending with the next instruction.
- Inherited from [CartesianMotionTpInstructionBase](underautomation.fanuc.rmi.tp_instructions.md#cartesianmotiontpinstructionbase): `target`
- Inherited from [FullMotionTpInstructionBase](underautomation.fanuc.rmi.tp_instructions.md#fullmotiontpinstructionbase): `acc`, `offset_pr_number`, `vision_pr_number`, `lcb_type`, `lcb_value`, `port_type`, `port_number`, `port_value`, `tool_offset_pr_number`
- Inherited from [MotionTpInstructionBase](underautomation.fanuc.rmi.tp_instructions.md#motiontpinstructionbase): `speed`, `term_type`, `term_value`

## LinearMotionJRepTpInstruction

`from underautomation.fanuc.rmi.tp_instructions.linear_motion_j_rep_tp_instruction import LinearMotionJRepTpInstruction`

Instruction for a linear motion (L in TP), joint-angle representation. Pass to send_tp_instruction().

- `LinearMotionJRepTpInstruction()`
- `speed_type: RmiLinearSpeedType`: Speed unit (mm/s, inch/min, or time).
- `wrist_joint: bool`: When true, enables wrist-joint mode for this motion.
- `mrot: bool`: When true, enables coordinated motion (MROT).
- `no_blend: bool`: When true, disables blending with the next instruction. Requires MajorVersion >= 5.
- `alim: int | None`: Acceleration limit value. null uses the controller default. Requires MajorVersion >= 5 and the R921 option.
- `alim_reg: int | None`: Acceleration limit register number. null disables register-based limit. Requires MajorVersion >= 5 and the R921 option.
- Inherited from [JRepMotionTpInstructionBase](underautomation.fanuc.rmi.tp_instructions.md#jrepmotiontpinstructionbase): `joints`
- Inherited from [FullMotionTpInstructionBase](underautomation.fanuc.rmi.tp_instructions.md#fullmotiontpinstructionbase): `acc`, `offset_pr_number`, `vision_pr_number`, `lcb_type`, `lcb_value`, `port_type`, `port_number`, `port_value`, `tool_offset_pr_number`
- Inherited from [MotionTpInstructionBase](underautomation.fanuc.rmi.tp_instructions.md#motiontpinstructionbase): `speed`, `term_type`, `term_value`

## LinearMotionTpInstruction

`from underautomation.fanuc.rmi.tp_instructions.linear_motion_tp_instruction import LinearMotionTpInstruction`

Instruction for a linear motion (L in TP), Cartesian target representation. Pass to send_tp_instruction().

- `LinearMotionTpInstruction()`
- `speed_type: RmiLinearSpeedType`: Speed unit (mm/s, inch/min, or time).
- `wrist_joint: bool`: When true, enables wrist-joint mode for this motion.
- `mrot: bool`: When true, enables coordinated motion (MROT).
- `no_blend: bool`: When true, disables blending with the next instruction. Requires MajorVersion >= 5.
- `alim: int | None`: Acceleration limit value. null uses the controller default. Requires MajorVersion >= 5 and the R921 option.
- `alim_reg: int | None`: Acceleration limit register number. null disables register-based limit. Requires MajorVersion >= 5 and the R921 option.
- Inherited from [CartesianMotionTpInstructionBase](underautomation.fanuc.rmi.tp_instructions.md#cartesianmotiontpinstructionbase): `target`
- Inherited from [FullMotionTpInstructionBase](underautomation.fanuc.rmi.tp_instructions.md#fullmotiontpinstructionbase): `acc`, `offset_pr_number`, `vision_pr_number`, `lcb_type`, `lcb_value`, `port_type`, `port_number`, `port_value`, `tool_offset_pr_number`
- Inherited from [MotionTpInstructionBase](underautomation.fanuc.rmi.tp_instructions.md#motiontpinstructionbase): `speed`, `term_type`, `term_value`

## LinearRelativeJRepTpInstruction

`from underautomation.fanuc.rmi.tp_instructions.linear_relative_j_rep_tp_instruction import LinearRelativeJRepTpInstruction`

Instruction for an incremental linear motion (L in TP), joint-angle representation. Pass to send_tp_instruction().

- `LinearRelativeJRepTpInstruction()`
- `speed_type: RmiLinearSpeedType`: Speed unit (mm/s, inch/min, or time).
- `wrist_joint: bool`: When true, enables wrist-joint mode for this motion.
- `mrot: bool`: When true, enables coordinated motion (MROT).
- `no_blend: bool`: When true, disables blending with the next instruction. Requires MajorVersion >= 5.
- `alim: int | None`: Acceleration limit value. null uses the controller default. Requires MajorVersion >= 5 and the R921 option.
- `alim_reg: int | None`: Acceleration limit register number. null disables register-based limit. Requires MajorVersion >= 5 and the R921 option.
- Inherited from [JRepMotionTpInstructionBase](underautomation.fanuc.rmi.tp_instructions.md#jrepmotiontpinstructionbase): `joints`
- Inherited from [FullMotionTpInstructionBase](underautomation.fanuc.rmi.tp_instructions.md#fullmotiontpinstructionbase): `acc`, `offset_pr_number`, `vision_pr_number`, `lcb_type`, `lcb_value`, `port_type`, `port_number`, `port_value`, `tool_offset_pr_number`
- Inherited from [MotionTpInstructionBase](underautomation.fanuc.rmi.tp_instructions.md#motiontpinstructionbase): `speed`, `term_type`, `term_value`

## LinearRelativeTpInstruction

`from underautomation.fanuc.rmi.tp_instructions.linear_relative_tp_instruction import LinearRelativeTpInstruction`

Instruction for an incremental linear motion (L in TP), Cartesian delta representation. Pass to send_tp_instruction().

- `LinearRelativeTpInstruction()`
- `speed_type: RmiLinearSpeedType`: Speed unit (mm/s, inch/min, or time).
- `wrist_joint: bool`: When true, enables wrist-joint mode for this motion.
- `mrot: bool`: When true, enables coordinated motion (MROT).
- `no_blend: bool`: When true, disables blending with the next instruction. Requires MajorVersion >= 5.
- `alim: int | None`: Acceleration limit value. null uses the controller default. Requires MajorVersion >= 5 and the R921 option.
- `alim_reg: int | None`: Acceleration limit register number. null disables register-based limit. Requires MajorVersion >= 5 and the R921 option.
- Inherited from [CartesianMotionTpInstructionBase](underautomation.fanuc.rmi.tp_instructions.md#cartesianmotiontpinstructionbase): `target`
- Inherited from [FullMotionTpInstructionBase](underautomation.fanuc.rmi.tp_instructions.md#fullmotiontpinstructionbase): `acc`, `offset_pr_number`, `vision_pr_number`, `lcb_type`, `lcb_value`, `port_type`, `port_number`, `port_value`, `tool_offset_pr_number`
- Inherited from [MotionTpInstructionBase](underautomation.fanuc.rmi.tp_instructions.md#motiontpinstructionbase): `speed`, `term_type`, `term_value`

## MotionTpInstructionBase

`from underautomation.fanuc.rmi.tp_instructions.motion_tp_instruction_base import MotionTpInstructionBase`

Base class for all RMI motion instructions. Carries the three parameters that are mandatory on every motion instruction.

- `speed: int`: Speed value whose unit is defined by the concrete subclass.
- `term_type: RmiTerminationType`: Termination type (FINE, CNT, or CR).
- `term_value: int`: Termination value (0 for FINE, 1-100 for CNT, radius for CR).

## RmiInstructionBase

`from underautomation.fanuc.rmi.tp_instructions.rmi_instruction_base import RmiInstructionBase`

Base class for all RMI TP instructions. Pass an instance to send_tp_instruction() to queue the instruction on the controller.

## SetPayloadTpInstruction

`from underautomation.fanuc.rmi.tp_instructions.set_payload_tp_instruction import SetPayloadTpInstruction`

Instruction for a PAYLOAD[n] schedule selection. Pass to send_tp_instruction().

- `SetPayloadTpInstruction()`
- `schedule_number: int`: Payload schedule number to activate.

## SetUFrameTpInstruction

`from underautomation.fanuc.rmi.tp_instructions.set_u_frame_tp_instruction import SetUFrameTpInstruction`

Instruction for a UFRAME_NUM = n assignment. Pass to send_tp_instruction().

- `SetUFrameTpInstruction()`
- `frame_number: int`: User frame number to activate.

## SetUToolTpInstruction

`from underautomation.fanuc.rmi.tp_instructions.set_u_tool_tp_instruction import SetUToolTpInstruction`

Instruction for a UTOOL_NUM = n assignment. Pass to send_tp_instruction().

- `SetUToolTpInstruction()`
- `tool_number: int`: Tool frame number to activate.

## SplineMotionJRepTpInstruction

`from underautomation.fanuc.rmi.tp_instructions.spline_motion_j_rep_tp_instruction import SplineMotionJRepTpInstruction`

Instruction for a spline motion with joint-angle representation. Pass to send_tp_instruction(). Requires MajorVersion >= 7.

- `SplineMotionJRepTpInstruction()`
- `speed_type: RmiJointSpeedType`: Speed unit (percent override or time).
- Inherited from [JRepMotionTpInstructionBase](underautomation.fanuc.rmi.tp_instructions.md#jrepmotiontpinstructionbase): `joints`
- Inherited from [FullMotionTpInstructionBase](underautomation.fanuc.rmi.tp_instructions.md#fullmotiontpinstructionbase): `acc`, `offset_pr_number`, `vision_pr_number`, `lcb_type`, `lcb_value`, `port_type`, `port_number`, `port_value`, `tool_offset_pr_number`
- Inherited from [MotionTpInstructionBase](underautomation.fanuc.rmi.tp_instructions.md#motiontpinstructionbase): `speed`, `term_type`, `term_value`

## SplineMotionTpInstruction

`from underautomation.fanuc.rmi.tp_instructions.spline_motion_tp_instruction import SplineMotionTpInstruction`

Instruction for a spline motion with a Cartesian target. Pass to send_tp_instruction(). Requires MajorVersion >= 7.

- `SplineMotionTpInstruction()`
- `speed_type: RmiLinearSpeedType`: Speed unit (mm/s, inch/min, or time).
- Inherited from [CartesianMotionTpInstructionBase](underautomation.fanuc.rmi.tp_instructions.md#cartesianmotiontpinstructionbase): `target`
- Inherited from [FullMotionTpInstructionBase](underautomation.fanuc.rmi.tp_instructions.md#fullmotiontpinstructionbase): `acc`, `offset_pr_number`, `vision_pr_number`, `lcb_type`, `lcb_value`, `port_type`, `port_number`, `port_value`, `tool_offset_pr_number`
- Inherited from [MotionTpInstructionBase](underautomation.fanuc.rmi.tp_instructions.md#motiontpinstructionbase): `speed`, `term_type`, `term_value`

## WaitDinTpInstruction

`from underautomation.fanuc.rmi.tp_instructions.wait_din_tp_instruction import WaitDinTpInstruction`

Instruction for a WAIT DI[n] = value condition. Pass to send_tp_instruction().

- `WaitDinTpInstruction()`
- `port_number: int`: Digital input port number to wait on.
- `value: RmiOnOff`: Expected port state that releases the wait.

## WaitTimeTpInstruction

`from underautomation.fanuc.rmi.tp_instructions.wait_time_tp_instruction import WaitTimeTpInstruction`

Instruction for a WAIT t (sec) time delay. Pass to send_tp_instruction().

- `WaitTimeTpInstruction()`
- `seconds: float`: Duration to wait, in seconds.
