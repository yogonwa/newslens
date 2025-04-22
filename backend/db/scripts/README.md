# Database Scripts

This directory contains scripts for managing the MongoDB database.

## Available Scripts

### `seed_data.py`
Populates the database with initial data:
- News sources (CNN, Fox News, NYT, WaPo, USA Today)
- Test headlines for each source
- Test screenshots

To run:
```bash
python -m backend.db.scripts.seed_data
```

## Next Steps

1. **Schema Validation**
   - Add validation for headline metadata
   - Ensure all required fields are present
   - Add data type checking

2. **Test Data Enhancement**
   - Add more realistic test headlines
   - Include actual screenshot URLs
   - Add historical data for time-based testing

3. **Migration Scripts**
   - Create scripts for schema updates
   - Add data migration utilities
   - Implement backup procedures 