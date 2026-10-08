# UnderAutomation agent skills

This repository contains the agent skills of the [UnderAutomation](https://underautomation.com) robot SDKs, for AI coding agents such as Claude Code, Codex, GitHub Copilot and Cursor. A skill gives the agent the documentation, the API reference and the code examples of one SDK in one language (C# or Python), at the version of the SDK.

With the skill, the agent can answer questions such as "why do I get this exception?" or "what is the difference between SNPX and CGTP?", and write code such as "write an app that reads the position registers".

## Plugins

| Plugin | Skill | SDK | Package |
| --- | --- | --- | --- |
| `abb-csharp` | `underautomation-abb-csharp` | [ABB SDK](https://underautomation.com/abb) for C# and .NET | NuGet `UnderAutomation.ABB` |
| `abb-python` | `underautomation-abb-python` | [ABB SDK](https://underautomation.com/abb) for Python | pip `UnderAutomation.ABB` |
| `fanuc-csharp` | `underautomation-fanuc-csharp` | [Fanuc SDK](https://underautomation.com/fanuc) for C# and .NET | NuGet `UnderAutomation.Fanuc` |
| `fanuc-python` | `underautomation-fanuc-python` | [Fanuc SDK](https://underautomation.com/fanuc) for Python | pip `UnderAutomation.Fanuc` |
| `staubli-csharp` | `underautomation-staubli-csharp` | [Staubli SDK](https://underautomation.com/staubli) for C# and .NET | NuGet `UnderAutomation.Staubli` |
| `staubli-python` | `underautomation-staubli-python` | [Staubli SDK](https://underautomation.com/staubli) for Python | pip `UnderAutomation.Staubli` |
| `universal-robots-csharp` | `underautomation-universal-robots-csharp` | [Universal Robots SDK](https://underautomation.com/universal-robots) for C# and .NET | NuGet `UnderAutomation.UniversalRobots` |
| `universal-robots-python` | `underautomation-universal-robots-python` | [Universal Robots SDK](https://underautomation.com/universal-robots) for Python | pip `UnderAutomation.UniversalRobots` |
| `yaskawa-csharp` | `underautomation-yaskawa-csharp` | [Yaskawa SDK](https://underautomation.com/yaskawa) for C# and .NET | NuGet `UnderAutomation.Yaskawa` |
| `yaskawa-python` | `underautomation-yaskawa-python` | [Yaskawa SDK](https://underautomation.com/yaskawa) for Python | pip `UnderAutomation.Yaskawa` |

The version of a plugin is the version of the SDK it documents. Install the skill of the language of your project only: the .NET API uses PascalCase and the Python API uses snake_case.

## Installation

Replace `fanuc-csharp` with the plugin of your SDK and language.

### Claude Code

```bash
claude plugin marketplace add underautomation/skills
claude plugin install fanuc-csharp@underautomation
```

Inside a Claude Code session, the same commands are `/plugin marketplace add underautomation/skills` and `/plugin install fanuc-csharp@underautomation`. Add `--scope project` to `claude plugin install` to share the plugin with the other developers of the project.

### Codex

```bash
codex plugin marketplace add underautomation/skills
```

Then open Codex, run `/plugins`, select the UnderAutomation marketplace and install `fanuc-csharp`.

### Other agents (npx skills)

With Node.js installed, [skills](https://github.com/vercel-labs/skills) installs the skill for GitHub Copilot, Cursor, Gemini CLI, OpenCode and about 70 other agents:

```bash
npx skills add underautomation/skills --skill underautomation-fanuc-csharp
```

Add `-y` to skip the questions, `-a <agent>` to choose the agent and `-g` to install for the user instead of the project.

### Manual installation

Download the zip of the skill from the latest release, for example [underautomation-fanuc-csharp.zip](https://github.com/underautomation/skills/releases/latest/download/underautomation-fanuc-csharp.zip), and extract it into the skills folder of your agent. The zip contains the folder `underautomation-fanuc-csharp/`.

| Agent | Project folder | User folder |
| --- | --- | --- |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| Codex | `.agents/skills/` | `~/.agents/skills/` |
| GitHub Copilot | `.agents/skills/` | `~/.copilot/skills/` or `~/.agents/skills/` |
| Cursor | `.agents/skills/` | `~/.cursor/skills/` or `~/.agents/skills/` |

A project folder is relative to the root of the project. On Windows, `~` is `%USERPROFILE%`.

The URL `https://github.com/underautomation/skills/releases/latest/download/<skill>.zip` always gives the last version. Each release also contains `<plugin>-plugin.zip`, the complete plugin folder.

## Check the version

The frontmatter of `SKILL.md` gives the SDK version that the skill documents (`metadata.sdk-version`). Compare it with the package of your project:

- C#: `dotnet list package`
- Python: `pip show UnderAutomation.<Brand>`, for example `pip show UnderAutomation.Fanuc`

When the versions differ, update the plugin (`claude plugin update fanuc-csharp@underautomation`, `npx skills update`) or download the zip again. The agent also does this check before it writes code.

## Content of a skill

```
underautomation-fanuc-csharp/
  SKILL.md                  when to use the skill, protocol choice, connection, license, motion safety, rules
  references/pages/         one file per page of the documentation, with the code of the language
  references/api/           every public type and member of the SDK, one line each
  references/errors.md      exceptions of the SDK and what to check
```

The skills are generated from the documentation of [underautomation.com](https://underautomation.com) at each release of an SDK. Do not change the files of `plugins/` by hand: report a problem in the [issues](https://github.com/underautomation/skills/issues) and it will be fixed in the documentation.

## Repository layout

```
.claude-plugin/marketplace.json     Claude Code marketplace, also read by npx skills
.agents/plugins/marketplace.json    Codex marketplace
plugins/<plugin>/
  .claude-plugin/plugin.json        Claude Code manifest
  .codex-plugin/plugin.json         Codex manifest, same name and version
  skills/<skill>/SKILL.md
.github/workflows/ci.yml            validation, zips and release at each push to main
```

To publish a new plugin, copy its folder into `plugins/` and add one entry to each `marketplace.json`, with the same values as the other entries. The CI checks that the two marketplaces list the same plugins and that the two manifests of a plugin have the same name and version.

## License

The content of this repository (the skills, their text and their code examples) is under the [MIT license](LICENSE).

The SDKs themselves are commercial products with their own license agreement, for example [underautomation.com/fanuc/eula](https://underautomation.com/fanuc/eula). Installing a skill does not give a license of the SDK. Each SDK has a 30-day trial that starts at the first use. Prices and license keys: [underautomation.com](https://underautomation.com).

## Support

- Documentation: [underautomation.com](https://underautomation.com)
- Contact: [underautomation.com/contact](https://underautomation.com/contact)
