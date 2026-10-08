# RMI overview

RMI (Remote Motion Interface) is a TCP-based protocol for sending motion commands, managing frames, and controlling the robot remotely.

Web page: https://underautomation.com/fanuc/documentation/rmi

RMI (Remote Motion Interface) is a TCP-based protocol that lets you send TP-equivalent motion instructions and administrative commands to a Fanuc controller in real time.

## Robot requirements

- **Option R912** (Remote Motion Interface) must be loaded on the controller.
- The bootstrap port is **16001** (TCP).
- Before calling `Initialize()`, the teach pendant must be **disabled** and the controller must be in **AUTO mode**.
- Do not leave the RMI_MOVE TP program selected on the teach pendant before calling `Initialize()`.

## How it works

1. **Connect** to the controller on the bootstrap port (16001). The controller assigns a working port for the session.
2. Call **`Initialize()`** to create the `RMI_MOVE` TP program and start it.
3. Send motion or non-motion instructions via **`SendTpInstruction()`**. Each call returns an `RmiInstructionResponse` you can track.
4. The client manages the 8-slot controller buffer automatically. Instructions beyond that limit are held locally and sent as soon as a slot is free.
5. When done, call **`Abort()`** or **`Disconnect()`**. Always end your session with one of those; otherwise the controller keeps RMI_MOVE selected and other TP programs cannot run.

## Quick example

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

# Initialize the RMI_MOVE program on the controller.
# TP must be disabled and the controller must be in AUTO mode.
robot.rmi.initialize()

# Linear motion at 100 mm/s to a Cartesian target (tool 1, frame 0)
instr = LinearMotionTpInstruction()
instr.speed_type = RmiLinearSpeedType.MmSec
instr.speed = 100
instr.term_type = RmiTerminationType.Fine
instr.target = CartesianPositionWithUserFrame(500, 200, 300, 0, 90, 0, 1, 0)

r = robot.rmi.send_tp_instruction(instr)

# Wait for the controller to confirm the motion completed
r.wait_for_completion()

if r.status == RmiInstructionStatus.Error:
    print("Error:", r.error_text)

# Abort when done - always end the session with abort() or disconnect()
robot.rmi.abort()

robot.disconnect()
```

## Connection

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters

robot = FanucRobot()

# Enable RMI and connect. The bootstrap port is 16001.
# The controller assigns a working port automatically.
parameters = ConnectionParameters("192.168.0.1")
parameters.rmi.enable = True
robot.connect(parameters)

print("Connected:", robot.rmi.connected)
print("Protocol version:", robot.rmi.major_version, ".", robot.rmi.minor_version)
print("Working port:", robot.rmi.working_port)

# Subscribe to events before sending instructions
def on_fault(seq_id):
    print("System fault on sequence", seq_id)
robot.rmi.system_fault_received += on_fault

def on_terminated():
    print("Controller closed the RMI session")
robot.rmi.connection_terminated += on_terminated

def on_pos_recorded(pos):
    print("Recorded position", pos.position_id)
robot.rmi.recorded_cartesian_position_received += on_pos_recorded

robot.disconnect()
```

## Initialize and status

Call `Initialize()` after connecting. Check the controller state with `GetStatus()` first if needed.

```python
from underautomation.fanuc.fanuc_robot import FanucRobot
from underautomation.fanuc.connection_parameters import ConnectionParameters
from underautomation.fanuc.rmi.data.rmi_pltz_mode import RmiPltzMode

robot = FanucRobot()
parameters = ConnectionParameters("192.168.0.1")
parameters.rmi.enable = True
robot.connect(parameters)

# Check controller state before initializing
status = robot.rmi.get_status()
print("Servo ready:", status.servo_ready)
print("TP enabled: ", status.tp_enabled)
print("RMI running:", status.rmi_motion_status)

# Initialize: creates and starts the RMI_MOVE TP program.
# Will throw if TP is enabled or servos are off.
robot.rmi.initialize()

# For multi-group controllers (requires MajorVersion >= 2)
# robot.rmi.initialize(group_mask=0b00000011)  # groups 1 and 2

# Enable real-time singularity avoidance (requires MajorVersion >= 6, R792 option)
# robot.rmi.initialize(rtsa=True)

# Set palletizing motion mode (requires MajorVersion >= 7)
# robot.rmi.initialize(pltz_mode=RmiPltzMode.ZeroDown)

print("RMI initialized")

# Resynchronize the sequence ID counter if needed
robot.rmi.auto_set_next_sequence_id()

robot.rmi.abort()

robot.disconnect()
```

