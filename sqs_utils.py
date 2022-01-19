import json
import boto3


def send_message(message):
    sqs_client = boto3.client("sqs", region_name="us-east-1")

    # message = {"key": "value"}
    response = sqs_client.send_message(
        QueueUrl="https://sqs.us-east-1.amazonaws.com/657320242713/OrderQueue",
        MessageBody=json.dumps(message)
    )
    print(response)

    return response


def receive_message():
    sqs_client = boto3.client("sqs", region_name="us-east-1")
    response = sqs_client.receive_message(
        QueueUrl="https://sqs.us-east-1.amazonaws.com/657320242713/OrderQueue",
        MaxNumberOfMessages=1,
        WaitTimeSeconds=20,
    )

    print(f"Number of messages received: {len(response.get('Messages', []))}")

    return_message = ''
    receipt_handle = ''

    for message in response.get("Messages", []):
        message_body = message["Body"]
        print(f"Message body: {json.loads(message_body)}")
        print(f"Receipt Handle: {message['ReceiptHandle']}")

        return_message = json.loads(message_body)
        receipt_handle = message['ReceiptHandle']

        break

    if receipt_handle == '' and return_message == '':
        return None

    delete_message(receipt_handle)

    return return_message


def delete_message(receipt_handle):
    sqs_client = boto3.client("sqs", region_name="us-east-1")
    response = sqs_client.delete_message(
        QueueUrl="https://sqs.us-east-1.amazonaws.com/657320242713/OrderQueue",
        ReceiptHandle=receipt_handle,
    )
    print(response)
