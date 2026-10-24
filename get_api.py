import requests
from dotenv import dotenv_values


config = dotenv_values('.env.my') #for use
# config = 'put_here_api_from_openweathermap' #for tests
API_KEY = config.get('API_KEY')


def _get_data(endpoint: str, city: str, language: str):
    if not API_KEY:
        print('Ошибка: API_KEY не найден в файле .env.my')
        return None

    url = f'https://api.openweathermap.org/data/2.5/{endpoint}'

    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric',
        'lang': language
    }

    try:
        response = requests.get(
            url=url,
            params=params,
            timeout=5
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as error:
        print(f'HTTP ошибка при запросе погоды для {city}: {error}')
    except requests.exceptions.ConnectionError:
        print(f'Нет соединения при запросе погоды для {city}')
    except requests.exceptions.Timeout:
        print(f'Истекло время ожидания ответа для {city}')
    except requests.exceptions.RequestException as error:
        print(f'Ошибка запроса для {city}: {error}')

    return None


def get_weather(city: str, language: str = 'ru'):
    return _get_data('weather', city, language)


def get_forecast(city: str, language: str = 'ru'):
    return _get_data('forecast', city, language)


if __name__ == '__main__':
    city = 'Rostov-on-Don'

    data = get_weather(city)

    if data:
        print(f'Город: {data["name"]}')
        print(f'Температура: {data["main"]["temp"]} °C')
        print(f'Погода: {data["weather"][0]["description"]}')

    forecast = get_forecast(city)

    if forecast:
        print(f'Количество прогнозов: {len(forecast["list"])}')