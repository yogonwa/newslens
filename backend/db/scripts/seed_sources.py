import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
MONGO_DB = os.getenv('MONGO_DB')

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
sources_col = db['news_sources']

# Canonical source list
sources = [
    {
        "short_id": "cnn",
        "name": "CNN",
        "color": "#CC0000",
        "logo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/CNN_International_logo.svg/1200px-CNN_International_logo.svg.png",
        "website": "https://cnn.com",
        "region": "US"
    },
    {
        "short_id": "foxnews",
        "name": "Fox News",
        "color": "#003366",
        "logo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/Fox_News_Channel_logo.svg/1200px-Fox_News_Channel_logo.svg.png",
        "website": "https://foxnews.com",
        "region": "US"
    },
    {
        "short_id": "nytimes",
        "name": "New York Times",
        "color": "#000000",
        "logo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/NewYorkTimes.svg/1200px-NewYorkTimes.svg.png",
        "website": "https://nytimes.com",
        "region": "US"
    },
    {
        "short_id": "usatoday",
        "name": "USA Today",
        "color": "#00529B",
        "logo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/USA_Today_Logo.svg/1200px-USA_Today_Logo.svg.png",
        "website": "https://usatoday.com",
        "region": "US"
    },
    {
        "short_id": "washingtonpost",
        "name": "Washington Post",
        "color": "#231F20",
        "logo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Washington_Post_logo_2015.svg/1200px-Washington_Post_logo_2015.svg.png",
        "website": "https://washingtonpost.com",
        "region": "US"
    }
]

for src in sources:
    result = sources_col.replace_one({"short_id": src["short_id"]}, src, upsert=True)
    print(f"Upserted {src['name']} (short_id={src['short_id']})")

print("Seeding complete.") 