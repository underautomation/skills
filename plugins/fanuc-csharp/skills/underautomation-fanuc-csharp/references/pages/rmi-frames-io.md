# Frames, I/O & status

Manage user frames and tools, read/write I/O, read positions, set speed override, and get controller status via RMI.

Web page: https://underautomation.com/fanuc/documentation/rmi-frames-io

RMI provides access to controller status, user frames and tools, digital and generic I/O, position reading, registers, system variables, payload, and TCP speed.

## Controller status

`GetStatus()` returns the full controller state. Use it before `Initialize()` to verify the controller is ready.

```csharp
using System;
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Rmi.Data;

public class RmiFramesIoStatus
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");
        parameters.Rmi.Enable = true;
        robot.Connect(parameters);

        // Basic status: servo, TP mode, RMI running, override
        RmiControllerStatusResponse status = robot.Rmi.GetStatus();
        Console.WriteLine("Servo ready:   " + status.ServoReady);
        Console.WriteLine("TP enabled:    " + status.TPEnabled);
        Console.WriteLine("RMI running:   " + status.RmiMotionStatus);
        Console.WriteLine("Program state: " + status.ProgramStatus);
        Console.WriteLine("Override:      " + status.SpeedOverride + "%");
        Console.WriteLine("UFrame count:  " + status.NumberUFrame);
        Console.WriteLine("UTool count:   " + status.NumberUTool);

        // Extended status: drive power, control mode, speed clamp
        RmiExtendedControllerStatusResponse ext = robot.Rmi.GetExtendedStatus();
        Console.WriteLine("Drives on:     " + ext.DrivesPowered);
        Console.WriteLine("In motion:     " + ext.InMotion);

        // Read last controller error (up to 5 at once)
        RmiControllerErrorTextResponse errors = robot.Rmi.ReadError(count: 3);
        foreach (string entry in errors.ErrorDataEntries)
            Console.WriteLine("Error: " + entry);

        // HOLD state
        Console.WriteLine("In HOLD:       " + robot.Rmi.IsInHoldState);

        robot.Disconnect();
    }
}
```

## Admin commands

```csharp
using UnderAutomation.Fanuc;

public class RmiFramesIoAdmin
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");
        parameters.Rmi.Enable = true;
        robot.Connect(parameters);
        robot.Rmi.Initialize();

        // Set speed override (1-100 %)
        robot.Rmi.SetOverride(50);

        // Pause and resume the motion program
        robot.Rmi.Pause();
        robot.Rmi.Continue();

        // Reset controller errors and exit the HOLD state
        robot.Rmi.Reset();

        // Resynchronize the sequence ID counter
        robot.Rmi.AutoSetNextSequenceId();

        // Get/set current UFRAME and UTOOL numbers
        var ut = robot.Rmi.GetUFrameUTool();
        System.Console.WriteLine("Frame: " + ut.Frame + ", Tool: " + ut.Tool);
        robot.Rmi.SetUFrameUTool(uframe: 1, utool: 2);

        // Abort the RMI_MOVE program
        robot.Rmi.Abort();

        robot.Disconnect();
    }
}
```

## Position reading

Read the current robot position and TCP speed. On firmware MajorVersion >= 6, the position reflects actual encoder counts.

```csharp
using System;
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Rmi.Data;

public class RmiFramesIoPosition
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");
        parameters.Rmi.Enable = true;
        robot.Connect(parameters);

        // Read current Cartesian position.
        // On MajorVersion >= 6, returns actual encoder position.
        RmiCartesianPositionResponse cart = robot.Rmi.ReadCartesianPosition();
        Console.WriteLine($"X={cart.Position.X:F1}  Y={cart.Position.Y:F1}  Z={cart.Position.Z:F1}");
        Console.WriteLine($"W={cart.Position.W:F1}  P={cart.Position.P:F1}  R={cart.Position.R:F1}");
        Console.WriteLine($"Tool={cart.Position.Tool}  Frame={cart.Position.Frame}");
        Console.WriteLine($"Timestamp={cart.TimeTag}");

        // Read current joint angles
        RmiJointAnglesSampleResponse joints = robot.Rmi.ReadJointAngles();
        Console.WriteLine($"J1={joints.JointAngle.J1:F2}  J2={joints.JointAngle.J2:F2}  J3={joints.JointAngle.J3:F2}");
        Console.WriteLine($"J4={joints.JointAngle.J4:F2}  J5={joints.JointAngle.J5:F2}  J6={joints.JointAngle.J6:F2}");

        // Read TCP speed (mm/s)
        RmiTcpSpeedResponse speed = robot.Rmi.ReadTcpSpeed();
        Console.WriteLine($"TCP speed={speed.Speed:F2} mm/s");

        robot.Disconnect();
    }
}
```

