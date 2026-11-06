# Contexto TFD · 512 palavras · 1024 tokens (o200k_base)

"""Measure local UTF-8 files without sending their contents to the agent."""

import argparse
import json
import os
import re
import sys
from pathlib import Path


WORDS = re.compile(r"\b\w+(?:[-’']\w+)*\b")
LABEL = r"Contexto TFD · [0-9]+ palavras · (?:[0-9]+ tokens \([\w-]+\)|tokens indisponíveis)\n\n"
MARKERS = {".md": ">", ".py": "#", ".js": "//", ".ts": "//"}
ENCODING_COOKIE = re.compile(r"^[ \t\f]*#.*?coding[:=][ \t]*[-\w.]+")


def markdown_body(text):
    return re.sub(r"\A> " + LABEL, "", text, count=1)


def split_header(path, text):
    suffix = path.suffix.lower()
    marker = MARKERS.get(suffix)
    if marker is None:
        return "", text
    lines = text.splitlines(keepends=True)
    start = int(text.startswith("#!") and suffix != ".md")
    if suffix == ".py":
        for index, line in enumerate(lines[:2]):
            if ENCODING_COOKIE.match(line):
                start = index + 1
                break
    prefix = "".join(lines[:start])
    body = re.sub(r"\A" + re.escape(marker) + " " + LABEL, "", "".join(lines[start:]), count=1)
    return prefix, body


def measure(path, encoding):
    text = path.read_text(encoding="utf-8-sig")
    prefix, body = split_header(path, text)
    words = len(WORDS.findall(prefix + body))
    tokens = len(encoding.encode_ordinary(prefix + body)) if encoding is not None else None
    return prefix, body, words, tokens


def load_encoding(name):
    import tiktoken

    cache = Path(sys.prefix) / "tfd-tokenizer-cache"
    if cache.is_dir():
        os.environ.setdefault("TIKTOKEN_CACHE_DIR", str(cache))
    return tiktoken.get_encoding(name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--encoding", default="o200k_base")
    parser.add_argument("--max-tokens", type=int, help="maximum per file")
    parser.add_argument("--max-total-tokens", type=int, help="maximum combined token budget")
    parser.add_argument("--stamp", action="store_true", help="update Markdown, Python, JS or TS headers in place")
    args = parser.parse_args()
    if any(limit is not None and limit < 0 for limit in (args.max_tokens, args.max_total_tokens)):
        parser.error("token limits must be nonnegative")
    if args.stamp and any(path.suffix.lower() not in MARKERS for path in args.files):
        parser.error("unsupported header format; keep counts in the run receipt")

    encoding = None
    try:
        encoding = load_encoding(args.encoding)
    except (ImportError, AttributeError, OSError, ValueError) as exc:
        print(f"Tokenizer unavailable: {exc}", file=sys.stderr)

    try:
        measured = [(path, *measure(path, encoding)) for path in args.files]
        files = []
        for path, prefix, body, words, tokens in measured:
            over = tokens > args.max_tokens if tokens is not None and args.max_tokens is not None else None
            files.append({"path": str(path), "words": words, "tokens": tokens, "over_limit": over})
            if args.stamp:
                token_label = f"{tokens} tokens ({encoding.name})" if encoding else "tokens indisponíveis"
                header = f"{MARKERS[path.suffix.lower()]} Contexto TFD · {words} palavras · {token_label}\n\n"
                if prefix and not prefix.endswith("\n"):
                    prefix += "\n"
                path.write_text(prefix + header + body, encoding="utf-8", newline="\n")
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    total = sum(item["tokens"] for item in files) if encoding is not None else None
    over_total = total > args.max_total_tokens if total is not None and args.max_total_tokens is not None else None
    print(json.dumps({"encoding": encoding.name if encoding else None, "files": files,
                      "total_tokens": total, "over_total_limit": over_total}, indent=2))
    if encoding is None:
        return 3
    return 2 if over_total or any(item["over_limit"] for item in files) else 0


if __name__ == "__main__":
    raise SystemExit(main())
