import requests
import os

# Получаем API ключ из переменной окружения
API_KEY = os.getenv('API')

def find_location_key(location):
    """
    Получает уникальный ключ для локации из API AccuWeather.

    :param location: Название города или локации
    :return: Уникальный ключ локации (если найден) или None
    """
    url = f'http://dataservice.accuweather.com/locations/v1/cities/search?apikey={API_KEY}&q={location}&language=ru-ru'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверяем успешность запроса
        data = response.json()
        if not data:
            return None  # Если данные пусты, возвращаем None
        return data[0]['Key']  # Возвращаем первый найденный ключ локации
    except requests.RequestException as e:
        # Обработка ошибок в запросе
        print(f"Ошибка при получении ключа локации для '{location}': {e}")
        return None

def retrieve_weather_data(location_key):
    """
    Получает данные о погоде для локации по ее уникальному ключу.

    :param location_key: Уникальный ключ локации
    :return: Данные о погоде (JSON) или None, если произошла ошибка
    """
    url = f'http://dataservice.accuweather.com/forecasts/v1/daily/5day/{location_key}?apikey={API_KEY}&language=ru-ru&details=true&metric=true'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверяем успешность запроса
        return response.json()  # Возвращаем данные о погоде
    except requests.RequestException as e:
        # Обработка ошибок в запросе
        print(f"Ошибка при получении данных о погоде для ключа '{location_key}': {e}")
        return None

def fetch_weather_info(weather_data):
    """
    Извлекает основные данные о погоде для каждого дня из полученных данных.

    :param weather_data: Данные о погоде (JSON)
    :return: Список с данными о температуре, ветре и осадках для каждого дня
    """
    daily_forecasts = weather_data.get('DailyForecasts', [])
    weather_info = []
    for forecast in daily_forecasts:
        date = forecast['Date']
        temperature_min = forecast['Temperature']['Minimum']['Value']
        temperature_max = forecast['Temperature']['Maximum']['Value']
        wind_speed = forecast['Day']['Wind']['Speed']['Value']
        precipitation_probability = forecast['Day']['PrecipitationProbability']
        
        weather_info.append({
            'date': date,
            'temperature_min': temperature_min,
            'temperature_max': temperature_max,
            'wind_speed': wind_speed,
            'precipitation_probability': precipitation_probability
        })
    return weather_info

def get_coordinates(location):
    """
    Получает координаты (широту и долготу) локации по ее названию.

    :param location: Название города или локации
    :return: Кортеж с координатами (широта, долгота) или None, если ошибка
    """
    location_key = find_location_key(location)
    if location_key is None:
        return None  # Если не удалось получить ключ локации, возвращаем None
    url = f'http://dataservice.accuweather.com/locations/v1/{location_key}?apikey={API_KEY}'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверяем успешность запроса
        data = response.json()
        # Возвращаем координаты
        return (data['GeoPosition']['Latitude'], data['GeoPosition']['Longitude'])
    except requests.RequestException as e:
        # Обработка ошибок в запросе
        print(f"Ошибка при получении координат для '{location}': {e}")
        return None
