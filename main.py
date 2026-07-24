from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rooms = [
    {
        "id": 1,
        "room_number": 101,
        "room_type": "Single",
        "price": 300000,
        "is_available": True
    },
    {
        "id": 2,
        "room_number": 102,
        "room_type": "Double",
        "price": 500000,
        "is_available": True
    },
    {
        "id": 3,
        "room_number": 103,
        "room_type": "Luxury",
        "price": 900000,
        "is_available": False
    },
    {
        "id": 4,
        "room_number": 777,
        "room_type": "President",
        "price": 0.99,
        "is_available": True
    }
]

class RoomCreate(BaseModel):
    room_number: int
    room_type: str
    price: int
    is_available: bool = True
    
class RoomUpdate(BaseModel):
    room_number: int
    room_type: str
    price: int
    is_available: bool

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )
    
@app.get("/rooms")
def get_rooms():
    return rooms

@app.get("/rooms/{room_id}")
def get_room(room_id: int):
    for room in rooms:
        if room["id"] == room_id:
            return room
    raise HTTPException(
        status_code=404,
        detail="Xana tabilmadi yaki joq uliwma"
    )
    
@app.post("/rooms")
def create_room(new_room: RoomCreate):
    room = {
        "id": len(rooms) + 1,
        "room_number": new_room.room_number,
        "room_type": new_room.room_type,
        "price": new_room.price,
        "is_available": new_room.is_available
    }
    
    rooms.append(room)
    
    return {
        "message": "Jana Xana qosildi",
        "room": room
    }
    
@app.put("/rooms/{room_id}")
def update_room(room_id: int, update_room: RoomUpdate):
    for room in rooms:
        if room["id"] == room_id:
            room["room_number"] = update_room.room_number
            room["room_type"] = update_room.room_type
            room["price"] = update_room.price
            room["is_available"] = update_room.is_available
            
            return {
                "message": "Xana janalandi",
                "room": room
            }
    raise HTTPException(
        status_code=404,
        detail="Xana tabilmadi"
    )
    
@app.delete("/rooms/{room_id}")
def delete_room(room_id: int):

    for room in rooms:
        if room["id"] == room_id:
            rooms.remove(room)

            return {
                "message": "Xona o‘chirildi",
                "room": room
            }

    raise HTTPException(
        status_code=404,
        detail="Xona topilmadi"
    )
    
# start Booking

class BookingCreate(BaseModel):
    room_id: int
    guest_name: str
    phone: str
    
bookings = []

@app.post("/bookings")
def create_booking(new_booking: BookingCreate):
    selected_room = None
    
    for room in rooms:
        if room["id"] == new_booking.room_id:
            selected_room = room
            break
        
    if selected_room is None:
        raise HTTPException(
            status_code=404,
            detail="xana tabilmadi"
        )
        
    if selected_room["is_available"] == False:
        raise HTTPException(
            status_code=400,
            detail="Xana Aldin Bron qilingan"
        )
        
    booking = {
        "id": len(bookings) + 1,
        "room_id": new_booking.room_id,
        "guest_name": new_booking.guest_name,
        "phone": new_booking.phone
    }
    
    bookings.append(booking)
    
    selected_room["is_available"] = False
    
    return {
        "message": "Xana bron qilindi",
        "Booking": booking
    }
    
@app.get("/bookings")
def get_bookings():
    return bookings

@app.delete("/bookings/{booking_id}")
def cancel_booking(booking_id: int):
    for booking in bookings:
        if booking["id"] == booking_id:
            for room in rooms:
                if room["id"] == booking["room_id"]:
                    room["is_available"] = True
                    break
                
            bookings.remove(booking)
            
            return {
                "message": "Bron otmen qilindi",
                "booking": booking
            }
    raise HTTPException(
        status_code=404,
        detail="Bron tabilmadi"
    )
