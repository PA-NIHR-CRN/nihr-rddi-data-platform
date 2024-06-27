import boto3
import json
import os
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import logging

def lambda_handler(event, context):
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    try:
        targetBucket = ""
        if "TARGET_BUCKET" in os.environ:
            targetBucket = os.environ.get("TARGET_BUCKET")
        else:
            log.error("[ERROR] Target Bucket not set")

        s3 = boto3.client('s3')
        bucketName = event["detail"]["bucket"]["name"]
        keyName = event["detail"]["object"]["key"]

        source_data = download(s3,bucket_name=bucketName,object_key=keyName)
        jsonData = json.loads(source_data)
        path, filename = split_path(keyName)
        parquetFileName = replace_ext(filename,"parquet")
        if path is None or path == "":
            outputPath = parquetFileName
        else:
            outputPath = f"{path}/{parquetFileName}"
        
        localPath = convert_parquet(jsonData)
        
        upload_file(s3,localPath,targetBucket,outputPath)
    except Exception as e:
        return {
            'statusCode':500,
            'body': json.dumps(e)
        }
    
    return {
        'statusCode': 200,
        'body': json.dumps('OK')
    }


def download(client,bucket_name,object_key):
    response = client.get_object(Bucket=bucket_name,Key=object_key)
    contents = response['Body'].read().decode('utf-8')
    return contents

def upload_file(client,localPath,bucket,key):
    client.upload_file(localPath,bucket,key)

def split_path(key_path):
    last_slash_index = key_path.rfind('/')
    if last_slash_index == -1:
        path = ''
        filename = key_path
    else:
        path = key_path[:last_slash_index]
        filename = key_path[last_slash_index + 1:]

    return path, filename

def replace_ext(filename,ext):
    if not ext.startswith('.'):
        ext = '.' + ext
    
    base_name = os.path.splitext(filename)[0]

    return base_name + ext

def convert_parquet(json_data):
    localPath = f"/tmp/file.parquet"
    json_data = [json_data]
    df = pd.DataFrame(json_data)
    table = pa.Table.from_pandas(df)
    pq.write_table(table,localPath)

    return localPath