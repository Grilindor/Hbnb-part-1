from datetime import datetime
from src import db
import uuid
from src.models.city import City
from src.models.user import User

class Place(db.Model):
    __tablename__ = 'places'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(1024))
    address = db.Column(db.String(256), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    host_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    city_id = db.Column(db.String(36), db.ForeignKey('cities.id'), nullable=False)
    price_per_night = db.Column(db.Integer, nullable=False)
    number_of_rooms = db.Column(db.Integer, nullable=False)
    number_of_bathrooms = db.Column(db.Integer, nullable=False)
    max_guests = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

    def __init__(self, data: dict | None = None, **kw) -> None:
        if data:
            self.name = data.get("name", "")
            self.description = data.get("description", "")
            self.address = data.get("address", "")
            self.city_id = data["city_id"]
            self.latitude = float(data.get("latitude", 0.0))
            self.longitude = float(data.get("longitude", 0.0))
            self.host_id = data["host_id"]
            self.price_per_night = int(data.get("price_per_night", 0))
            self.number_of_rooms = int(data.get("number_of_rooms", 0))
            self.number_of_bathrooms = int(data.get("number_of_bathrooms", 0))
            self.max_guests = int(data.get("max_guests", 0))

    def __repr__(self) -> str:
        return f"<Place {self.id} ({self.name})>"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "address": self.address,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "city_id": self.city_id,
            "host_id": self.host_id,
            "price_per_night": self.price_per_night,
            "number_of_rooms": self.number_of_rooms,
            "number_of_bathrooms": self.number_of_bathrooms,
            "max_guests": self.max_guests,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(data: dict) -> "Place":
        from src.persistence import repo

        user = User.query.get(data["host_id"])
        if not user:
            raise ValueError(f"User with ID {data['host_id']} not found")

        city = City.query.get(data["city_id"])
        if not city:
            raise ValueError(f"City with ID {data['city_id']} not found")

        new_place = Place(data=data)
        repo.save(new_place)
        return new_place

    @staticmethod
    def update(place_id: str, data: dict) -> "Place | None":
        from src.persistence import repo

        place = Place.query.get(place_id)
        if not place:
            return None

        for key, value in data.items():
            setattr(place, key, value)

        repo.update(place)
        return place
