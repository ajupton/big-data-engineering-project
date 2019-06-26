# Big Data Engineering Project
Hey there! Welcome to this repo where I practice building a big data engineering project. Here is a basic run down of the project:

1. Generate synthetic log data on hourly/daily basis, emulating a production system
2. Create a library of utility function for use across future ETLs
3. Create a mini data lake on S3 
4. Practice applying the big data performance optimization techniques on our tables and datasets
5. Run multiple ETL job on Amazon EMR using the S3 log data
  * ETL 1 : Daily/hourly injection job that cleans the raw logs on S3, extracts required fields and creates an incremental table
  * ETL2: Daily/hourly summary job that reads from the clean table from ETL 1 to create an aggregated table that would be updated daily/hourly
6. Incorporate Hive and Spark-SQL in ETL jobs

To accomplish all of this, we will use python, Airflow, AWS (S3 and EMR), and Spark



Props to the folks over at [ConfusedCoders](https://confusedcoders.com/) for inspiring this project
