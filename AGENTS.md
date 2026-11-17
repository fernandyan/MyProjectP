# AGENTS.md

Flask portfolio app (dark mode) with SQLAlchemy + Flask-WTF + Flask-Login, a Stripe Checkout store, a scikit-learn "mental health" predictor, and python-dotenv config. Windows / PowerShell; Python lives in the repo-local `venv/`.

## Commands

Run from the repo root (the ML route loads `classificador.pkl` with a CWD-relative path).

```powershell
# Install deps
.\venv\Scripts\pip install -r requirements.txt

# Env + DB (both required before first boot)
Copy-Item .env.example .env   # then set STRIPE keys
.\venv\Scripts\python seed.py # tables + admin user + sample data

# Dev server (debug=True, http://127.0.0.1:5000)
.\venv\Scripts\python app.py

# Tests (in-memory DB via tests/conftest.py; does NOT touch instance/portfolio.db)
.\venv\Scripts\python -m pytest tests -q

# Focused
.\venv\Scripts\python -m pytest tests/test_loja.py -v
.\venv\Scripts\python -m pytest "tests/test_blog_flow.py::test_usuario_exclui_proprio_post" -v
```

No lint, formatter, typecheck, or CI is configured. Current suite: 33 tests.

User-facing setup docs are in `README.md`; point users there instead of restating setup.

## Architecture

- `app.py` — entrypoint. `load_dotenv()`, then config from `.env` with fallbacks: `SECRET_KEY`, `SQLALCHEMY_DATABASE_URI`, `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY`, `BASE_URL`. Sets `stripe.api_key`, inits `db` + `login_manager`, defines `user_loader`, registers blueprints. `db.create_all()` runs only inside `if __name__ == "__main__"` (so importing app does not create tables; `seed.py` calls it itself).
- Context processor `inject_year` makes `current_year`, `perfil`, and `csrf_token` available to every template. `perfil` (and the hardcoded `habilidades` / `contato_info`) live in `blueprints/main.py`.
- `blueprints/main.py` — `main_bp`: `/`, `/contato`, `/data` (hub page), `/data_science_mental` (endpoint `main.data_science_metal`, a deliberate typo used by `data/data.html`), and `/student_depression`.
- `blueprints/auth.py` — `/registro`, `/login`, `/logout`; `login_manager.login_view = "auth.login"`.
- `blueprints/blog.py` — `blog_bp` (`/blog`): list/detail + own-post CRUD; ownership via `_pode_gerenciar_post()` (admins can manage all).
- `blueprints/loja.py` — `loja_bp`: `/loja`, `POST /loja/checkout/<id>` (Stripe Session `mode="payment"`, `currency="usd"`, 303 redirect), `/loja/sucesso`, `/loja/cancelado`. No webhook; orders are not persisted.
- `blueprints/admin.py` — `admin_bp` (`/admin`): dashboard + CRUD behind `@admin_required`; DRY helpers `CAMPOS_ITEM`, `_processar_item()`, `_excluir_item()`.
- `models.py` — shared `db`; `User`, `Projeto`, `Experiencia`, `Educacao`, `Post`, `Mensagem`, `Produto`.
- `forms.py` — WTForms classes (one per model + login/registro/contato) plus the lowercase `data_science_mental` form.
- `seed.py` — `db.create_all()` + admin (`admin` / `admin123`) + sample data. Without it there is no admin user.
- `templates/` — all pages extend `base.html`; admin forms reuse `admin/item_form.html`. Always use blueprint-prefixed endpoints in `url_for`.

## Data Science routes

- `forms.py::data_science_mental` (~23 fields) and `DepressionForm` feed `classificador.pkl` / `student_depression01.pkl`. Field names and posted values must match the pickled model's expected columns.
- `main.data_science_metal` and `main.student_depression` load the pickles with `joblib.load` (CWD-relative, committed at repo root), build a one-row DataFrame, then call `predict()` and `predict_proba()`.
- Results render directly on POST (no session/redirect, so F5 re-submits) into `templates/data/data_science_mental_result.html` and `depression_result.html`: status, confidence, class distribution, curated summary + all answers, and disclaimers. `_calcular_probabilidades()` hides the probability UI if a model lacks `predict_proba`.
- Shared result markup lives in `templates/data/_result_components.html` (Jinja macros).
- Covered by `tests/test_data_science.py`, which monkeypatches `blueprints.main.joblib.load` with fake models (no real pickle or Stripe calls).

## Frontend / theming

- Two styling systems coexist: `static/css/style.css` uses CSS variables toggled by `[data-theme]`, while `templates/index.html` and `templates/data*.html` use Tailwind CDN utilities (`dark:` variants) plus `.theme-page` for the page background.
- `base.html` loads Tailwind with `darkMode: 'class'`; the theme toggle stores `theme` in `localStorage` (default `dark`) and sets both `data-theme` and the `.dark` class.
- `style.css` needs `body .container { max-width: 1080px }` because Tailwind's `.container` loads later and otherwise changes the navbar width between pages. Keep it.
- New Tailwind pages must supply both light and `dark:` classes; new CSS-variable pages should use the existing vars.

## Gotchas

- DB is SQLite at `instance/portfolio.db`. Schema comes only from `db.create_all()` — there are no migrations. Changing a column requires deleting the DB and re-running `seed.py`.
- Admin fields must be listed in `CAMPOS_ITEM` or they will not be persisted. `_processar_item()` repopulates the form from the DB after an invalid POST, overwriting submitted values — be aware if you touch validation/editing.
- Admin `*_excluir` routes are plain GET links with no CSRF; blog delete is POST-only with CSRF (a GET to `/blog/<id>/excluir` must return 405).
- `Post.author_id` is non-nullable; admin-created posts set `author_id = current_user.id` (not `author = current_user`).
- `Projeto.tecnologias` is a comma-separated string — use the `tecnologias_lista` property. `Produto.preco_centavos` is USD cents — use the `preco_usd` property.
- CSRF is enabled everywhere. Tests scrape tokens with `conftest._csrf` / `csrf_para(client, path)` and log in with `conftest.login`.
- Tests build their own app in `tests/conftest.py` (hardcoded config, in-memory SQLite) and never import `app.py`, so `.env` is irrelevant to tests. Stripe is monkeypatched via `stripe.checkout.Session.create`; never call the real API in tests.
- `.gitignore` excludes `venv/`, `instance/`, `.env`; `.env.example` and `classificador.pkl` are committed.
- `SECRET_KEY` and Stripe keys come from `.env`; the app has insecure dev fallbacks, so don't ship them.
