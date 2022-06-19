from datetime import datetime
from typing import NamedTuple, Literal
from enum import Enum
import json
from json.decoder import JSONDecodeError
import ssl
import urllib.request
from urllib.error import URLError

from coordinates import Coordinates
import config
from exceptions import ApiServiceError


class WeatherType(Enum):
    THUNDERSTORM = 'Гроза'
    DRIZZLE = 'Изморозь'
    RAIN = 'Дождь'
    SNOW = 'Снег'
    CLEAR = 'Ясно'
    FOG = 'Туман'
    CLOUDS = 'Облачно'


# print(WeatherType.RAIN)
# print(WeatherType.RAIN.value)
# print(WeatherType.RAIN.name)


# def print_weather_type(weather_type: WeatherType) -> None:
#     print(weather_type.value)


# print_weather_type(WeatherType.RAIN)
# print(isinstance(WeatherType.RAIN, WeatherType))

# for weather_type in WeatherType:
#     print(weather_type.name, weather_type.value)


# def what_should_i_do(weather_type: WeatherType) -> None:
#     match weather_type:
#         case WeatherType.THUNDERSTORM | WeatherType.RAIN:
#             print('Уф, лучше сиди дома')
#         case WeatherType.CLEAR:
#             print('О, отличная погодка')
#         case _:
#             print('Ну так, выходить можно')


# what_should_i_do(WeatherType.CLOUDS)


Celsius = int


class Weather(NamedTuple):
    temperature: Celsius
    weather_type: WeatherType
    sunrise: datetime
    sunset: datetime
    city: str


def get_weather(coordinates: Coordinates) -> Weather:
    """Requests weather in OpenWeather API and returns it"""
    openweather_response = _get_openweather_response(
        longitude=coordinates.longitude,
        latitude=coordinates.latitude
    )
    weather = _parse_openweather_response(openweather_response)
    return weather
    # return Weather(
    #     temperature=20,
    #     weather_type=WeatherType.CLEAR,
    #     sunrise=datetime.fromisoformat('2022-05-04 04:00:00'),
    #     sunset=datetime.fromisoformat('2022-05-04 20:25:00'),
    #     city='Kyiv',
    # )


def _get_openweather_response(latitude: float, longitude: float) -> str:
    ssl._create_default_https_context = ssl._create_unverified_context
    url = config.OPENWEATHER_URL.format(
        latitude=latitude, longitude=longitude)
    try:
        return urllib.request.urlopen(url).read()
    except URLError:
        raise ApiServiceError


def _parse_openweather_response(openweather_response: str) -> Weather:
    try:
        openweather_dict = json.loads(openweather_response)
    except JSONDecodeError:
        raise ApiServiceError
    return Weather(
        temperature=_parse_temperature(openweather_dict),
        weather_type=_parse_weather_type(openweather_dict),
        sunrise=_parse_sun_time(openweather_dict, 'sunrise'),
        sunset=_parse_sun_time(openweather_dict, 'sunset'),
        city='Kyiv'
    )


def _parse_temperature(openweather_dict: dict) -> Celsius:
    return round(openweather_dict['main']['temp'])


def _parse_weather_type(openweather_dict: dict) -> WeatherType:
    try:
        weather_type_id = str(openweather_dict['weather'][0]['id'])
    except (IndexError, KeyError):
        raise ApiServiceError
    weather_types = {
        '1': WeatherType.THUNDERSTORM,
        '3': WeatherType.DRIZZLE,
        '5': WeatherType.RAIN,
        '6': WeatherType.SNOW,
        '7': WeatherType.FOG,
        '800': WeatherType.CLEAR,
        '80': WeatherType.CLOUDS,
    }
    for _id, _weather_type in weather_types.items():
        if weather_type_id.startswith(_id):
            return _weather_type
    raise ApiServiceError


def _parse_sun_time(
    openweather_dict: dict,
    time: Literal['sunrise'] | Literal['sunset']
) -> datetime:
    return datetime.fromtimestamp(openweather_dict['sys'][time])


if __name__ == '__main__':
    print(get_weather(Coordinates(latitude=50.4, longitude=30.4)))
