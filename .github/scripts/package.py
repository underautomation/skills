"""Checks the plugins of this repository and writes the release zips.

Usage: python .github/scripts/package.py [--out dist]

For each folder of plugins/:
- the Claude Code and Codex manifests exist and have the same name and version,
- the name is the folder name,
- each skill folder has a SKILL.md whose name is the folder name and whose
  metadata.sdk-version is the plugin version,
- the Codex manifest has the fields that Codex requires.
The two marketplace files must list the same plugins, and each listed plugin
must exist.

Output in --out: <skill>.zip (the skill folder at the root of the zip),
<plugin>-plugin.zip (the content of the plugin folder at the root of the zip)
and release-notes.md.
"""

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PLUGINS = ROOT / "plugins"
CLAUDE_MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
CODEX_MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"

CODEX_REQUIRED = ["name", "version", "description", "author", "skills", "interface"]
CODEX_INTERFACE_REQUIRED = [
    "displayName",
    "shortDescription",
    "longDescription",
    "developerName",
    "category",
    "capabilities",
    "composerIcon",
    "logo",
]

errors = []
warnings = []


def error(message):
    errors.append(message)
    print(f"::error::{message}")


def warning(message):
    warnings.append(message)
    print(f"::warning::{message}")


def load_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        error(f"{path.relative_to(ROOT).as_posix()}: missing")
    except json.JSONDecodeError as e:
        error(f"{path.relative_to(ROOT).as_posix()}: invalid JSON ({e})")
    return None


def read_frontmatter(skill_md):
    text = skill_md.read_text(encoding="utf-8")
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.DOTALL)
    if not match:
        return None
    block = match.group(1)
    name = re.search(r"^name:\s*['\"]?([^'\"\r\n]+?)['\"]?\s*$", block, re.MULTILINE)
    version = re.search(r"^\s+sdk-version:\s*['\"]?([^'\"\r\n]+?)['\"]?\s*$", block, re.MULTILINE)
    return {
        "name": name.group(1) if name else None,
        "sdk-version": version.group(1) if version else None,
    }


def marketplace_paths(data, codex):
    result = {}
    for entry in (data or {}).get("plugins", []):
        source = entry.get("source")
        if codex and isinstance(source, dict):
            source = source.get("path")
        result[entry.get("name")] = source
    return result


def check_relative_file(plugin_dir, value, label):
    if not isinstance(value, str) or not value.startswith("./"):
        error(f"{label}: '{value}' must be a path that starts with ./")
        return
    if not (plugin_dir / value).exists():
        error(f"{label}: '{value}' does not exist")


def check_plugin(plugin_dir):
    rel = plugin_dir.relative_to(ROOT).as_posix()
    claude = load_json(plugin_dir / ".claude-plugin" / "plugin.json")
    codex = load_json(plugin_dir / ".codex-plugin" / "plugin.json")
    if claude is None or codex is None:
        return None

    name = claude.get("name")
    version = claude.get("version")
    if codex.get("name") != name:
        error(f"{rel}: name differs between the manifests ('{name}' and '{codex.get('name')}')")
    if codex.get("version") != version:
        error(f"{rel}: version differs between the manifests ('{version}' and '{codex.get('version')}')")
    if name != plugin_dir.name:
        error(f"{rel}: the name '{name}' is not the folder name")
    if not version:
        error(f"{rel}: no version")

    for field in CODEX_REQUIRED:
        if field not in codex:
            error(f"{rel}/.codex-plugin/plugin.json: missing field '{field}'")
    if not (codex.get("author") or {}).get("name"):
        error(f"{rel}/.codex-plugin/plugin.json: missing field 'author.name'")
    interface = codex.get("interface") or {}
    for field in CODEX_INTERFACE_REQUIRED:
        if field not in interface:
            error(f"{rel}/.codex-plugin/plugin.json: missing field 'interface.{field}'")
    for field in ("composerIcon", "logo"):
        if field in interface:
            check_relative_file(plugin_dir, interface[field], f"{rel}/.codex-plugin/plugin.json interface.{field}")
    if "skills" in codex:
        check_relative_file(plugin_dir, codex["skills"], f"{rel}/.codex-plugin/plugin.json skills")
    for field in ("displayName", "shortDescription"):
        if len(interface.get(field, "")) > 30:
            warning(f"{rel}: interface.{field} has more than 30 characters (limit of the OpenAI directory)")
    prompts = interface.get("defaultPrompt", [])
    if isinstance(prompts, str):
        prompts = [prompts]
    if len(prompts) > 3 or any(len(p) > 128 for p in prompts):
        warning(f"{rel}: interface.defaultPrompt has more than 3 prompts or a prompt longer than 128 characters")

    skills_dir = plugin_dir / "skills"
    skills = sorted(p for p in skills_dir.iterdir() if p.is_dir()) if skills_dir.is_dir() else []
    if not skills:
        error(f"{rel}: no skill in skills/")
    for skill in skills:
        skill_md = skill / "SKILL.md"
        if not skill_md.is_file():
            error(f"{rel}/skills/{skill.name}: missing SKILL.md")
            continue
        front = read_frontmatter(skill_md)
        if front is None:
            error(f"{rel}/skills/{skill.name}/SKILL.md: no frontmatter")
            continue
        if front["name"] != skill.name:
            error(f"{rel}/skills/{skill.name}/SKILL.md: name '{front['name']}' is not the folder name")
        if front["sdk-version"] != version:
            error(f"{rel}/skills/{skill.name}/SKILL.md: sdk-version '{front['sdk-version']}' is not the plugin version '{version}'")

    return {"name": name, "version": version, "dir": plugin_dir, "skills": skills}


