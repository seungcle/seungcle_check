from pathlib import Path
from ..models import CheckResult

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".pytest_cache", ".venv", "venv", "env", ".mypy_cache", ".ruff_cache"}
KEYWORDS = ["TODO", "FIXME", "HACK", "TEMP"]
TEXT_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".go", ".rs", ".rb",
    ".php", ".c", ".cpp", ".h", ".cs", ".swift", ".kt", ".scala",
    ".md", ".txt", ".yaml", ".yml", ".toml", ".json", ".html", ".css",
    ".sh", ".bash", ".zsh", ".fish", ".sql", ".r", ".m",
}


def check_todos(path: Path) -> CheckResult:
    result = CheckResult("TODO / FIXME")
    counts: dict[str, int] = {k: 0 for k in KEYWORDS}

    for file in _iter_text_files(path):
        try:
            text = file.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for keyword in KEYWORDS:
            counts[keyword] += text.count(keyword)

    total = sum(counts.values())

    if total == 0:
        result.add(
            "No TODO / FIXME / HACK / TEMP found.",
            "코드가 완벽하거나, 주석을 아예 안 쓰거나 둘 중 하나입니다.\n솔직히 후자겠죠.",
        )
        return result

    detail_parts = [f"{k}: {v}" for k, v in counts.items() if v > 0]
    result.add(
        f"Total: {total}  ({',  '.join(detail_parts)})",
        _todo_diagnosis(total),
    )
    return result


def _todo_diagnosis(total: int) -> str:
    if total <= 5:
        return "TODO가 몇 개 있습니다.\n미래의 당신한테 숙제를 넘긴 상태입니다."
    if total <= 15:
        return "TODO가 꽤 쌓였습니다.\n계획은 항상 충분하더라고요."
    if total <= 37:
        return f"TODO가 {total}개입니다.\n이쯤 되면 TODO가 주석이 아니라 일정입니다."
    return f"TODO가 {total}개입니다.\n축하합니다. TODO 자체가 하나의 프로젝트가 되었습니다."


def _iter_text_files(path: Path):
    for item in path.rglob("*"):
        if item.is_file() and not _should_skip(item, path):
            if item.suffix.lower() in TEXT_EXTENSIONS or item.suffix == "":
                yield item


def _should_skip(file: Path, root: Path) -> bool:
    try:
        parts = file.relative_to(root).parts
    except ValueError:
        return True
    return any(part in SKIP_DIRS for part in parts)
