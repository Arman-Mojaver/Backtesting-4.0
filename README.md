# Backtesting-4.0

### Create virtual environment and install dependencies:
   1. Create virtual environment: `python -m venv venv`
   2. Activate virtual environment: `.\venv\Scripts\activate`
   3. Install dependencies: `pip install -r requirements.txt`

### Add new dependency:
  1. Activate virtual environment: `.\venv\Scripts\activate`
  2. Install package/s: `pip install <package>`
  3. Add package to requirements: `pip freeze > requirements.txt`
  4. Commit to main branch.

### Install and execute the CLI:
  1. From the root directory: `pip install -e .`
  2. While venv is active, execute: `bt`

### Create new alembic revision:
  1. Make model modifications (when creating a new model, it needs to be added to the __init__.py file)
  2. Get inside the api docker container
  3. Execute command: `alembic revision --autogenerate -m "<revision title>"`
