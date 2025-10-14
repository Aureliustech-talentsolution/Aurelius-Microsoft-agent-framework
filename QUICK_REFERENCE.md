# Quick Reference Card
# Microsoft Agent Framework - Aurelius Implementation

**⚡ Keep this handy while developing!**

---

## 🚀 Essential Commands

### Open Workspace
```bash
code microsoft-agent-framework.code-workspace
```

### Python Setup
```bash
cd python
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install uv && uv pip install -e .[all]
```

### Azure Login
```bash
az login --tenant 944b3898-fcbe-4631-91e1-794e102c9c7d
```

### Install Git Hooks
```bash
pre-commit install
pre-commit install --hook-type commit-msg
```

---

## ⌨️ Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Command Palette | `Ctrl+Shift+P` |
| Quick Open File | `Ctrl+P` |
| Go to Symbol | `Ctrl+Shift+O` |
| Search Files | `Ctrl+Shift+F` |
| Toggle Terminal | ``Ctrl+` `` |
| Debug | `F5` |
| Toggle Breakpoint | `F9` |
| Save & Format | `Ctrl+S` |
| Build | `Ctrl+Shift+B` |
| Run Tests | `Ctrl+Shift+P` → Test |

---

## 🏃 Quick Tasks

Access: `Ctrl+Shift+P` → `Tasks: Run Task`

### Python
- `Python: Install Dependencies`
- `Python: Run Tests`
- `Python: Format (Ruff + Black + isort)`
- `Python: Type Check (MyPy)`

### DevUI
- `DevUI: Start Server (Default Port 8080)`
- `DevUI: Start with Tracing (Framework)`
- `DevUI: Start Headless (API Only)`
- `DevUI: Test API Endpoints`
- `DevUI: Open in Browser`

### .NET
- `.NET: Build Solution`
- `.NET: Run Tests`

### Security
- `Security: Run All Scans`
- `Compliance: Generate All Evidence`

### Quality
- `Quality: Run All Checks`
- `Pre-commit: Run All Hooks`

---

## 🐛 Debug Configurations

| Configuration | Use For |
|--------------|---------|
| Python: Current File | Debug open Python file (F5) |
| Python: Pytest Current File | Debug tests |
| .NET: Launch Current Project | Debug .NET project |

---

## 📁 Workspace Folders

```
🏠 Root - Agent Framework          # Repository root
🐍 Python - Core Framework         # Python code
📦 Python - Packages               # Python packages
🧪 Python - Samples                # Python examples
🔷 .NET - Framework                # .NET code
🔷 .NET - Samples                  # .NET examples
🔒 Aurelius - Compliance & Security # Compliance docs
📚 Documentation                   # Framework docs
🚀 Workflows                       # Workflow samples
```

---

## 🧪 Testing

### Python
```bash
# Run all tests with coverage
pytest --cov --cov-report=html -v

# Run specific test
pytest tests/test_example.py -v

# Run with coverage threshold
pytest --cov --cov-fail-under=85
```

### .NET
```bash
# Run all tests
dotnet test dotnet/agent-framework-dotnet.slnx

# With coverage
dotnet test --collect:"XPlat Code Coverage"
```

---

## 🔐 Security & Compliance

### Security Scans
```bash
# All scans
bandit -r . && semgrep --config=auto . && safety check && pip-audit

# Individual
bandit -r .          # Python security
semgrep --config=auto .  # Multi-language
safety check         # Dependencies
pip-audit           # Package audit
```

### Evidence Generation
```bash
# SBOM
cyclonedx-py -o .aurelius/evidence/sbom/sbom-$(date +%Y%m%d).json

