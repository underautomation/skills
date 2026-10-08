# Frames, I/O & status

Manage user frames and tools, read/write I/O, read positions, set speed override, and get controller status via RMI.

Web page: https://underautomation.com/fanuc/documentation/rmi-frames-io

RMI provides access to controller status, user frames and tools, digital and generic I/O, position reading, registers, system variables, payload, and TCP speed.

## Controller status

`GetStatus()` returns the full controller state. Use it before `Initialize()` to verify the controller is ready.

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.rmi.enable = True
robot.connect(parameters)

# Basic status: servo, TP mode, RMI running, override
status = robot.rmi.get_status()
print("Servo ready:   ", status.servo_ready)
print("TP enabled:    ", status.tp_enabled)
print("RMI running:   ", status.rmi_motion_status)
print("Program state: ", status.program_status)
print("Override:      ", status.speed_override, "%")
print("UFrame count:  ", status.number_u_frame)
print("UTool count:   ", status.number_u_tool)

# Extended status: drive power, control mode, speed clamp
ext = robot.rmi.get_extended_status()
print("Drives on:     ", ext.drives_powered)
print("In motion:     ", ext.in_motion)

# Read last controller error (up to 5 at once)
errors = robot.rmi.read_error(count=3)
for entry in errors.error_data_entries:
    print("Error:", entry)

# HOLD state
print("In HOLD:       ", robot.rmi.is_in_hold_state)

robot.disconnect()
```

## Admin commands

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.rmi.enable = True
robot.connect(parameters)
robot.rmi.initialize()

# Set speed override (1-100 %)
robot.rmi.set_override(50)

# Pause and resume the motion program
robot.rmi.pause()
robot.rmi.continue_()

# Reset controller errors and exit the HOLD state
robot.rmi.reset()

# Resynchronize the sequence ID counter
robot.rmi.auto_set_next_sequence_id()

# Get/set current UFRAME and UTOOL numbers
ut = robot.rmi.get_u_frame_u_tool()
print("Frame:", ut.frame, "Tool:", ut.tool)
robot.rmi.set_u_frame_u_tool(uframe=1, utool=2)

# Abort the RMI_MOVE program
robot.rmi.abort()

robot.disconnect()
```

## Position reading

Read the current robot position and TCP speed. On firmware MajorVersion >= 6, the position reflects actual encoder counts.

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.rmi.enable = True
robot.connect(parameters)

# Read current Cartesian position.
# On MajorVersion >= 6, returns actual encoder position.
cart = robot.rmi.read_cartesian_position()
print(f"X={cart.position.x:.1f}  Y={cart.position.y:.1f}  Z={cart.position.z:.1f}")
print(f"W={cart.position.w:.1f}  P={cart.position.p:.1f}  R={cart.position.r:.1f}")
print(f"Tool={cart.position.tool}  Frame={cart.position.frame}")
print(f"Timestamp={cart.time_tag}")

# Read current joint angles
joints = robot.rmi.read_joint_angles()
print(f"J1={joints.joint_angle.j1:.2f}  J2={joints.joint_angle.j2:.2f}  J3={joints.joint_angle.j3:.2f}")

# Read TCP speed (mm/s)
speed = robot.rmi.read_tcp_speed()
print(f"TCP speed={speed.speed:.2f} mm/s")

robot.disconnect()
```

## User frames and tools

Read and write user frames (UFrame) and tools (UTool):

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters
from underautomation.fanuc.common.xyzwpr_position import XYZWPRPosition

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.rmi.enable = True
robot.connect(parameters)

# Read UFRAME 1
uf = robot.rmi.read_u_frame(1)
print(f"UFrame 1: X={uf.frame.x:.1f}  Y={uf.frame.y:.1f}  Z={uf.frame.z:.1f}")

# Write UFRAME 1
frame_pos = XYZWPRPosition()
frame_pos.x = 100
robot.rmi.write_u_frame(1, frame_pos)

# Read UTOOL 1
ut = robot.rmi.read_u_tool(1)
print(f"UTool 1: X={ut.frame.x:.1f}  Y={ut.frame.y:.1f}  Z={ut.frame.z:.1f}")

# Write UTOOL 1
tool_pos = XYZWPRPosition()
tool_pos.z = 200
robot.rmi.write_u_tool(1, tool_pos)

# Get current UFRAME and UTOOL numbers
current = robot.rmi.get_u_frame_u_tool()
print(f"Active UFRAME={current.frame}  UTOOL={current.tool}")

# Set the active UFRAME and UTOOL
robot.rmi.set_u_frame_u_tool(uframe=1, utool=2)

robot.disconnect()
```

