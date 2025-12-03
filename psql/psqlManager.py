# Standard imports
from datetime import datetime

# Custom imports
from psql.config import connection, Logging
from psql.requests import psqlAuthReq
from psql.models.auth import profiles, registrations, roles

# Takes all database requests (CRUD) and sorts them into the correct database (psqlAuthReq, psqlSecureMailReq, psqlFeaturesReq)

class Manager:
    def __init__(self, file_name: str):

        # Logger
        self.logger = Logging.Logger(__name__).get()

        # Initialize PSQL connections
        self.auth_connection = connection.main()
        self.auth_connection.connect("project1")

        # Requests manager
        self.auth_manager = psqlAuthReq.Requests(self.auth_connection)

        self.logger.info(f"PsqlManager initialized for: {file_name}")


    def close(self):
        self.auth_connection.close()


###################################################################### AUTHENTICATION ######################################################################


    ################################################ PROFILES ################################################

    def getProfile(self, unique_identifier: str = None, email: str = None):
        if not unique_identifier and not email:
            raise ValueError("No unique identifier or email provided")
            
        return self.auth_manager.getProfile(unique_identifier, email)

    def getProfiles(self):
        return self.auth_manager.getProfiles()

    def getActiveProfiles(self):
        return self.auth_manager.getActiveProfiles()

    def getDeleteProfiles(self):
        return self.auth_manager.getDeleteProfiles()

    def createProfile(self, unique_identifier: str, email: str, password: str, firstname: str, lastname: str, role_id: int, status: str, signup_type: str):
        # Create the profile
        profile = self.auth_manager.createProfile(unique_identifier, email, password, firstname, lastname, role_id, status, signup_type)
        
        # Automatically create default user settings for the new profile
        if profile:
            try:
                self.createUserSettings(profile.unique_identifier)
                self.logger.info(f"Created default user settings for profile: {profile.unique_identifier}")
            except Exception as e:
                self.logger.error(f"Failed to create user settings for profile {profile.unique_identifier}: {str(e)}")
                # Don't fail the profile creation if user settings creation fails
        
        return profile

    ################################################ REGISTRATIONS ################################################

    def getRegistration(self, unique_identifier: str = None, email: str = None):
        if not unique_identifier and not email:
            raise ValueError("No unique identifier or email provided")
            
        return self.auth_manager.getRegistration(unique_identifier, email)

    def getRegistrations(self):
        return self.auth_manager.getRegistrations()

    def getInactiveRegistrations(self):
        return self.auth_manager.getInactiveRegistrations()

    def createRegistration(self, email: str, firstname: str, lastname: str, status: str, signup_type: str):
        return self.auth_manager.createRegistration(email, firstname, lastname, status, signup_type)

    ################################################ ROLES ################################################

    def getRole(self, role_id: int = None, role_name: str = None):
        if not role_id and not role_name:
            raise ValueError("No role id or role name provided")
            
        return self.auth_manager.getRole(role_id, role_name)

    def getRoles(self):
        return self.auth_manager.getRoles()

    def createRole(self, role_name: str):
        return self.auth_manager.createRole(role_name)

    ###################################################################### UPDATES ######################################################################

    def update(self, model_object: object, document_requests : list = None):
        if isinstance(model_object, profiles.User):
            return self.auth_manager.updateProfile(model_object)
        elif isinstance(model_object, registrations.User):
            return self.auth_manager.updateRegistration(model_object)
        elif isinstance(model_object, roles.Role):
            return self.auth_manager.updateRole(model_object)
        
        
    
###################################################################### DELETES ######################################################################

    def delete(self, model_object: object):
        if isinstance(model_object, profiles.User):
            return self.auth_manager.deleteProfile(model_object)
        elif isinstance(model_object, registrations.User):
            return self.auth_manager.deleteRegistration(model_object)
        elif isinstance(model_object, roles.Role):
            return self.auth_manager.deleteRole(model_object)
