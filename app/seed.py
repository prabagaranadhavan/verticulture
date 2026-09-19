from .database import SessionLocal, Base, engine
from . import models
import datetime

Base.metadata.create_all(bind=engine)


def steps(*lines):
    return "|".join(lines)


STARTER_CROPS = [
    dict(
        name="Spinach", category="leaf", water_needs="medium", sunlight_needs_hours=4,
        space_needed_sqft=0.5, days_to_harvest=30, suited_soil_types="loamy,silty", good_for_selling=True,
        tray_area_sqft=0.5, watering_frequency_days=1, fertilizing_frequency_days=14,
        pruning_frequency_days=None, pest_check_frequency_days=7,
        care_steps=steps(
            "Fill a tray 4-6 inches deep with loamy or silty soil mixed with compost.",
            "Sow seeds about 1 inch apart and cover lightly with soil.",
            "Water once daily - keep the soil consistently moist, never soggy.",
            "Thin seedlings to 3 inches apart once they sprout.",
            "Feed with a balanced liquid fertilizer every 2 weeks.",
            "Harvest outer leaves at 3-4 inches long, leaving the center to keep growing.",
        ),
    ),
    dict(
        name="Mint", category="herb", water_needs="medium", sunlight_needs_hours=3,
        space_needed_sqft=0.3, days_to_harvest=25, suited_soil_types="loamy,clay", good_for_selling=True,
        tray_area_sqft=0.3, watering_frequency_days=2, fertilizing_frequency_days=21,
        pruning_frequency_days=14, pest_check_frequency_days=7,
        care_steps=steps(
            "Use a wide, shallow tray or pot - mint spreads fast, so give it its own container.",
            "Plant cuttings or seedlings about 4 inches apart in loamy or clay soil.",
            "Water every 2 days, keeping soil moist but well-drained.",
            "Trim back growth every 2 weeks to keep it bushy and stop it overtaking the tray.",
            "Feed with diluted fertilizer once every 3 weeks.",
            "Harvest leaves regularly from the top to encourage fresh new growth.",
        ),
    ),
    dict(
        name="Coriander", category="herb", water_needs="low", sunlight_needs_hours=4,
        space_needed_sqft=0.3, days_to_harvest=28, suited_soil_types="loamy,sandy", good_for_selling=True,
        tray_area_sqft=0.3, watering_frequency_days=2, fertilizing_frequency_days=21,
        pruning_frequency_days=None, pest_check_frequency_days=7,
        care_steps=steps(
            "Fill a tray with light, well-draining loamy or sandy soil.",
            "Scatter seeds thinly and cover with a thin layer of soil.",
            "Water every 2 days - coriander doesn't like to sit in wet soil.",
            "Keep in a spot with 3-4 hours of indirect sunlight to avoid bolting.",
            "Feed lightly with fertilizer every 3 weeks.",
            "Harvest by snipping outer stems once the plant reaches 4-6 inches.",
        ),
    ),
    dict(
        name="Lettuce", category="leaf", water_needs="medium", sunlight_needs_hours=4,
        space_needed_sqft=0.5, days_to_harvest=35, suited_soil_types="loamy,silty", good_for_selling=False,
        tray_area_sqft=0.5, watering_frequency_days=1, fertilizing_frequency_days=14,
        pruning_frequency_days=None, pest_check_frequency_days=7,
        care_steps=steps(
            "Fill trays 6 inches deep with loamy or silty soil enriched with compost.",
            "Sow seeds 6 inches apart, or transplant seedlings at that spacing.",
            "Water daily to keep soil evenly moist - lettuce roots are shallow.",
            "Feed with a balanced fertilizer every 2 weeks.",
            "Watch for slugs and aphids weekly, especially in humid conditions.",
            "Harvest outer leaves as needed, or cut the whole head once mature.",
        ),
    ),
    dict(
        name="Tomato", category="vegetable", water_needs="high", sunlight_needs_hours=6,
        space_needed_sqft=2.0, days_to_harvest=70, suited_soil_types="loamy,sandy", good_for_selling=True,
        tray_area_sqft=2.0, watering_frequency_days=2, fertilizing_frequency_days=10,
        pruning_frequency_days=7, pest_check_frequency_days=5,
        care_steps=steps(
            "Use a large grow bag or pot at least 12 inches deep - one plant per container.",
            "Fill with loamy or sandy soil enriched with compost.",
            "Transplant seedlings once they have 3-4 true leaves.",
            "Stake or cage each plant early to support it as it grows tall.",
            "Water deeply every 2 days, aiming at the soil rather than the leaves.",
            "Feed with a phosphorus-rich fertilizer every 10 days once flowering starts.",
            "Prune side suckers weekly so the plant focuses energy on fruiting branches.",
            "Check for aphids and whiteflies every 5 days - tomatoes attract pests easily.",
        ),
    ),
    dict(
        name="Okra", category="vegetable", water_needs="medium", sunlight_needs_hours=6,
        space_needed_sqft=1.5, days_to_harvest=60, suited_soil_types="loamy,sandy,clay", good_for_selling=True,
        tray_area_sqft=1.5, watering_frequency_days=2, fertilizing_frequency_days=12,
        pruning_frequency_days=None, pest_check_frequency_days=7,
        care_steps=steps(
            "Use a deep pot or grow bag, one plant per container, in loamy or sandy soil.",
            "Sow seeds directly and thin to the strongest seedling once sprouted.",
            "Water every 2 days, more often during hot, dry spells.",
            "Feed with a balanced fertilizer every 12 days.",
            "Check weekly for aphids and pod borers.",
            "Harvest pods every 2-3 days once they reach 3-4 inches - they get tough if left too long.",
        ),
    ),
    dict(
        name="Chilli", category="vegetable", water_needs="medium", sunlight_needs_hours=6,
        space_needed_sqft=1.0, days_to_harvest=75, suited_soil_types="loamy,sandy", good_for_selling=True,
        tray_area_sqft=1.0, watering_frequency_days=2, fertilizing_frequency_days=12,
        pruning_frequency_days=14, pest_check_frequency_days=5,
        care_steps=steps(
            "Use a medium pot (10-12 inches) with loamy or sandy soil, one plant per pot.",
            "Transplant seedlings once they have 4-5 true leaves.",
            "Water every 2 days, keeping soil moist but not waterlogged.",
            "Feed with a balanced fertilizer every 12 days, more potassium once fruiting.",
            "Prune leggy branches every 2 weeks to encourage bushier growth.",
            "Check for aphids and mites every 5 days, especially on new growth.",
            "Harvest pods once they reach full color for the variety you're growing.",
        ),
    ),
    dict(
        name="Guava", category="fruit", water_needs="medium", sunlight_needs_hours=6,
        space_needed_sqft=25.0, days_to_harvest=730, suited_soil_types="loamy,clay", good_for_selling=True,
        tray_area_sqft=25.0, watering_frequency_days=4, fertilizing_frequency_days=30,
        pruning_frequency_days=60, pest_check_frequency_days=14,
        care_steps=steps(
            "Choose a planting spot with at least 6 hours of direct sun and good drainage.",
            "Dig a hole twice the width of the root ball and mix in compost with loamy or clay soil.",
            "Water deeply every 4 days while establishing, tapering off once mature.",
            "Feed with a balanced fertilizer once a month during the growing season.",
            "Prune every 2 months to shape the tree and remove dead or crossing branches.",
            "Check for fruit flies and scale insects every 2 weeks.",
            "Expect first fruit in 1-2 years - harvest when the fruit gives slightly to gentle pressure.",
        ),
    ),
    dict(
        name="Papaya", category="fruit", water_needs="medium", sunlight_needs_hours=6,
        space_needed_sqft=15.0, days_to_harvest=270, suited_soil_types="loamy,sandy", good_for_selling=True,
        tray_area_sqft=15.0, watering_frequency_days=3, fertilizing_frequency_days=30,
        pruning_frequency_days=None, pest_check_frequency_days=14,
        care_steps=steps(
            "Pick a warm, sheltered planting spot with well-draining loamy or sandy soil.",
            "Plant seedlings in a raised mound to prevent waterlogging at the roots.",
            "Water every 3 days, keeping soil moist but never flooded.",
            "Feed with a balanced fertilizer every month, increasing potassium as fruit forms.",
            "Check every 2 weeks for mealybugs and fungal spots on leaves.",
            "Harvest fruit once it starts turning yellow at the base - it ripens quickly after that.",
        ),
    ),
    dict(
        name="Lemon", category="fruit", water_needs="low", sunlight_needs_hours=6,
        space_needed_sqft=20.0, days_to_harvest=545, suited_soil_types="loamy,sandy", good_for_selling=True,
        tray_area_sqft=20.0, watering_frequency_days=4, fertilizing_frequency_days=45,
        pruning_frequency_days=90, pest_check_frequency_days=14,
        care_steps=steps(
            "Choose a sunny planting spot with loamy or sandy, well-draining soil.",
            "Plant in a hole twice the width of the root ball, backfilled with compost-enriched soil.",
            "Water deeply every 4 days while young; established trees need less frequent watering.",
            "Feed with a citrus-specific fertilizer every 6 weeks during the growing season.",
            "Prune every 3 months to remove dead wood and improve airflow.",
            "Check every 2 weeks for citrus leaf miner and scale insects.",
            "First harvest typically takes 1.5-2 years - pick fruit once it's fully colored and slightly soft.",
        ),
    ),
]


