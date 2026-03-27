# UACCS Website Backend

### Clone Repository

```bash
git clone git@github.com:Ucluelet-and-Area-Childcare-Society/uaccs-backend.git
cd uaccs-backend
```

## Backend Setup

### 1. Create and Activate Virtual Environment

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

**Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

> **Note:** If Python is incompatible, substitute `python3` for `python` throughout.

### 4. Run Migrations

  Ensure you are at the folder ./uaccs-backend/uaccs for *Mac/Linux*, and .\uaccs-backend\uaccs for *Windows*.

```bash
cd uaccs
python manage.py migrate
```