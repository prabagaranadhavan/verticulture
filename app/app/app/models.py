import enum
import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Enum, Date, Text
)
from sqlalchemy.orm import relationship
from .database import Base


class SpaceType(str, enum.Enum):
    backyard = "backyard"
    terrace = "terrace"
    balcony = "balcony"
    room = "room"


class SoilType(str, enum.Enum):
    sandy = "sandy"
    clay = "clay"
    loamy = "loamy"
    silty = "silty"
    unknown = "unknown"


class SoilMethod(str, enum.Enum):
    manual = "manual"
    photo = "photo"
    quiz = "quiz"


class CropCategory(str, enum.Enum):
    leaf = "leaf"
    herb = "herb"
    vegetable = "vegetable"
    fruit = "fruit"


class Purpose(str, enum.Enum):
    home = "home"
    sell = "sell"


class TaskType(str, enum.Enum):
    watering = "watering"
    fertilizing = "fertilizing"
    pruning = "pruning"
    pest_check = "pest_check"


class SupplierType(str, enum.Enum):
    fertilizer = "fertilizer"
    seed = "seed"
    equipment = "equipment"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    location = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    spaces = relationship("Space", back_populates="owner", cascade="all, delete-orphan")


class Space(Base):
    __tablename__ = "spaces"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    area_sqft = Column(Float, nullable=False)
    space_type = Column(Enum(SpaceType), nullable=False)
    indoor = Column(Boolean, default=False)
    sunlight_hours = Column(Float, default=4.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    owner = relationship("User", back_populates="spaces")
    soil_profile = relationship("SoilProfile", back_populates="space", uselist=False,
                                 cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="space",
                                    cascade="all, delete-orphan")
    tasks = relationship("MaintenanceTask", back_populates="space",
                          cascade="all, delete-orphan")


class SoilProfile(Base):
    __tablename__ = "soil_profiles"

    id = Column(Integer, primary_key=True, index=True)
    space_id = Column(Integer, ForeignKey("spaces.id"), nullable=False, unique=True)
    soil_type = Column(Enum(SoilType), default=SoilType.unknown)
    method = Column(Enum(SoilMethod), default=SoilMethod.manual)
    photo_url = Column(String, nullable=True)
    confidence = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    space = relationship("Space", back_populates="soil_profile")


class Crop(Base):
    __tablename__ = "crops"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(Enum(CropCategory), nullable=False)
    water_needs = Column(String, default="medium")
    sunlight_needs_hours = Column(Float, default=4.0)
    space_needed_sqft = Column(Float, default=1.0)
    days_to_harvest = Column(Integer, default=30)
    suited_soil_types = Column(String, default="loamy")
    good_for_selling = Column(Boolean, default=False)

    # ---- growing-guide fields ----
    # Area one tray/pot/planting-spot takes up, used to estimate how many
    # fit in a user's available space.
    tray_area_sqft = Column(Float, default=1.0)
    watering_frequency_days = Column(Integer, default=2)
    fertilizing_frequency_days = Column(Integer, default=14)
    pruning_frequency_days = Column(Integer, nullable=True)
    pest_check_frequency_days = Column(Integer, nullable=True)
    # Step-by-step growing procedure, stored as steps joined by "|".
    care_steps = Column(Text, nullable=True)


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    space_id = Column(Integer, ForeignKey("spaces.id"), nullable=False)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=False)
    purpose = Column(Enum(Purpose), default=Purpose.home)
    score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    space = relationship("Space", back_populates="recommendations")
    crop = relationship("Crop")


class MaintenanceTask(Base):
    __tablename__ = "maintenance_tasks"

    id = Column(Integer, primary_key=True, index=True)
    space_id = Column(Integer, ForeignKey("spaces.id"), nullable=False)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=False)
    task_type = Column(Enum(TaskType), nullable=False)
    frequency_days = Column(Integer, nullable=False)
    next_due = Column(Date, nullable=False)
    last_completed = Column(Date, nullable=True)

    space = relationship("Space", back_populates="tasks")
    crop = relationship("Crop")


class MarketPrice(Base):
    __tablename__ = "market_prices"

    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=False)
    region = Column(String, nullable=False)
    price_per_kg = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    source = Column(String, nullable=True)

    crop = relationship("Crop")


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(Enum(SupplierType), nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    address = Column(String, nullable=True)
    contact = Column(String, nullable=True)