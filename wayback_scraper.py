import requests
from datetime import datetime, timedelta
import json
import time
from typing import List, Dict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# News sites to scrape
NEWS_SITES = [
    "cnn.com",
    "foxnews.com",
    "nytimes.com",
    "washingtonpost.com",
    "usatoday.com"
]

def get_timestamps() -> List[str]:
    """Generate timestamps for the last day at 3-hour intervals from 6 AM to 9 PM."""
    now = datetime.now()
    start_time = now.replace(hour=6, minute=0, second=0, microsecond=0)
    if now.hour < 6:
        start_time -= timedelta(days=1)
    
    timestamps = []
    for i in range(6):  # 6 snapshots
        timestamp = start_time + timedelta(hours=i*3)
        if timestamp > now:
            break
        timestamps.append(timestamp.strftime("%Y%m%d%H%M%S"))
    
    return timestamps

def query_wayback_cdx(site: str, timestamp: str) -> List[Dict]:
    """Query the Wayback Machine CDX API for a specific site and timestamp."""
    url = f"https://web.archive.org/cdx/search/cdx"
    params = {
        "url": site,
        "from": timestamp[:8],  # YYYYMMDD
        "to": timestamp[:8],
        "output": "json",
        "filter": "statuscode:200",
        "collapse": "digest"
    }
    
    headers = {
        "User-Agent": "NewsLensBot/0.1 (+https://github.com/yourusername/newslens; contact: your@email.com)"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error querying Wayback CDX for {site} at {timestamp}: {e}")
        return []

def process_snapshots():
    """Process snapshots for all news sites at specified timestamps."""
    timestamps = get_timestamps()
    results = {}
    
    for site in NEWS_SITES:
        logging.info(f"Processing snapshots for {site}")
        site_results = {}
        
        for timestamp in timestamps:
            logging.info(f"Querying timestamp {timestamp}")
            snapshots = query_wayback_cdx(site, timestamp)
            
            if snapshots and len(snapshots) > 1:  # First row is headers
                # Find the closest snapshot to our target timestamp
                closest_snapshot = min(snapshots[1:], key=lambda x: abs(int(x[1]) - int(timestamp)))
                site_results[timestamp] = {
                    "url": f"https://web.archive.org/web/{closest_snapshot[1]}/{closest_snapshot[2]}",
                    "timestamp": closest_snapshot[1]
                }
            
            time.sleep(1)  # Be polite to the API
        
        results[site] = site_results
    
    return results

def save_results(results: Dict):
    """Save the results to a JSON file."""
    filename = f"wayback_snapshots_{datetime.now().strftime('%Y%m%d')}.json"
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    logging.info(f"Results saved to {filename}")

def main():
    logging.info("Starting Wayback Machine scraper")
    results = process_snapshots()
    save_results(results)
    logging.info("Scraping complete")

if __name__ == "__main__":
    main() 