# Supabase Database Writer

A Python script that sends continuous WRITE requests to a Supabase database endpoint with anti-blocking measures.

## Features

**Rate Limiting**: Randomized delays between requests (2-5 seconds by default)

**Batch Pauses**: Long pauses after every N requests to avoid rate limiting

**Random Data Generation**: Creates varied test data to appear more natural

**Statistics Tracking**: Monitors success/failure rates

**Error Handling**: Gracefully handles network issues and API errors

**Configurable**: Easy to adjust timing and behavior

## Anti-Blocking Measures

1. **Random Delays**: Each request waits 2-5 seconds (configurable) with random variation
2. **Periodic Long Pauses**: Takes 15-second breaks after every 50 requests
3. **Varied Data**: Generates different names, emails, and messages
4. **Proper Headers**: Uses standard Supabase authentication headers
5. **Timeout Handling**: 10-second timeout prevents hanging connections

## Installation

```bash
# Install required package
pip install requests
```

## Usage

### Basic Usage
```bash
python supabase_writer.py
```

### Configuration

Edit the settings in the `main()` function:

```python
# Timing Configuration
MIN_DELAY = 2.0              # Minimum seconds between requests
MAX_DELAY = 5.0              # Maximum seconds between requests
BATCH_SIZE = 10              # Show stats every N requests
LONG_PAUSE_AFTER = 50        # Take break after N requests
LONG_PAUSE_DURATION = 15.0   # Break duration in seconds

# Supabase Configuration
SUPABASE_URL = "https://your-project.supabase.co/rest/v1/your-table"
API_KEY = "your-anon-key-here"
```

## Adjusting Rate Limits

### More Aggressive (Higher Rate)
```python
MIN_DELAY = 0.5
MAX_DELAY = 1.5
LONG_PAUSE_AFTER = 100
LONG_PAUSE_DURATION = 5.0
```

### More Conservative (Lower Rate)
```python
MIN_DELAY = 5.0
MAX_DELAY = 10.0
LONG_PAUSE_AFTER = 20
LONG_PAUSE_DURATION = 30.0
```

## Output Example

```
Starting Supabase Writer...
Target URL: https://wmjwbmvkofitcgglalun.supabase.co/rest/v1/submissions
Delay range: 2.0s - 5.0s
Long pause every 50 requests (15.0s)

Press Ctrl+C to stop

✓ Request #1 - SUCCESS
  Inserted: Alice (alice123@gmail.com)
✓ Request #2 - SUCCESS
  Inserted: Bob (bob456@yahoo.com)

============================================================
Statistics at 2026-01-29 14:30:15
Total Requests: 10
Successful: 10
Failed: 0
Success Rate: 100.00%
============================================================
```

## Stopping the Script

Press `Ctrl+C` to stop. The script will display final statistics before exiting.

## Data Structure

The script inserts records with these fields:
- **name**: Random name from a predefined list
- **email**: Generated email address
- **message**: Random message from a predefined list

The `id` and `created_at` fields are handled by Supabase automatically.

## Troubleshooting

### 429 Too Many Requests
- Increase `MIN_DELAY` and `MAX_DELAY`
- Increase `LONG_PAUSE_DURATION`
- Decrease `LONG_PAUSE_AFTER` (pause more frequently)

### Connection Timeouts
- Check your internet connection
- Verify the Supabase URL is correct
- Ensure the API key is valid

### 401 Unauthorized
- Verify your API key is correct
- Check Row Level Security (RLS) policies on your table
- Ensure the anon role has INSERT permissions

## Security Note

⚠️ The API key in this script is visible in the code. For production use:
- Store API keys in environment variables
- Use a `.env` file with python-dotenv
- Never commit API keys to version control

## Example: Using Environment Variables

```python
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
API_KEY = os.getenv('SUPABASE_API_KEY')
```

## License

Free to use and modify as needed.
