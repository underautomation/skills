# Motion commands

Send linear, joint, and circular motion commands with configurable speed, termination type, and acceleration via RMI.

Web page: https://underautomation.com/fanuc/documentation/rmi-motion

RMI lets you send TP-equivalent motion instructions to the robot. Each call to `SendTpInstruction()` returns an `RmiInstructionResponse` that tracks the instruction through its execution lifecycle.

## Linear motion

Move the robot in a straight line to a Cartesian target:

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters
from underautomation.fanuc.rmi.tp_instructions.linear_motion_tp_instruction import LinearMotionTpInstruction
from underautomation.fanuc.rmi.tp_instructions.linear_relative_tp_instruction import LinearRelativeTpInstruction
from underautomation.fanuc.rmi.tp_instructions.linear_motion_j_rep_tp_instruction import LinearMotionJRepTpInstruction
from underautomation.fanuc.rmi.data.rmi_linear_speed_type import RmiLinearSpeedType
from underautomation.fanuc.rmi.data.rmi_termination_type import RmiTerminationType
from underautomation.fanuc.common.cartesian_position_with_user_frame import CartesianPositionWithUserFrame
from underautomation.fanuc.common.joints_position import JointsPosition

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.rmi.enable = True
robot.connect(parameters)
robot.rmi.initialize()

# Linear motion to a Cartesian target (tool 1, frame 0)
move = LinearMotionTpInstruction()
move.speed_type = RmiLinearSpeedType.MmSec
move.speed = 100
move.term_type = RmiTerminationType.Fine
move.target = CartesianPositionWithUserFrame(500, 200, 300, 0, 90, 0, 1, 0)
robot.rmi.send_tp_instruction(move).wait_for_completion()

# Incremental linear motion (delta from current position)
inc = LinearRelativeTpInstruction()
inc.speed_type = RmiLinearSpeedType.MmSec
inc.speed = 50
inc.term_type = RmiTerminationType.Fine
inc.target = CartesianPositionWithUserFrame(0, 0, -50, 0, 0, 0, 1, 0)
robot.rmi.send_tp_instruction(inc).wait_for_completion()

# Linear motion with joint-angle target representation
jrep = LinearMotionJRepTpInstruction()
jrep.speed_type = RmiLinearSpeedType.MmSec
jrep.speed = 80
jrep.term_type = RmiTerminationType.Fine
jrep.joints = JointsPosition(10, -20, 30, 0, 60, 0)
robot.rmi.send_tp_instruction(jrep).wait_for_completion()

# CNT blending: chain motions without stopping
p1 = LinearMotionTpInstruction()
p1.speed_type = RmiLinearSpeedType.MmSec
p1.speed = 200
p1.term_type = RmiTerminationType.Cnt
p1.term_value = 100
p1.target = CartesianPositionWithUserFrame(600, 0, 400, 0, 90, 0, 1, 0)

p2 = LinearMotionTpInstruction()
p2.speed_type = RmiLinearSpeedType.MmSec
p2.speed = 200
p2.term_type = RmiTerminationType.Fine  # last motion must be Fine (or no_blend = True)
p2.target = CartesianPositionWithUserFrame(700, 0, 350, 0, 90, 0, 1, 0)

robot.rmi.send_tp_instruction(p1)
robot.rmi.send_tp_instruction(p2).wait_for_completion()

