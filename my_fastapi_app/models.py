from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class FctMessage(Base):
    __tablename__ = "fct_messages"
    __table_args__ = {"schema": "raw"}  # or your dbt schema name

    telegram_message_id = Column(Integer, primary_key=True, index=True)
    channel_name = Column(String)
    message_text = Column(String)
    product_name = Column(String)  # optional, if you're extracting product names
    date = Column(DateTime)
    view_count = Column(Integer)


class FctImageDetection(Base):
    __tablename__ = "fct_image_detections"
    __table_args__ = {"schema": "raw"}  

    message_id = Column(Integer, primary_key=True)
    detected_object_class = Column(String, primary_key=True)
    detected_at = Column(DateTime, primary_key=True)
    confidence_score = Column(Float)
    image_path = Column(String)
