import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(tags=["growing"])


@router.get("/crops/{crop_id}/guide", response_model=schemas.CropGuideOut)
def get_crop_guide(crop_id: int, area_sqft: float = Query(...), db: Session = Depends(get_db)):
    crop = db.query(models.Crop).get(crop_id)
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")

    tray_area = crop.tray_area_sqft or 1.0
    estimated_trays = max(1, int(area_sqft // tray_area))
    step_list = crop.care_steps.split("|") if crop.care_steps else []

    return {
        "crop_id": crop.id,
        "crop_name": crop.name,
        "category": crop.category.value,
        "tray_area_sqft": tray_area,
        "estimated_trays": estimated_trays,
        "watering_frequency_days": crop.watering_frequency_days,
        "fertilizing_frequency_days": crop.fertilizing_frequency_days,
        "pruning_frequency_days": crop.pruning_frequency_days,
        "pest_check_frequency_days": crop.pest_check_frequency_days,
        "days_to_harvest": crop.days_to_harvest,
        "steps": step_list,
    }


@router.post("/spaces/{space_id}/plant", response_model=list[schemas.TaskOut])
def plant_crop(space_id: int, body: schemas.PlantRequest, db: Session = Depends(get_db)):
    space = db.query(models.Space).get(space_id)
    if not space:
        raise HTTPException(status_code=404, detail="Space not found")

    crop = db.query(models.Crop).get(body.crop_id)
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")

    today = datetime.date.today()
    schedule_plan = [
        (models.TaskType.watering, crop.watering_frequency_days),
        (models.TaskType.fertilizing, crop.fertilizing_frequency_days),
    ]
    if crop.pruning_frequency_days:
        schedule_plan.append((models.TaskType.pruning, crop.pruning_frequency_days))
    if crop.pest_check_frequency_days:
        schedule_plan.append((models.TaskType.pest_check, crop.pest_check_frequency_days))

    created_tasks = []
    for task_type, frequency in schedule_plan:
        task = models.MaintenanceTask(
            space_id=space_id,
            crop_id=crop.id,
            task_type=task_type,
            frequency_days=frequency,
            next_due=today + datetime.timedelta(days=frequency),
        )
        db.add(task)
        created_tasks.append(task)

    db.commit()
    for task in created_tasks:
        db.refresh(task)

    return [
        {
            "id": t.id,
            "crop_name": crop.name,
            "task_type": t.task_type.value,
            "frequency_days": t.frequency_days,
            "next_due": t.next_due,
        }
        for t in created_tasks
    ]