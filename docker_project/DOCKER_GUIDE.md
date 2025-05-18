# Docker Setup and Testing Guide for TennisCourtReserve

This guide explains how to set up, run, and test the TennisCourtReserve project using Docker Compose.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) (version 20.10.0 or higher)
- [Docker Compose](https://docs.docker.com/compose/install/) (version 2.0.0 or higher)
- Git (to clone the repository)

## Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/oguzhandilber/TennisCourtReserve.git
   cd TennisCourtReserve
   ```

2. Start the application:
   ```bash
   docker-compose up -d
   ```

3. Access the application:
   - Frontend: http://localhost
   - Backend API: http://localhost:5000/api

## Detailed Instructions

### Building and Starting the Application

1. Build and start all services:
   ```bash
   docker-compose up --build -d
   ```
   This command builds the Docker images and starts the containers in detached mode.

2. View logs:
   ```bash
   # View logs from all services
   docker-compose logs -f
   
   # View logs from a specific service
   docker-compose logs -f backend
   docker-compose logs -f frontend
   ```

3. Check container status:
   ```bash
   docker-compose ps
   ```

### Testing the Application

1. **Backend API Testing**:
   - Health check: http://localhost:5000/api/health
   - API documentation: http://localhost:5000/api/docs
   - Test authentication: http://localhost:5000/api/auth/test

2. **Frontend Testing**:
   - Access the landing page: http://localhost
   - Sign up/login: http://localhost/signup_login.html
   - View courts: http://localhost/court_listing.html

3. **End-to-End Testing**:
   - Register a new user
   - Log in with the registered user
   - Browse available courts
   - Make a booking request
   - Check booking status

### Database Management

The application uses SQLite with a persistent volume for data storage:

1. Access the database:
   ```bash
   docker-compose exec backend sqlite3 /app/instance/tennis_court_reserve.db
   ```

2. Backup the database:
   ```bash
   docker-compose exec backend sqlite3 /app/instance/tennis_court_reserve.db .dump > backup.sql
   ```

### Stopping and Cleaning Up

1. Stop the application:
   ```bash
   docker-compose down
   ```

2. Stop and remove volumes (will delete all data):
   ```bash
   docker-compose down -v
   ```

3. Remove built images:
   ```bash
   docker-compose down --rmi all
   ```

## Troubleshooting

### Common Issues

1. **Services not starting properly**:
   - Check logs: `docker-compose logs`
   - Ensure ports 80 and 5000 are not in use by other applications

2. **Backend not connecting to database**:
   - Check backend logs: `docker-compose logs backend`
   - Verify environment variables in docker-compose.yml

3. **Frontend not connecting to backend**:
   - Check frontend logs: `docker-compose logs frontend`
   - Verify the API URL configuration in frontend files

### Restarting Services

If you need to restart a specific service:
```bash
docker-compose restart backend
docker-compose restart frontend
```

## Development Workflow

For development purposes, you can mount your local code directories:

1. Modify the docker-compose.yml to include volume mounts:
   ```yaml
   backend:
     # ... other configurations
     volumes:
       - ./backend:/app
       - backend_data:/app/instance
   
   frontend:
     # ... other configurations
     volumes:
       - ./frontend:/usr/share/nginx/html
   ```

2. Start the services with the updated configuration:
   ```bash
   docker-compose up -d
   ```

3. Changes to the code will be reflected in the running containers.

## Security Notes

- The default setup is intended for development and testing
- For production deployment, consider:
  - Using environment variables for sensitive information
  - Implementing HTTPS with proper certificates
  - Setting up proper authentication mechanisms
  - Configuring database backups

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Nginx Documentation](https://nginx.org/en/docs/)
