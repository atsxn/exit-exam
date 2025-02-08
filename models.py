import json

class DriverModel:
    FILE_PATH = "drivers.json"

    @staticmethod
    def load_data():
        with open(DriverModel.FILE_PATH, "r", encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def save_data(data):
        with open(DriverModel.FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    @staticmethod
    def find_driver(license_no):
        drivers = DriverModel.load_data()
        return next((d for d in drivers if d["license_no"] == license_no), None)