SAMPLE_MARKET_PRICES = [
    ("Spinach", "Chennai", 18.0),
    ("Spinach", "Coimbatore", 16.0),
    ("Mint", "Chennai", 42.0),
    ("Mint", "Bangalore", 45.0),
    ("Coriander", "Chennai", 30.0),
    ("Coriander", "Coimbatore", 28.0),
    ("Lettuce", "Chennai", 55.0),
    ("Tomato", "Chennai", 28.0),
    ("Tomato", "Bangalore", 24.0),
    ("Tomato", "Coimbatore", 26.0),
    ("Okra", "Chennai", 32.0),
    ("Okra", "Bangalore", 30.0),
    ("Chilli", "Chennai", 60.0),
    ("Chilli", "Coimbatore", 58.0),
    ("Guava", "Chennai", 40.0),
    ("Papaya", "Chennai", 22.0),
    ("Lemon", "Chennai", 70.0),
]

SAMPLE_SUPPLIERS = [
    dict(name="Chennai Agro Fertilizers", type="fertilizer", lat=13.0827, lng=80.2707,
         address="Anna Salai, Chennai", contact="044-2345-6789"),
    dict(name="Greenhouse Seed Co.", type="seed", lat=13.0604, lng=80.2496,
         address="T. Nagar, Chennai", contact="044-2345-1122"),
    dict(name="Vertical Grow Equipment", type="equipment", lat=13.1067, lng=80.2206,
         address="Anna Nagar, Chennai", contact="044-2345-3344"),
    dict(name="Urban Roots Nursery", type="seed", lat=13.0067, lng=80.2206,
         address="Adyar, Chennai", contact="044-2345-5566"),
    dict(name="South Fert Supplies", type="fertilizer", lat=12.9716, lng=80.2200,
         address="Velachery, Chennai", contact="044-2345-7788"),
    dict(name="Tower Farm Tools", type="equipment", lat=13.0475, lng=80.1970,
         address="Vadapalani, Chennai", contact="044-2345-9900"),
]


