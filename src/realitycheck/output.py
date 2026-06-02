from .models import CheckResult

SEPARATOR = "─" * 52


def print_header(project_path: str) -> None:
    print()
    print("  seungcle realitycheck")
    print(f"  현실 점검 대상: {project_path}")
    print(SEPARATOR)
    print()


def print_result(result: CheckResult) -> None:
    if not result.findings:
        return

    print(f"[{result.title}]")
    print()

    for finding in result.findings:
        if finding.status:
            print(finding.status)
        if finding.diagnosis:
            print()
            print(finding.diagnosis)
        print()

    print(SEPARATOR)
    print()


def print_footer() -> None:
    print("현실 점검이 완료되었습니다.")
    print()
