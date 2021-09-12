import boto3
import os
import time
import logging

try:
    logging.basicConfig(filename='trazabilidad.log', level=logging.INFO, format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', encoding="UTF-8")
    sqs_client = boto3.client(
            'sqs',
            region_name=os.environ['AWS_REGION'],
            endpoint_url=os.environ['SQS_ENDPOINT'],
            use_ssl=os.environ['USE_SSL'] == '1',
            verify=False,
            aws_access_key_id=os.environ['ACCESS_KEY'],
            aws_secret_access_key=os.environ['SECRET_KEY'])
except Exception as e:
    logging.error(e)

queue_url = sqs_client.get_queue_url(QueueName=os.environ['SQS_QUEUE_NAME'])['QueueUrl']
#logger.logger.info(queue_url)
while True:
    #logging.info('******Incia ciclo')
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

        logging.info('Received message: %s' % message)
        logging.info(message['Body'])

        # Delete received message from queue
        sqs_client.delete_message(
              QueueUrl=queue_url,
              ReceiptHandle=receipt_handle
            )

        #logging.info('Delete')

    except Exception as e:
        logging.error(e)
    time.sleep(1)