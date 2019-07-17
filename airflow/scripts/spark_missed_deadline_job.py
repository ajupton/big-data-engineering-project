# First, unzip the file with the Olist ecommerce data
from zipfile import ZipFile

# Create a ZipFile Object and load brazilian-ecommerce.zip in it
with ZipFile('/path/to/Brazilian-ecommerce.zip', #<<<<<<<< edit path location where you saved the file!!!
             'r') as zipObj:
    # Extract all the contents of zip file in current directory
    zipObj.extractall()

# Setting up spark
import findspark
findspark.init()
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql import *
from pyspark.sql.functions import *
conf = SparkConf().setMaster("local").setAppName("Missed_Deadlines")
spark = SparkSession.builder.getOrCreate()
print(spark)

# Set sqlContext from the Spark context
from pyspark.sql import SQLContext
sqlContext = SQLContext(spark)

# Edit Spark SQL context for ease of use with Pandas
spark.conf.set("spark.sql.execution.arrow.enabled", "true")

# Build a spark session
spark = SparkSession.builder.getOrCreate()

# Load in csv files into spark dataframes
df_items = spark.read.format("csv") \
            .option("header", "true") \
            .option("inferSchema", "true") \
            .load("olist_order_items_dataset.csv")

df_orders = spark.read.format("csv") \
             .option("header", "true") \
             .option("inferSchema", "true") \
             .load("olist_orders_dataset.csv")

df_products = spark.read.format("csv") \
                .option("header", "true") \
                .option("inferSchema", "true") \
                .load("olist_products_dataset.csv")

# Create SQL Table Views from dfs for SQL querying
df_items.createOrReplaceTempView('items')
df_orders.createOrReplaceTempView('orders')
df_products.createOrReplaceTempView('products')

# SQL Query to pull order/seller/product info for orders where the
# seller missed the deadline to deliver the shipment to the carrier
late_carrier_deliveries = spark.sql("""
SELECT i.order_id, i.seller_id, i.shipping_limit_date, i.price, i.freight_value,
       p.product_id, p.product_category_name,
       o.customer_id, o.order_status, o.order_purchase_timestamp, o.order_delivered_carrier_date,
       o.order_delivered_customer_date, o.order_estimated_delivery_date
FROM items AS i
JOIN orders AS o
ON i.order_id = o.order_id
JOIN products AS p
ON i.product_id = p.product_id
WHERE i.shipping_limit_date < o.order_delivered_carrier_date
""")

# Write the results to a single csv file
# coalesce(1) requires that the file is small enough to fit
# in the heap memory of the master Spark node and is therefore
# only recommended for very small datasets
# Alternatives are converting the Spark df to a Pandas df before
# writing to disk.
# Otherwise, it's best practice to maintain the partitions to
# take advantage of HDFS
late_carrier_deliveries.coalesce(1) \
                       .write \
                       .option("header", "true") \
                       .csv("/path/where/you/want/missed_shipping_limit_orders.csv") # <<<<<<< edit path
