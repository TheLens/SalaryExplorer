#!/bin/bash

#!/bin/bash

echo ""
echo "Employees"
echo "---------"
echo "Number of employees in employees table:"
psql statesalaries -c "
SELECT COUNT(*)
FROM (
  SELECT DISTINCT *
  FROM employees
) AS temp;"
echo "Number of lines in data.txt:"
# Subtract 1 for header row:
cat $PYTHONPATH/data/export/data.csv | wc -l | awk '{print $1 - 1}'

echo ""
echo "Departments"
echo "-------"
echo "Number of unique departments in employees table:"
psql statesalaries -c "
SELECT COUNT(*)
FROM (
  SELECT DISTINCT department
  FROM employees
) AS temp;"
echo "Number of lines in departments.txt..."
cat $PYTHONPATH/data/export/departments.txt | wc -l | awk '{print $1 + 1}'

echo ""
echo "Offices"
echo "-------"
echo "Number of unique offices in employees table:"
psql statesalaries -c "
SELECT COUNT(*)
FROM (
  SELECT DISTINCT office
  FROM employees
) AS temp;"
echo "Number of lines in offices.txt..."
# Extra +1 because of null offices
cat $PYTHONPATH/data/export/offices.txt | wc -l | awk '{print $1 + 1 + 1}'

echo ""
echo "Positions"
echo "---------"
echo "Number of unique positions in employees table:"
psql statesalaries -c "
SELECT COUNT(*)
FROM (
  SELECT DISTINCT job_title
  FROM employees
) AS temp;"
echo "Number of lines in positions.txt..."
cat $PYTHONPATH/data/export/positions.txt | wc -l | awk '{print $1 + 1}'
