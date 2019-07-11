# Big Data Engineering Project
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
* Runs a Spark/Spark SQL job producing a cleaned-up dataset of delivery deadline missing orders
* Upload the cleaned-up dataset back to the same S3 bucket in a folder primed for higher level analytics

I'll provide an overview of each of these steps but assume that the reader is already somewhe familiar with python, SQL, and Spark. 

## Step 1: Setup and populate an AWS S3 Bucket
Setting up an S3 bucket is pretty straightforward, and the current 5 GB free tier limit for 12 months is a great way to get started with AWS S3 without having to break the bank. Simply create an AWS account, click on "Services" in the upper left hand side, navigate to "Storage" and select S3. From there you'll be able to create a new S3 bucket following the prompts and inputing settings based on your unique needs. I largely followed the default options. Once created, simply select the bucket and in the Overview tab, there are options to upload objects/files, create folders, or set permissions. Alternatively, it's possible to install AWS Cli to your machine in order to transfer files at the command line. 

A meaningful data engineering project requires motivation and dedication to see all the way through. Because of this, it's really important to find a dataset or datasets that a truly interesting to the aspiring data engineer. Additionally, a solid data engineering project must lead to the creation of value for an organization. In that regard, the specific technologies are generally of less interest than the problem statement and the outcome. While technologies will change, the underlying data handling methodologies that data engineers use are unlikely to dramatically change in the near term future. 

Sports data, home inventory/sales data, and tweets are examples of data that can lead to strong data engineering projects because they are updated frequently, large in size and scope, require lots of post-processing, and are often topically driven around the interests of aspiring data engineers. 

There are a number of ways to upload data onto S3. One way is to use the GUI tool in the S3 interface. Alternatively, the AWS CLI (command line interface) can be used to interact with S3 through the command line. [You can find out more about installing the AWS CLI here.](https://aws.amazon.com/cli/) In short, you'll need to install the AWS CLI using `pip install awscli --upgrade --user` [and then configure your credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html). [Or see here for a brief overview of transferring files to an S3 bucket using AWS Cli](https://confusedcoders.com/data-engineering/how-to-copy-kaggle-data-to-amazon-s3). 

Once your AWS CLI credentials are input, it's easy to copy (or cp) files onto it from the terminal using the following syntax: `aws s3 cp <local file path> <s3 path>`  e.g. `aws s3 cp ~/file_to_upload.csv s3://s3-bucket-name/folder_path/`

The method for interacting with S3 taken here uses the [python library boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html). boto3 has all sorts of functions for interacting with products across the AWS landscape using python. 

We'll use boto3 as part of python scripts to both download the Brazilian ecommerce data to our S3 bucket as well upload the csv file that results from the Spark job back into the S3 bucket. 

## Step 2: Analyze the tables with an eye toward identifying the delivery performance of Olist orders/sellers 
One of the strongest skillsets needed by a data engineer is communication. That communication needs to be flexed primarily in conversations with stakeholders that manage data sets as well as stakeholders that will consume the data at the end of the ETL and stream pipelines that data engineers construct. Data engineers often need to rely on the domain expertise of analysts, data scientists, program managers, executives, and others in order to understand what specific data features are needed for various analytics applications. That said, data engineers still need to possess strong EDA (exploratory data analysis) chops in order to deliver data sets that meet the needs of various stakeholders. As a result, it's very often worthwhile for data engineers to get down and dirty with the data in the data lake through data visualization, the computing of summary statistics, and other exploratory methods. 

My go-to tool of choice in this regard is a Jupyter notebook using python. A typical workflow involes using SQLAlchemy or the pyspark API to connect to a database and pull data with some pythonic SQL and then use numpy, pandas, altair/seaborn/matplotlib/plotly, and other python packages for visualization, the computing of summary statitistics, maybe running a few statistical models, and other EDA techniques. For data that is truly 'big' and can't fit in memory on a single machine, Spark becomes invaluable. Spark SQL makes pulling and manipulating data a breeze as well for those with SQL chops. Of course, this analytics approach is possible in all sorts of AWS services like Athena and EMR among many others. With massive volumes of data, it can often be worthwhile to take samples of data from the data lake and get some EDA in to get a feel for the tables and schema as well as to understand the quirks of the data. OLTP processes often must follow multiple business rules that make it a major challenge to do things like join disparate datasets, hammer down ground-truth insights, or compare current and historical trends.  

## Step 5: Get hands-on with Airflow 
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
*



## More steps on the way!




Props to the folks over at [ConfusedCoders](https://confusedcoders.com/) for inspiring this project
