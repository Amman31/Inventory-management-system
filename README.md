# Inventory Management System

Desktop **Inventory Management System** built with Python, **Tkinter**, **SQLite**, and **Pillow** for images. The codebase is organized as a small application package under `app/`, with shared configuration in `config/`, an entry point `main.py`, and automated tests under `tests/`.

## Project layout

- **`main.py`** — Starts the app: ensures the database exists, then opens the dashboard.
- **`config/settings.py`** — Central paths: project root, `database/ims.db`, `bill/`, and `images/` (directories are created if missing).
- **`config/database.py`** — `initialize_database()` creates required tables if they do not exist; `get_connection()` opens SQLite using the configured path.
- **`app/dashboard.py`** — Main window (`IMS`): menu, stats, clock, and navigation to feature screens.
- **`app/employee.py`**, **`supplier.py`**, **`category.py`**, **`product.py`**, **`sales.py`**, **`billing.py`** — Feature modules (each can still be run standalone for quick UI checks).
- **`app/ui/`** — Reusable UI pieces: fonts/colors (`theme.py`), CRUD/search buttons (`buttons.py`), scrolled `Treeview` factory (`tables.py`), search `LabelFrame` helper (`search_frame.py`), and common window setup (`window.py`).
- **`app/sql_helpers.py`** — Whitelisted column names and parameterized `LIKE` queries for employee and product search (reduces SQL injection risk from UI input).
- **`tests/`** — **pytest** suite: unit, integration, and regression tests.

## How to run

1. Create and activate a virtual environment (recommended).
2. Install dependencies:

   `pip install -r requirements.txt`

3. Add optional assets under **`images/`** (e.g. `logo1.png`, `menu_im.png`, `side.png`, `cat2.jpg`, category images). The dashboard uses placeholders if files are missing so the app still starts.
4. Launch the application:

   `python main.py`

The database file is created automatically under **`database/ims.db`** on first run. You no longer need to run a separate `create_db.py` script first.

## Running tests

From the project root:

`python -m pytest tests -v`

The suite includes **at least three unit tests** (database initialization, connection behavior, SQL helper safety), **two integration scenarios** (multi-step employee lifecycle; category/supplier/product flow; plus bill directory behavior), and **regression tests** that pin fixes for fragile patterns (e.g. `StringVar` comparison bugs, parameterized search SQL).

## Maintenance coursework notes (refactoring and structure)

**Configuration and database.** All modules now use `get_connection()` and paths from `config.settings` instead of hard-coded `ims.db` or per-file `BASE_DIR` guesses. That removes duplicated path logic and keeps a single place to change where data and bills live. `initialize_database()` is invoked from `main.py` so first-time setup is automatic.

**UI deduplication.** Repeated patterns—standard CRUD window geometry, the green “Search” button, the Save/Update/Delete/Clear strip with the same colors, and every `Treeview` plus horizontal/vertical scrollbars—were extracted into `app/ui/`. Screens import these helpers so future style or behavior changes happen in one module instead of six copies.

**Code quality and naming.** Database connections are closed in `finally` blocks where appropriate; product validation now correctly uses `self.var_sup.get()` (and the same pattern for category) instead of comparing `StringVar` objects to strings, which was always false. Employee and product search use whitelisted column names and bound parameters instead of concatenating user text into SQL.

**Billing and sales.** Bill files are written with `os.path.join(BILL_DIR, …)` and UTF-8 encoding. The cart grid only displays four columns, but each cart row still stores stock in memory; selecting a cart line resolves stock from `cart_list` so “In Stock” stays correct (avoiding an off-by-column bug with `row[4]` on the tree). Billing product search uses a parameterized `LIKE` query.

These changes are aimed at **software maintenance**: easier evolution, fewer duplicated UI blocks, safer queries, and tests that document expected behavior for future edits.

## Original feature overview (unchanged behavior)

The application still provides:

- **Dashboard** — Totals for employees, suppliers, categories, products, and sales (bill `.txt` count), plus navigation.
- **Employee** — CRUD and search by email, name, or contact.
- **Supplier** — CRUD and search by invoice.
- **Category** — Add/delete categories.
- **Product** — CRUD with category and supplier dropdowns; search by category, supplier, or name.
- **Sales** — List bill files and view contents by invoice.
- **Billing** — Product picker, cart, calculator, discount, generate/save bill.

## Prerequisites

- Python 3.x  
- `pip install -r requirements.txt` (includes **Pillow** and **pytest**)

Standard library modules (`sqlite3`, `os`, `tkinter`, etc.) do not need separate installation.
