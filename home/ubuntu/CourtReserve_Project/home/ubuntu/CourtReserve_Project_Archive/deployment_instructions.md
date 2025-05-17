# CourtReserve Deployment Instructions

This document provides detailed instructions for deploying the CourtReserve application.

## Prerequisites

*   Python 3.9+ (Python 3.11 recommended, as used in development)
*   pip (Python package installer)
*   Node.js and npm (if you need to modify or build frontend assets, though prototypes are HTML/CSS/JS)
*   A WSGI server like Gunicorn (for production)
*   Eventlet (for SocketIO with Gunicorn)
*   A relational database (SQLite is used for development, PostgreSQL or MySQL recommended for production)

## 1. Obtain Project Files

Ensure you have the complete project files, including the `CourtReserve_Backend` directory and the `courtreserve_prototypes` directory.

## 2. Backend Setup (CourtReserve_Backend)

Navigate to the `CourtReserve_Backend` directory for these steps:

```bash
cd path/to/CourtReserve_Backend
```

### 2.1. Create and Activate Virtual Environment

It is highly recommended to use a virtual environment to manage dependencies.

```bash
python3 -m venv venv
source venv/bin/activate  # On Linux/macOS
# venv\Scripts\activate    # On Windows
```

### 2.2. Install Dependencies

Install all required Python packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 2.3. Configure Environment Variables

Create a `.env` file in the `CourtReserve_Backend` directory. This file will store sensitive configuration and environment-specific settings. The application uses `python-dotenv` to load these variables.

**Example `.env` file:**

```env
FLASK_APP="src.main:create_app"
FLASK_ENV="development" # Set to "production" for production deployment
SECRET_KEY="your_strong_random_secret_key_here" # Generate a strong random key
JWT_SECRET_KEY="your_strong_random_jwt_secret_key_here" # Generate another strong random key

# Database Configuration (SQLite for development)
DATABASE_URL="sqlite:///courtreserve.db"

# For Production (Example: PostgreSQL - uncomment and configure if used)
# DATABASE_URL="postgresql://user:password@host:port/database_name"

# For Production (Example: MySQL - uncomment and configure if used)
# DATABASE_URL="mysql+mysqlconnector://user:password@host:port/database_name"

# Other potential variables (e.g., for email, external services)
# MAIL_SERVER="smtp.example.com"
# MAIL_PORT=587
# MAIL_USE_TLS=True
# MAIL_USERNAME="your_email@example.com"
# MAIL_PASSWORD="your_email_password"
```

**Notes on Environment Variables:**

*   `SECRET_KEY` and `JWT_SECRET_KEY`: These are critical for security. Use strong, unique random strings. You can generate them using Python: `python -c "import secrets; print(secrets.token_hex(32))"`.
*   `DATABASE_URL`: 
    *   For **SQLite** (development/testing): `sqlite:///courtreserve.db` (creates a file named `courtreserve.db` in the instance folder, or `CourtReserve_Backend/instance/courtreserve.db` if instance folder is explicitly configured).
    *   For **PostgreSQL** (production): `postgresql://<user>:<password>@<host>:<port>/<database_name>`. You will need to install the `psycopg2-binary` package: `pip install psycopg2-binary`.
    *   For **MySQL** (production): `mysql+mysqlconnector://<user>:<password>@<host>:<port>/<database_name>`. You will need to install the `mysql-connector-python` package: `pip install mysql-connector-python`.
    *   Ensure the `src/config.py` file correctly parses `DATABASE_URL` for `SQLALCHEMY_DATABASE_URI`.
*   `FLASK_ENV`: Set to `development` for debugging features. Set to `production` for production deployments to disable the debugger and enable optimizations.

### 2.4. Database Migrations

The application uses Flask-Migrate (Alembic) to manage database schema changes.

1.  **Initialize Migrations (if not already done, usually only once per project):**
    ```bash
    flask db init 
    ```
    (The project already has a migrations folder, so this step is likely done.)

2.  **Create a New Migration (if you made changes to SQLAlchemy models):**
    ```bash
    flask db migrate -m "Your descriptive migration message"
    ```

3.  **Apply Migrations to the Database:**
    This command creates or updates the database tables according to the latest migration scripts.
    ```bash
    flask db upgrade
    ```

### 2.5. Seed Initial Data

The project includes a command to seed the database with initial data (e.g., admin user, court types, sample courts).

```bash
flask seed-db
```
This command will check if data already exists and skip seeding if it does, to prevent duplication.




### 2.6. Running the Flask Application (Development)

For development, you can use the Flask development server. Ensure your `.env` file has `FLASK_ENV="development"`.

```bash
flask run --host=0.0.0.0 --port=5000
```

