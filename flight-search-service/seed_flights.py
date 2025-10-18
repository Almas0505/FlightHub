"""
Seed real flights data to MongoDB
Популярные маршруты из Казахстана
"""
import asyncio
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
import random
import uuid

# MongoDB connection
import os
MONGO_URI = os.getenv("MONGODB_URL", "mongodb://mongodb:27017")
DB_NAME = "flight_search"

# Popular routes from Kazakhstan
ROUTES = [
    # From Almaty
    {"from": "ALA", "from_city": "Almaty", "to": "DXB", "to_city": "Dubai", "country": "UAE"},
    {"from": "ALA", "from_city": "Almaty", "to": "IST", "to_city": "Istanbul", "country": "Turkey"},
    {"from": "ALA", "from_city": "Almaty", "to": "SVO", "to_city": "Moscow", "country": "Russia"},
    {"from": "ALA", "from_city": "Almaty", "to": "DOH", "to_city": "Doha", "country": "Qatar"},
    {"from": "ALA", "from_city": "Almaty", "to": "TSE", "to_city": "Astana", "country": "Kazakhstan"},
    {"from": "ALA", "from_city": "Almaty", "to": "BKK", "to_city": "Bangkok", "country": "Thailand"},
    {"from": "ALA", "from_city": "Almaty", "to": "DEL", "to_city": "Delhi", "country": "India"},
    
    # From Astana
    {"from": "TSE", "from_city": "Astana", "to": "DXB", "to_city": "Dubai", "country": "UAE"},
    {"from": "TSE", "from_city": "Astana", "to": "IST", "to_city": "Istanbul", "country": "Turkey"},
    {"from": "TSE", "from_city": "Astana", "to": "SVO", "to_city": "Moscow", "country": "Russia"},
    {"from": "TSE", "from_city": "Astana", "to": "ALA", "to_city": "Almaty", "country": "Kazakhstan"},
]

# Airlines
AIRLINES = [
    {"code": "KC", "name": "Air Astana"},
    {"code": "EK", "name": "Emirates"},
    {"code": "TK", "name": "Turkish Airlines"},
    {"code": "QR", "name": "Qatar Airways"},
    {"code": "SU", "name": "Aeroflot"},
    {"code": "FZ", "name": "FlyDubai"},
]

# Aircraft types
AIRCRAFT = [
    "Boeing 737-800",
    "Airbus A320",
    "Boeing 787-9",
    "Airbus A321",
    "Boeing 777-300ER",
    "Airbus A330-200",
]


