"""The bundle's leak scanner (P1 §7.3; disclosure policy §3 "scanner"). One file, vendored into binka-lab's `tools/`:
the standard library only, plus `pyarrow` to decode parquet string columns (SD-SC-11; a tree holding parquet fails
when pyarrow is missing, it never skips the file). No binka imports.

    python scan.py PATH...        # a file or a tree; a bundle dir (with manifest.json) takes its listed digests

It reads decoded strings, never compressed bytes: every string of a JSON file (keys included), every string cell, column
name and metadata value of a parquet file, and the text of any other file. A finding names the file, the place, the
offset and the rule, never the value. Exit 1 on any finding.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import sys
from collections import Counter
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

VERSION = "1"

RULES = tuple((name, re.compile(p)) for name, p in (
    ("aws_key_id", r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    ("pem_block", r"-----BEGIN[ A-Z0-9]*-----"),
    ("auth_header", r"(?i)\bauthorization\s*[:=]\s*[\"']?(?:basic|bearer|token)\s+[A-Za-z0-9._~+/-]{8,}"),
    ("bearer_token", r"(?i)\bbearer\s+[A-Za-z0-9._~+/-]{16,}"),
    ("basic_auth_url", r"\b[a-z][a-z0-9+.-]*://[^/\s:@'\"]+:[^/\s:@'\"]{3,}@"),
    ("jwt", r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}"),
    ("token_prefix", r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_\w{40,}|sk-ant-[\w-]{20,}|sk-[A-Za-z0-9_-]{32,}"
                     r"|xox[abprs]-[A-Za-z0-9-]{16,}|[sr]k_live_[A-Za-z0-9]{16,}|AIza[0-9A-Za-z_-]{35})"),
    ("notify_url", r"https?://[^\s/'\"]*ntfy[^\s/'\"]*/[\w-]{4,}"),
    ("password_assignment", r"(?i)pass(?:word|wd)[\"']?\s*[=:]\s*[\"']?[^\s\"'`,;]{6,}"),
    ("user_password_flag", r"\s-u\s*[\"']?[^\s:\"'/]+:[^\s\"'@]{4,}"),         # curl's -u flag with a user and a password
))
HEX64 = re.compile(r"(?<![0-9A-Fa-f])[0-9A-Fa-f]{64}(?![0-9A-Fa-f])")
HEXLONG = re.compile(r"(?<![0-9A-Fa-f])[0-9A-Fa-f]{65,}(?![0-9A-Fa-f])")      # hex entropy can't pass 4.0
KEY64 = re.compile(r"(?<![A-Za-z0-9])(?=[A-Za-z0-9]{0,63}[A-Z])(?=[A-Za-z0-9]{0,63}[a-z])(?=[A-Za-z0-9]{0,63}\d)"
                   r"[A-Za-z0-9]{64}(?![A-Za-z0-9])")              # an exchange-style API key
RUN = re.compile(r"[A-Za-z0-9+/=_-]{32,}")
PIECE = re.compile(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\d+")       # a word, an acronym or a number, camelCase split
HEX = re.compile(r"[0-9a-f]+|[0-9A-F]+")
SEPARATORS = re.compile(r"[/_.=+-]")
NONSPACE = re.compile(r"\S+")
DIGEST_KEY = re.compile(r"(?:sha256|fingerprint)$")          # a manifest's recorded digests: `*sha256` keys
ENTROPY_MIN = 4.0


@dataclass(frozen=True, order=True)
class Finding:
    where: str                          # file, then the place inside it: a JSON path, a column and row, a line
    offset: int
    rule: str

    def __str__(self) -> str:
        return f"{self.where} @{self.offset}: {self.rule}"


@dataclass(frozen=True)
class Allowed:
    """What a recorded bundle lets pass the shape rules (64-hex, long hex, 64-character key, entropy): its recorded
    digests, by the exact token, and the strings a review record covers, by their sha256 (their reader saw every
    token in them). The credential rules always apply."""
    digests: frozenset[str] = frozenset()
    reviewed: frozenset[str] = frozenset()

    def __or__(self, other: Allowed) -> Allowed:
        return Allowed(self.digests | other.digests, self.reviewed | other.reviewed)


@dataclass(frozen=True)
class Digests:
    """Salted sha256 digests of the secret values and their encodings (P1 §7.3). The file holds no value."""
    salt: str
    entries: tuple[tuple[str, int, str, bool], ...]       # (name, length, sha256, the value holds whitespace)

    def matches(self, strings: Iterable[tuple[str, str]]) -> list[tuple[str, str]]:
        """(where, secret name) for every same-length run of characters that hashes to a digest. A value without
        whitespace is looked for inside each string's non-space runs only, which keeps prose cheap."""
        by_len: dict[tuple[int, bool], dict[str, str]] = {}
        for name, n, sha, spaces in self.entries:
            by_len.setdefault((n, spaces), {})[sha] = name
        salt, out, places = self.salt.encode(), set(), {}
        for where, s in strings:                          # each distinct string is hashed once
            places.setdefault(s, []).append(where)
        for s, wheres in places.items():
            runs = NONSPACE.findall(s)
            for (n, spaces), shas in by_len.items():
                for run in [s] if spaces else runs:
                    for i in range(len(run) - n + 1):
                        if name := shas.get(hashlib.sha256(salt + run[i:i + n].encode()).hexdigest()):
                            out.update((where, name) for where in wheres)
        return sorted(out)


