# TINQAD V3.0

## Total Integrated Network for Quality Assurance and Development

TINQAD v3.0 is system meant to streamline the internal processes of the different teams of the UPD QAO.

## Features
This version will only focus on specific features of the Director and Admin Dashboards.

## Quick Start

## Prerequisites
Python 3.12

### Installation

1. Clone the repository

```bash
git clone git@github.com:carltzzz/tinqad-v3.git
```

2. Change directory to the project folder**
```bash
cd <your-project-directory>/tinqad-v3
```

3. Set up a virtual environment
```bash
python3.12 -m venv venv
source venv/bin/activate
```

4. Set up environment variables

```bash
cp .env.example .env
Edit .env and set your database credentials and a unique FLASK_SECRET_KEY.
Generate a secret key with:
python -c "import secrets; print(secrets.token_hex(32))"
```

5. Install the dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

6. Run the project
```bash
python index.py
```


## Tech Stack