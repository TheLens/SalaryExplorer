#This script gets static files for the app ready from the master list (starting from data from state civil service)
csvcut -c 1,2,5,8,9 La\ State\ Employee\ Listing\ -\ Data\ as\ of\ 5-15-2015.csv > all.csv #pull out columns you need 
csvcut -c 1 La\ State\ Employee\ Listing\ -\ Data\ as\ of\ 5-15-2015.csv | sort | uniq > organizations.csv
csvcut -c 2 La\ State\ Employee\ Listing\ -\ Data\ as\ of\ 5-15-2015.csv | sort | uniq > departments.csv
csvcut -c 8 La\ State\ Employee\ Listing\ -\ Data\ as\ of\ 5-15-2015.csv | sort | uniq > positions.csv

python tsvprocessor.py

rm organizations.csv.gz
rm departments.csv.gz
rm positions.csv.gz

gzip all.tsv
gzip positions.csv
gzip departments.csv
gzip organizations.csv

aws s3 cp all.tsv.gz s3://lensnola/salaryexplorer/data/all.tsv.gz --acl public-read --content-type text/plain --content-encoding gzip
aws s3 cp positions.csv.gz s3://lensnola/salaryexplorer/data/positions.csv.gz --acl public-read --content-type text/plain --content-encoding gzip
aws s3 cp departments.csv.gz s3://lensnola/salaryexplorer/data/departments.csv.gz --acl public-read --content-type text/plain --content-encoding gzip
aws s3 cp organizations.csv.gz s3://lensnola/salaryexplorer/data/organizations.csv.gz --acl public-read --content-type text/plain --content-encoding gzip