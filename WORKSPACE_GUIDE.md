# VS Code Workspace Guide
# Microsoft Agent Framework - Aurelius Implementation

**Date**: 2025-10-13
**Status**: Ready for Development

---

## 📂 Workspace Structure

This workspace is organized into **9 logical folders** for optimal navigation and development:

```
🏠 Root - Agent Framework          # Top-level configuration and documentation
🐍 Python - Core Framework         # Python implementation root
📦 Python - Packages               # Individual Python packages (core, a2a, azure-ai, etc.)
🧪 Python - Samples                # Python code samples and examples
🔷 .NET - Framework                # .NET implementation root
🔷 .NET - Samples                  # .NET code samples and examples
🔒 Aurelius - Compliance & Security # Aurelius-specific compliance documentation
📚 Documentation                   # Framework documentation
🚀 Workflows                       # Workflow samples and templates
```

---

## 🚀 Quick Start

### 1. Open the Workspace

```bash
# From VS Code
File → Open Workspace from File → select "microsoft-agent-framework.code-workspace"

# Or from command line
code microsoft-agent-framework.code-workspace
```

### 2. Install Recommended Extensions

When you open the workspace, VS Code will prompt you to install recommended extensions. Click **"Install All"** or install individually:

**Essential Extensions:**
- **Python**: `ms-python.python`
- **Pylance**: `ms-python.vscode-pylance`
- **Ruff**: `charliermarsh.ruff`
- **C# Dev Kit**: `ms-dotnettools.csdevkit`
- **GitLens**: `eamodio.gitlens`

**Full list in**: [`.vscode/extensions.json`](.vscode/extensions.json)

### 3. Configure Python Environment

```bash
# Option 1: Use the task (Ctrl+Shift+P → Tasks: Run Task)
"Python: Setup Environment"

# Option 2: Manual setup
cd python
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install uv
uv pip install -e .[all]
```

### 4. Configure Azure CLI

```bash
# Run the Azure Login task (Ctrl+Shift+P → Tasks: Run Task)
"Azure: Login"

# Or manually
az login --tenant 944b3898-fcbe-4631-91e1-794e102c9c7d
az account show
```

### 5. Install Pre-commit Hooks

```bash
# Use the task
"Pre-commit: Install Hooks"

# Or manually
pre-commit install
pre-commit install --hook-type commit-msg
```

---

## 🎯 Common Tasks

All tasks are accessible via **Ctrl+Shift+P** → **Tasks: Run Task**

### Python Development

| Task Name | Description | Shortcut |
|-----------|-------------|----------|
| **Python: Install Dependencies** | Install all Python dependencies | - |
| **Python: Run Tests** | Run pytest with coverage | Ctrl+Shift+P → Test |
| **Python: Lint (Ruff)** | Run Ruff linter | - |
| **Python: Format (Ruff + Black + isort)** | Format all Python code | - |
| **Python: Type Check (MyPy)** | Run MyPy type checker | - |
| **Python: Type Check (Pyright)** | Run Pyright type checker | - |

### .NET Development

| Task Name | Description | Shortcut |
|-----------|-------------|----------|
| **.NET: Restore Dependencies** | Restore NuGet packages | - |
| **.NET: Build Solution** | Build the entire solution | Ctrl+Shift+B |
| **.NET: Run Tests** | Run all .NET tests | - |
| **.NET: Run Tests with Coverage** | Run tests with code coverage | - |
| **.NET: Clean** | Clean build artifacts | - |

### Security & Compliance

| Task Name | Description | Shortcut |
|-----------|-------------|----------|
| **Security: Run Bandit** | Python security scanner | - |
| **Security: Run Semgrep** | Multi-language security scanner | - |
| **Security: Run All Scans** | Run all security tools | - |
| **Compliance: Generate SBOM** | Create Software Bill of Materials | - |
| **Compliance: Generate License Report** | License compliance report | - |
| **Compliance: Generate All Evidence** | Generate all compliance artifacts | - |

### Quality Assurance

| Task Name | Description | Shortcut |
|-----------|-------------|----------|
| **Quality: Run All Checks** | Run all linting, type checking, tests, and security scans | - |
| **Pre-commit: Run All Hooks** | Run all pre-commit hooks manually | - |

---

## 🐛 Debugging

### Python Debugging

**Available Configurations:**

1. **Python: Current File** (F5)
   - Debug the currently open Python file
   - Use breakpoints by clicking in the gutter

2. **Python: Agent Sample**
   - Debug a specific agent sample
   - Will prompt for folder and filename

3. **Python: Pytest Current File**
   - Debug tests in the current file
   - Stops at test failures automatically

4. **Python: Pytest All Tests**
   - Debug entire test suite
   - Includes coverage reporting

5. **Python: Remote Attach**
   - Attach to a running Python process
   - Useful for Docker containers

