# UnderAutomation ABB (C#)

Write C# code for ABB robots with the UnderAutomation ABB SDK. Agent skill for Claude Code, Codex, GitHub Copilot, Cursor and the other agents that read `SKILL.md` files.

## What the skill gives to the agent

- The documentation of the ABB SDK 1.1.0: 25 pages, with the C# code samples.
- The protocol to choose for a task, and the controller option or setting it needs.
- Every public type and member of the SDK, with its C# signature, so that the agent does not invent members.
- The exceptions of the SDK and what to check when they are thrown.
- Safety rules for the code that moves a robot.

## Example prompts

- What do I need on my OmniCore controller to write a RAPID variable from my application?
- Write a program that reads the robot position and the digital inputs of my ABB robot.
- Why do I get an RwsException with HTTP 403 when I write a RAPID variable?

## Requirements

The SDK itself: `dotnet add package UnderAutomation.ABB` ([NuGet](https://www.nuget.org/packages/UnderAutomation.ABB)).
The SDK is a commercial product with a 30 day trial: see https://underautomation.com/abb.

## Installation

Claude Code:

```bash
claude plugin marketplace add underautomation/skills
claude plugin install abb-csharp@underautomation
```

Codex: `codex plugin marketplace add underautomation/skills`, then `/plugins` in Codex.

Other agents:

```bash
npx skills add underautomation/skills --skill underautomation-abb-csharp
```

## What the skill runs and reads

The plugin contains Markdown files, two JSON manifests and one icon. It has no script, no hook, no MCP server and no command. The skill tells the agent to:

- run `dotnet list package` in the folder of the project, to compare the version of the installed SDK with the version of the skill. When the package is missing, the agent asks the user before it runs `dotnet add package UnderAutomation.ABB`, which downloads the package from nuget.org;
- read the XML documentation of the installed NuGet package in `~/.nuget/packages` when a member seems missing from the skill;
- write C# code that connects to the robot controller of the user. The agent runs this code only when the user asks for it. A generated program that moves the robot does not move by default: it prints what it will do, then asks for a typed confirmation or needs an option such as `--run`.

## Privacy

The skill reads, stores and sends no personal data. It has no telemetry and never contacts UnderAutomation. Privacy policy of UnderAutomation: https://underautomation.com/legal#privacy_policy

## Troubleshooting

- The agent does not use the skill: name the SDK in the prompt, for example "with the UnderAutomation ABB SDK". In Claude Code, `claude plugin list` shows the installed plugins.
- The version of the skill is not the version of the installed SDK: update the plugin (`claude plugin update abb-csharp@underautomation`, `npx skills update`), or install version 1.1.0 of the SDK.
- The agent writes a member that does not exist: check the two versions above, then report the problem in the issues of the repository.

## Support

- Documentation: https://underautomation.com/abb/documentation
- Questions on the SDK and on the skill: https://underautomation.com/contact
- Problems with the content of the skill: https://github.com/underautomation/skills/issues

## License

Skill version: 1.1.0, the version of the SDK it documents. The skill is under the MIT license of the repository https://github.com/underautomation/skills. The SDK is under its own license agreement: https://underautomation.com/abb/eula

## Trademarks

ABB, IRC5, OmniCore, RobotWare, RAPID and RobotStudio are trademarks or registered trademarks of ABB Ltd. or its affiliates. Other product names, company names and brands in this documentation belong to their owners. They are used only to say which equipment the SDK communicates with.

UnderAutomation is an independent software publisher. It is not affiliated with, endorsed by or sponsored by ABB Ltd. or its affiliates. This SDK is not an ABB product. ABB does not certify, review or support it. UnderAutomation provides the support of the SDK.
