# Test with a RobotStudio virtual controller

Run the SDK without a real robot. Create a virtual controller in ABB RobotStudio and enable Robot Web Services on it.

Web page: https://underautomation.com/abb/documentation/virtual-controller

You do not need a real robot to develop with this SDK. ABB RobotStudio runs a virtual controller on your PC, and that virtual controller answers Robot Web Services exactly like a cabinet on the network. The whole SDK works against it.

RobotStudio is published by ABB and runs on Windows. Download it from the ABB website. The basic license is enough to run a virtual controller.

## Create a virtual controller

The steps have kept the same shape across RobotStudio versions:

1. Install RobotStudio, then install the RobotWare version you want to work with. RobotWare is downloaded separately, from the RobotStudio installation manager.
2. Create a station and add a robot to it. RobotStudio then creates a system for that robot, or asks you to pick an existing one.
3. Start the virtual controller. RobotStudio lists it, with its state, in the controller view.

Two points decide how your code connects:

- The RobotWare version. RobotWare 6 gives an IRC5 virtual controller, RobotWare 7 and later give an OmniCore one.
- The system has to include the options your code uses. A bare system has no Collision Detection and no Safety Module, and the matching requests are then refused with an error naming the missing option.

## Connect to it

A virtual controller runs on the PC that runs RobotStudio, so it answers on `127.0.0.1`. Everything else is the same as with a real controller.

| Virtual controller | RobotWare   | RWS version | `RwsVersion` value |
| ------------------ | ----------- | ----------- | ------------------ |
| IRC5               | 6           | RWS 1.0     | `Irc5_V1_0`        |
| OmniCore           | 7 and later | RWS 2.0     | `OmniCore_V2_0`    |

```csharp
using UnderAutomation.ABB;
using UnderAutomation.ABB.Rws;

public class VirtualController
{
    static void Main()
    {
        // A virtual controller runs on the PC that runs RobotStudio, so it answers on 127.0.0.1.
        // A RobotWare 7 virtual controller speaks RWS 2.0 over HTTPS, like an OmniCore.
        ConnectionParameters parameters = new ConnectionParameters("127.0.0.1");
        parameters.Rws.Version = RwsVersion.OmniCore_V2_0;
        parameters.Rws.UseHttps = true;
        parameters.Rws.Username = "Default User";
        parameters.Rws.Password = "robotics";

        AbbController robot = new AbbController();
        robot.Connect(parameters);

        Console.WriteLine(robot.Rws.System.GetInfo().Version);

        // A RobotWare 6 virtual controller speaks RWS 1.0 over HTTP, like an IRC5
        ConnectionParameters irc5 = new ConnectionParameters("127.0.0.1");
        irc5.Rws.Version = RwsVersion.Irc5_V1_0;
        irc5.Rws.UseHttps = false;

        AbbController virtualIrc5 = new AbbController();
        virtualIrc5.Connect(irc5);

        // GetLicense answers VIRTUAL_USE on a virtual controller, which is one way
        // to tell a simulated system from a real one.
        Console.WriteLine(robot.Rws.System.GetLicense());

        robot.Disconnect();
        virtualIrc5.Disconnect();
    }
}
```

The default user account is `Default User` with the password `robotics`, like on a real controller.

HTTP versus HTTPS is independent of the RobotWare version here too. A virtual controller answers on whichever one it is configured for in RobotStudio, set `UseHttps` to match. When it answers on HTTPS with a self-signed certificate, the SDK accepts it, nothing has to be added to the certificate store of Windows.

A RobotWare 6 virtual controller and a RobotWare 7 one can run at the same time, as long as they are not both listening on the same port. Both are then reachable on `127.0.0.1`.

If the connection fails, check first that the virtual controller is started in RobotStudio, then that the RWS version of your connection parameters matches its RobotWare generation. A wrong version usually fails with the HTTP status code 404 on the first request. See [Connect to your robot](connect.md) for the full list of parameters.

## What a virtual controller does not do

A virtual controller simulates the robot software, not the hardware. Several resources are not implemented and answer with an error whatever you send them:

- The time zone, the time server, the list of installed systems and the RobotWare compatibility.
- Writing the clock and writing the identity of the controller.
- The network interfaces, on an OmniCore virtual controller.
- The device commands and the firmware upgrade information of the I/O system.

The SDK turns those answers into an `RwsException` explaining that the resource needs a real controller.

Two other differences are worth knowing:

- `robot.Rws.System.GetLicense()` returns `VIRTUAL_USE`. This is a simple way to tell a simulated system from a real one.
- No I/O signal of a bare virtual controller grants write access, so every signal write is refused with the HTTP status code 403. Signals become writable once the system is built with a real I/O configuration.

On the other hand, a virtual controller accepts one thing a real one refuses: `robot.Rws.MotionSystem.SetMechanicalUnitPosition` places the simulated robot at the joint values you give, without moving through the positions in between. See [Motion system, position and kinematics](rws-motion.md).

## Operation mode and motors

Most write operations depend on the state of the controller. A virtual controller has the same states as a real one, and RobotStudio gives you a virtual control panel and a virtual FlexPendant to change them.

- Jogging, and everything that moves the robot, needs the manual mode with the motors on.
- Many RAPID writes are refused in manual mode, whatever mastership is held. Switch to automatic mode for those.
- Every write needs the [mastership](rws-mastership.md) of the matching domain.

Your code reads and changes what it can with [the control panel service](rws-panel.md), and sets the mode selector from RobotStudio for the rest.

## Session limit

A controller accepts a limited number of simultaneous sessions, around 70 on OmniCore, and a virtual one is no different. An application that connects in a loop without calling `Disconnect` exhausts them, and every following request then answers with the HTTP status code 503. Restarting the virtual controller clears them.
