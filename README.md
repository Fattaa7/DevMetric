# DevMetrics

**DevMetrics** is a backend API that logs developer activity and exposes metrics such as commit logs, bug reports, and task completions. Built with FastAPI, PostgreSQL, and Docker, it’s designed for scalable, efficient backend service monitoring developer productivity and project health.

---

## Features

### Current

- **Activity Logging:** Capture and store developer activities including commits, bug reports, and task updates.
- **Metrics API:** Expose endpoints that return detailed developer and project metrics.
- **Authentication:** JWT-based authentication and authorization.
- **Database:** PostgreSQL backend with Alembic migrations for schema management.
- **Dockerized:** Containerized setup for easy deployment and environment consistency.
- **Async Endpoints:** FastAPI async support for high throughput and scalability.
- **Git Hooks Integration:** Automate code quality checks, linting, formatting, and tests on commit/push to maintain codebase health.
- **Error Handling:** Centralized, structured error responses with clear HTTP status codes.
- **Logging:** Integrated logging for debugging and operational visibility.

---

## Getting Started

1. Clone the repository

   ```bash
   git clone https://github.com/Fattaa7/DevMetric.git
   cd DevMetric
   ```

2. Set up a Python virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. On Windows (CMD):

   ```bash
   python -m venv venv
   venv\Scripts\activate.bat
   ```

4. Install project dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Configure your PostgreSQL database connection by creating a .env file in the project root and adding your database credentials, for example:

   ```bash
   DATABASE_URL=postgresql://user:password@localhost:5432/devmetrics
   ```

6. Start the FastAPI development server:
   ```bash
   uvicorn app.main:app --reload
   ```

---

## Docker Setup

1. Build image

   ```bash
   docker build -t devmetrics .
   ```

2. Run container
   ```bash
   docker run -p 8000:8000 --env-file .env devmetrics
   ```