## User frames and tools

Read and write user frames (UFrame) and tools (UTool):

```csharp
using System;
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common;
using UnderAutomation.Fanuc.Rmi.Data;

public class RmiFramesIoFrames
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");
        parameters.Rmi.Enable = true;
        robot.Connect(parameters);

        // Read UFRAME 1
        RmiIndexedFrameResponse uf = robot.Rmi.ReadUFrame(1);
        Console.WriteLine($"UFrame 1: X={uf.Frame.X:F1}  Y={uf.Frame.Y:F1}  Z={uf.Frame.Z:F1}");

        // Write UFRAME 1
        robot.Rmi.WriteUFrame(1, new XYZWPRPosition { X = 100, Y = 0, Z = 0, W = 0, P = 0, R = 0 });

        // Read UTOOL 1
        RmiIndexedFrameResponse ut = robot.Rmi.ReadUTool(1);
        Console.WriteLine($"UTool 1: X={ut.Frame.X:F1}  Y={ut.Frame.Y:F1}  Z={ut.Frame.Z:F1}");

        // Write UTOOL 1
        robot.Rmi.WriteUTool(1, new XYZWPRPosition { X = 0, Y = 0, Z = 200, W = 0, P = 0, R = 0 });

        // Get current UFRAME and UTOOL numbers
        RmiUFrameUToolNumbersResponse current = robot.Rmi.GetUFrameUTool();
        Console.WriteLine($"Active UFRAME={current.Frame}  UTOOL={current.Tool}");

        // Set the active UFRAME and UTOOL
        robot.Rmi.SetUFrameUTool(uframe: 1, utool: 2);

        robot.Disconnect();
    }
}
```

## Digital I/O

```csharp
using System;
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Rmi.Data;

public class RmiFramesIoIo
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");
        parameters.Rmi.Enable = true;
        robot.Connect(parameters);

        // Read digital input DI[2]
        RmiDigitalInputValueResponse din = robot.Rmi.ReadDIN(2);
        Console.WriteLine($"DI[2] = {din.PortValue}");

        // Write digital output DO[1]
        robot.Rmi.WriteDOUT(1, RmiOnOff.ON);
        robot.Rmi.WriteDOUT(1, RmiOnOff.OFF);

        robot.Disconnect();
    }
}
```

## Generic I/O ports

`ReadIOPort` and `WriteIOPort` work with any port type (DI, DO, AI, AO, GO, RO, FLAG, RI, UI, UO):

```csharp
using System;
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Rmi.Data;

public class RmiFramesIoGenericIo
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");
        parameters.Rmi.Enable = true;
        robot.Connect(parameters);

        // Read any IO port type: DI, DO, AI, AO, GO, RO, FLAG, RI, UI, UO
        RmiIoPortValueResponse di = robot.Rmi.ReadIOPort(RmiIoPortType.DI, 1);
        Console.WriteLine($"DI[1] = {di.Value}");

        RmiIoPortValueResponse ai = robot.Rmi.ReadIOPort(RmiIoPortType.AI, 1);
        Console.WriteLine($"AI[1] = {ai.Value}");

        RmiIoPortValueResponse flag = robot.Rmi.ReadIOPort(RmiIoPortType.FLAG, 5);
        Console.WriteLine($"FLAG[5] = {flag.Value}");

        // Write AO[1] = 2.5
        robot.Rmi.WriteIOPort(RmiIoPortType.AO, 1, 2.5);

        // Write GO[1] = 7
        robot.Rmi.WriteIOPort(RmiIoPortType.GO, 1, 7);

        // Write FLAG[5] = 1
        robot.Rmi.WriteIOPort(RmiIoPortType.FLAG, 5, 1);

        robot.Disconnect();
    }
}
```

## Position registers

