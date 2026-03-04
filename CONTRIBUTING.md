# Contributing to zigporter

Thanks for your interest in contributing! Bug reports, feature requests, and pull requests are all welcome.

## Reporting Issues

Open an [issue](https://github.com/nordstad/zigporter/issues) and include:

- zigporter version (`zigporter --version`)
- Home Assistant OS, Supervisor, and Zigbee2MQTT versions
- What you expected vs. what happened
- Relevant CLI output or error messages

## Development Setup

```bash
git clone https://github.com/nordstad/zigporter.git
cd zigporter
uv sync --dev
```

## Making Changes

```bash
# Run tests
uv run pytest

# Lint and format (scope to changed files to avoid noisy diffs)
uv run ruff check src/zigporter/<file>.py tests/<file>.py
uv run ruff format src/zigporter/<file>.py tests/<file>.py
```

All async methods on `HAClient` that are called from commands need a corresponding `AsyncMock`
in the relevant test fixtures — see `tests/commands/test_migrate.py` (`mock_ha_client`) and
`tests/commands/test_rename.py` (`mock_device_exec_client`).

## Submitting a Pull Request

1. Fork the repo and create a branch from `main`
2. Make your changes with tests
3. Ensure `uv run pytest` and `uv run ruff check .` pass
4. Open a PR against `main` with a clear description of what changed and why

## Code Style

- Python 3.12+; use built-in generics (`list[str]`, `dict[str, int]`) — never `from typing import List, Dict`
- All I/O is async (`asyncio` / `httpx` / `websockets`)
- Pydantic v2 models for structured data
- Line length: 100 characters (enforced by ruff)

## License

By contributing you agree that your contributions will be licensed under the [MIT License](LICENSE).