robot.rmi.abort()
robot.disconnect()
```

### Speed types for linear motion

| `RmiLinearSpeedType` | Description |
|----------------------|-------------|
| `MmSec` | Millimeters per second. |
| `InchMin` | Inches per minute (0.1 in/min units). |
| `Time` | Duration in 0.1-second steps. |
| `MSec` | Duration in milliseconds. |

### Termination types

| `RmiTerminationType` | Description |
|----------------------|-------------|
| `Fine` | Stop precisely at the target. |
| `Cnt` | Continuous blending with the next motion (value 1-100). The last motion sent must be `Fine` unless `NoBlend = true`. |
| `Cr` | Corner region (requires Advanced Constant Path option). |

## Joint motion

Move using joint interpolation (Cartesian target or joint-angle target):

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters
from underautomation.fanuc.rmi.tp_instructions.joint_motion_tp_instruction import JointMotionTpInstruction
from underautomation.fanuc.rmi.tp_instructions.joint_motion_j_rep_tp_instruction import JointMotionJRepTpInstruction
from underautomation.fanuc.rmi.tp_instructions.joint_relative_j_rep_tp_instruction import JointRelativeJRepTpInstruction
from underautomation.fanuc.rmi.data.rmi_joint_speed_type import RmiJointSpeedType
from underautomation.fanuc.rmi.data.rmi_termination_type import RmiTerminationType
from underautomation.fanuc.common.cartesian_position_with_user_frame import CartesianPositionWithUserFrame
from underautomation.fanuc.common.joints_position import JointsPosition

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.rmi.enable = True
robot.connect(parameters)
robot.rmi.initialize()

# Joint motion with Cartesian target, percent speed
cart = JointMotionTpInstruction()
cart.speed_type = RmiJointSpeedType.Percent
cart.speed = 10
cart.term_type = RmiTerminationType.Fine
cart.target = CartesianPositionWithUserFrame(500, 200, 300, 0, 90, 0, 1, 0)
robot.rmi.send_tp_instruction(cart).wait_for_completion()

# Joint motion with joint-angle target representation
jrep = JointMotionJRepTpInstruction()
jrep.speed_type = RmiJointSpeedType.Percent
jrep.speed = 5
jrep.term_type = RmiTerminationType.Fine
jrep.joints = JointsPosition(10, -20, 30, 0, 60, 0)
robot.rmi.send_tp_instruction(jrep).wait_for_completion()

# Incremental joint motion: rotate J5 by 5 degrees
rel = JointRelativeJRepTpInstruction()
rel.speed_type = RmiJointSpeedType.Percent
rel.speed = 5
rel.term_type = RmiTerminationType.Fine
rel.joints = JointsPosition(0, 0, 0, 0, 5, 0)
robot.rmi.send_tp_instruction(rel).wait_for_completion()

robot.rmi.abort()
robot.disconnect()
```

### Speed types for joint motion

| `RmiJointSpeedType` | Description |
|---------------------|-------------|
| `Percent` | Percentage of maximum joint speed (1-100). |
| `Time` | Duration in 0.1-second steps. |
| `MSec` | Duration in milliseconds. |

## Circular motion

Circular motion requires a **via point** and a **destination**:

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters
from underautomation.fanuc.rmi.tp_instructions.circular_motion_tp_instruction import CircularMotionTpInstruction
from underautomation.fanuc.rmi.tp_instructions.circular_relative_tp_instruction import CircularRelativeTpInstruction
from underautomation.fanuc.rmi.data.rmi_linear_speed_type import RmiLinearSpeedType
from underautomation.fanuc.rmi.data.rmi_termination_type import RmiTerminationType
from underautomation.fanuc.common.cartesian_position_with_user_frame import CartesianPositionWithUserFrame

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.rmi.enable = True
robot.connect(parameters)
robot.rmi.initialize()

# Circular motion: define a via-point and a destination
arc = CircularMotionTpInstruction()
arc.speed_type = RmiLinearSpeedType.MmSec
arc.speed = 80
arc.term_type = RmiTerminationType.Fine
arc.via = CartesianPositionWithUserFrame(600, 100, 350, 0, 90, 0, 1, 0)
arc.target = CartesianPositionWithUserFrame(700, 0, 300, 0, 90, 0, 1, 0)
robot.rmi.send_tp_instruction(arc).wait_for_completion()

# Incremental circular motion (via and target are deltas)
arc_rel = CircularRelativeTpInstruction()
arc_rel.speed_type = RmiLinearSpeedType.MmSec
arc_rel.speed = 60
arc_rel.term_type = RmiTerminationType.Fine
arc_rel.via = CartesianPositionWithUserFrame(50, 50, 0, 0, 0, 0, 1, 0)
arc_rel.target = CartesianPositionWithUserFrame(100, 0, 0, 0, 0, 0, 1, 0)
robot.rmi.send_tp_instruction(arc_rel).wait_for_completion()

