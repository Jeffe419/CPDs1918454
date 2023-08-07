import boto3
import json

dynamodb = boto3.resource('dynamodb')
rekognition = boto3.client('rekognition')

TABLE_NAME = 'Celebrities-s1918454'

def lambda_handler(event, context):
    print(f"Received event: {json.dumps(event)}")  # Log the entire event

    try:
        if 'Records' in event:
            # Check if it's an S3 event
            if event['Records'][0]['eventSource'] == 'aws:s3':
                # Handle S3 event
                bucket = event['Records'][0]['s3']['bucket']['name']
                key = event['Records'][0]['s3']['object']['key']

                response = rekognition.recognize_celebrities(
                    Image={
                        'S3Object': {
                            'Bucket': bucket,
                            'Name': key
                        }
                    }
                )

                celebrities = response.get('CelebrityFaces', [])

                # Store recognized celebrities in DynamoDB
                if celebrities:
                    table = dynamodb.Table(TABLE_NAME)

                    for celebrity in celebrities:
                        item = {
                            'celebrity_image_file_name': key,
                            'CelebrityName': celebrity['Name'],
                            'Confidence': str(celebrity['Face']['Confidence'])
                        }
                        try:
                            table.put_item(Item=item)
                        except Exception as e:
                            # Handle any DynamoDB put_item errors
                            return {
                                'statusCode': 500,
                                'body': json.dumps({
                                    'error': f'Error writing data to DynamoDB: {e}'
                                })
                            }

                    return {
                        'statusCode': 200,
                        'body': json.dumps({
                            'message': 'Processing complete',
                            'recognizedCelebrities': [c['Name'] for c in celebrities]
                        })
                    }
                else:
                    return {
                        'statusCode': 200,
                        'body': json.dumps({
                            'message': 'No celebrities recognized'
                        })
                    }

            # Check if it's an SNS event
            elif event['Records'][0]['EventSource'] == 'aws:sns':
                sns_message = event['Records'][0]['Sns']['Message']
                print(f"Received SNS message: {sns_message}")

                return {
                    'statusCode': 200,
                    'body': json.dumps({
                        'message': 'SNS notification received',
                        'snsMessage': sns_message
                    })
                }

    except KeyError:
        print(f"KeyError: Unexpected event structure: {event}")
    except Exception as e:
        print(f"Error processing event: {e}")

    return {
        'statusCode': 400,
        'body': json.dumps({
            'error': 'Unexpected event structure or error processing event'
        })
   }
