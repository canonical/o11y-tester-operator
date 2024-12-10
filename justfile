# set quiet  # Recipes are silent by default
set export  # Just variables are exported to the environment

uv := `which uv`  # require `uv`

# Setup variables
project := invocation_directory()
src := project + "/src"
tests := project + "/tests"
PYTHONPATH := project + ":" + src + ":" + tests
PY_COLORS := "1"
uv_flags := "--frozen --isolated --extra=dev -q"

[private]
default:
  just --list

# Update uv.lock with the latest deps
lock:
  uv lock --upgrade --no-cache

# Generate requirements.txt from pyproject.toml
requirements:
  uv export --frozen --no-hashes --format=requirements-txt -o requirements.txt

# Lint the code
lint:
  uv run ${uv_flags} ruff check ${src} ${tests}
  uv run ${uv_flags} ruff check ${src} ${tests}

# Run static checks
static:
  uv run ${uv_flags} pyright

# Format the code
fmt:
  uv run ${uv_flags} ruff check --fix-only ${src} ${tests}
  uv run ${uv_flags} ruff format ${src} ${tests}

# Run unit tests
[positional-arguments]
unit *args="":
  uv run ${uv_flags} coverage run --source=${src} -m pytest ${tests}/unit "$@"
  uv run ${uv_flags} coverage report

# Run integration tests
[positional-arguments]
integration *args="":
  uv run ${uv_flags} pytest --exitfirst ${tests}/integration "$@"

