
class Record:
    def from_dict(self, dictionary):
        if not dictionary:
            return self

        for key in dictionary:
            if key in self.__dict__:
                setattr(self, key, dictionary[key])
        return self


class City(Record):
    def __init__(self):
        self.title: str = None
        self.woeid: int = 0


class Forecast(Record):
    def __init__(self):
        self.weather_state_name: str = ""
        self.the_temp: float = 0
        self.min_temp: float = 0
        self.max_temp: float = 0
        self.wind_speed: float = 0
        self.humidity: int = 0
        self.air_pressure: float = 0

    def __str__(self):
        return (
            '{weather_state_name} \n'
            'Temp: {the_temp:.2f} °C\n'
            'Min: {min_temp:.2f} °C\n'
            'Max: {max_temp:.2f} °C\n'
            'Wind speed: {wind_speed:.1f} m/s\n'
            'Humidity: {humidity} %\n'
            'Air pressure: {air_pressure:.1f} mbar'
        ).format(**self.__dict__)
