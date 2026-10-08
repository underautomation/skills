# Motion commands

Send linear, joint, and circular motion commands with configurable speed, termination type, and acceleration via RMI.

Web page: https://underautomation.com/fanuc/documentation/rmi-motion

RMI lets you send TP-equivalent motion instructions to the robot. Each call to `SendTpInstruction()` returns an `RmiInstructionResponse` that tracks the instruction through its execution lifecycle.

## Linear motion

Move the robot in a straight line to a Cartesian target:

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common;
using UnderAutomation.Fanuc.Rmi.Data;
using UnderAutomation.Fanuc.Rmi.TpInstructions;

public class RmiMotionLinear
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");
        parameters.Rmi.Enable = true;
        robot.Connect(parameters);
        robot.Rmi.Initialize();

        // Linear motion to a Cartesian target (tool 1, frame 0)
        var move = new LinearMotionTpInstruction
        {
            SpeedType = RmiLinearSpeedType.MmSec,
            Speed = 100,
            TermType = RmiTerminationType.Fine,
            Target = new CartesianPositionWithUserFrame(500, 200, 300, 0, 90, 0, tool: 1, frame: 0)
        };
        robot.Rmi.SendTpInstruction(move).WaitForCompletion();

        // Incremental linear motion (delta from current position)
        var inc = new LinearRelativeTpInstruction
        {
            SpeedType = RmiLinearSpeedType.MmSec,
            Speed = 50,
            TermType = RmiTerminationType.Fine,
            Target = new CartesianPositionWithUserFrame(0, 0, -50, 0, 0, 0, 1, 0)
        };
        robot.Rmi.SendTpInstruction(inc).WaitForCompletion();

        // Linear motion with joint-angle target representation
        var jrep = new LinearMotionJRepTpInstruction
        {
            SpeedType = RmiLinearSpeedType.MmSec,
            Speed = 80,
            TermType = RmiTerminationType.Fine,
            Joints = new JointsPosition(10, -20, 30, 0, 60, 0)
        };
        robot.Rmi.SendTpInstruction(jrep).WaitForCompletion();

        // CNT blending: chain motions without stopping
        var p1 = new LinearMotionTpInstruction
        {
            SpeedType = RmiLinearSpeedType.MmSec,
            Speed = 200,
            TermType = RmiTerminationType.Cnt,
            TermValue = 100,
            Target = new CartesianPositionWithUserFrame(600, 0, 400, 0, 90, 0, 1, 0)
        };
        var p2 = new LinearMotionTpInstruction
        {
            SpeedType = RmiLinearSpeedType.MmSec,
            Speed = 200,
            TermType = RmiTerminationType.Fine,  // last motion must be Fine (or NoBlend = true)
            Target = new CartesianPositionWithUserFrame(700, 0, 350, 0, 90, 0, 1, 0)
        };
        robot.Rmi.SendTpInstruction(p1);
        robot.Rmi.SendTpInstruction(p2).WaitForCompletion();

        robot.Rmi.Abort();
        robot.Disconnect();
    }
}
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

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common;
using UnderAutomation.Fanuc.Rmi.Data;
using UnderAutomation.Fanuc.Rmi.TpInstructions;

