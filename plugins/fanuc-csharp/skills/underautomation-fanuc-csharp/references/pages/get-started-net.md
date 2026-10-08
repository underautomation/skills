# Get started with .NET

Add the Fanuc SDK to a C# or VB.NET project from NuGet or as a DLL, and write a first program for a Fanuc controller or ROBOGUIDE. One managed DLL, .NET Framework 3.5 to .NET Standard 2.1.

Web page: https://underautomation.com/fanuc/documentation/get-started-net

This page shows how to add the Fanuc SDK to a C#, VB.NET or F# project and write a first program for a Fanuc controller (R-J3iB, R-30iA, R-30iB, R-30iB Plus, R-50iA) or a ROBOGUIDE virtual robot. The SDK is one fully managed DLL, `UnderAutomation.Fanuc.dll`, that talks to the controller over Telnet KCL, FTP, SNPX, CGTP, RMI and Stream Motion.

## Supported frameworks

### Targets of the DLL

The DLL is compiled in `AnyCPU` for these targets:

| Family         | Versions                                                               |
| -------------- | ---------------------------------------------------------------------- |
| .NET Framework | 3.5, 4.0, 4.5, 4.5.1, 4.5.2, 4.6, 4.6.1, 4.6.2, 4.7, 4.7.1, 4.7.2, 4.8 |
| .NET Standard  | 2.0, 2.1                                                               |

