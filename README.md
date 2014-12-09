#width_bucket

Use the width bucket function for histogram binning. The output is a little strange because it shows n+2 bins. The 0th bin is how many fall below the lower_threshold and the final bin shows how many fall above the top threshold.

select width_bucket(annualsalary, lower_threshold, upper_threshold,n), count(*) from people group by 1 order by 1;