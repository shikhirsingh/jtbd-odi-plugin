#!/usr/bin/env bash
# fix-skills.sh — make jtbd-odi skills visible to Claude Code & Cowork
#
# Claude Code and Cowork scan ~/.claude/skills/, ~/.claude/commands/, and
# ~/.claude/agents/. Several cross-agent installers (notably `npx skills add`)
# instead write to ~/.agents/skills/, leaving the skills invisible to the
# canonical scanners. This script reconciles both layouts.
#
# Run it from the repo root after either:
#   - `git clone` + manual install, OR
#   - `npx skills add shikhirsingh/jtbd-odi-plugin -a claude-code`
#
# It is idempotent and uses symlinks, so updates flow through automatically.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_HOME="${CLAUDE_HOME:-$HOME/.claude}"
AGENTS_HOME="${AGENTS_HOME:-$HOME/.agents}"

link_tree() {
  local kind="$1"        # skills | commands | agents
  local src="$REPO_ROOT/$kind"
  [[ -d "$src" ]] || return 0

  for target_root in "$CLAUDE_HOME/$kind" "$AGENTS_HOME/$kind"; do
    mkdir -p "$target_root"
    if [[ "$kind" == "commands" ]]; then
      for f in "$src"/*.md; do
        [[ -e "$f" ]] || continue
        ln -sfn "$f" "$target_root/$(basename "$f")"
      done
    else
      for d in "$src"/*/; do
        [[ -d "$d" ]] || continue
        name="$(basename "$d")"
        ln -sfn "${d%/}" "$target_root/$name"
      done
    fi
  done
}

echo "→ Linking jtbd-odi into $CLAUDE_HOME and $AGENTS_HOME"
link_tree skills
link_tree commands
link_tree agents

skill_count=$(find "$REPO_ROOT/skills" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')
command_count=$(find "$REPO_ROOT/commands" -maxdepth 1 -name '*.md' 2>/dev/null | wc -l | tr -d ' ')
agent_count=$(find "$REPO_ROOT/agents" -maxdepth 1 -name '*.md' 2>/dev/null | wc -l | tr -d ' ')

echo "✓ Linked $skill_count skills, $command_count commands, $agent_count agents"
echo "  Claude Code / Cowork: $CLAUDE_HOME/skills"
echo "  npx skills add:       $AGENTS_HOME/skills"
echo
echo "Restart Claude Code (or run :rebuild), then try /odihelp"
