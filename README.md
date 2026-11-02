# Pathwise

Student skill and career roadmap. Django stores students, skills, careers, and progress. React is the workspace where a student rates skills, compares roles, and marks roadmap steps.

## Run it

Backend, from `backend`:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_catalog
python manage.py runserver
```

Frontend, from `frontend`:

```bash
npm install
npm run dev
```

Open http://127.0.0.1:5173. The Vite dev server proxies `/api` to Django on port 8000.

## Demo accounts

| Who | Username | Password |
| --- | --- | --- |
| Student Maya Chen | `demo` | `pathwise123` |
| Django admin | `admin` | `pathwise-admin` |

Admin: http://127.0.0.1:8000/admin/

## What a student can do

- Create an account and edit a short profile
- Rate skills from unrated (0) through expert (5)
- Compare six careers. Readiness weighs core skills twice as much as recommended ones, and extra skill past the requirement does not raise the score
- Set one target career
- Mark roadmap steps as to do, doing, or done

Salary figures in the catalog are illustrative US ranges, not offers.