robot.rmi.abort()
robot.disconnect()
```

## Spline motion

Spline motion requires firmware **MajorVersion >= 7** (V9.40P/54 or later). The controller needs at least one more spline instruction after the first to start executing the segment.

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters
from underautomation.fanuc.rmi.tp_instructions.spline_motion_tp_instruction import SplineMotionTpInstruction
from underautomation.fanuc.rmi.tp_instructions.spline_motion_j_rep_tp_instruction import SplineMotionJRepTpInstruction
from underautomation.fanuc.rmi.tp_instructions.wait_time_tp_instruction import WaitTimeTpInstruction
from underautomation.fanuc.rmi.data.rmi_linear_speed_type import RmiLinearSpeedType
from underautomation.fanuc.rmi.data.rmi_joint_speed_type import RmiJointSpeedType
from underautomation.fanuc.rmi.data.rmi_termination_type import RmiTerminationType
from underautomation.fanuc.common.cartesian_position_with_user_frame import CartesianPositionWithUserFrame
from underautomation.fanuc.common.joints_position import JointsPosition

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.rmi.enable = True
robot.connect(parameters)
robot.rmi.initialize()

# Spline motion requires MajorVersion >= 7 (firmware V9.40P/54 or later).
# The controller will not execute the first spline segment until it receives
# a second instruction after the last spline point.

s1 = SplineMotionTpInstruction()
s1.speed_type = RmiLinearSpeedType.MmSec
s1.speed = 200
s1.term_type = RmiTerminationType.Cnt
s1.term_value = 100
s1.target = CartesianPositionWithUserFrame(500, 100, 300, 0, 90, 0, 1, 0)
robot.rmi.send_tp_instruction(s1)

s2 = SplineMotionTpInstruction()
s2.speed_type = RmiLinearSpeedType.MmSec
s2.speed = 200
s2.term_type = RmiTerminationType.Cnt
s2.term_value = 100
s2.target = CartesianPositionWithUserFrame(550, 200, 320, 0, 90, 0, 1, 0)
robot.rmi.send_tp_instruction(s2)

s3 = SplineMotionTpInstruction()
s3.speed_type = RmiLinearSpeedType.MmSec
s3.speed = 200
s3.term_type = RmiTerminationType.Fine
s3.target = CartesianPositionWithUserFrame(600, 100, 300, 0, 90, 0, 1, 0)
robot.rmi.send_tp_instruction(s3)

# Non-spline instruction flushes the spline buffer
flush = WaitTimeTpInstruction()
flush.seconds = 0.1
robot.rmi.send_tp_instruction(flush).wait_for_completion()

robot.rmi.abort()
robot.disconnect()
```

## Relative (incremental) motions

All motion types have incremental variants. The position is a delta from the current robot position:

| Absolute | Incremental |
|----------|-------------|
| `LinearMotionTpInstruction` | `LinearRelativeTpInstruction` |
| `JointMotionTpInstruction` | `JointRelativeTpInstruction` |
| `CircularMotionTpInstruction` | `CircularRelativeTpInstruction` |
| `LinearMotionJRepTpInstruction` | `LinearRelativeJRepTpInstruction` |
| `JointMotionJRepTpInstruction` | `JointRelativeJRepTpInstruction` |

## Motion options

Most instruction classes expose optional motion modifiers:

