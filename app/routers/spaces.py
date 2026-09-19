from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/spaces", tags=["spaces"])


@router.post("", response_model=schemas.SpaceOut)
def create_space(space_in: schemas.SpaceCreate, user_id: int, db: Session = Depends(get_db)):
    space = models.Space(
        user_id=user_id,
        area_sqft=space_in.area_sqft,
        space_type=space_in.space_type,
        indoor=space_in.indoor,
        sunlight_hours=space_in.sunlight_hours,
    )
    db.add(space)
    db.commit()
    db.refresh(space)
    return space


@router.get("/{space_id}", response_model=schemas.SpaceOut)
def get_space(space_id: int, db: Session = Depends(get_db)):
    space = db.query(models.Space).get(space_id)
    if not space:
        raise HTTPException(status_code=404, detail="Space not found")
    return space


@router.post("/{space_id}/soil", response_model=schemas.SoilOut)
def set_soil_manual(space_id: int, soil_in: schemas.SoilManualIn, db: Session = Depends(get_db)):
    space = db.query(models.Space).get(space_id)
    if not space:
        raise HTTPException(status_code=404, detail="Space not found")

    profile = space.soil_profile or models.SoilProfile(space_id=space_id)
    profile.soil_type = soil_in.soil_type
    profile.method = "manual"
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@router.post("/{space_id}/soil/photo", response_model=schemas.SoilOut)
async def set_soil_from_photo(space_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    space = db.query(models.Space).get(space_id)
    if not space:
        raise HTTPException(status_code=404, detail="Space not found")

    contents = await file.read()
    predicted_soil_type = "loamy"
    confidence = 0.0

    profile = space.soil_profile or models.SoilProfile(space_id=space_id)
    profile.soil_type = predicted_soil_type
    profile.method = "photo"
    profile.confidence = confidence
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile
