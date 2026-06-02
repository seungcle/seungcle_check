from pathlib import Path
from ..models import CheckResult
from ..git_utils import run_git


def check_env(path: Path) -> CheckResult:
    result = CheckResult("ENVIRONMENT VARIABLES")
    env_file = path / ".env"

    if not env_file.exists():
        result.add(".env not found.")
        return result

    result.add(".env detected.")

    gitignore = path / ".gitignore"
    env_ignored = False
    if gitignore.exists():
        content = gitignore.read_text(encoding="utf-8-sig", errors="ignore")
        rules = [l.strip() for l in content.splitlines() if l.strip() and not l.startswith("#")]
        env_ignored = any(r in (".env", "*.env", ".env*") for r in rules)

    if not env_ignored:
        result.add(
            ".env is not ignored.",
            "API 키 공개 중입니다. 님 돈 많으세요? (아니면 그냥 깜빡하신 거겠죠?)",
        )

    if (path / ".git").exists():
        tracked, code = run_git(["ls-files", ".env"], path)
        if code == 0 and tracked:
            result.add(
                ".env is tracked by Git.",
                "이건 설정 파일이 아니라 사고 보고서입니다.",
            )

    return result
