"""
Country related functionality
"""


from datetime import datetime
from src import db
import uuid

class Country(db.Model):
    __tablename__ = 'countries'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(128), nullable=False)
    code = db.Column(db.String(3), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

    def __init__(self, name: str, code: str):
        self.name = name
        self.code = code

    def __repr__(self) -> str:
        return f"<Country {self.code} ({self.name})>"

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "code": self.code,
        }

    @staticmethod
    def get_all() -> list["Country"]:
        return Country.query.all()

    @staticmethod
    def get(code: str) -> "Country | None":
        return Country.query.filter_by(code=code).first()

    @staticmethod
    def create(name: str, code: str) -> "Country":
        country = Country(name, code)
        db.session.add(country)
        db.session.commit()
        return country
