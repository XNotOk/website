# Fare-Cab

London black cab fare lookup site for fare-cab.co.uk.

## Quick start

```bash
# Seed the fares database
python3 seed.py

# Build the frontend HTML
python3 build.py

# Start the server
python3 server.py
```

Open http://localhost:8080 and enter a London postcode area (e.g. SW1, N1, TW6) to see the Heathrow fare.

## Stack

- **Frontend**: pyfront — generates static HTML with scoped CSS
- **Backend**: pyback — HTTP server with RPC bridge
- **Database**: SQLite with postcode prefix -> Heathrow fare mappings
