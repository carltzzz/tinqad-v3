# TINQAD V3.0

## Total Integrated Network for Quality Assurance and Development

TINQAD v3.0 is an internal web application for the **UPD Quality Assurance Office (QAO)** that streamlines the internal processes of the different QA teams.

---

## Features

- **Director Dashboard** — Team overviews, announcements, peer evaluation management, evaluation summaries, and PDF report generation
- **Admin Dashboard** — Expense tracking, inventory management, staff profiles, training records, and report generation
- **Peer Evaluation System** — Director-managed evaluation periods, form responses, and results
- **User Management** — Registration, profiles, password management, role-based access control

---

## Prerequisites

| Requirement | Version |
|---|---|
| Python | 3.12 |
| PostgreSQL | 12+ |
| pip | Latest |

You must have a running PostgreSQL instance with a database named `TINQAD_Database` containing the required schemas and tables.

---

## Installation

### 1. Clone the repository

```bash
git clone git@github.com:carltzzz/tinqad-v3.git
cd tinqad-v3
```

### 2. Create and activate a virtual environment

```bash
python3.12 -m venv venv
source venv/bin/activate
```

### 3. Set up environment variables

```bash
cp .env.example .env
```

Generate a secret key and set it in `.env`:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Then edit `.env` with your database credentials and the generated secret key.

### 4. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Run the application

```bash
python index.py
```

The app will be available at [http://127.0.0.1:8050/](http://127.0.0.1:8050/) and will open automatically in your browser.

---

## Environment Variables

Set the following in your `.env` file (copied from `.env.example`):

| Variable | Description | Default |
|---|---|---|
| `FLASK_SECRET_KEY` | Secret key for Flask session encryption | *(must be generated)* |
| `DB_HOST` | PostgreSQL host address | `localhost` |
| `DB_PORT` | PostgreSQL port | `5433` |
| `DB_NAME` | Database name | `TINQAD_Database` |
| `DB_USER` | Database username | `postgres` |
| `DB_PASSWORD` | Database password | `postgres` |

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Language** | Python 3.12 |
| **Web Framework** | Flask 3.0.3 |
| **Dashboard Framework** | Plotly Dash 3.0.4 |
| **UI Components** | Dash Bootstrap Components, Dash Core Components, Dash Mantine Components |
| **Database** | PostgreSQL (via psycopg2) |
| **Authentication** | Flask Sessions + bcrypt password hashing |
| **PDF Generation** | WeasyPrint 65.1 (Jinja2 templates) |
| **Data Processing** | Pandas, NumPy, Plotly, Matplotlib |
| **WSGI Server** | Gunicorn 23.0.0 (production) |
| **Environment Config** | python-dotenv |

---

## Project Structure

```
tinqad-v3/
├── app.py                  # Flask + Dash app initialization
├── index.py                # Main entry point, routing, role-based access control
├── index.wsgi              # WSGI entry for production deployment
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
│
├── apps/                   # Core application modules
│   ├── dbconnect.py        # Database connection & query helpers
│   ├── commonmodules.py    # Shared navbar, sidebar, footer
│   ├── auth_utils.py       # Session/auth utilities
│   ├── home.py             # Login page
│   ├── maindashboard/      # Main dashboard (homepage, profiles, user mgmt)
│   ├── director/           # Director features (evaluations, reports, PDFs)
│   ├── admin/              # Admin features (expenses, inventory, staff)
│   ├── iqa/                # Internal QA (directories, ISO, IAADS reports)
│   ├── eqa/                # External QA (accreditation, programs, SAR)
│   ├── km/                 # Knowledge Management (SDGs, QS rankings)
│   └── qaofficers/         # QA Officers (directory, training, CDF)
│
├── assets/                 # Static assets (CSS, JS, icons, images)
│   ├── bootstrap.css       # Custom Bootstrap overrides
│   ├── dccstyle.css        # Custom Dash component styles
│   ├── clientside.js       # Client-side JS callbacks
│   └── icons/              # Logos and UI icons
│
├── templates/              # Jinja2 templates for PDF generation
├── migrations/             # Manual SQL migration scripts
└── venv/                   # Virtual environment (gitignored)
```

---

## Authentication & Access Control

TINQAD uses role-based access control via numeric `user_access_type` values:

| Access Level | Role |
|---|---|---|
| 0 | Unauthenticated | Login page only |
| 1 | Basic Access|
| 2 | Director’s Access / Super Admin |
| 3 | Admin III and V’s Access |
| 4 | Admin Others’ Access |
| 5 | IQA Access |
| 6 | EQA Access |
| 7 | KM Access |

Passwords are double-hashed: SHA-256 of the plaintext, then bcrypt of the hash.

---

## Database

The application connects to a PostgreSQL database named `TINQAD_Database` with the following schemas:

| Schema | Purpose |
|---|---|
| `maindashboard` | Users, offices, announcements, alerts, team messages |
| `adminteam` | Expenses, inventory |
| `kmteam` | SDG submissions, ranking bodies |
| `public` | Municipalities, provinces, colleges, degree programs |

SQL migration scripts in `/migrations` must be run manually against the database.

---

## License

*Not yet specified.*
