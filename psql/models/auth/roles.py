import json
from datetime import datetime

class Role:
    def __init__(self, role_data: dict = None):
        self.id = ""
        self.name = ""

        if role_data:
            self.init_properties(role_data)

    ################################################ FUNCTIONS ################################################

    def init_properties(self, role_data: dict):
        for key, value in role_data.items():
            setattr(self, key, value)

    ################################################ SETTERS ################################################

    ################################################ GETTERS ################################################

    def getJSON(self):
        return {
            'id': self.id,
            'name': self.name
        }

        
        