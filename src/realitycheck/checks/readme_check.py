from pathlib import Path
from ..models import CheckResult


def check_readme(path: Path) -> CheckResult:
    result = CheckResult("README")

    candidates = ["README.md", "README.rst", "README.txt", "README"]
    readme_file = next((path / c for c in candidates if (path / c).exists()), None)

    if readme_file is None:
        result.add(
            "README.md not found.",
            "본인도 3개월 뒤엔 이게 뭔지 모릅니다. 장담합니다.",
        )
        return result

    content = readme_file.read_text(encoding="utf-8", errors="ignore")
    lines = [l for l in content.splitlines() if l.strip()]
    char_count = len(content.strip())

    if char_count < 50:
        result.add(
            f"{readme_file.name} found.  ({char_count} chars)",
            "README가 있긴 한데 제목만 있습니다.\n'파일이 존재한다'는 사실 하나로 양심을 달래는 타입이군요.",
        )
    elif len(lines) <= 5:
        result.add(
            f"{readme_file.name} found.  ({len(lines)} lines)",
            "README가 너무 짧습니다.\n최소한의 성의는 보였다고 치겠습니다.",
        )
    else:
        result.add(
            f"{readme_file.name} found.  ({len(lines)} lines)",
            "README를 제대로 썼군요.\n이 팀에서 제일 욕 안 먹는 사람일 것 같습니다.",
        )

    return result
