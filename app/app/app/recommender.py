from sqlalchemy.orm import Session
from . import models


def score_crop(crop: models.Crop, space: models.Space, soil_type: str) -> float:
    score = 0.0

    suited = [s.strip() for s in crop.suited_soil_types.split(",")]
    if soil_type in suited:
        score += 40
    elif soil_type == "unknown":
        score += 15

    if crop.space_needed_sqft <= space.area_sqft:
        score += 30
    else:
        ratio = space.area_sqft / crop.space_needed_sqft
        score += max(0, 30 * ratio)

    if space.sunlight_hours >= crop.sunlight_needs_hours:
        score += 20
    else:
        deficit = crop.sunlight_needs_hours - space.sunlight_hours
        score += max(0, 20 - deficit * 5)

    if crop.days_to_harvest <= 45:
        score += 10
    elif crop.days_to_harvest <= 90:
        score += 5

    return round(score, 1)


def recommend_crops(db: Session, space: models.Space, top_n: int = 8):
    soil_type = "unknown"
    if space.soil_profile:
        soil_type = space.soil_profile.soil_type.value

    crops = db.query(models.Crop).all()
    scored = [(crop, score_crop(crop, space, soil_type)) for crop in crops]
    scored.sort(key=lambda pair: pair[1], reverse=True)

    results = []
    for crop, score in scored[:top_n]:
        purpose = "sell" if crop.good_for_selling and score >= 50 else "home"
        results.append({
            "crop_id": crop.id,
            "crop_name": crop.name,
            "category": crop.category.value,
            "purpose": purpose,
            "score": score,
            "days_to_harvest": crop.days_to_harvest,
        })
    return results