public class RmiMotionJoint
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");
        parameters.Rmi.Enable = true;
        robot.Connect(parameters);
        robot.Rmi.Initialize();

        // Joint motion with Cartesian target, percent speed
        var cart = new JointMotionTpInstruction
        {
            SpeedType = RmiJointSpeedType.Percent,
            Speed = 10,
            TermType = RmiTerminationType.Fine,
            Target = new CartesianPositionWithUserFrame(500, 200, 300, 0, 90, 0, tool: 1, frame: 0)
        };
        robot.Rmi.SendTpInstruction(cart).WaitForCompletion();

        // Joint motion with joint-angle target representation
        var jrep = new JointMotionJRepTpInstruction
        {
            SpeedType = RmiJointSpeedType.Percent,
            Speed = 5,
            TermType = RmiTerminationType.Fine,
            Joints = new JointsPosition(10, -20, 30, 0, 60, 0)
        };
        robot.Rmi.SendTpInstruction(jrep).WaitForCompletion();

        // Incremental joint motion (joint-angle delta)
        var relJrep = new JointRelativeJRepTpInstruction
        {
            SpeedType = RmiJointSpeedType.Percent,
            Speed = 5,
            TermType = RmiTerminationType.Fine,
            Joints = new JointsPosition(0, 0, 0, 0, 5, 0)   // rotate J5 by 5 degrees
        };
        robot.Rmi.SendTpInstruction(relJrep).WaitForCompletion();

        robot.Rmi.Abort();
        robot.Disconnect();
    }
}
```

### Speed types for joint motion

| `RmiJointSpeedType` | Description |
|---------------------|-------------|
| `Percent` | Percentage of maximum joint speed (1-100). |
| `Time` | Duration in 0.1-second steps. |
| `MSec` | Duration in milliseconds. |

## Circular motion

Circular motion requires a **via point** and a **destination**:

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common;
using UnderAutomation.Fanuc.Rmi.Data;
using UnderAutomation.Fanuc.Rmi.TpInstructions;

public class RmiMotionCircular
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");
        parameters.Rmi.Enable = true;
        robot.Connect(parameters);
        robot.Rmi.Initialize();

        // Circular motion: define a via-point and a destination
        var arc = new CircularMotionTpInstruction
        {
            SpeedType = RmiLinearSpeedType.MmSec,
            Speed = 80,
            TermType = RmiTerminationType.Fine,
            Via = new CartesianPositionWithUserFrame(600, 100, 350, 0, 90, 0, tool: 1, frame: 0),
            Target = new CartesianPositionWithUserFrame(700, 0, 300, 0, 90, 0, tool: 1, frame: 0)
        };
        robot.Rmi.SendTpInstruction(arc).WaitForCompletion();

        // Incremental circular motion (via and target are deltas)
        var arcRel = new CircularRelativeTpInstruction
        {
            SpeedType = RmiLinearSpeedType.MmSec,
            Speed = 60,
            TermType = RmiTerminationType.Fine,
            Via = new CartesianPositionWithUserFrame(50, 50, 0, 0, 0, 0, 1, 0),
            Target = new CartesianPositionWithUserFrame(100, 0, 0, 0, 0, 0, 1, 0)
        };
        robot.Rmi.SendTpInstruction(arcRel).WaitForCompletion();

        robot.Rmi.Abort();
        robot.Disconnect();
    }
}
```

## Spline motion

Spline motion requires firmware **MajorVersion >= 7** (V9.40P/54 or later). The controller needs at least one more spline instruction after the first to start executing the segment.

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common;
using UnderAutomation.Fanuc.Rmi.Data;
using UnderAutomation.Fanuc.Rmi.TpInstructions;

