"""Read native Codex apply_patch input without losing individual file paths."""
def patch_changes(data):
    raw = data.get("tool_input", {})
    if isinstance(raw, dict):
        patch = raw.get("command") or raw.get("patch") or raw.get("input") or raw.get("patch_text") or ""
    else:
        patch = raw if isinstance(raw, str) else ""
    path, added, removed = None, [], []
    for line in str(patch).splitlines():
        if line.startswith(("*** Add File: ", "*** Update File: ", "*** Delete File: ")):
            if path is not None:
                yield path, "\n".join(added), "\n".join(removed)
            path, added, removed = line.split(": ", 1)[1], [], []
        elif line.startswith("*** Move to: "):
            path = line.split(": ", 1)[1]
        elif line.startswith("+"):
            added.append(line[1:])
        elif line.startswith("-"):
            removed.append(line[1:])
    if path is not None:
        yield path, "\n".join(added), "\n".join(removed)
