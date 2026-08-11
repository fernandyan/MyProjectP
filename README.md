# Flask Portfolio

A modern dark-mode portfolio website built with Flask, featuring a public portfolio section, a contact form, a Stripe-powered online store, and a password-protected admin panel for managing projects, work experience, education, incoming messages, and store products.

## Features

- Public portfolio page with projects, work experience, education, skills, and contact links
- Contact form that saves messages to the database
- Online store with Stripe Checkout (products + payment pages)
- Admin authentication with Flask-Login
- Full admin CRUD for projects, experiences, education, and products
- Message inbox in the admin panel
- Environment-based configuration via `.env` (python-dotenv)
- Dark-mode UI with Bootstrap

## Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- Flask-WTF
- Flask-Login
- Stripe Checkout
- SQLite
- Bootstrap
- python-dotenv

## Prerequisites

- Python 3.9 or newer
- Git
- A Stripe account with test API keys (https://dashboard.stripe.com/test/apikeys)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/seu-usuario/flask-portfolio.git
cd flask-portfolio
```

2. Create and activate a virtual environment:

Windows (PowerShell):

```powershell
python -m venv venv
.\venv\Scripts\activate
```

macOS / Linux:

```bash
python -m venv venv
source venv/bin/activate
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

4. Configure the environment. Copy `.env.example` to `.env` and fill in your Stripe test keys:

Windows (PowerShell):

```powershell
Copy-Item .env.example .env
```

macOS / Linux:

```bash
cp .env.example .env
```

Then edit `.env` and set `STRIPE_SECRET_KEY` and `STRIPE_PUBLISHABLE_KEY` to your test keys.

5. Seed the database. This is required before the first boot — it creates the tables, the admin user, and sample portfolio data (including store products):

```bash
python seed.py
```

6. Start the development server:

```bash
python app.py
```

7. Open http://127.0.0.1:5000 in your browser. Products are listed at http://127.0.0.1:5000/loja.

## Online Store (Stripe Checkout)

- Manage products from the admin panel (Admin → Produtos). The price is stored in USD cents (e.g. `2990` = US$ 29.90).
- Only products marked as **disponível** appear in the store.
- Clicking **Comprar** creates a Stripe Checkout Session and redirects to Stripe's hosted payment page.
- After payment the user is redirected to `/loja/sucesso`; if they cancel, to `/loja/cancelado`.
- To test payments in Stripe's test mode, use the card `4242 4242 4242 4242` with any future expiry date and any CVC.
- `STRIPE_SECRET_KEY` and `STRIPE_PUBLISHABLE_KEY` must be test keys (`sk_test_...` / `pk_test_...`) for local development.

## Default Admin Credentials

| Username | Password |
|----------|----------|
| `admin`  | `admin123` |

> **Security note:** The `SECRET_KEY` in `app.py` is a hardcoded development fallback. In production, set a strong random value in `.env`. The default admin password should also be changed.

## Project Structure

```
├── app.py          # App entrypoint: loading of env vars and app config, blueprint registration
├── models.py       # SQLAlchemy models (User, Projeto, Experiencia, Educacao, Mensagem, Produto)
├── forms.py        # WTForms form classes
├── seed.py         # Database seeding: admin user + sample data
├── blueprints/     # main, auth, blog, loja (Stripe Checkout) e admin
├── requirements.txt
├── .env.example    # Template of environment variables (commit to GitHub)
└── templates/      # Jinja2 templates (base.html + page templates)
```

## Notes

- The database is SQLite at `instance/portfolio.db`. There are no migrations; changing the schema requires deleting the database and re-running `python seed.py`.
- `app.py` also runs `db.create_all()` on startup, which creates any missing tables (e.g. the new `produtos` table) without deleting existing data.
- Portfolio content is in Portuguese and stored in the database; edit it through the admin panel at http://127.0.0.1:5000/admin after logging in.