*   `--host=0.0.0.0`: Makes the server accessible from your local network (and for frontend testing if frontend is served separately or on a different device).
*   `--port=5000`: Specifies the port. Change if 5000 is in use.

The application, including SocketIO, should now be running.

### 2.7. Running the Flask Application (Production)

For production, a robust WSGI server like Gunicorn is recommended, along with Eventlet for SocketIO compatibility.

1.  **Ensure Gunicorn and Eventlet are installed (they should be in `requirements.txt`):**
    ```bash
    pip install gunicorn eventlet
    ```

2.  **Set `FLASK_ENV="production"` in your `.env` file.**

3.  **Run Gunicorn with Eventlet worker:**
    The entry point for the application is the `create_app` factory in `src/main.py`. Gunicorn needs to be pointed to this.

    ```bash
    gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 "src.main:create_app()"
    ```
    *   `--worker-class eventlet`: Specifies Eventlet for asynchronous workers, necessary for SocketIO.
    *   `-w 1`: Number of worker processes. For SocketIO with Eventlet, it's often recommended to start with 1 worker due to how Eventlet handles concurrency. You might need to adjust based on your server and load.
    *   `--bind 0.0.0.0:5000`: Binds to all network interfaces on port 5000.
    *   `"src.main:create_app()"`: Path to your Flask app factory function. The parentheses `()` are important if `create_app` is a factory that needs to be called.

    You might want to run Gunicorn as a background service using tools like `systemd` or `supervisor` in a real production environment.

### 2.8. Notes on Production Database

*   **SQLite is not recommended for production** due to limitations with concurrent access and write performance.
*   **Switch to PostgreSQL or MySQL:**
    1.  Set up a PostgreSQL or MySQL server.
    2.  Create a new database and a user with appropriate permissions for the CourtReserve application.
    3.  Install the necessary Python driver:
        *   PostgreSQL: `pip install psycopg2-binary`
        *   MySQL: `pip install mysql-connector-python`
    4.  Update the `DATABASE_URL` in your `.env` file to point to your production database. Examples:
        *   `DATABASE_URL="postgresql://youruser:yourpassword@yourhost:yourport/yourdatabase"`
        *   `DATABASE_URL="mysql+mysqlconnector://youruser:yourpassword@yourhost:yourport/yourdatabase"`
    5.  Ensure `src/config.py` correctly uses this `DATABASE_URL` to set `SQLALCHEMY_DATABASE_URI`.
    6.  Run `flask db upgrade` again to apply migrations to your new production database.
    7.  Run `flask seed-db` to seed initial data into your production database.

## 3. Frontend Prototype Deployment (courtreserve_prototypes)

The frontend prototypes are located in the `/home/ubuntu/CourtReserve_Project_Archive/courtreserve_prototypes/` directory and consist of HTML, CSS, and JavaScript files.

### 3.1. Serving Statically

These files can be served by any static web server (e.g., Nginx, Apache, Caddy, or even a simple Python HTTP server for testing).

**Example using Python's built-in HTTP server (for simple testing only, not for production):**

Navigate to the `courtreserve_prototypes` directory:
```bash
cd path/to/CourtReserve_Project_Archive/courtreserve_prototypes/
python3 -m http.server 8080
```
Then access the prototypes at `http://localhost:8080` (or your server's IP) in your browser.

### 3.2. Production Static Serving (e.g., Nginx)

For production, configure a web server like Nginx to serve the static files from the `courtreserve_prototypes` directory. You would also typically configure Nginx as a reverse proxy for your Gunicorn backend API.

**Example Nginx Configuration Snippet (conceptual):**

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    # Serve Frontend Static Files
    location / {
        root /path/to/CourtReserve_Project_Archive/courtreserve_prototypes;
        try_files $uri $uri/ /index.html; # Or your main HTML file e.g. signup_login.html
    }

    # Proxy API requests to Gunicorn backend
    location /api/ { # Assuming your API is at /api/ or you adjust frontend to call /api/
        proxy_pass http://127.0.0.1:5000; # Gunicorn backend
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # For SocketIO
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # If API is not under /api/ and frontend calls directly to /auth, /courts etc.
    # you'll need separate location blocks or more complex routing.
    # For example, if your Flask routes are /auth, /courts, etc., and frontend calls them directly:
    location ~ ^/(auth|users|courts|bookings|trainer|messages|notifications|waitlist|socket.io)/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # For SocketIO specifically under /socket.io/
        if ($uri ~* "/socket.io/") {
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }
    }
}
```

**Important:** Ensure the `API_BASE_URL` in the frontend JavaScript files (e.g., `dashboard.html`, `signup_login.html`) is correctly set to point to where your backend API is accessible (e.g., `http://yourdomain.com` if Nginx is proxying, or `http://yourdomain.com:5000` if accessed directly and CORS is configured).

