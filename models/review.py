from models.base import Base
from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

class Review(Base):
    __tablename__ = 'review'

    id = mapped_column(Integer, primary_key=True)
    email = mapped_column(String(30), nullable= False)
    description = mapped_column(Text)
    rating = mapped_column(Integer)
    
    def __repr__(self):
        return f'<Review {self.id}>'