| Property | Type | Description |
|----------|------|-------------|
| `Acc` | `byte?` | Acceleration override (20-100 %). |
| `OffsetPrNumber` | `short?` | Offset position register number. |
| `ToolOffsetPrNumber` | `short?` | Tool offset PR number (MajorVersion >= 4). |
| `VisionPrNumber` | `short?` | Vision offset register number. |
| `WristJoint` | `bool` | Enable wrist-joint mode (linear and circular only). |
| `Mrot` | `bool` | MROT option - requires WristJoint and R640 option. |
| `NoBlend` | `bool` | Allow CNT motion to execute without waiting for the next instruction (MajorVersion >= 5). |
| `Alim` | `int?` | Acceleration limit in mm/s² (MajorVersion >= 5, R921 option). |
| `AlimReg` | `short?` | Register-based acceleration limit (MajorVersion >= 5, R921 option). |
| `LcbType` | `string` | Local Condition Block type: `"TB"`, `"TA"`, or `"DB"`. |
| `LcbValue` | `short?` | LCB value (ms for TA/TB, 0.01 mm for DB). |
| `PortType` | `RmiPortType?` | Output port type (`DOUT` or `ROUT`) triggered by LCB. |
| `PortNumber` | `short?` | LCB output port number. |
| `PortValue` | `RmiOnOff?` | LCB output port value (ON or OFF). |

## Non-motion instructions

Insert wait conditions, frame changes, and program calls between motions:

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters
from underautomation.fanuc.rmi.data.rmi_on_off import RmiOnOff
from underautomation.fanuc.rmi.tp_instructions.wait_din_tp_instruction import WaitDinTpInstruction
from underautomation.fanuc.rmi.tp_instructions.wait_time_tp_instruction import WaitTimeTpInstruction
from underautomation.fanuc.rmi.tp_instructions.set_u_frame_tp_instruction import SetUFrameTpInstruction
from underautomation.fanuc.rmi.tp_instructions.set_u_tool_tp_instruction import SetUToolTpInstruction
from underautomation.fanuc.rmi.tp_instructions.set_payload_tp_instruction import SetPayloadTpInstruction
from underautomation.fanuc.rmi.tp_instructions.call_program_tp_instruction import CallProgramTpInstruction

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.rmi.enable = True
robot.connect(parameters)
robot.rmi.initialize()

# Wait for digital input DI[1] to turn ON before continuing
wait_din = WaitDinTpInstruction()
wait_din.port_number = 1
wait_din.value = RmiOnOff.ON
robot.rmi.send_tp_instruction(wait_din)

# Wait 0.5 seconds
wait_time = WaitTimeTpInstruction()
wait_time.seconds = 0.5
robot.rmi.send_tp_instruction(wait_time)

# Switch to UFRAME 2 for the next motions
uframe = SetUFrameTpInstruction()
uframe.frame_number = 2
robot.rmi.send_tp_instruction(uframe)

# Switch to UTOOL 3
utool = SetUToolTpInstruction()
utool.tool_number = 3
robot.rmi.send_tp_instruction(utool)

# Activate payload schedule 1
payload = SetPayloadTpInstruction()
payload.schedule_number = 1
robot.rmi.send_tp_instruction(payload)

# Call a TP program (requires MajorVersion >= 4)
call = CallProgramTpInstruction()
call.program_name = "GRIPPER_OPEN"
robot.rmi.send_tp_instruction(call).wait_for_completion()

robot.rmi.abort()
robot.disconnect()
```

## Tracking instruction status

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters
from underautomation.fanuc.rmi.tp_instructions.linear_motion_tp_instruction import LinearMotionTpInstruction
from underautomation.fanuc.rmi.data.rmi_linear_speed_type import RmiLinearSpeedType
from underautomation.fanuc.rmi.data.rmi_termination_type import RmiTerminationType
from underautomation.fanuc.rmi.data.rmi_instruction_status import RmiInstructionStatus
from underautomation.fanuc.common.cartesian_position_with_user_frame import CartesianPositionWithUserFrame

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.rmi.enable = True
robot.connect(parameters)
robot.rmi.initialize()

# Send several instructions. Each returns immediately.
for i in range(5):
    instr = LinearMotionTpInstruction()
    instr.speed_type = RmiLinearSpeedType.MmSec
    instr.speed = 100
    instr.term_type = RmiTerminationType.Fine
    instr.target = CartesianPositionWithUserFrame(500 + i * 20, 200, 300, 0, 90, 0, 1, 0)
    r = robot.rmi.send_tp_instruction(instr)

    def on_change(status, seq=r.sequence_id):
        print(f"  Seq {seq}: {status}")
    r.status_changed += on_change

# Wait for all instructions to complete
for r in robot.rmi.instructions:
    r.wait_for_completion()

# Print final results
for r in robot.rmi.instructions:
    if r.status == RmiInstructionStatus.Error:
        print(f"  Seq {r.sequence_id} failed: {r.error_text}")
    else:
        print(f"  Seq {r.sequence_id} completed OK")

# Remove completed instructions from the tracking list
robot.rmi.clear_completed_instructions()

robot.rmi.abort()
robot.disconnect()
```

