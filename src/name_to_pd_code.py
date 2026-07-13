"""Run the bundled name-to-PD resolver as a local program."""

from ast import literal_eval
from pathlib import Path
import subprocess
import sys


SOURCE_DIR = Path(__file__).resolve().parent
RESOLVER_MAIN = SOURCE_DIR / "name_to_pd_code" / "src" / "main.py"


def name_to_pd_code(knotname: str, *, timeout: float = 30.0) -> list[list[int]]:
    """Return the bundled resolver's PD code for *knotname*."""

    if not isinstance(knotname, str):
        raise TypeError("knotname must be a string")
    if not RESOLVER_MAIN.is_file():
        raise FileNotFoundError(RESOLVER_MAIN)
    if timeout <= 0:
        raise ValueError("timeout must be positive")
    completed = subprocess.run(
        [sys.executable, str(RESOLVER_MAIN)],
        input=knotname,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
        check=False,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise RuntimeError(
            f"bundled name resolver failed with exit code {completed.returncode}: "
            f"{detail or 'no diagnostic output'}"
        )
    try:
        pd_code = literal_eval(completed.stdout.strip())
    except (SyntaxError, ValueError) as exc:
        raise RuntimeError(f"bundled name resolver returned invalid output: {completed.stdout!r}") from exc
    if not isinstance(pd_code, list):
        raise RuntimeError("bundled name resolver did not return a PD-code list")
    return pd_code
