from boto3.s3.transfer import S3Transfer
import boto3

########################################
## Edit the keys/paths for your setup ##
########################################
access_key = 'your_access_key_here'
secret_key = 'your_secret_key_here'
s3_bucket_name = 'your_s3_bucket_name'
s3_filename = 'brazilian-ecommerce.zip'
download_path = '/path/to/brazilian-ecommerce.zip'

client = boto3.client('s3',
                      aws_access_key_id = access_key,
                      aws_secret_access_key = secret_key)

print('client')

client.download_file(s3_bucket_name, s3_filename, download_path)
