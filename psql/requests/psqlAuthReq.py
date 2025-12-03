# Standard imports
from datetime import datetime
import pytz
import uuid

# Custom imports
from psql.config import Logging
from psql.operations import database
from psql.models.auth import profiles, registrations, roles

###################################################################### AUTHENTICATION ######################################################################

class Requests:
    def __init__(self, psql_connection):

        # Logger
        self.logger = Logging.Logger(__name__).get()

        # Initialize database connection
        self.psql_database = database.main(psql_connection.conn)



    ################################################ PROFILES ################################################

    def getProfile(self, unique_identifier: str = None, email: str = None):
        condition_field = "unique_identifier" if unique_identifier else "email"
        query = f"SELECT * FROM profiles WHERE {condition_field} = %s"
        result = self.psql_database.selectOne(query, [str(unique_identifier) if unique_identifier else email])
        if result:
            profileUser = profiles.User(result)
            return profileUser

    def getProfiles(self):
        query = "SELECT * FROM profiles"
        results = self.psql_database.execute(query)
        profileUsers = []
        for result in results:
            profileUser = profiles.User(result)
            profileUsers.append(profileUser)
        return profileUsers
    
    def getActiveProfiles(self):
        query = "SELECT * FROM profiles WHERE status NOT IN ('pending', 'deleted')"
        results = self.psql_database.execute(query)
        profileUsers = []
        for result in results:
            profileUser = profiles.User(result)
            profileUsers.append(profileUser)
        return profileUsers
    
    def getDeleteProfiles(self):
        query = "SELECT * FROM profiles WHERE status = 'deleted'"
        results = self.psql_database.execute(query)
        profileUsers = []
        for result in results:
            profileUser = profiles.User(result)
            profileUsers.append(profileUser)
        return profileUsers

    def createProfile(self, unique_identifier: str, email: str, password: str, firstname: str, lastname: str, role_id: int, status: str, signup_type: str):
        query = "INSERT INTO profiles (unique_identifier, email, password, firstname, lastname, role_id, status, signup_type, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *"
        created_at = datetime.now(pytz.timezone("America/New_York")).strftime("%Y-%m-%d %H:%M:%S")
        result = self.psql_database.execute(query, [unique_identifier, email, password, firstname, lastname, role_id, status, signup_type, created_at])
        if result:
            return profiles.User(result[0])

    def updateProfile(self, profileUser: profiles.User):
        query = """
            UPDATE profiles 
            SET role_id = %s,
                email = %s,
                password = %s,
                firstname = %s,
                lastname = %s,
                status = %s,
                reference_id = %s,
                signup_type = %s
            WHERE unique_identifier = %s
            RETURNING *
        """
        values = [
            profileUser.role_id,
            profileUser.email,
            profileUser.password,
            profileUser.firstname,
            profileUser.lastname,
            profileUser.status,
            profileUser.reference_id,
            profileUser.signup_type,
            profileUser.unique_identifier
        ]
        
        result = self.psql_database.execute(query, values)
        if result:
            return profiles.User(result[0])

    def deleteProfile(self, profileUser: profiles.User):
        query = "DELETE FROM profiles WHERE unique_identifier = %s"
        result = self.psql_database.delete(query, [profileUser.unique_identifier])
        if result:
            return True

    ################################################ REGISTRATIONS ################################################

    def getRegistration(self, unique_identifier: str = None, email: str = None):
        condition_field = "unique_identifier" if unique_identifier else "email"
        query = f"SELECT * FROM registrations WHERE {condition_field} = %s"
        result = self.psql_database.selectOne(query, [unique_identifier if unique_identifier else email])

        if result:
            registrationUser = registrations.User(result)
            return registrationUser

    def getRegistrations(self):
        query = "SELECT * FROM registrations"
        results = self.psql_database.execute(query)
        registrationUsers = []
        for result in results:
            registrationUser = registrations.User(result)
            registrationUsers.append(registrationUser)
        return registrationUsers

    def getInactiveRegistrations(self):
        # This query includes a has_profile that checks if the registration has an associated profile
        query = """
            SELECT r.*,
                p.unique_identifier IS NOT NULL AS has_profile
            FROM registrations r
            LEFT JOIN profiles p
                ON p.unique_identifier = r.unique_identifier
            WHERE r.status IN ('inactive', 'pending', 'revoked');
        """
        results = self.psql_database.execute(query)
        registrationUsers = []
        for result in results:
            registrationUser = registrations.User(result)
            registrationUsers.append(registrationUser)
        return registrationUsers
    
    def createRegistration(self, email: str, firstname: str, lastname: str, status: str, signup_type: str):
        query = "INSERT INTO registrations (unique_identifier, email, firstname, lastname, status, signup_type, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING *"
        unique_identifier = str(uuid.uuid4())
        created_at = datetime.now(pytz.timezone("America/New_York")).strftime("%Y-%m-%d %H:%M:%S")
        result = self.psql_database.execute(query, [unique_identifier, email, firstname, lastname, status, signup_type, created_at])
        if result:
            return registrations.User(result[0])

    def updateRegistration(self, registrationUser: registrations.User):
        query = """
            UPDATE registrations 
            SET email = %s,
                firstname = %s,
                lastname = %s,
                status = %s,
                reference_id = %s,
                signup_type = %s
            WHERE unique_identifier = %s
            RETURNING *
        """
        values = [
            registrationUser.email,
            registrationUser.firstname,
            registrationUser.lastname,
            registrationUser.status,
            registrationUser.reference_id,
            registrationUser.signup_type,
            registrationUser.unique_identifier
        ]
        
        result = self.psql_database.execute(query, values)
        if result:
            return registrations.User(result[0])

    def deleteRegistration(self, registrationUser: registrations.User):
        query = "DELETE FROM registrations WHERE unique_identifier = %s"
        result = self.psql_database.delete(query, [registrationUser.unique_identifier])
        if result:
            return True

    ################################################ ROLES ################################################

    def getRole(self, role_id: int = None, role_name: str = None):
        condition_field = "id" if role_id else "name"
        query = f"SELECT * FROM roles WHERE {condition_field} = %s"
        result = self.psql_database.selectOne(query, [role_id if role_id else role_name])

        if result:
            role = roles.Role(result)
            return role

    def getRoles(self):
        query = "SELECT * FROM roles"
        results = self.psql_database.execute(query)
        allRoles = []
        for result in results:
            role = roles.Role(result)
            allRoles.append(role)
        return allRoles
    
    def updateRole(self, role: roles.Role):
        query = """
            UPDATE roles 
            SET name = %s
            WHERE id = %s
            RETURNING *
        """
        values = [
            role.name,
            role.id
        ]
        result = self.psql_database.execute(query, values)
        if result:
            return roles.Role(result[0])
        
    def createRole(self, role_name: str):
        query = "INSERT INTO roles (name) VALUES (%s) RETURNING *"
        result = self.psql_database.execute(query, [role_name])
        if result:
            return roles.Role(result[0])
        
    def deleteRole(self, role: roles.Role):
        query = "DELETE FROM roles WHERE id = %s"
        result = self.psql_database.delete(query, [role.id])
        if result:
            return True