public class RmiMotionSpline
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");
        parameters.Rmi.Enable = true;
        robot.Connect(parameters);
        robot.Rmi.Initialize();

        // Spline motion requires MajorVersion >= 7 (firmware V9.40P/54 or later).
        // The controller will not execute the first spline segment until it receives
        // a second instruction (motion or non-motion) after the last spline point.

        robot.Rmi.SendTpInstruction(new SplineMotionTpInstruction
        {
            SpeedType = RmiLinearSpeedType.MmSec,
            Speed = 200,
            TermType = RmiTerminationType.Cnt,
            TermValue = 100,
            Target = new CartesianPositionWithUserFrame(500, 100, 300, 0, 90, 0, 1, 0)
        });
        robot.Rmi.SendTpInstruction(new SplineMotionTpInstruction
        {
            SpeedType = RmiLinearSpeedType.MmSec,
            Speed = 200,
            TermType = RmiTerminationType.Cnt,
            TermValue = 100,
            Target = new CartesianPositionWithUserFrame(550, 200, 320, 0, 90, 0, 1, 0)
        });
        robot.Rmi.SendTpInstruction(new SplineMotionTpInstruction
        {
            SpeedType = RmiLinearSpeedType.MmSec,
            Speed = 200,
            TermType = RmiTerminationType.Fine,
            Target = new CartesianPositionWithUserFrame(600, 100, 300, 0, 90, 0, 1, 0)
        });

        // Send a non-spline instruction to flush the spline buffer and trigger execution
        robot.Rmi.SendTpInstruction(new WaitTimeTpInstruction { Seconds = 0.1 })
             .WaitForCompletion();

        // Spline with joint-angle representation
        robot.Rmi.SendTpInstruction(new SplineMotionJRepTpInstruction
        {
            SpeedType = RmiJointSpeedType.Percent,
            Speed = 50,
            TermType = RmiTerminationType.Cnt,
            TermValue = 100,
            Joints = new JointsPosition(10, -20, 30, 0, 60, 0)
        });
        robot.Rmi.SendTpInstruction(new SplineMotionJRepTpInstruction
        {
            SpeedType = RmiJointSpeedType.Percent,
            Speed = 50,
            TermType = RmiTerminationType.Fine,
            Joints = new JointsPosition(15, -15, 35, 5, 55, 5)
        });
        robot.Rmi.SendTpInstruction(new WaitTimeTpInstruction { Seconds = 0.1 })
             .WaitForCompletion();

        robot.Rmi.Abort();
        robot.Disconnect();
    }
}
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

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Rmi.Data;
using UnderAutomation.Fanuc.Rmi.TpInstructions;

public class RmiMotionNonMotion
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");
        parameters.Rmi.Enable = true;
        robot.Connect(parameters);
        robot.Rmi.Initialize();

        // Wait for digital input DI[1] to turn ON before continuing
        robot.Rmi.SendTpInstruction(new WaitDinTpInstruction
        {
            PortNumber = 1,
            Value = RmiOnOff.ON
        });

        // Wait 0.5 seconds
        robot.Rmi.SendTpInstruction(new WaitTimeTpInstruction { Seconds = 0.5 });

        // Switch to UFRAME 2 for the next motions
        robot.Rmi.SendTpInstruction(new SetUFrameTpInstruction { FrameNumber = 2 });

        // Switch to UTOOL 3
        robot.Rmi.SendTpInstruction(new SetUToolTpInstruction { ToolNumber = 3 });

        // Activate payload schedule 1
        robot.Rmi.SendTpInstruction(new SetPayloadTpInstruction { ScheduleNumber = 1 });

        // Call a TP program (requires MajorVersion >= 4)
        robot.Rmi.SendTpInstruction(new CallProgramTpInstruction { ProgramName = "GRIPPER_OPEN" })
             .WaitForCompletion();

        robot.Rmi.Abort();
        robot.Disconnect();
    }
}
```

## Tracking instruction status

```csharp
using System;
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common;
using UnderAutomation.Fanuc.Rmi.Data;
using UnderAutomation.Fanuc.Rmi.TpInstructions;

public class RmiMotionTracking
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");
        parameters.Rmi.Enable = true;
        robot.Connect(parameters);
        robot.Rmi.Initialize();

        // Send several instructions. Each returns immediately.
        for (int i = 0; i < 5; i++)
        {
            var instr = new LinearMotionTpInstruction
            {
                SpeedType = RmiLinearSpeedType.MmSec,
                Speed = 100,
                TermType = RmiTerminationType.Fine,
                Target = new CartesianPositionWithUserFrame(500 + i * 20, 200, 300, 0, 90, 0, 1, 0)
            };
            RmiInstructionResponse r = robot.Rmi.SendTpInstruction(instr);

            // Subscribe to status changes
            r.StatusChanged += status =>
                Console.WriteLine($"  Seq {r.SequenceId}: {status}");
        }

        // Wait for all instructions to complete
        foreach (RmiInstructionResponse r in robot.Rmi.Instructions)
            r.WaitForCompletion();

        // Print final results
        foreach (RmiInstructionResponse r in robot.Rmi.Instructions)
        {
            if (r.Status == RmiInstructionStatus.Error)
                Console.WriteLine($"  Seq {r.SequenceId} failed: {r.ErrorText}");
            else
                Console.WriteLine($"  Seq {r.SequenceId} completed OK");
        }

        // Remove completed instructions from the tracking list
        robot.Rmi.ClearCompletedInstructions();

        robot.Rmi.Abort();
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

