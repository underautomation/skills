# Get started with .NET

Add the ABB SDK to a C# or VB.NET project from NuGet or as a DLL, and write a first program for an IRC5 or OmniCore controller. One managed DLL, no dependency, .NET Framework 3.5 to .NET 10.

Web page: https://underautomation.com/abb/documentation/get-started-net

This page shows how to add the ABB SDK to a C#, VB.NET or F# project and write a first program for an IRC5 or OmniCore controller. The SDK is one fully managed DLL, `UnderAutomation.ABB.dll`, with no dependency, that talks to the Robot Web Services (RWS) of the controller.

## Supported frameworks

The DLL is compiled in `AnyCPU` for these targets:

| Family         | Versions                                                               |
| -------------- | ---------------------------------------------------------------------- |
| .NET Framework | 3.5, 4.0, 4.5, 4.5.1, 4.5.2, 4.6, 4.6.1, 4.6.2, 4.7, 4.7.1, 4.7.2, 4.8 |
| .NET Standard  | 2.0, 2.1                                                               |
| .NET Core      | 3.0                                                                    |
| .NET           | 5.0, 6.0, 8.0, 9.0, 10.0                                               |

.NET and .NET Core run on Windows, Linux and macOS, on x64, x86, ARM and ARM64. For [Mono](https://www.mono-project.com) or [Universal Windows Platform](https://en.wikipedia.org/wiki/Universal_Windows_Platform) (UWP), use .NET Standard 2.1. For the [Unity](https://unity.com) engine, use a .NET Framework or a .NET Standard version.

The asynchronous methods are the only part that is not available everywhere: .NET Framework 3.5 and 4.0 have no `async` / `await`, so they only get the synchronous API. Everything else is the same on every target.

## Install from NuGet

NuGet picks the right DLL for your project and makes updates easy.

```bash
dotnet add package UnderAutomation.ABB
```

With the Package Manager console of Visual Studio:

```bash
Install-Package UnderAutomation.ABB
```

Or right click the `Dependencies` node of your project, select `Manage NuGet Packages...`, search for `UnderAutomation.ABB` and install the latest version.

Package page: [nuget.org/packages/UnderAutomation.ABB](https://www.nuget.org/packages/UnderAutomation.ABB)

## Or download the DLL

The [latest release](https://github.com/underautomation/ABB.NET/releases/latest) of the GitHub repository [ABB.NET](https://github.com/underautomation/ABB.NET) contains:

- [UnderAutomation.ABB.zip](https://github.com/underautomation/ABB.NET/releases/latest/download/UnderAutomation.ABB.zip): the DLL and its XML documentation, in one folder per target (`net48`, `netstandard2.0`, `net8.0`...). Reference the DLL of your target in your project.
- [UnderAutomation.ABB.Showcase.Forms.exe](https://github.com/underautomation/ABB.NET/releases/latest/download/UnderAutomation.ABB.Showcase.Forms.exe): the demo application for Windows. See [Demo application](demo-app.md).

On Windows, a downloaded file can be blocked. Before you extract the zip, right click it, open `Properties`, check `Unblock` and click `OK`. A blocked DLL can fail to load.

## Use the SDK with an AI agent

An AI agent such as Claude Code, Codex, GitHub Copilot or Cursor can write your C# code with the SDK. Without help, it does not know which protocol to use, which controller option is needed, or the exact names of the API, so it can invent members that do not exist. The UnderAutomation skill gives it the documentation of this version of the SDK: protocols, controller settings, API in C#, errors and safety rules for robot motion.

With the skill installed, you can ask for example:

> What do I need on my OmniCore controller to write a RAPID variable from my application?

> Write a program that reads the robot position and the digital inputs of my ABB robot.

Install the skill in your project:

```bash
npx skills add underautomation/skills --skill underautomation-abb-csharp
```

With Claude Code, you can also install it as a plugin:

```bash
claude plugin marketplace add underautomation/skills
claude plugin install abb-csharp@underautomation
```

Or paste this prompt to your agent: "Install the UnderAutomation ABB skill: follow https://underautomation.com/abb/documentation/ai-skills.md". The other installation modes are in [AI agent skills](https://underautomation.com/abb/documentation/ai-skills).

## First program

Import the namespace `UnderAutomation.ABB`, create an `AbbController`, connect and call a service.

```csharp
using UnderAutomation.ABB;

public class GetStartedNet
{
    static void Main()
    {
        // Without a key, the SDK runs in its 30 day trial period.
        // With a license, register it once, before the first connection.
        AbbController.RegisterLicense("YourCompanyName", "YOUR_LICENSE_KEY");

        // The whole SDK is reachable from a single object
        AbbController robot = new AbbController();
        robot.Connect("192.168.0.1");

        // Controller identity
        var identity = robot.Rws.Controller.GetIdentity();
        Console.WriteLine($"Connected to {identity.Name}");

        // RAPID tasks
        foreach (var task in robot.Rws.Rapid.GetTasks())
        {
            Console.WriteLine($"{task.Name} : {task.ExecutionState}");
        }

        robot.Disconnect();
    }
}
```

The SDK runs for 30 days without a key. After that, `RegisterLicense` is needed: see [Licensing](license.md).

The default parameters target an OmniCore controller over HTTP, with the default user of the controller. For an IRC5 with RobotWare 6, HTTPS or another user, see [Connect to your robot](connect.md).

## Demo application

The demo application is a Windows program that calls every service of the SDK, without writing code. It is a single executable, with no installation. Its C# sources are in the folder [UnderAutomation.ABB.Showcase.Forms](https://github.com/underautomation/ABB.NET/tree/main/UnderAutomation.ABB.Showcase.Forms) of `ABB.NET`. See [Demo application](demo-app.md).

## Shell sources

The folder [UnderAutomation.Abb.ObfuscatedSources](https://github.com/underautomation/ABB.NET/tree/main/UnderAutomation.Abb.ObfuscatedSources) of `ABB.NET` contains every public type and member of the SDK, with its XML documentation. The bodies of the methods are replaced by "Source is hidden". Use it to:

- browse the API and its documentation on GitHub, without installing anything;
- jump to a definition from your code editor, with the same names and signatures as the DLL;
- see the structure of the code that the source license delivers.

## Source license

The Standard and Pro licenses deliver the obfuscated DLL. The Source license delivers the full C# code of the library and its Visual Studio solution. You can change it and build it yourself, within the limits of the [license agreement](https://underautomation.com/abb/eula). See the licenses on the [pricing page](https://underautomation.com/order) and [Licensing](license.md).

## What to read next

- [Connect to your robot](connect.md): connection parameters, IRC5 and OmniCore, errors, asynchronous API.
- [Test with a RobotStudio virtual controller](virtual-controller.md): work without a real robot.
- [AI agent skills](https://underautomation.com/abb/documentation/ai-skills): install the C# skill of the SDK in Claude Code, Codex, GitHub Copilot or Cursor.
- [Robot Web Services overview](rws.md): the services of the SDK, one page per topic.
- [API reference](https://github.com/underautomation/ABB.NET/tree/main/UnderAutomation.Abb.ObfuscatedSources): the shell sources.
