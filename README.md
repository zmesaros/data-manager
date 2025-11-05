# Django + Vue.js Single Page Application

A full-stack web application built with Django REST Framework for the backend and Vue.js 3 for the frontend, featuring master/detail views.

## Features

- **Backend**: Django 5.2.7 with Django REST Framework
- **Frontend**: Vue.js 3 with Vue Router
- **Multi-database Support**: PostgreSQL, MariaDB/MySQL, SQL Server, or SQLite
- **RESTful API**: Full CRUD operations
- **CORS Enabled**: Frontend-backend communication configured

## Recent Changes & Enhancements (November 2025)

The application has undergone significant enhancements to improve user experience and functionality:

### UI/UX Enhancements & Bug Fixes (November 2025)

-   **Redesigned List Pages**: The Item and Customer list pages have been redesigned for a cleaner, more modern look inspired by Business Central list pages.
-   **Header Action Bar**: The floating action button (FAB) has been replaced with a more traditional action bar in the header, containing "New", "Delete", and "Refresh" actions.
-   **Improved Styling**: The UI has been refined with reduced padding and spacing for a more compact view, and the focus outline on edited fields has been improved for a cleaner look.
-   **Consistent Keyboard Navigation**: The keyboard navigation has been made consistent across all fields, including the email field, for a smoother user experience.
-   **Email Validation**: Added client-side validation for email fields to ensure data integrity.

### Bug Fixes & Performance

-   **Compilation & Linting**: Resolved critical syntax and linting errors in the frontend code that prevented the application from compiling.
-   **Sorting Stability**: Corrected a significant bug in the list views where the sort order would incorrectly revert to a previous state when editing multiple records sequentially. The sorting is now stable and predictable.
-   **Automatic Re-sorting**: The list now automatically and smoothly re-sorts itself after an edit is completed, ensuring the data displayed is always in the correct order without requiring a manual refresh.
-   **In-Edit Stability**: Fixed an issue where records would "jump" or re-sort while actively being edited, providing a much smoother editing experience.

### List Views (Items & Customers)

-   **No Pagination**: All records are now loaded and displayed on a single page.
-   **Header Action Bar**: A sticky header contains a search bar and an action bar with the following actions:
    -   **New**: Create a new record.
    -   **Delete**: Delete the selected record.
    -   **Refresh**: Refresh the list and re-apply the current sort order.
-   **Keyboard Navigation**:
    -   Use **Arrow Left/Right** to navigate between fields within a record.
    -   Use **Arrow Up/Down** to navigate between records.
    -   Pressing **Arrow Down** on the last record automatically creates a new, empty record and moves focus to it.
-   **Dynamic Search**: A sticky search bar in the header allows real-time filtering of records as you type.
    -   **Items**: Search by Name and Category.
    -   **Customers**: Search by First Name, Last Name, Email, Phone, and City.
-   **Row Selection**: Clicking a row (or navigating to it with arrow keys) selects it, highlighting it visually.
-   **Column Sorting**: Click on table headers to sort records by that column (ascending/descending).
-   **Compact UI**: Reduced padding between table rows for a more condensed view.
-   **Improved New Record Handling**:
    -   New records are only saved when all required fields are filled and the user navigates away from the row.
    -   If a new record is partially filled but invalid, an alert will notify the user upon navigation.
    -   Completely empty new records are automatically removed if the user navigates away without entering any data.

### Detail Views (Items & Customers)

-   **Escape Key to Close**: Pressing the `Esc` key will now navigate back to the respective list page.

## Project Structure

```
django-spa-app/
├── backend/                 # Django backend
│   ├── config/             # Django settings
│   ├── data_manager/       # Main Django app
│   ├── manage.py
│   ├── requirements.txt
│   └── .env.example
└── frontend/               # Vue.js frontend
    ├── src/
    │   ├── components/
    │   ├── views/          # Page components
    │   ├── router/         # Vue Router config
    │   ├── services/       # API services
    │   ├── App.vue
    │   └── main.js
    └── package.json
```

## Prerequisites

