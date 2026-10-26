"""binka-lab's guard rules, loaded by the autorun plugin's guard hook.

The framework supplies the mechanism and its generic rules; this file adds the one rule that is binka-lab's own:
a session here never reads or touches ~/dev/binka, the private repo (E9 §3, the one-way rule). Its self-test is
the guard hook's `--self-test`, run from this repo.
"""
import glob
import os
import re
from pathlib import Path

from guard_bash import segments

BINKA = (Path.home() / "dev/binka").resolve()
_PARTS = re.compile(r"[\s=:,;'\"()<>]")       # a path inside an option's value, a string or a call
# a mention anywhere, heredoc bodies included: lab text has no reason to name the private repo
_NAMED = re.compile(rf"(?:~|\$HOME|\$\{{HOME\}}|{re.escape(str(Path.home()))})/dev/(?:\{{(?:[\w.-]*,)*)?binka(?![\w-])")


def _into_binka(token: str, cwd: Path) -> bool:
    for part in _PARTS.split(token):
        part = os.path.expandvars(os.path.expanduser(part))
        if not part or ("binka" not in part and not glob.has_magic(part)):
            continue
        p = Path(part) if Path(part).is_absolute() else cwd / part
        for q in [p, *map(Path, glob.glob(str(p)))] if glob.has_magic(part) else [p]:
            try:
                if q.resolve().is_relative_to(BINKA):
                    return True
            except (OSError, RuntimeError):
                continue
    return False


def _hits(command: str, cwd: str) -> bool:
    """Each segment's paths, resolved where the shell is when it runs them (after any `cd` before it)."""
    here = Path(cwd or ".")
    for argv in segments(command):
        argv = [t.lstrip("({") for t in argv if t.lstrip("({")]       # a subshell or a group
        if any(_into_binka(tok, here) for tok in argv):
            return True
        if argv and argv[0] in ("cd", "pushd"):
            to = [t for t in argv[1:] if not t.startswith("-")]
            here = here / os.path.expandvars(os.path.expanduser(to[0] if to else "~"))
    return False


def rule_no_binka(command: str, cwd: str) -> str | None:
    if _NAMED.search(command) or _hits(command, cwd):
        return ("⛔ A binka-lab session never reads or touches ~/dev/binka (E9 §3, the one-way rule). Its only input "
                "from binka is the bundle in data/bundle/. If the site needs something else, open a card for binka's "
                "lane.")
    return None


EXTRA_RULES = [rule_no_binka]

_HOME = str(Path.home())

# (command, cwd relative to the repo root, should_block)
CASES = [
    ("cat ~/dev/binka/README.md", ".", True),
    (f"cat {_HOME}/dev/binka/py/showcase/scan.py", ".", True),
    ("git -C ~/dev/binka log -1", ".", True),
    ("cd ~/dev/binka && ls", ".", True),
    ("ls $HOME/dev/binka", ".", True),
    (f"python3 -c \"print(open('{_HOME}/dev/binka/x').read())\"", ".", True),
    ("grep -rn claim --include=*.md ~/dev/binka/py/doc", ".", True),
    ("cat ~/dev/binka-lab/docs/README.md", ".", False),
    ("ls docs content", ".", False),
    ("grep -rn binka docs/", ".", False),
    ("echo binka is the private repo", ".", False),
    ("cat > notes.md <<'EOF'\nnever read ~/dev/binka\nEOF", ".", True),
    ("python3 - <<'EOF'\nprint(open('" + _HOME + "/dev/binka/x').read())\nEOF", ".", True),
    ("cat ~/dev/bink?/README.md", ".", True),
    ("cd ~/dev && cat binka/README.md", ".", True),
    ("(cd ~/dev; cat binka/README.md)", ".", True),
    ("cd && cat dev/binka/README.md", ".", True),
    ("cat ~/dev/{binka,}/README.md", ".", True),
    ("cat > n.md <<EOF\nsee ~/dev/binka.\nEOF", ".", True),
    ("rm -rf node_modules dist", ".", False),
]
