# Contributing

To contribute with code, follow the instructions below to enforce automatic syntax formatting and linting.
Configuration is taken from https://www.pre-commit.com/#2-add-a-pre-commit-configuration and from git-hooks.

*Note*: apply commands from the root of the repository.

```bash
# Required: install the pre-commit hooks
pip3 install pre-commit
pre-commit install

# Optional: manual trigger (to know how validation will be applied or to force it manually on files before/after commit)
pre-commit run --all-files

# Optional: to keep the pre-commit versions of validation up-to-date
pre-commit autoupdate

# Optional: to remove the pre-commit git-hook binding
pre-commit uninstall
```
