#!/bin/bash

echo "Export employees' departments to departments.csv.."
psql statesalaries -c "COPY (
  SELECT DISTINCT department
  FROM employees
  ORDER BY department ASC
) to '$PYTHONPATH/data/intermediate/departments.csv' WITH CSV HEADER;"
sed -i '' 1d $PYTHONPATH/data/intermediate/departments.csv

echo "Export employees' offices to offices.csv.."
psql statesalaries -c "COPY (
  SELECT DISTINCT office
  FROM employees
  ORDER BY office ASC
) to '$PYTHONPATH/data/intermediate/offices.csv' WITH CSV HEADER;"
sed -i '' 1d $PYTHONPATH/data/intermediate/offices.csv

echo "Export employees' job titles to positions.csv.."
psql statesalaries -c "COPY (
  SELECT DISTINCT job_title
  FROM employees
  ORDER BY job_title ASC
) to '$PYTHONPATH/data/intermediate/positions.csv' WITH CSV HEADER;"
sed -i '' 1d $PYTHONPATH/data/intermediate/positions.csv

echo "Export final output with employees, salaries and job information to data.csv.."
psql statesalaries -c "COPY (
  SELECT last_name,
         first_name,
         salary,
         job_title,
         office
  FROM employees
  ORDER BY last_name ASC
) to '$PYTHONPATH/data/export/data.csv' WITH CSV HEADER;"

echo "Find the highest 25 salaries from data table and export to highest-paid.csv..."
psql statesalaries -c "COPY (
  SELECT last_name,
         first_name,
         salary,
         job_title,
         department
  FROM employees
  ORDER BY salary DESC
  LIMIT 25
) to '$PYTHONPATH/data/export/highest-paid.csv' WITH CSV HEADER;"

echo "Copying .csv files to .txt files..."
cp $PYTHONPATH/data/intermediate/departments.csv $PYTHONPATH/data/export/departments.txt
cp $PYTHONPATH/data/intermediate/offices.csv $PYTHONPATH/data/export/offices.txt
cp $PYTHONPATH/data/intermediate/positions.csv $PYTHONPATH/data/export/positions.txt

echo "Removing double quotes in .txt files..."
# Linux (GNU) and Mac (BSD) compatible sed commands:
sed -i.bak 's/^"//g' $PYTHONPATH/data/export/departments.txt
sed -i.bak 's/"$//g' $PYTHONPATH/data/export/departments.txt

sed -i.bak 's/^"//g' $PYTHONPATH/data/export/offices.txt
sed -i.bak 's/"$//g' $PYTHONPATH/data/export/offices.txt

sed -i.bak 's/^"//g' $PYTHONPATH/data/export/positions.txt
sed -i.bak 's/"$//g' $PYTHONPATH/data/export/positions.txt

echo "Deleting empty lines in .txt files..."
sed -i.bak '/^$/d' $PYTHONPATH/data/export/departments.txt
sed -i.bak '/^$/d' $PYTHONPATH/data/export/offices.txt
sed -i.bak '/^$/d' $PYTHONPATH/data/export/positions.txt

echo "Removing newline characters at the end of .txt files..."
# Find byte size of file, subtract 1 (for end of line character), then redirect everything up until that last byte to a temporary .bak file
head -c $(wc -c $PYTHONPATH/data/export/departments.txt | awk '{print $1 - 1}') $PYTHONPATH/data/export/departments.txt > $PYTHONPATH/data/export/departments.bak
head -c $(wc -c $PYTHONPATH/data/export/offices.txt | awk '{print $1 - 1}') $PYTHONPATH/data/export/offices.txt > $PYTHONPATH/data/export/offices.bak
head -c $(wc -c $PYTHONPATH/data/export/positions.txt | awk '{print $1 - 1}') $PYTHONPATH/data/export/positions.txt > $PYTHONPATH/data/export/positions.bak

cat $PYTHONPATH/data/export/departments.bak > $PYTHONPATH/data/export/departments.txt
cat $PYTHONPATH/data/export/offices.bak > $PYTHONPATH/data/export/offices.txt
cat $PYTHONPATH/data/export/positions.bak > $PYTHONPATH/data/export/positions.txt

echo "Copying .csv and .txt files..."
cp $PYTHONPATH/data/export/data.csv $PYTHONPATH/data/export/data-backup.csv
cp $PYTHONPATH/data/export/highest-paid.csv $PYTHONPATH/data/export/highest-paid-backup.csv

cat $PYTHONPATH/data/export/departments.txt > $PYTHONPATH/data/export/departments-backup.txt
cat $PYTHONPATH/data/export/offices.txt > $PYTHONPATH/data/export/offices-backup.txt
cat $PYTHONPATH/data/export/positions.txt > $PYTHONPATH/data/export/positions-backup.txt

echo "Removing any pre-existing .gz files..."
rm $PYTHONPATH/data/export/*.gz

echo "gzip .csv and .txt files..."
gzip -9 $PYTHONPATH/data/export/data.csv
gzip -9 $PYTHONPATH/data/export/highest-paid.csv

gzip -9 $PYTHONPATH/data/export/departments.txt
gzip -9 $PYTHONPATH/data/export/offices.txt
gzip -9 $PYTHONPATH/data/export/positions.txt

echo "Copying .csv and .txt backup files back to original filenames..."
cp $PYTHONPATH/data/export/data-backup.csv $PYTHONPATH/data/export/data.csv
cp $PYTHONPATH/data/export/highest-paid-backup.csv $PYTHONPATH/data/export/highest-paid.csv

cat $PYTHONPATH/data/export/departments-backup.txt > $PYTHONPATH/data/export/departments.txt
cat $PYTHONPATH/data/export/offices-backup.txt > $PYTHONPATH/data/export/offices.txt
cat $PYTHONPATH/data/export/positions-backup.txt > $PYTHONPATH/data/export/positions.txt

echo "Deleting backup files..."
rm $PYTHONPATH/data/export/*-backup.csv
rm $PYTHONPATH/data/export/*-backup.txt

echo "Deleting temporary .bak files..."
rm $PYTHONPATH/data/export/*.bak