**Debugging Tips:**
- Set breakpoints: Click in the left gutter next to line numbers
- Inspect variables: Hover over variables or use the Variables panel
- Use Debug Console: Execute Python commands in the current context
- Step through code: F10 (step over), F11 (step into), Shift+F11 (step out)

### .NET Debugging

**Available Configurations:**

1. **.NET: Launch Current Project**
   - Debug a .NET project
   - Will prompt for project name

2. **.NET: Attach to Process**
   - Attach to a running .NET process
   - Select from process picker

3. **.NET: Agent Sample - Azure OpenAI**
   - Pre-configured sample debugger

**Debugging Tips:**
- Breakpoints work the same as Python
- Use Immediate Window: Debug Console → Execute C# expressions
- Hot Reload: Edit code while debugging (limited scenarios)

---

## ⚙️ Workspace Settings

### Python Configuration

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/python/.venv/bin/python",
  "python.analysis.typeCheckingMode": "strict",
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports.ruff": "always",
      "source.fixAll.ruff": "always"
    }
  }
}
```

**What This Does:**
- Uses the virtual environment interpreter automatically
- Enables strict type checking (catches more errors)
- Auto-formats on save with Ruff
- Auto-fixes linting issues on save
- Auto-organizes imports on save

### .NET Configuration

```json
{
  "dotnet.defaultSolution": "dotnet/agent-framework-dotnet.slnx",
  "[csharp]": {
    "editor.defaultFormatter": "ms-dotnettools.csharp",
    "editor.formatOnSave": true
  }
}
```

**What This Does:**
- Loads the correct solution file
- Auto-formats C# code on save
- Uses .editorconfig rules

---

## 🧪 Testing

### Running Tests

**Via Command Palette** (Ctrl+Shift+P):
1. `Tasks: Run Task` → `Python: Run Tests`
2. `Tasks: Run Task` → `.NET: Run Tests`

**Via Test Explorer**:
1. Click the beaker icon in the left sidebar
2. Click "Run All Tests" or individual tests
3. View results inline with code

**Via Terminal**:
```bash
# Python tests
cd python && pytest --cov --cov-report=html -v

# .NET tests
dotnet test dotnet/agent-framework-dotnet.slnx
```

### Test Coverage

**Python Coverage:**
- HTML Report: `python/htmlcov/index.html`
- Terminal: Shown after test run
- Threshold: 85% required (configured in pyproject.toml)

**.NET Coverage:**
- Results in: `./coverage/`
- View with Coverage Gutters extension

---

## 🔍 Code Navigation

### Quick Navigation Shortcuts

| Action | Shortcut | Description |
|--------|----------|-------------|
| Go to File | **Ctrl+P** | Quick file search |
| Go to Symbol | **Ctrl+Shift+O** | Navigate to functions/classes in file |
| Go to Symbol in Workspace | **Ctrl+T** | Search all symbols in workspace |
| Go to Definition | **F12** | Jump to definition |
| Peek Definition | **Alt+F12** | Preview definition inline |
| Go to References | **Shift+F12** | Find all references |
| Go to Implementation | **Ctrl+F12** | Jump to implementation |

### Breadcrumbs

Enable breadcrumbs for easy navigation:
- View → Show Breadcrumbs
- Click any breadcrumb to navigate

---

## 🎨 Customization

### Workspace Folders

The workspace uses **named folders** with emojis for easy identification:

```json
{
  "folders": [
    {
      "name": "🏠 Root - Agent Framework",
      "path": "."
    },
    // ... more folders
  ]
}
```

**To Add a New Folder:**
1. Edit `microsoft-agent-framework.code-workspace`
2. Add to the `folders` array
3. Reload window (Ctrl+Shift+P → Reload Window)

### Custom Tasks

**To Add a Custom Task:**
1. Edit `.vscode/tasks.json`
2. Add your task configuration
3. Use: Ctrl+Shift+P → Tasks: Run Task

**Example Custom Task:**
```json
{
  "label": "My Custom Task",
  "type": "shell",
  "command": "echo Hello",
  "group": "build",
  "presentation": {
    "reveal": "always"
  }
}
```

---

## 🔐 Security Features

### Secret Detection

Pre-commit hooks automatically scan for secrets:
- **detect-secrets**: Scans all staged files
- Blocks commits containing secrets
- Baseline: `.secrets.baseline`

**If False Positive:**
```bash
# Update baseline (review carefully first!)
detect-secrets scan --baseline .secrets.baseline
```

### Security Scanning

Run security scans before commits:
```bash
# All scans
Tasks: Run Task → "Security: Run All Scans"

