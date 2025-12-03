import json
from datetime import datetime

class User:
    def __init__(self, registration_data: dict = None):
        self.id = ""
        self.email = ""
        self.firstname = ""
        self.lastname = ""
        self.status = ""
        self.reference_id = ""
        self.unique_identifier = ""
        self.created_at = ""
        self.signup_type = ""
        self.has_profile = False

        if registration_data:
            self.init_properties(registration_data)

    ################################################ FUNCTIONS ################################################

    def init_properties(self, registration_data: dict):
        for key, value in registration_data.items():
            setattr(self, key, value)

    ################################################ SETTERS ################################################

    ################################################ GETTERS ################################################

    def getJSON(self):
        return {
            'id': self.id,
            'unique_identifier': self.unique_identifier,
            'email': self.email,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'signup_type': self.signup_type,
            'reference_id': self.reference_id,
            'has_profile': bool(self.has_profile)
        }
        