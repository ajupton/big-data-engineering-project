from datetime import datetime
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

dag = DAG('late_shipments_to_carrier',
          description='Returns list of orders where the seller missed the carrier delivery deadline',
          schedule_interval='0 5 * * *',
          start_date=datetime(2019, 7, 10), catchup=False)

# Download the data from S3
s3_download_operator = BashOperator(task_id='s3_download',
                                    bash_command='python /path/to/airflow/scripts/s3_download.py', ##<<<< edit path!!
                                    dag=dag)

# Run Spark job to return order information where the seller
# missed the deadline to deliver the shipment to the carrier
spark_missed_deadline_operator = BashOperator(task_id='spark_missed_deadline_job',
                                              bash_command='python /path/to/airflow/scripts/spark_missed_deadline_job.py', ##<<<< edit path!!
                                              dag=dag)

# Specify that the Spark task above depends on the dataset downloading properly
spark_missed_deadline_operator.set_upstream(s3_download_operator)

# Upload cleaned dataset to S3
s3_upload_operator = BashOperator(task_id='s3_upload',
                                  bash_command='python /path/to/airflow/scripts/s3_upload.py', ##<<<< edit path!!
                                  dag=dag)

# Specify that the S3 upload task depends on the Spark job running successfully
s3_upload_operator.set_upstream(spark_missed_deadline_operator)

s3_download_operator >> spark_missed_deadline_operator >> s3_upload_operator
