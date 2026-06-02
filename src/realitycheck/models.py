from dataclasses import dataclass, field


@dataclass
class Finding:
    status: str
    diagnosis: str = ""


@dataclass
class CheckResult:
    title: str
    findings: list[Finding] = field(default_factory=list)

    def add(self, status: str, diagnosis: str = "") -> None:
        self.findings.append(Finding(status, diagnosis))
