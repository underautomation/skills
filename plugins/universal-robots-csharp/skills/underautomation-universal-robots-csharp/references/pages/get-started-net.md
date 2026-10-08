# Get started with .NET

Add the Universal Robots SDK to a C#, VB.NET or F# project from NuGet or from the zip, and write a first program. .NET Framework 3.5 to .NET 10, Windows, Linux and macOS.

Web page: https://underautomation.com/universal-robots/documentation/get-started-net

This page shows how to add the Universal Robots SDK to a C#, VB.NET or F# project and write a first program for a UR cobot. The SDK is one fully managed DLL, `UnderAutomation.UniversalRobots.dll`, that uses the standard interfaces of the robot: Primary Interface, RTDE, Dashboard Server, REST API, Interpreter Mode, XML-RPC, sockets, SSH and SFTP.

## Supported frameworks

The DLL is compiled in `AnyCPU` for these targets:

| Family         | Versions                                                               |
| -------------- | ---------------------------------------------------------------------- |
| .NET Framework | 3.5, 4.0, 4.5, 4.5.1, 4.5.2, 4.6, 4.6.1, 4.6.2, 4.7, 4.7.1, 4.7.2, 4.8 |
| .NET Standard  | 2.0, 2.1                                                               |
| .NET Core      | 3.0                                                                    |
| .NET           | 5.0, 6.0, 8.0, 9.0, 10.0                                               |

