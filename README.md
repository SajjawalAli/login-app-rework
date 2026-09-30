# Login App Rework

A production-grade Django authentication system built with Python 3.13 and PostgreSQL 17.

## Prerequisites

- **Python 3.13**
- **Docker Desktop** (with WSL 2 integration enabled)
- **Git**

## Setup & Local Installation

# 1. Clone the repository
```bash
git clone https://github.com/SajjawalAli/login-app-rework.git
```
```bash
cd login-app-rework
```
# 2. Prepare environment variables
```bash
cp .env.example .env
```
# 3. Spin up PostgreSQL and run migrations
```bash
docker compose up -d
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
```

# 4. Run automated test suite
```bash
python manage.py test accounts
```
