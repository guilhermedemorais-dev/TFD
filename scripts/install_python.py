# Contexto TFD · 222 palavras · 468 tokens (o200k_base)

"""Prepare an isolated Python environment for the TFD tools."""

import argparse
import os
import subprocess
import sys
import venv
from pathlib import Path


REQUIREMENTS = Path(__file__).resolve().parents[1] / "requirements.txt"


def install(destination):
    destination = destination.resolve()
    config = destination / "pyvenv.cfg"
    if destination.exists() and (not destination.is_dir() or (not config.is_file() and any(destination.iterdir()))):
        raise ValueError("choose an empty directory or an existing virtual environment")

    python = destination / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    if not python.is_file():
        venv.EnvBuilder(with_pip=True).create(destination)
    subprocess.run([python, "-I", "-m", "pip", "install", "--disable-pip-version-check",
                    "--only-binary=:all:", "-r", REQUIREMENTS], check=True)
    subprocess.run([python, "-I", "-m", "pip", "check"], check=True)

    cache = destination / "tfd-tokenizer-cache"
    cache.mkdir(exist_ok=True)
    subprocess.run([python, "-I", "-c", "import yaml, tiktoken; "
                    "assert yaml.safe_load('ready: true')['ready']; "
                    "assert tiktoken.get_encoding('o200k_base').encode_ordinary('ready')"],
                   env={**os.environ, "TIKTOKEN_CACHE_DIR": str(cache)}, check=True)
    return python


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--venv", required=True, type=Path, help="directory for the isolated Python environment")
    args = parser.parse_args()
    if sys.version_info < (3, 10):
        parser.error("Python 3.10 or newer is required")
    try:
        print(f"TFD Python: {install(args.venv)}")
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"TFD Python setup failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