## Digital I/O

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters
from underautomation.fanuc.rmi.data.rmi_on_off import RmiOnOff

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.rmi.enable = True
robot.connect(parameters)

# Read digital input DI[2]
din = robot.rmi.read_din(2)
print(f"DI[2] = {din.port_value}")

# Write digital output DO[1]
robot.rmi.write_dout(1, RmiOnOff.ON)
robot.rmi.write_dout(1, RmiOnOff.OFF)

robot.disconnect()
```

## Generic I/O ports

`ReadIOPort` and `WriteIOPort` work with any port type (DI, DO, AI, AO, GO, RO, FLAG, RI, UI, UO):

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters
from underautomation.fanuc.rmi.data.rmi_io_port_type import RmiIoPortType

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.rmi.enable = True
robot.connect(parameters)

# Read any IO port type: DI, DO, AI, AO, GO, RO, FLAG, RI, UI, UO
di = robot.rmi.read_io_port(RmiIoPortType.DI, 1)
print(f"DI[1] = {di.value}")

ai = robot.rmi.read_io_port(RmiIoPortType.AI, 1)
print(f"AI[1] = {ai.value}")

flag = robot.rmi.read_io_port(RmiIoPortType.FLAG, 5)
print(f"FLAG[5] = {flag.value}")

# Write AO[1] = 2.5
robot.rmi.write_io_port(RmiIoPortType.AO, 1, 2.5)

# Write GO[1] = 7
robot.rmi.write_io_port(RmiIoPortType.GO, 1, 7)

# Write FLAG[5] = 1
robot.rmi.write_io_port(RmiIoPortType.FLAG, 5, 1)

robot.disconnect()
```

## Position registers

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters
from underautomation.fanuc.common.cartesian_position_with_user_frame import CartesianPositionWithUserFrame

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.rmi.enable = True
robot.connect(parameters)

# Read position register PR[1]
pr = robot.rmi.read_position_register(1)
print(f"PR[1]: X={pr.cartesian_position.x:.1f}  Y={pr.cartesian_position.y:.1f}  Z={pr.cartesian_position.z:.1f}")

# Write position register PR[2] with a Cartesian value
robot.rmi.write_position_register_cartesian(
    2,
    CartesianPositionWithUserFrame(500, 200, 300, 0, 90, 0, 1, 0)
)

robot.disconnect()
```

## Numeric registers and system variables

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.rmi.enable = True
robot.connect(parameters)

# Read numeric register R[1]
r1 = robot.rmi.read_numeric_register(1)
print(f"R[1] is_integer={r1.value.is_integer}  value={r1.value.real_value}")

# Write integer value to R[1]
robot.rmi.write_numeric_register_as_integer(1, 42)

# Write float value to R[2]
robot.rmi.write_numeric_register_as_double(2, 3.14)

# Read system variable $MCR.$GENOVERRIDE (include the leading $)
var = robot.rmi.read_variable("$MCR.$GENOVERRIDE")
print(f"Speed override = {var.real_value}")

# Write system variable
robot.rmi.write_variable_as_integer("$MCR.$GENOVERRIDE", 80)

robot.disconnect()
```

## Payload

Define payload mass, center of gravity, and inertia for a schedule. You can also send a `SetPayloadTpInstruction` as a motion-sequence instruction.

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.rmi.enable = True
robot.connect(parameters)

# Define payload for schedule 1: 5 kg, center of gravity offset 0.1 m in Z
robot.rmi.set_payload_value(
    schedule_number=1,
    mass_kg=5.0,
    cg_xm=0.0, cg_ym=0.0, cg_zm=0.1
)

# Include inertia values
robot.rmi.set_payload_value(
    schedule_number=2,
    mass_kg=3.0,
    cg_xm=0.05, cg_ym=0.0, cg_zm=0.08,
    inertia_xkgm2=0.002, inertia_ykgm2=0.002, inertia_zkgm2=0.001
)

# Define payload compensation
robot.rmi.set_payload_compensation(
    schedule_number=1,
    mass_kg=1.0,
    cg_xm=0.0, cg_ym=0.0, cg_zm=0.05,
    inertia_xkgm2=0.001, inertia_ykgm2=0.001, inertia_zkgm2=0.0005
)

# Activate schedule 1 immediately (command, not a TP instruction)
robot.rmi.set_payload_schedule(1)

