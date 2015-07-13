#!/bin/bash

# Setup database
echo "Force users to quit statesalaries database session..."
psql statesalaries -c "
SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE datname = current_database()
  AND pid <> pg_backend_pid();"

echo "Drop statesalaries database if it exists..."
dropdb --if-exists statesalaries

echo "Create statesalaries database..."
createdb statesalaries

# Define database layout
echo "Create employees table..."
# python make_db.py
psql statesalaries -c "
CREATE TABLE employees (
    department      varchar(100),
    office          varchar(100),
    parish          varchar(50),
    employee_id     varchar(8),
    full_name       varchar(100),
    classification  varchar(50),
    employee_status varchar(50),
    job_title       varchar(50),
    salary          numeric(9, 2),
    date_hired      date,
    last_name       varchar(50),
    first_name      varchar(50),
    middle_name     varchar(15)
);"

# CSVs that were generated from LDOE's Excel file:

echo "Import salaries.csv to employees table..."
psql statesalaries -c "
COPY employees (
  department,
  office,
  parish,
  employee_id,
  full_name,
  classification,
  employee_status,
  job_title,
  salary,
  date_hired,
  last_name,
  first_name,
  middle_name
)
FROM '$PYTHONPATH/data/intermediate/salaries.csv'
DELIMITER ',' CSV HEADER;"
