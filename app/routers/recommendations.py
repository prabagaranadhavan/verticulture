import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..recommender import recommend_crops

router = APIRouter(prefix="/spaces", tags=["recommendations"])


@router.get("/{space_id}/recommendations", response_model=list[schemas.RecommendationOut])
def get_recommendations(space_id: int, db: Session = Depends(get_db)):
    space = db.query(models.Space).get(space_id)
    if not space:
        raise HTTPException(status_code=404, detail="Space not found")

    return recommend_crops(db, space)


@router.get("/{space_id}/schedule", response_model=list[schemas.TaskOut])
def get_schedule(space_id: int, db: Session = Depends(get_db)):
    tasks = (
        db.query(models.MaintenanceTask)
        .filter(models.MaintenanceTask.space_id == space_id)
        .order_by(models.MaintenanceTask.next_due)
        .all()
    )
    return [
        {
            "id": t.id,
            "crop_name": t.crop.name,
            "task_type": t.task_type.value,
            "frequency_days": t.frequency_days,
            "next_due": t.next_due,
        }
        for t in tasks
    ]


@router.get("/{space_id}/schedule/summary", response_model=schemas.ScheduleSummaryOut)
def get_schedule_summary(space_id: int, db: Session = Depends(get_db)):
    tasks = (
        db.query(models.MaintenanceTask)
        .filter(models.MaintenanceTask.space_id == space_id)
        .all()
    )

    today = datetime.date.today()
    total_tasks = len(tasks)
    overdue = sum(1 for t in tasks if t.next_due < today)
    on_track = total_tasks - overdue
    total_completions = sum(t.times_completed or 0 for t in tasks)
    care_score = round((on_track / total_tasks) * 100, 1) if total_tasks > 0 else 100.0

    return {
        "total_tasks": total_tasks,
        "on_track": on_track,
        "overdue": overdue,
        "care_score": care_score,
        "total_completions": total_completions,
    }


@router.post("/{space_id}/schedule/{task_id}/complete", response_model=schemas.TaskOut)
def complete_task(space_id: int, task_id: int, body: schemas.TaskCompleteIn, db: Session = Depends(get_db)):
    task = db.query(models.MaintenanceTask).get(task_id)
    if not task or task.space_id != space_id:
        raise HTTPException(status_code=404, detail="Task not found")

    completed_on = body.completed_on or datetime.date.today()
    task.last_completed = completed_on
    task.next_due = completed_on + datetime.timedelta(days=task.frequency_days)
    task.times_completed = (task.times_completed or 0) + 1
    db.commit()
    db.refresh(task)

    return {
        "id": task.id,
        "crop_name": task.crop.name,
        "task_type": task.task_type.value,
        "frequency_days": task.frequency_days,
        "next_due": task.next_due,
    }
