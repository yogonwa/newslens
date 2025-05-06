import os
import logging
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from typing import Optional, List

load_dotenv()

"""
s3_service.py

Provides S3Service for uploading, downloading, listing, and deleting files in AWS S3.
Used in the NewsLens pipeline to store and retrieve screenshots and related artifacts.
"""

class S3Service:
    """
    Service for interacting with AWS S3 for file storage, retrieval, and management.
    Handles uploads, downloads, presigned URLs, and batch deletions.
    """
    def __init__(self, bucket_name: Optional[str] = None, region: Optional[str] = None):
        """Initialize S3Service with optional bucket and region (defaults to env vars)."""
        self.bucket_name = bucket_name or os.getenv('S3_BUCKET_NAME')
        self.region = region or os.getenv('AWS_DEFAULT_REGION')
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=self.region
        )
        self.logger = logging.getLogger(__name__)

    def upload_file(self, file_path: str, s3_key: str, content_type: str = 'application/octet-stream') -> str:
        """Upload a file from disk to S3 under the given key."""
        try:
            self.s3_client.upload_file(
                Filename=file_path,
                Bucket=self.bucket_name,
                Key=s3_key,
                ExtraArgs={'ContentType': content_type}
            )
            return s3_key
        except ClientError as e:
            self.logger.error(f"Failed to upload {file_path} to S3: {e}")
            raise

    def upload_bytes(self, file_bytes: bytes, s3_key: str, content_type: str = 'application/octet-stream', metadata: dict = None) -> str:
        """Upload bytes directly to S3 under the given key, with optional metadata."""
        try:
            extra_args = {'ContentType': content_type}
            if metadata:
                extra_args['Metadata'] = {k: str(v) for k, v in metadata.items()}
                
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=file_bytes,
                **extra_args
            )
            return s3_key
        except ClientError as e:
            self.logger.error(f"Failed to upload bytes to S3 key {s3_key}: {e}")
            raise

    def generate_presigned_url(self, s3_key: str, expires_in: int = 3600) -> str:
        """Generate a presigned URL for accessing a file in S3."""
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': s3_key},
                ExpiresIn=expires_in
            )
            return url
        except ClientError as e:
            self.logger.error(f"Failed to generate presigned URL for {s3_key}: {e}")
            raise

    def delete_file(self, s3_key: str) -> None:
        """Delete a file from S3 by key."""
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=s3_key)
        except ClientError as e:
            self.logger.error(f"Failed to delete S3 key {s3_key}: {e}")
            raise

    def list_files(self, prefix: str = "") -> List[str]:
        """List all files in S3 under a given prefix."""
        try:
            paginator = self.s3_client.get_paginator('list_objects_v2')
            page_iterator = paginator.paginate(Bucket=self.bucket_name, Prefix=prefix)
            files = []
            for page in page_iterator:
                for obj in page.get('Contents', []):
                    files.append(obj['Key'])
            return files
        except ClientError as e:
            self.logger.error(f"Failed to list files with prefix '{prefix}': {e}")
            raise

    def delete_prefix(self, prefix: str) -> int:
        """Delete all objects under a given prefix. Returns number of deleted objects."""
        try:
            files = self.list_files(prefix)
            deleted = 0
            for key in files:
                self.delete_file(key)
                deleted += 1
            return deleted
        except ClientError as e:
            self.logger.error(f"Failed to delete files with prefix '{prefix}': {e}")
            raise 