robot.disconnect()
```

## Position recording

The RMI Position Record menu (UTILITIES on the teach pendant) lets an operator jog the robot to a position and press **Record**. The controller sends the position back to the connected remote device as a packet. Subscribe to `RecordedCartesianPositionReceived` or `RecordedJointPositionReceived` to receive these positions.

The position ID is assigned by the controller and increments with each recorded position. Use it to correlate incoming positions with your application data.

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.rmi.enable = True
robot.connect(parameters)

# Subscribe before connecting to the RMI session.
# The controller fires these events when the operator uses the
# RMI Position Record menu on the teach pendant (UTILITIES > RMI Position Record)
# and presses the Record key.

def on_cartesian(rec):
    print(f"Recorded Cartesian pos {rec.position_id}:")
    print(f"  X={rec.position.x:.1f}  Y={rec.position.y:.1f}  Z={rec.position.z:.1f}")
    print(f"  W={rec.position.w:.1f}  P={rec.position.p:.1f}  R={rec.position.r:.1f}")
    print(f"  Tool={rec.position.tool}  Frame={rec.position.frame}")

robot.rmi.recorded_cartesian_position_received(on_cartesian)

def on_joint(rec):
    print(f"Recorded joint pos {rec.position_id}:")
    print(f"  J1={rec.joints.j1:.2f}  J2={rec.joints.j2:.2f}  J3={rec.joints.j3:.2f}")
    print(f"  J4={rec.joints.j4:.2f}  J5={rec.joints.j5:.2f}  J6={rec.joints.j6:.2f}")

robot.rmi.recorded_joint_position_received(on_joint)

# Keep the application alive while the operator records positions
input("Waiting for positions. Press ENTER to exit.")

robot.disconnect()
```

## Complete example

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters
from underautomation.fanuc.rmi.tp_instructions.linear_motion_tp_instruction import LinearMotionTpInstruction
from underautomation.fanuc.rmi.data.rmi_linear_speed_type import RmiLinearSpeedType
from underautomation.fanuc.rmi.data.rmi_termination_type import RmiTerminationType
from underautomation.fanuc.rmi.data.rmi_on_off import RmiOnOff
from underautomation.fanuc.common.cartesian_position_with_user_frame import CartesianPositionWithUserFrame
from underautomation.fanuc.common.xyzwpr_position import XYZWPRPosition

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.rmi.enable = True
robot.connect(parameters)

print("Protocol version:", robot.rmi.major_version, ".", robot.rmi.minor_version)

# Verify the controller is ready
status = robot.rmi.get_status()
if not status.servo_ready or status.tp_enabled:
    print("Controller not ready for RMI.")
    robot.disconnect()
    exit()

# Read current position before moving
pos = robot.rmi.read_cartesian_position()
print(f"Start: X={pos.position.x:.1f} Y={pos.position.y:.1f} Z={pos.position.z:.1f}")

# Read UFrame 1
uf = robot.rmi.read_u_frame(1)
print(f"UFrame 1 origin: X={uf.frame.x:.1f}")

# Read DI[1]
din = robot.rmi.read_din(1)
print(f"DI[1] = {din.port_value}")

# Read R[1]
r1 = robot.rmi.read_numeric_register(1)
print(f"R[1] = {r1.value.real_value}")

# Initialize and send some motion
robot.rmi.initialize()
robot.rmi.set_override(50)

instr = LinearMotionTpInstruction()
instr.speed_type = RmiLinearSpeedType.MmSec
instr.speed = 100
instr.term_type = RmiTerminationType.Fine
instr.target = CartesianPositionWithUserFrame(500, 200, 300, 0, 90, 0, 1, 0)
robot.rmi.send_tp_instruction(instr).wait_for_completion()

# Write DO[1] ON
robot.rmi.write_dout(1, RmiOnOff.ON)

# Read TCP speed
tcp = robot.rmi.read_tcp_speed()
print(f"TCP speed: {tcp.speed:.1f} mm/s")

