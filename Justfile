set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]
set dotenv-load := true

# Available recipes
_default:
    @just --list --unsorted --list-prefix "    > " --justfile {{justfile()}}


# 📦 Create a requirements.txt from pyproject.toml
export-requirements:
    @echo "Exporting requirements"
    uv pip compile pyproject.toml -o requirements.txt

# Run pre-commit hooks
pre-commit:
    @echo "Running pre-commit hooks"
    uv run pre-commit run --all-files