## Instruction pipeline

`SendTpInstruction()` returns an `RmiInstructionResponse` immediately. The instruction goes through several states:

| Status | Meaning |
|--------|---------|
| `LocalQueued` | Held in the client buffer, not yet sent (controller buffer full). |
| `ControllerQueued` | Sent to the controller, waiting its turn. |
| `Executing` | The robot is currently executing this instruction. |
| `Completed` | Done without error. |
| `Error` | Failed. Check `ErrorId` and `ErrorText`. |

Call `WaitForCompletion()` to block until the instruction reaches a terminal state.

## Troubleshooting

### "Connection refused by controller"

`Connect()` throws a `ConnectException` with this message. It is not a network problem: the controller answered on port 16001, then refused the RMI session. The inner exception is an `RmiException`, and its `ErrorId` gives the error code of the controller.

Check:

- Option R912 is loaded on the controller.
- No alarm is active on the teach pendant. Reset the alarms and try again.
- No other RMI session is open. A session that was not ended with `Abort()` or `Disconnect()` keeps `RMI_MOVE` selected. Abort the programs on the teach pendant (`FCTN`, `ABORT (ALL)`), then connect again.

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Next steps

- [Motion commands](rmi-motion.md): linear, joint, circular, spline motions and non-motion instructions.
- [Frames, I/O & status](rmi-frames-io.md): frame management, I/O, position reading, registers.

## API reference

