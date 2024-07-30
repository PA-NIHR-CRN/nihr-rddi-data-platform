import boto3
import os
import logging
import datetime


def lambda_handler(event,ctx):
    glue = boto3.client('glue')
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    # TODO implement
    try:
        bucketName = event["detail"]["bucket"]["name"]
        keyName = event["detail"]["object"]["key"]
        inputPath = f"s3://{bucketName}/{keyName}"
        if os.environ.get('TARGET_BUCKET') is not None:
            currentTime = datetime.datetime.now()
            outputPath = f"s3://{os.environ.get('TARGET_BUCKET')}/{currentTime.year}/{currentTime.month}/{currentTime.day}/{currentTime.hour}/"
        else:
            raise Exception("Target bucket not set")
        
        if os.environ.get("JOB_NAME") is not None:
            jobName = os.environ.get("JOB_NAME")
        else:
            raise Exception("Job name is not set correctly")
        

        job_parameters = {
            '--input_path': inputPath,
            '--output_path': outputPath,
            '--table_name': normalize_table_name(keyName)
        }
        
        response = glue.start_job_run(JobName=jobName,Arguments=job_parameters)
        return {
            'statusCode': 200,
            'body': "OK"
        }
    except Exception as e:
        print(e + "\n")
        return {
            'statusCode':500,
            'body': e
        }

def normalize_table_name(path: str) -> str:
    base_name = os.path.basename(path)
    name_without_extension = os.path.splitext(base_name)[0]

    dir_names = []
    current_path = os.path.dirname(path)
    while current_path != '/':
        dir_names.append(os.path.basename(current_path))
        current_path = os.path.dirname(current_path)

    dir_names.reverse()
    normalized_table_name = "_".join(dir_names + [name_without_extension])
    return normalized_table_name