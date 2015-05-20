aws s3 cp index.html s3://lensnola/salaryexplorer/index.html --acl public-read
aws s3 cp js/ s3://lensnola/salaryexplorer/js/ --acl public-read --recursive
aws s3 cp css/ s3://lensnola/salaryexplorer/css/ --acl public-read --recursive
aws s3 cp data/ s3://lensnola/salaryexplorer/data/ --acl public-read --recursive