.NET and .NET Core run on Windows, Linux and macOS, on x64, x86, ARM and ARM64. For [Mono](https://www.mono-project.com) or [Universal Windows Platform](https://en.wikipedia.org/wiki/Universal_Windows_Platform) (UWP), use .NET Standard 2.1. For the [Unity](https://unity.com) engine, use a .NET Framework or a .NET Standard version, or the package of [UniversalRobots.Unity](https://github.com/underautomation/UniversalRobots.Unity).

The only dependency is [System.Text.Encoding.CodePages](https://www.nuget.org/packages/System.Text.Encoding.CodePages), for the .NET Standard 2.0 DLL. NuGet installs it. The other targets have no dependency. The same API is available on every target.

Supported robots: UR3, UR5, UR10 (CB-Series), UR3e, UR5e, UR7e, UR10e, UR12e, UR16e (e-Series), UR8 Long, UR15, UR18, UR20, UR30, with PolyScope or PolyScope X, and the URSim simulator.

## Install the SDK

### From NuGet

NuGet picks the right DLL for your project and makes updates easy.

```bash
dotnet add package UnderAutomation.UniversalRobots
```

With the Package Manager console of Visual Studio:

```bash
Install-Package UnderAutomation.UniversalRobots
```

Or right click the `Dependencies` node of your project, select `Manage NuGet Packages...`, search for `UnderAutomation.UniversalRobots` and install the latest version.

Package page: [nuget.org/packages/UnderAutomation.UniversalRobots](https://www.nuget.org/packages/UnderAutomation.UniversalRobots)

### Or download the DLL

The [latest release](https://github.com/underautomation/UniversalRobots.NET/releases/latest) of the GitHub repository [UniversalRobots.NET](https://github.com/underautomation/UniversalRobots.NET) contains:

- [UnderAutomation.UniversalRobots.zip](https://github.com/underautomation/UniversalRobots.NET/releases/latest/download/UnderAutomation.UniversalRobots.zip): the DLL and its XML documentation, in one folder per target (`net48`, `netstandard2.0`, `net8.0`...). Reference the DLL of your target in your project.
- [UnderAutomation.UniversalRobots.Showcase.Forms.exe](https://github.com/underautomation/UniversalRobots.NET/releases/latest/download/UnderAutomation.UniversalRobots.Showcase.Forms.exe): the demo application for Windows. See [Demo application](demo-app.md).
- The console demo for Windows, Linux and macOS: see [Try the SDK on Linux and macOS](#try_the_sdk_on_linux_and_macos) below.

On Windows, a downloaded file can be blocked. Before you extract the zip, right click it, open `Properties`, check `Unblock` and click `OK`. A blocked DLL can fail to load.

## Use the SDK with an AI agent

An AI agent such as Claude Code, Codex, GitHub Copilot or Cursor can write your C# code with the SDK. Without help, it does not know which protocol to use, which controller option is needed, or the exact names of the API, so it can invent members that do not exist. The UnderAutomation skill gives it the documentation of this version of the SDK: protocols, controller settings, API in C#, errors and safety rules for robot motion.

With the skill installed, you can ask for example:

> Should I use RTDE or the Primary Interface to read the TCP position of my UR cobot?

> Write a program that powers on my UR robot, releases the brakes and plays a program.

Install the skill in your project:

```bash
npx skills add underautomation/skills --skill underautomation-universal-robots-csharp
```

With Claude Code, you can also install it as a plugin:

```bash
claude plugin marketplace add underautomation/skills
claude plugin install universal-robots-csharp@underautomation
```

Or paste this prompt to your agent: "Install the UnderAutomation Universal Robots skill: follow https://underautomation.com/universal-robots/documentation/ai-skills.md". The other installation modes are in [AI agent skills](https://underautomation.com/universal-robots/documentation/ai-skills).

## First program

Import the namespace `UnderAutomation.UniversalRobots`, create a `UR`, connect and read a value.

```csharp
using UnderAutomation.UniversalRobots;

class GetStartedNet
{
  static void Main(string[] args)
  {
    // Only after the 30 day trial: register your license key
    // UR.RegisterLicense("YourCompanyName", "YOUR_LICENSE_KEY");

    var robot = new UR();

    // Connect with the default services: Primary Interface and Dashboard Server
    robot.Connect("192.168.0.1");

    // The Primary Interface receives the state of the robot at 10 Hz
    Thread.Sleep(500);

    // Cartesian position of the tool, in meters and radians
    var pose = robot.PrimaryInterface.CartesianInfo.AsPose();
    Console.WriteLine($"X={pose.X} Y={pose.Y} Z={pose.Z}");

    // Mode of the robot, read with the Dashboard Server
    var mode = robot.Dashboard.GetRobotMode();
    Console.WriteLine($"Robot mode: {mode.Value}");

    robot.Disconnect();
  }
}
```

The SDK runs for 30 days without a key. After that, `RegisterLicense` is needed: see [Licensing](license.md).

`Connect("192.168.0.1")` opens the Primary Interface and the Dashboard Server. The other interfaces are enabled with a `ConnectParameters`, and some must be enabled on the robot first: see [Connect to the robot](connect.md).

## Demo application

The demo application is a Windows program that calls every interface of the SDK, without writing code. It is a single executable, with no installation. Its C# sources are in the folder [UnderAutomation.UniversalRobots.Showcase.Forms](https://github.com/underautomation/UniversalRobots.NET/tree/main/UnderAutomation.UniversalRobots.Showcase.Forms) of `UniversalRobots.NET`, and a VB.NET version is in `UnderAutomation.UniversalRobots.Showcase.Forms.vb`. See [Demo application](demo-app.md).

## Try the SDK on Linux and macOS

A console demo, built for 6 platforms, connects to a robot and prints its data in a terminal. Each file is self contained: the .NET runtime is not needed.

| Platform    | File                                                                                                                                                                         |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Windows x64 | [UnderAutomation.UniversalRobots.Showcase.Console.win-x64.exe](https://github.com/underautomation/UniversalRobots.NET/releases/latest/download/UnderAutomation.UniversalRobots.Showcase.Console.win-x64.exe) |
| Windows x86 | [UnderAutomation.UniversalRobots.Showcase.Console.win-x86.exe](https://github.com/underautomation/UniversalRobots.NET/releases/latest/download/UnderAutomation.UniversalRobots.Showcase.Console.win-x86.exe) |
| Linux x64   | [UnderAutomation.UniversalRobots.Showcase.Console.linux-x64](https://github.com/underautomation/UniversalRobots.NET/releases/latest/download/UnderAutomation.UniversalRobots.Showcase.Console.linux-x64)     |
| Linux ARM   | [UnderAutomation.UniversalRobots.Showcase.Console.linux-arm](https://github.com/underautomation/UniversalRobots.NET/releases/latest/download/UnderAutomation.UniversalRobots.Showcase.Console.linux-arm)     |
| macOS x64   | [UnderAutomation.UniversalRobots.Showcase.Console.osx-x64](https://github.com/underautomation/UniversalRobots.NET/releases/latest/download/UnderAutomation.UniversalRobots.Showcase.Console.osx-x64)         |
| macOS ARM64 | [UnderAutomation.UniversalRobots.Showcase.Console.osx-arm64](https://github.com/underautomation/UniversalRobots.NET/releases/latest/download/UnderAutomation.UniversalRobots.Showcase.Console.osx-arm64)     |

On Linux and macOS, make the file executable before you run it:

```bash
chmod +x UnderAutomation.UniversalRobots.Showcase.Console.linux-x64
./UnderAutomation.UniversalRobots.Showcase.Console.linux-x64
```

Its sources are in the folder `UnderAutomation.UniversalRobots.Showcase.Console` of `UniversalRobots.NET`.

## Shell sources

The folder [UnderAutomation.UniversalRobots.ObfuscatedSources](https://github.com/underautomation/UniversalRobots.NET/tree/main/UnderAutomation.UniversalRobots.ObfuscatedSources) of `UniversalRobots.NET` contains every public type and member of the SDK, with its XML documentation. The bodies of the methods are replaced by "Source is hidden". Use it to:

- browse the API and its documentation on GitHub, without installing anything;
- jump to a definition from your code editor, with the same names and signatures as the DLL;
- see the structure of the code that the source license delivers.

## Source license

The Standard and Pro licenses deliver the obfuscated DLL. The Source license delivers the full C# code of the library and its Visual Studio solution. You can change it and build it yourself, within the limits of the [license agreement](https://underautomation.com/universal-robots/eula). See the licenses on the [pricing page](https://underautomation.com/order) and [Licensing](license.md).

## What to read next

- [Connect to the robot](connect.md): the settings of the robot, the connection parameters, the errors.
- [Develop without a robot](configure-offline-simulator.md): install URSim.
- [RTDE](rtde.md) and [Primary Interface](data-streaming.md): the data of the robot.
- [AI agent skills](https://underautomation.com/universal-robots/documentation/ai-skills): install the C# skill of the SDK in Claude Code, Codex, GitHub Copilot or Cursor.
- [API reference](https://github.com/underautomation/UniversalRobots.NET/tree/main/UnderAutomation.UniversalRobots.ObfuscatedSources): the shell sources.
