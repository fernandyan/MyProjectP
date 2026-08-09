# AGENTS.md

Flask portfolio app (dark mode) with SQLAlchemy + Flask-WTF + Flask-Login. Windows / PowerShell; Python lives in a repo-local `venv/`.

## Commands

```powershell
# Install deps (after fresh clone)
.\venv\Scripts\pip install -r requirements.txt

# Seed DB first: creates tables, admin user, and sample data
.\venv\Scripts\python seed.py

# Run dev server (debug=True)
.\venv\Scripts\python app.py
```

No tests, lint, or formatter are configured. Verify changes with Flask's test client; POSTs need a `csrf_token` scraped from the form HTML because Flask-WTF CSRF is enabled.

## Architecture

- `app.py` — single entrypoint. App config, extension init (`db`, `login_manager`), ALL routes: public (`/`, `/contato`), auth (`/login`, `/logout`), admin CRUD (`/admin*`, `@login_required`).
- `models.py` — defines the shared `db` instance; models `User`, `Projeto`, `Experiencia`, `Educacao`, `Mensagem`.
- `forms.py` — WTForms form classes (one per model + login/contato).
- `seed.py` — `db.create_all()` + admin user (`admin` / `admin123`) + sample portfolio data. Must run before first boot.
- `templates/` — all pages extend `base.html`. Admin forms reuse the generic `admin/item_form.html`.

## Gotchas

- DB is SQLite at `instance/portfolio.db` (URI `sqlite:///portfolio.db`). Schema is created via `db.create_all()` only — there are NO migrations. Adding/renaming a column requires deleting `instance/portfolio.db` and re-running `seed.py`.
- `base.html` title/nav use `perfil.nome`; `perfil`, `habilidades`, `contato` are hardcoded dicts in `app.py`, made available to every template via the `inject_year` context processor (injects `current_year` AND `perfil`). Portfolio items (projetos/experiencias/educacao/mensagens) come from the DB.
- Admin CRUD is DRY via `_processar_item()` / `_excluir_item()` in `app.py`. New fields must be added to the `CAMPOS_ITEM` list or they won't be persisted. New admin entities should follow this pattern.
- `Projeto.tecnologias` is a comma-separated string; use the `tecnologias_lista` property in templates, not `split` inline.
- `SECRET_KEY` is a hardcoded dev value — do not use in production as-is.
- `.gitignore` excludes `venv/`, `__pycache__/`, `instance/` (so `portfolio.db` is not committed).
