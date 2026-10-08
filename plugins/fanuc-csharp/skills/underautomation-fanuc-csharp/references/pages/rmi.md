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

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common;
using UnderAutomation.Fanuc.Rmi.Data;
using UnderAutomation.Fanuc.Rmi.TpInstructions;

public class Rmi
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");
        parameters.Rmi.Enable = true;
        robot.Connect(parameters);

        // Initialize the RMI_MOVE program on the controller.
        // TP must be disabled and the controller must be in AUTO mode.
        robot.Rmi.Initialize();

        // Linear motion at 100 mm/s to a Cartesian target (tool 1, frame 0)
        var instr = new LinearMotionTpInstruction
        {
            SpeedType = RmiLinearSpeedType.MmSec,
            Speed = 100,
            TermType = RmiTerminationType.Fine,
            Target = new CartesianPositionWithUserFrame(500, 200, 300, 0, 90, 0, tool: 1, frame: 0)
        };
        RmiInstructionResponse r = robot.Rmi.SendTpInstruction(instr);

        // Wait for the controller to confirm the motion completed
        r.WaitForCompletion();

        if (r.Status == RmiInstructionStatus.Error)
            System.Console.WriteLine("Error: " + r.ErrorText);

        // Abort when done - always end the session with Abort() or Disconnect()
        robot.Rmi.Abort();

        robot.Disconnect();
    }
}
```

## Connection

```csharp
using UnderAutomation.Fanuc;

