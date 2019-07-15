# 'Little' Big Data Engineering Project
Hey there! Welcome to this repo where I practice building a big data engineering project. Here is a basic run down of the project:

# Problem Statement
Retailers in the current landscape are adapting to the digital age. Digital retail behemoths have carved out substantial market shares in the online space at the same time that traditional retail stores are broadly in decline. In this time of digital flux, an omni-channel retail approach is necessary to keep pace. This is especially true for retailers that have invested in an extensive brick-and-mortar store portfolio or have strong relationships with brick-and-mortar partners. 

This data engineering project uses a real world retail dataset to explore delivery performance at scale. The primary concern of data engineering efforts in this project is to create a strong foundation onto which data analytics and modeling may be applied as well as provide summary reports for daily ingestion by decision makers. 

A series of ETL jobs are programmed as part of this project using python, SQL, Airflow, and Spark to build pipelines that download data from an AWS S3 bucket, apply some manipulations, and then load the cleaned-up data set into another location on the same AWS S3 bucket for higher level analytics. 

# Dataset of choice
The dataset of choice for this project is a series of tables [provided by the Brazilian Ecommerce company Olist](https://www.kaggle.com/olistbr/brazilian-ecommerce/home#olist_orders_dataset.csvhttps://www.kaggle.com/olistbr/brazilian-ecommerce/home#olist_orders_dataset.csv). The table schema is provided here:

![](https://i.imgur.com/HRhd2Y0.png)

# Methodology:
1. Construct a mock production data lake in AWS S3 replete with the table schema above
2. Analyze the tables with an eye toward identifying the delivery performance of Olist orders/sellers 
3. Write a Spark and Spark SQL job to join together tables answering the question, "Which orders/sellers missed the deadline imposed by Olist for when their packages need to be delivered to a carrier?"
4. Build an ETL pipeline using Airflow that accomplishes the following:
* Downloads data from an AWS S3 bucket
* Runs a Spark/Spark SQL job on the downloaded data producing a cleaned-up dataset of delivery deadline missing orders
* Upload the cleaned-up dataset back to the same S3 bucket in a folder primed for higher level analytics

I'll provide an overview of each of these steps but assume that the reader is already somewhat familiar with python, SQL, Airflow, and Spark. 

## Step 1: Setup and populate an AWS S3 Bucket
Setting up an S3 bucket is pretty straightforward, and the current 5 GB free tier limit for 12 months is a great way to get started with AWS S3 without having to break the bank. Simply create an AWS account, click on "Services" in the upper left hand side, navigate to "Storage" and select S3. From there you'll be able to create a new S3 bucket following the prompts and inputing settings based on your unique needs. I largely followed the default options. Once created, simply select the bucket and in the Overview tab, there are options to upload objects/files, create folders, or set permissions. Alternatively, it's possible to install AWS Cli to your machine in order to transfer files at the command line. 

The method for interacting with S3 taken here uses the [python library boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html). boto3 has all sorts of functions for interacting with products across the AWS landscape using python. 

We'll use boto3 as part of python scripts to both download the Brazilian ecommerce data to our S3 bucket as well upload the csv file that results from the Spark job back into the S3 bucket. 

In reality, a data lake often consists of various SQL tables or log files, which are often billions of rows long. The Brazilian ecommerce data used here comes in a zip file that contains 9 different csv files as seen schema above. This gets sort of close to a data lake format but in a way that's amenable for practicing and learning. 

## Step 2: Analyze the tables with an eye toward identifying the delivery performance of Olist orders/sellers 
One of the strongest skillsets needed by a data engineer is communication. That communication needs to be flexed primarily in conversations with stakeholders that manage data sets as well as stakeholders that will consume the data at the end of the ETL and stream pipelines that data engineers construct. Data engineers often need to rely on the domain expertise of analysts, data scientists, program managers, executives, and others in order to understand what specific data features are needed for various analytics applications. That said, data engineers still need to possess strong EDA (exploratory data analysis) chops in order to deliver data sets that meet the needs of various stakeholders. As a result, it's very often worthwhile for data engineers to get down and dirty with the data in the data lake through data visualization, the computing of summary statistics, and other exploratory methods. 

My go-to tool of choice in this regard is a Jupyter notebook using python. A typical workflow involes using SQLAlchemy or the pyspark API to connect to a database and pull data with some pythonic SQL and then use numpy, pandas, altair/seaborn/matplotlib/plotly, and other python packages for visualization, the computing of summary statitistics, maybe running a few statistical models, and other EDA techniques. For data that is truly 'big' and can't fit in memory on a single machine, Spark becomes invaluable. Spark SQL makes pulling and manipulating data a breeze as well for those with SQL chops. Of course, this analytics approach is possible in all sorts of AWS services like Athena and EMR among many others. With massive volumes of data, it can often be worthwhile to take samples of data from the data lake and get some EDA in to get a feel for the tables and schema as well as to understand the quirks of the data. OLTP processes often must follow multiple business rules that make it a major challenge to do things like join disparate datasets, hammer down ground-truth insights, or compare current and historical trends.  

Some very basic EDA is applied on the database tables to answer the question "Which orders/sellers missed the deadline imposed by Olist for when their packages need to be delivered to a carrier?". [See the code here or navigate to `Data` -> Brazilian ecommerce.ipynb](https://github.com/ajupton/big-data-engineering-project/blob/master/Data/Brazilian%20ecommerce%20EDA%20.ipynb)

## Step 3: Get hands-on with Airflow 
There are many tools out there to run big data ETL jobs that turn messy data lakes into analytics-ready data warehouses. Here, I'll focus on one of the most popular open source ETL tools currently available - Apache Airflow. [Check out the Airflow docs here](https://airflow.apache.org/index.html). First, install Airflow  with `pip install apache-airflow`. Make sure to include the 'apache' part there, or you'll download an older version of Airflow that will lead to a whole lot of problems down the line. 

_Note:_ It can often be worthwhile to run Airflow in a Docker container. There are some major advantages to using a Docker container such as: 
* creating a fully reproducible data analysis in Jupyter notebooks or other dev platforms (something that's less trivial than you might think) 
* having fully documented dependencies (a Dockerfile contains descriptions of all the packages/files/stuff that your container needs to run) 
* having an isolated environment to work in that ensures your tools don't conflict with each other AND recreates the conditions in development, testing, staging, or production environments to ensure your code will run as expected
* not having to start from scratch by taking advantage of DockerHub container 'templates' 

Here are a few resources to help you get started with Airflow:
* [Airflow quickstart guide](http://airflow.apache.org/start.html)
* [ETL Best Practices with Airflow](https://gtoonstra.github.io/etl-with-airflow/index.html)
* [Developing Workflows with Apache Airflow](http://michal.karzynski.pl/blog/2017/03/19/developing-workflows-with-apache-airflow/)
* [Getting Started with Airflow Using Docker](https://towardsdatascience.com/getting-started-with-airflow-using-docker-cd8b44dbff98)
* [Basic DAG Configuration](https://adataguru.net/basic-dag-configuration/)

Once you have Airflow installed and are able to run through a HelloWorld dag, you're ready for the next step. 

Airflow is all about writing python scripts to create data pipelines. There are two primary scripts that need to be written for this purpose. The first are dags and the second are operators. No analytics or processing occurs in dags, which encompass the processes or steps involved in developing a pipeline. The actual analytics live in various scripts that are run as per instructed in the dags. 

[The late_shipments_to_carrier.py dag includes the three steps needed to complete our pipeline as defined above.]( https://github.com/ajupton/big-data-engineering-project/blob/master/airflow/dags/late_shipments_to_carrier_dag.py)

The first step is downloading the brazilian-ecommerce.zip file from your S3 bucket. [The script to accomplish this task is found here.](https://github.com/ajupton/big-data-engineering-project/blob/master/airflow/scripts/s3_download.py)

The next step is to run a Spark SQL job to do a pretty simply join of three relations and filter for orders/sellers that missed the delivery deadline to get their package to a designated carrier for shipment to the consumer. [This script first unzips the dataset, then sets up a Spark session, runs a simple Spark SQL operation, and then writes the results of the Spark SQL operation to a single csv file.](https://github.com/ajupton/big-data-engineering-project/blob/master/airflow/scripts/spark_missed_deadline_job.py)

Finally, the dataset identifying orders that missed the carrier delivery deadline is uploaded to the same S3 bucket in a different folder. [This script also screens out non-csv files from being uploaded to keep the folder fairly clean.](https://github.com/ajupton/big-data-engineering-project/blob/master/airflow/scripts/s3_upload.py)

To run the job, make sure to first edit the paths of each of the scripts to match the paths where you'd like to run your analysis on your own machine and of course make sure to include the specific details of your S3 bucket. 

One thing to note about the scripts is the `.set_upstream()` method applied to the second two operators. This ensures that if, for any reason, the initial file download fails that Airflow will retry the jobs. Another thing to note about the dag is the schedule, which I'm manually triggering using the Airflow UI. There's a lot more depth to job scheduling. 

But there you have it! This is a pretty simple pipeline, and shows how powerful Airflow can be in its ability to schedule various jobs using a variety of technologies like python and Spark. This only scratches the surface of what's capable with Airflow. 
