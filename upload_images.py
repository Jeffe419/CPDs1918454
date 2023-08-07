# -*- coding: utf-8 -*-
import boto3
import os
import time
import json

s3 = boto3.resource('s3')
sns = boto3.client('sns')
bucket_name = 'images-s1918454'
topic_arn = 'arn:aws:sns:us-east-1:940428369783:celebrity-recognizer-s1918454'

def upload_files(path):
    if not os.path.exists(path):
        print(f"Error: The path '{path}' does not exist.")
        return
    
    for file in os.listdir(path):
        filename = os.path.join(path, file)
        
        # Check if the file is an image
        if filename.lower().endswith(('.jpg', '.png')):
            print(f'Uploading: {file}')
            
            # Upload to S3
            try:
                s3.meta.client.upload_file(Filename=filename, Bucket=bucket_name, Key=file)
                print('Upload completed')
            except Exception as e:
                print(f"Error uploading {file} to S3: {e}")
                continue
            
            # Publish to SNS
            try:
                message = {
                    'default': f'New image file uploaded: {file}'
                }
                sns.publish(
                    TopicArn=topic_arn,
                    Message=json.dumps(message),
                    MessageStructure='json'
                )
                print('Message published to SNS')
            except Exception as e:
                print(f"Error publishing message to SNS for {file}: {e}")
            
            time.sleep(10)  # Pause for 30 seconds

if __name__ == "__main__":
    upload_files(r"C:\Users\jeffe\OneDrive\Desktop\4th Year\CLD PLATFORM\Images\Images")
