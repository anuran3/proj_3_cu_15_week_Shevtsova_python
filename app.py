from flask import Flask, render_template, request
from met_office import find_location_key, retrieve_weather_data, get_coordinates
import os
import plotly.graph_objs as go
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

# Функция для создания карты с маршрутом
def create_map_with_route(coordinates, locations):
    # Преобразуем координаты в формат, подходящий для графика
    route_coordinates = [{"lat": coord[0], "lon": coord[1]} for coord in coordinates]

    # Создаем карту с точками маршрута
    fig = px.scatter_mapbox(
        lat=[coord[0] for coord in coordinates],
        lon=[coord[1] for coord in coordinates],
        hover_name=locations,  # Отображение названий локаций при наведении
        zoom=5,  # Начальный уровень масштабирования
        height=500  # Высота графика
    )

    # Добавляем линию маршрута на карту
    fig.add_trace(go.Scattermapbox(
        mode="lines",  # Режим "линии"
        lon=[coord["lon"] for coord in route_coordinates],
        lat=[coord["lat"] for coord in route_coordinates],
        line=dict(width=2, color="blue"),  # Цвет и толщина линии маршрута
        name="Маршрут"
    ))

    # Настройки отображения карты
    fig.update_layout(
        mapbox_style="open-street-map",  # Используем стиль карты OpenStreetMap
        margin={"r": 0, "t": 0, "l": 0, "b": 0}  # Убираем отступы
    )

    return fig

@app.route('/', methods=['GET', 'POST'])
def index():
    # Обрабатываем POST-запрос, когда пользователь отправляет форму
    if request.method == 'POST':
        # Проверяем, есть ли в форме точки маршрута
        if 'locations' not in request.form:
            return render_template('result.html', error="Ошибка: не указаны точки маршрута.")

        locations = request.form['locations'].splitlines()  # Разделяем введенные локации по строкам
        days = int(request.form['days'])  # Количество дней для прогноза

        weather_data_list = []  # Список для хранения данных о погоде
        coordinates = []  # Список для хранения координат точек маршрута

        # Для каждой локации получаем данные о погоде и координатах
        for location in locations:
            if not location.strip():
                return render_template('result.html', error=f"Ошибка: пустая строка в точках маршрута.")

            original_location = location.strip()  # Убираем пробелы в начале и в конце

            location_key = find_location_key(location)  # Получаем ключ для локации
            if location_key is None:
                return render_template('result.html', error=f"Ошибка: локация '{original_location}' не найдена.")

            weather_data = retrieve_weather_data(location_key)  # Получаем данные о погоде для локации
            if weather_data is None:
                return render_template('result.html', error=f"Ошибка: не удалось получить данные о погоде для локации '{original_location}'.")

            # Ограничиваем количество прогнозов количеством дней, выбранных пользователем
            weather_data['DailyForecasts'] = weather_data['DailyForecasts'][:days]
            weather_data_list.append({
                'location': original_location,  # Добавляем данные о локации
                'data': weather_data
            })
            coord = get_coordinates(location)  # Получаем координаты локации
            if coord:
                coordinates.append(coord)

        graphs = []  # Список для хранения графиков
        # Создаем графики для каждой локации
        for data in weather_data_list:
            forecasts = data['data']['DailyForecasts']
            dates = [forecast['Date'] for forecast in forecasts]
            temps_min = [forecast['Temperature']['Minimum']['Value'] for forecast in forecasts]
            temps_max = [forecast['Temperature']['Maximum']['Value'] for forecast in forecasts]
            precipitation = [forecast['Day']['PrecipitationProbability'] for forecast in forecasts]
            wind_speed = [forecast['Day']['Wind']['Speed']['Value'] for forecast in forecasts]

            # График температуры
            fig_temp = go.Figure()
            fig_temp.add_trace(go.Scatter(x=dates, y=temps_min, mode='lines+markers', name='Min Temp'))
            fig_temp.add_trace(go.Scatter(x=dates, y=temps_max, mode='lines+markers', name='Max Temp'))
            fig_temp.update_layout(title=f"Температура в {data['location']}")

            # График вероятности осадков
            fig_precip = go.Figure()
            fig_precip.add_trace(go.Bar(x=dates, y=precipitation, name='Вероятность осадков'))
            fig_precip.update_layout(title=f"Вероятность осадков в {data['location']}")

            # График скорости ветра
            fig_wind = go.Figure()
            fig_wind.add_trace(go.Scatter(x=dates, y=wind_speed, mode='lines', name='Скорость ветра'))
            fig_wind.update_layout(title=f"Скорость ветра в {data['location']}")

            # Добавляем графики в список
            graphs.append({
                'location': data['location'],
                'temp_graph': pio.to_json(fig_temp),
                'precip_graph': pio.to_json(fig_precip),
                'wind_graph': pio.to_json(fig_wind)
            })

        # Если координаты существуют, создаем карту с маршрутом
        if coordinates:
            fig_map = create_map_with_route(coordinates, locations)
            map_json = pio.to_json(fig_map)  # Преобразуем график карты в формат JSON
        else:
            map_json = None  # Если координат нет, карта не создается

        # Отправляем данные на страницу с результатами
        return render_template('result.html', graphs=graphs, map_json=map_json)

    # Отображаем страницу с формой ввода для запроса
    return render_template('index.html')

# Запуск приложения в режиме отладки
if __name__ == '__main__':
    app.run(debug=True)