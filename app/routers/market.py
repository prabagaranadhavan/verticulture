import math
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from .. import models, schemas
from ..database import get_db

router = APIRouter(tags=["market"])


@router.get("/market/prices", response_model=list[schemas.MarketPriceOut])
def get_market_prices(
    crop: Optional[str] = None,
    region: Optional[str] = None,
    db: Session = Depends(get_db),
):
    q = db.query(models.MarketPrice).join(models.Crop)
    if crop:
        q = q.filter(models.Crop.name.ilike(f"%{crop}%"))
    if region:
        q = q.filter(models.MarketPrice.region.ilike(f"%{region}%"))

    prices = q.order_by(models.MarketPrice.date.desc()).limit(50).all()
    return [
        {
            "crop_name": p.crop.name,
            "region": p.region,
            "price_per_kg": p.price_per_kg,
            "date": p.date,
        }
        for p in prices
    ]


def _distance_km(lat1, lng1, lat2, lng2):
    r = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lng2 - lng1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


@router.get("/suppliers", response_model=list[schemas.SupplierOut])
def get_suppliers(
    lat: float = Query(...),
    lng: float = Query(...),
    type: Optional[str] = None,
    radius_km: float = 15.0,
    db: Session = Depends(get_db),
):
    q = db.query(models.Supplier)
    if type:
        q = q.filter(models.Supplier.type == type)

    suppliers = q.all()
    nearby = [s for s in suppliers if _distance_km(lat, lng, s.lat, s.lng) <= radius_km]
    nearby.sort(key=lambda s: _distance_km(lat, lng, s.lat, s.lng))
    return nearby