```csharp
using System;
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common;
using UnderAutomation.Fanuc.Rmi.Data;

public class RmiFramesIoPositionRegisters
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");
        parameters.Rmi.Enable = true;
        robot.Connect(parameters);

        // Read position register PR[1]
        RmiPositionRegisterDataResponse pr = robot.Rmi.ReadPositionRegister(1);
        Console.WriteLine($"PR[1]: X={pr.CartesianPosition.X:F1}  Y={pr.CartesianPosition.Y:F1}  Z={pr.CartesianPosition.Z:F1}");

        // Write position register PR[2] with a Cartesian value
        robot.Rmi.WritePositionRegisterCartesian(2,
            new CartesianPositionWithUserFrame(500, 200, 300, 0, 90, 0, tool: 1, frame: 0));

        robot.Disconnect();
    }
}
```

## Numeric registers and system variables

```csharp
using System;
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Rmi.Data;

public class RmiFramesIoRegisters
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");
        parameters.Rmi.Enable = true;
        robot.Connect(parameters);

        // Read numeric register R[1]
        RmiNumericRegisterValueResponse r1 = robot.Rmi.ReadNumericRegister(1);
        Console.WriteLine($"R[1] IsInteger={r1.Value.IsInteger}  Value={r1.Value.RealValue}");

        // Write integer value to R[1]
        robot.Rmi.WriteNumericRegisterAsInteger(1, 42);

        // Write float value to R[2]
        robot.Rmi.WriteNumericRegisterAsDouble(2, 3.14);

        // Read system variable $MCR.$GENOVERRIDE (include the leading $)
        RmiVariableValueResponse var = robot.Rmi.ReadVariable("$MCR.$GENOVERRIDE");
        Console.WriteLine($"Speed override = {var.RealValue}");

        // Write system variable
        robot.Rmi.WriteVariableAsInteger("$MCR.$GENOVERRIDE", 80);

        robot.Disconnect();
    }
}
```

## Payload

Define payload mass, center of gravity, and inertia for a schedule. You can also send a `SetPayloadTpInstruction` as a motion-sequence instruction.

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Rmi.Data;

public class RmiFramesIoPayload
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");
        parameters.Rmi.Enable = true;
        robot.Connect(parameters);

        // Define payload for schedule 1: 5 kg, center of gravity offset 0.1 m in Z
        robot.Rmi.SetPayloadValue(
            scheduleNumber: 1,
            massKg: 5.0f,
            cgXm: 0f, cgYm: 0f, cgZm: 0.1f);

        // Include inertia values
        robot.Rmi.SetPayloadValue(
            scheduleNumber: 2,
            massKg: 3.0f,
            cgXm: 0.05f, cgYm: 0f, cgZm: 0.08f,
            inertiaXkgm2: 0.002f, inertiaYkgm2: 0.002f, inertiaZkgm2: 0.001f);

        // Define payload compensation
        robot.Rmi.SetPayloadCompensation(
            scheduleNumber: 1,
            massKg: 1.0f,
            cgXm: 0f, cgYm: 0f, cgZm: 0.05f,
            inertiaXkgm2: 0.001f, inertiaYkgm2: 0.001f, inertiaZkgm2: 0.0005f);

        // Activate schedule 1 immediately (command, not a TP instruction)
        robot.Rmi.SetPayloadSchedule(1);

        robot.Disconnect();
    }
}
```

## Position recording

The RMI Position Record menu (UTILITIES on the teach pendant) lets an operator jog the robot to a position and press **Record**. The controller sends the position back to the connected remote device as a packet. Subscribe to `RecordedCartesianPositionReceived` or `RecordedJointPositionReceived` to receive these positions.

The position ID is assigned by the controller and increments with each recorded position. Use it to correlate incoming positions with your application data.

```csharp
using System;
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Rmi.Data;

