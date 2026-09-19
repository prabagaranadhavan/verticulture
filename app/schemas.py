import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    location: Optional[str] = None


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    location: Optional[str] = None

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class SpaceCreate(BaseModel):
    area_sqft: float
    space_type: str
    indoor: bool = False
    sunlight_hours: float = 4.0


class SpaceOut(BaseModel):
    id: int
    area_sqft: float
    space_type: str
    indoor: bool
    sunlight_hours: float

    class Config:
        from_attributes = True


class SoilManualIn(BaseModel):
    soil_type: str


class SoilOut(BaseModel):
    soil_type: str
    method: str
    confidence: Optional[float] = None

    class Config:
        from_attributes = True


class RecommendationOut(BaseModel):
    crop_id: int
    crop_name: str
    category: str
    purpose: str
    score: float
    days_to_harvest: int


class CropGuideOut(BaseModel):
    crop_id: int
    crop_name: str
    category: str
    tray_area_sqft: float
    estimated_trays: int
    watering_frequency_days: int
    fertilizing_frequency_days: int
    pruning_frequency_days: Optional[int] = None
    pest_check_frequency_days: Optional[int] = None
    days_to_harvest: int
    steps: List[str]


class PlantRequest(BaseModel):
    crop_id: int


class TaskOut(BaseModel):
    id: int
    crop_name: str
    task_type: str
    frequency_days: int
    next_due: datetime.date

    class Config:
        from_attributes = True


class ScheduleSummaryOut(BaseModel):
    total_tasks: int
    on_track: int
    overdue: int
    care_score: float
    total_completions: int


class TaskCompleteIn(BaseModel):
    completed_on: Optional[datetime.date] = None


class MarketPriceOut(BaseModel):
    crop_name: str
    region: str
    price_per_kg: float
    date: datetime.date

    class Config:
        from_attributes = True


class SupplierOut(BaseModel):
    id: int
    name: str
    type: str
    lat: float
    lng: float
    address: Optional[str] = None

    class Config:
        from_attributes = True
