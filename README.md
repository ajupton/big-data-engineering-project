# Big Data Engineering Project
Hey there! Welcome to this repo where I practice building a big data engineering project. Here is a basic run down of the project:

# Problem Statement
Retailers in the current landscape are adapting to the digital age. Digital behemoths like Amazon and Ebay have carved out substantial market shares in the online space at the same time that traditional retail venues are in decline. In this time of flux, an omni-channel approach is necessary. This is especially true for retailers that have invested in an extensive brick-and-mortar portfolio and strong relationships with brick-and-mortar partners. 

This data engineering project uses a real world retail dataset to explore delivery performance at scale. The primary concern of data engineering efforts in this project is to create a strong foundation onto which data analytics and modeling may be applied as well as provide summary reports for daily ingestion by decision makers. 

# Dataset of choice
The dataset of choice for this project is a series of tables [provided by the Brazilian Ecommerce company Olist](https://www.kaggle.com/olistbr/brazilian-ecommerce/home#olist_orders_dataset.csvhttps://www.kaggle.com/olistbr/brazilian-ecommerce/home#olist_orders_dataset.csv). The table schema is provided here:

![](https://i.imgur.com/HRhd2Y0.png)

# Methodology:
1. Construct a mock production database replete with a table schema that can be updated hourly/daily 
2. Create a library of utility functions for use across current and future ETLs
3. Populate a mini data lake on S3 
4. Use big data performance optimization techniques to analyze the tables and prepare them for ETL jobs
5. Build ETL pipelines to extract data from the lake, clean and transform it, and load it into a mini data warehouse on the same S3 bucket
  * ETL 1 : Hourly/daily injection job that cleans the tables on S3, extracts/combines required fields and creates an incremental table
  * ETL 2 : Hourly/daily summary job that reads from the clean table from ETL 1 to create an aggregated table for ingestion in a daily report
  * ETL 3: Daily feature engineering job that extracts features from multiple tables, cleans them up, and prepares them for ingestion in a data modeling task related to delivery performance
6. Incorporate Hive and Spark-SQL in ETL jobs

To accomplish all of this, we will use python, Airflow, AWS (S3 and EMR), and Spark

## Step 1: Setup an AWS S3 Bucket
Setting up an S3 bucket is pretty straightforward, and the current 5 GB free tier limit for 12 months is a great way to get started with AWS S3 without having to break the bank. Simply create an AWS account, click on Services in the upper left hand side, navigate to Storage and select S3. From there you'll be able to create a new S3 bucket following the prompts and inputing settings based on your unique needs. I largely followed the default options. Once created, simply select the bucket and in the Overview tab, there are options to upload object/files, create folders, or set permissions. Alternatively, it's possible to install AWS Cli to your machine in order to transfer files at the command line. [See here for a brief overview of transferring files to an S3 bucket using AWS Cli](https://confusedcoders.com/data-engineering/how-to-copy-kaggle-data-to-amazon-s3).

## Step 2: Library of ETL Utility functions
At it's heart, ETL (extract, transform, load) is all about automation. ETL jobs take data from a variety of sources, combine the data, manipulate the data, clean the data, and finally load the data into a data warehouse or analytics suite for ingestion by analysts, data scientists, or decision makers. Along the way, quality checks are performed and the process is monitored to ensure that all the pieces parts have operated as intended. This kind of process would be a burden to manually code and oversee for each batch. ETL is therefore an exercise in automation. As essential part of automation is the writing of utility functions to handle the different aspects of an ETL pipeline. It's important to break each utility function into individual components instead of writing all-encompassing functions because not only are they easier to maintain this way but individual utility functions can be more easily integrated as operators into ETL schedulers like Apache Airflow, Luigi, or others. 

## Step 3: Populate a mini data lake on S3
A meaningful data engineering project requires motivation and dedication to see all the way through. Because of this, it's really important to find a dataset or datasets that a truly interesting to the aspiring data engineer. Additionally, a solid data engineering project must lead to the creation of value for an organization. In that regard, the specific technologies are generally of less interest than the problem statement and the outcome. While technologies will change, the underlying data foundations that data engineers are unlikely to dramatically change significantly in the near term future. 

Sports data, home inventory/sales data, and tweets are examples of data that can lead to strong data engineering projects because they are updated frequently, large in size and scope, require lots of post-processing, and are often topically driven around the interests of aspiring data engineers. 

There are two general ways to upload data onto S3. The first is to use the GUI tool in the S3 interface. This is all manual and as a result isn't something that a good data engineer would want to use. Instead, the AWS CLI (command line interface) is preferred. [You can find out more about installing the AWS CLI here.](https://aws.amazon.com/cli/) In short, you'll need to install the AWS CLI using `pip install awscli --upgrade --user` [and then configure your credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html).

Once your AWS CLI credentials are input, it's easy to copy (or cp) files onto it from the terminal using the following syntax: `aws s3 cp <local file path> <s3 path>`  e.g. `aws s3 cp ~/file_to_upload.csv s3://s3-bucket-name/folder_path/`

In general, data lakes are populated with data that was created in an OLTP (or online transaction processing) system. These kinds of systems are, in essence, what drive data collection in modern industry. They are designed to be fast and reliable above all else in processing transactions. These systems take orders, sign up new customers, record shipments, log comments and complaints, etc. As a result, they aren't optimized for analytics (or OLAP). The objective of OLAP systems are getting the data from the OLTP out and in such a way as to make it amenable for digestion by analytics platforms like Tableau dashboards or TensorFlow deep learning models. Our objective here is to create data pipelines that take in messy OLTP data, transform it, and load it into a nice neat data warehouse. 

## Step 4: Let's do some analytics
One of the strongest skillsets needed by a data engineer is communication. That communication needs to be flexed primarily in conversations with stakeholders that will consume the data at the end of the ETL and stream pipelines that data engineers construct. Data engineers often need to rely on the domain expertise of analysts, data scientists, program managers, executives, and others in order to understand what specific data features are needed for various analytics applications. That said, data engineers still need to possess strong EDA (exploratory data analysis) chops in order to deliver data sets that meet the needs of various stakeholders. As a result, it's very often worthwhile for the data engineer to get down and dirty with the data in the data lake through data visualization, the computing of summary statistics, and other exploratory methods. 

My go-to tool of choice in this regard is a Jupyter notebook using python, numpy, pandas, altair/seaborn/matplotlib/plotly, and other python packages. For data that is truly 'big' and can't fit in memory of a single machine, Spark becomes invaluable. Of course, this analytics approach is possible in all sorts of AWS services like Athena and EMR, it can often be worthwhile to take samples of data from the data lake and get some EDA in to get a feel for the tables and schema. 

## Step 5: Get hands-on with Airflow 
There are many tools out there to run big data ETL jobs that turn messy data lakes into analytics-ready data warehouses. Here, I'll focus on one of the most popular open source ETL tools currently available - Apache Airflow. [Check out the Airflow docs here](https://airflow.apache.org/index.html). First, get Airflow installed with `pip install apache-airflow`. Make sure to include the 'apache' part there, or you'll download an older version of Airflow that will lead to a whole lot of problems down the line. 



## More steps on the way!




Props to the folks over at [ConfusedCoders](https://confusedcoders.com/) for inspiring this project
