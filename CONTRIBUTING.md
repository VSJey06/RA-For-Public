# Contributing to RA Language

Thank you for your interest in contributing to RA Language! This document outlines the process for contributing to the project.

## How to Report Bugs

1. **Search existing issues** — check if the bug has already been reported.
2. **Open a new issue** — use the bug report template and include:
   - A clear, descriptive title
   - Steps to reproduce the issue
   - Expected vs. actual behavior
   - Environment details (OS, Python version, RA version)
   - Code snippets or test cases if applicable

## How to Suggest Features

1. **Search existing issues** — check if the feature has already been suggested.
2. **Open a new issue** — use the feature request template and include:
   - A clear, descriptive title
   - Detailed description of the proposed feature
   - Use cases and benefits
   - Any potential implementation ideas

## Development Setup

- **Python 3.14+** is required.
- Clone the repository:
  ```
  git clone https://github.com/RA-Language/RA.lang.git
  cd RA.lang
  ```
- Install development dependencies:
  ```
  pip install -e ".[dev]"
  ```
- Verify your setup by running the test suite:
  ```
  python run_verification.py
  ```

## Pull Request Process

1. **Fork the repository** and create a feature branch from `main`.
2. **Write tests** for any new functionality or bug fixes.
3. **Ensure all tests pass** before submitting.
4. **Keep pull requests focused** — one feature or fix per PR.
5. **Update documentation** if your changes affect the public API or behavior.
6. **Write a clear PR description** explaining what the change does and why.
7. Your PR will be reviewed by maintainers. Address any feedback promptly.

## Coding Standards

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code.
- Use type hints for all function signatures.
- Write clear, self-documenting code. Avoid unnecessary comments.
- Keep functions and methods focused on a single responsibility.
- Use meaningful variable and function names.

## Testing Requirements

- All new code must include tests.
- Run the full test suite before submitting:
  ```
  python run_verification.py
  ```
- Maintain or improve code coverage.
- Tests should be deterministic and not depend on external services.

## Community Guidelines

- Be respectful and inclusive in all interactions.
- Provide constructive feedback when reviewing others' work.
- Ask questions if something is unclear — we are all here to learn.
- Follow the [Code of Conduct](CODE_OF_CONDUCT.md) in all project spaces.

## License

By contributing to RA Language, you agree that your contributions will be licensed under the [MIT License](LICENSE).

---

Thank you for contributing to RA Language!
