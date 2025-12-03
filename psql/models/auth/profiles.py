import json
from datetime import datetime

class User:
    def __init__(self, profile_data: dict = None):
        self.id = ""
        self.unique_identifier = ""
        self.role_id = ""
        self.email = ""
        self.password = ""
        self.firstname = ""
        self.lastname = ""
        self.status = ""
        self.reference_id = ""
        self.signup_type = ""
        self.created_at = ""

        if profile_data:
            self.init_properties(profile_data)

    ################################################ FUNCTIONS ################################################

    def init_properties(self, profile_data: dict):
        for key, value in profile_data.items():
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
            'role_id': self.role_id,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'signup_type': self.signup_type,
            'reference_id': self.reference_id
        }

    def getProfileJSON(self, request):
        return {
            'unique_identifier': self.unique_identifier,
            'email': self.email,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'role': request.role,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'signup_type': self.signup_type
        }
