from pathlib import Path
from ..models import CheckResult


def check_nodejs(path: Path) -> CheckResult:
    result = CheckResult("NODE.JS")

    node_modules = path / "node_modules"
    pkg_lock = path / "package-lock.json"
    pnpm_lock = path / "pnpm-lock.yaml"
    yarn_lock = path / "yarn.lock"
    package_json = path / "package.json"

    if not package_json.exists():
        return result

    result.add("package.json found.")

    if node_modules.exists():
        try:
            pkg_count = sum(1 for _ in node_modules.iterdir() if _.is_dir())
        except OSError:
            pkg_count = 0
        result.add(
            f"node_modules detected.  (~{pkg_count} packages)",
            "이 폴더 하나가 우주의 절반보다 파일이 많습니다.\n.gitignore에는 넣으셨죠?",
        )

    if pkg_lock.exists():
        result.add("package-lock.json found.")
    elif pnpm_lock.exists():
        result.add("pnpm-lock.yaml found.")
    elif yarn_lock.exists():
        result.add("yarn.lock found.")
    else:
        result.add(
            "No lockfile found.",
            "npm install 할 때마다 다른 버전이 설치됩니다.\n'내 컴퓨터에서는 됐는데'의 원인이 바로 이겁니다.",
        )

    return result
