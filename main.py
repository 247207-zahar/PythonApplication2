from fastapi import FastAPI, HTTPException
from uuid import uuid4, UUID
from models import *
from database import events

app = FastAPI(title="Event Booking API")


@app.post("/events", response_model=Event, status_code=201)
def create_event(event: EventCreate):

    event_id = uuid4()

    new_event = Event(
        id=event_id,
        title=event.title,
        event_date=event.event_date,
        total_capacity=event.total_capacity,
        booked_seats=0
    )

    events[event_id] = new_event

    return new_event


@app.post("/events/{event_id}/book")
def book_seats(event_id: UUID, booking: Booking):

    if event_id not in events:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    event = events[event_id]

    remaining = event.total_capacity - event.booked_seats

    if booking.seats > remaining:
        raise HTTPException(
            status_code=422,
            detail=f"Only {remaining} seats remaining"
        )

    event.booked_seats += booking.seats

    events[event_id] = event

    return {
        "message": "Booking Successful",
        "Booked": booking.seats,
        "Remaining": event.total_capacity - event.booked_seats
    }


@app.get("/events/{event_id}")
def get_event(event_id: UUID):

    if event_id not in events:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    return events[event_id]
