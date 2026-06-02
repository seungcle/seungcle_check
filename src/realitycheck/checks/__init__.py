from pathlib import Path
from ..models import CheckResult
from .git_check import check_git_repo, check_git_branch, check_commit_history
from .readme_check import check_readme
from .gitignore_check import check_gitignore
from .env_check import check_env
from .python_env_check import check_python_env
from .todo_check import check_todos
from .cache_check import check_cache
from .nodejs_check import check_nodejs
from .structure_check import check_structure


def run_all_checks(path: Path) -> list[CheckResult]:
    return [
        check_git_repo(path),
        check_git_branch(path),
        check_commit_history(path),
        check_readme(path),
        check_gitignore(path),
        check_env(path),
        check_python_env(path),
        check_todos(path),
        check_cache(path),
        check_nodejs(path),
        check_structure(path),
    ]
