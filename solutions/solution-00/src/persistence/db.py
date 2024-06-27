"""
  Now is easy to implement the database repository. The DBRepository
  should implement the Repository (Storage) interface and the methods defined
  in the abstract class Storage.

  The methods to implement are:
    - get_all
    - get
    - save
    - update
    - delete
    - reload (which can be empty)
"""

from src.models.base import Base
from src.persistence.repository import Repository
from src import db  # Assurez-vous que votre application Flask est configurée pour utiliser SQLAlchemy
from sqlalchemy.orm.exc import NoResultFound

class DBRepository(Repository):
    """Database repository implementing the Storage interface"""

    def __init__(self) -> None:
        """Initialize the DBRepository"""
        self.__session = db.session

    def get_all(self, model_name: str) -> list:
        """Get all objects of a specific model"""
        try:
            model = getattr(db.models, model_name)
            return self.__session.query(model).all()
        except AttributeError:
            return []

    def get(self, model_name: str, obj_id: str) -> Base | None:
        """Get a specific object by model name and ID"""
        try:
            model = getattr(db.models, model_name)
            return self.__session.query(model).get(obj_id)
        except (AttributeError, NoResultFound):
            return None

    def reload(self) -> None:
        """Reload the database session (can be empty)"""
        self.__session.rollback()

    def save(self, obj: Base) -> None:
        """Save an object to the database"""
        self.__session.add(obj)
        self.__session.commit()

    def update(self, obj: Base) -> Base | None:
        """Update an object in the database"""
        try:
            self.__session.merge(obj)
            self.__session.commit()
            return obj
        except Exception as e:
            self.__session.rollback()
            print(f"Error updating object: {e}")
            return None

    def delete(self, obj: Base) -> bool:
        """Delete an object from the database"""
        try:
            self.__session.delete(obj)
            self.__session.commit()
            return True
        except Exception as e:
            self.__session.rollback()
            print(f"Error deleting object: {e}")
            return False