def shannon(s: str) -> float:
    n = len(s)
    return -sum(c / n * math.log2(c / n) for c in Counter(s).values())


def _wordlike(s: str) -> bool:
    """An identifier, a path or a slug rather than a random token: most of it is in segments that are short, hex, or
    words averaging four characters or more (a random token's pieces average under three)."""
    def plain(seg: str) -> bool:
        if len(seg) <= 3 or HEX.fullmatch(seg):
            return True
        pieces = PIECE.findall(seg)
        return sum(map(len, pieces)) == len(seg) and len(seg) >= 4 * len(pieces)
    return sum(len(x) for x in SEPARATORS.split(s) if x and plain(x)) >= 0.6 * len(s)


def scan_string(s: str, where: str, allowed: Allowed = Allowed()) -> list[Finding]:
    """Every rule over one decoded string, the shape rules except where `allowed` covers the token or the string."""
    out = [Finding(where, m.start(), name) for name, rx in RULES for m in rx.finditer(s)]
    if allowed.reviewed and hashlib.sha256(s.encode()).hexdigest() in allowed.reviewed:
        return out
    seen = {f.offset for f in out}                    # a credential already found there isn't reported twice
    return out + [f for f in shape_findings(s, where, allowed.digests) if f.offset not in seen]


def shape_findings(s: str, where: str, digests: frozenset[str] = frozenset()) -> list[Finding]:
    """The shape rules alone: what a reviewer is told a text trips."""
    out = [Finding(where, m.start(), name) for name, rx in (("hex64", HEX64), ("hex_long", HEXLONG), ("key64", KEY64))
           for m in rx.finditer(s) if m.group() not in digests]
    seen = {f.offset for f in out}
    out += [Finding(where, m.start(), "entropy") for m in RUN.finditer(s)
            if m.start() not in seen and m.group() not in digests and shannon(m.group()) > ENTROPY_MIN
            and not _wordlike(m.group())]
    return out


def _json_strings(obj, path: str) -> Iterator[tuple[str, str]]:
    if isinstance(obj, str):
        yield path, obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield f"{path}.<key>", k
            yield from _json_strings(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from _json_strings(v, f"{path}[{i}]")


def _parquet_strings(data: bytes) -> Iterator[tuple[str, str]]:
    import pyarrow as pa                    # the one non-stdlib import: parquet columns are compressed (SD-SC-11)
    import pyarrow.parquet as pq
    table = pq.read_table(pa.BufferReader(data))
    for k, v in (table.schema.metadata or {}).items():
        yield "<metadata>", k.decode(errors="replace")
        yield "<metadata>", v.decode(errors="replace")
    for name in table.column_names:
        yield "<columns>", name
        col = table.column(name)
        if pa.types.is_string(col.type) or pa.types.is_large_string(col.type) or pa.types.is_dictionary(col.type):
            for i, v in enumerate(col.to_pylist()):
                if isinstance(v, str):
                    yield f"{name}[{i}]", v


def strings_of(rel: str, data: bytes) -> Iterator[tuple[str, str]]:
    """A file's decoded strings, each with its place: `rel` then a JSON path, a column and row, or nothing. A `.json`
    file that doesn't parse (a config with comments) is scanned as text, which still holds every string."""
    if rel.endswith(".parquet"):
        for where, s in _parquet_strings(data):
            yield f"{rel}:{where}", s
        return
    if rel.endswith(".json"):
        try:
            obj = json.loads(data)
        except ValueError:
            pass
        else:
            yield from ((f"{rel}:{where}", s) for where, s in _json_strings(obj, "$"))
            return
    yield rel, data.decode("utf-8", errors="replace")


def scan_strings(strings: Iterable[tuple[str, str]], allowed: Allowed = Allowed(), tokens=(),
                 digests: Digests | None = None) -> list[Finding]:
    """The rules, then binka's private token lists ((list name, pattern)) and the secret digests, if given. A token
    or a secret is reported by its list's or its secret's name."""
    strings = list(strings)
    out = [f for where, s in strings for f in scan_string(s, where, allowed)]
    out += [Finding(where, m.start(), f"token:{name}") for where, s in strings for name, pat in tokens
            if (m := pat.search(s))]
    if digests:
        out += [Finding(where, 0, f"secret:{name}") for where, name in digests.matches(strings)]
    return sorted(out)


def scoped(rel: str, scopes: dict[str, Allowed]) -> Allowed:
    """What the manifests over a file record: each manifest's, for the files under its own directory only."""
    out = Allowed()
    for d, a in scopes.items():
        if PurePosixPath(rel).is_relative_to(d):
            out |= a
    return out


def scan_files(files: dict[str, bytes], allowed: Allowed | dict[str, Allowed] = Allowed(), tokens=(),
               digests: Digests | None = None) -> list[Finding]:
    """Every file's strings, and its path: a name can hold a token too. `allowed` is one bundle's, or a manifest's
    directory → its records (`read_tree`'s scopes); files are scanned together per scope."""
    groups: dict[Allowed, list[str]] = {}
    for rel in sorted(files):
        groups.setdefault(allowed if isinstance(allowed, Allowed) else scoped(rel, allowed), []).append(rel)
    return sorted(f for a, rels in groups.items()
                  for f in scan_strings([(f"{rel}:<path>", rel) for rel in rels] +
                                        [x for rel in rels for x in strings_of(rel, files[rel])], a, tokens, digests))


def manifest_allowed(manifest: dict) -> Allowed:
    """What a bundle's manifest records: every value under a `*sha256` or `*fingerprint` key (its tables, schemas
    and inputs), and the hashes of its reviewed strings (`reviewed_prose_sha256`)."""
    reviewed = frozenset(x for x in manifest.get("reviewed_prose_sha256") or () if isinstance(x, str))
    return Allowed(frozenset(s for path, s in _json_strings(manifest, "$") if DIGEST_KEY.search(path)) | reviewed,
                   reviewed)


def _manifest(data: bytes) -> Allowed:
    """A bundle manifest's records; a file of that name that isn't one records nothing (its strings are still read)."""
    try:
        obj = json.loads(data)
    except ValueError:
        return Allowed()
    return manifest_allowed(obj) if isinstance(obj, dict) else Allowed()


def add_scope(scopes: dict[str, Allowed], rel: str, data: bytes) -> None:
    """A manifest's records, for the files under its own directory (`scoped`)."""
    d = str(PurePosixPath(rel).parent)
    scopes[d] = scopes.get(d, Allowed()) | _manifest(data)


def read_tree(paths: Iterable[Path]) -> tuple[dict[str, bytes], dict[str, Allowed]]:
    """The CLI's reader: every file under the paths, and what each bundle manifest among them records, by the
    manifest's directory: a manifest exempts nothing outside it."""
    files, scopes = {}, {}
    for root in map(Path, paths):
        for f in sorted(root.rglob("*")) if root.is_dir() else [root]:
            if f.is_file():
                files[str(f)] = f.read_bytes()
                if f.name == "manifest.json":
                    add_scope(scopes, str(f), files[str(f)])
    return files, scopes


def main(argv: list[str] | None = None) -> int:
    paths = sys.argv[1:] if argv is None else argv
    if not paths:
        print(__doc__)
        return 2
    files, scopes = read_tree(paths)
    findings = scan_files(files, scopes)
    for f in findings:
        print(f)
    print(f"scan {VERSION}: {len(files)} files, {len(findings)} findings")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
