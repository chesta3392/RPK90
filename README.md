# Demo Play Hub (Django)

A local full-stack prototype inspired by the supplied screenshots. All points, games, and results are simulated. No real-money payments, betting, or withdrawals are implemented.

## Run on Windows
1. Install Python 3.10+.
2. Open a terminal in this folder.
3. Create and activate a virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
4. Install dependencies and initialize the database:
   ```powershell
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```
5. Open http://127.0.0.1:8000/

## Included
- Registration and login
- Home, Play, Wallet, History, Result History, Notifications, App Details, Terms, Help
- SQLite models for demo wallet transactions, demo game entries, notifications, and results
- Django admin at `/admin/`
- Demo-point crediting and simulated game actions only
