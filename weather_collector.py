from datetime import date, datetime

from database import SessionLocal, init_db
from models import WeatherRecord
from get_api import get_weather


CITIES = [
    'Rostov-on-Don',
    'Moscow',
    'Kazan'
]


def collect_weather():
    init_db()

    today = date.today()

    session = SessionLocal()

    try:
        for city in CITIES:
            print(f'Получаем погоду: {city}')

            data = get_weather(city, 'ru')

            if not data:
                print(f'Не удалось получить погоду для {city}')
                continue

            existing_record = session.query(WeatherRecord).filter_by(
                city=city,
                record_date=today
            ).first()

            if existing_record:
                print(f'Запись за {today} уже существует. Пропускаем.')
                continue

            try:
                main = data['main']
                weather = data['weather'][0]
                wind = data.get('wind', {})

                # Создаём объект будущей записи
                record = WeatherRecord(
                    city=city,
                    record_date=today,
                    recorded_at=datetime.now(),
                    temperature=main['temp'],
                    feels_like=main['feels_like'],
                    humidity=main['humidity'],
                    pressure=main['pressure'],
                    description=weather['description'],
                    wind_speed=wind.get('speed', 0)
                )

                session.add(record)
                session.commit()

                print(
                    f'Сохранено: {city}, '
                    f'{record.temperature} °C, '
                    f'{record.description}'
                )

            except (KeyError, IndexError, TypeError) as error:
                session.rollback()
                print(f'Некорректные данные для {city}: {error}')

            except Exception as error:
                session.rollback()
                print(f'Ошибка сохранения для {city}: {error}')

    finally:
        session.close()


if __name__ == '__main__':
    collect_weather()