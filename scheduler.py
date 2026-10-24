from apscheduler.schedulers.blocking import BlockingScheduler

from weather_collector import collect_weather

scheduler = BlockingScheduler(timezone="Europe/Moscow")


def collect_safely():
    try:
        print("Начинаем сбор погоды...")
        collect_weather()
        print("Сбор погоды завершён.")
    except Exception as error:
        print(f"Ошибка сбора погоды: {error}")


if __name__ == "__main__":
    collect_safely()
    hour = 6
    minutes = 0
    scheduler.add_job(
        collect_safely,
        trigger="cron",
        hour=hour,
        minute=minutes,
        id="daily_weather_collection",
        max_instances=1,
        coalesce=True,
    )

    print(f"Планировщик запущен. Сбор ежедневно в {f'{hour}'*2 if hour < 1 else hour}:{f'0{minutes}' if minutes < 10 else minutes}.")
    scheduler.start()
