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

# Run tests (pytest; isolated in-memory DB, does NOT touch instance/portfolio.db)
.\venv\Scripts\python -m pytest tests -v
```

No tests, lint, or formatter are configured. Verify changes with Flask's test client; POSTs need a `csrf_token` scraped from the form HTML because Flask-WTF CSRF is enabled.

User-facing install/setup docs live in `README.md` — point users there instead of re-explaining setup.

## Architecture

- `app.py` — entrypoint. App config, extension init (`db`, `login_manager`), `user_loader`, the `inject_year` context processor, and blueprint registration. No routes live here.
- `blueprints/main.py` — `main_bp`: public routes `/`, `/contato`. Holds the hardcoded `perfil`, `habilidades`, `contato_info` dicts (`contato_info` is passed to templates as `contato` — don't name a route `contato` after the dict, it shadows it).
- `blueprints/auth.py` — `auth_bp`: `/registro`, `/login`, `/logout`. `login_manager.login_view` is `"auth.login"`.
- `blueprints/blog.py` — `blog_bp` (url_prefix `/blog`): list, `/blog/<id>`, user blog CRUD (`/blog/novo`, `/blog/<id>/editar`, `/blog/<id>/excluir`, `@login_required` + `_pode_gerenciar_post()` ownership check).
- `blueprints/admin.py` — `admin_bp` (url_prefix `/admin`): dashboard + CRUD (`@admin_required`), plus `admin_required`, `CAMPOS_ITEM`, `_processar_item()`, `_excluir_item()`.
- `models.py` — defines the shared `db` instance; models `User` (with `email`, `is_admin`), `Projeto`, `Experiencia`, `Educacao`, `Post` (with `author_id` FK to users), `Mensagem`.
- `forms.py` — WTForms form classes (one per model + login/registro/contato).
- `seed.py` — `db.create_all()` + admin user (`admin` / `admin123`) + sample portfolio data. Must run before first boot. Note: `app.py` also calls `db.create_all()` at startup, but that only creates empty tables — no admin user, so you cannot log in without running `seed.py` once.
- `templates/` — all pages extend `base.html`. Admin forms reuse the generic `admin/item_form.html`. `url_for()` in templates must use blueprint-prefixed endpoints (`main.index`, `auth.login`, `blog.blog_novo`, `admin.projeto_editar`, …).

## Gotchas

- DB is SQLite at `instance/portfolio.db` (URI `sqlite:///portfolio.db`). Schema is created via `db.create_all()` only — there are NO migrations. Adding/renaming a column requires deleting `instance/portfolio.db` and re-running `seed.py`.
- `base.html` title/nav use `perfil.nome`; `perfil`, `habilidades`, `contato` are hardcoded dicts in `blueprints/main.py`, made available to every template via the `inject_year` context processor in `app.py` (injects `current_year`, `perfil` AND `csrf_token`). Portfolio items (projetos/experiencias/educacao/mensagens) come from the DB.
- Admin CRUD is DRY via `_processar_item()` / `_excluir_item()` in `blueprints/admin.py`. New fields must be added to the `CAMPOS_ITEM` list or they won't be persisted. New admin entities should follow this pattern. `_processar_item()` sets `author=current_user` on new `Post` rows (author_id is NOT nullable).
- `Projeto.tecnologias` is a comma-separated string; use the `tecnologias_lista` property in templates, not `split` inline.
- `Post` requires `author_id` (FK to `users`). Regular logged-in users manage only their own posts (see `_pode_gerenciar_post()`); admins manage all. Blog delete is POST-only with CSRF.
- `csrf_token()` is exposed to templates via the `inject_year` context processor — needed for plain (non-WTForms) POST forms like the blog delete button.
- `SECRET_KEY` is a hardcoded dev value — do not use in production as-is.
- `.gitignore` excludes `venv/`, `__pycache__/`, `instance/` (so `portfolio.db` is not committed).