public class RmiFramesIoPositionRecord
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");
        parameters.Rmi.Enable = true;
        robot.Connect(parameters);

        // Subscribe before connecting to the RMI session.
        // The controller fires these events when the operator uses the
        // RMI Position Record menu on the teach pendant (UTILITIES > RMI Position Record)
        // and presses the Record key.

        robot.Rmi.RecordedCartesianPositionReceived += (RmiRecordedCartesianPosition rec) =>
        {
            Console.WriteLine($"Recorded Cartesian pos {rec.PositionId}:");
            Console.WriteLine($"  X={rec.Position.X:F1}  Y={rec.Position.Y:F1}  Z={rec.Position.Z:F1}");
            Console.WriteLine($"  W={rec.Position.W:F1}  P={rec.Position.P:F1}  R={rec.Position.R:F1}");
            Console.WriteLine($"  Tool={rec.Position.Tool}  Frame={rec.Position.Frame}");
        };

        robot.Rmi.RecordedJointPositionReceived += (RmiRecordedJointPosition rec) =>
        {
            Console.WriteLine($"Recorded joint pos {rec.PositionId}:");
            Console.WriteLine($"  J1={rec.Joints.J1:F2}  J2={rec.Joints.J2:F2}  J3={rec.Joints.J3:F2}");
            Console.WriteLine($"  J4={rec.Joints.J4:F2}  J5={rec.Joints.J5:F2}  J6={rec.Joints.J6:F2}");
        };

        // Keep the application alive while the operator records positions
        Console.WriteLine("Waiting for positions. Press ENTER to exit.");
        Console.ReadLine();

        robot.Disconnect();
    }
}
```

## Complete example

```csharp
using System;
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common;
using UnderAutomation.Fanuc.Rmi.Data;
using UnderAutomation.Fanuc.Rmi.TpInstructions;

