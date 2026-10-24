import subprocess
import sys
import time
from pathlib import Path
from get_api import get_weather, get_forecast


BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / 'frontend'

city = 'Rostov-on-Don'
language = 'ru'
processes = []

def test_api():
    print('=' * 8 + ' ТЕКУЩАЯ ПОГОДА ' +  '=' * 8)

    data = get_weather(city, language)

    if data is not None:
        print(f'Город: {data["name"]}')
        print(f'Температура: {data["main"]["temp"]} °C')
        print(f'Ощущается как: {data["main"]["feels_like"]} °C')
        print(f'Погода: {data["weather"][0]["description"]}')
        print(f'Влажность: {data["main"]["humidity"]}%')
    else:
        print('Не удалось получить текущую погоду')

    print('=' * 8 + ' ПРОГНОЗ ПОГОДЫ ' +  '=' * 8)

    forecast = get_forecast(city, language)

    if forecast is not None:
        for item in forecast['list'][:5]:
            print(
                f'{item["dt_txt"]}: '
                f'{item["main"]["temp"]} °C, '
                f'{item["weather"][0]["description"]}'
            )
    else:
        print('Не удалось получить прогноз')


def start_process(name, command, cwd):
    print(f'Запуск: {name}')

    process = subprocess.Popen(command, cwd=cwd)
    processes.append((name, process))


def stop_processes():
    print('Остановка проекта...')

    for name, process in reversed(processes):
        if process.poll() is None:
            process.terminate()

    for name, process in processes:
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()

    print('Проект остановлен.')


def start():
    try:
        test_api()

        start_process(
            'FastAPI',
            [
                sys.executable, '-m', 'uvicorn',
                'api:app',
                '--reload'
            ],
            BASE_DIR
        )
        start_process(
            'Планировщик погоды',
            [sys.executable, 'scheduler.py'],
            BASE_DIR
        )

        if sys.platform == 'win32':
            command = ['npm.cmd', 'run', 'dev', '--', '--host', '127.0.0.1']
        else:
            command = ['npm', 'run', 'dev', '--', '--host', '127.0.0.1']

        start_process('Vue', command, FRONTEND_DIR)

        print('=' * 8 + ' ПРОЕКТ ЗАПУЩЕН ' +  '=' * 8)
        print('Сайт: http://localhost:5173')
        print('API: http://127.0.0.1:8000')
        print('Документация: http://127.0.0.1:8000/docs')
        print('Для остановки нажми Ctrl+C')

        while True:
            for name, process in processes:
                if process.poll() is not None:
                    raise RuntimeError(
                        f'Процесс {name} завершился.'
                    )

            time.sleep(1)

    except KeyboardInterrupt:
        pass
    except (OSError, RuntimeError) as error:
        print(f'Ошибка: {error}')
    finally:
        stop_processes()


if __name__ == '__main__':
    start()