# Licenses
pip-licenses --format=json --output-file=.aurelius/evidence/compliance/licenses.json
```

---

## 📂 Important Files

| File | Purpose |
|------|---------|
| `.vscode/tasks.json` | All automated tasks |
| `.vscode/launch.json` | Debug configurations |
| `.vscode/settings.json` | Workspace settings |
| `.pre-commit-config.yaml` | Git hooks configuration |
| `pyproject.toml` | Python dependencies & config |
| `.editorconfig` | Code style rules |
| `.aurelius/CLAUDE.md` | Development standards |

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| **[WORKSPACE_GUIDE.md](WORKSPACE_GUIDE.md)** | Complete workspace guide ⭐ |
| **[WORKSPACE_SUMMARY.md](WORKSPACE_SUMMARY.md)** | Setup summary |
| **[SETUP_COMPLETE.md](SETUP_COMPLETE.md)** | Project setup details |
| **[README.aurelius.md](README.aurelius.md)** | Aurelius implementation |
| **[.aurelius/PRD.md](.aurelius/PRD.md)** | Product requirements |
| **[.aurelius/ARCHITECTURE.md](.aurelius/ARCHITECTURE.md)** | Technical architecture |

---

## 🔧 Troubleshooting

### Python interpreter not found
```bash
cd python && python -m venv .venv
# Restart VS Code
# Click Python version in status bar → Select .venv
```

### Tasks not showing
```bash
Ctrl+Shift+P → Developer: Reload Window
```

### Git hooks not running
```bash
pre-commit install
pre-commit install --hook-type commit-msg
```

### .NET solution not loading
```bash
# Check .vscode/settings.json has:
"dotnet.defaultSolution": "dotnet/agent-framework-dotnet.slnx"
# Reload window
```

---

## 💡 Pro Tips

1. **Auto-Format**: Code auto-formats on save
2. **Inline Errors**: Error Lens shows errors next to code
3. **TODOs**: TODO Tree highlights all TODO comments
4. **GitLens**: Inline git blame and history
5. **Multi-Cursor**: `Alt+Click` or `Ctrl+Alt+↑/↓`
6. **Split Editor**: `Ctrl+\`
7. **Zen Mode**: `View → Appearance → Zen Mode`
8. **Search in Files**: `Ctrl+Shift+F`
9. **Replace in Files**: `Ctrl+Shift+H`
10. **Command Palette**: `Ctrl+Shift+P` (access everything!)

---

## 🎯 Quality Gates

**Pre-Commit:**
- ✅ Linting, type checking, secret detection

**Pre-Merge:**
- ✅ 85%+ test coverage
- ✅ 65%+ mutation score
- ✅ Zero critical vulnerabilities
- ✅ SBOM & license compliance

---

## 🤝 Support

**Slack Channels:**
- `#agent-framework-dev`
- `#agent-framework-security`
- `#agent-framework-compliance`

**Email:**
- technical-support@aureliustech.com
- security@aureliustech.com

---

## 🚦 Status Bar Info

| Item | What It Shows |
|------|---------------|
| Python Version | Current interpreter (click to change) |
| Git Branch | Current branch (click to switch) |
| Errors/Warnings | Problem count (click to view) |
| Line/Column | Cursor position |
| Encoding | File encoding (UTF-8) |
| EOL | Line endings (LF) |

---

## 📦 Extensions Categories

**Essential:**
- Python, Pylance, Ruff, C# Dev Kit, GitLens

**Security:**
- Snyk, Trunk.io, ShellCheck

**Productivity:**
- GitHub Copilot, TODO Tree, Error Lens, Better Comments

**Full list**: `.vscode/extensions.json`

---

## 🎨 Code Formatting

### Python
- **Formatter**: Ruff (auto on save)
- **Linter**: Ruff
- **Type Check**: MyPy (strict mode), Pyright
- **Import Sort**: Ruff

### C#
- **Formatter**: ms-dotnettools.csharp (auto on save)
- **Style**: .editorconfig rules
- **Analyzer**: Roslyn + StyleCop

---

## 🔄 Git Workflow

### Commit Format
```
type(scope): description [evidence: path]

Types: feat, fix, docs, test, security, compliance, refactor
Scope: python, dotnet, workflows, agents, mcp, devui
Evidence: Path to generated artifacts
```

### Example
```bash
git commit -m "feat(agents): add CUI handling [evidence: .aurelius/evidence/security/]"
```

### Branch Naming
```
feature/AF-123-my-feature
bugfix/AF-456-fix-issue
security/CVE-2024-XXXXX
compliance/CMMC-AC-1-001
```

---

## ⚡ One-Liners

```bash
# Setup everything
cd python && python -m venv .venv && source .venv/bin/activate && pip install uv && uv pip install -e .[all] && pre-commit install

# Run all quality checks
ruff check --fix . && black . && isort . && mypy . && pytest --cov --cov-fail-under=85

# Generate all evidence
cyclonedx-py -o .aurelius/evidence/sbom/sbom-latest.json && pip-licenses --format=json --output-file=.aurelius/evidence/compliance/licenses.json

# Security scan
bandit -r . && semgrep --config=auto . && safety check && pip-audit
```

---

## 📊 Test Markers

```python
@pytest.mark.unit          # Unit tests
@pytest.mark.integration   # Integration tests
@pytest.mark.security      # Security tests
@pytest.mark.compliance    # Compliance tests
@pytest.mark.slow          # Slow tests
```

Run specific: `pytest -m unit`

---

## 🎯 Coverage Thresholds

- **Python Test Coverage**: ≥85%
- **Mutation Testing**: ≥65%
- **.NET Test Coverage**: ≥80%

---

## 🔗 Quick Links

- [Microsoft Agent Framework Docs](https://learn.microsoft.com/agent-framework/)
- [Aurelius Federal Platform](https://github.com/AureliustechandTalentSolutions/Resource-libraryAurelius-Federal-Platform)
- [CMMC v2.0](https://www.acq.osd.mil/cmmc/)
- [NIST 800-171](https://csrc.nist.gov/publications/detail/sp/800-171/rev-2/final)

---

**🎉 Happy Coding!**

**Last Updated**: 2025-10-13