robot.rmi.abort()
robot.disconnect()
```

## API reference

**RmiControllerStatusResponse** ([reference](../api/underautomation.fanuc.rmi.data.md#rmicontrollerstatusresponse))

- `RmiControllerStatusResponse()`
- `servo_ready: bool`: The robot controller is ready for motion
- `tp_enabled: bool`: Teach Pendant Enabled (Switch on position ON) The Remote Motion interface only works when the teach pendant is disabled
- `rmi_motion_status: bool`: The Remote Motion Interface is running
- `program_status: TaskStatus`: RMI_MOVE program status
- `single_step_mode: bool`: Single step mode
- `number_u_tool: int`: Number of user tools available in the robot controller
- `next_sequence_id: int | None`: The next valid sequence ID. This key is only valid if the system variable $RMI_CFG.$Chk_seqID = TRUE
- `number_u_frame: int`: Number of user frames available in the robot controller
- `speed_override: int`: The current speed override setting (1–100).
- `check_sequence_id: bool (read only)`: Indicates the value of $RMI_CFG.$Chk_seqID, which is the configuration value that determines whether the controller checks valid incremented sequence IDs on incoming instructions.
- Inherited from [RmiResponseBase](../api/underautomation.fanuc.rmi.data.md#rmiresponsebase): `error_id`, `error_text`

**RmiExtendedControllerStatusResponse** ([reference](../api/underautomation.fanuc.rmi.data.md#rmiextendedcontrollerstatusresponse))

- `RmiExtendedControllerStatusResponse()`
- `error_code: str`: Last reported error code text, or null when no error is active.
- `in_motion: bool`: Whether the robot is currently executing a motion.
- `control_mode: str`: Active control mode string (e.g. "AUTO"), or null when unavailable.
- `drives_powered: bool`: Whether the servo drives are powered on.
- `gen_override: int`: General speed override percentage.
- `speed_clamp_limit: float | None`: Speed clamp limit in mm/s, or null when not configured.
- Inherited from [RmiResponseBase](../api/underautomation.fanuc.rmi.data.md#rmiresponsebase): `error_id`, `error_text`

**RmiUFrameUToolNumbersResponse** ([reference](../api/underautomation.fanuc.rmi.data.md#rmiuframeutoolnumbersresponse))

- `RmiUFrameUToolNumbersResponse()`
- `frame: int`: Current user frame number.
- `tool: int`: Current user tool number.
- `group: int | None`: Motion group number, or null when not applicable.
- Inherited from [RmiResponseBase](../api/underautomation.fanuc.rmi.data.md#rmiresponsebase): `error_id`, `error_text`

**RmiIndexedFrameResponse** ([reference](../api/underautomation.fanuc.rmi.data.md#rmiindexedframeresponse))

- `RmiIndexedFrameResponse()`
- `index: int`: Index (UFRAME or UTOOL number).
- `frame: XYZWPRPosition`: Frame data.
- Inherited from [RmiResponseBase](../api/underautomation.fanuc.rmi.data.md#rmiresponsebase): `error_id`, `error_text`

**RmiDigitalInputValueResponse** ([reference](../api/underautomation.fanuc.rmi.data.md#rmidigitalinputvalueresponse))

- `RmiDigitalInputValueResponse()`
- `port_number: int`: Port number.
- `port_value: RmiOnOff`: Port value
- Inherited from [RmiResponseBase](../api/underautomation.fanuc.rmi.data.md#rmiresponsebase): `error_id`, `error_text`

**RmiIoPortValueResponse** ([reference](../api/underautomation.fanuc.rmi.data.md#rmiioportvalueresponse))

- `RmiIoPortValueResponse()`
- `port_type: RmiIoPortType`: Port type (DI, DO, AI, AO, GO, etc.).
- `port_number: int`: Port number.
- `value: float`: Current port value.
- Inherited from [RmiResponseBase](../api/underautomation.fanuc.rmi.data.md#rmiresponsebase): `error_id`, `error_text`

**RmiCartesianPositionResponse** ([reference](../api/underautomation.fanuc.rmi.data.md#rmicartesianpositionresponse))

- `RmiCartesianPositionResponse()`
- `position: CartesianPositionWithUserFrame`: Current TCP position including configuration and active frame/tool numbers.
- Inherited from [RmiTimedResponse](../api/underautomation.fanuc.rmi.data.md#rmitimedresponse): `time_tag`
- Inherited from [RmiResponseBase](../api/underautomation.fanuc.rmi.data.md#rmiresponsebase): `error_id`, `error_text`

**RmiJointAnglesSampleResponse** ([reference](../api/underautomation.fanuc.rmi.data.md#rmijointanglessampleresponse))

- `RmiJointAnglesSampleResponse()`
- `joint_angle: JointsPosition`: Joint angle set in degrees.
- Inherited from [RmiTimedResponse](../api/underautomation.fanuc.rmi.data.md#rmitimedresponse): `time_tag`
- Inherited from [RmiResponseBase](../api/underautomation.fanuc.rmi.data.md#rmiresponsebase): `error_id`, `error_text`

**RmiPositionRegisterDataResponse** ([reference](../api/underautomation.fanuc.rmi.data.md#rmipositionregisterdataresponse))

- `RmiPositionRegisterDataResponse()`
- `register_number: int`: Register number
- `cartesian_position: CartesianPositionWithUserFrame`: Position register value.
- Inherited from [RmiResponseBase](../api/underautomation.fanuc.rmi.data.md#rmiresponsebase): `error_id`, `error_text`

**RmiNumericRegisterValueResponse** ([reference](../api/underautomation.fanuc.rmi.data.md#rminumericregistervalueresponse))

- `RmiNumericRegisterValueResponse()`
- `register_number: int`: Register number.
- `value: NumericRegister`: Register value.
- Inherited from [RmiResponseBase](../api/underautomation.fanuc.rmi.data.md#rmiresponsebase): `error_id`, `error_text`

**RmiVariableValueResponse** ([reference](../api/underautomation.fanuc.rmi.data.md#rmivariablevalueresponse))

- `RmiVariableValueResponse()`
- `name: str`: Variable name, including the leading $ character.
- `is_integer: bool`: Whether the variable holds a floating-point value.
- `integer_value: int`: Gets or sets the value as an integer. Internally stored as a double.
- `real_value: float`: Gets or sets the value as a double-precision floating-point number.
- Inherited from [RmiResponseBase](../api/underautomation.fanuc.rmi.data.md#rmiresponsebase): `error_id`, `error_text`

**RmiTcpSpeedResponse** ([reference](../api/underautomation.fanuc.rmi.data.md#rmitcpspeedresponse))

- `RmiTcpSpeedResponse()`
- `speed: float`: Current tool center point speed in mm/s.
- Inherited from [RmiTimedResponse](../api/underautomation.fanuc.rmi.data.md#rmitimedresponse): `time_tag`
- Inherited from [RmiResponseBase](../api/underautomation.fanuc.rmi.data.md#rmiresponsebase): `error_id`, `error_text`

**RmiSetPayloadParameters** ([reference](../api/underautomation.fanuc.rmi.data.md#rmisetpayloadparameters))

- `RmiSetPayloadParameters()`
- `schedule_number: int`: Payload schedule number to configure.
- `mass_kg: float`: Payload mass in kilograms.
- `cg_xm: float`: Center-of-gravity X offset in meters.
- `cg_ym: float`: Center-of-gravity Y offset in meters.
- `cg_zm: float`: Center-of-gravity Z offset in meters.
- `inertia_xkgm2: float | None`: Inertia around the X axis in kg·m². null omits this field from the command.
- `inertia_ykgm2: float | None`: Inertia around the Y axis in kg·m². null omits this field from the command.
- `inertia_zkgm2: float | None`: Inertia around the Z axis in kg·m². null omits this field from the command.
- `group: int | None`: Optional motion group number. null uses the active group.

**RmiSetPayloadCompensationParameters** ([reference](../api/underautomation.fanuc.rmi.data.md#rmisetpayloadcompensationparameters))

- `RmiSetPayloadCompensationParameters()`
- `schedule_number: int`: Payload schedule number to configure.
- `mass_kg: float`: Payload mass in kilograms.
- `cg_xm: float`: Center-of-gravity X offset in meters.
- `cg_ym: float`: Center-of-gravity Y offset in meters.
- `cg_zm: float`: Center-of-gravity Z offset in meters.
- `inertia_xkgm2: float`: Inertia around the X axis in kg·m².
- `inertia_ykgm2: float`: Inertia around the Y axis in kg·m².
- `inertia_zkgm2: float`: Inertia around the Z axis in kg·m².
- `group: int | None`: Optional motion group number. null uses the active group.

**RmiRecordedCartesianPosition** ([reference](../api/underautomation.fanuc.rmi.data.md#rmirecordedcartesianposition))

- `RmiRecordedCartesianPosition()`
- `position_id: int`: Position identifier assigned by the controller.
- `position: CartesianPositionWithUserFrame`: Recorded Cartesian position including arm configuration and active frame/tool numbers.

**RmiRecordedJointPosition** ([reference](../api/underautomation.fanuc.rmi.data.md#rmirecordedjointposition))

- `RmiRecordedJointPosition()`
- `position_id: int`: Position identifier assigned by the controller.
- `joints: JointsPosition`: Recorded joint angles in degrees.
