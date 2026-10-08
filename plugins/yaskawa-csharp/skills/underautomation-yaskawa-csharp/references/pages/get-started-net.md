# Get started with .NET

Add the Yaskawa SDK to a C# or VB.NET project from NuGet or as a DLL, and write a first program for a Yaskawa Motoman controller. One managed DLL, .NET Framework 3.5 to .NET 10.

Web page: https://underautomation.com/yaskawa/documentation/get-started-net

This page shows how to add the Yaskawa SDK to a C#, VB.NET or F# project and write a first program for a Yaskawa Motoman controller. The SDK is one fully managed DLL, `UnderAutomation.Yaskawa.dll`, that talks to the High Speed Ethernet Server of the controller over UDP, and to its Ethernet Server, web server and FTP server. It also computes the kinematics of the robot offline.

## Supported frameworks

The DLL is compiled in `AnyCPU` for these targets:

| Family         | Versions                                                               |
| -------------- | ---------------------------------------------------------------------- |
| .NET Framework | 3.5, 4.0, 4.5, 4.5.1, 4.5.2, 4.6, 4.6.1, 4.6.2, 4.7, 4.7.1, 4.7.2, 4.8 |
| .NET Standard  | 2.0, 2.1                                                               |
| .NET Core      | 3.0                                                                    |
| .NET           | 5.0, 6.0, 8.0, 9.0, 10.0                                               |

