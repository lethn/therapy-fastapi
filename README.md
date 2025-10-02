# Therapy FastAPI

### Project Description: 
Therapy FastAPI is an application that manages therapists and patients, built with FastAPI, PostgreSQL, and SQLAlchemy ORM. The app allows creating and retrieving therapists and patients, assigning therapists to patients (many-to-many relationship), and retrieving all patients for a given therapist.

---

### Features:
+ Create and retrieve Therapists
+ Create and retrieve Patients
+ Assign therapists to patients (many-to-many relationship)  
+ Retrieve all patients for a given therapist  
+ PostgreSQL database integration with SQLAlchemy ORM  
+ API documentation available via Swagger UI at `/docs`  
+ Dockerized for local development and easy setup  

---

### Setup Application:
1. Clone this repository
2. Navigate to the therapy-fastapi directory: `cd therapy-fastapi`
3. Create and activate virtual environment (recommended)
  ```bash
  python -m venv venv

  # On Windows
  .\venv\Scripts\activate

  # On macOS/Linux
  source venv/bin/activate
  ```
4. Install dependencies
  ```bash
  pip install -r requirements.txt
  ```
5. Create a `.env` file (see `.env.example`) with
 ```env
 POSTGRES_USER=postgres
 POSTGRES_PASSWORD=12345678
 POSTGRES_DB=therapy_fastapi

 # For localhost
 DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:5432/${POSTGRES_DB}
 # For Docker
 DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}
 ```
**Important:**  
- When running **Locally**, uncomment the `localhost` line and comment out the `db` line
- When running with **Docker Compose**, uncomment the `db` line and comment out the `localhost` line

---

### Running Application:

**Option 1: Run with Docker**
  ```bash
  docker compose down -v   # Optional: Reset database
  docker compose up --build
  ```
Access at:  
- Base URL: [http://localhost:8000](http://localhost:8000)  
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)  

##

**Option 2: Run Locally (without Docker)**
1. Make sure PostgreSQL is running on your machine at `localhost:5432`.  
2. Update `.env` to use the **localhost** `DATABASE_URL`.  
3. Install dependencies:  
  ```bash
  pip install -r requirements.txt
  ```
4. Run FastAPI server with either
  ```bash
  # Option 1: Uvicorn
  uvicorn main:app --reload
  
  # Option 2: FastAPI CLI
  fastapi dev main.py
  ```
5. Access at:  
- Base URL: [http://localhost:8000](http://localhost:8000)  
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)   

---

### Example API Requests
**Create a therapist**
```bash
curl -X POST http://localhost:8000/therapists \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice","age":40,"specialty":"Physical Therapy"}'
```
**Create a patient**
```bash
curl -X POST http://localhost:8000/patients \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","age":30}'
```
**Assign therapist to patient**
```bash
curl -X PUT http://localhost:8000/patients/1/assign/1
```

