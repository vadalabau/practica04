# database.py
import json
import os

class SatelliteDatabase:
    def __init__(self, file_path='data.json'):
        self.file_path = file_path
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump({"satelites": [], "misiones": [], "datos": []}, f, indent=4)

    def load_data(self):
        with open(self.file_path, 'r') as f:
            return json.load(f)

    def save_data(self, data):
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=4)

    def add_satellite(self, sat):
        data = self.load_data()
        data["satelites"].append(sat)
        self.save_data(data)

    def get_satellites(self, filtro=None):
        sats = self.load_data().get("satelites", [])
        if filtro:
            return [s for s in sats if all(s.get(k) == v for k,v in filtro.items())]
        return sats

    def add_mission(self, mission):
        data = self.load_data()
        data["misiones"].append(mission)
        self.save_data(data)

    def get_missions(self, filtro=None):
        misiones = self.load_data().get("misiones", [])
        if filtro:
            return [m for m in misiones if all(m.get(k) == v for k,v in filtro.items())]
        return misiones

    def add_data(self, dato):
        data = self.load_data()
        data["datos"].append(dato)
        self.save_data(data)

    def get_data(self, filtro=None):
        datos = self.load_data().get("datos", [])
        if filtro:
            return [d for d in datos if all(d.get(k) == v for k,v in filtro.items())]
        return datos