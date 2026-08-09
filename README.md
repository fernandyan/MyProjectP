# Flask Portfolio

A modern dark-mode portfolio website built with Flask, featuring a public portfolio section, a contact form, and a password-protected admin panel for managing projects, work experience, education, and incoming messages.

## Features

- Public portfolio page with projects, work experience, education, skills, and contact links
- Contact form that saves messages to the database
- Admin authentication with Flask-Login
- Full admin CRUD for projects, experiences, and education
- Message inbox in the admin panel
- Dark-mode UI with Bootstrap

## Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- Flask-WTF
- Flask-Login
- SQLite
- Bootstrap

## Prerequisites

- Python 3.9 or newer
- Git

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

4. Seed the database. This is required before the first boot — it creates the tables, the admin user, and sample portfolio data:

```bash
python seed.py
```

5. Start the development server:

```bash
python app.py
```

6. Open http://127.0.0.1:5000 in your browser.

## Default Admin Credentials

| Username | Password |
|----------|----------|
| `admin`  | `admin123` |

> **Security note:** The `SECRET_KEY` in `app.py` is a hardcoded development value. Replace it with a strong random value before deploying to production, and change the default admin password.

## Project Structure

```
├── app.py          # App entrypoint: config, routes, admin CRUD helpers
├── models.py       # SQLAlchemy models (User, Projeto, Experiencia, Educacao, Mensagem)
├── forms.py        # WTForms form classes
├── seed.py         # Database seeding: admin user + sample data
├── requirements.txt
└── templates/      # Jinja2 templates (base.html + page templates)
```

## Notes

- The database is SQLite at `instance/portfolio.db`. There are no migrations; changing the schema requires deleting the database and re-running `python seed.py`.
- Portfolio content is in Portuguese and stored in the database; edit it through the admin panel at http://127.0.0.1:5000/admin after logging in.
