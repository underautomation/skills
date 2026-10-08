# Try the SDK with the demo application

A Windows application, one executable and open source, that calls every function of the SDK. Test what your Yaskawa controller answers before you write any code.

Web page: https://underautomation.com/yaskawa/documentation/demo-app

The demo application lets you try the whole Yaskawa SDK on your Motoman controller, before you write any code. It is a Windows desktop application that exposes the functions of the SDK with buttons and fields, and shows what the controller answers.

## Download

**[Download UnderAutomation.Yaskawa.Showcase.Forms.exe](https://github.com/underautomation/Yaskawa.NET/releases/latest/download/UnderAutomation.Yaskawa.Showcase.Forms.exe)**

There is no installer. The application is one self contained executable, built with .NET 8 for Windows: it runs on a PC without .NET. Copy it where you want, run it, delete it when you are done.

Windows can block a file downloaded from the internet. Right click the file, open `Properties`, check `Unblock` and click `OK`.

The application runs in the 30 day trial of the SDK. The `License` page registers a key.

## What it does

The tree on the left has one page per topic. It connects to a real controller: MotoSim EG-VRC does not answer the High Speed Ethernet Server (see [Develop without a robot](simulator.md)).

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

| Page in the application | What you can try                                                                  | Documentation                                                           |
| ----------------------- | --------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| Connection              | Address of the controller, connect                                                | [Connect to your robot](connect.md)                 |
| Job                     | List the jobs, select one at a line, servo on and off, start, read the call stack | [Jobs](hses-jobs.md)                                |
| Alarms and system info  | The active alarms, reset, the software version and the operating times            | [Alarms](hses-alarms.md)                            |
| Files                   | List, download, upload, edit and delete files, CMOS backup                        | [Files and backup](hses-files.md)                   |
| Teach Pendant           | Show a message on the pendant, lock and unlock it                                 | [Status and servo](hses-status.md)                  |
| Status                  | Mode, cycle, servo, hold and alarm flags                                          | [Status and servo](hses-status.md)                  |
| Variables               | Read and write B, M, I, D, R, S and P variables                                   | [Variables and registers](hses-variables.md)        |
| Inputs / Outputs        | Read the I/O groups of each type, write the network inputs                        | [Inputs and outputs](hses-io.md)                    |
| System Parameters       | Read a system parameter by type, number and group                                 | [System information and parameters](hses-system.md) |
| Current position        | Cartesian position, joint pulses, position error and torque                       | [Positions](hses-positions.md)                      |
| Move robot              | Cartesian and joint moves, with the frame, the speed, the tool and the posture    | [Motion](hses-motion.md)                            |
| License                 | Register a license key, read the state of the trial                               | [Licensing](license.md)                             |

Start with the Connection page: the other pages stay disabled until a connection is open.

The `Move robot` page moves the arm. Try it with low speeds, in a cell with its safety functions active.

## Read its source

The application is open source: [github.com/underautomation/Yaskawa.NET](https://github.com/underautomation/Yaskawa.NET), folder `UnderAutomation.Yaskawa.Showcase.Forms`.

It is a Windows Forms project for .NET 8. It references the same `UnderAutomation.Yaskawa` DLL as your project: there is nothing specific to the demo in the way it calls the SDK. Each page of the application is one C# user control in the `Components` folder. Copy the calls you need into your code.

## What to read next

- [Connect to your robot](connect.md): the settings of the controller and the connection parameters, in code.
- [High Speed Ethernet Server overview](high-speed-ethernet-server.md): what each topic covers.
- [Licensing](license.md): the 30 day trial and the license key.