# Individual scans
Tasks: Run Task → "Security: Run Bandit"
Tasks: Run Task → "Security: Run Semgrep"
```

---

## 📊 Integrated Tools

### GitLens

**Features Enabled:**
- Code lens (inline blame)
- Current line blame
- File/Line history
- Commit search

**Quick Access:**
- View → Open View → GitLens

### TODO Tree

Highlights TODO comments in your code:

```python
# TODO: Implement this feature
# FIXME: Bug in this function
# SECURITY: Review this for vulnerabilities
# COMPLIANCE: CMMC control AC.1.001
# CMMC: NIST 800-171 requirement
```

**View TODOs:**
- Click TODO Tree icon in sidebar
- Or: View → Open View → TODO Tree

### Error Lens

Displays errors inline next to code (no need to hover):
- **Red**: Errors
- **Yellow**: Warnings
- **Blue**: Info

---

## 🚦 Status Bar

The VS Code status bar shows:
- **Python Interpreter**: Click to change
- **Git Branch**: Click to switch branches
- **Errors/Warnings**: Click to view Problems panel
- **Line/Column**: Current cursor position
- **Indentation**: Tab size (click to change)
- **Encoding**: File encoding (UTF-8)
- **EOL**: Line ending (LF)

---

## 🔧 Troubleshooting

### Python Issues

**Problem**: "No module named 'agent_framework'"
**Solution**: Ensure virtual environment is activated
```bash
cd python
source .venv/bin/activate
uv pip install -e .[all]
```

**Problem**: MyPy/Pyright errors
**Solution**: Install type stubs
```bash
pip install types-requests types-PyYAML
```

**Problem**: Tests not discovered
**Solution**: Check Python interpreter
- Click Python version in status bar
- Select: `Python 3.x.x ('.venv': venv)`

### .NET Issues

**Problem**: "Cannot find solution file"
**Solution**: Set default solution
```bash
# In .vscode/settings.json
"dotnet.defaultSolution": "dotnet/agent-framework-dotnet.slnx"
```

**Problem**: IntelliSense not working
**Solution**: Reload window
- Ctrl+Shift+P → Developer: Reload Window

### Git Issues

**Problem**: Pre-commit hooks not running
**Solution**: Reinstall hooks
```bash
pre-commit install
pre-commit install --hook-type commit-msg
```

---

## 📖 Additional Resources

### Workspace Files

- **Workspace**: [`microsoft-agent-framework.code-workspace`](microsoft-agent-framework.code-workspace)
- **Settings**: [`.vscode/settings.json`](.vscode/settings.json)
- **Tasks**: [`.vscode/tasks.json`](.vscode/tasks.json)
- **Launch**: [`.vscode/launch.json`](.vscode/launch.json)
- **Extensions**: [`.vscode/extensions.json`](.vscode/extensions.json)

### Documentation

- **Setup Guide**: [SETUP_COMPLETE.md](SETUP_COMPLETE.md)
- **Aurelius README**: [README.aurelius.md](README.aurelius.md)
- **PRD**: [.aurelius/PRD.md](.aurelius/PRD.md)
- **Architecture**: [.aurelius/ARCHITECTURE.md](.aurelius/ARCHITECTURE.md)
- **Development Standards**: [.aurelius/CLAUDE.md](.aurelius/CLAUDE.md)

### External Links

- [Microsoft Agent Framework Docs](https://learn.microsoft.com/agent-framework/)
- [Python Samples](python/samples/getting_started/)
- [.NET Samples](dotnet/samples/GettingStarted/)
- [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial)
- [VS Code C# Tutorial](https://code.visualstudio.com/docs/languages/csharp)

---

## 💡 Pro Tips

1. **Multi-Cursor Editing**: Alt+Click or Ctrl+Alt+Up/Down
2. **Command Palette**: Ctrl+Shift+P (access everything)
3. **Zen Mode**: View → Appearance → Zen Mode (distraction-free)
4. **Split Editor**: Ctrl+\\ (work on multiple files)
5. **Integrated Terminal**: Ctrl+` (toggle terminal)
6. **Quick Open**: Ctrl+P (navigate files instantly)
7. **Search in Files**: Ctrl+Shift+F (project-wide search)
8. **Replace in Files**: Ctrl+Shift+H (project-wide replace)
9. **Git Integration**: Source Control icon in sidebar
10. **Keyboard Shortcuts**: Ctrl+K Ctrl+S (view/customize)

---

## 🤝 Support

**Internal Support:**
- #agent-framework-dev (Slack)
- #agent-framework-security (Slack)
- #agent-framework-compliance (Slack)

**External Support:**
- technical-support@aureliustech.com
- security@aureliustech.com

---

## 🎉 You're Ready!

Your workspace is fully configured with:

✅ Multi-project organization
✅ Python & .NET development
✅ Integrated debugging
✅ Automated testing
✅ Security scanning
✅ Compliance tools
✅ Git integration
✅ Tasks automation

**Start developing with confidence!**

---

**Document Control**
- Classification: Unclassified // Technical
- Distribution: Aurelius Internal
- Owner: Aurelius Microsoft Agent Framework Team
- Last Updated: 2025-10-13
