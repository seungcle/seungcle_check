from pathlib import Path
from ..models import CheckResult


def check_python_env(path: Path) -> CheckResult:
    result = CheckResult("PYTHON ENVIRONMENT")

    venv_candidates = [".venv", "venv", "env", ".env_venv"]
    venv_found = next(
        (path / v for v in venv_candidates if (path / v).is_dir() and (path / v / "pyvenv.cfg").exists()),
        None,
    )

    if venv_found:
        result.add(f"Virtual environment found: {venv_found.name}/")
    else:
        result.add(
            "No virtual environment found.",
            "글로벌 환경에 pip install 하고 있군요.\n언젠가 충돌 나서 파이썬 통째로 날릴 겁니다.",
        )

    has_pyproject = (path / "pyproject.toml").exists()
    has_requirements = (path / "requirements.txt").exists()
    has_uv_lock = (path / "uv.lock").exists()
    has_pipfile = (path / "Pipfile").exists()

    if has_pyproject:
        result.add(
            "pyproject.toml found.",
            "현대 도구를 쓰고 있습니다. 그나마 다행입니다.",
        )
    elif has_requirements:
        result.add(
            "requirements.txt found.",
            "버전 고정은 했습니까?\n안 했으면 내일 갑자기 안 될 수 있습니다.",
        )
    elif has_pipfile:
        result.add(
            "Pipfile found.",
            "Pipenv 쓰는 분 아직 계셨군요. 선택은 존중합니다.",
        )
    else:
        result.add(
            "No dependency file detected.",
            "다른 컴퓨터에서 이 프로젝트 실행하면 어떻게 됩니까?\n아마 그냥 안 됩니다.",
        )

    if has_uv_lock:
        result.add(
            "uv.lock found.",
            "uv 쓰는 분이군요. 이 프로젝트에서 제일 빠른 사람입니다.",
        )

    return result
