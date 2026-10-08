# Develop without a robot

MotoSim EG-VRC does not simulate the network of the controller. What you need to test the SDK, and how to organize your code when the robot is not available.

Web page: https://underautomation.com/yaskawa/documentation/simulator

This page explains what you need to test the Yaskawa SDK, and how to work when the robot is not available. The SDK talks to the High Speed Ethernet Server, the Ethernet Server, the web server and the FTP server of a Motoman controller: it needs controller hardware, a simulator is not enough. The [offline kinematics](kinematics.md) are the exception: they run on the PC, without a controller.

## MotoSim EG-VRC

MotoSim EG-VRC is the offline programming and simulation software of Yaskawa. Its virtual controller runs the controller software on a PC, to teach jobs, check the reach and measure cycle times.

MotoSim does not simulate the network of the controller. Its virtual controller does not answer the High Speed Ethernet Server, so the SDK cannot connect to it. MotoSim itself uses the High Speed Ethernet Server of a real controller for its online functions, as a client, like the SDK.

## What you need

One of these, with the High Speed Ethernet Server enabled:

- **A real controller with its robot**, the one of your cell or another one.
- **A debug controller**: a controller on a test bench, without the arm or with a small robot. Every function of the SDK that does not move the robot can be tested on it: status, alarms, variables, I/O, jobs, files, parameters. The motion needs the servo power and an arm.

Use the same controller generation as your cell (YRC1000, DX200...) and the same software version when you can: the answers of the controller depend on them.

## Work without the controller

When the controller is not available, keep the code that uses the SDK in one class of your application, and test the rest of the application with a fake of this class. For example:

- one interface with the calls your application needs (`ReadStatus()`, `ReadPosition()`, `StartJob(name)`...);
- one implementation that calls `robot.HighSpeedEServer`;
- one fake implementation that returns fixed values, for your unit tests and for the development of the user interface.

Then test the real implementation on the controller, with the [demo application](demo-app.md) to compare the values.

## Use MotoSim with the SDK

MotoSim and the SDK work on the same files. Teach and check a job in MotoSim, export it as a `.JBI` file, then send it to the controller with the SDK, and start it. See [Transfer files and backups](how-to-transfer-files.md) and [Run a job](how-to-run-program.md).

## What to read next

- [Connect to your robot](connect.md): the settings of the controller and the connection parameters.
- [Demo application](demo-app.md): try the SDK on a controller without writing code.
- [Move the robot from a PC](how-to-move-robot.md): test the motion at low speed first.