public class RmiConnection
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();

        // Enable RMI and connect. The bootstrap port is 16001.
        // The controller assigns a working port automatically.
        ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");
        parameters.Rmi.Enable = true;
        robot.Connect(parameters);

        System.Console.WriteLine("Connected: " + robot.Rmi.Connected);
        System.Console.WriteLine("Protocol version: " + robot.Rmi.MajorVersion + "." + robot.Rmi.MinorVersion);
        System.Console.WriteLine("Working port: " + robot.Rmi.WorkingPort);

        // Subscribe to events before sending instructions
        robot.Rmi.SystemFaultReceived += seqId =>
            System.Console.WriteLine("System fault on sequence " + seqId);

        robot.Rmi.ConnectionTerminated += () =>
            System.Console.WriteLine("Controller closed the RMI session");

        robot.Rmi.RecordedCartesianPositionReceived += pos =>
            System.Console.WriteLine("Recorded position " + pos.PositionId);

        robot.Disconnect();
    }
}
```

## Initialize and status

Call `Initialize()` after connecting. Check the controller state with `GetStatus()` first if needed.

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common;
using UnderAutomation.Fanuc.Rmi.Data;

public class RmiInit
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");
        parameters.Rmi.Enable = true;
        robot.Connect(parameters);

        // Check controller state before initializing
        RmiControllerStatusResponse status = robot.Rmi.GetStatus();
        System.Console.WriteLine("Servo ready: " + status.ServoReady);
        System.Console.WriteLine("TP enabled: " + status.TPEnabled);
        System.Console.WriteLine("RMI running: " + status.RmiMotionStatus);

        // Initialize: creates and starts the RMI_MOVE TP program.
        // Will throw if TP is enabled or servos are off.
        robot.Rmi.Initialize();

        // For multi-group controllers, specify a group mask (bit N = group N+1)
        // robot.Rmi.Initialize(groupMask: 0b00000011);  // groups 1 and 2

        // Enable real-time singularity avoidance (requires MajorVersion >= 6, R792 option)
        // robot.Rmi.Initialize(rtsa: true);

        // Set palletizing motion mode (requires MajorVersion >= 7)
        // robot.Rmi.Initialize(pltzMode: RmiPltzMode.ZeroDown);

        System.Console.WriteLine("RMI initialized");

        // The controller checks sequence IDs by default.
        // AutoSetNextSequenceId() resynchronizes the counter if needed.
        robot.Rmi.AutoSetNextSequenceId();

        robot.Rmi.Abort();
        robot.Disconnect();
    }
}
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

**RmiClient** ([reference](../api/UnderAutomation.Fanuc.Rmi.md#rmiclient))

- `RmiClient()`: Creates a new instance of the RMI client.
- `void Connect(string ip, int port = 16001, int readTimeoutMs = 2000)`: Connect to the FANUC controller using the RMI protocol.
- Inherited from [RmiClientBase](../api/UnderAutomation.Fanuc.Rmi.Internal.md#rmiclientbase-robotrmi): `Disconnect`, `Initialize`, `Abort`, `Pause`, `Continue`, `Reset`, `ReadError`, `GetUFrameUTool`, `SetUFrameUTool`, `GetStatus`, `AutoSetNextSequenceId`, `GetExtendedStatus`, `ReadUFrame`, `WriteUFrame`, `ReadUTool`, `WriteUTool`, `ReadDIN`, `WriteDOUT`, `ReadIOPort`, `WriteIOPort`, `ReadCartesianPosition`, `ReadJointAngles`, `SetOverride`, `ReadPositionRegister`, `WritePositionRegisterCartesian`, `ReadNumericRegister`, `WriteNumericRegisterAsInteger`, `WriteNumericRegisterAsDouble`, `ReadVariable`, `WriteVariableAsInteger`, `WriteVariableAsDouble`, `ReadTcpSpeed`, `SetPayloadSchedule`, `SetPayloadValue`, `SetPayloadCompensation`, `ClearCompletedInstructions`, `ClearLocalQueuedInstructions`, `SendTpInstruction`, `Dispose`, `Connected`, `MajorVersion`, `MinorVersion`, `WorkingPort`, `LastSequenceId`, `CheckSequenceId`, `IsInHoldState`, `ReadTimeoutMs`, `Instructions`, `ConnectionTerminated`, `SystemFaultReceived`, `RecordedCartesianPositionReceived`, `RecordedJointPositionReceived`, `UnknownPacketReceived`

**RmiClientBase** ([reference](../api/UnderAutomation.Fanuc.Rmi.Internal.md#rmiclientbase-robotrmi))

- `RmiClientBase()`: Creates a new instance of the RMI client.
- `void Abort()`: Abort the running motion program. Note that a Reset() will be called automatically if the controller is in the HOLD state.
- `RmiControllerStatusResponse AutoSetNextSequenceId()`: Calls internally RmiClientBase.GetStatus and set RmiClientBase.LastSequenceId only if $RMI_CFG.$Chk_seqID = FALSE. It also set RmiClientBase.CheckSequenceId to $RMI_CFG.$Chk_seqID.
- `bool CheckSequenceId { get; set; }`: Indicates whether the controller checks for consecutive sequence IDs in motion instructions ($RMI_CFG.$Chk_seqID). Modified by RmiClientBase.AutoSetNextSequenceId.
- `void ClearCompletedInstructions()`: Removes all instructions with a terminal status (RmiInstructionStatus.Completed or RmiInstructionStatus.Error) from the tracked instruction list. Instructions that are still pending or in progress are not affected.
- `void ClearLocalQueuedInstructions()`: Cancels and removes all instructions that are still in the local client buffer (RmiInstructionStatus.LocalQueued). These instructions have not been sent to the controller yet. Each cancelled instruction is marked with an error so that any thread blocked on WaitForCompletion(System.Int32) is unblo...
- `bool Connected { get; }`: Indicates that the client is currently connected to the controller working port.
- `event Action ConnectionTerminated`: Fired when the controller closes the session (e.g. communication idle timeout). The client is automatically disconnected after this event fires.
- `void Continue()`: Resume a paused motion program.
- `void Disconnect()`: Disconnect from the controller by sending the disconnect command on the working port. Safe to call even when already disconnected.
- `void Dispose()`: Disconnect from the controller and release resources.
- `RmiExtendedControllerStatusResponse GetExtendedStatus()`: Get extended controller status including drive power state and speed clamp.
- `RmiControllerStatusResponse GetStatus()`: Get the current controller and RMI motion status.
- `RmiUFrameUToolNumbersResponse GetUFrameUTool(byte? group = null)`: Get the current UFRAME and UTOOL numbers.
- `void Initialize(byte? groupMask = null, bool? rtsa = null, RmiPltzMode? pltzMode = null)`: Initialize RMI and start the motion program. Must be called before sending any motion instructions. It also Resets RmiClientBase.LastSequenceId and empty the instruction buffer RmiClientBase.Instructions
- `RmiInstructionResponse[] Instructions { get; }`: All instructions submitted since the last Data.RmiPltzMode%7d) or explicit clear, in submission order. Includes instructions in all states: RmiInstructionStatus.LocalQueued, RmiInstructionStatus.ControllerQueued, RmiInstructionStatus.Executing, RmiInstructionStatus.Completed and RmiInstructionSta...
- `bool IsInHoldState { get; }`: Indicates that the controller has entered the HOLD state and will not accept new TP instructions until RmiClientBase.Reset is called. The HOLD state is entered in two situations: An invalid sequence ID was detected (error RMIT-029, error code 2556957). RMI checks that sequence IDs are consecutive...
- `int LastSequenceId { get; }`: Sequence ID used for the last instruction sent to the controller. Reset to 0 by Data.RmiPltzMode%7d).. Modified by RmiClientBase.AutoSetNextSequenceId.
- `short MajorVersion { get; }`: Controller protocol major version reported during the connection handshake.
- `short MinorVersion { get; }`: Controller protocol minor version reported during the connection handshake.
- `void Pause()`: Pause the running motion program.
- `RmiCartesianPositionResponse ReadCartesianPosition(byte? group = null)`: Read current Cartesian TCP position.
- `RmiDigitalInputValueResponse ReadDIN(short portNumber)`: Read a digital input port value.
- `RmiControllerErrorTextResponse ReadError(byte? count = null)`: Read the most recent controller error text. Up to 5 consecutive errors can be requested.
- `RmiIoPortValueResponse ReadIOPort(RmiIoPortType portType, int portNumber)`: Read a generic IO port (DI, DO, AI, AO, GO, RO, FLAG, RI, UI, UO).
- `RmiJointAnglesSampleResponse ReadJointAngles(byte? group = null)`: Read current joint angles.
- `RmiNumericRegisterValueResponse ReadNumericRegister(int number)`: Read a numeric register
- `RmiPositionRegisterDataResponse ReadPositionRegister(short number, byte? group = null)`: Read a position register
- `RmiTcpSpeedResponse ReadTcpSpeed()`: Read the current TCP speed in mm/s.
- `int ReadTimeoutMs { get; }`: RMI connection parameters used during Connect().
- `RmiIndexedFrameResponse ReadUFrame(byte number, byte? group = null)`: Read the UFRAME at the given index.
- `RmiIndexedFrameResponse ReadUTool(byte number, byte? group = null)`: Read the UTOOL at the given index.
- `RmiVariableValueResponse ReadVariable(string name)`: Read a system variable by name (name must include the leading $ character).
- `event Action<RmiRecordedCartesianPosition> RecordedCartesianPositionReceived`: Fired when the controller sends a Cartesian position via the RMI Position Record menu.
- `event Action<RmiRecordedJointPosition> RecordedJointPositionReceived`: Fired when the controller sends a joint position via the RMI Position Record menu.
- `void Reset()`: Reset controller errors and exit the HOLD state.
- `RmiInstructionResponse SendTpInstruction(RmiInstructionBase instruction)`: Sends the instruction to the controller, which queues it. Returns an Data.RmiInstructionResponse that tracks execution.
- `void SetOverride(byte value)`: Set the program speed override (1–100 %).
- `void SetPayloadCompensation(byte scheduleNumber, float massKg, float cgXm, float cgYm, float cgZm, float inertiaXkgm2, float inertiaYkgm2, float inertiaZkgm2, byte? group = null)`: Define payload compensation parameters for a payload schedule.
- `void SetPayloadCompensation(RmiSetPayloadCompensationParameters p)`: Define payload compensation parameters for a payload schedule.
- `void SetPayloadSchedule(byte scheduleNumber, byte? group = null)`: Immediately apply a payload schedule to the active group (command, not an instruction).
- `void SetPayloadValue(byte scheduleNumber, float massKg, float cgXm, float cgYm, float cgZm, float? inertiaXkgm2 = null, float? inertiaYkgm2 = null, float? inertiaZkgm2 = null, byte? group = null)`: Define payload mass, center of gravity, and optionally inertia for a payload schedule.
- `void SetPayloadValue(RmiSetPayloadParameters p)`: Define payload mass, center of gravity, and optionally inertia for a payload schedule.
- `void SetUFrameUTool(byte uframe, byte utool, byte? group = null)`: Set the current UFRAME and UTOOL numbers.
- `event Action<int> SystemFaultReceived`: Fired when the controller reports a system fault on a given sequence. The argument is the SequenceID of the faulted instruction (0 when unknown).
- `event Action<RmiResponseBase> UnknownPacketReceived`: Fired when the controller sends a response that the SDK does not know.
- `int WorkingPort { get; }`: Working port returned by the controller; all commands use this port after connection.
- `void WriteDOUT(short portNumber, RmiOnOff value)`: Write a digital output port value.
- `void WriteIOPort(RmiIoPortType portType, int portNumber, double value)`: Write a generic IO port (AO, GO, DO, RO, FLAG).
- `void WriteNumericRegisterAsDouble(int number, double value)`: Write a float value to a numeric register
- `void WriteNumericRegisterAsInteger(int number, int value)`: Write an integer value to a numeric register
- `void WritePositionRegisterCartesian(short number, CartesianPositionWithUserFrame target, byte? group = null)`: Write a Cartesian position register
- `void WriteUFrame(byte number, XYZWPRPosition position, byte? group = null)`: Write the UFRAME at the given index.
- `void WriteUTool(byte number, XYZWPRPosition position, byte? group = null)`: Write the UTOOL at the given index.
- `void WriteVariableAsDouble(string name, double value)`: Write a float value to a system variable (name must include the leading $).
- `void WriteVariableAsInteger(string name, int value)`: Write an integer value to a system variable (name must include the leading $).

**RmiInstructionResponse** ([reference](../api/UnderAutomation.Fanuc.Rmi.Data.md#rmiinstructionresponse))

- `RmiInstructionResponse()`
- `RmiInstructionBase Instruction { get; }`: Sent instruction
- `int SequenceId { get; }`: Sequence identifier assigned to this instruction. 0 until the instruction has been dispatched to the controller.
- `RmiInstructionStatus Status { get; }`: Current execution state of the instruction.
- `event Action<RmiInstructionStatus> StatusChanged`: Fired each time RmiInstructionResponse.Status changes. The argument is the new status value. This event may be raised from a background thread.
- `bool WaitForCompletion(int timeoutMs = -1)`: Blocks the calling thread until the instruction reaches a terminal state (RmiInstructionStatus.Completed or RmiInstructionStatus.Error), or until timeoutMs milliseconds have elapsed. Pass -1 (or omit) to wait indefinitely.
- Inherited from [RmiResponseBase](../api/UnderAutomation.Fanuc.Rmi.Data.md#rmiresponsebase): `ErrorId`, `ErrorText`

**RmiControllerStatusResponse** ([reference](../api/UnderAutomation.Fanuc.Rmi.Data.md#rmicontrollerstatusresponse))

- `RmiControllerStatusResponse()`
- `bool CheckSequenceId { get; }`: Indicates the value of $RMI_CFG.$Chk_seqID, which is the configuration value that determines whether the controller checks valid incremented sequence IDs on incoming instructions.
- `int? NextSequenceId { get; set; }`: The next valid sequence ID. This key is only valid if the system variable $RMI_CFG.$Chk_seqID = TRUE
- `byte NumberUFrame { get; set; }`: Number of user frames available in the robot controller
- `byte NumberUTool { get; set; }`: Number of user tools available in the robot controller
- `TaskStatus ProgramStatus { get; set; }`: RMI_MOVE program status
- `bool RmiMotionStatus { get; set; }`: The Remote Motion Interface is running
- `bool ServoReady { get; set; }`: The robot controller is ready for motion
- `bool SingleStepMode { get; set; }`: Single step mode
- `byte SpeedOverride { get; set; }`: The current speed override setting (1–100).
- `bool TPEnabled { get; set; }`: Teach Pendant Enabled (Switch on position ON) The Remote Motion interface only works when the teach pendant is disabled
- Inherited from [RmiResponseBase](../api/UnderAutomation.Fanuc.Rmi.Data.md#rmiresponsebase): `ErrorId`, `ErrorText`
