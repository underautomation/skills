# Move robot remotely

Move a Fanuc robot from an external application using RMI motion commands, Stream Motion real-time streaming, or DPM with SNPX.

Web page: https://underautomation.com/fanuc/documentation/move-robot-remotely

Move a Fanuc robot remotely using the SDK. There are several approaches depending on your application requirements.

## RMI : TP-like motion commands

RMI (Remote Motion Interface) sends motion instructions similar to a TP program. Best for pick-and-place, welding paths, and multi-waypoint trajectories.

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

**Requirements**: R912 (Remote Motion Interface) robot option.

See also: [RMI Motion commands](rmi-motion.md)

## Stream Motion : Real-time streaming (J519)

Stream Motion gives the position of the robot at every communication cycle (2 to 8 ms). The SDK plans smooth trajectories within the limits of the robot and sends them in real time. Best for computed paths, sensor guided motion and teleoperation.

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common;
using UnderAutomation.Fanuc.Motion;
using UnderAutomation.Fanuc.StreamMotion;
using UnderAutomation.Fanuc.StreamMotion.Data;
using UnderAutomation.Robotics.Motion;

public class MoveRobotRemotelyStreamMotion
{
    static void Main()
    {
        var robot = new FanucRobot();
        var parameters = new ConnectionParameters("192.168.0.1");
        parameters.StreamMotion.Enable = true;
        robot.Connect(parameters);
        var sm = robot.StreamMotion;

        // A TP program with IBGN start[1] / IBGN end[1] must run on the robot
        sm.StartMonitoring();

        var planner = new MotionPlanner(sm.JointLimits, null);
        JointsPosition start = sm.QueueEndJointPosition;
        var target = new JointsPosition(start.Values) { J1 = start.J1 + 20, J2 = start.J2 - 10 };

        // Smooth trajectory within the velocity, acceleration and jerk limits of the robot
        sm.Enqueue(planner.CreateJointPath(FanucMotion.ToJointValues(start))
            .MoveJoint(FanucMotion.ToJointValues(target), 30, FanucMotion.Cnt(100))
            .MoveJoint(FanucMotion.ToJointValues(start), 30, FanucMotion.Fine())
            .Build());

        sm.Finish(60000);

        robot.Disconnect();
    }
}
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
