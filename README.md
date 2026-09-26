
# ETL Pipeline

A full-stack ETL (Extract, Transform, Load) pipeline for processing
customer CSV data, cleaning and transforming it with Python/Pandas,
checking existing records in MySQL, and loading new records into the
database.

<img width="1847" height="845" alt="Screenshot From 2026-09-26 18-32-42" src="https://github.com/user-attachments/assets/114b83de-987d-4654-87ca-c07d149f3cfb" />


## Table of Contents

-   [What is ETL](#what-is-etl)
-   [How It Works](#how-it-works)
-   [Architecture](#architecture)
-   [Features](#features)
-   [Tech Stack](#tech-stack)
-   [Project Structure](#project-structure)
-   [Prerequisites](#prerequisites)
-   [Backend Setup](#backend-setup)
-   [MySQL Setup](#mysql-setup)
-   [Environment Variables](#environment-variables)
-   [Running the Backend](#running-the-backend)
-   [API Endpoint](#api-endpoint)
-   [Incremental Loading](#incremental-loading)
-   [Frontend Setup](#frontend-setup)
-   [Example Workflow](#example-workflow)
-   [Example Response](#example-response)
-   [Troubleshooting](#troubleshooting)
-   [Security](#security)

 <img width="1847" height="845" alt="Screenshot From 2026-09-26 18-32-52" src="https://github.com/user-attachments/assets/6e144b45-c4b4-48d7-9e28-0ba6ebd4f047" />


## What is ETL?

ETL stands for:

``` text
Extract → Transform → Load
```

It is a data engineering process used to collect data from a source,
clean and process it, and store the resulting data in a destination.

This project uses:

``` text
CSV File
   ↓
Extract
   ↓
Raw Data
   ↓
Transform
   ↓
Clean Data
   ↓
Check MySQL
   ↓
New Records
   ↓
Load
   ↓
MySQL
```

## How It Works

### 1. Extract

The pipeline receives a CSV file and reads it using Pandas.

``` python
df = pd.read_csv(file_path)
```

The CSV is converted into a Pandas DataFrame.

### 2. Transform

The raw data is cleaned and standardized.

The transformation stage can:

-   Remove empty rows
-   Remove duplicate records
-   Clean column names
-   Clean names
-   Standardize email addresses
-   Validate email format
-   Clean phone numbers
-   Convert age to numeric values
-   Validate age ranges
-   Convert signup dates
-   Clean city and state values
-   Clean status values
-   Handle missing values

### 3. Check Existing Records

The pipeline checks MySQL for records that already exist.

Email is used to identify existing customer records.

``` text
CSV Records
     ↓
Compare with MySQL
     ↓
Existing Records → Skip
New Records      → Continue
```

### 4. Load

Only new, cleaned records are inserted into the MySQL `customers` table.

## Architecture

``` text
                    ┌─────────────────┐
                    │    React UI     │
                    │   CSV Upload    │
                    └────────┬────────┘
                             │
                             │ HTTP
                             ▼
                    ┌─────────────────┐
                    │    FastAPI      │
                    │      API        │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │      ETL        │
                    │    Pipeline     │
                    └────────┬────────┘
                             │
                ┌────────────┼────────────┐
                ▼            ▼            ▼
            EXTRACT      TRANSFORM      LOAD
                │            │            │
                ▼            ▼            ▼
              CSV       Pandas DataFrame MySQL
```

## Features

-   CSV file upload
-   CSV data extraction
-   Data cleaning and transformation
-   Duplicate removal
-   Email validation
-   Phone number cleaning
-   Age validation
-   Date conversion
-   Missing-value handling
-   MySQL integration
-   Existing-record detection
-   Incremental loading
-   REST API with FastAPI
-   React frontend integration
-   Environment-based database configuration
-   ETL processing statistics

## Tech Stack

### Frontend

-   React
-   JavaScript
-   Vite

### Backend

-   Python
-   FastAPI
-   Pandas

### Database

-   MySQL

### Database Libraries

-   SQLAlchemy
-   PyMySQL

### Configuration

-   python-dotenv

## Project Structure

``` text
ETL-Project/
│
├── backend/
│   ├── etl.py
│   ├── main.py
│   ├── .env
│   └── uploads/
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── ...
│
├── .gitignore
└── README.md
```

## Prerequisites

Install:

-   Python 3.10+
-   Node.js
-   npm
-   MySQL Server
-   Git

Check versions:

``` bash
python3 --version
node --version
npm --version
mysql --version
```

## Backend Setup

Navigate to the backend:

``` bash
cd backend
```

Create a virtual environment:

``` bash
python3 -m venv .venv
```

Activate it on Linux/macOS:

``` bash
source .venv/bin/activate
```

Install dependencies:

``` bash
pip install fastapi uvicorn pandas sqlalchemy pymysql python-dotenv python-multipart
``

## MySQL Setup

Start MySQL:

``` bash
sudo systemctl start mysql
```

Check MySQL:

``` bash
sudo systemctl status mysql
```

Log in:

``` bash
mysql -u root -p
```

Create the database:

``` sql
CREATE DATABASE etlpipeline;
```

Select it:

``` sql
USE etlpipeline;
```

Create the customer table:

``` sql
CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20),
    city VARCHAR(100),
    state VARCHAR(100),
    age INT,
    signup_date DATE,
    status VARCHAR(50),
    notes TEXT
);
```

Check the table:

``` sql
DESCRIBE customers;
```

## Environment Variables

Create `.env` inside `backend/`:

``` dotenv
DB_HOST=localhost
DB_PORT=3306
DB_USER=admin
DB_PASSWORD=your_mysql_password
DB_NAME=etlpipeline
```

The database password should be kept in `.env` rather than inside Python
source code.

## Running the Backend

From the backend directory:

``` bash
uvicorn main:app --reload
```

The API runs at:

``` text
http://localhost:8000
```

FastAPI documentation:

``` text
http://localhost:8000/docs
```

## API Endpoint

### Upload CSV

``` http
POST /upload
```

Example:

``` bash
curl -X POST   -F "file=@customers.csv"   http://localhost:8000/upload
```

The endpoint:

``` text
Receive CSV
     ↓
Save temporary file
     ↓
Extract
     ↓
Transform
     ↓
Check MySQL
     ↓
Find new records
     ↓
Load into MySQL
     ↓
Return JSON response
```

## Incremental Loading

The pipeline checks existing MySQL records before inserting new data.

``` text
               CSV
                │
                ▼
         Clean DataFrame
                │
                ▼
       Existing MySQL Data
                │
                ▼
        Compare email
          /                   /                Existing          New
       │               │
       ▼               ▼
     Skip             Load
                       │
                       ▼
                     MySQL
```

For example, if MySQL contains:

``` text
rahul@example.com
amit@example.com
```

and the new CSV contains:

``` text
rahul@example.com
amit@example.com
priya@example.com
neha@example.com
```

the pipeline identifies:

``` text
rahul@example.com → Existing
amit@example.com  → Existing
priya@example.com → New
neha@example.com  → New
```

Only the new records are loaded.

## Database Loading

SQLAlchemy is used to connect Python to MySQL:

``` python
URL.create(
    drivername="mysql+pymysql",
    username=...,
    password=...,
    host=...,
    port=...,
    database=...
)
```

The DataFrame is loaded with:

``` python
df.to_sql(
    "customers",
    con=engine,
    if_exists="append",
    index=False
)
```

## Frontend Setup

Navigate to the frontend:

``` bash
cd frontend
```

Install dependencies:

``` bash
npm install
```

Start the development server:

``` bash
npm run dev
```

The frontend normally runs at:

``` text
http://localhost:5173
```

The frontend sends the selected CSV to:

``` text
http://localhost:8000/upload
```

## Example Workflow

Start MySQL:

``` bash
sudo systemctl start mysql
```

Start the backend:

``` bash
cd backend
source .venv/bin/activate
uvicorn main:app --reload
```

Start the frontend in another terminal:

``` bash
cd frontend
npm install
npm run dev
```

Open:

``` text
http://localhost:5173
```

Upload a CSV file.

The pipeline processes it as:

``` text
Upload
  ↓
Extract
  ↓
Transform
  ↓
Check MySQL
  ↓
Find New Records
  ↓
Load
```

Verify the data:

``` sql
USE etlpipeline;

SELECT * FROM customers;
```

## Example Response

A successful request can return:

``` json
{
    "filename": "customers.csv",
    "success": true,
    "message": "ETL pipeline completed successfully",
    "extracted_records": 100,
    "cleaned_records": 70,
    "removed_records": 30,
    "existing_records": 20,
    "loaded_records": 50
}
```

The values depend on the uploaded CSV and existing database records.

## Troubleshooting

### MySQL connection error

Check:

``` bash
sudo systemctl status mysql
```

Verify `.env`:

``` dotenv
DB_HOST=localhost
DB_PORT=3306
DB_USER=admin
DB_PASSWORD=your_password
DB_NAME=etlpipeline
```

Test login:

``` bash
mysql -u admin -p
```

### Database does not exist

``` sql
CREATE DATABASE etlpipeline;
```

### Table does not exist

``` sql
CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20),
    city VARCHAR(100),
    state VARCHAR(100),
    age INT,
    signup_date DATE,
    status VARCHAR(50),
    notes TEXT
);
```

### Port 8000 is already in use

``` bash
uvicorn main:app --reload --port 8001
```

Update the frontend API URL if required.

### CSV file is rejected

Make sure the file has a `.csv` extension and includes the required
fields:

``` text
name
email
```

Other supported fields include:

``` text
phone
city
state
age
signup_date
status
notes
```

## Security

Do not commit database credentials to GitHub.

Add the following to `.gitignore`:

``` text
.env
.venv/
__pycache__/
uploads/
```

Keep credentials in `.env`:

``` dotenv
DB_PASSWORD=your_password
```

## Future Improvements

-   Scheduled ETL jobs
-   Batch processing for large datasets
-   Data quality reports
-   Logging and monitoring
-   Retry mechanisms
-   Multiple data sources
-   PostgreSQL support
-   Cloud storage integration
-   Data validation rules
-   ETL job history
-   Background task processing
-   Authentication and authorization
-   Docker deployment
-   Production database migrations

## Author

**Abhijeet Verma**

### Project Technologies

``` text
Python
Pandas
ETL
FastAPI
React
MySQL
SQLAlchemy
REST API
Data Cleaning
Incremental Data Loading
```