public class RmiMotion
{
    static void Main()
    {
        FanucRobot robot = new FanucRobot();
        ConnectionParameters parameters = new ConnectionParameters("192.168.0.1");
        parameters.Rmi.Enable = true;
        robot.Connect(parameters);

        // Check status
        RmiControllerStatusResponse status = robot.Rmi.GetStatus();
        if (status.TPEnabled)
        {
            Console.WriteLine("Turn off the teach pendant before proceeding.");
            return;
        }
        if (!status.ServoReady)
        {
            Console.WriteLine("Servos are not ready.");
            return;
        }

        // Initialize RMI_MOVE
        robot.Rmi.Initialize();

        // Set speed override
        robot.Rmi.SetOverride(80);

        // Move to a start position
        robot.Rmi.SendTpInstruction(new JointMotionJRepTpInstruction
        {
            SpeedType = RmiJointSpeedType.Percent,
            Speed = 10,
            TermType = RmiTerminationType.Fine,
            Joints = new JointsPosition(0, 0, 0, 0, 0, 0)
        }).WaitForCompletion();

        // Approach
        robot.Rmi.SendTpInstruction(new LinearMotionTpInstruction
        {
            SpeedType = RmiLinearSpeedType.MmSec,
            Speed = 200,
            TermType = RmiTerminationType.Cnt,
            TermValue = 50,
            Target = new CartesianPositionWithUserFrame(500, 200, 350, 0, 90, 0, 1, 0)
        });

        // Descend to pick position
        robot.Rmi.SendTpInstruction(new LinearMotionTpInstruction
        {
            SpeedType = RmiLinearSpeedType.MmSec,
            Speed = 50,
            TermType = RmiTerminationType.Fine,
            Target = new CartesianPositionWithUserFrame(500, 200, 300, 0, 90, 0, 1, 0)
        }).WaitForCompletion();

        // Activate gripper
        robot.Rmi.SendTpInstruction(new CallProgramTpInstruction { ProgramName = "GRIP_ON" })
             .WaitForCompletion();

        // Retract
        robot.Rmi.SendTpInstruction(new LinearMotionTpInstruction
        {
            SpeedType = RmiLinearSpeedType.MmSec,
            Speed = 100,
            TermType = RmiTerminationType.Fine,
            Target = new CartesianPositionWithUserFrame(500, 200, 400, 0, 90, 0, 1, 0)
        }).WaitForCompletion();

        // Check HOLD state
        if (robot.Rmi.IsInHoldState)
        {
            Console.WriteLine("Controller in HOLD. Calling Reset...");
            robot.Rmi.Reset();
        }

        robot.Rmi.Abort();
        robot.Disconnect();
    }
}
```

## API reference

**LinearMotionTpInstruction** ([reference](../api/UnderAutomation.Fanuc.Rmi.TpInstructions.md#linearmotiontpinstruction))

- `LinearMotionTpInstruction()`
- `int? Alim { get; set; }`: Acceleration limit value. null uses the controller default. Requires MajorVersion &gt;= 5 and the R921 option.
- `short? AlimReg { get; set; }`: Acceleration limit register number. null disables register-based limit. Requires MajorVersion &gt;= 5 and the R921 option.
- `bool Mrot { get; set; }`: When true, enables coordinated motion (MROT).
- `bool NoBlend { get; set; }`: When true, disables blending with the next instruction. Requires MajorVersion &gt;= 5.
- `RmiLinearSpeedType SpeedType { get; set; }`: Speed unit (mm/s, inch/min, or time).
- `bool WristJoint { get; set; }`: When true, enables wrist-joint mode for this motion.
- Inherited from [CartesianMotionTpInstructionBase](../api/UnderAutomation.Fanuc.Rmi.TpInstructions.md#cartesianmotiontpinstructionbase): `Target`
- Inherited from [FullMotionTpInstructionBase](../api/UnderAutomation.Fanuc.Rmi.TpInstructions.md#fullmotiontpinstructionbase): `Acc`, `OffsetPrNumber`, `VisionPrNumber`, `LcbType`, `LcbValue`, `PortType`, `PortNumber`, `PortValue`, `ToolOffsetPrNumber`
- Inherited from [MotionTpInstructionBase](../api/UnderAutomation.Fanuc.Rmi.TpInstructions.md#motiontpinstructionbase): `Speed`, `TermType`, `TermValue`

**JointMotionTpInstruction** ([reference](../api/UnderAutomation.Fanuc.Rmi.TpInstructions.md#jointmotiontpinstruction))

- `JointMotionTpInstruction()`
- `bool Mrot { get; set; }`: When true, enables coordinated motion (MROT).
- `bool NoBlend { get; set; }`: When true, disables blending with the next instruction.
- `RmiJointSpeedType SpeedType { get; set; }`: Speed unit (percent override or time).
- Inherited from [CartesianMotionTpInstructionBase](../api/UnderAutomation.Fanuc.Rmi.TpInstructions.md#cartesianmotiontpinstructionbase): `Target`
- Inherited from [FullMotionTpInstructionBase](../api/UnderAutomation.Fanuc.Rmi.TpInstructions.md#fullmotiontpinstructionbase): `Acc`, `OffsetPrNumber`, `VisionPrNumber`, `LcbType`, `LcbValue`, `PortType`, `PortNumber`, `PortValue`, `ToolOffsetPrNumber`
- Inherited from [MotionTpInstructionBase](../api/UnderAutomation.Fanuc.Rmi.TpInstructions.md#motiontpinstructionbase): `Speed`, `TermType`, `TermValue`

**JointMotionJRepTpInstruction** ([reference](../api/UnderAutomation.Fanuc.Rmi.TpInstructions.md#jointmotionjreptpinstruction))

- `JointMotionJRepTpInstruction()`
- `bool Mrot { get; set; }`: When true, enables coordinated motion (MROT).
- `bool NoBlend { get; set; }`: When true, disables blending with the next instruction.
- `RmiJointSpeedType SpeedType { get; set; }`: Speed unit (percent override or time).
- Inherited from [JRepMotionTpInstructionBase](../api/UnderAutomation.Fanuc.Rmi.TpInstructions.md#jrepmotiontpinstructionbase): `Joints`
- Inherited from [FullMotionTpInstructionBase](../api/UnderAutomation.Fanuc.Rmi.TpInstructions.md#fullmotiontpinstructionbase): `Acc`, `OffsetPrNumber`, `VisionPrNumber`, `LcbType`, `LcbValue`, `PortType`, `PortNumber`, `PortValue`, `ToolOffsetPrNumber`
- Inherited from [MotionTpInstructionBase](../api/UnderAutomation.Fanuc.Rmi.TpInstructions.md#motiontpinstructionbase): `Speed`, `TermType`, `TermValue`

**CircularMotionTpInstruction** ([reference](../api/UnderAutomation.Fanuc.Rmi.TpInstructions.md#circularmotiontpinstruction))

- `CircularMotionTpInstruction()`
- `bool Mrot { get; set; }`: When true, enables coordinated motion (MROT).
- `bool NoBlend { get; set; }`: When true, disables blending with the next instruction.
- `RmiLinearSpeedType SpeedType { get; set; }`: Speed unit (mm/s, inch/min, or time).
- `CartesianPositionWithUserFrame Via { get; set; }`: Via-point Cartesian position that defines the arc.
- `bool WristJoint { get; set; }`: When true, enables wrist-joint mode for this motion.
- Inherited from [CartesianMotionTpInstructionBase](../api/UnderAutomation.Fanuc.Rmi.TpInstructions.md#cartesianmotiontpinstructionbase): `Target`
- Inherited from [FullMotionTpInstructionBase](../api/UnderAutomation.Fanuc.Rmi.TpInstructions.md#fullmotiontpinstructionbase): `Acc`, `OffsetPrNumber`, `VisionPrNumber`, `LcbType`, `LcbValue`, `PortType`, `PortNumber`, `PortValue`, `ToolOffsetPrNumber`
- Inherited from [MotionTpInstructionBase](../api/UnderAutomation.Fanuc.Rmi.TpInstructions.md#motiontpinstructionbase): `Speed`, `TermType`, `TermValue`

**SplineMotionTpInstruction** ([reference](../api/UnderAutomation.Fanuc.Rmi.TpInstructions.md#splinemotiontpinstruction))

- `SplineMotionTpInstruction()`
- `RmiLinearSpeedType SpeedType { get; set; }`: Speed unit (mm/s, inch/min, or time).
- Inherited from [CartesianMotionTpInstructionBase](../api/UnderAutomation.Fanuc.Rmi.TpInstructions.md#cartesianmotiontpinstructionbase): `Target`
- Inherited from [FullMotionTpInstructionBase](../api/UnderAutomation.Fanuc.Rmi.TpInstructions.md#fullmotiontpinstructionbase): `Acc`, `OffsetPrNumber`, `VisionPrNumber`, `LcbType`, `LcbValue`, `PortType`, `PortNumber`, `PortValue`, `ToolOffsetPrNumber`
- Inherited from [MotionTpInstructionBase](../api/UnderAutomation.Fanuc.Rmi.TpInstructions.md#motiontpinstructionbase): `Speed`, `TermType`, `TermValue`

**FullMotionTpInstructionBase** ([reference](../api/UnderAutomation.Fanuc.Rmi.TpInstructions.md#fullmotiontpinstructionbase))

- `byte? Acc { get; set; }`: Optional acceleration override (1-100 %). null uses the controller default.
- `string LcbType { get; set; }`: Lock-and-continue (LCB) condition type string. null disables LCB.
- `short? LcbValue { get; set; }`: Lock-and-continue (LCB) condition value. Required when FullMotionTpInstructionBase.LcbType is set.
- `short? OffsetPrNumber { get; set; }`: Offset position register number. null disables offset.
- `short? PortNumber { get; set; }`: Digital output port number. Required when FullMotionTpInstructionBase.PortType is set.
- `RmiPortType? PortType { get; set; }`: Digital output port type to trigger at the end of this motion. null disables output.
- `RmiOnOff? PortValue { get; set; }`: Digital output port value. Required when FullMotionTpInstructionBase.PortType is set.
- `short? ToolOffsetPrNumber { get; set; }`: Tool-offset position register number. null disables tool offset. Requires MajorVersion &gt;= 4.
- `short? VisionPrNumber { get; set; }`: Vision offset position register number. null disables vision offset.
- Inherited from [MotionTpInstructionBase](../api/UnderAutomation.Fanuc.Rmi.TpInstructions.md#motiontpinstructionbase): `Speed`, `TermType`, `TermValue`

**RmiInstructionResponse** ([reference](../api/UnderAutomation.Fanuc.Rmi.Data.md#rmiinstructionresponse))

- `RmiInstructionResponse()`
- `RmiInstructionBase Instruction { get; }`: Sent instruction
- `int SequenceId { get; }`: Sequence identifier assigned to this instruction. 0 until the instruction has been dispatched to the controller.
- `RmiInstructionStatus Status { get; }`: Current execution state of the instruction.
- `event Action<RmiInstructionStatus> StatusChanged`: Fired each time RmiInstructionResponse.Status changes. The argument is the new status value. This event may be raised from a background thread.
- `bool WaitForCompletion(int timeoutMs = -1)`: Blocks the calling thread until the instruction reaches a terminal state (RmiInstructionStatus.Completed or RmiInstructionStatus.Error), or until timeoutMs milliseconds have elapsed. Pass -1 (or omit) to wait indefinitely.
- Inherited from [RmiResponseBase](../api/UnderAutomation.Fanuc.Rmi.Data.md#rmiresponsebase): `ErrorId`, `ErrorText`
