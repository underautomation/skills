# UnderAutomation UR (C#)

Write C# code for Universal Robots cobots with the UnderAutomation Universal Robots SDK. Agent skill for Claude Code, Codex, GitHub Copilot, Cursor and the other agents that read `SKILL.md` files.

## What the skill gives to the agent

- The documentation of the Universal Robots SDK 9.4.0: 27 pages, with the C# code samples.
- The protocol to choose for a task, and the controller option or setting it needs.
- Every public type and member of the SDK, with its C# signature, so that the agent does not invent members.
- The exceptions of the SDK and what to check when they are thrown.
- Safety rules for the code that moves a robot.

## Example prompts

- Should I use RTDE or the Primary Interface to read the TCP position of my UR cobot?
- Write a program that powers on my UR robot, releases the brakes and plays a program.
- Why do I get a ConnectException when I connect to my UR cobot?

## Requirements

The SDK itself: `dotnet add package UnderAutomation.UniversalRobots` ([NuGet](https://www.nuget.org/packages/UnderAutomation.UniversalRobots)).
The SDK is a commercial product with a 30 day trial: see https://underautomation.com/universal-robots.

## Installation

Claude Code:

```bash
claude plugin marketplace add underautomation/skills
claude plugin install universal-robots-csharp@underautomation
```

Codex: `codex plugin marketplace add underautomation/skills`, then `/plugins` in Codex.

Other agents:

```bash
npx skills add underautomation/skills --skill underautomation-universal-robots-csharp
```

## What the skill runs and reads

The plugin contains Markdown files, two JSON manifests and one icon. It has no script, no hook, no MCP server and no command. The skill tells the agent to:

- run `dotnet list package` in the folder of the project, to compare the version of the installed SDK with the version of the skill. When the package is missing, the agent asks the user before it runs `dotnet add package UnderAutomation.UniversalRobots`, which downloads the package from nuget.org;
- read the XML documentation of the installed NuGet package in `~/.nuget/packages` when a member seems missing from the skill;
- write C# code that connects to the robot controller of the user. The agent runs this code only when the user asks for it. A generated program that moves the robot does not move by default: it prints what it will do, then asks for a typed confirmation or needs an option such as `--run`.

## Privacy

The skill reads, stores and sends no personal data. It has no telemetry and never contacts UnderAutomation. Privacy policy of UnderAutomation: https://underautomation.com/legal#privacy_policy

## Troubleshooting

- The agent does not use the skill: name the SDK in the prompt, for example "with the UnderAutomation Universal Robots SDK". In Claude Code, `claude plugin list` shows the installed plugins.
- The version of the skill is not the version of the installed SDK: update the plugin (`claude plugin update universal-robots-csharp@underautomation`, `npx skills update`), or install version 9.4.0 of the SDK.
- The agent writes a member that does not exist: check the two versions above, then report the problem in the issues of the repository.

## Support

- Documentation: https://underautomation.com/universal-robots/documentation
- Questions on the SDK and on the skill: https://underautomation.com/contact
- Problems with the content of the skill: https://github.com/underautomation/skills/issues

## License

Skill version: 9.4.0, the version of the SDK it documents. The skill is under the MIT license of the repository https://github.com/underautomation/skills. The SDK is under its own license agreement: https://underautomation.com/universal-robots/eula

## Trademarks

Universal Robots, PolyScope, URScript, URCap and e-Series are trademarks or registered trademarks of Universal Robots A/S or its affiliates. Other product names, company names and brands in this documentation belong to their owners. They are used only to say which equipment the SDK communicates with.

UnderAutomation is an independent software publisher. It is not affiliated with, endorsed by or sponsored by Universal Robots A/S or its affiliates. This SDK is not a Universal Robots product. Universal Robots does not certify, review or support it. UnderAutomation provides the support of the SDK.
