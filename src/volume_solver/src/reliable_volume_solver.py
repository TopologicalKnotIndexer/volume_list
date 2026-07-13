"""Run volume_solver in an isolated process with a hard timeout."""

from pathlib import Path
import math
import os
import subprocess
import sys


EXECFILE = Path(__file__).resolve().parent / "main.py"
TIMEOUT = 15.0


def run(
    command: list[str], input_text: str, timeout_sec: float
) -> float:
    """Run a solver command and return its validated numeric output."""

    if timeout_sec <= 0:
        raise ValueError("timeout_sec must be positive")
    completed = subprocess.run(
        command,
        input=input_text,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout_sec,
        check=False,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise RuntimeError(
            f"volume solver failed with exit code {completed.returncode}: "
            f"{detail or 'no diagnostic output'}"
        )
    try:
        value = float(completed.stdout.strip())
    except ValueError as exc:
        raise RuntimeError(f"volume solver returned invalid output: {completed.stdout!r}") from exc
    if not math.isfinite(value) or value < 0:
        raise RuntimeError(f"volume solver returned an invalid volume: {value!r}")
    return value


def get_volume_safe(
    pd_code: list[list[int]],
    *,
    timeout: float = TIMEOUT,
    python_path: str | os.PathLike[str] | None = None,
    verified: bool = False,
    bits_prec: int = 80,
) -> float:
    """Compute a volume in a child process and enforce *timeout*."""

    executable = os.fspath(python_path) if python_path is not None else sys.executable
    command = [executable, str(EXECFILE), "--bits-prec", str(bits_prec)]
    if verified:
        command.append("--verified")
    return run(command, repr(pd_code), timeout)


if __name__ == "__main__":
    print(get_volume_safe([[1, 5, 2, 4], [3, 1, 4, 6], [5, 3, 6, 2]]))
