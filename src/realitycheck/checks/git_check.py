from pathlib import Path
from ..models import CheckResult
from ..git_utils import run_git


def check_git_repo(path: Path) -> CheckResult:
    result = CheckResult("GIT")
    git_dir = path / ".git"

    if not git_dir.exists():
        result.add(
            "Git repository not found.",
            "git init 한 번이면 되는데, 안 하셨군요.\n하드 날아가면 그냥 처음부터 다시입니다. 화이팅.",
        )
        return result

    result.add("Git repository found.")
    return result


def check_git_branch(path: Path) -> CheckResult:
    result = CheckResult("GIT BRANCH")

    if not (path / ".git").exists():
        return result

    branch, code = run_git(["branch", "--show-current"], path)
    if code != 0 or not branch:
        result.add(
            "Current branch: (unknown)",
            "브랜치 이름도 모르는 상태로 개발 중입니다.",
        )
        return result

    if branch in ("main", "master"):
        result.add(
            f"Current branch: {branch}",
            f"{branch}에서 직접 작업 중입니다.\n망가지면 되돌릴 방법이 없습니다. 뭐, 본인 선택이죠.",
        )
    else:
        result.add(
            f"Current branch: {branch}",
            "브랜치를 따로 팠군요. 팀에서 제일 성숙한 사람일 가능성이 있습니다.",
        )

    return result


def check_commit_history(path: Path) -> CheckResult:
    result = CheckResult("COMMIT HISTORY")

    if not (path / ".git").exists():
        return result

    log, code = run_git(["log", "--oneline"], path)
    if code != 0 or not log:
        result.add(
            "No commits found.",
            "git init은 했는데 커밋은 없습니다.\n이건 프로젝트가 아니라 빈 의지입니다.",
        )
        return result

    commit_count = len(log.splitlines())
    last_date, _ = run_git(["log", "-1", "--format=%cr"], path)

    if not last_date:
        last_date = "알 수 없음"

    if commit_count == 1:
        result.add(
            f"Total commits: {commit_count}  |  Last commit: {last_date}",
            "'first commit'이라고 쓰셨죠?\n다들 거기서 멈추더라고요.",
        )
    else:
        days_stale = _extract_days(last_date)
        if days_stale is not None and days_stale > 30:
            result.add(
                f"Total commits: {commit_count}  |  Last commit: {last_date}",
                f"마지막 커밋으로부터 {days_stale}일째입니다.\n이 프로젝트, 아직 살아있긴 합니까?",
            )
        else:
            result.add(
                f"Total commits: {commit_count}  |  Last commit: {last_date}",
                "꾸준히 커밋하고 있습니다. 칭찬은 딱 여기까지입니다.",
            )

    return result


def _extract_days(relative_date: str) -> int | None:
    import re
    m = re.search(r"(\d+)\s+day", relative_date)
    if m:
        return int(m.group(1))
    m = re.search(r"(\d+)\s+week", relative_date)
    if m:
        return int(m.group(1)) * 7
    m = re.search(r"(\d+)\s+month", relative_date)
    if m:
        return int(m.group(1)) * 30
    return None
