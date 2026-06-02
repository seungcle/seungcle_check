from pathlib import Path
from ..models import CheckResult


def check_structure(path: Path) -> CheckResult:
    result = CheckResult("PROJECT STRUCTURE")

    src_exists = (path / "src").is_dir()
    tests_exists = (path / "tests").is_dir() or (path / "test").is_dir()
    test_files = list(path.rglob("test_*.py")) + list(path.rglob("*_test.py"))

    if src_exists:
        result.add("src/ directory found.")
    else:
        result.add(
            "No src/ directory found.",
            "파일이 루트에 전부 몰려 있습니다.\n파일 20개 넘어가는 순간 본인도 길 잃습니다.",
        )

    if tests_exists or test_files:
        test_count = len(test_files)
        result.add(
            f"Tests detected.  ({test_count} test files)",
            "테스트가 있군요.\n통과한다고 버그가 없는 건 아닙니다만, 없는 것보단 낫습니다.",
        )
    else:
        result.add(
            "No tests directory or test files found.",
            "'돌아가면 됐지'를 신봉하는 타입으로 분류되었습니다.",
        )

    return result
