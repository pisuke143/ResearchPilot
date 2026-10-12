# ResearchPilot — Development Setup Guide

## 1. Purpose

This guide describes a repeatable development setup. Verify commands against
the actual repository and environment before treating the guide as final.

## 2. Requirements

- Windows and PowerShell for the current development setup
- Python version compatible with the project's dependencies
- Git
- VS Code
- A working internet connection for obtaining dependencies and model files when needed

## 3. Open the project

From PowerShell, navigate to the project root:

```powershell
Set-Location "C:\Users\debjg\Desktop\Debjyoti Ganguly\code\Projects\ResearchPilot"
```

Verify the project structure:

```powershell
Get-Location
Get-ChildItem
```

## 4. Activate the existing virtual environment

If the project environment is named `ResearchEnv`:

```powershell
.\ResearchEnv\Scripts\Activate.ps1
```

Verify Python:

```powershell
python --version
python -m pip --version
```

If script execution is blocked by PowerShell policy, follow your organization's
security guidance. Do not change system-wide security settings unnecessarily.

## 5. Dependency management

Inspect existing dependencies before installing anything:

```powershell
Get-ChildItem -Force
python -m pip list
```

Check whether the repository already contains a dependency file. If it does,
follow its documented installation instructions. If it does not, dependency
pinning should be added as a planned reproducibility task after the environment
has been audited.

Do not reinstall or upgrade all packages blindly in the existing environment.

## 6. Run tests

From the repository root:

```powershell
python -m unittest discover -s tests -v
```

Record failures rather than assuming all existing tests pass.

## 7. Inspect source files

```powershell
Get-ChildItem .\src\researchpilot
Get-ChildItem .\tests
```

Read files individually before modifying them.

## 8. Git status

Before and after documentation changes:

```powershell
git status --short
git diff -- README.md
git diff -- docs
```

New untracked files may not appear in `git diff` until they are staged. Use
`git status --short` to inspect them.

## 9. Documentation verification

Confirm the documentation files exist:

```powershell
Get-ChildItem .\docs
```

Check for unresolved planning decisions before implementing future components.

## 10. Troubleshooting

### Python command not found

Verify Python installation and PATH, or activate the project environment.

### Module import error

Confirm the virtual environment is active and the required package is installed.
Use the project's documented invocation method.

### Model download failure

Check network access, disk space, model identifier, and the model library's
cache configuration.

### FAISS or PyTorch installation error

Check Python version, operating system, and package compatibility. Avoid
randomly upgrading unrelated packages.

### Test failure

Capture the complete error, identify the failing test, and reproduce it before
changing application code.
