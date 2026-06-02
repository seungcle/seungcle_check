import argparse
import sys
import io
from pathlib import Path
from .checks import run_all_checks
from .output import print_header, print_result, print_footer


def _fix_win_encoding() -> None:
    if sys.platform != "win32":
        return
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    else:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


def main() -> None:
    _fix_win_encoding()

    parser = argparse.ArgumentParser(
        prog="realitycheck",
        description="개발자의 현실을 직시하게 만드는 도구",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="분석할 프로젝트 경로 (기본값: 현재 디렉토리)",
    )
    args = parser.parse_args()

    project_path = Path(args.path).resolve()

    if not project_path.exists():
        print(f"오류: 경로를 찾을 수 없습니다 — {project_path}", file=sys.stderr)
        sys.exit(1)

    if not project_path.is_dir():
        print(f"오류: 디렉토리가 아닙니다 — {project_path}", file=sys.stderr)
        sys.exit(1)

    print_header(str(project_path))

    results = run_all_checks(project_path)
    for result in results:
        if result.findings:
            print_result(result)

    print_footer()
