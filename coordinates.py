import subprocess
from typing import NamedTuple, Literal, TypedDict
from dataclasses import dataclass

# from pympler import asizeof

from exceptions import CantGetCoordinates
import config

# def get_gps_coordinates() -> dict[Literal['latitude'] | Literal['longitude'], float]:
#     return {'latitude': 10.0, 'longitude': 20.0}


# coordinates = get_gps_coordinates()
# print(coordinates['longitude'])


# class Coordinates(TypedDict):
#     latitude: float
#     longitude: float


# def get_gps_coordinates() -> Coordinates:
#     return Coordinates({'latitude': 10.0, 'longitude': 20.0})


# coordinates = get_gps_coordinates()
# print(coordinates['longitude'])


@dataclass
class CoordinatesDT:
    latitude: float
    longitude: float


class CoordinatesNT(NamedTuple):
    latitude: float
    longitude: float


# def get_gps_coordinates() -> Coordinates:
#     return Coordinates(**{'latitude': 10.0, 'longitude': 20.0})


# coordinates = get_gps_coordinates()
# print(coordinates.latitude)


class Coordinates(NamedTuple):
    latitude: float
    longitude: float


command = '''Add-Type -AssemblyName System.Device;
             $GeoWatcher = New-Object System.Device.Location.GeoCoordinateWatcher;
             $GeoWatcher.Start();
             while (($GeoWatcher.Status -ne 'Ready') -and ($GeoWatcher.Permission -ne 'Denied')) {
                 Start-Sleep -Milliseconds 100
             };
             if ($GeoWatcher.Permission -eq 'Denied'){
                 Write-Error 'Access Denied for Location Information'
             } else {
                 $GeoWatcher.Position.Location | Select Latitude,Longitude
             };
'''


def get_coordinates() -> Coordinates:
    """Returns current coordiantes using Windows GPS"""
    coordinates = _get_powershell_coordinates()
    return _round_coordinates(coordinates)


def _get_powershell_coordinates() -> Coordinates:
    powershell_output = _get_powershell_output()
    coordinates = _parse_coordinates(powershell_output)
    return coordinates


def _get_powershell_output() -> subprocess.CompletedProcess:
    completed = subprocess.run(
        ['powershell', command],
        capture_output=True,
        text=True
    )
    if completed.returncode:
        raise CantGetCoordinates(completed.stderr)
    return completed


def _parse_coordinates(completed: subprocess.CompletedProcess) -> Coordinates:
    latitude_longitude = completed.stdout.strip().split('\n')
    keys = latitude_longitude[0].strip().lower().split()
    values = (float(value.replace(',', '.'))
              for value in latitude_longitude[2].strip().split())
    coordinates = Coordinates(**dict(zip(keys, values)))
    return coordinates


def _round_coordinates(coordinates: Coordinates) -> Coordinates:
    if not config.USE_ROUNDED_COORDS:
        return coordinates
    return Coordinates(
        *map(
            lambda c: round(c, 1),
            [coordinates.latitude, coordinates.longitude]
        )
    )


if __name__ == '__main__':
    coordinates = get_coordinates()
    print(coordinates.latitude)
    print(coordinates.longitude)
    # lat, long = get_coordinates()
    # print(lat, long)
    # coordinates_dt = CoordinatesDT(longitude=10.0, latitude=20.0)
    # coordinates_nt = CoordinatesNT(longitude=10.0, latitude=20.0)
    # print('dataclass:', asizeof.asized(coordinates_dt).size)
    # print('dataclass:', asizeof.asized(coordinates_nt).size)
