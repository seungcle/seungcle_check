# seungcle-check

[![PyPI](https://img.shields.io/pypi/v/seungcle-check)](https://pypi.org/project/seungcle-check/)
[![Python](https://img.shields.io/pypi/pyversions/seungcle-check)](https://pypi.org/project/seungcle-check/)

개발자의 현실을 직시하게 만드는 CLI 도구.

프로젝트 폴더를 분석해서 나중에 후회할 것들을 미리 알려줍니다.  

---

## 설치

```bash
pip install seungcle-check
```

## 사용법

```bash
seungcle-check                 # 현재 디렉토리 분석
seungcle-check ./my-project    # 특정 경로 분석
seungcle-check -v              # 버전 확인
```

## 출력 예시

```
  seungcle realitycheck
  현실 점검 대상: /my-project
────────────────────────────────────────────────────

[GIT]

Git repository not found.

git init 한 번이면 되는데, 안 하셨군요.
하드 날아가면 그냥 처음부터 다시입니다. 화이팅.

────────────────────────────────────────────────────

[README]

README.md not found.

본인도 3개월 뒤엔 이게 뭔지 모릅니다. 장담합니다.

────────────────────────────────────────────────────

[PROJECT STRUCTURE]

No tests directory or test files found.

'돌아가면 됐지'를 신봉하는 타입으로 분류되었습니다.

────────────────────────────────────────────────────

현실 점검이 완료되었습니다.
```

## 검사 항목

| 항목 | 내용 |
|---|---|
| Git | 저장소 존재 여부 |
| Git Branch | main/master 직접 작업 감지 |
| Commit History | 커밋 수, 마지막 커밋 날짜 |
| README | 존재 여부, 내용 충실도 |
| .gitignore | 존재 여부, 누락 항목 감지 |
| Environment Variables | .env 감지, gitignore 누락, git tracking 여부 |
| Python Environment | 가상환경, 의존성 파일 |
| Python Cache | \_\_pycache\_\_, .pytest_cache |
| Project Structure | src/, tests/ 디렉토리 |

## 요구사항

- Python 3.10 이상
