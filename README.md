# Big Data Engineering Project
Hey there! Welcome to this repo where I practice building a big data engineering project. Here is a basic run down of the project:

1. Generate synthetic log data on hourly/daily basis, emulating a production system
2. Create a library of utility functions for use across current and future ETLs
3. Populate a mini data lake on S3 
4. Practice applying the big data performance optimization techniques on our tables and datasets
5. Run multiple ETL job on Amazon EMR using the S3 log data
  * ETL 1 : Daily/hourly injection job that cleans the raw logs on S3, extracts required fields and creates an incremental table
  * ETL 2 : Daily/hourly summary job that reads from the clean table from ETL 1 to create an aggregated table that would be updated daily/hourly
6. Incorporate Hive and Spark-SQL in ETL jobs

To accomplish all of this, we will use python, Airflow, AWS (S3 and EMR), and Spark



Props to the folks over at [ConfusedCoders](https://confusedcoders.com/) for inspiring this project


## Step 1: Setup an AWS S3 Bucket
Setting up an S3 bucket is pretty straightforward, and the current 5 GB free tier limit for 12 months is a great way to get started with AWS S3 without having to break the bank. Simply create an AWS account, click on Services in the upper left hand side, navigate to Storage and select S3. From there you'll be able to create a new S3 bucket following the prompts and inputing settings based on your unique needs. I largely followed the default options. Once created, simply select the bucket and in the Overview tab, there are options to upload object/files, create folders, or set permissions. Alternatively, it's possible to install AWS Cli to your machine in order to transfer files at the command line. [See here for a brief overview of transferring files to an S3 bucket using AWS Cli](https://confusedcoders.com/data-engineering/how-to-copy-kaggle-data-to-amazon-s3).

## Step 2: Library of ETL Utility functions
At it's heart, ETL (extract, transform, load) is all about automation. ETL jobs take data from a variety of sources, combine the data, manipulate the data, clean the data, and finally load the data into a data warehouse or analytics suite for ingestion by analysts, data scientists, or decision makers. Along the way, quality checks are performed and the process is monitored to ensure that all the pieces parts are operated as intended. This kind of process would be a burden to manually code and oversee for each batch process. ETL is therefore an exercise in automation. As essential part of automation is the writing of utility functions to handle the different aspects of an ETL pipeline. It's important to break each utility function into individual components instead of writing all-encompassing functions because not only are they easier to maintain this way but individual utility functions can be more easily integrated into ETL schedulers like Apache Airflow, Luigi, and others. 