public class RmiFramesIo
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");
        parameters.Rmi.Enable = true;
        robot.Connect(parameters);

        Console.WriteLine("Protocol version: " + robot.Rmi.MajorVersion + "." + robot.Rmi.MinorVersion);

        // Verify the controller is ready
        var status = robot.Rmi.GetStatus();
        if (!status.ServoReady || status.TPEnabled)
        {
            Console.WriteLine("Controller not ready for RMI.");
            return;
        }

        // Read current position before moving
        var pos = robot.Rmi.ReadCartesianPosition();
        Console.WriteLine($"Start: X={pos.Position.X:F1} Y={pos.Position.Y:F1} Z={pos.Position.Z:F1}");

        // Read UFrame 1
        var uf = robot.Rmi.ReadUFrame(1);
        Console.WriteLine($"UFrame 1 origin: X={uf.Frame.X:F1}");

        // Read DI[1]
        var din = robot.Rmi.ReadDIN(1);
        Console.WriteLine($"DI[1] = {din.PortValue}");

        // Read R[1]
        var r1 = robot.Rmi.ReadNumericRegister(1);
        Console.WriteLine($"R[1] = {r1.Value.RealValue}");

        // Initialize and send some motion
        robot.Rmi.Initialize();
        robot.Rmi.SetOverride(50);

        robot.Rmi.SendTpInstruction(new LinearMotionTpInstruction
        {
            SpeedType = RmiLinearSpeedType.MmSec,
            Speed = 100,
            TermType = RmiTerminationType.Fine,
            Target = new CartesianPositionWithUserFrame(500, 200, 300, 0, 90, 0, 1, 0)
        }).WaitForCompletion();

        // Write DO[1] ON
        robot.Rmi.WriteDOUT(1, RmiOnOff.ON);

        // Read TCP speed
        var tcp = robot.Rmi.ReadTcpSpeed();
        Console.WriteLine($"TCP speed: {tcp.Speed:F1} mm/s");

        robot.Rmi.Abort();
        robot.Disconnect();
    }
}
```

## API reference

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

**RmiExtendedControllerStatusResponse** ([reference](../api/UnderAutomation.Fanuc.Rmi.Data.md#rmiextendedcontrollerstatusresponse))

- `RmiExtendedControllerStatusResponse()`
- `string ControlMode { get; set; }`: Active control mode string (e.g. "AUTO"), or null when unavailable.
- `bool DrivesPowered { get; set; }`: Whether the servo drives are powered on.
- `string ErrorCode { get; set; }`: Last reported error code text, or null when no error is active.
- `int GenOverride { get; set; }`: General speed override percentage.
- `bool InMotion { get; set; }`: Whether the robot is currently executing a motion.
- `double? SpeedClampLimit { get; set; }`: Speed clamp limit in mm/s, or null when not configured.
- Inherited from [RmiResponseBase](../api/UnderAutomation.Fanuc.Rmi.Data.md#rmiresponsebase): `ErrorId`, `ErrorText`

**RmiUFrameUToolNumbersResponse** ([reference](../api/UnderAutomation.Fanuc.Rmi.Data.md#rmiuframeutoolnumbersresponse))

- `RmiUFrameUToolNumbersResponse()`
- `byte Frame { get; set; }`: Current user frame number.
- `byte? Group { get; set; }`: Motion group number, or null when not applicable.
- `byte Tool { get; set; }`: Current user tool number.
- Inherited from [RmiResponseBase](../api/UnderAutomation.Fanuc.Rmi.Data.md#rmiresponsebase): `ErrorId`, `ErrorText`

**RmiIndexedFrameResponse** ([reference](../api/UnderAutomation.Fanuc.Rmi.Data.md#rmiindexedframeresponse))

- `RmiIndexedFrameResponse()`
- `XYZWPRPosition Frame { get; set; }`: Frame data.
- `byte Index { get; set; }`: Index (UFRAME or UTOOL number).
- Inherited from [RmiResponseBase](../api/UnderAutomation.Fanuc.Rmi.Data.md#rmiresponsebase): `ErrorId`, `ErrorText`

**RmiDigitalInputValueResponse** ([reference](../api/UnderAutomation.Fanuc.Rmi.Data.md#rmidigitalinputvalueresponse))

- `RmiDigitalInputValueResponse()`
- `short PortNumber { get; set; }`: Port number.
- `RmiOnOff PortValue { get; set; }`: Port value
- Inherited from [RmiResponseBase](../api/UnderAutomation.Fanuc.Rmi.Data.md#rmiresponsebase): `ErrorId`, `ErrorText`

**RmiIoPortValueResponse** ([reference](../api/UnderAutomation.Fanuc.Rmi.Data.md#rmiioportvalueresponse))

- `RmiIoPortValueResponse()`
- `int PortNumber { get; set; }`: Port number.
- `RmiIoPortType PortType { get; set; }`: Port type (DI, DO, AI, AO, GO, etc.).
- `double Value { get; set; }`: Current port value.
- Inherited from [RmiResponseBase](../api/UnderAutomation.Fanuc.Rmi.Data.md#rmiresponsebase): `ErrorId`, `ErrorText`

**RmiCartesianPositionResponse** ([reference](../api/UnderAutomation.Fanuc.Rmi.Data.md#rmicartesianpositionresponse))

- `RmiCartesianPositionResponse()`
- `CartesianPositionWithUserFrame Position { get; set; }`: Current TCP position including configuration and active frame/tool numbers.
- Inherited from [RmiTimedResponse](../api/UnderAutomation.Fanuc.Rmi.Data.md#rmitimedresponse): `TimeTag`
- Inherited from [RmiResponseBase](../api/UnderAutomation.Fanuc.Rmi.Data.md#rmiresponsebase): `ErrorId`, `ErrorText`

**RmiJointAnglesSampleResponse** ([reference](../api/UnderAutomation.Fanuc.Rmi.Data.md#rmijointanglessampleresponse))

- `RmiJointAnglesSampleResponse()`
- `JointsPosition JointAngle { get; set; }`: Joint angle set in degrees.
- Inherited from [RmiTimedResponse](../api/UnderAutomation.Fanuc.Rmi.Data.md#rmitimedresponse): `TimeTag`
- Inherited from [RmiResponseBase](../api/UnderAutomation.Fanuc.Rmi.Data.md#rmiresponsebase): `ErrorId`, `ErrorText`

**RmiPositionRegisterDataResponse** ([reference](../api/UnderAutomation.Fanuc.Rmi.Data.md#rmipositionregisterdataresponse))

- `RmiPositionRegisterDataResponse()`
- `CartesianPositionWithUserFrame CartesianPosition { get; set; }`: Position register value.
- `short RegisterNumber { get; set; }`: Register number
- Inherited from [RmiResponseBase](../api/UnderAutomation.Fanuc.Rmi.Data.md#rmiresponsebase): `ErrorId`, `ErrorText`

**RmiNumericRegisterValueResponse** ([reference](../api/UnderAutomation.Fanuc.Rmi.Data.md#rminumericregistervalueresponse))

- `RmiNumericRegisterValueResponse()`
- `int RegisterNumber { get; set; }`: Register number.
- `NumericRegister Value { get; set; }`: Register value.
- Inherited from [RmiResponseBase](../api/UnderAutomation.Fanuc.Rmi.Data.md#rmiresponsebase): `ErrorId`, `ErrorText`

**RmiVariableValueResponse** ([reference](../api/UnderAutomation.Fanuc.Rmi.Data.md#rmivariablevalueresponse))

- `RmiVariableValueResponse()`
- `int IntegerValue { get; set; }`: Gets or sets the value as an integer. Internally stored as a double.
- `bool IsInteger { get; set; }`: Whether the variable holds a floating-point value.
- `string Name { get; set; }`: Variable name, including the leading $ character.
- `double RealValue { get; set; }`: Gets or sets the value as a double-precision floating-point number.
- Inherited from [RmiResponseBase](../api/UnderAutomation.Fanuc.Rmi.Data.md#rmiresponsebase): `ErrorId`, `ErrorText`

**RmiTcpSpeedResponse** ([reference](../api/UnderAutomation.Fanuc.Rmi.Data.md#rmitcpspeedresponse))

- `RmiTcpSpeedResponse()`
- `double Speed { get; set; }`: Current tool center point speed in mm/s.
- Inherited from [RmiTimedResponse](../api/UnderAutomation.Fanuc.Rmi.Data.md#rmitimedresponse): `TimeTag`
- Inherited from [RmiResponseBase](../api/UnderAutomation.Fanuc.Rmi.Data.md#rmiresponsebase): `ErrorId`, `ErrorText`

**RmiSetPayloadParameters** ([reference](../api/UnderAutomation.Fanuc.Rmi.Data.md#rmisetpayloadparameters))

- `RmiSetPayloadParameters()`
- `float CgXm { get; set; }`: Center-of-gravity X offset in meters.
- `float CgYm { get; set; }`: Center-of-gravity Y offset in meters.
- `float CgZm { get; set; }`: Center-of-gravity Z offset in meters.
- `byte? Group { get; set; }`: Optional motion group number. null uses the active group.
- `float? InertiaXkgm2 { get; set; }`: Inertia around the X axis in kg·m². null omits this field from the command.
- `float? InertiaYkgm2 { get; set; }`: Inertia around the Y axis in kg·m². null omits this field from the command.
- `float? InertiaZkgm2 { get; set; }`: Inertia around the Z axis in kg·m². null omits this field from the command.
- `float MassKg { get; set; }`: Payload mass in kilograms.
- `byte ScheduleNumber { get; set; }`: Payload schedule number to configure.

**RmiSetPayloadCompensationParameters** ([reference](../api/UnderAutomation.Fanuc.Rmi.Data.md#rmisetpayloadcompensationparameters))

- `RmiSetPayloadCompensationParameters()`
- `float CgXm { get; set; }`: Center-of-gravity X offset in meters.
- `float CgYm { get; set; }`: Center-of-gravity Y offset in meters.
- `float CgZm { get; set; }`: Center-of-gravity Z offset in meters.
- `byte? Group { get; set; }`: Optional motion group number. null uses the active group.
- `float InertiaXkgm2 { get; set; }`: Inertia around the X axis in kg·m².
- `float InertiaYkgm2 { get; set; }`: Inertia around the Y axis in kg·m².
- `float InertiaZkgm2 { get; set; }`: Inertia around the Z axis in kg·m².
- `float MassKg { get; set; }`: Payload mass in kilograms.
- `byte ScheduleNumber { get; set; }`: Payload schedule number to configure.

**RmiRecordedCartesianPosition** ([reference](../api/UnderAutomation.Fanuc.Rmi.Data.md#rmirecordedcartesianposition))

- `RmiRecordedCartesianPosition()`
- `CartesianPositionWithUserFrame Position { get; set; }`: Recorded Cartesian position including arm configuration and active frame/tool numbers.
- `ushort PositionId { get; set; }`: Position identifier assigned by the controller.

**RmiRecordedJointPosition** ([reference](../api/UnderAutomation.Fanuc.Rmi.Data.md#rmirecordedjointposition))

- `RmiRecordedJointPosition()`
- `JointsPosition Joints { get; set; }`: Recorded joint angles in degrees.
- `ushort PositionId { get; set; }`: Position identifier assigned by the controller.