- Python 3.8+
- Node.js 14+ and npm
- One of the following databases (optional):
  - PostgreSQL
  - MariaDB/MySQL
  - SQL Server
  - SQLite (default, no setup required)

## Backend Setup

### 1. Navigate to backend directory
```bash
cd backend
```

### 2. Create virtual environment (recommended)
```bash
python -m venv venv
# On Windows:
venc\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure database (optional)
Copy `.env.example` to `.env` and configure your database:
```bash
cp .env.example .env
```

Edit `.env` to set your database type:
- For SQLite (default): `DB_TYPE=sqlite`
- For PostgreSQL: `DB_TYPE=postgresql`
- For MariaDB/MySQL: `DB_TYPE=mariadb`
- For SQL Server: `DB_TYPE=sqlserver`

Also set the connection parameters (DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT).

### 5. Run migrations
```bash
python manage.py migrate
```

### 6. Create superuser (optional, for admin access)
```bash
python manage.py createsuperuser
```

### 7. Start the development server
```bash
python manage.py runserver
```

The backend API will be available at `http://localhost:8000/api/`

## Frontend Setup

### 1. Navigate to frontend directory
```bash
cd frontend
```

### 2. Install dependencies
```bash
npm install
```

### 3. Start the development server
```bash
npm run serve
```

The frontend will be available at `http://localhost:8080/`

## Running the Application

1. Start the Django backend server (in one terminal):
   ```bash
   cd backend
   python manage.py runserver
   ```

2. Start the Vue.js frontend server (in another terminal):
   ```bash
   cd frontend
   npm run serve
   ```

3. Open your browser and navigate to `http://localhost:8080`

## API Endpoints

### Items
- `GET /api/items/` - List all items
- `POST /api/items/` - Create a new item
- `GET /api/items/{id}/` - Retrieve a specific item
- `PUT /api/items/{id}/` - Update an item (full update)
- `PATCH /api/items/{id}/` - Partial update an item
- `DELETE /api/items/{id}/` - Delete an item
- `GET /api/items/active/` - List only active items

### Customers
- `GET /api/customers/` - List all customers
- `POST /api/customers/` - Create a new customer
- `GET /api/customers/{id}/` - Retrieve a specific customer
- `PUT /api/customers/{id}/` - Update a customer (full update)
- `PATCH /api/customers/{id}/` - Partial update a customer
- `DELETE /api/customers/{id}/` - Delete a customer
- `GET /api/customers/active/` - List only active customers

## Database Configuration Examples

### PostgreSQL
```env
DB_TYPE=postgresql
DB_NAME=django_spa_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### MariaDB/MySQL
```env
DB_TYPE=mariadb
DB_NAME=django_spa_db
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
```

### SQL Server
```env
DB_TYPE=sqlserver
DB_NAME=django_spa_db
DB_USER=sa
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=1433
```

## Admin Interface

Django admin is available at `http://localhost:8000/admin/`

Login with the superuser credentials you created during setup.

## Technology Stack

### Backend
- Django 5.2.7
- Django REST Framework 3.16.1
- Django CORS Headers 4.9.0
- Python Dotenv 1.2.1
- Database drivers: psycopg2-binary, mysqlclient, pyodbc

### Frontend
- Vue.js 3
- Vue Router 4
- Axios for HTTP requests
- Modern ES6+ JavaScript

## Development Notes

- The backend runs on port 8000
- The frontend runs on port 8080
- CORS is configured to allow requests from localhost:8080
- All API responses follow REST conventions

## Troubleshooting

### CORS Issues
If you encounter CORS errors, ensure:
- Django backend is running on port 8000
- Frontend is running on port 8080
- `django-cors-headers` is installed and configured in settings

### Database Connection Issues
- Check your database credentials in `.env`
- Ensure the database server is running
- Verify the database drivers are installed

### Frontend Can't Connect to Backend
- Verify the backend is running on `http://localhost:8000`
- Check the API base URL in `frontend/src/services/api.js`

## License

This project is open source and available under the MIT License.
