# Move robot remotely

Move a Fanuc robot from an external application using RMI motion commands, Stream Motion real-time streaming, or DPM with SNPX.

Web page: https://underautomation.com/fanuc/documentation/move-robot-remotely

Move a Fanuc robot remotely using the SDK. There are several approaches depending on your application requirements.

## RMI : TP-like motion commands

RMI (Remote Motion Interface) sends motion instructions similar to a TP program. Best for pick-and-place, welding paths, and multi-waypoint trajectories.

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

**Requirements**: R912 (Remote Motion Interface) robot option.

See also: [RMI Motion commands](rmi-motion.md)

## Stream Motion : Real-time streaming (J519)

Stream Motion gives the position of the robot at every communication cycle (2 to 8 ms). The SDK plans smooth trajectories within the limits of the robot and sends them in real time. Best for computed paths, sensor guided motion and teleoperation.

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters
from underautomation.fanuc.common.joints_position import JointsPosition
from underautomation.fanuc.motion.fanuc_motion import FanucMotion
from underautomation.robotics.motion.motion_planner import MotionPlanner

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.stream_motion.enable = True
robot.connect(parameters)
sm = robot.stream_motion

# A TP program with IBGN start[1] / IBGN end[1] must run on the robot
sm.start_monitoring()

planner = MotionPlanner(sm.joint_limits, None)
start = sm.queue_end_joint_position
values = list(start.values)
values[0] += 20
values[1] -= 10
target = JointsPosition(*values)

# Smooth trajectory within the velocity, acceleration and jerk limits of the robot
sm.enqueue(planner.create_joint_path(FanucMotion.to_joint_values(start))
           .move_joint(FanucMotion.to_joint_values(target), 30, FanucMotion.cnt(100))
           .move_joint(FanucMotion.to_joint_values(start), 30, FanucMotion.fine())
           .build())

sm.finish(60000)

robot.disconnect()
```

**Requirements**: J519 (Stream Motion) robot option.

See also: [Stream Motion](stream-motion.md) and the [motion planner](motion.md)

## SNPX + DPM : Position register handshake

See : [Move Robot with Mouse](move-robot-with-mouse.md)

# FTP

If you have option ASCII Upload, you can build th TP program .ls file, download it via FTP and execute the task with Telnet, SNPX. or CGTP

See : [TP editor with breakpoints](tp-editor-with-breakpoints.md)

## CGTP

CGTP allows you to create a new program, insert instructions, and execute it.
