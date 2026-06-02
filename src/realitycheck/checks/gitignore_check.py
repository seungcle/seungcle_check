from pathlib import Path
from ..models import CheckResult

SHOULD_BE_IGNORED = [
    ".env",
    ".venv/",
    "__pycache__/",
    "chat_history.json",
    "resumes/",
    "outputs/*.json",
]


def check_gitignore(path: Path) -> CheckResult:
    result = CheckResult(".GITIGNORE")
    gitignore = path / ".gitignore"

    if not gitignore.exists():
        result.add(
            ".gitignore not found.",
            "뭘 올리고 뭘 숨길지 아직 결정하지 못한 상태입니다.",
        )
        return result

    content = gitignore.read_text(encoding="utf-8-sig", errors="ignore")
    rules = {l.strip() for l in content.splitlines() if l.strip() and not l.startswith("#")}

    missing = [item for item in SHOULD_BE_IGNORED if not _is_covered(item, rules)]

    if missing:
        missing_list = "\n".join(f"  {m}" for m in missing)
        result.add(
            f".gitignore found.  ({len(rules)} rules)",
            f".gitignore에 없는 항목이 있습니다:\n{missing_list}\n\n실수로 올리기 전에 추가하는 걸 추천합니다.",
        )
    else:
        result.add(f".gitignore found.  ({len(rules)} rules)")

    return result


def _is_covered(target: str, rules: set[str]) -> bool:
    if target in rules:
        return True
    # .venv/ 와 .venv 를 같은 것으로 취급
    return target.rstrip("/") in rules or (target + "/") in rules