def seed_market_prices(db):
    if db.query(models.MarketPrice).count() > 0:
        print("Market prices already seeded, skipping.")
        return

    today = datetime.date.today()
    added = 0
    for crop_name, region, price in SAMPLE_MARKET_PRICES:
        crop = db.query(models.Crop).filter(models.Crop.name == crop_name).first()
        if not crop:
            continue
        db.add(models.MarketPrice(
            crop_id=crop.id,
            region=region,
            price_per_kg=price,
            date=today,
            source="Rootline sample data",
        ))
        added += 1
    db.commit()
    print(f"Seeded {added} market price rows.")


def seed_suppliers(db):
    if db.query(models.Supplier).count() > 0:
        print("Suppliers already seeded, skipping.")
        return

    for s in SAMPLE_SUPPLIERS:
        db.add(models.Supplier(**s))
    db.commit()
    print(f"Seeded {len(SAMPLE_SUPPLIERS)} suppliers.")


def run():
    db = SessionLocal()
    try:
        existing_count = db.query(models.Crop).count()
        if existing_count > 0:
            print(f"Crops table already has {existing_count} rows.")
            print("Updating existing crops with growing-guide fields (won't duplicate)...")
            for c in STARTER_CROPS:
                crop = db.query(models.Crop).filter(models.Crop.name == c["name"]).first()
                if crop:
                    for key, value in c.items():
                        setattr(crop, key, value)
                else:
                    db.add(models.Crop(**c))
            db.commit()
            print("Done updating crops.")
        else:
            for c in STARTER_CROPS:
                db.add(models.Crop(**c))
            db.commit()
            print(f"Seeded {len(STARTER_CROPS)} crops.")

        seed_market_prices(db)
        seed_suppliers(db)
    finally:
        db.close()


if __name__ == "__main__":
    run()