## Complete example

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters
from underautomation.fanuc.rmi.tp_instructions.linear_motion_tp_instruction import LinearMotionTpInstruction
from underautomation.fanuc.rmi.tp_instructions.joint_motion_tp_instruction import JointMotionTpInstruction
from underautomation.fanuc.rmi.tp_instructions.joint_motion_j_rep_tp_instruction import JointMotionJRepTpInstruction
from underautomation.fanuc.rmi.tp_instructions.wait_din_tp_instruction import WaitDinTpInstruction
from underautomation.fanuc.rmi.tp_instructions.wait_time_tp_instruction import WaitTimeTpInstruction
from underautomation.fanuc.rmi.tp_instructions.set_payload_tp_instruction import SetPayloadTpInstruction
from underautomation.fanuc.rmi.tp_instructions.call_program_tp_instruction import CallProgramTpInstruction
from underautomation.fanuc.rmi.data.rmi_linear_speed_type import RmiLinearSpeedType
from underautomation.fanuc.rmi.data.rmi_joint_speed_type import RmiJointSpeedType
from underautomation.fanuc.rmi.data.rmi_termination_type import RmiTerminationType
from underautomation.fanuc.rmi.data.rmi_on_off import RmiOnOff
from underautomation.fanuc.common.cartesian_position_with_user_frame import CartesianPositionWithUserFrame
from underautomation.fanuc.common.joints_position import JointsPosition

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.rmi.enable = True
robot.connect(parameters)

# Check status before initializing
status = robot.rmi.get_status()
if status.tp_enabled:
    print("Turn off the teach pendant before proceeding.")
    robot.disconnect()
    exit()

robot.rmi.initialize()
robot.rmi.set_override(80)

# Move to home using joint motion with joint-angle target
home = JointMotionJRepTpInstruction()
home.speed_type = RmiJointSpeedType.Percent
home.speed = 10
home.term_type = RmiTerminationType.Fine
home.joints = JointsPosition(0, 0, 0, 0, 0, 0)
robot.rmi.send_tp_instruction(home).wait_for_completion()

# Approach
approach = LinearMotionTpInstruction()
approach.speed_type = RmiLinearSpeedType.MmSec
approach.speed = 200
approach.term_type = RmiTerminationType.Cnt
approach.term_value = 50
approach.target = CartesianPositionWithUserFrame(500, 200, 350, 0, 90, 0, 1, 0)
robot.rmi.send_tp_instruction(approach)

# Descend to pick position
pick = LinearMotionTpInstruction()
pick.speed_type = RmiLinearSpeedType.MmSec
pick.speed = 50
pick.term_type = RmiTerminationType.Fine
pick.target = CartesianPositionWithUserFrame(500, 200, 300, 0, 90, 0, 1, 0)
robot.rmi.send_tp_instruction(pick).wait_for_completion()

# Activate gripper
grip = CallProgramTpInstruction()
grip.program_name = "GRIP_ON"
robot.rmi.send_tp_instruction(grip).wait_for_completion()

# Retract
retract = LinearMotionTpInstruction()
retract.speed_type = RmiLinearSpeedType.MmSec
retract.speed = 100
retract.term_type = RmiTerminationType.Fine
retract.target = CartesianPositionWithUserFrame(500, 200, 400, 0, 90, 0, 1, 0)
robot.rmi.send_tp_instruction(retract).wait_for_completion()

# Handle HOLD state
if robot.rmi.is_in_hold_state:
    print("Controller in HOLD. Calling reset...")
    robot.rmi.reset()

