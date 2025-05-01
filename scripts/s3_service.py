import boto3
from botocore.exceptions import ClientError
from io import BytesIO
import logging
from typing import Optional, Dict

class S3Service:
    """Handles S3 operations for storing screenshots"""
    
    def __init__(self, bucket_name: str):
        self.s3 = boto3.client('s3')
        self.bucket = bucket_name

    async def upload_buffer(
        self,
        image_buffer: BytesIO,
        key: str,
        metadata: Optional[Dict] = None
    ) -> str:
        """
        Upload an image from BytesIO buffer to S3
        Returns the S3 URL of the uploaded file
        """
        try:
            # Ensure buffer is at start
            image_buffer.seek(0)
            
            # Upload to S3
            self.s3.upload_fileobj(
                image_buffer,
                self.bucket,
                key,
                ExtraArgs={
                    'ContentType': 'image/png',
                    'Metadata': metadata or {}
                }
            )
            
            # Generate URL
            url = f"https://{self.bucket}.s3.amazonaws.com/{key}"
            return url
            
        except ClientError as e:
            logging.error(f"S3 upload failed: {e}")
            raise
        finally:
            image_buffer.close()

    async def check_exists(self, s3_key: str) -> bool:
        """Check if object exists in S3"""
        try:
            self.s3.head_object(Bucket=self.bucket, Key=s3_key)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            raise 