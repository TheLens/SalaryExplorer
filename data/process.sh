#This script gets static files for the app ready from the master list (starting from data from state civil service)
csvcut -c 1,2,5,8,9 La\ State\ Employee\ Listing\ -\ Data\ as\ of\ 11-7-2014.csv > essentials.csv #pull out columns you need 
csvcut -c 1 La\ State\ Employee\ Listing\ -\ Data\ as\ of\ 11-7-2014.csv > organizations.csv
csvcut -c 2 La\ State\ Employee\ Listing\ -\ Data\ as\ of\ 11-7-2014.csv > departments.csv

