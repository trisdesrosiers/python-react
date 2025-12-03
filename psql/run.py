import sys
import json
sys.path.append("..")

from psql import psqlManager
from models.auth import profiles

def test_connection():
    try:
        manager = psqlManager.Manager(__file__)
        profile = manager.getProfile(email="demo@example.com")
        print(profile.firstname, profile.lastname)

    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_connection()
