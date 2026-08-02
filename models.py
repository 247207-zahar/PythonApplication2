from pydantic import BaseModel, Field
from datetime import date
from uuid import UUID

class EventCreate(BaseModel):
    title: str
    event_date: date
    total_capacity: int = Field(gt=0)


class Event(BaseModel):
    id: UUID
    title: str
    event_date: date
    total_capacity: int
    booked_seats: int = 0


class Booking(BaseModel):
    seats: int = Field(gt=0)