def zip_folder(zip_path, folder, prefix):
    # prefix: name of the root folder in the zip, or "" to put the content at the root.
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for path in sorted(folder.rglob("*")):
            if path.is_file():
                arcname = path.relative_to(folder).as_posix()
                if prefix:
                    arcname = f"{prefix}/{arcname}"
                z.write(path, arcname)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="dist")
    args = parser.parse_args()
    out = Path(args.out).resolve()

    plugin_dirs = sorted(p for p in PLUGINS.iterdir() if p.is_dir()) if PLUGINS.is_dir() else []
    plugins = [p for p in (check_plugin(d) for d in plugin_dirs) if p]

    claude_listed = marketplace_paths(load_json(CLAUDE_MARKETPLACE), codex=False)
    codex_listed = marketplace_paths(load_json(CODEX_MARKETPLACE), codex=True)
    if set(claude_listed) != set(codex_listed):
        error(
            "the two marketplaces do not list the same plugins: "
            f"Claude Code {sorted(claude_listed)}, Codex {sorted(codex_listed)}"
        )
    for listed, label in ((claude_listed, "Claude Code"), (codex_listed, "Codex")):
        for name, source in listed.items():
            if source != f"./plugins/{name}":
                error(f"{label} marketplace: plugin '{name}' must have the source ./plugins/{name}, not '{source}'")
            elif not (PLUGINS / name).is_dir():
                error(f"{label} marketplace: plugin '{name}' is listed but plugins/{name} does not exist")
    for plugin in plugins:
        if plugin["name"] not in claude_listed:
            warning(f"plugins/{plugin['name']} is not listed in the marketplaces: it is released as zip only")

    if errors:
        print(f"{len(errors)} error(s)")
        return 1

    out.mkdir(parents=True, exist_ok=True)
    lines = ["| Plugin | Version | Skill zip | Plugin zip |", "| --- | --- | --- | --- |"]
    for plugin in plugins:
        for skill in plugin["skills"]:
            zip_folder(out / f"{skill.name}.zip", skill, skill.name)
        plugin_zip = f"{plugin['name']}-plugin.zip"
        zip_folder(out / plugin_zip, plugin["dir"], "")
        skill_zips = ", ".join(f"`{s.name}.zip`" for s in plugin["skills"])
        lines.append(f"| `{plugin['name']}` | {plugin['version']} | {skill_zips} | `{plugin_zip}` |")
        print(f"{plugin['name']} {plugin['version']}: {len(plugin['skills'])} skill(s)")

    notes = [
        "Plugins of this release:",
        "",
        *lines,
        "",
        "Installation: see the [README](https://github.com/underautomation/skills#installation).",
        "",
    ]
    (out / "release-notes.md").write_text("\n".join(notes), encoding="utf-8")
    print(f"{len(plugins)} plugin(s), {len(warnings)} warning(s), output in {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
