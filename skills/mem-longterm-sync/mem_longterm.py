#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""MemOS long-term memory helper (skeleton).

This is a minimal stub that defines the CLI shape for:
- adding long-term memories following mem-longterm-spec
- searching long-term memories

The concrete HTTP calls to MemOS/memos should be filled in later.
"""

import argparse
import json
import os
import sys
from typing import List


def get_env_or_die(name: str) -> str:
    value = os.getenv(name)
    if not value:
        print(json.dumps({"error": f"Missing env var: {name}"}, ensure_ascii=False))
        sys.exit(1)
    return value


def cmd_add(args: argparse.Namespace) -> None:
    """Build a long-term memory JSON object and (eventually) send to MemOS.

    For now, we just print the JSON payload to stdout so callers can see
    exactly what would be sent. HTTP integration can be added later.
    """

    user_id = get_env_or_die("MEMOS_USER_ID")
    _ = get_env_or_die("MEMOS_API_KEY")  # reserved for future HTTP calls

    project: List[str]
    if "," in args.project:
        project = [p.strip() for p in args.project.split(",") if p.strip()]
    else:
        project = [args.project.strip()] if args.project else []

    topics: List[str] = []
    if args.topics:
        topics = [t.strip() for t in args.topics.split(",") if t.strip()]

    payload = {
        "user_id": user_id,
        "type": args.type,
        "date": args.date,
        "project": project,
        "topics": topics,
        "summary": args.summary,
        "reason": args.reason,
        "impact": args.impact,
        "source": {
            "file": args.source_file,
            "anchor": args.source_anchor,
        },
    }

    print(json.dumps({"ok": True, "memory": payload}, ensure_ascii=False))


def cmd_search(args: argparse.Namespace) -> None:
    """Search long-term memories.

    This is a stub: it only prints the search parameters. Actual MemOS HTTP
    search should be implemented later.
    """

    user_id = get_env_or_die("MEMOS_USER_ID")
    _ = get_env_or_die("MEMOS_API_KEY")

    project: List[str] = []
    if args.project:
        if "," in args.project:
            project = [p.strip() for p in args.project.split(",") if p.strip()]
        else:
            project = [args.project.strip()]

    topics: List[str] = []
    if args.topics:
        topics = [t.strip() for t in args.topics.split(",") if t.strip()]

    query_payload = {
        "user_id": user_id,
        "project": project,
        "topics": topics,
        "query": args.query,
        "limit": args.limit,
    }

    print(json.dumps({"ok": True, "search": query_payload}, ensure_ascii=False))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="MemOS long-term memory helper")
    sub = parser.add_subparsers(dest="command", required=True)

    # add
    p_add = sub.add_parser("add", help="add a long-term memory entry")
    p_add.add_argument("--type", required=True, help="memory type, e.g. rule/decision/milestone/lesson")
    p_add.add_argument("--date", required=True, help="date in YYYY-MM-DD")
    p_add.add_argument("--project", required=True, help="project name(s), comma-separated")
    p_add.add_argument("--topics", required=False, default="", help="topics, comma-separated")
    p_add.add_argument("--summary", required=True, help="short summary")
    p_add.add_argument("--reason", required=True, help="reason for this rule/decision/lesson")
    p_add.add_argument("--impact", required=True, help="long-term impact / constraints")
    p_add.add_argument("--source-file", required=True, help="local source file, e.g. MEMORY.md")
    p_add.add_argument("--source-anchor", required=True, help="anchor inside the source file")
    p_add.set_defaults(func=cmd_add)

    # search
    p_search = sub.add_parser("search", help="search long-term memories")
    p_search.add_argument("--project", required=False, default="", help="project name(s), comma-separated")
    p_search.add_argument("--topics", required=False, default="", help="topics, comma-separated")
    p_search.add_argument("--query", required=True, help="free text query")
    p_search.add_argument("--limit", type=int, required=False, default=3, help="max results to return")
    p_search.set_defaults(func=cmd_search)

    return parser


def main(argv: List[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
