import plotly.express as px
import pandas as pd # type: ignore
from datetime import datetime

def extract_weather_data(raw_weather_data):
    """
    Извлекает и обрабатывает основные параметры погоды для создания графиков.
    
    :param raw_weather_data: Исходные данные о погодных условиях
    :return: Список данных с извлеченными параметрами для дальнейшего использования
    """
    forecasts = raw_weather_data.get('DailyForecasts', [])
    weather_info = []
    
    for forecast in forecasts:
        # Извлекаем данные для каждого прогноза
        forecast_date = forecast.get("Date", "")
        max_temp = forecast.get("Temperature", {}).get("Maximum", {}).get("Value", None)
        wind_speed_value = forecast.get("Day", {}).get("Wind", {}).get("Speed", {}).get("Value", None)
        precip_prob = forecast.get("Day", {}).get("PrecipitationProbability", None)

        # Добавляем обработанные данные в список
        weather_info.append({
            "date": forecast_date,
            "temperature": max_temp,
            "wind_speed": wind_speed_value,
            "precipitation_probability": precip_prob
        })
    
    return weather_info

def generate_weather_plot(weather_data, parameter, chart_type="line"):
    """
    Генерирует график на основе выбранного параметра погоды.

    :param weather_data: Обработанные данные о погоде
    :param parameter: Параметр для отображения ("temperature", "wind_speed", "precipitation_probability")
    :param chart_type: Тип графика ("line" или "bar")
    :return: Построенный график с использованием Plotly
    """
    # Обрабатываем исходные данные
    weather_info = extract_weather_data(weather_data)
    
    # Проверка на наличие данных
    if not weather_info:
        return None

    # Создаем DataFrame из обработанных данных
    df_weather = pd.DataFrame(weather_info)

    # Преобразуем строки с датами в формат datetime для корректного отображения
    df_weather['date'] = pd.to_datetime(df_weather['date'])

    # В зависимости от выбранного параметра создаем нужный график
    if parameter == "temperature":
        if chart_type == "line":
            plot = px.line(df_weather, x="date", y="temperature", title="Температура")
        elif chart_type == "bar":
            plot = px.bar(df_weather, x="date", y="temperature", title="Температура")
    elif parameter == "wind_speed":
        if chart_type == "line":
            plot = px.line(df_weather, x="date", y="wind_speed", title="Скорость ветра")
        elif chart_type == "bar":
            plot = px.bar(df_weather, x="date", y="wind_speed", title="Скорость ветра")
    elif parameter == "precipitation_probability":
        if chart_type == "line":
            plot = px.line(df_weather, x="date", y="precipitation_probability", title="Вероятность осадков")
        elif chart_type == "bar":
            plot = px.bar(df_weather, x="date", y="precipitation_probability", title="Вероятность осадков")
    
    return plot
