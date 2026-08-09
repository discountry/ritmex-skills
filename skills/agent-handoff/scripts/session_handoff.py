#!/usr/bin/env python3
"""Deterministic native-session discovery and reading for agent-handoff.

The script intentionally owns session discovery so the calling model does not need to
invent paths or session-selection logic. It reads only local Claude Code / Codex
session metadata and transcript files; it never modifies them.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sqlite3
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Optional, Sequence, Tuple

SKILL_VERSION = "2"
DEFAULT_MAX_CANDIDATES = 8
DEFAULT_CHUNK_LINES = 200
DEFAULT_WORKSPACE_CHUNK_LINES = 300
MAX_PREVIEW_CHARS = 5000
MAX_PREVIEW_ITEMS = 12


@dataclass
class Candidate:
    session_id: str
    path: Path
    cwd: str
    mtime: float
    source_agent: str
    archived: bool = False


def canonical_path(value: str | Path) -> str:
    return os.path.realpath(os.path.abspath(os.path.expanduser(str(value))))


def same_cwd(left: str | Path, right: str | Path) -> bool:
    try:
        return canonical_path(left) == canonical_path(right)
    except OSError:
        return os.path.abspath(os.path.expanduser(str(left))) == os.path.abspath(
            os.path.expanduser(str(right))
        )


def detect_host_and_source() -> Tuple[str, str]:
    """Return (host_agent, source_agent) using shell-tool environment markers.

    Claude Code exports CLAUDE_CODE_SESSION_ID into Bash/PowerShell subprocesses.
    Codex exports CODEX_THREAD_ID into shell tool subprocesses. Any host without the
    Claude marker follows the user's rule and hands off from Claude Code.
    """
    if os.environ.get("CLAUDE_CODE_SESSION_ID"):
        return "claude", "codex"
    if os.environ.get("CODEX_THREAD_ID"):
        return "codex", "claude"
    return "other", "claude"


def claude_home() -> Path:
    configured = os.environ.get("CLAUDE_CONFIG_DIR")
    return Path(configured).expanduser() if configured else Path.home() / ".claude"


def codex_home() -> Path:
    configured = os.environ.get("CODEX_HOME")
    return Path(configured).expanduser() if configured else Path.home() / ".codex"


def encode_claude_project_path(cwd: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]", "-", cwd)


def iter_jsonl_head(path: Path, max_lines: int = 50) -> Iterator[Dict[str, Any]]:
    try:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            for index, raw in enumerate(handle):
                if index >= max_lines:
                    break
                raw = raw.strip()
                if not raw:
                    continue
                try:
                    value = json.loads(raw)
                except json.JSONDecodeError:
                    continue
                if isinstance(value, dict):
                    yield value
    except OSError:
        return


def read_tail_lines(path: Path, max_lines: int = 100) -> List[str]:
    """Read the last max_lines without loading a multi-megabyte transcript at once."""
    try:
        with path.open("rb") as handle:
            handle.seek(0, os.SEEK_END)
            size = handle.tell()
            block = 8192
            data = bytearray()
            position = size
            newlines = 0
            while position > 0 and newlines <= max_lines:
                take = min(block, position)
                position -= take
                handle.seek(position)
                chunk = handle.read(take)
                data[:0] = chunk
                newlines = data.count(b"\n")
            text = data.decode("utf-8", errors="replace")
            lines = text.splitlines()
            return lines[-max_lines:]
    except OSError:
        return []


def nested_get(mapping: Dict[str, Any], path: Sequence[str]) -> Any:
    current: Any = mapping
    for key in path:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def extract_cwd(record: Dict[str, Any]) -> Optional[str]:
    for key_path in (
        ("cwd",),
        ("payload", "cwd"),
        ("payload", "meta", "cwd"),
    ):
        value = nested_get(record, key_path)
        if isinstance(value, str) and value.strip():
            return value
    return None


def extract_session_id(record: Dict[str, Any]) -> Optional[str]:
    for key_path in (
        ("sessionId",),
        ("session_id",),
        ("id",),
        ("payload", "session_id"),
        ("payload", "id"),
        ("payload", "meta", "session_id"),
        ("payload", "meta", "id"),
    ):
        value = nested_get(record, key_path)
        if isinstance(value, str) and value.strip():
            return value
    return None


def fallback_session_id(path: Path) -> str:
    stem = path.stem
    uuid_match = re.search(
        r"([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})",
        stem,
    )
    if uuid_match:
        return uuid_match.group(1)
    digest = hashlib.sha256(str(path).encode("utf-8")).hexdigest()[:20]
    return f"file-{digest}"


def metadata_from_head(path: Path) -> Tuple[Optional[str], Optional[str]]:
    found_cwd: Optional[str] = None
    found_id: Optional[str] = None
    for record in iter_jsonl_head(path):
        if found_cwd is None:
            found_cwd = extract_cwd(record)
        if found_id is None:
            found_id = extract_session_id(record)
        if found_cwd and found_id:
            break
    return found_cwd, found_id


def discover_claude(target_cwd: str) -> List[Candidate]:
    root = claude_home()
    projects = root / "projects"
    if not projects.is_dir():
        return []

    raw_cwd = os.path.abspath(os.path.expanduser(target_cwd))
    canonical_cwd = canonical_path(target_cwd)
    expected_dirs = {
        encode_claude_project_path(raw_cwd),
        encode_claude_project_path(canonical_cwd),
    }
    candidates: List[Candidate] = []

    try:
        project_dirs = list(projects.iterdir())
    except OSError:
        return []

    # Prefer the expected project directory, while still scanning other top-level
    # project folders for sessions whose embedded cwd matches exactly. This protects
    # against path-encoding collisions and config migrations.
    project_dirs.sort(key=lambda p: (p.name not in expected_dirs, p.name))

    for project_dir in project_dirs:
        if not project_dir.is_dir():
            continue
        try:
            files = list(project_dir.glob("*.jsonl"))
        except OSError:
            continue
        for path in files:
            try:
                stat = path.stat()
            except OSError:
                continue
            if stat.st_size <= 0:
                continue

            embedded_cwd, embedded_id = metadata_from_head(path)
            matches = bool(embedded_cwd and same_cwd(embedded_cwd, target_cwd))
            if not matches and embedded_cwd is None and project_dir.name in expected_dirs:
                matches = True
            if not matches:
                continue

            candidates.append(
                Candidate(
                    session_id=embedded_id or fallback_session_id(path),
                    path=path,
                    cwd=embedded_cwd or target_cwd,
                    mtime=stat.st_mtime,
                    source_agent="claude",
                )
            )

    return dedupe_and_sort(candidates)


def sqlite_thread_candidates(home: Path, target_cwd: str) -> List[Candidate]:
    databases: List[Path] = []
    for path in home.glob("state_*.sqlite"):
        match = re.search(r"state_(\d+)\.sqlite$", path.name)
        rank = int(match.group(1)) if match else -1
        databases.append((rank, path))  # type: ignore[arg-type]
    databases.sort(key=lambda item: item[0], reverse=True)  # type: ignore[index]

    results: List[Candidate] = []
    for _, db_path in databases:  # type: ignore[misc]
        try:
            uri = f"file:{db_path.resolve()}?mode=ro"
            connection = sqlite3.connect(uri, uri=True, timeout=0.2)
        except (OSError, sqlite3.Error):
            continue
        try:
            cols = {
                row[1]
                for row in connection.execute("PRAGMA table_info(threads)").fetchall()
            }
            required = {"id", "cwd", "rollout_path"}
            if not required.issubset(cols):
                continue
            select_cols = ["id", "cwd", "rollout_path"]
            if "archived" in cols:
                select_cols.append("archived")
            query = f"SELECT {', '.join(select_cols)} FROM threads"
            for row in connection.execute(query):
                session_id, cwd, rollout_path = row[:3]
                archived = bool(row[3]) if len(row) > 3 else False
                if archived or not isinstance(cwd, str) or not same_cwd(cwd, target_cwd):
                    continue
                if not isinstance(rollout_path, str) or not rollout_path.strip():
                    continue
                path = Path(rollout_path).expanduser()
                if not path.is_absolute():
                    path = home / path
                try:
                    stat = path.stat()
                except OSError:
                    continue
                if stat.st_size <= 0:
                    continue
                results.append(
                    Candidate(
                        session_id=str(session_id) if session_id else fallback_session_id(path),
                        path=path,
                        cwd=cwd,
                        mtime=stat.st_mtime,
                        source_agent="codex",
                        archived=False,
                    )
                )
        except sqlite3.Error:
            pass
        finally:
            connection.close()
        # Newest state DB is the relevant one. Avoid duplicate work against old schemas.
        if results:
            break
    return results


def scan_codex_rollouts(home: Path, target_cwd: str) -> List[Candidate]:
    sessions = home / "sessions"
    if not sessions.is_dir():
        return []
    results: List[Candidate] = []
    try:
        paths = sessions.rglob("*.jsonl")
        for path in paths:
            try:
                stat = path.stat()
            except OSError:
                continue
            if stat.st_size <= 0:
                continue
            embedded_cwd, embedded_id = metadata_from_head(path)
            if not embedded_cwd or not same_cwd(embedded_cwd, target_cwd):
                continue
            results.append(
                Candidate(
                    session_id=embedded_id or fallback_session_id(path),
                    path=path,
                    cwd=embedded_cwd,
                    mtime=stat.st_mtime,
                    source_agent="codex",
                )
            )
    except OSError:
        return results
    return results


def discover_codex(target_cwd: str) -> List[Candidate]:
    home = codex_home()
    results = sqlite_thread_candidates(home, target_cwd)
    # Rollout JSONL is the durable transcript source and also catches sessions missing
    # from the SQLite state DB. Union both sources instead of trusting an index alone.
    results.extend(scan_codex_rollouts(home, target_cwd))
    return dedupe_and_sort(results)


def dedupe_and_sort(candidates: Iterable[Candidate]) -> List[Candidate]:
    by_path: Dict[str, Candidate] = {}
    for candidate in candidates:
        key = canonical_path(candidate.path)
        existing = by_path.get(key)
        if existing is None or candidate.mtime > existing.mtime:
            by_path[key] = candidate
    return sorted(by_path.values(), key=lambda item: item.mtime, reverse=True)


def discover_for_source(source_agent: str, target_cwd: str) -> List[Candidate]:
    if source_agent == "codex":
        return discover_codex(target_cwd)
    if source_agent == "claude":
        return discover_claude(target_cwd)
    raise ValueError(f"unsupported source agent: {source_agent}")


def flatten_text(value: Any, output: List[str], depth: int = 0) -> None:
    if depth > 6 or len(output) >= 50:
        return
    if isinstance(value, str):
        text = value.strip()
        if text:
            output.append(text)
        return
    if isinstance(value, list):
        for item in value:
            flatten_text(item, output, depth + 1)
        return
    if not isinstance(value, dict):
        return

    # Prefer message-bearing keys and ignore opaque reasoning/encrypted blobs.
    for key in ("text", "message", "content", "error", "last_agent_message", "reason"):
        if key in value:
            flatten_text(value[key], output, depth + 1)


def preview_from_record(record: Dict[str, Any]) -> Optional[str]:
    line_type = record.get("type")
    role: Optional[str] = None
    payload: Any = record.get("payload")
    body: Any = None

    if line_type in {"user", "assistant"}:
        role = str(line_type)
        body = record.get("message", record)
    elif line_type == "response_item" and isinstance(payload, dict):
        if payload.get("type") == "message":
            role_value = payload.get("role")
            role = str(role_value) if role_value else "message"
            body = payload.get("content", payload)
    elif line_type == "event_msg" and isinstance(payload, dict):
        event_type = payload.get("type")
        if event_type in {
            "user_message",
            "agent_message",
            "task_complete",
            "error",
            "turn_aborted",
        }:
            role = str(event_type)
            body = payload
    elif line_type in {"error", "result"}:
        role = str(line_type)
        body = record

    if body is None:
        return None
    fragments: List[str] = []
    flatten_text(body, fragments)
    if not fragments:
        return None
    text = " ".join(fragments)
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return None
    if len(text) > 700:
        text = text[:697] + "..."
    return f"{role}: {text}"


def tail_preview(path: Path) -> Tuple[str, str]:
    raw_lines = read_tail_lines(path, max_lines=120)
    previews: List[str] = []
    raw_tail = "\n".join(raw_lines)
    for raw in raw_lines:
        try:
            record = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if not isinstance(record, dict):
            continue
        preview = preview_from_record(record)
        if preview and (not previews or preview != previews[-1]):
            previews.append(preview)
    previews = previews[-MAX_PREVIEW_ITEMS:]
    joined = "\n".join(previews)
    if len(joined) > MAX_PREVIEW_CHARS:
        joined = joined[-MAX_PREVIEW_CHARS:]

    lowered = raw_tail.lower()
    interruption_markers = (
        "usage limit",
        "rate limit",
        "rate_limit",
        "quota exceeded",
        "quota_exceeded",
        "credit balance",
        "turn_aborted",
        "turn aborted",
        "interrupted",
        "you've hit your",
        "you have hit your",
    )
    status_hint = "interrupted" if any(marker in lowered for marker in interruption_markers) else "unknown"
    return joined, status_hint


def count_lines(path: Path) -> int:
    total = 0
    try:
        with path.open("rb") as handle:
            for block in iter(lambda: handle.read(1024 * 1024), b""):
                total += block.count(b"\n")
        if path.stat().st_size and total == 0:
            return 1
        return total
    except OSError:
        return 0


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def iso_mtime(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat().replace("+00:00", "Z")


def candidate_to_dict(candidate: Candidate, index: int) -> Dict[str, Any]:
    preview, status_hint = tail_preview(candidate.path)
    try:
        size = candidate.path.stat().st_size
    except OSError:
        size = 0
    return {
        "index": index,
        "session_id": candidate.session_id,
        "updated_at": iso_mtime(candidate.mtime),
        "path": str(candidate.path),
        "bytes": size,
        "lines": count_lines(candidate.path),
        "status_hint": status_hint,
        "tail_preview": preview,
    }


def cmd_discover(args: argparse.Namespace) -> int:
    cwd = canonical_path(args.cwd or os.getcwd())
    host_agent, source_agent = detect_host_and_source()
    candidates = discover_for_source(source_agent, cwd)
    selected = candidates[: max(1, args.max_candidates)]
    payload = {
        "schema_version": SKILL_VERSION,
        "host_agent": host_agent,
        "source_agent": source_agent,
        "cwd": cwd,
        "source_home": str(codex_home() if source_agent == "codex" else claude_home()),
        "candidate_count": len(selected),
        "has_more_candidates": len(candidates) > len(selected),
        "candidates": [candidate_to_dict(candidate, index) for index, candidate in enumerate(selected)],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def find_session(source_agent: str, cwd: str, session_id: str) -> Optional[Candidate]:
    for candidate in discover_for_source(source_agent, cwd):
        if candidate.session_id == session_id:
            return candidate
    return None


def cmd_read(args: argparse.Namespace) -> int:
    cwd = canonical_path(args.cwd or os.getcwd())
    _, source_agent = detect_host_and_source()
    candidate = find_session(source_agent, cwd, args.session)
    if candidate is None:
        print(
            f"agent-handoff: session {args.session!r} is not a valid {source_agent} session for cwd {cwd}",
            file=sys.stderr,
        )
        return 3

    digest = sha256_file(candidate.path)
    if args.expect_sha256 and args.expect_sha256 != digest:
        print(
            "agent-handoff: transcript changed after discovery/read; aborting to avoid mixed history",
            file=sys.stderr,
        )
        return 4

    total = count_lines(candidate.path)
    start = max(1, args.start_line)
    max_lines = max(1, args.max_lines)
    if start > total and total > 0:
        print(f"agent-handoff: start line {start} is past end of transcript ({total})", file=sys.stderr)
        return 5

    end = min(total, start + max_lines - 1) if total else 0
    next_start = end + 1 if end and end < total else None

    print("HANDOFF_SESSION_CHUNK")
    print(f"source_agent={source_agent}")
    print(f"session_id={candidate.session_id}")
    print(f"path={candidate.path}")
    print(f"sha256={digest}")
    print(f"lines={start}-{end}/{total}")
    print(f"next_start_line={next_start if next_start is not None else 'NONE'}")
    print("---")

    try:
        with candidate.path.open("r", encoding="utf-8", errors="replace") as handle:
            for line_no, raw in enumerate(handle, start=1):
                if line_no < start:
                    continue
                if line_no > end:
                    break
                sys.stdout.write(raw)
                if not raw.endswith("\n"):
                    sys.stdout.write("\n")
    except OSError as exc:
        print(f"agent-handoff: failed to read transcript: {exc}", file=sys.stderr)
        return 6

    print("---")
    print("END_HANDOFF_SESSION_CHUNK")
    return 0



def run_git(cwd: str, args: Sequence[str]) -> Tuple[int, str, str]:
    """Run git deterministically without pagers, colors, external diffs, or textconv."""
    command = [
        "git",
        "-C",
        cwd,
        "--no-pager",
        "-c",
        "color.ui=false",
        "-c",
        "core.pager=cat",
        *args,
    ]
    env = os.environ.copy()
    env["GIT_PAGER"] = "cat"
    env["PAGER"] = "cat"
    try:
        completed = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env,
            check=False,
        )
    except OSError as exc:
        return 127, "", str(exc)
    return completed.returncode, completed.stdout, completed.stderr


def git_output_or_error(cwd: str, args: Sequence[str], label: str) -> str:
    code, stdout, stderr = run_git(cwd, args)
    if code != 0:
        detail = stderr.strip() or stdout.strip() or f"git exited with status {code}"
        raise RuntimeError(f"{label} failed: {detail}")
    return stdout.rstrip("\n")


def build_workspace_snapshot(cwd: str) -> str:
    """Return an immutable textual snapshot of current Git state and full tracked diffs.

    The snapshot includes exact branch/HEAD metadata, porcelain status with every
    untracked path, the complete unstaged `git diff`, and the complete staged
    `git diff --cached`. The model must consume this instead of guessing workspace
    state from transcript history.
    """
    cwd = canonical_path(cwd)
    code, root_out, _ = run_git(cwd, ["rev-parse", "--show-toplevel"])
    if code != 0:
        return "\n".join(
            [
                "HANDOFF_WORKSPACE_SNAPSHOT",
                f"cwd={cwd}",
                "git_repo=false",
                "---",
                "Current working directory is not inside a Git repository.",
                "---",
                "END_HANDOFF_WORKSPACE_SNAPSHOT",
            ]
        ) + "\n"

    repo_root = canonical_path(root_out.strip())
    branch = git_output_or_error(cwd, ["branch", "--show-current"], "git branch --show-current")
    head = git_output_or_error(cwd, ["rev-parse", "HEAD"], "git rev-parse HEAD")
    status = git_output_or_error(
        cwd,
        ["status", "--porcelain=v1", "--branch", "--untracked-files=all"],
        "git status",
    )
    unstaged = git_output_or_error(
        cwd,
        [
            "diff",
            "--no-ext-diff",
            "--no-textconv",
            "--no-color",
            "--submodule=diff",
            "--",
        ],
        "git diff",
    )
    staged = git_output_or_error(
        cwd,
        [
            "diff",
            "--cached",
            "--no-ext-diff",
            "--no-textconv",
            "--no-color",
            "--submodule=diff",
            "--",
        ],
        "git diff --cached",
    )

    branch_value = branch if branch else "DETACHED"
    sections = [
        "HANDOFF_WORKSPACE_SNAPSHOT",
        f"cwd={cwd}",
        "git_repo=true",
        f"repo_root={repo_root}",
        f"branch={branch_value}",
        f"head={head}",
        "--- git status --porcelain=v1 --branch --untracked-files=all ---",
        status,
        "--- git diff --no-ext-diff --no-textconv --no-color --submodule=diff -- ---",
        unstaged,
        "--- git diff --cached --no-ext-diff --no-textconv --no-color --submodule=diff -- ---",
        staged,
        "---",
        "END_HANDOFF_WORKSPACE_SNAPSHOT",
    ]
    return "\n".join(sections) + "\n"


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def cmd_workspace(args: argparse.Namespace) -> int:
    cwd = canonical_path(args.cwd or os.getcwd())
    snapshot = build_workspace_snapshot(cwd)
    digest = sha256_text(snapshot)
    if args.expect_sha256 and args.expect_sha256 != digest:
        print(
            "agent-handoff: workspace changed while its Git snapshot was being read; aborting to avoid mixed state",
            file=sys.stderr,
        )
        return 7

    lines = snapshot.splitlines(keepends=True)
    total = len(lines)
    start = max(1, args.start_line)
    max_lines = max(1, args.max_lines)
    if start > total and total > 0:
        print(f"agent-handoff: workspace start line {start} is past end of snapshot ({total})", file=sys.stderr)
        return 8

    end = min(total, start + max_lines - 1) if total else 0
    next_start = end + 1 if end and end < total else None

    print("HANDOFF_WORKSPACE_CHUNK")
    print(f"sha256={digest}")
    print(f"lines={start}-{end}/{total}")
    print(f"next_start_line={next_start if next_start is not None else 'NONE'}")
    print("---")
    for raw in lines[start - 1 : end]:
        sys.stdout.write(raw)
        if raw and not raw.endswith("\n"):
            sys.stdout.write("\n")
    print("---")
    print("END_HANDOFF_WORKSPACE_CHUNK")
    return 0

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Discover and read native Claude Code/Codex sessions for cross-agent handoff."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    discover = subparsers.add_parser("discover", help="discover exact-cwd source sessions")
    discover.add_argument("--cwd", default=None, help="working directory; defaults to current directory")
    discover.add_argument(
        "--max-candidates",
        type=int,
        default=DEFAULT_MAX_CANDIDATES,
        help=f"maximum newest candidates to show (default {DEFAULT_MAX_CANDIDATES})",
    )
    discover.set_defaults(func=cmd_discover)

    read = subparsers.add_parser("read", help="read an exact chunk of a discovered native transcript")
    read.add_argument("--session", required=True, help="session_id returned by discover")
    read.add_argument("--cwd", default=None, help="working directory; defaults to current directory")
    read.add_argument("--start-line", type=int, default=1, help="1-based line number")
    read.add_argument(
        "--max-lines",
        type=int,
        default=DEFAULT_CHUNK_LINES,
        help=f"maximum lines to emit (default {DEFAULT_CHUNK_LINES})",
    )
    read.add_argument(
        "--expect-sha256",
        default=None,
        help="abort if transcript SHA-256 differs from this value",
    )
    read.set_defaults(func=cmd_read)

    workspace = subparsers.add_parser(
        "workspace",
        help="read a deterministic snapshot of current Git branch, status, and diffs",
    )
    workspace.add_argument(
        "--cwd", default=None, help="working directory; defaults to current directory"
    )
    workspace.add_argument("--start-line", type=int, default=1, help="1-based snapshot line number")
    workspace.add_argument(
        "--max-lines",
        type=int,
        default=DEFAULT_WORKSPACE_CHUNK_LINES,
        help=f"maximum snapshot lines to emit (default {DEFAULT_WORKSPACE_CHUNK_LINES})",
    )
    workspace.add_argument(
        "--expect-sha256",
        default=None,
        help="abort if the regenerated workspace snapshot differs from this SHA-256",
    )
    workspace.set_defaults(func=cmd_workspace)
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except KeyboardInterrupt:
        return 130
    except Exception as exc:  # Keep failure explicit; the skill must not improvise around it.
        print(f"agent-handoff: unexpected error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
