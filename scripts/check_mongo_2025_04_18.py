import os
from datetime import datetime, timedelta
from backend.db.operations import db_ops
from backend.services.s3_service import S3Service
from pprint import pprint
from collections import Counter, defaultdict

def main():
    # Define the date range for 2025-04-18
    start = datetime(2025, 4, 18, 0, 0, 0)
    end = datetime(2025, 4, 18, 23, 59, 59)
    print(f"Querying headlines for display_timestamp between {start} and {end}")
    results = db_ops.get_headlines_by_time(start, end)
    print(f"Found {len(results)} documents.")
    if not results:
        return

    # Build source_id to name mapping
    source_id_to_name = {}
    for src in db_ops.sources.find({}):
        source_id_to_name[str(src['_id'])] = src.get('name', str(src['_id']))

    # Collect 06:00 docs by source
    six_am_docs = defaultdict(list)
    for doc in results:
        dt = doc.get('display_timestamp')
        if dt and dt.strftime('%H:%M') == '06:00':
            source_id = str(doc.get('source_id', 'unknown'))
            source_name = source_id_to_name.get(source_id, source_id)
            six_am_docs[source_name].append(doc)

    # Only use main sources (not outlier IDs)
    main_sources = ["CNN", "Fox News", "The New York Times", "The Washington Post", "USA Today"]
    s3 = S3Service()
    print("\n06:00 S3 presigned URLs by source:")
    for source in main_sources:
        docs = six_am_docs.get(source, [])
        for doc in docs:
            s3_key = doc.get('screenshot', {}).get('url', None)
            if s3_key:
                try:
                    url = s3.s3_client.generate_presigned_url(
                        'get_object',
                        Params={'Bucket': s3.bucket_name, 'Key': s3_key},
                        ExpiresIn=3600
                    )
                    print(f"  {source}: {url}")
                except Exception as e:
                    print(f"  {source}: ERROR generating presigned URL for {s3_key}: {e}")
    if not any(six_am_docs[source] for source in main_sources):
        print("No 06:00 documents found for main sources.")

if __name__ == "__main__":
    main() 