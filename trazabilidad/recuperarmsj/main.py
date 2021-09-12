import boto3
import logger
import os
import time

try:
    sqs_client = boto3.client(
            'sqs',
            region_name=os.environ['AWS_REGION'],
            endpoint_url=os.environ['SQS_ENDPOINT'],
            use_ssl=os.environ['USE_SSL'] == '1',
            verify=False,
            aws_access_key_id=os.environ['ACCESS_KEY'],
            aws_secret_access_key=os.environ['SECRET_KEY'])
except Exception as e:
    logger.logger.error(e)

queue_url = sqs_client.get_queue_url(QueueName=os.environ['SQS_QUEUE_NAME'])['QueueUrl']
#logger.logger.info(queue_url)
while True:
    logger.logger.info('******Incia ciclo')
    try:
        # Receive message from SQS queue
        response = sqs_client.receive_message(
            QueueUrl=queue_url,
            AttributeNames=[
                'SentTimestamp'
            ],
            MaxNumberOfMessages=1,
            MessageAttributeNames=[
                'All'
            ],
            VisibilityTimeout=20,
            WaitTimeSeconds=2
        )

        message = response['Messages'][0]
        receipt_handle = message['ReceiptHandle']

        logger.logger.info('Received message: %s' % message)

        # Delete received message from queue
        sqs_client.delete_message(
              QueueUrl=queue_url,
              ReceiptHandle=receipt_handle
            )

        logger.logger.info('Delete')

    except Exception as e:
        logger.logger.error(e)
    time.sleep(5)