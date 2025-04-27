import os
from dotenv import load_dotenv
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

# Load environment variables from .env
load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

def main():
    print(f"Testing S3 access for bucket: {S3_BUCKET_NAME}")
    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_DEFAULT_REGION
        )
        response = s3.list_objects_v2(Bucket=S3_BUCKET_NAME)
        contents = response.get('Contents', [])
        if not contents:
            print("Bucket is empty or no objects found.")
        else:
            print("Objects in bucket:")
            for obj in contents:
                print(f"- {obj['Key']}")
    except NoCredentialsError:
        print("AWS credentials not found. Check your .env file.")
    except ClientError as e:
        print(f"AWS ClientError: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main() 