def generate_flight(route, date_offset=0):
    """Generate a single flight"""
    airline = random.choice(AIRLINES)
    
    # Base flight times (realistic for routes)
    duration_map = {
        "ALA-DXB": 240,  # 4 hours
        "ALA-IST": 300,  # 5 hours
        "ALA-SVO": 240,  # 4 hours
        "ALA-DOH": 240,  # 4 hours
        "ALA-TSE": 90,   # 1.5 hours
        "ALA-BKK": 360,  # 6 hours
        "ALA-DEL": 180,  # 3 hours
        "TSE-DXB": 270,  # 4.5 hours
        "TSE-IST": 330,  # 5.5 hours
        "TSE-SVO": 210,  # 3.5 hours
        "TSE-ALA": 90,   # 1.5 hours
    }
    
    route_key = f"{route['from']}-{route['to']}"
    duration = duration_map.get(route_key, 240)
    
    # Departure time (random time during day)
    dep_date = datetime.now() + timedelta(days=date_offset)
    dep_hour = random.randint(6, 22)
    dep_minute = random.choice([0, 15, 30, 45])
    departure_time = dep_date.replace(hour=dep_hour, minute=dep_minute, second=0, microsecond=0)
    arrival_time = departure_time + timedelta(minutes=duration)
    
    # Price calculation (based on route and cabin class)
    base_prices = {
        "economy": random.randint(30000, 80000),
        "premium_economy": random.randint(60000, 120000),
        "business": random.randint(150000, 350000),
    }
    
    cabin_class = random.choice(["economy", "economy", "economy", "premium_economy", "business"])
    base_fare = base_prices[cabin_class]
    taxes = base_fare * 0.15
    fees = 2000.0
    
    flight_id = f"FL-{uuid.uuid4().hex[:12]}"
    
    return {
        "id": flight_id,
        "segments": [{
            "id": f"SEG-{uuid.uuid4().hex[:8]}",
            "airline": airline,
            "flight_number": f"{airline['code']}{random.randint(100, 999)}",
            "aircraft_type": random.choice(AIRCRAFT),
            "departure": {
                "airport_code": route["from"],
                "airport_name": f"{route['from_city']} International",
                "city": route["from_city"],
                "country": "Kazakhstan" if route["from"] in ["ALA", "TSE"] else route["country"],
                "terminal": f"Terminal {random.randint(1, 3)}",
                "datetime": departure_time.isoformat()
            },
            "arrival": {
                "airport_code": route["to"],
                "airport_name": f"{route['to_city']} International",
                "city": route["to_city"],
                "country": route["country"],
                "terminal": f"Terminal {random.randint(1, 3)}",
                "datetime": arrival_time.isoformat()
            },
            "duration_minutes": duration,
            "cabin_class": cabin_class,
            "available_seats": random.randint(10, 100),
            "baggage": {
                "checked": {"pieces": 1 if cabin_class == "economy" else 2, "weight_kg": 23},
                "carry_on": {"pieces": 1, "weight_kg": 7}
            },
            "meal_included": True,
            "wifi_available": random.choice([True, False])
        }],
        "price": {
            "base_fare": base_fare,
            "taxes": taxes,
            "fees": fees,
            "total": base_fare + taxes + fees,
            "currency": "KZT"
        },
        "cabin_class": cabin_class,
        "total_duration_minutes": duration,
        "stops": 0,
        "refundable": random.choice([True, False]),
        "changeable": True,
        "change_fee": 5000.0 if random.choice([True, False]) else None,
        "baggage": {
            "checked": {"pieces": 1 if cabin_class == "economy" else 2, "weight_kg": 23},
            "carry_on": {"pieces": 1, "weight_kg": 7}
        },
        "provider": "seed",
        "cached_at": datetime.utcnow().isoformat(),
        "expires_at": (datetime.utcnow() + timedelta(days=30)).isoformat(),
        "created_at": datetime.utcnow().timestamp(),
    }


async def seed_flights():
    """Seed flights to MongoDB"""
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db.flights
    
    print("🌱 Starting seed process...")
    print(f"📍 Routes: {len(ROUTES)}")
    
    # Clear existing seed flights
    result = await collection.delete_many({"provider": "seed"})
    print(f"🗑️  Deleted {result.deleted_count} old seed flights")
    
    # Generate flights for next 30 days
    flights_to_insert = []
    
    for route in ROUTES:
        # Generate 3-5 flights per day for next 7 days
        for day_offset in range(7):
            num_flights = random.randint(3, 5)
            for _ in range(num_flights):
                flight = generate_flight(route, day_offset)
                flights_to_insert.append(flight)
    
    # Insert flights
    if flights_to_insert:
        result = await collection.insert_many(flights_to_insert)
        print(f"✅ Inserted {len(result.inserted_ids)} flights")
    
    # Create TTL index
    await collection.create_index("expires_at", expireAfterSeconds=0)
    print("⏰ TTL index created")
    
    # Show stats
    total_flights = await collection.count_documents({})
    print(f"\n📊 Database Statistics:")
    print(f"   Total flights: {total_flights}")
    
    # Show sample flights
    print(f"\n📋 Sample Flights:")
    async for flight in collection.find({"provider": "seed"}).limit(5):
        seg = flight['segments'][0]
        print(f"   {seg['flight_number']}: {seg['departure']['airport_code']} → "
              f"{seg['arrival']['airport_code']} | "
              f"{int(flight['price']['total']):,} KZT | {flight['cabin_class']}")
    
    client.close()
    print("\n✨ Seed completed successfully!")


if __name__ == "__main__":
    asyncio.run(seed_flights())
