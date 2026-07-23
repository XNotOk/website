# Fare-Cab

London black cab fare lookup site — know your Heathrow fare before you ride.

## Quick start

```bash
python3 seed.py   # populate fares database
python3 build.py  # generate index.html
```

Open `index.html` in a browser, or serve with any static file server.

## How it works

Enter a London postcode area (e.g. SW1, N1, TW6) and the page instantly returns the fixed fare to Heathrow Airport. All fare data is embedded client-side — no server required.
