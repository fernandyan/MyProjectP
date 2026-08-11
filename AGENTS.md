# AGENTS.md

Flask portfolio app (dark mode) with SQLAlchemy + Flask-WTF + Flask-Login, a Stripe Checkout store, and python-dotenv-driven config. Windows / PowerShell; Python lives in a repo-local `venv/`.

## Commands

```powershell
# Install deps (after fresh clone) — fills venv from requirements.txt
.\venv\Scripts\pip install -r requirements.txt

# Configure env first: Copy-Item .env.example .env, then set your STRIPE keys.
# Seed DB first: creates tables, admin user, and sample data (incl. produtos)
.\venv\Scripts\python seed.py

# Run dev server (debug=True)
.\venv\Scripts\python app.py

# Run tests (pytest; isolated in-memory DB, does NOT touch instance/portfolio.db)
.\venv\Scripts\python -m pytest tests -v

# Focused: one file, or one test
.\venv\Scripts\python -m pytest tests/test_loja.py -v
.\venv\Scripts\python -m pytest "tests/test_blog_flow.py::test_usuario_exclui_proprio_post" -v
```

No lint or formatter is configured. Tests live in `tests/` (pytest, isolated in-memory DB via `tests/conftest.py`) — run them with `.\venv\Scripts\python -m pytest tests -v`. POSTs need a `csrf_token` scraped from the form HTML because Flask-WTF CSRF is enabled (`tests/conftest.py` has `_csrf`/`csrf_para` helpers for that).

User-facing install/setup docs live in `README.md` — point users there instead of re-explaining setup.

## Architecture

- `app.py` — entrypoint. `load_dotenv()` then app config from `.env` (with dev fallbacks): `SECRET_KEY`, `SQLALCHEMY_DATABASE_URI`, `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY`, `BASE_URL`. Sets `stripe.api_key`. Extension init (`db`, `login_manager`), `user_loader`, the `inject_year` context processor, and blueprint registration. No routes live here.
- `blueprints/main.py` — `main_bp`: public routes `/`, `/contato`. Holds the hardcoded `perfil`, `habilidades`, `contato_info` dicts (`contato_info` is passed to templates as `contato`). `perfil` is imported by `app.py` for the context processor.
- `blueprints/auth.py` — `auth_bp`: `/registro`, `/login`, `/logout`. `login_manager.login_view` is `"auth.login"`.
- `blueprints/blog.py` — `blog_bp` (url_prefix `/blog`): list, `/blog/<id>`, user blog CRUD (`/blog/novo`, `/blog/<id>/editar`, `/blog/<id>/excluir`, `@login_required` + `_pode_gerenciar_post()` ownership check).
- `blueprints/loja.py` — `loja_bp`: `/loja` (product list from DB, only `disponivel=True`, passes `publishable_key` to the template), `POST /loja/checkout/<id>` (creates a Stripe Checkout Session with `mode="payment"` and `price_data.currency="usd"`, redirects 303 to `session.url`), `/loja/sucesso`, `/loja/cancelado`. No webhook — orders are not persisted. `success_url`/`cancel_url` built from `BASE_URL` config.
- `blueprints/admin.py` — `admin_bp` (url_prefix `/admin`): dashboard + CRUD (`@admin_required`), plus `admin_required`, `CAMPOS_ITEM`, `_processar_item()`, `_excluir_item()`.
- `models.py` — defines the shared `db` instance; models `User` (with `email`, `is_admin`), `Projeto`, `Experiencia`, `Educacao`, `Post` (with `author_id` FK to users), `Mensagem`, `Produto` (with `preco_centavos` in USD cents and `preco_usd` property, `disponivel` boolean).
- `forms.py` — WTForms form classes (one per model + login/registro/contato).
- `seed.py` — `db.create_all()` + admin user (`admin` / `admin123`) + sample portfolio data (incl. sample products). Must run before first boot. Note: `app.py` also calls `db.create_all()` at startup, but that only creates empty/missing tables — no admin user, so you cannot log in without running `seed.py` once.
- `templates/` — all pages extend `base.html`. Admin forms reuse the generic `admin/item_form.html`. `url_for()` in templates must use blueprint-prefixed endpoints (`main.index`, `auth.login`, `blog.blog_novo`, `loja.loja`, `admin.produto_editar`, …).

## Gotchas

- DB is SQLite at `instance/portfolio.db` (URI `sqlite:///portfolio.db`). Schema is created via `db.create_all()` only — there are NO migrations. Adding/renaming a column requires deleting `instance/portfolio.db` and re-running `seed.py`.
- `base.html` title/nav use `perfil.nome`. `perfil`, `habilidades`, `contato_info` are hardcoded in `blueprints/main.py`; only `perfil` is available to every template (via the `inject_year` context processor in `app.py`, which injects `current_year`, `perfil` AND `csrf_token`). `habilidades` and `contato` are passed explicitly by `main.index`/`main.contato`. Portfolio items (projetos/experiencias/educacao/mensagens) come from the DB.
- Admin CRUD is DRY via `_processar_item()` / `_excluir_item()` in `blueprints/admin.py`. New fields must be added to the `CAMPOS_ITEM` list or they won't be persisted. New admin entities should follow this pattern. `_processar_item()` sets `author=current_user` on new `Post` rows (author_id is NOT nullable). Unlike blog delete (POST+CSRF), admin `*_excluir` routes are plain GET links (tests expect this).
- `Projeto.tecnologias` is a comma-separated string; use the `tecnologias_lista` property in templates, not `split` inline.
- `Post` requires `author_id` (FK to `users`). Regular logged-in users manage only their own posts (see `_pode_gerenciar_post()`); admins manage all. Blog delete is POST-only with CSRF.
- `csrf_token()` is exposed to templates via the `inject_year` context processor — needed for plain (non-WTForms) POST forms like the blog delete button.
- `SECRET_KEY` is a hardcoded dev value — do not use in production as-is.
- `.gitignore` excludes `venv/`, `__pycache__/`, `instance/` (so `portfolio.db` is not committed) and `.env`; `.env.example` IS committed.
- Config comes from `.env` (loaded via `load_dotenv()` in `app.py`) with dev fallbacks. Tests don't read `.env` — `tests/conftest.py` builds a fresh app with hardcoded config.
- `Produto.preco_centavos` is an integer in USD cents (e.g. `2990` = US$ 29.90). Use the `preco_usd` property in templates, not division inline.
- No webhook: orders are not persisted. `loja.checkout` catches `stripe.error.StripeError`; `success_url`/`cancel_url` come from the `BASE_URL` config. Local testing with Stripe test keys (`sk_test_...`) uses the card `4242 4242 4242 4242`.
- Tests mock `stripe.checkout.Session.create` via monkeypatch — never call the real Stripe API in tests.
