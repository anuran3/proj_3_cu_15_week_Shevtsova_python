import plotly.express as px
import pandas as pd # type: ignore

def create_route_map(locations, weather_data):
    """
    Создает интерактивную карту маршрута с отметками для каждой точки и погодными данными.

    :param locations: Список локаций (например, [{'name': 'Москва', 'latitude': 55.75, 'longitude': 37.61}])
    :param weather_data: Данные о погоде для каждой точки маршрута
    :return: Интерактивная карта с маршрутом
    """
    # Добавляем данные о погоде в локации
    for i, location in enumerate(locations):
        # Используем .get для безопасного получения значений, с установкой значений по умолчанию
        location['temperature'] = weather_data[i].get('temperature', 'N/A')
        location['wind_speed'] = weather_data[i].get('wind_speed', 'N/A')
        location['precipitation_probability'] = weather_data[i].get('precipitation_probability', 'N/A')

    # Преобразуем данные в DataFrame для удобства работы с Plotly
    df = pd.DataFrame(locations)

    # Создаем карту с использованием Plotly Express
    fig = px.scatter_mapbox(
        df,
        lat="latitude",
        lon="longitude",
        hover_name="name",
        hover_data={
            "latitude": False,
            "longitude": False,
            "temperature": True,
            "wind_speed": True,
            "precipitation_probability": True
        },
        mapbox_style="open-street-map",
        zoom=5,
        title="Маршрут с прогнозом погоды"
    )

    # Добавляем линии маршрута, если точек больше одной
    if len(locations) > 1:
        fig.add_trace(
            px.line_mapbox(
                df,
                lat="latitude",
                lon="longitude",
                mapbox_style="open-street-map"
            ).data[0]
        )

    return fig
