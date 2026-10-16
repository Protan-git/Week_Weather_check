from get_api import get_weather, get_forecast
import gui_part


city = 'Rostov-on-Don'
language = 'ru'


def test_api():
    print('========== ТЕКУЩАЯ ПОГОДА ==========')

    data = get_weather(city, language)

    if data is not None:
        print(f'Город: {data["name"]}')
        print(f'Температура: {data["main"]["temp"]} °C')
        print(f'Ощущается как: {data["main"]["feels_like"]} °C')
        print(f'Погода: {data["weather"][0]["description"]}')
        print(f'Влажность: {data["main"]["humidity"]}%')
    else:
        print('Не удалось получить текущую погоду')

    print('========== ПРОГНОЗ ПОГОДЫ ==========')

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


def start():
    test_api()

    print('\n========== ЗАПУСК САЙТА ==========')
    gui_part.start()


if __name__ == '__main__':
    start()