.NET and .NET Core run on Windows, Linux and macOS, on x64, x86, ARM and ARM64. For [Mono](https://www.mono-project.com) or [Universal Windows Platform](https://en.wikipedia.org/wiki/Universal_Windows_Platform) (UWP), use .NET Standard 2.1. For the [Unity](https://unity.com) engine, use a .NET Framework or a .NET Standard version.

The only dependency is [System.Text.Encoding.CodePages](https://www.nuget.org/packages/System.Text.Encoding.CodePages), for the .NET Standard 2.0 DLL. NuGet installs it. The other targets have no dependency. The same API is available on every target.

Supported controllers: YRC1000 (micro), MOTOMAN NEXT, DX100 / DX200, FS100, ERC / XRC / MRC.

## Install from NuGet

NuGet picks the right DLL for your project and makes updates easy.

```bash
dotnet add package UnderAutomation.Yaskawa
```

With the Package Manager console of Visual Studio:

```bash
Install-Package UnderAutomation.Yaskawa
```

Or right click the `Dependencies` node of your project, select `Manage NuGet Packages...`, search for `UnderAutomation.Yaskawa` and install the latest version.

Package page: [nuget.org/packages/UnderAutomation.Yaskawa](https://www.nuget.org/packages/UnderAutomation.Yaskawa)

## Or download the DLL

The [latest release](https://github.com/underautomation/Yaskawa.NET/releases/latest) of the GitHub repository [Yaskawa.NET](https://github.com/underautomation/Yaskawa.NET) contains:

- [UnderAutomation.Yaskawa.zip](https://github.com/underautomation/Yaskawa.NET/releases/latest/download/UnderAutomation.Yaskawa.zip): the DLL and its XML documentation, in one folder per target (`net48`, `netstandard2.0`, `net8.0`...). Reference the DLL of your target in your project.
- [UnderAutomation.Yaskawa.Showcase.Forms.exe](https://github.com/underautomation/Yaskawa.NET/releases/latest/download/UnderAutomation.Yaskawa.Showcase.Forms.exe): the demo application for Windows. See [Demo application](demo-app.md).

On Windows, a downloaded file can be blocked. Before you extract the zip, right click it, open `Properties`, check `Unblock` and click `OK`. A blocked DLL can fail to load.

## Use the SDK with an AI agent

An AI agent such as Claude Code, Codex, GitHub Copilot or Cursor can write your C# code with the SDK. Without help, it does not know which protocol to use, which controller option is needed, or the exact names of the API, so it can invent members that do not exist. The UnderAutomation skill gives it the documentation of this version of the SDK: protocols, controller settings, API in C#, errors and safety rules for robot motion.

With the skill installed, you can ask for example:

> Should I use the High Speed Ethernet Server or the Ethernet Server for my YRC1000?

> Write a program that reads the I variables 0 to 9 and the robot position.

Install the skill in your project:

```bash
npx skills add underautomation/skills --skill underautomation-yaskawa-csharp
```

With Claude Code, you can also install it as a plugin:

```bash
claude plugin marketplace add underautomation/skills
claude plugin install yaskawa-csharp@underautomation
```

Or paste this prompt to your agent: "Install the UnderAutomation Yaskawa skill: follow https://underautomation.com/yaskawa/documentation/ai-skills.md". The other installation modes are in [AI agent skills](https://underautomation.com/yaskawa/documentation/ai-skills).

## First program

Import the namespace `UnderAutomation.Yaskawa`, create a `YaskawaRobot`, connect and read a value.

```csharp
using UnderAutomation.Yaskawa;
using UnderAutomation.Yaskawa.HighSpeedEServer;

public class GetStartedNet
{
    static void Main()
    {
        // Without a key, the SDK runs in its 30 day trial period.
        // With a license, register it once, before the first connection.
        YaskawaRobot.RegisterLicense("YourCompanyName", "YOUR_LICENSE_KEY");

        // The whole SDK is reachable from a single object
        var robot = new YaskawaRobot();
        robot.Connect("192.168.0.1");

        // Read the position of the tool center point, in mm and degrees
        RobotPositionCartesianData position = robot.HighSpeedEServer.GetRobotCartesianPosition();
        Console.WriteLine($"X={position.X} Y={position.Y} Z={position.Z} Rx={position.Rx} Ry={position.Ry} Rz={position.Rz}");

        robot.Disconnect();
    }
}
```

The SDK runs for 30 days without a key. After that, `RegisterLicense` is needed: see [Licensing](license.md).

`Connect` uses the default settings of the High Speed Ethernet Server: UDP ports 10040 and 10041. The controller must accept remote commands for the methods that change its state (servo, jobs, motion, file write). See [Connect to your robot](connect.md).

## Demo application

The demo application is a Windows program that calls every function of the SDK, without writing code. It is a single executable, with no installation. Its C# sources are in the folder [UnderAutomation.Yaskawa.Showcase.Forms](https://github.com/underautomation/Yaskawa.NET/tree/main/UnderAutomation.Yaskawa.Showcase.Forms) of `Yaskawa.NET`. See [Demo application](demo-app.md).

## Shell sources

The folder [UnderAutomation.Yaskawa.ObfuscatedSources](https://github.com/underautomation/Yaskawa.NET/tree/main/UnderAutomation.Yaskawa.ObfuscatedSources) of `Yaskawa.NET` contains every public type and member of the SDK, with its XML documentation. The bodies of the methods are replaced by "Source is hidden". Use it to:

- browse the API and its documentation on GitHub, without installing anything;
- jump to a definition from your code editor, with the same names and signatures as the DLL;
- see the structure of the code that the source license delivers.

## Source license

The Standard and Pro licenses deliver the obfuscated DLL. The Source license delivers the full C# code of the library and its Visual Studio solution. You can change it and build it yourself, within the limits of the [license agreement](https://underautomation.com/yaskawa/eula). See the licenses on the [pricing page](https://underautomation.com/order) and [Licensing](license.md).

## What to read next

- [Connect to your robot](connect.md): the settings of the controller, the connection parameters, the errors.
- [Develop without a robot](simulator.md): what you need to test your application.
- [High Speed Ethernet Server overview](high-speed-ethernet-server.md): the functions of the SDK, one page per topic.
- [Choose a protocol](protocols.md): the Ethernet Server, HTTP and FTP, and when to use them.
- [Offline kinematics](kinematics.md): forward and inverse kinematics of 169 robot models, without a controller.
- [API reference](https://github.com/underautomation/Yaskawa.NET/tree/main/UnderAutomation.Yaskawa.ObfuscatedSources): the shell sources.
- [AI agent skills](https://underautomation.com/yaskawa/documentation/ai-skills): install the C# skill of the SDK in Claude Code, Codex, GitHub Copilot or Cursor.
