import boto3
import json
import time
from sqlmodel import create_engine, Session
from app.infrastructure.scripts.rocket_loader import fetch_and_load_rockets, fetch_and_load_launches, fetch_and_load_starlinks
from dotenv import load_dotenv
import os

load_dotenv()

REGION = os.getenv("REGION")
QUEUE_URL = os.getenv("QUEUE_URL")
DATABASE_URL = os.getenv("DATABASE_URL")

# Create SQS client
sqs = boto3.client("sqs", region_name=REGION)
engine = create_engine(DATABASE_URL, echo=True)

def process_message(message_body):
    """Process the message body and call the appropriate loader function."""
    data = json.loads(message_body)
    with Session(engine) as session:
        if "rocket" in data[0]:
            fetch_and_load_rockets(session, data)
        elif "launch" in data[0]:
            fetch_and_load_launches(session, data)
        elif "starlink" in data[0]:
            fetch_and_load_starlinks(session, data)
        else:
            print("Unknown message type")

def receive_messages():
    """Continuously listens for messages in the SQS queue."""
    print("Listening for messages from SQS queue...\n")
    while True:
        try:
            response = sqs.receive_message(
                QueueUrl=QUEUE_URL,
                MaxNumberOfMessages=5,
                WaitTimeSeconds=10, 
                MessageAttributeNames=["All"]
            )
            messages = response.get("Messages", [])
            if messages:
                for message in messages:
                    print("\n📩 New Message Received:")
                    print(f"MessageId: {message['MessageId']}")
                    print(f"Body: {message['Body']}")
                    
                    # Process the message
                    process_message(message['Body'])

                    sqs.delete_message(QueueUrl=QUEUE_URL, ReceiptHandle=message["ReceiptHandle"])
                    print("✅ Message deleted from queue.")
            else:
                print("⏳ No new messages. Waiting...")
        except Exception as e:
            print("❌ Error receiving messages:", str(e))
        
        # Avoid excessive API requests
        time.sleep(1)

if __name__ == "__main__":
    receive_messages()