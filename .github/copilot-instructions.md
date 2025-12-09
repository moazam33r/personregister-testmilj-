# Copilot / AI Agent Instructions for personregister-testmilj-

Purpose
- Provide targeted, actionable guidance for AI coding agents working in this repository.

Big picture
- Single small Python application in `app.py`. It's a CLI-style script (not a web service).
- Data persistence: SQLite file, default path `/data/test_users.db`. The path can be overridden with the `DATABASE_PATH` environment variable.
- Containerization: `dockerfile` builds an image using `python:3.10-slim` and runs `app.py` as a non-root `appuser`. `docker-compose.yml` defines a single `app` service and a named volume `dbdata` mounted at `/data`.

Key files (start here)
- `app.py` — core logic: DB helpers (`get_db_path`, `open_conn`), DB lifecycle (`init_db`), and operations (`get_all_users`, `display_users`, `anonymize_users`, `clear_users`).
- `dockerfile` — base image, non-root user creation, volume path `/data`, default `CMD ["python","app.py"]`.
- `docker-compose.yml` — how the project runs in Docker. Environment variable `DATABASE_PATH=/data/test_users.db` and persistent volume `dbdata` are important.

Developer workflows (explicit commands)
- Run locally (simple):
  - `python app.py` — initializes DB (if missing) and prints users.
- Run one-off functions locally (useful for CI/dev):
  - `python -c "from app import anonymize_users; print(anonymize_users())"`
  - `python -c "from app import get_all_users; print(get_all_users())"`
- Run in Docker:
  - Build & run: `docker-compose up --build`
  - Run a single command inside the container: `docker-compose run --rm app python -c "from app import get_all_users; print(get_all_users())"`
- Inspect the SQLite DB (inside container):
  - `docker-compose run --rm app sh -c "sqlite3 /data/test_users.db '.tables'"`
  - Or map the volume to a host path and open with `sqlite3` locally.

Project-specific conventions & patterns
- Logging: `logging` is used across the app instead of `print()` — keep adding log messages, follow existing level usage (INFO by default).
- No side effects on import: `app.py`'s main block runs only when executed as a script. When writing code, keep functions import-safe so tests/agents can import and call them directly.
- Small, function-based design: prefer adding standalone functions (like the existing ones) rather than global script-level work.
- DB access: uses `sqlite3.connect()` via `open_conn()` and relies on `rowcount` for affected rows. Keep transactions explicit (commit where needed) and use `with open_conn() as conn` to ensure closure.

Adding dependencies
- If you add external packages, create `requirements.txt` and update the `dockerfile` to install them:
  - Add `COPY requirements.txt .` and `RUN pip install -r requirements.txt` before switching to `USER appuser`.

Tests & debugging notes (discoverable from repo)
- There are no tests present. Create `tests/` with pytest and call functions directly (they are import-safe): e.g., `from app import init_db, get_all_users`.
- For CI, set `DATABASE_PATH` to a temporary file and remove it after tests to avoid touching the Docker volume.
- To increase logging for debugging, set `logging.basicConfig(level=logging.DEBUG)` or modify the call site when running.

Integration points & important environment detail
- `DATABASE_PATH` environment variable controls where SQLite file is located. In Docker it's set to `/data/test_users.db` and backed by the `dbdata` volume in `docker-compose.yml`.

Examples agents should follow when editing code
- To add a new DB operation: add a function in `app.py` that uses `open_conn()` and returns data structures (prefer dicts for testability). Example pattern: `get_all_users()` → returns `List[dict]`.
- When making CLI changes, keep the `if __name__ == "__main__":` block minimal and import-safe.

Notes about merging or updating
- No existing `.github/copilot-instructions.md` or AGENT files were found; this file is the starting point. If you find other agent docs later, merge their concrete, repo-specific examples into this file (preserve commands, env vars, and DB/volume notes).

If anything here is unclear or you want additional sections (e.g., recommended tests, example CI job, or how to expose metrics), tell me which areas to expand.
