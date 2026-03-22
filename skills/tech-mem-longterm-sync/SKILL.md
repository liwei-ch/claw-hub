---
name: mem-longterm-sync
description: Sync long-term memories to MemOS/memos using a unified schema, and search them efficiently to save tokens while preserving context.
persona: tech
user-invocable: true
metadata: {
  "openclaw": {
    "emoji": "🧠",
    "os": ["win32", "darwin", "linux"],
    "requires": {
      "bins": ["python3"],
      "env": ["MEMOS_API_KEY", "MEMOS_USER_ID"]
    }
  }
}
---

# mem-longterm-sync Skill

This skill implements the "long-term memory" spec for MemOS/memos:

- Writes only **rules, decisions, milestones, lessons** to MemOS
- Uses a **structured JSON schema** for each memory
- Provides simple CLI-style entrypoints for:
  - adding long-term memories
  - searching long-term memories

See `design-docs/mem-longterm-spec.md` for the schema and conventions.

## Environment

Required env vars:

- `MEMOS_API_KEY` – API key for MemOS/memos
- `MEMOS_USER_ID` – logical user/agent id (e.g. `openclaw-user`)

## Commands (proposal)

This skill is designed to be called via `python3` and simple subcommands:

### 1. Add long-term memory

```bash
python3 skills/mem-longterm-sync/mem_longterm.py add \
  --type "decision+lesson" \
  --date "2026-03-21" \
  --project "openclaw-runtime,claw-tech" \
  --topics "自我进化,cron,定时任务,配置管理" \
  --summary "自我进化任务从 heartbeat 改为 cron，每晚 22:30 在隔离 session 执行。" \
  --reason "heartbeat 未正确配置导致两天未执行，自我进化依赖不可靠。" \
  --impact "所有自我进化依赖该 cron 任务，环境迁移时必须同步并校验。" \
  --source-file "MEMORY.md" \
  --source-anchor "2026-03-21"
```

The script will:

1. Parse CLI args into a JSON object following the spec
2. Attach `user_id = MEMOS_USER_ID`
3. Call the MemOS/memos API (e.g. via `add_message` or a dedicated endpoint) to store this long-term memory

### 2. Search long-term memory

```bash
python3 skills/mem-longterm-sync/mem_longterm.py search \
  --project "openclaw-runtime" \
  --topics "自我进化,cron" \
  --query "自我进化机制" \
  --limit 3
```

The script will:

1. Build a search payload using `project`, `topics`, and `query`
2. Call the MemOS/memos search API
3. Print JSON list of matching long-term memories

The calling Agent should then:

- Pick at most **3** entries
- Compress each entry into 1–2 sentences
- Attach them to the main model prompt as context

## Implementation stub

The actual implementation lives in `mem_longterm.py`. It should:

- Read `MEMOS_API_KEY` and `MEMOS_USER_ID` from env
- Provide a small CLI (e.g. `argparse`) with `add` and `search` subcommands
- Internally call the appropriate MemOS/memos HTTP endpoints

This skill intentionally **does not** define any OpenClaw tool wrappers itself –
OpenClaw can call it via `exec`/`python3` as needed, and higher-level Agents
can encapsulate the `add/search` flows according to their own logic.