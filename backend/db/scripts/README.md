# Database Scripts

This directory contains scripts for managing the MongoDB database.

## Available Scripts

### `migrate_apr18_6am.py`
Seeds the MVP database with real data for 5 major news sources at the 6am slot, including headlines and S3 screenshot keys. This script aligns with the current frontend and backend data requirements.

To run:
```bash
python -m backend.db.scripts.migrate_apr18_6am
```

## Next Steps

1. **Schema Validation**
   - Add validation for headline metadata
   - Ensure all required fields are present
   - Add data type checking

2. **Data Enhancement**
   - Add more realistic headlines and editorial tags
   - Include actual screenshot URLs for additional time slots
   - Add historical data for time-based testing

3. **Migration Scripts**
   - Add scripts for future schema updates
   - Implement backup procedures 