.NET Core 2.0 and later and .NET 5 to .NET 10 use the .NET Standard 2.0 or 2.1 DLL. They run on Windows, Linux and macOS, on x64, x86, ARM and ARM64. For [Mono](https://www.mono-project.com) or [Universal Windows Platform](https://en.wikipedia.org/wiki/Universal_Windows_Platform) (UWP), use .NET Standard 2.1. For the [Unity](https://unity.com) engine, use a .NET Framework or a .NET Standard version.

### Dependencies

The .NET Framework DLLs have no dependency. The .NET Standard DLLs depend on the NuGet package `System.Text.Encoding.CodePages`, which decodes the strings of Japanese (Shift-JIS) and Chinese (GB2312) controllers. NuGet installs it with the SDK.

## Install from NuGet

NuGet picks the right DLL for your project and makes updates easy.

```bash
dotnet add package UnderAutomation.Fanuc
```

With the Package Manager console of Visual Studio:

```bash
Install-Package UnderAutomation.Fanuc
```

Or right click the `Dependencies` node of your project, select `Manage NuGet Packages...`, search for `UnderAutomation.Fanuc` and install the latest version.

Package page: [nuget.org/packages/UnderAutomation.Fanuc](https://www.nuget.org/packages/UnderAutomation.Fanuc)

## Or download the DLL

The [latest release](https://github.com/underautomation/Fanuc.NET/releases/latest) of the GitHub repository [Fanuc.NET](https://github.com/underautomation/Fanuc.NET) contains:

- [UnderAutomation.Fanuc.zip](https://github.com/underautomation/Fanuc.NET/releases/latest/download/UnderAutomation.Fanuc.zip): the DLL and its XML documentation, in one folder per target (`net35`, `net48`, `netstandard2.0`...). Reference the DLL of your target in your project.
- [UnderAutomation.Fanuc.Showcase.Forms.exe](https://github.com/underautomation/Fanuc.NET/releases/latest/download/UnderAutomation.Fanuc.Showcase.Forms.exe): the demo application for Windows. See [Demo application](demo-app.md).

On Windows, a downloaded file can be blocked. Before you extract the zip, right click it, open `Properties`, check `Unblock` and click `OK`. A blocked DLL can fail to load.

With a .NET Standard DLL from the zip, also add the NuGet package `System.Text.Encoding.CodePages` to your project.

## Use the SDK with an AI agent

An AI agent such as Claude Code, Codex, GitHub Copilot or Cursor can write your C# code with the SDK. Without help, it does not know which protocol to use, which controller option is needed, or the exact names of the API, so it can invent members that do not exist. The UnderAutomation skill gives it the documentation of this version of the SDK: protocols, controller settings, API in C#, errors and safety rules for robot motion.

With the skill installed, you can ask for example:

> Which protocol should I use to read the position registers of my Fanuc robot?

> Write a program that reads R[1] to R[10] and prints them.

Install the skill in your project:

```bash
npx skills add underautomation/skills --skill underautomation-fanuc-csharp
```

With Claude Code, you can also install it as a plugin:

```bash
claude plugin marketplace add underautomation/skills
claude plugin install fanuc-csharp@underautomation
```

Or paste this prompt to your agent: "Install the UnderAutomation Fanuc skill: follow https://underautomation.com/fanuc/documentation/ai-skills.md". The other installation modes are in [AI agent skills](https://underautomation.com/fanuc/documentation/ai-skills).

## First program

### Connect and read a register

Import the namespace `UnderAutomation.Fanuc`, create a `FanucRobot`, connect and read a value.

```csharp
using UnderAutomation.Fanuc;
using UnderAutomation.Fanuc.Common;

public class GetStartedNet
{
    static void Main()
    {
        // Without a key, the SDK runs in its 30 day trial period.
        // With a license, register it once, before the first connection.
        FanucRobot.RegisterLicense("YourCompanyName", "YOUR_LICENSE_KEY");

        // With an IP address only, the SDK connects to the web server of the controller (CGTP)
        FanucRobot robot = new FanucRobot();
        robot.Connect("192.168.0.1");

        // Numeric register R[1]
        NumericRegisterWithComment r1 = robot.Cgtp.ReadNumericRegisterWithComment(1);
        Console.WriteLine($"R[1] = {r1}");

        // Current position of motion group 1
        CartesianPosition position = robot.Cgtp.ReadCartesianPosition();
        Console.WriteLine($"X={position.X}, Y={position.Y}, Z={position.Z}");

        robot.Disconnect();
    }
}
```

With an IP address only, `Connect` uses the web server of the controller (CGTP). It needs no option on the controller, and firmware V8.30 or later (V9.10 for the position). To use Telnet KCL, FTP, SNPX, RMI or Stream Motion, enable them in a `ConnectionParameters` object: see [Connect to your robot](connect.md).

### License

The SDK runs for 30 days without a key. After that, `RegisterLicense` is needed: see [Licensing](license.md). The offline features (kinematics, motion planner, file parsers) do not need a connection.

## Demo application

The demo application is a Windows program that calls the features of the SDK, without writing code: CGTP, SNPX, Telnet, FTP, RMI, Stream Motion, DPM, kinematics. It is a single executable, with no installation. Its C# sources are in the folder [UnderAutomation.Fanuc.Showcase.Forms](https://github.com/underautomation/Fanuc.NET/tree/main/UnderAutomation.Fanuc.Showcase.Forms) of `Fanuc.NET`. See [Demo application](demo-app.md).

## Shell sources

The folder [UnderAutomation.Fanuc.ObfuscatedSources](https://github.com/underautomation/Fanuc.NET/tree/main/UnderAutomation.Fanuc.ObfuscatedSources) of `Fanuc.NET` contains every public type and member of the SDK, with its XML documentation. The bodies of the methods are replaced by "Source is hidden". Use it to:

- browse the API and its documentation on GitHub, without installing anything;
- jump to a definition from your code editor, with the same names and signatures as the DLL;
- see the structure of the code that the source license delivers.

## Source license

The Standard and Pro licenses deliver the obfuscated DLL. The Source license delivers the full C# code of the library and its Visual Studio solution. You can change it and build it yourself, within the limits of the [license agreement](https://underautomation.com/fanuc/eula). See the licenses on the [pricing page](https://underautomation.com/order) and [Licensing](license.md).

## What to read next

- [Connect to your robot](connect.md): the protocols, their setup on the controller, the connection parameters.
- [Test with ROBOGUIDE](simulator.md): work without a real robot.
- [AI agent skills](https://underautomation.com/fanuc/documentation/ai-skills): install the C# skill of the SDK in Claude Code, Codex, GitHub Copilot or Cursor.
- The protocol pages: [CGTP](cgtp.md), [SNPX](snpx.md), [Telnet](telnet.md), [FTP](ftp.md), [RMI](rmi.md), [Stream Motion](stream-motion.md).
- [API reference](https://github.com/underautomation/Fanuc.NET/tree/main/UnderAutomation.Fanuc.ObfuscatedSources): the shell sources.
