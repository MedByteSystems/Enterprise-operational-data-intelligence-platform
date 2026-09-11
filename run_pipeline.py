from __future__ import annotations

import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent

STEPS = [
    ("RAW ingestion", PROJECT_ROOT / "src" / "ingestion" / "load_raw.py"),
    ("RAW -> STAGING", PROJECT_ROOT / "src" / "transformation" / "build_staging.py"),
    ("STAGING -> DWH", PROJECT_ROOT / "src" / "warehouse" / "build_dwh.py"),
]


def run_step(name: str, script: Path) -> None:
    print("\n" + "=" * 70)
    print(f"START: {name}")
    print(f"SCRIPT: {script}")
    print("=" * 70)

    if not script.exists():
        raise FileNotFoundError(f"Script not found: {script}")

    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=PROJECT_ROOT,
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"{name} failed with exit code {result.returncode}"
        )

    print(f"SUCCESS: {name}")


def main() -> None:
    print("=" * 70)
    print("EODIP - FULL DATA PIPELINE")
    print("=" * 70)

    try:
        for name, script in STEPS:
            run_step(name, script)

        print("\n" + "=" * 70)
        print("EODIP PIPELINE COMPLETED SUCCESSFULLY")
        print("=" * 70)

    except Exception as exc:
        print("\n" + "=" * 70)
        print("EODIP PIPELINE FAILED")
        print(f"ERROR: {exc}")
        print("=" * 70)
        sys.exit(1)


if __name__ == "__main__":
    main()