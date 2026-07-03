# Chekicha Timeline

Streamlit dashboard for tracking JKT48 chekicha schedules, roulette results, and member history.

## Requirements

- Python 3.11+
- Supabase project with the required tables already created

## Install

```bash
pip install -r requirements.txt
```

## Secrets

Create `.streamlit/secrets.toml` locally with:

```toml
SUPABASE_URL = "your-supabase-url"
SUPABASE_KEY = "your-supabase-anon-key"
ADMIN_PASSWORD = "your-password"
```

Do not commit this file.

## Run locally

```bash
streamlit run app.py
```

## Streamlit Community Cloud

Set these secrets in the app settings:

- `SUPABASE_URL`
- `SUPABASE_KEY`
- `ADMIN_PASSWORD`

Main file:

- `app.py`

## App structure

- `pages/1_📊_Overview.py`
- `pages/2_⏳_Timeline.py`
- `pages/3_👤_Member_Corner.py`
- `pages/4_🔐_Admin_Panel.py`

## Notes

- Admin actions depend on valid Supabase write access.
- Member and event schema are expected to already exist in Supabase.
