import requests
from dotenv import dotenv_values

config = dotenv_values('.env.my')

city = 'Rostov-on-Don'
language = 'ru'

API_KEY = config['API_KEY']


def get_weather(city: str, language: str = 'ru'):
    url = 'https://api.openweathermap.org/data/2.5/weather'

    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric',
        'lang': language
    }

    try:
        response = requests.get(url=url, params=params, timeout=5)
        response.raise_for_status()

        return response.json()

    except requests.exceptions.HTTPError as errh:
        print('HTTP ошибка:', errh)
    except requests.exceptions.ConnectionError as errc:
        print('Ошибка соединения:', errc)
    except requests.exceptions.Timeout as errt:
        print('Таймаут:', errt)
    except requests.exceptions.RequestException as err:
        print('Другая ошибка:', err)

    return None


def get_forecast(city: str, language: str = 'ru'):
    url = 'https://api.openweathermap.org/data/2.5/forecast'

    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric',
        'lang': language
    }

    try:
        response = requests.get(url=url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        print(data)
        return data

    except requests.exceptions.HTTPError as errh:
        print('HTTP ошибка:', errh)
    except requests.exceptions.ConnectionError as errc:
        print('Ошибка соединения:', errc)
    except requests.exceptions.Timeout as errt:
        print('Таймаут:', errt)
    except requests.exceptions.RequestException as err:
        print('Другая ошибка:', err)

    return None


if __name__ == '__main__':
    get_weather(city, language)
    get_forecast(city, language)
