from pathlib import Path
from ..models import CheckResult


def check_cache(path: Path) -> CheckResult:
    result = CheckResult("PYTHON CACHE")

    pycache_dirs = list(path.rglob("__pycache__"))
    pycache_count = len(pycache_dirs)

    if pycache_count > 0:
        result.add(
            f"{pycache_count} __pycache__ {'directory' if pycache_count == 1 else 'directories'} found.",
            ".gitignore에 추가는 하셨습니까?",
        )
    else:
        result.add("No __pycache__ directories found.")

    if (path / ".pytest_cache").exists():
        result.add(
            ".pytest_cache detected.",
            "테스트를 돌린 흔적이 있습니다. 통과는 했습니까?",
        )

    return result
