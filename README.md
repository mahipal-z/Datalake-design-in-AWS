# Data lake Implementation with AWS
Implementation of data lake design using CloudFormation and Analytics for a farming company.

![](/images/lake.PNG)

## Summary
This project has three major deliverables.
1. CloudFormation stack with given AWS resources that works as an ETL pipeline.
2. Analysis of farm yield dataset with 1000 records to find useful insights.
3. Development of ML Application that can predict farm-yield based on the user input and explains model interpretation.

## Part-I CloudFormation
Using the CloudFormation template I developed, one can create a stack to build an ETL pipeline that works as following:
* Upon pipeline activation, a Lambda function will copy the files in the source as is and upload them to the Raw bucket of the Storage Layer.
* Upon upload completion, a python shell Glue job will automatically start. This job will combine both files and upload the combined file to the Processed S3 bucket.
* Upon upload completion, an Apache spark Glue job will be automatically kicked off. This job will create a new column, namely yield_per_hectare. This column is the result of dividing the yield column by the area. This job will also convert the file to parquet format and store the resulting file in the Transformed S3 bucket.

### Prerequisites
A. An S3 bucket that acts as a source, where CSV files are uploaded. Following three files must be stored in the bucket's root directory.
> 1. 'run_configurations.config', 2. 'combine_csv.py', 3. 'csvtoparquet.py'

B. All the CSV files must have the same schema.  

### Setup instructions
1. Create a CloudFormation stack using the 'cf_template.yml'. Input source bucket name. 
2. Create S3 event notification in the source bucket 'Properties' with following configurations:
> Event Name,
> Suffix: run-configuration.config
> Event types: Object creation: Put, Post, Copy
> Destination: Lambda Function: Specify Lambda function: Enter Lambda function ARN (copy arn from lambda created by stack)
> Save Changes
3. Upload CSV files to be merged in the desired folder in the source bucket.
4. To activate the pipeline, upload the 'run_configurations.config' in the same folder where CSV files are located.

## Part-II Analytics
Using Sagemaker notebook instance, analysis is performed in jupyter notebook to visualize insights to help make better decisions for future farming practices for given geographicsl regions.

### Instructions
1. Once, pipeline has ran succesfully, go to 'combined_file.csv' generated in the Processed S3 Bucket and copy S3 URI. 
2. Update S3 URI in the 'notebook_configuration.config' file.
3. Start 'farm-yield-analytics' notebook instance in the Sagemaker console.
4. Once, instance is in service, run the 'farm_yield.ipynb' notebook to generate analysis.
5. Stop notebook instance, once done, to avoid additional costs.

## Part-III Yield-Prediction Application
Using the streamlit.py script, the ML Application can be launched using local host. This application allows user to select parameters based on farming technique and generates predicted yield per unit hectare. The GUI will also provide explaination on which attributes contributed the most in final predictions.

### Instructions
1. Save the model artifacts generated by jupyter notebook.
2. Update the script with the location for model artifacts.
3. run the application using local machine using 'streamlit run <script directory>'
4. Have fun with the user interface!



