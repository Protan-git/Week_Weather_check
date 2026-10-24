from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    DateTime,
    UniqueConstraint
)

from database import Base


class WeatherRecord(Base):
    __tablename__ = 'weather_records'

    id = Column(Integer, primary_key=True, index=True)

    city = Column(String, nullable=False)
    record_date = Column(Date, nullable=False)
    recorded_at = Column(DateTime, nullable=False)

    temperature = Column(Float, nullable=False)
    feels_like = Column(Float, nullable=False)
    humidity = Column(Integer, nullable=False)
    pressure = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    wind_speed = Column(Float, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            'city',
            'record_date',
            name='unique_city_date'
        ),
    )