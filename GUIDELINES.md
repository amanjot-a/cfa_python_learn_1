# Project Guidelines — Detailed Reference

This document describes the repository layout, purpose of each file, setup and usage instructions, development workflow, coding standards, and contribution guidelines.

---

## 1. Project Overview

This repository contains a collection of small Python scripts, interactive calculators, exercises and learning materials used while studying CFA-related quantitative topics. The code has been organized into logical folders to make it easier to navigate.

Purpose: provide easily runnable examples (time-value-of-money calculators, interest examples), learning notebooks, and generated charts.

## 2. Repository Structure (what lives where)

- `src/` — Primary Python scripts and modules. These are the runnable examples and utilities.
- `notebooks/` — Jupyter notebooks for interactive learning and demonstration.
- `charts/` — Generated images and figures created by scripts (e.g., TVM chart images).
- `LICENSE` — Licensing information for the repository.
- `.gitignore` — Files and directories excluded from version control.
- `README.md` — Short overview and quick usage information.
- `GUIDELINES.md` — This file: detailed guidelines and development notes.

Files of interest (high-level descriptions):

- `src/tvm_calculator.py` — Interactive Time-Value-of-Money (TVM) calculator. Solves for PV/FV/N/I/PMT and (optionally) generates charts using `matplotlib`/`numpy`.
- `src/Professional_TVM.py` — Alternate or enhanced TVM utilities (kept for examples and reference).
- `src/CAPM.py` — Small example demonstrating Capital Asset Pricing Model computations.
- `src/SimpleINT.py` — Simple interest calculation examples.
- `src/module2.py` — Course exercise module (Module 2 examples).
- `src/Loops.py` and `src/Whileloops.py` — Loop examples used for learning iteration constructs.
- `src/Practise.py` — Sandbox/practice script (examples and ad-hoc code).
- `src/Start.py` — Entry or starter script for demonstrations.
- `notebooks/Variables Assignment, Math Ops and Data Types.ipynb` — Interactive notebook for learning variable assignment and basic data types.
- `charts/tvm_charts.png` — Example output image produced by `tvm_calculator.py` when plotting is enabled.

## 3. Recommended Environment & Dependencies

- Python: 3.8+ recommended (3.10/3.11 are fine). Use a virtual environment for development.

Example (Windows PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt   # optional if requirements.txt is present
```

Minimal dependencies to enable full functionality (charts & notebooks):

- numpy
- matplotlib
- jupyter (if you plan to open notebooks)

You can create a `requirements.txt` like:

```
numpy>=1.24
matplotlib>=3.6
jupyter>=1.0
```

Then install with `pip install -r requirements.txt`.

If you will not generate charts, the scripts will still run for numeric output (charting is optional and gracefully skipped when `matplotlib`/`numpy` are missing).

## 4. How to Run Key Files

- Run the interactive TVM calculator:

```powershell
python src/tvm_calculator.py
```

- Run any example script (from project root):

```powershell
python src/Start.py
python src/CAPM.py
```

- Open the notebook (Jupyter):

```powershell
jupyter notebook notebooks/Variables\ Assignment,\ Math\ Ops\ and\ Data\ Types.ipynb
```

Notes about running:
- Running `tvm_calculator.py` will prompt for inputs in the console. If `matplotlib`/`numpy` are installed, the script can optionally generate charts and save `charts/tvm_charts.png`.

## 5. File-by-File Details and Responsibilities

Each source file has a role. When you modify or add files, follow these rules:

- Keep interactive scripts self-contained: prompt/validate input and handle errors gracefully.
- Utility modules (pure computation) should expose functions which are easy to unit test.
- Large blocks of sample execution should be guarded by `if __name__ == "__main__":` so modules remain importable.

Suggested refactors (future work):

- Split computation logic (TVM math) into a small importable module (e.g., `src/tvm/math.py`) and keep `tvm_calculator.py` strictly as the CLI wrapper and plotting orchestrator.
- Add unit tests for core numerics (solve_i, solve_n, solve_pmt, etc.) using `pytest`.

## 6. Development Workflow

Branching and commits:

- Create small, focused branches per change: `feat/tvm-cli`, `fix/tvm-numeric`.
- Commit messages: use semantic prefixes: `feat:`, `fix:`, `chore:`, `docs:`.
- Before pushing, run a quick smoke test for changed scripts.

Pull requests:

- Describe intent and any manual testing performed.
- Link to expected behaviors or issue numbers.

Code review checklist:

- Does the change include tests or a test plan for numeric code?
- Are input validations and edge cases covered (zero rates, zero periods, negative contributions)?
- Are outputs formatted and documented for users?

## 7. Coding Standards

- Follow PEP 8 for style. Keep line lengths ~ 80–100 characters where reasonable.
- Prefer descriptive function and variable names; avoid single-letter names except in concise loops.
- Avoid side effects at import time; use `if __name__ == "__main__":` for scripts.

Type hints:

- Use Python type hints for public functions to improve readability and support static type checking (mypy) if added later.

Testing:

- Add a `tests/` directory for unit tests if you expand computation logic. Use `pytest`.

Example unit test target: validate `solve_fv`, `solve_pv`, `solve_pmt`, `solve_i`, and `solve_n` across typical inputs and edge cases.

## 8. Contribution Guidelines

- Open an issue to propose larger changes before implementing.
- For small fixes or improvements, submit a branch + PR with a clear description and sample usages.
- Keep PRs small and focused: separate formatting changes from functional changes.

## 9. Repo Maintenance Tasks

- Keep `README.md` up to date with major reorganizations or new usage instructions.
- Add `requirements.txt` if/when dependencies stabilize.
- Add CI (GitHub Actions) to run linters and tests for future reliability.

## 10. Security and Licensing

- Be cautious with dependencies: prefer pinned ranges in `requirements.txt` for reproducibility.
- License: follow the terms in `LICENSE`.

## 11. Contacts & Next Steps

If you want, I can also:

- Add a `requirements.txt` with recommended package versions.
- Create a minimal `src/__init__.py` and refactor `tvm_calculator.py` to import computation logic for easier testing.
- Add a `CONTRIBUTING.md` with pull request templates and issue templates.

Tell me which of these you'd like next and I'll implement it.
