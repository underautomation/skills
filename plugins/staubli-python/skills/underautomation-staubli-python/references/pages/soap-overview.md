# SOAP overview

The SOAP server of CS8 and CS9 controllers, what the SDK does with it, the units, and the list of topics: robots, position, kinematics, motion, I/O, applications and tasks.

Web page: https://underautomation.com/staubli/documentation/soap-overview

This page gives an overview of the SOAP interface of Staubli CS8 and CS9 controllers, and of what the SDK does with it. Each topic has its own page, listed below.

## What is the SOAP server

Staubli controllers run a SOAP server: a web service that external programs call over TCP/IP. Staubli Robotics Suite uses it to talk to the controller. The SDK uses the same server, so nothing is installed on the controller and no VAL 3 program has to run for the SDK to work.

The SDK sends the requests, reads the answers and gives you .NET objects. You do not have to write SOAP messages. One API covers CS8 and CS9 controllers.

```python
from underautomation.staubli.staubli_controller import StaubliController

controller = StaubliController()
controller.connect("192.168.0.254")

# Controller and robots
robots = controller.soap.get_robots()

# Position of the first robot
position = controller.soap.get_current_cartesian_joint_position(0)

# Inputs and outputs
ios = controller.soap.get_all_physical_ios()

# VAL 3 applications and tasks
applications = controller.soap.get_val_applications()
tasks = controller.soap.get_tasks()

controller.disconnect()
```

## Topics

| Page                                                            | What you can do                                                                         |
| --------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| [Controller and robots](soap-controller.md) | List the robots, read the controller parameters, the DH parameters and the joint ranges |
| [Position](soap-position.md)                | Read the joints and the Cartesian position, with a tool and a frame                     |
| [Kinematics](soap-kinematics.md)            | Compute the forward and inverse kinematics on the controller                            |
| [Motion](soap-motion.md)                    | Power the arm, send joint, linear and circular moves, stop and restart                  |
| [Inputs and outputs](soap-io.md)            | List, read and write the physical I/O                                                   |
| [VAL 3 applications](soap-applications.md)  | Load, start, stop and unload VAL 3 applications                                         |
| [VAL 3 tasks](soap-tasks.md)                | List the tasks and their state, suspend, resume and kill them                           |

All these functions are methods of `controller.Soap` (`controller.soap` in Python), after [the connection](connect.md).

## Units

| Value                               | Unit    |
| ----------------------------------- | ------- |
| Joint positions and joint ranges    | radians |
| Cartesian X, Y, Z and frame origins | meters  |
| Cartesian Rx, Ry, Rz                | radians |

Convert in your code if your application works in millimeters and degrees. The examples of this documentation do it where they print values.

## The robot argument

A controller can drive more than one arm. The methods that concern an arm take a `robot` argument: `0` is the first robot returned by `GetRobots()`. With one arm, pass `0`.

## Requests and timing

Each method call is one request to the controller, and waits for its answer. The time of a call depends on the network and on the load of the controller: measure it on your cell before you choose a polling period. Several values that are read together, like the joints and the Cartesian position, are cheaper in one call (`GetCurrentCartesianJointPosition`) than in two.

## What to read next

- [Connect to your robot](connect.md): parameters and errors.
- [How-to articles](how-to-get-position.md): complete programs for the frequent tasks.