robot.rmi.abort()
robot.disconnect()
```

## API reference

**LinearMotionTpInstruction** ([reference](../api/underautomation.fanuc.rmi.tp_instructions.md#linearmotiontpinstruction))

- `LinearMotionTpInstruction()`
- `speed_type: RmiLinearSpeedType`: Speed unit (mm/s, inch/min, or time).
- `wrist_joint: bool`: When true, enables wrist-joint mode for this motion.
- `mrot: bool`: When true, enables coordinated motion (MROT).
- `no_blend: bool`: When true, disables blending with the next instruction. Requires MajorVersion >= 5.
- `alim: int | None`: Acceleration limit value. null uses the controller default. Requires MajorVersion >= 5 and the R921 option.
- `alim_reg: int | None`: Acceleration limit register number. null disables register-based limit. Requires MajorVersion >= 5 and the R921 option.
- Inherited from [CartesianMotionTpInstructionBase](../api/underautomation.fanuc.rmi.tp_instructions.md#cartesianmotiontpinstructionbase): `target`
- Inherited from [FullMotionTpInstructionBase](../api/underautomation.fanuc.rmi.tp_instructions.md#fullmotiontpinstructionbase): `acc`, `offset_pr_number`, `vision_pr_number`, `lcb_type`, `lcb_value`, `port_type`, `port_number`, `port_value`, `tool_offset_pr_number`
- Inherited from [MotionTpInstructionBase](../api/underautomation.fanuc.rmi.tp_instructions.md#motiontpinstructionbase): `speed`, `term_type`, `term_value`

**JointMotionTpInstruction** ([reference](../api/underautomation.fanuc.rmi.tp_instructions.md#jointmotiontpinstruction))

- `JointMotionTpInstruction()`
- `speed_type: RmiJointSpeedType`: Speed unit (percent override or time).
- `mrot: bool`: When true, enables coordinated motion (MROT).
- `no_blend: bool`: When true, disables blending with the next instruction.
- Inherited from [CartesianMotionTpInstructionBase](../api/underautomation.fanuc.rmi.tp_instructions.md#cartesianmotiontpinstructionbase): `target`
- Inherited from [FullMotionTpInstructionBase](../api/underautomation.fanuc.rmi.tp_instructions.md#fullmotiontpinstructionbase): `acc`, `offset_pr_number`, `vision_pr_number`, `lcb_type`, `lcb_value`, `port_type`, `port_number`, `port_value`, `tool_offset_pr_number`
- Inherited from [MotionTpInstructionBase](../api/underautomation.fanuc.rmi.tp_instructions.md#motiontpinstructionbase): `speed`, `term_type`, `term_value`

**JointMotionJRepTpInstruction** ([reference](../api/underautomation.fanuc.rmi.tp_instructions.md#jointmotionjreptpinstruction))

- `JointMotionJRepTpInstruction()`
- `speed_type: RmiJointSpeedType`: Speed unit (percent override or time).
- `mrot: bool`: When true, enables coordinated motion (MROT).
- `no_blend: bool`: When true, disables blending with the next instruction.
- Inherited from [JRepMotionTpInstructionBase](../api/underautomation.fanuc.rmi.tp_instructions.md#jrepmotiontpinstructionbase): `joints`
- Inherited from [FullMotionTpInstructionBase](../api/underautomation.fanuc.rmi.tp_instructions.md#fullmotiontpinstructionbase): `acc`, `offset_pr_number`, `vision_pr_number`, `lcb_type`, `lcb_value`, `port_type`, `port_number`, `port_value`, `tool_offset_pr_number`
- Inherited from [MotionTpInstructionBase](../api/underautomation.fanuc.rmi.tp_instructions.md#motiontpinstructionbase): `speed`, `term_type`, `term_value`

**CircularMotionTpInstruction** ([reference](../api/underautomation.fanuc.rmi.tp_instructions.md#circularmotiontpinstruction))

- `CircularMotionTpInstruction()`
- `speed_type: RmiLinearSpeedType`: Speed unit (mm/s, inch/min, or time).
- `via: CartesianPositionWithUserFrame`: Via-point Cartesian position that defines the arc.
- `wrist_joint: bool`: When true, enables wrist-joint mode for this motion.
- `mrot: bool`: When true, enables coordinated motion (MROT).
- `no_blend: bool`: When true, disables blending with the next instruction.
- Inherited from [CartesianMotionTpInstructionBase](../api/underautomation.fanuc.rmi.tp_instructions.md#cartesianmotiontpinstructionbase): `target`
- Inherited from [FullMotionTpInstructionBase](../api/underautomation.fanuc.rmi.tp_instructions.md#fullmotiontpinstructionbase): `acc`, `offset_pr_number`, `vision_pr_number`, `lcb_type`, `lcb_value`, `port_type`, `port_number`, `port_value`, `tool_offset_pr_number`
- Inherited from [MotionTpInstructionBase](../api/underautomation.fanuc.rmi.tp_instructions.md#motiontpinstructionbase): `speed`, `term_type`, `term_value`

**SplineMotionTpInstruction** ([reference](../api/underautomation.fanuc.rmi.tp_instructions.md#splinemotiontpinstruction))

- `SplineMotionTpInstruction()`
- `speed_type: RmiLinearSpeedType`: Speed unit (mm/s, inch/min, or time).
- Inherited from [CartesianMotionTpInstructionBase](../api/underautomation.fanuc.rmi.tp_instructions.md#cartesianmotiontpinstructionbase): `target`
- Inherited from [FullMotionTpInstructionBase](../api/underautomation.fanuc.rmi.tp_instructions.md#fullmotiontpinstructionbase): `acc`, `offset_pr_number`, `vision_pr_number`, `lcb_type`, `lcb_value`, `port_type`, `port_number`, `port_value`, `tool_offset_pr_number`
- Inherited from [MotionTpInstructionBase](../api/underautomation.fanuc.rmi.tp_instructions.md#motiontpinstructionbase): `speed`, `term_type`, `term_value`

**FullMotionTpInstructionBase** ([reference](../api/underautomation.fanuc.rmi.tp_instructions.md#fullmotiontpinstructionbase))

- `acc: int | None`: Optional acceleration override (1-100 %). null uses the controller default.
- `offset_pr_number: int | None`: Offset position register number. null disables offset.
- `vision_pr_number: int | None`: Vision offset position register number. null disables vision offset.
- `lcb_type: str`: Lock-and-continue (LCB) condition type string. null disables LCB.
- `lcb_value: int | None`: Lock-and-continue (LCB) condition value. Required when lcb_type is set.
- `port_type: RmiPortType | None`: Digital output port type to trigger at the end of this motion. null disables output.
- `port_number: int | None`: Digital output port number. Required when port_type is set.
- `port_value: RmiOnOff | None`: Digital output port value. Required when port_type is set.
- `tool_offset_pr_number: int | None`: Tool-offset position register number. null disables tool offset. Requires MajorVersion >= 4.
- Inherited from [MotionTpInstructionBase](../api/underautomation.fanuc.rmi.tp_instructions.md#motiontpinstructionbase): `speed`, `term_type`, `term_value`

**RmiInstructionResponse** ([reference](../api/underautomation.fanuc.rmi.data.md#rmiinstructionresponse))

- `RmiInstructionResponse()`
- `status_changed(handler)`: Fired each time status changes. The argument is the new status value. This event may be raised from a background thread.
- `wait_for_completion(timeoutMs: int=-1) -> bool`: Blocks the calling thread until the instruction reaches a terminal state (Completed or Error), or until timeoutMs milliseconds have elapsed. Pass -1 (or omit) to wait indefinitely.
- `sequence_id: int (read only)`: Sequence identifier assigned to this instruction. 0 until the instruction has been dispatched to the controller.
- `status: RmiInstructionStatus (read only)`: Current execution state of the instruction.
- `instruction: RmiInstructionBase (read only)`: Sent instruction
- Inherited from [RmiResponseBase](../api/underautomation.fanuc.rmi.data.md#rmiresponsebase): `error_id`, `error_text`
