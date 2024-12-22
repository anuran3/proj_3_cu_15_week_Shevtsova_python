import unittest
from met_office import find_location_key, retrieve_weather_data, get_coordinates

class TestWeatherService(unittest.TestCase):
    """
    Класс для юнит-тестирования функций модуля met_office.
    """

    def test_find_location_key(self):
        """
        Тестирование функции find_location_key.
        Проверяет, что функция возвращает ключ локации для города 'London'.
        """
        key = find_location_key("London")
        # Проверяем, что ключ локации не None, если запрос выполнен успешно.
        self.assertIsNotNone(key, "Ключ локации не должен быть None.")

    def test_retrieve_weather_data(self):
        """
        Тестирование функции retrieve_weather_data.
        Проверяет, что функция возвращает данные о погоде для города 'London'.
        """
        key = find_location_key("London")
        self.assertIsNotNone(key, "Не удалось получить ключ локации для 'London'.")
        
        weather_data = retrieve_weather_data(key)
        # Проверяем, что данные о погоде не пустые.
        self.assertIsNotNone(weather_data, "Данные о погоде не должны быть None.")
        self.assertIn('DailyForecasts', weather_data, "Данные о погоде должны содержать 'DailyForecasts'.")

    def test_get_coordinates(self):
        """
        Тестирование функции get_coordinates.
        Проверяет, что функция возвращает координаты для города 'London',
        и что возвращаемые координаты имеют правильную структуру.
        """
        coord = get_coordinates("London")
        # Проверяем, что координаты не пустые.
        self.assertIsNotNone(coord, "Координаты не должны быть None.")
        # Проверяем, что координаты представлены в виде кортежа.
        self.assertIsInstance(coord, tuple, "Координаты должны быть кортежем.")
        # Проверяем, что кортеж содержит два элемента: широту и долготу.
        self.assertEqual(len(coord), 2, "Координаты должны содержать два элемента.")

if __name__ == '__main__':
    # Запуск тестов
    unittest.main()