**RmiClient** ([reference](../api/underautomation.fanuc.rmi.md#rmiclient))

- `RmiClient()`: Creates a new instance of the RMI client.
- `connect(ip: str, port: int=16001, readTimeoutMs: int=2000) -> None`: Connect to the FANUC controller using the RMI protocol.
- Inherited from [RmiClientBase](../api/underautomation.fanuc.rmi.internal.md#rmiclientbase-robotrmi): `disconnect`, `initialize`, `abort`, `pause`, `continue_`, `reset`, `read_error`, `get_u_frame_u_tool`, `set_u_frame_u_tool`, `get_status`, `auto_set_next_sequence_id`, `get_extended_status`, `read_u_frame`, `write_u_frame`, `read_u_tool`, `write_u_tool`, `read_din`, `write_dout`, `read_io_port`, `write_io_port`, `read_cartesian_position`, `read_joint_angles`, `set_override`, `read_position_register`, `write_position_register_cartesian`, `read_numeric_register`, `write_numeric_register_as_integer`, `write_numeric_register_as_double`, `read_variable`, `write_variable_as_integer`, `write_variable_as_double`, `read_tcp_speed`, `set_payload_schedule`, `set_payload_value`, `set_payload_compensation`, `clear_completed_instructions`, `clear_local_queued_instructions`, `send_tp_instruction`, `dispose`, `connected`, `major_version`, `minor_version`, `working_port`, `last_sequence_id`, `check_sequence_id`, `is_in_hold_state`, `read_timeout_ms`, `instructions`, `connection_terminated`, `system_fault_received`, `recorded_cartesian_position_received`, `recorded_joint_position_received`, `unknown_packet_received`

**RmiClientBase** ([reference](../api/underautomation.fanuc.rmi.internal.md#rmiclientbase-robotrmi))

- `RmiClientBase()`: Creates a new instance of the RMI client.
- `connection_terminated(handler)`: Fired when the controller closes the session (e.g. communication idle timeout). The client is automatically disconnected after this event fires.
- `system_fault_received(handler)`: Fired when the controller reports a system fault on a given sequence. The argument is the SequenceID of the faulted instruction (0 when unknown).
- `recorded_cartesian_position_received(handler)`: Fired when the controller sends a Cartesian position via the RMI Position Record menu.
- `recorded_joint_position_received(handler)`: Fired when the controller sends a joint position via the RMI Position Record menu.
- `unknown_packet_received(handler)`: Fired when an unknown packet is received from the controller.
- `disconnect() -> None`: Disconnect from the controller by sending the disconnect command on the working port. Safe to call even when already disconnected.
- `initialize(groupMask: int | None=None, rtsa: bool | None=None, pltzMode: RmiPltzMode | None=None) -> None`: Initialize RMI and start the motion program. Must be called before sending any motion instructions. It also Resets last_sequence_id and empty the instruction buffer instructions
- `abort() -> None`: Abort the running motion program. Note that a Reset() will be called automatically if the controller is in the HOLD state.
- `pause() -> None`: Pause the running motion program.
- `continue_() -> None`: Resume a paused motion program.
- `reset() -> None`: Reset controller errors and exit the HOLD state.
- `read_error(count: int | None=None) -> RmiControllerErrorTextResponse`: Read the most recent controller error text. Up to 5 consecutive errors can be requested.
- `get_u_frame_u_tool(group: int | None=None) -> RmiUFrameUToolNumbersResponse`: Get the current UFRAME and UTOOL numbers.
- `set_u_frame_u_tool(uframe: int, utool: int, group: int | None=None) -> None`: Set the current UFRAME and UTOOL numbers.
- `get_status() -> RmiControllerStatusResponse`: Get the current controller and RMI motion status.
- `auto_set_next_sequence_id() -> RmiControllerStatusResponse`: Calls internally get_status() and set last_sequence_id only if $RMI_CFG.$Chk_seqID = FALSE. It also set check_sequence_id to $RMI_CFG.$Chk_seqID.
- `get_extended_status() -> RmiExtendedControllerStatusResponse`: Get extended controller status including drive power state and speed clamp.
- `read_u_frame(number: int, group: int | None=None) -> RmiIndexedFrameResponse`: Read the UFRAME at the given index.
- `write_u_frame(number: int, position: XYZWPRPosition, group: int | None=None) -> None`: Write the UFRAME at the given index.
- `read_u_tool(number: int, group: int | None=None) -> RmiIndexedFrameResponse`: Read the UTOOL at the given index.
- `write_u_tool(number: int, position: XYZWPRPosition, group: int | None=None) -> None`: Write the UTOOL at the given index.
- `read_din(portNumber: int) -> RmiDigitalInputValueResponse`: Read a digital input port value.
- `write_dout(portNumber: int, value: RmiOnOff) -> None`: Write a digital output port value.
- `read_io_port(portType: RmiIoPortType, portNumber: int) -> RmiIoPortValueResponse`: Read a generic IO port (DI, DO, AI, AO, GO, RO, FLAG, RI, UI, UO).
- `write_io_port(portType: RmiIoPortType, portNumber: int, value: float) -> None`: Write a generic IO port (AO, GO, DO, RO, FLAG).
- `read_cartesian_position(group: int | None=None) -> RmiCartesianPositionResponse`: Read current Cartesian TCP position.
- `read_joint_angles(group: int | None=None) -> RmiJointAnglesSampleResponse`: Read current joint angles.
- `set_override(value: int) -> None`: Set the program speed override (1–100 %).
- `read_position_register(number: int, group: int | None=None) -> RmiPositionRegisterDataResponse`: Read a position register
- `write_position_register_cartesian(number: int, target: CartesianPositionWithUserFrame, group: int | None=None) -> None`: Write a Cartesian position register
- `read_numeric_register(number: int) -> RmiNumericRegisterValueResponse`: Read a numeric register
- `write_numeric_register_as_integer(number: int, value: int) -> None`: Write an integer value to a numeric register
- `write_numeric_register_as_double(number: int, value: float) -> None`: Write a float value to a numeric register
- `read_variable(name: str) -> RmiVariableValueResponse`: Read a system variable by name (name must include the leading $ character).
- `write_variable_as_integer(name: str, value: int) -> None`: Write an integer value to a system variable (name must include the leading $).
- `write_variable_as_double(name: str, value: float) -> None`: Write a float value to a system variable (name must include the leading $).
- `read_tcp_speed() -> RmiTcpSpeedResponse`: Read the current TCP speed in mm/s.
- `set_payload_schedule(scheduleNumber: int, group: int | None=None) -> None`: Immediately apply a payload schedule to the active group (command, not an instruction).
- `set_payload_value(scheduleNumber: int, massKg: float, cgXm: float, cgYm: float, cgZm: float, inertiaXkgm2: float | None=None, inertiaYkgm2: float | None=None, inertiaZkgm2: float | None=None, group: int | None=None) -> None`: Define payload mass, center of gravity, and optionally inertia for a payload schedule.
- `set_payload_value(p: RmiSetPayloadParameters) -> None`: Define payload mass, center of gravity, and optionally inertia for a payload schedule.
- `set_payload_compensation(scheduleNumber: int, massKg: float, cgXm: float, cgYm: float, cgZm: float, inertiaXkgm2: float, inertiaYkgm2: float, inertiaZkgm2: float, group: int | None=None) -> None`: Define payload compensation parameters for a payload schedule.
- `set_payload_compensation(p: RmiSetPayloadCompensationParameters) -> None`: Define payload compensation parameters for a payload schedule.
- `clear_completed_instructions() -> None`: Removes all instructions with a terminal status (Completed or Error) from the tracked instruction list. Instructions that are still pending or in progress are not affected.
- `clear_local_queued_instructions() -> None`: Cancels and removes all instructions that are still in the local client buffer (LocalQueued). These instructions have not been sent to the controller yet. Each cancelled instruction is marked with an error so that any thread blocked on wait_for_completion() is unblocked. Instructions already sent...
- `send_tp_instruction(instruction: RmiInstructionBase) -> RmiInstructionResponse`: Serializes the instruction to the RMI wire format and queues it on the controller. Returns an RmiInstructionResponse that tracks execution.
- `dispose() -> None`: Disconnect from the controller and release resources.
- `connected: bool (read only)`: Indicates that the client is currently connected to the controller working port.
- `major_version: int (read only)`: Controller protocol major version reported during the connection handshake.
- `minor_version: int (read only)`: Controller protocol minor version reported during the connection handshake.
- `working_port: int (read only)`: Working port returned by the controller; all commands use this port after connection.
- `last_sequence_id: int (read only)`: Sequence ID used for the last instruction sent to the controller. Reset to 0 by initialize().. Modified by auto_set_next_sequence_id().
- `check_sequence_id: bool`: Indicates whether the controller checks for consecutive sequence IDs in motion instructions ($RMI_CFG.$Chk_seqID). Modified by auto_set_next_sequence_id().
- `is_in_hold_state: bool (read only)`: Indicates that the controller has entered the HOLD state and will not accept new TP instructions until reset() is called. The HOLD state is entered in two situations: An invalid sequence ID was detected (error RMIT-029, error code 2556957). RMI checks that sequence IDs are consecutive. If a gap i...
- `read_timeout_ms: int (read only)`: RMI connection parameters used during Connect().
- `instructions: typing.List[RmiInstructionResponse] (read only)`: All instructions submitted since the last initialize() or explicit clear, in submission order. Includes instructions in all states: LocalQueued, ControllerQueued, Executing, Completed and Error. Returns a snapshot array; the array is not updated after it is returned.

**RmiInstructionResponse** ([reference](../api/underautomation.fanuc.rmi.data.md#rmiinstructionresponse))

- `RmiInstructionResponse()`
- `status_changed(handler)`: Fired each time status changes. The argument is the new status value. This event may be raised from a background thread.
- `wait_for_completion(timeoutMs: int=-1) -> bool`: Blocks the calling thread until the instruction reaches a terminal state (Completed or Error), or until timeoutMs milliseconds have elapsed. Pass -1 (or omit) to wait indefinitely.
- `sequence_id: int (read only)`: Sequence identifier assigned to this instruction. 0 until the instruction has been dispatched to the controller.
- `status: RmiInstructionStatus (read only)`: Current execution state of the instruction.
- `instruction: RmiInstructionBase (read only)`: Sent instruction
- Inherited from [RmiResponseBase](../api/underautomation.fanuc.rmi.data.md#rmiresponsebase): `error_id`, `error_text`

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