## 4. Final Checks

*   Ensure all environment variables are correctly set for the production environment.
*   Test all application functionalities thoroughly after deployment.
*   Monitor logs for any errors (Gunicorn logs, Nginx logs, application logs if configured).

This concludes the deployment instructions.




## 5. Docker Deployment (Recommended)

This project has been Dockerized for easier setup and deployment. You will need Docker and Docker Compose installed on your system.

### 5.1. Prerequisites for Docker Deployment

*   Docker Engine (latest stable version)
*   Docker Compose (V2 recommended, usually included with Docker Desktop or installable as `docker-compose-v2` or via `docker compose` CLI plugin)

### 5.2. Project Structure for Docker

Ensure you have the complete project structure, including:
*   `CourtReserve_Backend/Dockerfile`
*   `CourtReserve_Backend/entrypoint.sh`
*   `CourtReserve_Backend/.env` (configure this as per Section 2.3, especially `SECRET_KEY`, `JWT_SECRET_KEY`. `DATABASE_URL` will be `sqlite:///instance/courtreserve.db` for the Docker setup using SQLite by default, or can be configured to point to the `db` service if using PostgreSQL in `docker-compose.yml`)
*   `courtreserve_prototypes/Dockerfile`
*   `courtreserve_prototypes/nginx.conf`
*   `docker-compose.yml` (in the root of `CourtReserve_Project_Archive`)

### 5.3. Building and Running with Docker Compose

1.  **Navigate to the Project Root Directory:**
    Open your terminal and change to the directory containing the `docker-compose.yml` file (e.g., `CourtReserve_Project_Archive`).

    ```bash
    cd path/to/CourtReserve_Project_Archive
    ```

2.  **Configure Backend Environment Variables:**
    Ensure the `CourtReserve_Backend/.env` file is present and correctly configured with your `SECRET_KEY`, `JWT_SECRET_KEY`, and `DATABASE_URL`. For the default Docker setup with SQLite, `DATABASE_URL="sqlite:///instance/courtreserve.db"` is used, and the database file will be persisted in `CourtReserve_Backend/instance` on your host machine due to the volume mount.
    If you wish to use the PostgreSQL service defined in `docker-compose.yml` (currently commented out for the `backend` service dependency and the `db` service itself is present but not explicitly linked as a dependency unless uncommented in backend service), you would:
    *   Uncomment the `db` service in `docker-compose.yml` if it's fully commented out.
    *   Uncomment `depends_on: - db` in the `backend` service definition.
    *   Update `CourtReserve_Backend/.env` with `DATABASE_URL="postgresql://courtreserve_user:courtreserve_password@db:5432/courtreserve_db"`.
    *   Ensure `psycopg2-binary` is in `CourtReserve_Backend/requirements.txt` (it should be from previous steps).

3.  **Build and Start Containers:**
    Run the following command to build the images (if they don't exist or Dockerfiles have changed) and start the services in detached mode (`-d`):

    ```bash
    sudo docker compose up --build -d
    ```
    *   `sudo` might be required depending on your Docker installation and user permissions.
    *   `--build` forces a rebuild of the images.
    *   `-d` runs the containers in the background.

4.  **Accessing the Application:**
    *   **Frontend:** Open your web browser and navigate to `http://localhost:8080` (or the port you mapped for the `frontend` service in `docker-compose.yml`).
    *   **Backend API:** The API will be accessible at `http://localhost:5000` (or the port you mapped for the `backend` service). The frontend is configured to communicate with the backend via this port internally within the Docker network (or directly if you were running frontend outside Docker and backend exposed on localhost).

### 5.4. Managing Docker Containers

*   **View Logs:**
    ```bash
    sudo docker compose logs backend
    sudo docker compose logs frontend
    ```
*   **Stop Containers:**
    ```bash
    sudo docker compose down
    ```
*   **Stop and Remove Volumes (e.g., to reset the database):**
    ```bash
    sudo docker compose down -v
    ```
*   **List Running Containers:**
    ```bash
    sudo docker compose ps
    ```

### 5.5. Notes on Docker Deployment

*   The backend service uses an `entrypoint.sh` script that automatically runs database migrations (`flask db upgrade`) and seeds the database (`flask seed-db`) when the container starts.
*   The SQLite database (`courtreserve.db`) is stored in the `CourtReserve_Backend/instance` directory on your host machine and mounted into the backend container, ensuring data persistence across container restarts.
*   The frontend is served by Nginx. Any changes to frontend static files would require rebuilding the `frontend` image (`sudo docker compose up --build -d frontend`) or setting up a volume mount for development if desired (not configured by default in the provided `docker-compose.yml` for frontend static files).

