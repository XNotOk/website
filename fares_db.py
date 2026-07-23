import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "fares.db")

SCHEMA = {
    "postcode_prefix": "TEXT PRIMARY KEY",
    "cost": "REAL NOT NULL",
    "zone": "TEXT",
}

SEED_DATA = [
    ("SW1", 45.00, "Westminster"),
    ("SW3", 48.00, "Knightsbridge"),
    ("SW5", 42.00, "Earl's Court"),
    ("SW7", 44.00, "South Kensington"),
    ("SW11", 55.00, "Battersea"),
    ("SW15", 58.00, "Putney"),
    ("SW19", 52.00, "Wimbledon"),
    ("W1", 38.00, "West End"),
    ("W2", 36.00, "Paddington"),
    ("W8", 40.00, "Kensington"),
    ("W11", 42.00, "Notting Hill"),
    ("W14", 44.00, "West Kensington"),
    ("NW1", 50.00, "Camden"),
    ("NW3", 52.00, "Hampstead"),
    ("NW5", 55.00, "Kentish Town"),
    ("NW8", 48.00, "St John's Wood"),
    ("N1", 58.00, "Islington"),
    ("N5", 60.00, "Highbury"),
    ("N7", 62.00, "Holloway"),
    ("N19", 65.00, "Archway"),
    ("SE1", 48.00, "South Bank"),
    ("SE5", 52.00, "Camberwell"),
    ("SE11", 50.00, "Lambeth"),
    ("SE15", 55.00, "Peckham"),
    ("EC1", 42.00, "Clerkenwell"),
    ("EC2", 40.00, "City of London"),
    ("EC4", 44.00, "Fleet Street"),
    ("WC1", 40.00, "Bloomsbury"),
    ("WC2", 38.00, "Covent Garden"),
    ("E1", 52.00, "Whitechapel"),
    ("E2", 55.00, "Bethnal Green"),
    ("E14", 48.00, "Canary Wharf"),
    ("E15", 50.00, "Stratford"),
    ("TW1", 25.00, "Twickenham"),
    ("TW3", 22.00, "Hounslow"),
    ("TW6", 12.00, "Heathrow"),
    ("TW8", 18.00, "Brentford"),
    ("TW9", 28.00, "Richmond"),
    ("UB1", 30.00, "Southall"),
    ("UB3", 20.00, "Hayes"),
    ("UB6", 25.00, "Greenford"),
    ("HA0", 28.00, "Wembley"),
    ("HA1", 30.00, "Harrow"),
    ("HA4", 35.00, "Ruislip"),
    ("HA5", 32.00, "Pinner"),
    ("HA7", 35.00, "Stanmore"),
    ("HA9", 25.00, "Wembley Park"),
    ("KT1", 28.00, "Kingston"),
    ("KT3", 30.00, "New Malden"),
    ("KT6", 32.00, "Surbiton"),
    ("SM1", 35.00, "Sutton"),
    ("SM5", 38.00, "Carshalton"),
    ("CR0", 45.00, "Croydon"),
    ("CR2", 48.00, "South Croydon"),
    ("BR1", 55.00, "Bromley"),
    ("BR3", 58.00, "Beckenham"),
    ("DA1", 65.00, "Dartford"),
    ("DA5", 68.00, "Bexley"),
    ("IG1", 60.00, "Ilford"),
    ("IG3", 62.00, "Seven Kings"),
    ("RM1", 70.00, "Romford"),
    ("RM3", 72.00, "Harold Hill"),
    ("EN1", 60.00, "Enfield"),
    ("EN3", 62.00, "Enfield Highway"),
    ("EN5", 58.00, "Barnet"),
]


def get_conn():
    return sqlite3.connect(DB_PATH)


def init_db():
    cols = ", ".join(f"{name} {dtype}" for name, dtype in SCHEMA.items())
    with get_conn() as conn:
        conn.execute(f"CREATE TABLE IF NOT EXISTS fares ({cols})")


def seed_db():
    init_db()
    with get_conn() as conn:
        for prefix, cost, zone in SEED_DATA:
            conn.execute(
                "INSERT OR IGNORE INTO fares (postcode_prefix, cost, zone) VALUES (?, ?, ?)",
                (prefix, cost, zone),
            )
    print(f"Seeded {len(SEED_DATA)} fare records")


def lookup_fare(postcode_prefix: str):
    prefix = postcode_prefix.strip().upper()
    with get_conn() as conn:
        cursor = conn.execute(
            "SELECT postcode_prefix, cost, zone FROM fares WHERE postcode_prefix = ?",
            (prefix,),
        )
        row = cursor.fetchone()
        if row:
            return {"prefix": row[0], "cost": row[1], "zone": row[2]}
    return None


def fuzzy_lookup(postcode_prefix: str):
    prefix = postcode_prefix.strip().upper()
    with get_conn() as conn:
        cursor = conn.execute(
            "SELECT postcode_prefix, cost, zone FROM fares WHERE ? LIKE postcode_prefix || '%' ORDER BY LENGTH(postcode_prefix) DESC LIMIT 1",
            (prefix,),
        )
        row = cursor.fetchone()
        if row:
            return {"prefix": row[0], "cost": row[1], "zone": row[2]}
    return None
