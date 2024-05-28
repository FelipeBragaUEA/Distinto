import json

class Product:
    def __init__(self, name, serial_number, brand, acquisition_date, creation_date, owner):
        self.name = name
        self.serial_number = serial_number
        self.brand = brand
        self.acquisition_date = acquisition_date
        self.creation_date = creation_date
        self.owner = owner

    def to_json(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def from_json(json_data):
        data = json.loads(json_data)
        return Product(**data)
