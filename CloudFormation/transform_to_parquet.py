import boto3
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# Define the S3 bucket names and file paths
src_bucket = 'datalake-processed-s3-mz'
dest_bucket = 'datalake-transformed-s3-mz'
src_file = 'combined_file.csv'
dest_file = 'transformed_file.parquet'

# Initialize the S3 client
s3 = boto3.client('s3')

# Read the CSV files from S3 into pandas dataframes
df = pd.read_csv(f's3://{src_bucket}/{src_file}')

# Adding a new column
df['yield_per_hectare'] = df['yield'] / df['area']

# Writing the transformed dataframe to a Parquet file in a destination S3 bucket
table = pa.Table.from_pandas(df)
pq.write_table(table, f"s3://{dest_bucket}/{dest_file}")

