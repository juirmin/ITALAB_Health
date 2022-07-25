class FDK300:
    def __init__(self):
        self.mode = "temperature"

    def get_sensor_data(self):
        return {'temperature': 36.8}


class FDK400:
    def __init__(self):
        self.mode = "pressure"

    def get_sensor_data(self):
        return {'pressure_S': 200, 'pressure_D': 100, 'pulse': 100}


class M170:
    def __init__(self):
        self.mode = "oxygen"

    def get_sensor_data(self):
        return {'pulse': 100, 'oxygen': 100, 'pi': 92}


class MTKA1:
    def __init__(self):
        self.mode = "weight"

    def get_sensor_data(self):
        {'weight': 80}
